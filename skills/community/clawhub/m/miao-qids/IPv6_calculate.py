import re
from re import*

def ipv6_to_int(ipv6_str):
	if'::'in ipv6_str:
		parts=ipv6_str.split(':')
		missing=8-len([p for p in parts if p])
		expanded=[]
		for p in parts:
			if p:expanded.append(p)
			else:expanded.extend(['0']*missing)
		ipv6_str=':'.join(expanded)
	parts=[int(p,16)for p in ipv6_str.split(':')]
	return sum(parts[i]<<(112-16*i)for i in range(8))

def int_to_ipv6(ip_int):
	parts=[(ip_int>>(112-16*i))&0xFFFF for i in range(8)]
	return':'.join(f'{p:04x}'for p in parts)

def get_ipv6_common_prefix(ipv6_list):
	if not ipv6_list:return"::/128"
	bin_strings=[bin(ipv6_to_int(ip))[2:].zfill(128)for ip in ipv6_list]
	common_prefix_len=0
	for i in range(128):
		if all(bs[i]==bin_strings[0][i]for bs in bin_strings):
			common_prefix_len=i+1
		else:break
	network_int=ipv6_to_int(ipv6_list[0])&(0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF<<(128-common_prefix_len))
	return int_to_ipv6(network_int)+f'/{common_prefix_len}'

def smart_ipv6_aggregation(ip_ints):
	if len(ip_ints)==1:return int_to_ipv6(ip_ints[0])+"/128"
	first_32bits=[ip>>96 for ip in ip_ints]
	if len(set(first_32bits))==1:
		if first_32bits[0]in[0x20010db8,0xfc00,0xfd00]:
			return get_ipv6_common_prefix([int_to_ipv6(ip)for ip in ip_ints])
		else:
			min_ip,max_ip=min(ip_ints),max(ip_ints)
			diff=min_ip^max_ip
			mask_bits=64
			while diff>0 and mask_bits>48:
				mask_bits-=1
				diff>>=1
			network_ip=min_ip&(0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF<<(128-mask_bits))
			return int_to_ipv6(network_int)+f'/{mask_bits}'
	else:
		return"2000::/3"

def is_ipv6_in_network(ipv6_str,network_str):
	"""检查IPv6地址是否在指定网络内"""
	if'/'not in network_str:return False
	network_ip,mask=network_str.split('/')
	mask=int(mask)
	ip_int=ipv6_to_int(ipv6_str)
	network_int=ipv6_to_int(network_ip)
	mask_int=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF<<(128-mask)
	return(ip_int&mask_int)==(network_int&mask_int)