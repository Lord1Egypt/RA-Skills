import os,sys,pickle,random
import torch,torch.nn as nn,torch.optim as optim
import numpy as np
from fileload import FileLoader,attacktypes

DEVICE_TYPE='cuda'
os.environ['PYTORCH_CUDA_ALLOC_CONF']='expandable_segments:True,max_split_size_mb:128'
os.environ['CUDA_LAUNCH_BLOCKING']='1'

class CNN_MTD(nn.Module):
	def __init__(self,input_dim=180,latent_dim=64,center_weight=0.1,triplet_margin=1.0):
		super().__init__()
		self.input_dim,self.latent_dim=input_dim,latent_dim
		self.center_weight,self.triplet_margin=center_weight,triplet_margin
		self.device=torch.device(DEVICE_TYPE if torch.cuda.is_available()else'cpu')
		self.centers=nn.Parameter(torch.randn(len(attacktypes),latent_dim))
		
		# 编码器
		self.encoder=nn.Sequential(
			nn.Linear(input_dim,1024),nn.ReLU(inplace=True),
			nn.Linear(1024,512),nn.ReLU(inplace=True),
			nn.Linear(512,256),nn.ReLU(inplace=True),
			nn.Linear(256,128),nn.ReLU(inplace=True),
			nn.Linear(128,latent_dim),nn.Tanh())
		
		# 解码器
		self.decoder=nn.Sequential(
			nn.Linear(latent_dim,128),nn.ReLU(inplace=True),
			nn.Linear(128,256),nn.ReLU(inplace=True),
			nn.Linear(256,512),nn.ReLU(inplace=True),
			nn.Linear(512,1024),nn.ReLU(inplace=True),
			nn.Linear(1024,input_dim))
		
		self.to(self.device)
		print(f"CNN_MTD初始化完成,设备:{self.device},输入维度:{input_dim},潜在维度:{latent_dim}")
	
	def forward(self,x):
		latent=self.encoder(x)
		reconstructed=self.decoder(latent)
		return latent,reconstructed
	
	def compute_center_loss(self,latents,labels):#中心损失：使同类别样本靠近对应中心
		if labels is None or len(labels)==0:
			return torch.tensor(0.0,device=self.device)
		batch_centers=self.centers[labels]
		return torch.mean(torch.sum((latents-batch_centers)**2,dim=1))
	
	def compute_triplet_loss(self,latents,labels):#三元组损失：使正样本对更近，负样本对更远
		if labels is None or len(labels)<2:
			return torch.tensor(0.0,device=self.device)
		n=latents.shape[0]
		total_loss=0.0
		valid_pairs=0
		
		for i in range(n):
			anchor_latent,anchor_label=latents[i],labels[i]
			pos_indices=[j for j in range(n)if j!=i and labels[j]==anchor_label]
			neg_indices=[j for j in range(n)if labels[j]!=anchor_label]
			
			if not pos_indices or not neg_indices:
				continue
			
			# 选择最难正样本
			pos_dists=[torch.norm(anchor_latent-latents[j])**2 for j in pos_indices]
			#先将张量移动到CPU，然后转换为Python标量
			pos_dists_cpu=[dist.item()for dist in pos_dists]
			hardest_pos=pos_indices[np.argmax(pos_dists_cpu)]
			
			# 选择最难负样本
			neg_dists=[torch.norm(anchor_latent-latents[j])**2 for j in neg_indices]
			#先将张量移动到CPU，然后转换为Python标量
			neg_dists_cpu=[dist.item()for dist in neg_dists]
			hardest_neg=neg_indices[np.argmin(neg_dists_cpu)]
			
			pos_dist=torch.norm(anchor_latent-latents[hardest_pos])**2
			neg_dist=torch.norm(anchor_latent-latents[hardest_neg])**2
			loss=torch.relu(pos_dist-neg_dist+self.triplet_margin)
			total_loss+=loss
			valid_pairs+=1
		
		return total_loss/valid_pairs if valid_pairs>0 else torch.tensor(0.0,device=self.device)
	
	def train_model(self,data_generator,epochs=100,lr=0.0001,weight_decay=1e-5,resume_checkpoint=None):
		optimizer=optim.Adam(self.parameters(),lr=lr,weight_decay=weight_decay)
		recon_criterion=nn.MSELoss()
		start_epoch=0
		
		if resume_checkpoint and os.path.exists(resume_checkpoint):
			checkpoint=torch.load(resume_checkpoint,map_location=self.device)
			self.load_state_dict(checkpoint['model_state_dict'])
			if'optimizer_state_dict'in checkpoint:
				optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
			start_epoch=checkpoint.get('epoch',0)+1
			print(f"从检查点恢复训练,从第{start_epoch}轮开始")
		
		self.train()
		for epoch in range(start_epoch,epochs):
			total_loss,total_recon_loss,total_center_loss,total_triplet_loss,batch_count=0,0,0,0,0
			
			#获取并打乱数据
			all_data,all_labels=self._collect_and_shuffle_data(data_generator)
			if not all_data:continue
			
			batch_size=32
			n_batches=len(all_data)//batch_size
			
			for batch_idx in range(n_batches):
				start_idx=batch_idx*batch_size
				end_idx=min(start_idx+batch_size,len(all_data))
				batch_data=torch.stack(all_data[start_idx:end_idx]).to(self.device)
				batch_labels=torch.tensor(all_labels[start_idx:end_idx],device=self.device)
				
				optimizer.zero_grad()
				latents,reconstructed=self.forward(batch_data)
				
				# 计算三种损失
				recon_loss=recon_criterion(reconstructed,batch_data)
				center_loss=self.compute_center_loss(latents,batch_labels)
				triplet_loss=self.compute_triplet_loss(latents,batch_labels)
				
				loss=recon_loss+self.center_weight*center_loss+0.1*triplet_loss
				loss.backward()
				torch.nn.utils.clip_grad_norm_(self.parameters(),max_norm=1.0)
				optimizer.step()
				
				total_loss+=loss.item()
				total_recon_loss+=recon_loss.item()
				total_center_loss+=center_loss.item()
				total_triplet_loss+=triplet_loss.item()
				batch_count+=1
			
			if batch_count>0:
				avg_loss=total_loss/batch_count
				print(f"Epoch {epoch}完成,平均Loss:{avg_loss:.6f}"
					f"(R:{total_recon_loss/batch_count:.6f},C:{total_center_loss/batch_count:.6f},T:{total_triplet_loss/batch_count:.6f})")
				if avg_loss<0.0001:break
		
		self.save_model("cnn_mtd_final.pth",optimizer=optimizer,epoch=epoch)
		print("训练完成")
	
	def _collect_and_shuffle_data(self,data_generator):#收集并打乱所有数据
		all_data,all_labels=[],[]
		attack_idx_map={atk:i for i,atk in enumerate(attacktypes)}
		
		for attack_type in attacktypes:
			sessions,vectors=data_generator.load_attackTypeVector(attack_type,max_files=2000)
			if vectors:
				all_data.extend([v.cpu()if v.is_cuda else v for v in vectors])
				all_labels.extend([attack_idx_map[attack_type]]*len(vectors))
		
		if not all_data:return[],[]
		
		# 打乱数据顺序
		indices=list(range(len(all_data)))
		random.shuffle(indices)
		all_data=[all_data[i]for i in indices]
		all_labels=[all_labels[i]for i in indices]
		
		return all_data,all_labels
	
	def save_model(self,filepath,optimizer=None,epoch=None):
		save_dict={
			'model_state_dict':self.state_dict(),
			'input_dim':self.input_dim,
			'latent_dim':self.latent_dim,
			'center_weight':self.center_weight,
			'triplet_margin':self.triplet_margin
		}
		if optimizer is not None:
			save_dict['optimizer_state_dict']=optimizer.state_dict()
		if epoch is not None:
			save_dict['epoch']=epoch
		torch.save(save_dict,filepath)
		print(f"模型已保存:{filepath}")
	
	@classmethod
	def load_model(cls,filepath):
		device=torch.device(DEVICE_TYPE if torch.cuda.is_available()else'cpu')
		checkpoint=torch.load(filepath,map_location=device)
		model=cls(
			input_dim=checkpoint.get('input_dim',180),
			latent_dim=checkpoint.get('latent_dim',64),
			center_weight=checkpoint.get('center_weight',0.1),
			triplet_margin=checkpoint.get('triplet_margin',1.0))
		model.load_state_dict(checkpoint['model_state_dict'])
		return model

def find_latest_checkpoint():
	checkpoint_files=[f for f in os.listdir('.')if f.endswith('.pth')and f in['cnn_mtd_final.pth','interrupted_checkpoint.pth']or f.startswith('checkpoint_epoch_')]
	if not checkpoint_files:return None
	def get_epoch(f):
		if f=='cnn_mtd_final.pth':return float('inf')
		elif f=='interrupted_checkpoint.pth':return float('inf')-1
		else:return int(f.split('_')[-1].split('.')[0])
	checkpoint_files.sort(key=get_epoch)
	return checkpoint_files[-1]

if __name__=="__main__":
	loader=FileLoader()
	available_types=loader.get_available_attack_types()
	print(f"开始训练,攻击类型:{available_types}")
	
	if not available_types:
		print("错误:未找到任何可用的攻击类型数据")
		sys.exit(1)
	
	model=CNN_MTD(input_dim=loader.get_feature_dimension(available_types[0]))
	try:
		model.train_model(loader,epochs=1000,lr=0.00001)
	except KeyboardInterrupt:
		print("\n训练被用户中断")
		model.save_model("interrupted_checkpoint.pth")
	except Exception as e:
		print(f"训练出错:{e}")
		import traceback
		traceback.print_exc()
