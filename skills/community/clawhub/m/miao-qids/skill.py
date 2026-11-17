import sys,os,json,time,threading,socket,logging,argparse
sys.path.append('.')
from http.server import HTTPServer,BaseHTTPRequestHandler
import socketserver
from urllib.parse import urlparse,parse_qs
import numpy as np,pandas as pd,requests
from scapy.all import rdpcap,IP
import torch
from CNNmodel import CNN_MTD
from fileload import FileLoader,attacktypes
from QNNmodel import QNN_MTD
from pcap_analysis import analyze_pcap as pcap_analyze

#设置日志
logging.basicConfig(level=logging.INFO,format='[%(asctime)s]%(levelname)s:%(message)s')
logger=logging.getLogger(__name__)

def reduce_false_positive(probs,boost=1.25):#调高善意流量置信度后重新归一化以降误报
	p=np.asarray(probs,dtype=float).copy()
	p[attacktypes.index("善意流量")]*=boost
	s=p.sum()
	if s>0:p=p/s
	return p

class IDSDetector:
	def __init__(self,model_dir=None,cache_dir=None,quantum_shots=512,enable_ip_query=True):#初始化检测器
		self.cache_dir=cache_dir or(os.path.join(model_dir,"feature_cache")if model_dir else"./feature_cache")
		self.quantum_shots=quantum_shots
		self.enable_ip_query=enable_ip_query
		logger.info(f"初始化IDS检测器,量子测量次数:{quantum_shots},属地查询:{'开启'if enable_ip_query else'关闭'}")
		self.model_dir=model_dir or os.path.dirname(os.path.abspath(__file__))
		self.cnn_model=None
		self.qnn_model=None
		self.file_loader=None
		self.load_models()
		self.setup_ip_resolver()
		logger.info("IDS检测器初始化完成")
	
	def setup_ip_resolver(self):#设置IP解析器
		self.local_ip=self.get_local_ip()
		self.ip_cache={}
		logger.info(f"本机IP:{self.local_ip}")
	
	def get_local_ip(self):#获取本机IP
		try:
			s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
			s.connect(("8.8.8.8",80))
			local_ip=s.getsockname()[0]
			s.close()
			return local_ip
		except:
			return"未知"
	
	def load_models(self):#加载模型
		try:
			cnn_path=os.path.join(self.model_dir,"cnn_mtd_final.pth")
			qnn_path=os.path.join(self.model_dir,"qnn_model.pkl")
			if not os.path.exists(cnn_path):
				qnn_search=[f for f in os.listdir(self.model_dir)if f.startswith('best_freeze_')and f.endswith('.pkl')]
				if qnn_search:
					qnn_search.sort(reverse=True)
					qnn_path=os.path.join(self.model_dir,qnn_search[0])
			if not os.path.exists(cnn_path):
				raise FileNotFoundError(f"经典部分模型文件不存在:{cnn_path}")
			if not os.path.exists(qnn_path):
				raise FileNotFoundError(f"量子部分模型文件不存在:{qnn_path}")
			self.cnn_model=CNN_MTD.load_model(cnn_path)
			self.cnn_model.eval()
			self.qnn_model=QNN_MTD(qbits_num=8,layers_num=3,data_num_per_qbit=8)
			if not self.qnn_model.load_model(qnn_path):
				raise RuntimeError("QNN模型加载失败")
			self.qnn_model.freeze_parameters(mode='alternate')
			os.makedirs(self.cache_dir,exist_ok=True)
			self.file_loader=FileLoader(use_cache=True,cache_dir=self.cache_dir)
			logger.info(f"模型加载成功:经典部分{self.cnn_model.latent_dim}维,量子部分{self.qnn_model.total_params}参数")
		except Exception as e:
			logger.error(f"模型加载失败:{e}")
			raise
	
	def extract_ips_from_pcap(self,pcap_path,target_ip):#从PCAP提取IP
		try:
			logger.info(f"解析PCAP文件:{pcap_path}")
			packets=rdpcap(pcap_path)
			target_ips=set([target_ip])if target_ip else set()
			if self.local_ip!="未知":target_ips.add(self.local_ip)
			src_ips,dst_ips=set(),set()
			attack_targets=set()
			for pkt in packets:
				if IP in pkt:
					src,dst=pkt[IP].src,pkt[IP].dst
					src_ips.add(src)
					dst_ips.add(dst)
					if dst in target_ips:attack_targets.add(dst)
			suspicious_attackers=src_ips-attack_targets
			suspicious_attackers={ip for ip in suspicious_attackers if not self.is_private_ip(ip)}
			attackers=list(suspicious_attackers)[:10]
			return list(attack_targets),attackers
		except Exception as e:
			logger.error(f"PCAP解析失败:{e}")
			return[],[]
	
	def is_private_ip(self,ip):#判断是否为私有IP
		try:
			parts=list(map(int,ip.split('.')))
			if parts[0]==10:return True
			if parts[0]==172 and 16<=parts[1]<=31:return True
			if parts[0]==192 and parts[1]==168:return True
			return False
		except:
			return False
	
	def ip_query(self,ip):#查询IP属地(委托IPv6_calculate双接口JSON;内网直接返回内网IP;可由--no-ip-query整体关闭)
		if not self.enable_ip_query:return{"ip":ip,"属地查询":"未启用"}
		if ip in self.ip_cache:return self.ip_cache[ip]
		from IPv6_calculate import query_ip_location
		try:
			result=query_ip_location(ip)
		except Exception as e:
			result={"ip":ip,"查询失败":str(e)[:50]}
		self.ip_cache[ip]=result
		return result
	
	def analyze_pcap(self,pcap_path,target_ip):#分析PCAP文件
		start_time=time.time()
		logger.info(f"开始分析PCAP:{pcap_path},目标IP:{target_ip}")
		try:
			#IP分析
			logger.info("阶段1:IP地址分析...")
			target_ips,attacker_ips=self.extract_ips_from_pcap(pcap_path,target_ip)
			ip_results={
				"target_ips":[{"ip":ip,"location":self.ip_query(ip)}for ip in target_ips],
				"attacker_ips":[{"ip":ip,"location":self.ip_query(ip)}for ip in attacker_ips]
			}
			pcap_details=self.analyze_pcap_details(pcap_path)
			#特征提取
			logger.info("阶段2:特征提取...")
			feature_vector=None
			for atk_type in attacktypes:
				session,vector=self.file_loader.load_attackFileVector(pcap_path,atk_type,file_id=0,cache_dir=self.cache_dir)
				if vector is not None:
					feature_vector=vector
					break
			if feature_vector is None:
				raise RuntimeError("特征提取失败")
			#经典编码
			logger.info("阶段3:经典编码...")
			vector_tensor=feature_vector.unsqueeze(0).to(self.cnn_model.device)
			with torch.no_grad():
				latent,reconstructed=self.cnn_model.forward(vector_tensor)
			recon_error=float(torch.mean((vector_tensor-reconstructed)**2).item())
			latent_vector=latent.squeeze().cpu().numpy()
			centers=self.cnn_model.centers.detach().cpu().numpy()
			distances=np.linalg.norm(latent_vector-centers,axis=1)
			softmax_probs=np.exp(-distances)/np.sum(np.exp(-distances))
			cnn_class=np.argmax(softmax_probs)
			cnn_confidence=softmax_probs[cnn_class]
			cnn_prediction=attacktypes[cnn_class]if cnn_class<len(attacktypes)else"未知"
			#量子检测
			logger.info("阶段4:量子检测...")
			normalized_to_tanh=np.tanh(latent_vector/2)
			quantum_angles=(normalized_to_tanh+1)/2*(np.pi-(-np.pi))+(-np.pi)
			quantum_angles=np.clip(quantum_angles,-np.pi+1e-6,np.pi-1e-6)
			if len(quantum_angles)!=64:
				if len(quantum_angles)<64:quantum_angles=quantum_angles+[0.0]*(64-len(quantum_angles))
				else:quantum_angles=quantum_angles[:64]
			quantum_probs=self.qnn_model.forward(input_64d=quantum_angles,shots=self.quantum_shots)
			#结果融合
			logger.info("阶段5:结果融合...")
			alpha=0.7
			fused_probs=np.zeros(8)
			for i in range(8):
				cnn_weight=alpha if i==cnn_class else(1-alpha)/(len(attacktypes)-1)
				qnn_weight=quantum_probs[i]
				fused_probs[i]=cnn_weight*cnn_confidence+qnn_weight*(1-cnn_confidence)
			if np.sum(fused_probs)>0:fused_probs=fused_probs/np.sum(fused_probs)
			#调高善意流量置信度后重新归一化,降低误报率
			reduced=reduce_false_positive(fused_probs)
			final_class=np.argmax(reduced)
			final_confidence=reduced[final_class]
			final_prediction=attacktypes[final_class]if final_class<len(attacktypes)else"未知"
			confidence_dict={attacktypes[i]:float(reduced[i])for i in range(len(attacktypes))}
			
			suggestions=self.generate_suggestions(final_prediction,attacker_ips,recon_error)
			processing_time=time.time()-start_time
			result={
				"success":True,
				"final_prediction":final_prediction,
				"final_confidence":float(final_confidence),
				"cnn_prediction":cnn_prediction,
				"cnn_confidence":float(cnn_confidence),
				"reconstruction_error":float(recon_error),
				"confidence_distribution":confidence_dict,
				"ip_analysis":ip_results,
				"pcap_details":pcap_details,
				"suggestions":suggestions,
				"processing_time":processing_time,
				"timestamp":time.time()
			}
			logger.info(f"分析完成:最终预测={final_prediction},置信度={final_confidence*100:.1f}%")
			return result
		except Exception as e:
			logger.error(f"分析失败:{e}")
			return{"success":False,"error":str(e),"timestamp":time.time()}
	
	def analyze_pcap_details(self,pcap_path):#新接口:委托pcap_analysis.py获取IP对交互细节,转JSON可序列化结构
		"""调用 pcap_analysis.py 提取 PCAP 的 IP 对流量交互特征(端口/TCP会话/握手挥手/突发传输),
		将内部 set 转为列表并附统计摘要,供 LLM 理解流量细节。"""
		try:
			if not os.path.exists(pcap_path):
				return{"success":False,"error":f"文件不存在:{pcap_path}"}
			logger.info(f"调用 pcap_analysis 提取流量细节:{pcap_path}")
			raw=pcap_analyze(pcap_path)
			pairs=[];total_tcp=0
			for key,ses in raw.items():
				ports=ses.get('双方端口',{})
				burst=[{'发送方':b.get('发送方'),'报文数':int(b.get('报文数')),
					'平均载荷字节':float(b.get('平均载荷字节')),'平均间隔秒':float(b.get('平均间隔秒'))}
					for b in ses.get('突发传输段',[])]
				total_tcp+=ses.get('TCP会话数',0)
				pairs.append({
					'ip_pair':key,
					'源端口集':sorted(int(p)for p in ports.get('源端口集',set())),
					'目的端口集':sorted(int(p)for p in ports.get('目的端口集',set())),
					'tcp会话数':ses.get('TCP会话数',0),
					'三次握手完成':ses.get('三次握手完成',False),
					'四次挥手完成':ses.get('四次挥手完成',False),
					'突发传输段':burst})
			pairs.sort(key=lambda x:x['tcp会话数'],reverse=True)
			summary={'ip对数量':len(pairs),'tcp会话总数':total_tcp,
				'含完整握手的对':sum(1 for p in pairs if p['三次握手完成']),
				'含完整挥手的对':sum(1 for p in pairs if p['四次挥手完成'])}
			return{"success":True,"pcap_path":pcap_path,"summary":summary,"ip_pairs":pairs}
		except Exception as e:
			logger.error(f"流量细节分析失败:{e}")
			return{"success":False,"error":str(e)}
	
	def generate_suggestions(self,attack_type,attacker_ips,recon_error):#生成建议
		suggestions=[]
		if attack_type=="善意流量":suggestions.append("✓ 流量正常,可放行")
		else:suggestions.append(f"✗ 检测到{attack_type}攻击,建议立即阻断相关连接")
		if attacker_ips:
			for ip_info in attacker_ips[:3]:
				ip=ip_info.get("ip","")
				if ip and not self.is_private_ip(ip):suggestions.append(f"  考虑在防火墙屏蔽IP:{ip}")
		if recon_error<0.01:suggestions.append("✓ 模型重建质量良好,检测结果可靠")
		elif recon_error<0.05:suggestions.append("⚠ 模型重建质量一般,建议结合其他日志分析")
		else:suggestions.append("✗ 模型重建质量较差,可能为未知攻击类型,建议人工分析")
		attack_specific={
			"端口扫描":["检查防火墙规则","分析端口扫描范围和频率"],
			"SSH暴力破解":["修改SSH密码","限制SSH访问IP","启用双因素认证"],
			"FTP暴力破解":["禁用匿名FTP","修改FTP密码","限制FTP访问IP"],
			"拒绝服务攻击":["启用DDoS防护","增加带宽容量","与ISP协调"],
			"SQL注入":["检查Web应用日志","更新SQL注入防护规则","参数化查询"],
			"XSS":["检查用户输入过滤","更新XSS防护规则","内容安全策略"],
			"WebShell":["检查Web目录","查找后门文件","更新Web应用"]
		}
		if attack_type in attack_specific:suggestions.extend(attack_specific[attack_type])
		return suggestions

