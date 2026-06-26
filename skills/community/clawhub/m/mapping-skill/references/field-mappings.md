# Research Field Mapping (研究领域映射)

本文档定义了 22 个标准化研究领域及其别名映射，用于将候选人的研究方向标准化为统一的领域名称。

## 使用方法

1. **识别研究领域**: 从候选人的个人主页、论文、LinkedIn 等渠道获取其研究方向
2. **标准化映射**: 将研究方向文本与下方的别名列表进行匹配
3. **获取领域描述**: 使用标准化领域名称获取对应的简短描述

## 22 个标准化研究领域

| 标准领域 | 英文别名 | 中文别名 | 领域描述 |
|---------|---------|---------|---------|
| **RL** | RL, Reinforcement Learning, RLHF, PPO, DQN | 强化学习 | 强化学习与策略优化 |
| **Pre/Post-train × RL** | Pre/Post-train, Self-Adapting, self-evolution | 模型自我进化 | 模型自我进化与闭环训练 |
| **NLP** | NLP, Natural Language Processing, LLM, Language Model, Transformer | 自然语言处理, 大语言模型 | 自然语言处理与大语言模型 |
| **MOE** | MOE, MoE, Mixture of Experts | 混合专家 | 混合专家模型架构 |
| **EVAL** | EVAL, Evaluation, Benchmark | 评估, 基准测试 | 模型评估与基准测试 |
| **data** | data, Data-centric, Data Augmentation, Data Synthesis | 数据, 数据中心化, 数据增强 | 数据中心化AI与数据合成 |
| **AI4S** | AI4S, AI for Science, Drug Discovery, Material Science | 科学计算, 药物发现, 材料科学 | AI for Science科学计算 |
| **Audio** | Audio, Speech, TTS, ASR, Voice | 语音, 语音识别, 语音合成 | 语音与音频处理 |
| **MLSys** | MLSys, ML Systems, Distributed, Inference, Training Optimization | 系统, 分布式, 推理优化 | 机器学习系统与优化 |
| **LLM4CODE** | LLM4CODE, Code, Code Generation, Program Synthesis | 代码, 代码生成, 程序合成 | 代码生成与程序合成 |
| **Multimodal** | Multimodal, VLM, Vision-Language, CLIP, Video | 多模态, 视觉语言模型, 视频 | 多模态学习与视觉语言模型 |
| **Pre-training** | Pre-training, Self-supervised, Foundation Model | 预训练, 自监督, 基础模型 | 预训练与基础模型 |
| **post-train** | post-train, Instruction Tuning, Fine-tuning | 后训练, 指令微调, 微调 | 后训练与指令微调 |
| **Alignment** | Alignment, Super Alignment, Safety | 对齐, 安全, 模型对齐 | 模型对齐与安全 |
| **Reasoning** | Reasoning, CoT, Chain-of-Thought, ToT | 推理, 思维链 | 推理能力与思维链 |
| **Agent&RAG** | Agent, RAG, Retrieval, Multi-Agent | 智能体, 检索增强 | 智能体与检索增强生成 |
| **Interpretable AI** | Interpretable, XAI, Explainable | 可解释AI | 可解释AI |
| **Embodiment** | Embodiment, Robotics, Robot, Manipulation | 具身智能, 机器人, 操作 | 具身智能与机器人 |
| **Computer Vision** | Computer Vision, CV, Image, Object Detection, Segmentation | 计算机视觉, 图像, 目标检测 | 计算机视觉 |
| **Recommendation System** | Recommendation, RecSys | 推荐系统 | 推荐系统 |
| **Federated Learning** | Federated Learning, Privacy | 联邦学习, 隐私保护 | 联邦学习 |
| **Trustworthy AI** | Trustworthy, Robustness, Fairness | 可信AI, 鲁棒性, 公平性 | 可信AI与鲁棒性 |

## 映射逻辑

```python
def get_standardized_field(research_field: str) -> str:
    """
    将候选人的研究领域映射到标准化的领域名称

    Args:
        research_field: 候选人的原始研究领域字符串

    Returns:
        标准化的领域名称，如果没有匹配则返回 "default"
    """
    if not research_field:
        return "default"

    research_field_lower = research_field.lower()

    for standard_field, aliases in FIELD_MAPPING.items():
        for alias in aliases:
            if alias.lower() in research_field_lower:
                return standard_field

    return "default"
```

## 领域映射完整列表

### 1. RL (强化学习)
- **英文别名**: RL, Reinforcement Learning, RLHF, PPO, DQN, reward learning, policy optimization, inverse RL, offline RL, batch RL
- **中文别名**: 强化学习, 强化, 策略优化, 奖励学习
- **技术点**: reward signal设计, RLHF优化, reward hacking问题, process reward model, test time scaling

### 2. Pre/Post-train × RL (模型自我进化)
- **英文别名**: Pre/Post-train, Self-Adapting, self-evolution, closed-loop training, self-improving models
- **中文别名**: 模型自我进化, 自适应, 闭环训练
- **技术点**: 数据闭环, evolve数据集, self-loop训练, closed-loop pipeline

### 3. NLP (自然语言处理)
- **英文别名**: NLP, Natural Language Processing, LLM, Language Model, Transformer, BERT, GPT
- **中文别名**: 自然语言处理, 大语言模型, 语言模型
- **技术点**: reasoning能力, long-horizon数据, 合成数据, long context, RAG框架

