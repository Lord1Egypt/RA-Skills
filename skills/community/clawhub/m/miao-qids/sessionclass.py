import os,re,sys
import numpy as np
from math import*
from scapy.all import*
from scapy.layers.http import*
from scapy.layers.ssh import*
from scapy.layers.tls.all import*
from scapy.layers.dns import DNS
from scapy.layers.inet6 import IPv6
from scapy.contrib.ospf import OSPF_Hdr
from collections import defaultdict

def safe_log(x):return log(x+1e-10)
def safe_log2(x):return log2(x+1e-10)

def safe_sigmoid(x,scale=1.0):
	v=scale*x
	if scale*x>600:return 1
	elif scale*x<-600:return 0
	else:return 1/(1+exp(-v))

class AccessSession:
	def __init__(self,id,net_packages_in=[]):
		self.id=id
		self.net_packages,self.netextend_packages,self.trans_packages,self.app_packages=[],[],[],[]
		self.timesequence=[]
		self.represent_socket=[]
		self.srcIP_vector,self.destIP_vector=[],[]
		self.transProtocolType_vector,self.TTL_vector,self.NetSize_vector=[],[],[]
		self.IPFragId_vector,self.IPMF_vector,self.IPFragOffset_vector=[],[],[]
		self.srcPort_vector,self.destPort_vector=[],[]
		self.TCPseq_vector,self.TCPack_vector=[],[]
		self.TCPoffset_vector,self.TCPControl_vector,self.TCPwindow_vector=[],[],[]
		self.dataInforEntropy_vector,self.printableByteRate_vector=[],[]
		self.ByteAverage_vector,self.ByteStandDev_vector,self.emptyByteRate_vector=[],[],[]
		self.LongestRunsLength_vector,self.base_Property_matrix=[],[]
		self.load_netPackages(net_packages_in)
	
	def load_netPackages(self,net_packages_in):
		self.net_packages+=net_packages_in
		netextend_packages,trans_packages,app_packages=[],[],[]
		first_time=self.net_packages[0].time if self.net_packages else 0
		self.timesequence=[first_time]
		self.timesequence+=[safe_log2(p.time-first_time)for p in net_packages_in[1:]if p.time>first_time]
		for net_package in net_packages_in:
			netextend_packages.append(get_netextendLayer_fromIPPackage(net_package)[0])
		for net_package in net_packages_in:
			trans_packages.append(get_transmissionLayer_fromIPPackage(net_package)[0])
		for trans_package in trans_packages:
			app_packages.append(get_appLayer_fromTransmissionPackage(trans_package)[0])
		self.netextend_packages+=netextend_packages
		self.trans_packages+=trans_packages
		self.app_packages+=app_packages
		self.load_basePropertys(net_packages_in,trans_packages,app_packages)
	
	def load_basePropertys(self,net_packages_in,trans_packages,app_packages):
		for p in net_packages_in:
			if p.haslayer(IP):
				self.srcIP_vector.append(p[IP].src)
				self.destIP_vector.append(p[IP].dst)
				self.transProtocolType_vector.append(p[IP].proto)
				self.TTL_vector.append(p[IP].ttl)
				self.NetSize_vector.append(p[IP].len)
				self.IPFragId_vector.append(p[IP].id)
				self.IPMF_vector.append(int(p[IP].flags.MF))
				self.IPFragOffset_vector.append(p[IP].frag)
			elif p.haslayer(IPv6):
				self.srcIP_vector.append(p[IPv6].src)
				self.destIP_vector.append(p[IPv6].dst)
				self.transProtocolType_vector.append(p[IPv6].nh)
				self.TTL_vector.append(p[IPv6].hlim)
				self.NetSize_vector.append(len(p))
				self.IPFragId_vector.append(0)
				self.IPMF_vector.append(0)
				self.IPFragOffset_vector.append(0)
		ports=[getportfrompackage(p)for p in trans_packages]
		self.srcPort_vector+=[x[0]for x in ports]
		self.destPort_vector+=[x[1]for x in ports]
		self.TCPseq_vector+=[p.seq if p.haslayer(TCP)else 0 for p in trans_packages]
		self.TCPack_vector+=[p.ack if p.haslayer(TCP)else 0 for p in trans_packages]
		self.TCPoffset_vector+=[p.dataofs if p.haslayer(TCP)else 0 for p in trans_packages]
		self.TCPControl_vector+=[int(p.flags) if p.haslayer(TCP)else 0 for p in trans_packages]
		self.TCPwindow_vector+=[p.window if p.haslayer(TCP)else 0 for p in trans_packages]
		self.load_dataInformation_vector(app_packages)
		self.base_Property_matrix=[
			self.transProtocolType_vector,self.TTL_vector,
			self.NetSize_vector,self.IPFragId_vector,self.IPMF_vector,self.IPFragOffset_vector,
			self.TCPoffset_vector,self.TCPControl_vector,self.TCPwindow_vector,
			self.dataInforEntropy_vector,self.printableByteRate_vector,
			self.ByteAverage_vector,self.ByteStandDev_vector,self.emptyByteRate_vector]
	
	def update_represent_socket(self,net_package,sport,dport):
		if len(self.represent_socket)>1024:return
		src_ip=net_package[IP].src if net_package.haslayer(IP)else net_package[IPv6].src if net_package.haslayer(IPv6)else 0
		dst_ip=net_package[IP].dst if net_package.haslayer(IP)else net_package[IPv6].dst if net_package.haslayer(IPv6)else 0
		proto=net_package[IP].proto if net_package.haslayer(IP)else net_package[IPv6].nh if net_package.haslayer(IPv6)else 0
		socket_tuple=(src_ip,dst_ip,sport,dport,proto)
		if socket_tuple not in self.represent_socket:
			self.represent_socket.append(socket_tuple)
	
	def load_dataInformation_vector(self,app_packages_in):
		for app_package in app_packages_in:
			Rawdata=(app_package if isinstance(app_package,bytes)else
				app_package[Raw].load if app_package.haslayer(Raw)else
				app_package.load if hasattr(app_package,'load')and callable(getattr(app_package,'load',None))else
				bytes(app_package))
			if len(Rawdata)==0:
				self.dataInforEntropy_vector.append(0)
				self.printableByteRate_vector.append(0)
				self.ByteAverage_vector.append(0)
				self.ByteStandDev_vector.append(0)
				self.emptyByteRate_vector.append(0)
				self.LongestRunsLength_vector+=[0]*16
				continue
			InformationEntropy=get_InformationEntropyofBytes(Rawdata)
			self.dataInforEntropy_vector.append(safe_sigmoid(InformationEntropy,0.3))
			codetype=get_codetypeofApp_package(app_package)
			printable_rate=get_printableByteRateofBytes(Rawdata,codetype)
			self.printableByteRate_vector.append(printable_rate)
			aver,standDev,emptyByteRate=get_aver_standDev_emptyRate_ofBytes(Rawdata)
			self.ByteAverage_vector.append(safe_sigmoid(aver/255,2.0))
			self.ByteStandDev_vector.append(safe_sigmoid(standDev/255,2.0))
			self.emptyByteRate_vector.append(emptyByteRate)
	
	def get_averagePackageProperty_vector(self):
		if len(self.base_Property_matrix)==0 or any(len(v)==0 for v in self.base_Property_matrix):
			return [0]*14
		avg_vector=[]
		for linenum in range(0,min(14,len(self.base_Property_matrix))):
			v=self.base_Property_matrix[linenum]
			avg_vector.append(sum(v)/len(v)if len(v)>0 else 0)
		if len(avg_vector)<14:avg_vector.extend([0]*(14-len(avg_vector)))
		return avg_vector
	
	def get_extendProperty_vector(self):
		localIPs=[get_if_addr(x)for x in get_if_list()]
		IPPackageNumber=len(self.net_packages)
		IPPackageSizeAvg=sum(self.NetSize_vector)/len(self.NetSize_vector)if self.NetSize_vector else 0
		IPTimesequenceAvg=sum(self.timesequence)/(IPPackageNumber-1)if IPPackageNumber>1 else sum(self.timesequence)if self.timesequence else 0
		IPPackageSizek2=sum([(x-IPPackageSizeAvg)**2 for x in self.NetSize_vector])if self.NetSize_vector else 0
		IPPackageSizek3=sum([(x-IPPackageSizeAvg)**3 for x in self.NetSize_vector])if self.NetSize_vector else 0
		IPPackageSizek4=sum([(x-IPPackageSizeAvg)**4 for x in self.NetSize_vector])if self.NetSize_vector else 0
		IPPackageSizeStandDev=sqrt(IPPackageSizek2)if IPPackageSizek2>0 else 0
		IPTimesequenceStandDev=sqrt(sum([(x-IPTimesequenceAvg)**2 for x in self.timesequence])/len(self.timesequence))if self.timesequence else 0
		
		#使用sigmoid归一化大范围数值
		IPPackageSizeStandDev_norm=safe_sigmoid(IPPackageSizeStandDev/1000,1.0)
		IPTimesequenceStandDev_norm=safe_sigmoid(IPTimesequenceStandDev,0.5)
		
		uploadIPPackageNumber=sum([1 if p.dst in localIPs else 0 for p in self.net_packages])
		downloadIPPackageNumber=sum([1 if p.src in localIPs else 0 for p in self.net_packages])
		uploadIPPackageSize=sum([p.len if p.dst in localIPs else 0 for p in self.net_packages])
		downloadIPPackageSize=sum([p.len if p.src in localIPs else 0 for p in self.net_packages])
		updownload_IPPackageNumberRate=uploadIPPackageNumber/downloadIPPackageNumber if downloadIPPackageNumber>0 else 0.5
		updownload_IPPackageSizeRate=uploadIPPackageSize/downloadIPPackageSize if downloadIPPackageSize>0 else 0.5
		IPPackageSizeSkewness=IPPackageSizek3/(IPPackageSizek2**1.5+1e-10)if IPPackageSizek2>0 else 0
		IPPackageSizeKurtosis=IPPackageSizek4/(IPPackageSizek2**2+1e-10)if IPPackageSizek2>0 else 0
		
		tcp_connections={}
		for p in self.net_packages:
			if p.haslayer(TCP):
				src=p[IP].src if p.haslayer(IP)else p[IPv6].src if p.haslayer(IPv6)else 0
				dst=p[IP].dst if p.haslayer(IP)else p[IPv6].dst if p.haslayer(IPv6)else 0
				sport,dport=p[TCP].sport,p[TCP].dport
				conn_key=(min(src,dst),max(src,dst),min(sport,dport),max(sport,dport))
				if conn_key not in tcp_connections:
					tcp_connections[conn_key]=[]
				tcp_connections[conn_key].append(p[TCP].flags)
		complete_handshakes=0
		for conn_flags in tcp_connections.values():
			flags_str=''.join([str(f)for f in conn_flags])
			if'S'in flags_str and flags_str.count('SA')>=1:complete_handshakes+=1
		tcp_handshake_completeness=complete_handshakes/len(tcp_connections)if tcp_connections else 0
		
		tcp_seq_packets,retransmit_count={},0
		for p in self.net_packages:
			if p.haslayer(TCP):
				src=p[IP].src if p.haslayer(IP)else p[IPv6].src if p.haslayer(IPv6)else 0
				dst=p[IP].dst if p.haslayer(IP)else p[IPv6].dst if p.haslayer(IPv6)else 0
				conn_key=(src,dst,p[TCP].sport,p[TCP].dport)
				seq=p[TCP].seq
				if conn_key not in tcp_seq_packets:
					tcp_seq_packets[conn_key]=set()
				if seq in tcp_seq_packets[conn_key]:
					retransmit_count+=1
				else:
					tcp_seq_packets[conn_key].add(seq)
		total_tcp_packets=sum(len(seq_set)for seq_set in tcp_seq_packets.values())
		tcp_retransmit_rate=retransmit_count/total_tcp_packets if total_tcp_packets>0 else 0
		
		out_of_order_count=0
		for conn_key,seq_set in tcp_seq_packets.items():
			if len(seq_set)>1:
				seq_list=sorted(seq_set)
				for i in range(1,len(seq_list)):
					if seq_list[i]<seq_list[i-1]:out_of_order_count+=1
		tcp_out_of_order_rate=out_of_order_count/total_tcp_packets if total_tcp_packets>0 else 0
		
		TCPwindow_avg=sum(self.TCPwindow_vector)/len(self.TCPwindow_vector)if len(self.TCPwindow_vector)>0 else 0
		TCPwindowStandDev=sqrt(sum([(w-TCPwindow_avg)**2 for w in self.TCPwindow_vector])/len(self.TCPwindow_vector))if self.TCPwindow_vector else 0
		TCPwindowStandDev_norm=safe_sigmoid(TCPwindowStandDev/10000,1.0)
		
		
		
		v=[safe_sigmoid(IPPackageSizeAvg/1500,1.0),safe_sigmoid(IPTimesequenceAvg,0.2),safe_sigmoid(IPPackageNumber/100,0.5),
			safe_sigmoid(IPPackageSizek2/1e6,1.0),safe_sigmoid(IPPackageSizek3/1e9,1.0),safe_sigmoid(IPPackageSizek4/1e12,1.0),
			IPPackageSizeStandDev_norm,IPTimesequenceStandDev_norm,
			safe_sigmoid(uploadIPPackageNumber/50,1.0),safe_sigmoid(downloadIPPackageNumber/50,1.0),
			safe_sigmoid(uploadIPPackageSize/50000,1.0),safe_sigmoid(downloadIPPackageSize/50000,1.0),
			updownload_IPPackageNumberRate,updownload_IPPackageSizeRate,
			safe_sigmoid(IPPackageSizeSkewness,2.0),safe_sigmoid(IPPackageSizeKurtosis,0.5),
			tcp_handshake_completeness,tcp_retransmit_rate,tcp_out_of_order_rate,TCPwindowStandDev_norm]
		
		return v
	
	def get_enhanced_matrix_features(self):
		matrix=self.base_Property_matrix
		n_packets=len(matrix[0])if matrix and len(matrix)>0 else 0
		features=[]
		
		for row in matrix:
			if n_packets>0:
				row_array=np.array(row)
				stats=[np.mean(row_array),np.std(row_array),np.min(row_array),np.max(row_array),np.median(row_array)]
				features.extend([safe_sigmoid(s/1000,1.0)for s in stats])
			else:features.extend([0]*5)
		
		for row in matrix:
			if n_packets>1:
				diffs=np.diff(row)
				features.extend([safe_sigmoid(np.mean(diffs)/100,1.0),safe_sigmoid(np.std(diffs)/100,1.0)])
			else:features.extend([0]*2)
		
		if n_packets>0:
			features.extend([safe_sigmoid(n_packets/100,0.5),safe_sigmoid(safe_log(n_packets),0.5)])
		else:features.extend([0]*2)
		
		return features
	
	def get_selected_features(self,selected_indices):
		all_features=[]
		all_features.extend(self.get_averagePackageProperty_vector())
		all_features.extend(self.get_extendProperty_vector())
		all_features.extend(self.get_averAppDataBytes())
		all_features.extend(self.get_socket_history_sample(100))
		all_features.extend(self.get_enhanced_matrix_features())
		total_features=14+20+512+100+14
		if len(all_features)<total_features:
			all_features.extend([0]*(total_features-len(all_features)))
		selected_feature_vector=[all_features[i]for i in selected_indices if i<len(all_features)]
		return selected_feature_vector
	
	def get_averAppDataBytes(self):
		if len(self.app_packages)==0:return[0]*1500
		target_packets=4
		selected_packets=self.app_packages[:target_packets]if len(self.app_packages)<=target_packets else self._select_important_packets(target_packets)
		sum_vector=[0]*1500
		for packet in selected_packets:
			raw_data=self._extract_raw_data(packet)
			padded_data=list(raw_data[:1500])+[0]*(1500-len(raw_data[:1500]))
			sum_vector=[sum_vector[i]+padded_data[i]for i in range(1500)]
		return[sum_vector[i]/len(selected_packets)/255 for i in range(1500)]
	
	def _select_important_packets(self,target_count):
		scored_packets=[]
		for i,pkt in enumerate(self.app_packages):
			score=self._calculate_packet_importance(pkt,i,len(self.app_packages))
			scored_packets.append((score,pkt))
		scored_packets.sort(key=lambda x:x[0],reverse=True)
		return[pkt for _,pkt in scored_packets[:target_count]]
	
	def _calculate_packet_importance(self,packet,index,total_count):
		raw_data=self._extract_raw_data(packet)
		score=0.0
		score+=min(len(raw_data)/1500,1.0)*0.3
		position=index/total_count
		if position<0.1 or position>0.9:score+=0.4
		elif 0.4<position<0.6:score+=0.2
		if packet.haslayer(TLS):score+=0.5
		elif packet.haslayer(HTTP)and hasattr(packet[HTTP],'Method'):score+=0.4
		if len(raw_data)>0:
			entropy=get_InformationEntropyofBytes(raw_data)
			if 4.0<entropy<7.0:score+=0.3
		return score
	
	def _extract_raw_data(self,packet):
		if isinstance(packet,bytes):return packet
		elif packet.haslayer(Raw):return packet[Raw].load
		elif hasattr(packet,'load')and callable(getattr(packet,'load')):return packet.load
		else:return bytes(packet)
	
	def get_socket_history_sample(self,sample_size=100):
		if not hasattr(self,'represent_socket')or len(self.represent_socket)==0:
			return[0]*sample_size
		socket_features=[]
		for socket in self.represent_socket[:min(20,len(self.represent_socket))]:
			src_ip_hash=hash(socket[0])%1000/1000.0
			dst_ip_hash=hash(socket[1])%1000/1000.0
			sport_norm=socket[2]/65535.0
			dport_norm=socket[3]/65535.0
			proto_norm=socket[4]/255.0
			socket_features.extend([src_ip_hash,dst_ip_hash,sport_norm,dport_norm,proto_norm])
		if len(socket_features)<sample_size:
			socket_features.extend([0]*(sample_size-len(socket_features)))
		else:
			socket_features=socket_features[:sample_size]
		return socket_features

