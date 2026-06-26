import os,sys,pickle,re,warnings,numpy as np
warnings.filterwarnings('ignore')
from scapy.all import*
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import SelectKBest,f_classif

attacktypes=["善意流量","端口扫描","SSH暴力破解","FTP暴力破解","拒绝服务攻击","SQL注入","XSS","WebShell"]
TARGET_CLASSES=8
TARGET_DIM=180
FEATURE_SELECT_K=2586

class FeatureSelector:
	def __init__(self,use_cache=True,cache_dir="./feature_cache",result_dir="./特征选择结果"):
		self.use_cache,self.cache_dir,self.result_dir=use_cache,cache_dir,result_dir
		os.makedirs(cache_dir,exist_ok=True)
		os.makedirs(result_dir,exist_ok=True)
	
	def getportfrompackage(self,p):
		if p.haslayer(TCP)or p.haslayer(UDP):return p.sport,p.dport
		elif p.haslayer(ICMP):return -4,-4
		elif p.haslayer(ARP):return -2,-2
		elif p.haslayer(RIP):return -3,-3
		else:return 0,0
	
	def extract_features(self,filepath,file_id,attack_idx):
		cache_file=os.path.join(self.cache_dir,f"{os.path.splitext(os.path.basename(filepath))[0]}.npy")
		if self.use_cache and os.path.exists(cache_file):
			try:return np.load(cache_file)
			except:print(f"缓存失效:{os.path.basename(filepath)}")
		try:
			packets=rdpcap(filepath)
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
			return features
		except Exception as e:
			print(f"处理文件错误{filepath}:{e}")
			return np.zeros(5681,dtype=np.float32)
	
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
		except:return[0.0]*14
	
	def train_unified_spca(self):
		print("=== 开始针对8分类数据集训练统一SPCA模型 ===")
		all_features,all_labels=[],[]
		
		for attack_idx,attack_type in enumerate(attacktypes):
			attack_dir='./'+attack_type+'/'
			if not os.path.exists(attack_dir):continue
			filenames=[f for f in os.listdir(attack_dir)if f.endswith('.pcap')]
			print(f"收集 {attack_type}: {len(filenames)} 个文件")
			for filename in filenames:
				filepath=os.path.join(attack_dir,filename)
				base_name=os.path.splitext(filename)[0]
				match=re.search(r'(\d+)$',base_name)
				sub_id=int(match.group(1))if match else 0
				file_id=(attack_idx,sub_id)
				features=self.extract_features(filepath,file_id,attack_idx)
				all_features.append(features)
				all_labels.append(attack_idx)
		
		if not all_features:
			print("错误: 未收集到任何训练数据。")
			return
		
		X=np.array(all_features)
		y=np.array(all_labels)
		print(f"数据汇总: 总样本数={X.shape[0]}, 原始特征维度={X.shape[1]}, 类别数={len(np.unique(y))}")
		
		# 数据标准化
		scaler=StandardScaler()
		X_scaled=scaler.fit_transform(X)
		if np.isnan(X_scaled).any():
			imputer=SimpleImputer(strategy='mean')
			X_scaled=imputer.fit_transform(X_scaled)
		
		# 有监督特征选择 (8分类)
		print(f"步骤1: 8分类有监督特征选择 (K={min(FEATURE_SELECT_K, X.shape[1])})")
		selector=SelectKBest(score_func=f_classif,k=min(FEATURE_SELECT_K,X.shape[1]))
		X_selected=selector.fit_transform(X_scaled,y)
		selected_indices=selector.get_support(indices=True)
		
		# PCA降维
		print(f"步骤2: PCA降维 (目标维度={min(TARGET_DIM, X_selected.shape[1])})")
		pca=PCA(n_components=min(TARGET_DIM,X_selected.shape[1]))
		X_spca=pca.fit_transform(X_selected)
		
		print(f"统一SPCA完成: 最终维度 = {X_spca.shape[1]}, 累计解释方差 = {sum(pca.explained_variance_ratio_):.8f}")
		
		# 保存单个统一模型
		unified_model={
			'selected_indices':selected_indices,
			'selector_scores':selector.scores_,
			'pca_components':pca.components_,
			'pca_mean':pca.mean_,
			'pca_explained_variance_ratio':pca.explained_variance_ratio_,
			'scaler_mean':scaler.mean_,
			'scaler_scale':scaler.scale_,
			'n_components':X_spca.shape[1],
			'n_samples':X.shape[0],
			'attack_types':attacktypes
		}
		
		result_file=os.path.join(self.result_dir,"unified_8class_spca.pkl")
		with open(result_file,'wb')as f:
			pickle.dump(unified_model,f)
		print(f"已保存单个统一模型: {result_file}")
		print("\n=== 8分类统一SPCA模型训练完成 ===")
	
	def load_unified_pca_model(self):
		result_file=os.path.join(self.result_dir,"unified_8class_spca.pkl")
		if os.path.exists(result_file):
			with open(result_file,'rb')as f:return pickle.load(f)
		return None
	
	def transform_features_unified(self,features):
		model_data=self.load_unified_pca_model()
		if model_data is None:return features
		scaler_mean=model_data['scaler_mean']
		scaler_scale=model_data['scaler_scale']
		selected_indices=model_data['selected_indices']
		pca_components=model_data['pca_components']
		n_components=model_data['n_components']
		features_scaled=(features-scaler_mean)/np.where(scaler_scale!=0,scaler_scale,1.0)
		features_selected=features_scaled[selected_indices]
		features_spca=features_selected.dot(pca_components[:n_components].T)
		return features_spca

def main():
	selector=FeatureSelector()
	selector.train_unified_spca()

if __name__=="__main__":main()