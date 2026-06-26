# Talk Tracks Library (领域话术库)

本文档包含 22 个研究领域的专业话术，用于与候选人进行技术交流时参考。

## 使用方法

1. **确定候选人领域**: 使用 `field-mappings.md` 确定候选人的标准化研究领域
2. **选择话术**: 从对应领域的话术中选择 2-3 条与候选人研究最相关的
3. **融入交流**: 将话术自然地融入邮件或对话中，体现对领域的深度理解

---

## 1. RL (强化学习)

### 专业话术
- 什么样的 reward signal 能更匹配LLM 的策略优化，以及怎么样的 signal 能够提供更陡峭的 test time scaling 曲线
- 研究 rlhf 过程中的 reward hacking 问题的机理和优化方案
- 如何从算法设计和数据合成来提升 reasoning 能力
- 是否应该设计 process reward model 让模型能够探索不确定性更高、不确定且没有标准答案的领域
- Multi agent 的RL系统 vs 大规模scale 环境 哪个会更有效

### FDE 范式话术
- **Self loop + FDE**: 通过 FDE 范式帮助 self loop 搭建真实场景中的 evolve 管线，收集更贴合应用场景的关键数据
- **跨领域科学假设**: 如将凝聚物理学的重整化群概念结合到预训练过程中，提升不同场景任务下的数据结构处理
- **跨领域寻找idea**: 如姚舜宇将认知心理学的 "how human solve complex problem" 结合到 AI agent 方向，发明 Tree of Thoughts

---

## 2. Pre/Post-train × RL (模型自我进化)

### 专业话术
- 模型自我进化（Self-Adapting LLMs）Closed-Loop, self-evolution 方向，Anthropic 团队遇到的困难是大量模型训练数据缺失
- 字节的 Tianle Cai 团队遇到的困难是模型在多步任务之后丧失学习能力，缺少长期使命和 reward
- Claude Finance 落地过程中发现模型自动寻找 Reward Function 能力不足，无法在新环境中抽象更高效的有损压缩

---

## 3. NLP (自然语言处理)

### 专业话术
- 下一个阶段如何进一步提升模型的 reasoning 能力，以及如何通过各种新的合成数据去创造大量的 long horizon 和 long tail 数据
- Long-horizon reasoning 在多模态时代对于 general reasoning 能力的启发以及对于 long tail knowledge 的数据合成
- Billion级别的 long context 能够启发的对于 general reasoning 能力提升的理论研究
- 如何利用数据提升模型未来能力的 upper bound，如何去寻找更适合系统的模型架构调整以提升训练效率
- IR 技术在整合 LLM 与外部数据库以实现高效信息检索方面的应用，特别是在 RAG 框架下
- LLM 鲁棒性，特别是从 internal consistency 入手做 evaluate 和 improve

---

## 4. MOE (混合专家)

### 专业话术
- 从去年年初的 Dynamic MoE，到 Deepseek 的创新 MoE 架构，MoE 领域新进展带来的模型 Inference 效率提升
- 如何在已有的 MoE 模型上进行更高效、选择性地微调
- 如何在已有的 MoE 模型上自动且动态添加/修改/删除专家
- 如何将 MoE 应用在 Multimodal 上

---

## 5. EVAL (评估)

### 专业话术
- 动态的 Eval 项目，用工具插件和多模态来做 Eval，判断 reasoning 在不同 Domain 的 trajectory
- 随着 o1 开启的 inference time scaling 时代，探究 o1 的实验方法和针对未来模型能力点的 benchmark 设定：
  1) 如何定义 o1 时代的高质量数据；如何将 o1 的能力泛化到其他能力（数学物理之外）
  2) 如何开创性地沿着未来模型能力点去做一些 benchmark，data set 如何更好地去获取

---

## 6. data (数据)

### 专业话术
- 数据是大模型能力的上限，探索什么是这个时代所谓更高质量的 data、合成数据更好的方法
- 如何利用数据提升模型未来能力的 upper bound，如何去寻找更适合系统的模型架构调整以提升训练效率
- 更好的数据来提升数学 reasoning 能力上限的方法

---

## 7. AI4S (AI for Science)