def getportfrompackage(p):
	if p.haslayer(TCP)or p.haslayer(UDP):return p.sport,p.dport
	elif p.haslayer(ICMP):return -4,-4
	elif p.haslayer(ARP):return -2,-2
	elif p.haslayer(RIP):return -3,-3
	elif p.haslayer(OSPF_Hdr):return -5,-5
	else:return 0,0

def get_InformationEntropyofBytes(data):
	byte_frequencies={}
	for thebyte in data:
		byte_frequencies[thebyte]=byte_frequencies.get(thebyte,0)+1
	if len(data)==0:return 0
	InformationEntropy=0
	for freq in byte_frequencies.values():
		prob=freq/len(data)
		InformationEntropy-=prob*safe_log(prob)
	return InformationEntropy

def get_printableByteRateofBytes(data,codetype):
	try:
		printable_count=sum(1 for char in data.decode(codetype,errors='ignore')if char.isprintable())
		return printable_count/len(data)if len(data)>0 else 0
	except:
		return sum(1 for byte in data if 32<=byte<=126 or byte in(9,10,13))/len(data)

def get_aver_standDev_emptyRate_ofBytes(data):
	aver=sum(data)/len(data)
	standDev=sqrt(sum((x-aver)**2 for x in data)/len(data))
	emptyByteRate=sum(1 for x in data if x==0)/len(data)
	return aver,standDev,emptyByteRate

