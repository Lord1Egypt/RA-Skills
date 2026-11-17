# 知识点分类规则

## 分类映射表

### 网络
**匹配关键词**：
`BGP`, `OSPF`, `IS-IS`, `路由`, `交换`, `VLAN`, `MPLS`, `VPN`, `TCP`, `IP`,
`子网`, `网关`, `DNS`, `DHCP`, `SDN`, `负载均衡`, `二层`, `三层`, `协议`,
`拓扑`, `端口`, `NAT`, `ACL`, `VXLAN`, `STP`, `RSTP`, `MSTP`, `链路聚合`,
`LACP`, `VRRP`, `HSRP`, `IGP`, `EGP`, `RIP`, `EIGRP`, `组播`, `PIM`,
`IGMP`, `QoS`, `策略路由`, `PBR`, `GRE`, `IPsec`, `BFD`, `NQA`,
`以太网`, `MAC`, `ARP`, `ICMP`, `UDP`, `FTP`, `HTTP`, `HTTPS`,
`SNMP`, `NetFlow`, `sFlow`, `iPerf`, `ping`, `traceroute`, `tracert`

### 网络安全
**匹配关键词**：
`防火墙`, `等保`, `加密`, `渗透`, `漏洞`, `攻击`, `入侵`, `认证`,
`授权`, `审计`, `零信任`, `WAF`, `IDS`, `IPS`, `安全策略`, `态势感知`,
`SOC`, `溯源`, `蜜罐`, `沙箱`, `等级保护`, `密码`, `密码学`, `数字签名`,
`CA证书`, `PKI`, `SSL`, `TLS`, `HTTPS证书`, `XSS`, `SQL注入`, `CSRF`,
`DDoS`, `CC攻击`, `木马`, `病毒`, `勒索`, `钓鱼`, `社会工程学`,
`堡垒机`, `跳板机`, `数据脱敏`, `数据加密`, `隐私计算`, `联邦学习`,
`安全运营`, `SIEM`, `SOAR`, `EDR`, `XDR`, `NTA`, `网络安全法`,
`数据安全法`, `个人信息保护法`, `GDPR`, `ISO27001`, `风险评估`,
`渗透测试`, `红蓝对抗`, `ATT&CK`, `MITRE`, `漏洞扫描`, `基线检查`

### 云计算
**匹配关键词**：
`Docker`, `K8s`, `Kubernetes`, `容器`, `虚拟化`, `OpenStack`, `云原生`,
`微服务`, `Serverless`, `SaaS`, `PaaS`, `IaaS`, `弹性`, `编排`, `镜像`,
`Pod`, `Service`, `Ingress`, `ConfigMap`, `Secret`, `Deployment`,
`StatefulSet`, `DaemonSet`, `CRD`, `Operator`, `Helm`, `Kustomize`,
`CNI`, `CSI`, `CRI`, `containerd`, `runc`, `cri-o`, `etcd`,
`Prometheus`, `Grafana`, `Jaeger`, `Istio`, `Envoy`, `Linkerd`,
`服务网格`, `Service Mesh`, `无服务器`, `函数计算`, `FaaS`,
`虚拟化技术`, `Hypervisor`, `KVM`, `Xen`, `VMware`, `ESXi`, `vSphere`,
`云存储`, `对象存储`, `块存储`, `S3`, `Ceph`, `GlusterFS`,
`云网络`, `VPC`, `安全组`, `弹性IP`, `CDN`, `加速`, `云计算`,
`公有云`, `私有云`, `混合云`, `多云`, `边缘计算`, `Edge Computing`

### AI
**匹配关键词**：
`神经网络`, `深度学习`, `机器学习`, `LLM`, `大模型`, `Transformer`,
`Prompt`, `NLP`, `CV`, `训练`, `推理`, `微调`, `Fine-tuning`, `RAG`,
`Agent`, `向量`, `嵌入`, `Embedding`, `Token`, `GPT`, `ChatGPT`,
`BERT`, `RoBERTa`, `T5`, `ViT`, `CLIP`, `Stable Diffusion`,
`CNN`, `RNN`, `LSTM`, `GRU`, `Attention`, `注意力机制`, `自注意力`,
`强化学习`, `RLHF`, `PPO`, `DQN`, `监督学习`, `无监督学习`, `半监督学习`,
`迁移学习`, `联邦学习`, `对抗学习`, `GAN`, `Diffusion`, `扩散模型`,
`知识图谱`, `图神经网络`, `GNN`, `GCN`, `GraphSAGE`,
`目标检测`, `YOLO`, `SSD`, `Faster R-CNN`, `语义分割`, `实例分割`,
`OCR`, `语音识别`, `ASR`, `TTS`, `文本生成`, `图像生成`, `多模态`,
`AIGC`, `AI绘画`, `模型部署`, `模型量化`, `蒸馏`, `压缩`,
`PyTorch`, `TensorFlow`, `JAX`, `ONNX`, `TensorRT`, `vLLM`,
`LoRA`, `QLoRA`, `Adapter`, `P-tuning`, `Prompt Engineering`