### 专业话术
- **蛋白质设计与结构生物学**: 模型是否具备内在的物理引擎驱动，如 DeepMind 的 AlphaFold 通过深度学习与进化信息结合
- **药物分子设计与细胞模拟**: 模型能否结合高精度的分子动力学模拟或细胞级动力学约束
- **材料科学与计算材料**: 模型能否融入多尺度的原子级模拟与高通量筛选框架
- **气候与地球科学**: 模型能否结合高分辨率的气候模拟与地球系统动力学
- **自动化实验与机器人**: 机器到底能否真正发现新科学，如何将人类的假设生成能力与机器的高通量探索有效结合
- **理论数学与物理**: 模型能否结合符号推理、数值模拟与定理证明系统
- **生物医学成像**: 模型能否融合多模态影像数据、物理成像原理与生物学先验知识

---

## 8. Audio (语音)

### 专业话术
- a16z 发布的语音 AI 赛道洞察：语音将成为关键的切入点，而不是最终产品本身
- 跨模态的端到端模型相关问题：
  1) 类似于 Qwen2.5-Omni 的双通道/多通道编码/运算架构是否是多模态在序列上拼接并实现对齐的唯一解决范式
  2) 如何通过多个编码器或运算通道将不同模态的 token 实现拼接并将模态间的偏好实现对齐
  3) 针对 audio 模态进行单通道编码及运算，是否真的可以既保留副语义信息，又可以捕捉到语义信息
  4) 全双工的交互方式是否是 SpeechLM 的交互方式发展趋势
  5) 如何解决全双工交互时的时延问题

---

## 9. MLSys (机器学习系统)

### 专业话术
- 大规模 Pretrain 需要的异步训练系统 auto-scaler，自动并行以及软硬件 co-design 的 efficiency 方向
- 模拟计算和下一代模拟芯片与大模型训练和推理的共同演进
- 如何用数据提升模型能力上限，从 efficiency 和优化角度提升训练率
- Scaling law 的 ROI 已经逐步下降，相信在理论算法层面还存在从 CNN 到 ResNet 的跨越机会
- 随着 o1 开启的 Inference time scaling 时代，以及多模态模型在 workload 上变得越来越异构：
  1) 如何设计更好的 Inference task scheduling system，把 GPU 的 MFU 再往上提
  2) 未来如果 Inference Time Scale 到 1 天、5 天甚至更长之后，Infra 的压力会在哪里
  3) 多模态异构 workload 从 Infra 和 MLSys 的角度如何适配

---

## 10. LLM4CODE (代码生成)

### 专业话术
- LLM 在 Code 和 Math domain 上的 reasoning 能力还有很大的提升空间
- 围绕收集/合成更高质量的 Code/Math Data 的需求在大大增加
- 一些 researcher 在尝试把形式化证明等 Reasoning 能力放在 Code 之外的领域上
- 模型在 RL 范式下训练的能力天花板会在哪里，在代码领域模型的能力上限是什么
- Software Testing & GUI & LLM 这个方向，AI Agent 产品的测试还是非常耗费人工的，有蛮多的商业化落地场景

---

## 11. Multimodal (多模态)

### 专业话术
- 下一个阶段如何进一步提升 diffusion model 的生成质量和效率
- 如何通过各种新的采样策略和模型架构改善模型在复杂场景和长序列生成上的表现
- 视频的理解只停留在 abstract 的阶段，无法涵括所有细节，环境中细微的变化无法得到感知
- 如何用精确的数据在多帧间插入时间戳，用类似语言学习的方法让模型感知时间
- 未来是否会出现原生多模态模型，实现多模态与时间的直接对齐
- VLM 的未来发展：
  1) 如何设计更好的 Encoder/backbone
  2) 如何跳出基于语言模型 SFT 范式的 VLM 训练，探索原生视觉模型
  3) 如何定义价值更高的多模态数据范式
  4) 如何设计更好的 Long Video Understanding 的学习方式和训练系统

---

## 12. Pre-training (预训练)

