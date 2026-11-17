import numpy as np,random,math,time,hashlib,json,pickle,os,threading
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor,as_completed
import multiprocessing as mp
from pyqpanda3.core import*
from pyqpanda3.qcloud import*
from pyqpanda3.vqcircuit import*
from pyvqnet.qnn.pq3.measure import probs_measure
from pyvqnet.tensor import QTensor
from pyvqnet.optim import adam

def QTensor_protect(v):#返回保护的QTensor
	return v if type(v)==QTensor else QTensor(np.array(v))

_BITS8=(np.arange(256)[:,None]>>np.arange(8)[None,:])&1#预计算256状态x8比特矩阵,加速边缘化

#多进程支持:pyqpanda3的pybind绑定持有GIL,线程无法并行,只能用进程池
_MP_MODEL=None
def _mp_init(qbits_num,layers_num,data_num_per_qbit):#子进程初始化:每个进程独立建QVM
	global _MP_MODEL
	_MP_MODEL=QNN_MTD(qbits_num=qbits_num,layers_num=layers_num,data_num_per_qbit=data_num_per_qbit)

def _mp_sample_grad_chunk(args):#子进程:单样本参数块梯度(参数分块提高进程利用率)
	params_np,input_64d,label,param_chunk=args
	_MP_MODEL.params=QTensor(np.asarray(params_np,dtype=np.float64))
	grad=np.zeros(len(params_np))
	for param_idx in param_chunk:
		grad[param_idx]=_MP_MODEL._get_grad_single_param(np.asarray(params_np,dtype=np.float64),param_idx,input_64d,label)
	return grad

def _mp_forward_one(args):#子进程:单样本前向(精确概率)
	params_np,input_64d=args
	_MP_MODEL.params=QTensor(np.asarray(params_np,dtype=np.float64))
	return _MP_MODEL.forward(input_64d=input_64d,shots=0)

def tensor_empty(v):#检查张量是否为空
	if isinstance(v,QTensor):return not v.any()
	elif isinstance(v,np.ndarray):return v.size==0
	elif isinstance(v,list):return len(v)==0
	else:return not v