class MCPRequestHandler(BaseHTTPRequestHandler):
	protocol_version='HTTP/1.1'
	def __init__(self,request,client_address,server):
		self.detector=server.detector
		self.allowclients=[line.strip()for line in open('allowclients.txt','r').readlines()]
		super().__init__(request,client_address,server)
	
	def do_GET(self):#处理GET请求
		parsed_path=urlparse(self.path)
		if parsed_path.path=='/health':
			self.send_response(200)
			self.send_header('Content-Type','application/json')
			
			for allowclient in self.allowclients:self.send_header('Access-Control-Allow-Origin',allowclient)
			
			self.end_headers()
			response={"status":"ok","service":"量子IDS检测器","timestamp":time.time()}
			response_json=json.dumps(response,ensure_ascii=False)
			self.wfile.write(response_json.encode('utf-8'))
			self.wfile.write(b'\n')
		elif parsed_path.path=='/':
			self.send_response(200)
			self.send_header('Content-Type','text/html;charset=utf-8')
			self.end_headers()
			html=f"""<html><head><title>量子IDS检测器MCP服务</title></head>
				<body style="font-family:Arial,sans-serif;margin:20px">
				<h1>🐱 量子IDS检测器MCP服务</h1>
				<p>服务器运行正常 - 端口:49160</p>
				<h2>可用端点:</h2>
				<ul>
					<li><code>GET /health</code> - 健康检查</li>
					<li><code>POST /analyze</code> - PCAP文件分析</li>
					<li><code>POST /analyze_details</code> - PCAP流量细节(委托pcap_analysis.py)</li>
				</ul>
				<h2>POST /analyze 请求示例:</h2>
				<pre style="background:#f4f4f4;padding:10px;border-radius:5px">
				curl -X POST http://127.0.0.1:49160/analyze \\
				  -H "Content-Type: application/json" \\
				  -d '{{
					"pcap_path": "/path/to/file.pcap",
					"target_ip": "192.168.1.100"
				  }}'</pre>
				<p>当前时间:{time.strftime('%Y-%m-%d %H:%M:%S')}</p>
				</body></html>"""
			self.wfile.write(html.encode('utf-8'))
		else:
			self.send_response(404)
			self.send_header('Content-Type','application/json')
			self.end_headers()
			response={"error":"Endpoint not found","path":parsed_path.path}
			self.wfile.write(json.dumps(response,ensure_ascii=False).encode('utf-8'))
	
	def do_POST(self):#处理POST请求
		content_length=int(self.headers.get('Content-Length',0))
		if content_length==0:
			self.send_error(400,"Empty request body")
			return
		try:
			post_data=self.rfile.read(content_length)
			request_data=json.loads(post_data.decode('utf-8'))
			if'pcap_path' not in request_data:
				self.send_error(400,'Missing required parameter: pcap_path')
				return
			pcap_path=request_data.get('pcap_path')
			if not os.path.exists(pcap_path):
				self.send_error(400,f'PCAP file not found: {pcap_path}')
				return
			parsed_path=urlparse(self.path)
			if parsed_path.path=='/analyze_details':
				result=self.detector.analyze_pcap_details(pcap_path)
			elif parsed_path.path=='/analyze':
				target_ip=request_data.get('target_ip')
				cache_npy_path=request_data.get('cache_npy_path')
				if cache_npy_path and not os.path.exists(os.path.dirname(cache_npy_path)):
					os.makedirs(os.path.dirname(cache_npy_path),exist_ok=True)
				result=self.detector.analyze_pcap(pcap_path,target_ip)
			else:
				self.send_error(404,'Endpoint not found')
				return
			self.send_response(200)
			self.send_header('Content-Type','application/json;charset=utf-8')
			
			for allowclient in self.allowclients:self.send_header('Access-Control-Allow-Origin',allowclient)
			
			self.end_headers()
			response_json=json.dumps(result,indent=2,ensure_ascii=False)
			self.wfile.write(response_json.encode('utf-8'))
			self.wfile.write(b'\n')
		except json.JSONDecodeError:
			self.send_response(400)
			self.send_header('Content-Type','application/json')
			self.end_headers()
			response={"error":"Invalid JSON format"}
			self.wfile.write(json.dumps(response,ensure_ascii=False).encode('utf-8'))
		except Exception as e:
			self.send_response(500)
			self.send_header('Content-Type','application/json')
			self.end_headers()
			response={"error":f"Internal server error: {str(e)}"}
			self.wfile.write(json.dumps(response,ensure_ascii=False).encode('utf-8'))
	
	def log_message(self,format,*args):#自定义日志格式
		logger.info(f"HTTP {self.client_address[0]} - {format%args}")