### 专业话术
- 如何利用数据提升模型未来能力的 upper bound
- 如何去寻找更适合系统的模型架构调整以提升训练效率以及合成数据
- 更好的数据来提升数学 reasoning 能力上限的方法
- Pre-training Scaling Law 不断下降的今天，通过 Refine Pre-training pipeline data，或把更多高质量的 CoT 数据放进预训练数据中，还是能让 Base Model 能力进一步提高

---

## 13. post-train (后训练)

### 专业话术
- 模型在 continual pretrain 的时候如何解决模型学习效率可塑性降低的问题
- 有哪些维度的能力是目前多模态模型没有很好能够衡量到的
- 通过 RL 的范式进一步找到在数学之外的领域里边 reasoning 的踪迹和训练方法论
- Anthropic 在 characteristics 探索贯穿了整个训练过程，在其他 domain 上有时像回撤这样的 reasoning 能力，它预训练中提供的起始点跟数学很不一样

---

## 14. Alignment (对齐)

### 专业话术
- 在特定 domain 下快速找到 reward signal，以及未来 scalable oversight system 如何设计来实现 super alignment
- 随着 test time scaling law 的出现，还有哪些方向值得继续 scaling
- 怎么大规模地搭建更 diverse 的 test time scaling 的方式，来反哺 post train 的数据集
- 模型进展到今天有什么产品启发的模型设计方式
- 如何继续提升模型的 context length 和 incontext learning 的能力

---

## 15. Reasoning (推理)

### 专业话术
- o1 的实验方法和未来持续提高模型 Reasoning 能力的基础组件迭代方法：
  1) 是否应该设计 process reward model 以及如何设计比 system 2 更长期有效的 reward 机制
  2) 如何定义 o1 时代的高质量数据；如何将 o1 的能力泛化到其他能力
  3) 未来自动化形式验证器 like lean 还有哪些值得优化迭代的地方
- 如何借助 o1 的 test time scaling 的方法，赋予模型在做错事情时候能够提前止损的能力
- 在解决不同问题的时候，能够通过 pattern matching 使用更多来自其他领域的技能

---

## 16. Agent&RAG (智能体与检索)

### 专业话术
- Multi-Agents 的 simulation，比如存在多个 AI Agent 或者 100 个基于同一个 foundation model 的 individual
- 更好的 web agent 如何系统性地抽取通用的可评估能力，寻找网页之间长序列任务的模型推理能力
- RAG 在工业界使用的 pipeline，同时关注 GraphRag、LongContext 等方向前沿的突破和瓶颈
- 通过 knowledge graph 来提升 agent 在每家企业和不同领域落地时候回答问题的准确性
- 如何利用 o1 CoT 来解决 hallucination 的问题

---

## 17. Interpretable AI (可解释AI)

### 专业话术
- 寻找从数据到 gradient 到 system 之间联系的话题
- 从 tensor program 到 Anthropic 的 A Mathematical Framework for Transformer Circuits 再到 Allen Zhu 的 Physics of LLM
- 今天的模型 reasoning 能力上限和接下来 scaling law 的可持续性和瓶颈都将在这个话题中被探索出来

---

## 18. Embodiment (具身智能)

### 专业话术
- LLM-based robot planning，在多步骤以及多轮交互的复杂任务下，用 RL 的思路提升模型分步完成任务的成功率
- Low Level 场景下，如何在未来训练出一个更好的 Planning/执行的 VLA Model
- 全网 2D videos 通过单目深度估计的技术 convert 成双目 3D videos，然后让 Model 去学习空间感知能力和人的 action
- Multimodal understanding 会将全网的视频都吸收，如果能将模仿学习 + RL 获得具身到海量视频知识之间的链接将是高价值成果
- 端到端的落地数据闭环飞轮上，比亚迪的国内 8 个生产基地和智源机器人为什么没有特别好的办法落地在主产线上
- 如何让视觉与动作生成之间的耦合更加紧密，尤其是在复杂操作任务中如何建立更稳定、更具有层次感的感知—决策映射

---

## 19. Computer Vision (计算机视觉)