### 4. MOE (混合专家)
- **英文别名**: MOE, MoE, Mixture of Experts, sparse expert models, dynamic routing
- **中文别名**: 混合专家, 稀疏专家
- **技术点**: MoE架构创新, 动态专家选择, 高效微调, 多模态MoE

### 5. EVAL (评估)
- **英文别名**: EVAL, Evaluation, Benchmark, metrics, automated evaluation
- **中文别名**: 评估, 基准测试, 评测
- **技术点**: 动态评估, reasoning trajectory, benchmark设计, 高质量数据定义

### 6. data (数据)
- **英文别名**: data, Data-centric, Data Augmentation, Data Synthesis, data quality, curriculum learning
- **中文别名**: 数据, 数据中心化, 数据增强, 数据合成
- **技术点**: 高质量数据, 合成数据方法, 数据飞轮, data centric

### 7. AI4S (AI for Science)
- **英文别名**: AI4S, AI for Science, Drug Discovery, Material Science, scientific computing, computational biology
- **中文别名**: 科学计算, 药物发现, 材料科学, 计算生物学
- **技术点**: 物理引擎驱动, 多尺度模拟, 科学发现自动化, 跨学科融合

### 8. Audio (语音)
- **英文别名**: Audio, Speech, TTS, ASR, Voice, speech synthesis, speech recognition
- **中文别名**: 语音, 语音识别, 语音合成
- **技术点**: 端到端多模态, 全双工交互, 跨模态对齐, 语义与副语义信息

### 9. MLSys (机器学习系统)
- **英文别名**: MLSys, ML Systems, Distributed, Inference, Training Optimization, infrastructure
- **中文别名**: 系统, 分布式, 推理优化, 基础设施
- **技术点**: 软硬件co-design, 训练效率优化, 异构workload, inference time scaling

### 10. LLM4CODE (代码生成)
- **英文别名**: LLM4CODE, Code, Code Generation, Program Synthesis, code understanding
- **中文别名**: 代码, 代码生成, 程序合成
- **技术点**: 代码reasoning, 形式化证明, 自动化测试, 代码生成上限

### 11. Multimodal (多模态)
- **英文别名**: Multimodal, VLM, Vision-Language, CLIP, Video, vision-language model
- **中文别名**: 多模态, 视觉语言模型, 视频
- **技术点**: 原生多模态, 视觉语言对齐, 长视频理解, 世界模型

### 12. Pre-training (预训练)
- **英文别名**: Pre-training, Self-supervised, Foundation Model, base model training
- **中文别名**: 预训练, 自监督, 基础模型
- **技术点**: 数据质量提升, 训练效率, CoT数据预训练, 能力上限

### 13. post-train (后训练)
- **英文别名**: post-train, Instruction Tuning, Fine-tuning, SFT, alignment training
- **中文别名**: 后训练, 指令微调, 微调
- **技术点**: continual pretrain, 可塑性, 多模态后训练, reasoning能力

### 14. Alignment (对齐)
- **英文别名**: Alignment, Super Alignment, Safety, AI safety, constitutional AI
- **中文别名**: 对齐, 安全, 模型对齐
- **技术点**: scalable oversight, reward signal探索, super alignment, 安全对齐

### 15. Reasoning (推理)
- **英文别名**: Reasoning, CoT, Chain-of-Thought, ToT, Tree of Thoughts, reasoning models
- **中文别名**: 推理, 思维链
- **技术点**: inference time scaling, process reward model, CoT数据标注, 多领域泛化

### 16. Agent&RAG (智能体与检索)
- **英文别名**: Agent, RAG, Retrieval, Multi-Agent, autonomous agents
- **中文别名**: 智能体, 检索增强, AI Agent
- **技术点**: Multi-Agent系统, 知识图谱, 长序列任务, Agent RL

### 17. Interpretable AI (可解释AI)
- **英文别名**: Interpretable, XAI, Explainable, mechanistic interpretability
- **中文别名**: 可解释AI, 可解释性
- **技术点**: 模型可解释性, reasoning机理, gradient分析, 能力上限探索

### 18. Embodiment (具身智能)
- **英文别名**: Embodiment, Robotics, Robot, Manipulation, embodied AI, sim-to-real
- **中文别名**: 具身智能, 机器人, 操作
- **技术点**: Sim-to-Real, 世界模型, 具身数据, 动作学习

### 19. Computer Vision (计算机视觉)
- **英文别名**: Computer Vision, CV, Image, Object Detection, Segmentation, 3D vision
- **中文别名**: 计算机视觉, 图像, 目标检测
- **技术点**: 视觉backbone, 3D生成, 视频理解, 神经场景表示

### 20. Recommendation System (推荐系统)
- **英文别名**: Recommendation, RecSys, recommender systems
- **中文别名**: 推荐系统
- **技术点**: LLM+推荐, 数据效率, 行为建模

### 21. Federated Learning (联邦学习)
- **英文别名**: Federated Learning, Privacy, differential privacy, distributed learning
- **中文别名**: 联邦学习, 隐私保护
- **技术点**: 隐私保护, 模型鲁棒性, 可验证删除

### 22. Trustworthy AI (可信AI)
- **英文别名**: Trustworthy, Robustness, Fairness, reliability, safety
- **中文别名**: 可信AI, 鲁棒性, 公平性
- **技术点**: 模型安全, 幻觉减少, 可信度提升, benchmark设计

## Default (默认领域)

如果没有匹配到任何具体领域，使用 `default` 作为默认值。
- **描述**: 前沿AI研究
- **技术点**: 前沿技术探索, 模型能力提升, 创新应用场景