def get_codetypeofApp_package(app_package):
	if isinstance(app_package,bytes):return 'utf-8'
	if app_package.haslayer(HTTP):
		for attr_name in ['Content_Type','content_type']:
			if hasattr(app_package,attr_name):
				content_type_attr=getattr(app_package,attr_name)
				content_type=(content_type_attr.decode('utf-8','ignore').lower()
					if isinstance(content_type_attr,bytes)
					else str(content_type_attr).lower())
				if'charset='in content_type:
					charset=content_type.split('charset=')[1].split(';')[0].strip()
					if charset in['utf-8','gbk','gb2312','iso-8859-1','ascii']:return charset
	return 'utf-8'

def get_transmissionLayer_fromIPPackage(net_package):
	trans_protocoltypes=[TCP,UDP]
	for trans_protocoltype in trans_protocoltypes:
		if net_package.haslayer(trans_protocoltype):return net_package[trans_protocoltype],True
	return net_package.payload,False

def get_netextendLayer_fromIPPackage(net_package):
	netextend_protocoltypes=[ICMP,OSPF_Hdr,RIP]
	for trans_protocoltype in netextend_protocoltypes:
		if net_package.haslayer(trans_protocoltype):return net_package[trans_protocoltype],True
	return net_package.payload,False

def get_appLayer_fromTransmissionPackage(trans_package):
	app_protocoltypes=[HTTP,TFTP,DNS,SSH,TLS]
	for app_protocoltype in app_protocoltypes:
		if trans_package.haslayer(app_protocoltype):return trans_package[app_protocoltype],True
	return trans_package.payload,False
