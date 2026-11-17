import re
from re import*
import json,ipaddress
import requests

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
def is_private_ip(ip):#判断内网IP:IPv4私有/环回/链路本地与IPv6 ULA/环回均视为内网
	try:
		a=ipaddress.ip_address(ip)
		return a.is_private or a.is_loopback or a.is_link_local
	except ValueError:
		return False

def query_ip_location(ip,timeout=5):#统一IP属地查询:内网直接返回内网IP;公网查ip-api.com,返回JSON
	if is_private_ip(ip):
		return{"ip":ip,"内网":True,"ip-api.com":"内网IP"}
	res={"ip":ip,"内网":False}
	try:
		j=None
		for _ in range(2):#偶发超时自动重试一次
			try:
				j=json.loads(requests.get(f"http://ip-api.com/json/{ip}?lang=zh-CN",timeout=timeout).text)
				break
			except Exception:
				continue
		res["ip-api.com"]=f"{j.get('country','未知')}-{j.get('regionName','未知')}-{j.get('city','未知')}"if j and j.get("status")=="success"else"查询失败"
	except Exception as e:
		res["ip-api.com"]=f"查询失败:{str(e)[:50]}"
	return res