class QNN_MTD:
	def __init__(self,qbits_num=8,layers_num=6,data_num_per_qbit=8,cache_file="circuit_cache.json"):#初始化量子模型
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
		self.thread_pool=ThreadPoolExecutor(max_workers=max(4,os.cpu_count() or 8))
		self._cache_lock=threading.Lock()#线程锁
		self._qvm_local=threading.local()#每线程独立QVM,避免并行时共享状态冲突
		self._mp_pool=None#惰性创建的进程池

	def _get_mp_pool(self):#获取进程池(spawn启动避免fork与pyvqnet/torch状态冲突)
		if self._mp_pool is None:
			ctx=mp.get_context('spawn')
			self._mp_pool=ProcessPoolExecutor(max_workers=max(2,min(24,(os.cpu_count() or 8))),
				mp_context=ctx,initializer=_mp_init,
				initargs=(self.qbits_num,self.layers_num,self.data_num_per_qbit))
		return self._mp_pool

	def _get_qvm(self):#获取当前线程的QVM(线程局部)
		qvm=getattr(self._qvm_local,'qvm',None)
		if qvm is None:
			qvm=CPUQVM()
			self._qvm_local.qvm=qvm
		return qvm
		
	
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
			#print(f"从{filename}加载模型成功")
			#print(f" 参数数量:{self.total_params},冻结参数:{self.frozen_count}")
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
	
	def forward(self,params_in=None,input_64d=None,shots=0):#前向传播(纯VQC,无SWAP;shots<=0时用精确概率,确定性且更快)
		if tensor_empty(input_64d):return[0.0]*self.qbits_num
		params=self.params if params_in is None or tensor_empty(params_in)else QTensor_protect(params_in)
		params_np=params.to_numpy().flatten()
		circuit=self._build_circuit(params_np,input_64d)
		prog=QProg()
		prog<<circuit
		for i in range(self.qbits_num):prog<<measure(i,i)
		qvm=self._get_qvm()
		if shots<=0:#精确概率:run(prog,0)返回全态矢量概率,无采样噪声;纯8比特VQC直接256状态
			qvm.run(prog,0)
			full=np.asarray(qvm.result().get_prob_list(),dtype=np.float64)
			n_states=1<<self.qbits_num
			if self.qbits_num==8:p1=(_BITS8.T@full[:n_states])[::-1]#probs_measure为大端序
			else:
				bits=(np.arange(n_states)[:,None]>>np.arange(self.qbits_num)[None,:])&1
				p1=(bits.T@full[:n_states])[::-1]
			return p1.tolist()#各量子比特取1概率
		result=probs_measure(qvm,prog,range(self.qbits_num),shots=shots)
		qubit_probs=[0.0]*self.qbits_num
		for qubit_idx in range(self.qbits_num):
			mask=1<<qubit_idx
			for state,prob in enumerate(result):
				if state&mask:qubit_probs[qubit_idx]+=prob
		return qubit_probs

	def forward_batch(self,batch_inputs,shots=0):#批量并行前向(进程池),返回概率矩阵(N,qbits_num)
		if batch_inputs is None or len(batch_inputs)==0:return np.zeros((0,self.qbits_num))
		params_np=self.params.to_numpy().flatten()
		tasks=[(params_np,x)for x in batch_inputs]
		try:
			pool=self._get_mp_pool()
			futures=[pool.submit(_mp_forward_one,t)for t in tasks]
			return np.array([f.result()for f in futures])
		except Exception:
			return np.array([self.forward(input_64d=x,shots=shots)for x in batch_inputs])
	
	def forwardQ(self,params_in=None,input_64d=None,shots=1024):#前向传播
		if tensor_empty(input_64d):return[0.0]*self.qbits_num
		params=self.params if params_in is None or tensor_empty(params_in)else QTensor_protect(params_in)
		params_np=params.to_numpy().flatten()
		circuit=self._build_circuit(params_np,input_64d)
		prog=QProg()
		prog<<circuit<<SWAP(0,8)
		for i in range(self.qbits_num):prog<<measure(i,i)
		
		#{'HanYuan_01': False, 'PQPUMESH8': True, 'WK_C180': True, 'full_amplitude': True, 'partial_amplitude': True, 'single_amplitude': True}
		service=QCloudService("eca8012171babbc37d854e0f61d8240bbb2ed4d7801d5738c38b613e2d09cd073062576676394d74426c34786a4f4757")
		backend=QCloudBackend("WK_C180")
		options=QCloudOptions()
		job=backend.run([prog],shots,options)
		result=job.result().get_probs_list()
		
		qubit_probs=[0.0]*self.qbits_num
		qubit_probs=qubit_one_probabilities(result[0])
		return qubit_probs
	
	def get_loss(self,params_in=None,input_64d=None,label=None):#计算损失(精确概率)
		if tensor_empty(label):label=[1]+[0]*(self.qbits_num-1)
		probs=self.forward(params_in,input_64d,shots=0)
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
	
	def get_grad_batch_fast(self,batch_inputs,batch_labels,use_cache=True):#批量梯度计算(进程池并行)
		if not batch_inputs or not batch_labels:return QTensor(np.zeros(self.total_params))
		n_samples=len(batch_inputs)
		params_np=self.params.to_numpy().flatten()
		active_indices=[i for i in range(self.total_params) if self.frozen_mask[i]]
		if not active_indices:return QTensor(np.zeros(self.total_params))
		grad_matrix=np.zeros((n_samples,self.total_params))
		try:#进程池真并行(GIL不影响子进程);总任务数控制在约2x进程数,平衡IPC开销与并行度
			pool=self._get_mp_pool()
			workers=pool._max_workers
			chunk_size=max(1,-(-len(active_indices)*n_samples//(workers*2)))
			chunks=[active_indices[j:j+chunk_size]for j in range(0,len(active_indices),chunk_size)]
			submits=[(i,pool.submit(_mp_sample_grad_chunk,(params_np,batch_inputs[i],batch_labels[i],ch)))
				for i in range(n_samples)for ch in chunks]
			for i,fut in submits:grad_matrix[i]+=fut.result()
		except Exception as e:#回退线程池(受GIL限制,速度较慢)
			print(f"进程池不可用({e}),回退线程池")
			futures=[self.thread_pool.submit(self._compute_sample_grad,params_np.copy(),
				batch_inputs[i],batch_labels[i],active_indices,use_cache)for i in range(n_samples)]
			for i,f in enumerate(futures):grad_matrix[i]=f.result()
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

def qubit_one_probabilities(counts):#测量结果转化为各个量子比特的取1概率
	bitstring=next(iter(counts))#取出第一个key判断量子比特数
	n=len(bitstring)
	prob_one=[0.0]*n
	for bits,p in counts.items():
		for i,bit in enumerate(bits):
			if bit=='1':prob_one[i]+=p
	return prob_one
