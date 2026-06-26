import numpy as np,random,math,time,hashlib,json,pickle,os,threading
from concurrent.futures import ThreadPoolExecutor,as_completed
from pyqpanda3.core import*
from pyqpanda3.vqcircuit import*
from pyvqnet.qnn.pq3.measure import probs_measure
from pyvqnet.tensor import QTensor
from pyvqnet.optim import adam

def QTensor_protect(v):#返回保护的QTensor
	return v if type(v)==QTensor else QTensor(np.array(v))

def tensor_empty(v):#检查张量是否为空
	if isinstance(v,QTensor):return not v.any()
	elif isinstance(v,np.ndarray):return v.size==0
	elif isinstance(v,list):return len(v)==0
	else:return not v

class QNN_MTD:
	def __init__(self,qbits_num=8,layers_num=3,data_num_per_qbit=8,cache_file="circuit_cache.json"):#初始化量子模型
		self.qbits_num,self.layers_num,self.data_num_per_qbit=qbits_num,layers_num,data_num_per_qbit
		self.total_params=layers_num*qbits_num*2
		self.qvm=CPUQVM()
		limit=np.sqrt(6.0/(qbits_num*2))
		self.params=QTensor(np.random.uniform(-limit,limit,self.total_params))
		self.frozen_mask=[True]*self.total_params
		self.frozen_indices=[]
		self.frozen_count=0
		self._circuit_cache={}
		self._loss_cache={}
		self._cache_file=cache_file
		self.thread_pool=ThreadPoolExecutor(max_workers=4)
		self._cache_lock=threading.Lock()#线程锁
		print(f"QNN初始化:{qbits_num}量子比特,{layers_num}层,{data_num_per_qbit}角度/比特,{self.total_params}参数")
	
	def freeze_parameters(self,indices=None,ratio=0.5,mode='alternate'):#冻结参数
		if indices is not None:
			self.frozen_indices=indices
		else:
			if mode=='alternate':self.frozen_indices=[i for i in range(self.total_params) if i%2==0]
			elif mode=='first_half':self.frozen_indices=list(range(int(self.total_params*ratio)))
			elif mode=='last_layer':self.frozen_indices=list(range(self.total_params-self.qbits_num*2))
			elif mode=='random':self.frozen_indices=np.random.choice(self.total_params,size=int(self.total_params*ratio),replace=False).tolist()
		self.frozen_mask=[True]*self.total_params
		for idx in self.frozen_indices:
			if 0<=idx<self.total_params:self.frozen_mask[idx]=False
		self.frozen_count=sum(1 for m in self.frozen_mask if not m)
		active_count=self.total_params-self.frozen_count
		print(f"冻结参数:{self.frozen_count}/{self.total_params}({self.frozen_count/self.total_params*100:.1f}%),可训练:{active_count}")
	
	def save_model(self,filename="qnn_model.pkl"):#保存模型
		try:
			model_data={
				'params':self.params.to_numpy(),
				'frozen_mask':self.frozen_mask,
				'frozen_indices':self.frozen_indices,
				'qbits_num':self.qbits_num,
				'layers_num':self.layers_num,
				'data_num_per_qbit':self.data_num_per_qbit,
				'total_params':self.total_params
			}
			with open(filename,'wb')as f:
				pickle.dump(model_data,f)
			print(f"模型已保存到:{filename}")
		except Exception as e:
			print(f"保存模型失败:{e}")
	
	def load_model(self,filename="qnn_model.pkl"):#加载模型
		if not os.path.exists(filename):
			print(f"模型文件不存在:{filename}")
			return False
		try:
			with open(filename,'rb')as f:
				model_data=pickle.load(f)
			if'params'in model_data:self.params=QTensor(model_data['params'])
			if'frozen_mask'in model_data:
				self.frozen_mask=model_data['frozen_mask']
				self.frozen_count=sum(1 for m in self.frozen_mask if not m)
			if'frozen_indices'in model_data:self.frozen_indices=model_data['frozen_indices']
			for key in['qbits_num','layers_num','data_num_per_qbit','total_params']:
				if key in model_data and hasattr(self,key):setattr(self,key,model_data[key])
			print(f"从{filename}加载模型成功")
			print(f" 参数数量:{self.total_params},冻结参数:{self.frozen_count}")
			return True
		except Exception as e:
			print(f"加载模型失败:{e}")
			return False
	
	def _encode_64d_features(self,circuit,input_64d):#完整64维特征编码
		if tensor_empty(input_64d):return
		if len(input_64d)<64:input_64d=list(input_64d)+[0.0]*(64-len(input_64d))
		elif len(input_64d)>64:input_64d=input_64d[:64]
		angles=np.array(input_64d,dtype=np.float32)
		for qubit_idx in range(self.qbits_num):
			start_idx=qubit_idx*8
			end_idx=start_idx+8
			qubit_angles=angles[start_idx:end_idx]
			for angle_idx,angle in enumerate(qubit_angles):
				if angle_idx%3==0:circuit<<RY(qubit_idx,angle)
				elif angle_idx%3==1:circuit<<RZ(qubit_idx,angle)
				else:circuit<<RX(qubit_idx,angle)
	
	def _build_circuit(self,params,input_64d):#构建完整量子线路
		circuit=QCircuit(self.qbits_num)
		self._encode_64d_features(circuit,input_64d)
		param_idx=0
		for layer in range(self.layers_num):
			for qubit in range(self.qbits_num):
				if param_idx+1<len(params):
					circuit<<RX(qubit,params[param_idx])
					circuit<<RY(qubit,params[param_idx+1])
					param_idx+=2
			for qubit in range(self.qbits_num-1):
				circuit<<CNOT(qubit,qubit+1)
		return circuit
	
	def forward(self,params_in=None,input_64d=None,shots=1024):#前向传播
		if tensor_empty(input_64d):return[0.0]*self.qbits_num
		params=self.params if params_in is None or tensor_empty(params_in)else QTensor_protect(params_in)
		params_np=params.to_numpy().flatten()
		circuit=self._build_circuit(params_np,input_64d)
		prog=QProg()
		prog<<circuit
		prog<<SWAP(0,8)
		for i in range(self.qbits_num):prog<<measure(i,i)
		result=probs_measure(self.qvm,prog,range(self.qbits_num),shots=shots)
		qubit_probs=[0.0]*self.qbits_num
		for qubit_idx in range(self.qbits_num):
			mask=1<<qubit_idx
			for state,prob in enumerate(result):
				if state&mask:qubit_probs[qubit_idx]+=prob
		return qubit_probs
	
	def get_loss(self,params_in=None,input_64d=None,label=None):#计算损失
		if tensor_empty(label):label=[1]+[0]*(self.qbits_num-1)
		probs=self.forward(params_in,input_64d,shots=512)
		loss=sum([(label[i]-probs[i])**2 for i in range(min(len(label),self.qbits_num))])
		return loss
	
	def _get_grad_single_param(self,base_params,param_idx,input_64d,label):#单参数梯度计算
		params_plus=base_params.copy()
		params_minus=base_params.copy()
		params_plus[param_idx]+=math.pi/2.0
		params_minus[param_idx]-=math.pi/2.0
		loss_plus=self.get_loss(params_plus,input_64d,label)
		loss_minus=self.get_loss(params_minus,input_64d,label)
		return(loss_plus-loss_minus)/2.0
	
	def get_grad_batch_fast(self,batch_inputs,batch_labels,use_cache=True):#批量梯度计算
		if not batch_inputs or not batch_labels:return QTensor(np.zeros(self.total_params))
		n_samples=len(batch_inputs)
		params_np=self.params.to_numpy().flatten()
		active_indices=[i for i in range(self.total_params) if self.frozen_mask[i]]
		if not active_indices:return QTensor(np.zeros(self.total_params))
		grad_matrix=np.zeros((n_samples,self.total_params))
		futures=[]
		for sample_idx in range(n_samples):
			future=self.thread_pool.submit(self._compute_sample_grad,
				params_np.copy(),batch_inputs[sample_idx],batch_labels[sample_idx],
				active_indices,use_cache)
			futures.append(future)
		for i,future in enumerate(as_completed(futures)):
			grad_matrix[i]=future.result()
		avg_grad=grad_matrix.mean(axis=0)
		return QTensor(avg_grad)
	
	def _compute_sample_grad(self,base_params,input_64d,label,active_indices,use_cache=True):#单样本梯度计算
		grad=np.zeros(self.total_params)
		cache_key=None
		if use_cache:
			p_str=base_params.tobytes()[:50]
			i_str=np.array(input_64d,dtype=np.float32).tobytes()[:50]if isinstance(input_64d,list)else str(input_64d).encode()[:50]
			l_str=np.array(label,dtype=np.float32).tobytes()[:20]if isinstance(label,list)else str(label).encode()[:20]
			cache_key=hashlib.md5(p_str+i_str+l_str).hexdigest()
			with self._cache_lock:#线程安全的缓存读取
				if cache_key in self._loss_cache:return self._loss_cache[cache_key]
		for param_idx in active_indices:
			g=self._get_grad_single_param(base_params,param_idx,input_64d,label)
			grad[param_idx]=g
		if use_cache and cache_key:
			with self._cache_lock:#线程安全的缓存写入
				self._loss_cache[cache_key]=grad
				if len(self._loss_cache)>1000 and self._loss_cache:
					self._loss_cache.pop(next(iter(self._loss_cache)))
		return grad
	
	def get_MSELoss_grad(self,input_64d,label):#梯度接口
		return self.get_grad_batch_fast([input_64d],[label],use_cache=True)