class MCPServer(socketserver.ThreadingMixIn,HTTPServer):
	allow_reuse_address=True
	daemon_threads=True
	def __init__(self,server_address,detector):
		self.detector=detector
		super().__init__(server_address,MCPRequestHandler)

def main():#主函数
	parser=argparse.ArgumentParser(description='量子IDS检测器MCP服务器')
	parser.add_argument('--host',default='127.0.0.2',help='服务IP(默认127.0.0.2)')
	parser.add_argument('--port',type=int,default=49160,help='服务端口(默认49160)')
	parser.add_argument('--model-dir',default='.',help='模型文件路径')
	parser.add_argument('--cache-dir',default='./feature_cache',help='NPY特征缓存目录')
	parser.add_argument('--quantum-shots',type=int,default=512,help='量子测量次数(64-4096)')
	parser.add_argument('--ip-query',dest='ip_query',action='store_true',default=True,help='启用IP属地查询(默认开启,双接口:ip-api.com+ip.taobao.com)')
	parser.add_argument('--no-ip-query',dest='ip_query',action='store_false',help='关闭IP属地查询(结果中属地标记为未启用)')
	parser.add_argument('--log-level',default='INFO',choices=['DEBUG','INFO','WARNING','ERROR'],help='日志级别')
	args=parser.parse_args()
	
	logging.getLogger().setLevel(getattr(logging,args.log_level))
	
	try:
		logger.info(f"启动量子IDS检测器MCP服务器")
		logger.info(f"模型目录:{args.model_dir}")
		logger.info(f"缓存目录:{args.cache_dir}")
		logger.info(f"量子测量次数:{args.quantum_shots}")
		logger.info(f"IP属地查询:{'开启'if args.ip_query else'关闭'}")

		detector=IDSDetector(model_dir=args.model_dir,cache_dir=args.cache_dir,quantum_shots=args.quantum_shots,enable_ip_query=args.ip_query)
		server_address=(args.host,args.port)
		server=MCPServer(server_address,detector)
		
		logger.info(f"MCP服务器启动在 http://{args.host}:{args.port}")
		logger.info(f"健康检查: curl http://{args.host}:{args.port}/health")
		logger.info(f"分析端点: POST http://{args.host}:{args.port}/analyze")
		logger.info("按Ctrl+C停止服务器")
		
		server.serve_forever()
	except KeyboardInterrupt:
		logger.info("收到中断信号,停止服务器...")
	except Exception as e:
		logger.error(f"服务器启动失败:{e}")
		sys.exit(1)

if __name__=="__main__":
	main()