### 专业话术
- 如何利用更好的数据，寻找更合适的模型架构实现高效精准的视觉追踪
- 如何构建 CV 未来的 backbone
- 为了构建下一代原生视觉视频为主需要的数据合成工序管线
- 如何把视频里的物体在时间上的变化、动作、环境、镜头等元素用更好的数据集和更好的训练方式去捕捉到
- 从 GAN、NeRF、diffusion 到现在的 physical intelligence，哪些好的启发性的算法能够对于神经网络、对于 3D、语言等信息的压缩和表达有更好地表征能力
- 沿着 3D Generation，如何解决多视角不一致、生成过程中通过 object box 解决生成数量不一致、Text-to-3D 生成中的乱码问题

---

## 20. Recommendation System (推荐系统)

### 专业话术
- LLM & recommendation system 在一些行为数据不够丰富的场景下，也能发挥比较不错的效果，upper bound 会在哪里
- 在抖音、TK 类的短视频内容平台上，普通用户一年会贡献 40 万到 100 万的数据，如何持续提升模型的学习效率，data-efficiency 不断提高

---

## 21. Federated Learning (联邦学习)

### 专业话术
- 通过联邦学习等方法破解模型的鲁棒性，发掘黑盒模型的安全性
- 如何提升大模型的鲁棒性，探索 reasoning、灾难性遗忘、data recipe 以及 training curriculum 之间的关联
- "可验证删除"正在由经验对比向可证明的认证过渡，但现有证明多依赖强假设
- 训练部署一体化的"可删性"设计更关键：单点 unlearning 补丁在持续学习、增量数据、缓存与蒸馏管线中易"再污染"
- 在仅黑盒访问部署模型的现实约束下，如何设计"删除证明"的可执行协议

---

## 22. Trustworthy AI (可信AI)

### 专业话术
- o1 时代，如何构建下一代模型算法减少模型幻觉提升模型可信度：
  1) 未来模型不使用 PRM 的情况下，如何继续保证模型的安全性
  2) 如何定义 o1 时代的高质量数据；如何将 o1 的能力泛化到其他能力
  3) 如何开创性地沿着未来模型能力点去做一些 benchmark

---

## 通用话术 (适用于所有领域)

### FDE (Forward Deploy Engineer) 范式话术

1. **Self loop + FDE**: 通过 FDE 范式帮助 self loop 搭建真实场景中的 evolve 管线。FDE 让模型 agent 部署到场景时能够有驻场，个性化解决，做 training as service，整个全栈 AI 搭建 as service。只有通过这个过程才能对模型真实部署到场景中，在真实环境中完成闭环，这个过程的数据对 self loop 构建 evolve 数据集完成训练至关重要。

2. **跨领域提出科学假设**: 将不同领域的知识、经验、理论结合起来，形成新的、有价值的假设。例如将凝聚物理学的重整化群概念结合到预训练过程中，提升不同场景任务下的数据结构处理。

3. **跨领域寻找 idea**: 从很跨行、跨领域追寻久远的重要领域发现，把领域发现的思路结合到最新的论文发表的 idea 的寻找中。例如姚舜宇通过跟认知心理学泰斗的交流，发现 "how human solve complex problem" 并结合到 AI agent 方向，发明 Tree of Thoughts。

4. **FDE 范式与 AI 产业化落地**: FDE 正在改变传统的 ToB 产品交付模式。不同于传统模式的分工协作，FDE 能够从与用户交流确定订单，到技术设计、需求捕捉、客服运维全流程负责。例如 baseten 公司的 15 个 FDE 与 15 个销售配合，通过驻场优化客户 Infra、latency，将标杆客户的解决方案内化为公司产品能力。

5. **从研究到产品的价值转化路径**: 很多优秀的研究成果在实验室环境表现出色，但真正落地到产业场景时会面临各种挑战。相比 Fireworks 只能获取 workflow 进行仿真训练，或 OpenAI 获取全部数据进行真实场景训练，我们更关注如何在保护用户隐私的前提下，通过 FDE 模式获取关键的场景数据和反馈，实现研究成果的产业化转化。

6. **多角色能力融合与全栈价值创造**: FDE 需要具备三个核心能力：对外的客户沟通能力（控制预期、避免过度承诺）、对内的跨部门协调能力（向 Infra、产品、算法团队寻求支持）、以及对自身角色的清晰认知。这种多角色融合的工作模式，能够更快速地响应客户需求，将研究洞察直接转化为产品改进。