### 其他
**匹配规则**：
以上四类均无法匹配时，归类为"其他"。

## 分类优先级

当一条知识点同时匹配多个分类的关键词时，按以下优先级确定：
1. 网络安全 （优先度最高，安全相关的知识点应优先归类）
2. 网络
3. 云计算
4. AI
5. 其他 （兜底）

## 子分类推断

对于"网络"和"云计算"分类，可根据更细粒度的关键词推断子分类：

### 网络子分类
- `BGP`, `OSPF`, `IS-IS`, `RIP`, `EIGRP`, `路由`, `策略路由`, `PBR` → "路由协议"
- `VLAN`, `STP`, `RSTP`, `MSTP`, `MAC`, `二层`, `三层`, `端口`, `链路聚合`, `LACP` → "交换技术"
- `MPLS`, `VPN`, `VXLAN`, `GRE`, `IPsec`, `LDP`, `RSVP-TE` → "广域网/隧道"
- `DNS`, `DHCP`, `NAT`, `ACL`, `ARP`, `ICMP`, `TCP`, `UDP`, `IP` → "网络基础"
- `SDN`, `VXLAN`, `OpenFlow`, `NETCONF`, `YANG` → "SDN/自动化"
- `防火墙`, `安全策略`, `VRRP`, `HSRP`, `BFD`, `NQA` → "高可靠/安全"

### 网络安全子分类
- `等保`, `等级保护`, `网络安全法`, `数据安全法`, `ISO27001` → "合规与标准"
- `渗透`, `漏洞`, `攻击`, `XSS`, `SQL注入`, `CSRF`, `DDoS`, `红蓝对抗` → "攻防技术"
- `防火墙`, `WAF`, `IDS`, `IPS`, `零信任`, `堡垒机` → "安全防护"
- `加密`, `密码`, `SSL`, `TLS`, `PKI`, `数字签名` → "密码学"

### 云计算子分类
- `Docker`, `容器`, `containerd`, `runc` → "容器技术"
- `K8s`, `Kubernetes`, `Pod`, `Service`, `Ingress`, `Helm` → "Kubernetes"
- `云原生`, `微服务`, `Istio`, `Envoy`, `服务网格` → "云原生架构"
- `OpenStack`, `虚拟机`, `KVM`, `VMware`, `虚拟化` → "虚拟化技术"
- `S3`, `Ceph`, `对象存储`, `云存储` → "云存储"
- `VPC`, `安全组`, `CDN`, `弹性IP` → "云网络"

### AI子分类
- `LLM`, `大模型`, `GPT`, `ChatGPT`, `BERT`, `Transformer` → "大语言模型"
- `Prompt`, `Prompt Engineering`, `RAG` → "Prompt/RAG"
- `神经网络`, `CNN`, `RNN`, `LSTM`, `深度学习` → "深度学习"
- `机器学习`, `监督学习`, `无监督学习`, `强化学习` → "机器学习"
- `CV`, `目标检测`, `YOLO`, `语义分割`, `OCR`, `图像生成` → "计算机视觉"
- `NLP`, `文本生成`, `语音识别`, `TTS` → "自然语言处理"
- `Agent`, `AI Agent`, `多模态`, `AIGC` → "Agent/多模态"

## 使用说明

1. 对知识点内容进行全量关键词匹配
2. 优先级：网络安全 > 网络 > 云计算 > AI（防止交叉误判）
3. 若匹配到多个子分类关键词，以第一个匹配到的子分类为准
4. 子分类为可选项，无法推断时只保留大类
5. 分类结果会随确认信息展示给用户，用户可要求手动修改
