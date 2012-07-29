
#
# bignum.py
#
# Distributed under the MIT/X11 software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
#

import struct

def bn_bytes(v, have_ext=False):
	ext = 0
	if have_ext:
		ext = 1
	return ((v.bit_length()+7)/8) + ext

def bn2bin(v):
	s = bytearray()
	i = bn_bytes(v)
	while i > 0:
		s.append((v >> ((i-1) * 8)) & 0xff)
		i -= 1
	return s

def bin2bn(s):
	l = 0L
	for ch in s:
		l = (l << 8) | ord(ch)
	return l

def bn2mpi(v):
	have_ext = False
	if v.bit_length() > 0:
		have_ext = (v.bit_length() & 0x07) == 0

	neg = False
	if v < 0:
		neg = True
		v = -v

	s = struct.pack(">I", bn_bytes(v, have_ext))
	ext = bytearray()
	if have_ext:
		ext.append(0)
	v_bin = bn2bin(v)
	if neg:
		if have_ext:
			ext[0] |= 0x80
		else:
			v_bin[0] |= 0x80
	return s + ext + v_bin

def mpi2bn(s):
	if len(s) < 4:
		return None
	v_len = struct.unpack(">I", s)[0]
	if len(s) != (v_len + 4):
		return None
	if v_len == 0:
		return 0L

	v_str = s[4:]
	neg = False
	i = ord(v_str[0])
	if i & 0x80:
		neg = True
		i &= ~0x80
		v_str[0] = chr(i)

	v = bin2bn(v_str)

	if neg:
		return -v
	return v


