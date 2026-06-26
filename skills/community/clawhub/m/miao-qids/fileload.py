import os,re,sys,pickle
import numpy as np
import torch
from scapy.all import*
from FeatureSelection import*

class FileLoader:
	def __init__(self,use_cache=True,cache_dir="./feature_cache",result_dir="./特征选择结果"):
		self.use_cache=use_cache
		self.cache_dir=cache_dir
		self.result_dir=result_dir
		os.makedirs(cache_dir,exist_ok=True)
		os.makedirs(result_dir,exist_ok=True)
		self.feature_selector=FeatureSelector(use_cache,cache_dir,result_dir)
		self.unified_pca_model=self._load_unified_pca_model()
	
	def _load_unified_pca_model(self):#加载统一的8分类SPCA模型
		model_file=os.path.join(self.result_dir,"unified_8class_spca.pkl")
		if os.path.exists(model_file):
			try:
				with open(model_file,'rb')as f:
					return pickle.load(f)
			except Exception as e:
				print(f"加载统一PCA模型失败:{e}")
				return None
		else:
			print(f"警告:统一PCA模型文件不存在:{model_file}")
			return None
	
	def load_attackFileVector(self,filename,attack_type,file_id=None,cache_dir=None):
		if file_id is None:file_id=self.extract_trailing_number(filename)or 0
		#使用传入的cache_dir或默认的self.cache_dir
		actual_cache_dir=cache_dir if cache_dir is not None else self.cache_dir
		os.makedirs(actual_cache_dir,exist_ok=True)
		
		cache_file=os.path.join(actual_cache_dir,f"{os.path.splitext(os.path.basename(filename))[0]}.npy")
		if self.use_cache and os.path.exists(cache_file):
			try:
				features=np.load(cache_file)
				vector=self._apply_unified_pca_transform(features)
				return"cached_session",vector
			except Exception as e:
				print(f"缓存失效:{os.path.basename(filename)}:{e}")
				if os.path.exists(cache_file):os.remove(cache_file)
		try:
			packets=rdpcap(filename)
			from sessionclass import AccessSession
			session=AccessSession(file_id,packets)
			for j,pkt in enumerate(packets):
				if j<len(packets)/4:
					sport,dport=self.getportfrompackage(pkt)
					session.update_represent_socket(pkt,sport,dport)
			sv_sk=session.get_socket_history_sample(1024)
			sv0=session.get_averagePackageProperty_vector()
			sv1=session.get_extendProperty_vector()
			sv2=session.get_averAppDataBytes()
			sv3=self.get_safe_enhanced_features(session)
			features=np.array(sv_sk+sv0+sv1+sv2+sv3,dtype=np.float32)
			if self.use_cache:np.save(cache_file,features)
			vector=self._apply_unified_pca_transform(features)
			return session,vector
		except Exception as e:
			print(f"处理文件错误{filename}:{e}")
			return None,None
	
	def _apply_unified_pca_transform(self,features):
		"""使用统一SPCA模型转换特征"""
		if self.unified_pca_model is None:
			return torch.tensor(features,dtype=torch.float32)
		model_data=self.unified_pca_model
		scaler_mean=model_data.get('scaler_mean')
		scaler_scale=model_data.get('scaler_scale')
		selected_indices=model_data.get('selected_indices')
		pca_components=model_data.get('pca_components')
		n_components=model_data.get('n_components',len(features))
		
		if scaler_mean is None or pca_components is None or selected_indices is None:
			return torch.tensor(features,dtype=torch.float32)
		
		#应用统一的标准化、特征选择和PCA降维
		features_scaled=(features-scaler_mean)/np.where(scaler_scale!=0,scaler_scale,1.0)
		features_selected=features_scaled[selected_indices]
		features_pca=features_selected.dot(pca_components[:n_components].T)
		return torch.tensor(features_pca,dtype=torch.float32)
	
	def load_attackTypeVector(self,attack_type,max_files=1000,cache_dir=None):
		if attack_type not in attacktypes:
			print(f"未知攻击类型:{attack_type}")
			return[],[]
		dir_path=f'./{attack_type}/'
		if not os.path.exists(dir_path):
			print(f"目录不存在:{dir_path}")
			return[],[]
		filenames=[f for f in os.listdir(dir_path)if f.endswith('.pcap')][:max_files]
		sessions,vectors=[],[]
		for i,filename in enumerate(filenames):
			filepath=os.path.join(dir_path,filename)
			session,vector=self.load_attackFileVector(filepath,attack_type,i,cache_dir)
			if vector is not None:
				sessions.append(session)
				vectors.append(vector)
		return sessions,vectors
	
	def get_safe_enhanced_features(self,session):
		try:
			matrix=session.base_Property_matrix
			n_packets=len(matrix[0])if matrix and len(matrix)>0 else 0
			features=[]
			for row in matrix:
				if n_packets>0:
					row_array=np.array([float(x)for x in row])
					features.extend([float(np.mean(row_array)),float(np.std(row_array))])
				else:features.extend([0.0]*2)
			return features
		except Exception as e:
			print(f"安全特征提取错误:{e}")
			return[0.0]*14
	
	def getportfrompackage(self,p):
		if p.haslayer(TCP)or p.haslayer(UDP):return p.sport,p.dport
		elif p.haslayer(ICMP):return -4,-4
		elif p.haslayer(ARP):return -2,-2
		elif p.haslayer(RIP):return -3,-3
		elif p.haslayer(OSPF_Hdr):return -5,-5
		else:return 0,0
	
	def extract_trailing_number(self,filename):
		base_name=os.path.splitext(filename)[0]
		match=re.search(r'(\d+)$',base_name)
		return int(match.group(1))if match else None
	
	def get_feature_dimension(self,attack_type):#返回统一SPCA模型的输出维度
		if self.unified_pca_model is not None:
			return self.unified_pca_model.get('n_components',5681)
		return 5681
	
	def get_available_attack_types(self):
		available_types=[]
		for attack_type in attacktypes:
			dir_path=f'./{attack_type}/'
			if os.path.exists(dir_path)and any(f.endswith('.pcap')for f in os.listdir(dir_path)):
				available_types.append(attack_type)
		return available_types

def load_attackFileVector(filename,attack_type,file_id=None,cache_dir=None):
	loader=FileLoader()
	return loader.load_attackFileVector(filename,attack_type,file_id,cache_dir)

def load_attackTypeVector(attack_type,max_files=1000,cache_dir=None):
	loader=FileLoader()
	return loader.load_attackTypeVector(attack_type,max_files,cache_dir)

if __name__=="__main__":
	loader=FileLoader()
	available_types=loader.get_available_attack_types()
	print(f"可用的攻击类型:{available_types}")
	for attack_type in available_types:
		sessions,vectors=load_attackTypeVector(attack_type,max_files=5)