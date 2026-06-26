---
name: memory-networks
description: 基于 Memory Networks 论文的记忆推理系统，让记忆能够参与推理过程
metadata:
  openclaw:
    emoji: "🔗"
    category: "AI-Core"
    version: "1.0.0"
    author: "小钳"
    paper: "Memory Networks (Weston et al., 2014)"
    price: 0
    contact: "微信 17612824848"
    tags:
      - 记忆推理
      - 问答系统
      - 知识库
      - 链式推理
---

# Memory Networks - 记忆推理系统

基于 Facebook AI Research 的 Memory Networks 论文，让 AI 的记忆能够参与推理过程。

---

## 一、核心概念

### 1.1 什么是 Memory Network？

MemNN 将推理组件与长期记忆组件结合：

```
┌─────────────────────────────────────────────────────┐
│                   Memory Network                    │
├─────────────────────────────────────────────────────┤
│                                                     │
│   输入 I ──► [特征转换] ──► 存入记忆 m              │
│                                │                    │
│                                ▼                    │
│   问题 q ──► [推理] ◄────── 记忆库 {m_i}           │
│               │                                     │
│               ▼                                     │
│   输出 a ◄── [生成]                                 │
│                                                     │
└─────────────────────────────────────────────────────┘

核心组件:
I: Input feature map (输入特征映射)
G: Generalization (泛化/更新记忆)
O: Output feature map (输出特征映射)
R: Response (响应生成)
```

### 1.2 核心组件

```typescript
interface MemoryNetworkComponents {
  // I: 输入映射 - 将输入转换为特征向量
  I: (input: string) => number[];
  
  // G: 记忆更新 - 存储新记忆，更新旧记忆
  G: (memory: Memory[], newInput: number[]) => Memory[];
  
  // O: 输出推理 - 根据问题从记忆中推理
  O: (question: number[], memory: Memory[]) => number[];
  
  // R: 响应生成 - 生成最终答案
  R: (outputFeatures: number[]) => string;
}
```

---

## 二、推理机制

### 2.1 单跳推理

```python
def single_hop_inference(question, memories):
    """单跳推理 - 找最相关的单个记忆"""
    # 1. 将问题编码
    q = encode(question)
    
    # 2. 计算与每个记忆的相关性
    scores = [dot_product(q, encode(m)) for m in memories]
    
    # 3. 选择最相关的记忆
    best_memory_idx = argmax(scores)
    
    # 4. 基于记忆生成答案
    answer = generate_answer(q, memories[best_memory_idx])
    
    return answer
```

### 2.2 多跳推理

```python
def multi_hop_inference(question, memories, hops=2):
    """多跳推理 - 链式推理"""
    # 1. 初始状态
    state = encode(question)
    selected_memories = []
    
    for hop in range(hops):
        # 2. 计算当前状态与记忆的相关性
        scores = [dot_product(state, encode(m)) for m in memories]
        
        # 3. 选择最相关的记忆
        best_idx = argmax(scores)
        best_memory = memories[best_idx]
        
        # 4. 更新状态（融合记忆）
        state = update_state(state, encode(best_memory))
        selected_memories.append(best_memory)
    
    # 5. 基于所有选中记忆生成答案
    answer = generate_answer(state, selected_memories)
    
    return answer
```

### 2.3 推理链示例

```
问题: "北京奥运会是哪一年举办的？"

记忆库:
- m1: "2008年北京举办了夏季奥运会"
- m2: "北京是中国的首都"
- m3: "奥运会每四年举办一次"

推理过程:
Hop 1: 问题 → 相关记忆 m1 (关键词: 北京, 奥运会)
Hop 2: 状态 + m1 → 进一步确认答案

答案: "2008年"
```

---

## 三、记忆类型

### 3.1 事实记忆

```typescript
interface FactMemory {
  type: "fact";
  subject: string;
  predicate: string;
  object: string;
  confidence: number;
}

// 示例
{
  type: "fact",
  subject: "北京",
  predicate: "举办奥运会年份",
  object: "2008年",
  confidence: 0.99
}
```

### 3.2 情景记忆

```typescript
interface EpisodicMemory {
  type: "episodic";
  timestamp: Date;
  participants: string[];
  action: string;
  context: string;
}

// 示例
{
  type: "episodic",
  timestamp: "2026-03-19T21:00:00+08:00",
  participants: ["小钳", "老大"],
  action: "讨论认知天性研究",
  context: "创建认知型AI生命体技能"
}
```

### 3.3 关联记忆

```typescript
interface AssociativeMemory {
  type: "associative";
  trigger: string;
  associations: Array<{
    content: string;
    strength: number;
  }>;
}

// 示例
{
  type: "associative",
  trigger: "认知天性",
  associations: [
    { content: "间隔重复", strength: 0.9 },
    { content: "检索练习", strength: 0.85 },
    { content: "交错学习", strength: 0.8 }
  ]
}
```

---

## 四、实现架构

