'''
输入pcap文件，输出如下：
1.一个大字典，里面是一个个字典，每个小字典表示两个ip之间的交互（大字典的键就是双方IP,注意，不包括端口号）
2.小字典里有各种键，记载了，这两个ip各自的端口号、tcp会话的数目和握手与放手完整度；
3.小字典里有一个列表，里面是小小字典，里面记载了，发送方连续发送了几个报文，平均报文数据量和平均延迟是多少，如果双方之间收发关系变化（接收方返回了报文的话）就新开一个小小字典到这个列表里，如果只是换了ip则仅是修改该ip对应的其它字典
4.最多涉及30个IP,用户也可以对其修改，但太多的话分析就太费劲了
'''

import sys
from scapy.all import *
from collections import defaultdict

def analyze_pcap(path):
	"""从pcap提取IP对交互统计"""
	packets=rdpcap(path)
	sessions=defaultdict(lambda:{
		'双方端口':{'源端口集':set(),'目的端口集':set()},
		'TCP会话数':0,'三次握手完成':False,'四次挥手完成':False,
		'突发传输段':[]
	})
	burst_state={}
	seen_ips=set()
	max_ips=30
	for pkt in packets:
		if not pkt.haslayer(IP) or not pkt.haslayer(TCP):continue
		ip=pkt[IP];tcp=pkt[TCP]
		src_ip,dst_ip=ip.src,ip.dst
		if src_ip not in seen_ips or dst_ip not in seen_ips:
			new_ips={src_ip,dst_ip}-seen_ips
			if len(seen_ips)+len(new_ips)>max_ips:continue
			seen_ips.update(new_ips)
		src,dst=sorted([src_ip,dst_ip]);key=f"{src}-{dst}";ses=sessions[key]
		ses['双方端口']['源端口集'].add(tcp.sport if src_ip==src else tcp.dport)
		ses['双方端口']['目的端口集'].add(tcp.dport if src_ip==dst else tcp.sport)
		if tcp.flags&0x02:ses['三次握手完成']=True
		if tcp.flags&0x01:ses['四次挥手完成']=True
		ses['TCP会话数']+=1
		sender=src_ip;recver=dst_ip;bid=(sender,recver)
		if bid not in burst_state:
			burst_state[bid]={'计数':0,'总字节':0,'首次时间':pkt.time,'末次时间':pkt.time}
		bs=burst_state[bid];bs['计数']+=1;bs['总字节']+=len(pkt);bs['末次时间']=pkt.time
		if len(ses['突发传输段'])==0 or ses['突发传输段'][-1]['发送方']!=sender:
			ses['突发传输段'].append({'发送方':sender,'报文数':0,'平均载荷字节':0,'平均间隔秒':0})
		cb=ses['突发传输段'][-1];cb['报文数']=bs['计数'];cb['平均载荷字节']=round(bs['总字节']/bs['计数'],2)
		cb['平均间隔秒']=round((bs['末次时间']-bs['首次时间'])/(bs['计数']-1),4) if bs['计数']>1 else 0.0
		if sender!=recver and (recver,sender) in burst_state:del burst_state[(recver,sender)]
	return dict(sessions)

if __name__=='__main__':
	if len(sys.argv)<2:print("用法:python脚本.py <pcap文件>",file=sys.stderr);sys.exit(1)
	result=analyze_pcap(sys.argv[1]);import json;print(json.dumps(result,ensure_ascii=False,default=str))