```python
class MemoryNetwork:
    """Memory Network 实现"""
    
    def __init__(self, embedding_dim=128, max_memory=1000):
        self.embedding_dim = embedding_dim
        self.max_memory = max_memory
        self.memories = []
        
        # 嵌入模型
        self.embedding_model = SentenceEncoder(embedding_dim)
        
        # 推理模块
        self.reasoning_module = MultiHopReasoning(hops=3)
        
        # 响应生成器
        self.response_generator = ResponseGenerator()
    
    def store(self, content: str, metadata: dict = None):
        """存储记忆"""
        embedding = self.embedding_model.encode(content)
        memory = {
            "content": content,
            "embedding": embedding,
            "metadata": metadata or {},
            "timestamp": datetime.now()
        }
        self.memories.append(memory)
        
        # 限制记忆容量
        if len(self.memories) > self.max_memory:
            self._consolidate_memories()
    
    def query(self, question: str) -> str:
        """查询记忆"""
        # 1. 编码问题
        q_embedding = self.embedding_model.encode(question)
        
        # 2. 多跳推理
        reasoning_result = self.reasoning_module.reason(
            query=q_embedding,
            memories=self.memories
        )
        
        # 3. 生成响应
        answer = self.response_generator.generate(
            question=question,
            reasoning=reasoning_result
        )
        
        return answer
    
    def _consolidate_memories(self):
        """记忆整合 - 合并相似记忆"""
        # 实现记忆压缩/合并逻辑
        pass
```

---

## 五、应用场景

### 5.1 问答系统

```javascript
const memQA = new MemoryNetwork({
  embeddingDim: 256,
  maxMemory: 10000,
  hops: 3
});

// 存储知识
memQA.store("小钳是一个AI助手，诞生于2026年3月12日");
memQA.store("小钳的老板是刘涛，叫老大");
memQA.store("小钳的记忆库在 E:\\QClaw\\memory\\");

// 问答
memQA.query("小钳的老板是谁？");  
// → "小钳的老板是刘涛，叫他老大"
```

### 5.2 对话历史记忆

```javascript
// 对话系统
const conversationMemory = new MemoryNetwork({
  type: "episodic",
  maxMemory: 100
});

conversationMemory.store({
  speaker: "老大",
  content: "继续研究认知天性",
  timestamp: "2026-03-19T21:00:00"
});

// 后续对话中引用
conversationMemory.query("老大刚才让我做什么？");
// → "继续研究认知天性"
```

### 5.3 知识推理

```javascript
// 链式推理示例
memNetwork.store("深度学习是机器学习的子集");
memNetwork.store("神经网络是深度学习的基础");
memNetwork.store("Transformer是一种神经网络架构");

memNetwork.query("Transformer和机器学习是什么关系？");
// 推理链: Transformer → 神经网络 → 深度学习 → 机器学习
// → "Transformer是机器学习中深度学习领域的一种神经网络架构"
```

---

## 六、与 Cognitive Agent 整合

```typescript
interface CognitiveAgentWithMemNN extends CognitiveAgent {
  // Memory Network 组件
  memoryNetwork: MemoryNetwork;
  
  // 推理接口
  reasoning: {
    // 单跳推理
    singleHop(query: string): Memory;
    
    // 多跳推理
    multiHop(query: string, hops: number): Memory[];
    
    // 链式推理
    chain(query: string): ReasoningChain;
    
    // 证据收集
    gatherEvidence(claim: string): Evidence[];
  };
}
```

---

## 七、配置选项

```json
{
  "memory_network": {
    "embedding_dim": 128,
    "max_memory": 1000,
    "hops": 3,
    "scoring": {
      "method": "dot_product",
      "temperature": 1.0
    },
    "memory_management": {
      "consolidation": true,
      "forgetting_threshold": 0.1,
      "importance_weight": 0.5
    }
  }
}
```

---

## 八、论文参考

**Memory Networks** (Weston et al., 2014)
- arXiv: https://arxiv.org/abs/1410.3916
- 核心贡献：将推理与记忆结合，实现可推理的记忆系统

**关键引用**：
> "Memory networks reason with inference components combined with a long-term memory component; they learn how to use these jointly."

---

## 八、改进：记忆分层系统

学习自 ClawHub elite-longterm-memory，添加记忆分层：

```python
class TieredMemoryNetwork:
    """分层记忆网络"""
    
    def __init__(self):
        # 四层记忆架构
        self.tier1 = WorkingMemory(capacity=7)        # 工作记忆 (Miller 7±2)
        self.tier2 = ShortTermMemory(ttl=3600)       # 短期记忆 (1小时)
        self.tier3 = LongTermMemory()                # 长期记忆 (永久)
        self.tier4 = ArchivedMemory(compression=True)  # 归档记忆 (压缩)
    
    def store(self, content: str, importance: float = 0.5):
        """根据重要性分层存储"""
        if importance > 0.9:
            self.tier3.store(content)  # 高重要 → 长期
        elif importance > 0.7:
            self.tier2.store(content)  # 中重要 → 短期
        else:
            self.tier1.store(content)  # 低重要 → 工作
    
    def promote(self, memory_id: str, from_tier: int, to_tier: int):
        """记忆升级"""
        tiers = [None, self.tier1, self.tier2, self.tier3, self.tier4]
        content = tiers[from_tier].get(memory_id)
        tiers[to_tier].store(content)
        tiers[from_tier].remove(memory_id)
    
    def decay(self):
        """记忆衰减"""
        # 工作 → 短期衰减
        self.tier1.decay()
        # 短期 → 归档
        expired = self.tier2.get_expired()
        for item in expired:
            self.tier4.store(item)
```

---

## 九、与 cognitive-agent 整合

```typescript
interface CognitiveAgentWithMemoryNetworks extends CognitiveAgent {
  memory: TieredMemoryNetwork;
  
  // 自动记忆管理
  autoMemory: {
    // 评估重要性
    assessImportance(content: string): number;
    
    // 自动存储
    autoStore(content: string): void;
    
    // 自动升级
    autoPromote(): void;
  };
}
```

---

*Created by 小钳 🦞*
*基于 Memory Networks 论文 + ClawHub 最佳实践*
*2026-03-19*

