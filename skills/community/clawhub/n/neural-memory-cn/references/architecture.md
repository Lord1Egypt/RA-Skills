# Neural Memory Architecture / 神经记忆架构

## Overview / 概述

**English**: The neural memory system is inspired by how human memory works, using concepts from cognitive science and neuroscience.

**中文**: 神经记忆系统受人类记忆工作方式的启发，采用认知科学和神经科学的概念。

- **Neurons / 神经元**: represent knowledge units (concepts, facts, experiences) / 表示知识单元（概念、事实、经验）
- **Synapses / 突触**: represent connections between knowledge / 表示知识之间的连接
- **Activation Spreading / 激活扩散**: models how memories are retrieved through association / 模拟记忆如何通过联想被检索
- **Intent Layer / 意图层**: provides intelligent query understanding / 提供智能查询理解

---

## System Architecture / 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                      ThinkingModule / 思维模块                    │
│  ┌───────────────┐  ┌───────────────────┐  ┌─────────────────┐  │
│  │  Intent Layer │  │  Semantic Engine  │  │  Spreading Eng. │  │
│  │  意图层       │  │  语义引擎         │  │  扩散引擎       │  │
│  │  (Query       │  │  (Similarity      │  │  (Activation    │  │
│  │   Analysis)   │  │   Matching)       │  │   Propagation)  │  │
│  └───────┬───────┘  └─────────┬─────────┘  └────────┬────────┘  │
│          │                    │                     │           │
│          └────────────────────┼─────────────────────┘           │
│                               │                                 │
│                    ┌──────────▼──────────┐                      │
│                    │  LazyStorageManager │                      │
│                    │  惰性存储管理器     │                      │
│                    └──────────┬──────────┘                      │
└───────────────────────────────┼─────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
   ┌────▼────┐            ┌─────▼─────┐           ┌─────▼─────┐
   │ L1: Hot │            │ L2: Index │           │ L3: Files │
   │ Cache   │            │ (Metadata)│           │ (JSON)    │
   │ 热缓存  │            │ 索引      │           │ 文件存储  │
   │ (LRU)   │            │           │           │           │
   └─────────┘            └───────────┘           └───────────┘
```

---

## Memory Retrieval Flow / 记忆检索流程

### Smart Mode / 智能模式

```
User Query / 用户查询
    │
    ▼
┌─────────────────────┐
│ Intent Analysis     │  意图分析
│ - Extract concepts  │  - 提取概念
│ - Detect intent     │  - 检测意图
│ - Find related      │  - 查找相关
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ On-Demand Loading   │  按需加载
│ - Load related      │  - 仅加载相关
│   neurons only      │    神经元
│ - Use semantic      │  - 使用语义
│   similarity        │    相似度
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Activation Spreading│  激活扩散
│ - Start from seeds  │  - 从种子开始
│ - Spread through    │  - 通过突触
│   synapses          │    扩散
│ - Apply decay       │  - 应用衰减
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Result Ranking      │  结果排序
│ - Sort by           │  - 按激活值
│   activation        │    排序
│ - Filter threshold  │  - 阈值过滤
│ - Return top N      │  - 返回前N个
└─────────────────────┘
```

---

## Activation Spreading Algorithm / 激活扩散算法

**English**: The core algorithm implements the **Spreading Activation** theory from cognitive psychology.

**中文**: 核心算法实现了认知心理学中的**激活扩散**理论。

```python
def spread(query_neuron_id, max_depth=3, decay_factor=0.8):
    activations = {query_neuron_id: 1.0}
    frontier = [query_neuron_id]
    
    for depth in range(max_depth):
        new_frontier = []
        for current_id in frontier:
            current_activation = activations[current_id]
            synapses = get_synapses_from(current_id)
            
            for synapse in synapses:
                transmitted = current_activation * synapse.weight * (decay_factor ** depth)
                target_id = synapse.toNeuron
                
                if target_id not in activations:
                    activations[target_id] = 0
                    new_frontier.append(target_id)
                
                activations[target_id] += transmitted
        
        frontier = new_frontier
    
    return sort_and_filter(activations)
```

### Parameters / 参数

| Parameter | Default | Range | Description (EN) | Description (CN) |
|-----------|---------|-------|------------------|------------------|
| max_depth | 3 | 1-5 | How many hops to spread | 扩散跳数 |
| decay_factor | 0.8 | 0.5-0.9 | Activation decay per depth | 每层衰减因子 |
| min_activation | 0.15 | 0.0-0.5 | Minimum threshold to include | 最小激活阈值 |
| result_limit | 20 | 1-100 | Maximum results returned | 最大返回结果数 |

---

## Three-Tier Storage / 三层存储

### L1: Hot Cache (LRU) / 热缓存

- **Purpose / 用途**: Fast access to frequently used neurons / 快速访问常用神经元
- **Size / 大小**: Configurable (default: 100 neurons) / 可配置（默认：100个神经元）
- **Eviction / 淘汰**: Least Recently Used / 最近最少使用
- **Hit Rate / 命中率**: Typically 80%+ for active sessions / 活跃会话通常80%以上

### L2: Neuron Index / 神经元索引

- **Purpose / 用途**: Lightweight metadata for fast lookups / 轻量级元数据用于快速查找
- **Contents / 内容**: ID, name, type, tags, activation count
- **Memory / 内存**: Minimal compared to full neuron content / 相比完整神经元内容占用最小
- **Operations / 操作**: Name search, tag search, type filter

### L3: File Storage / 文件存储

- **Format / 格式**: JSON files / JSON文件
- **Location / 位置**: `memory_long_term/neurons.json`
- **Synapses / 突触**: Individual files per neuron in `synapses/` / 每个神经元的独立文件
- **Persistence / 持久化**: Survives restarts / 重启后保留

---

## Intent Understanding Layer / 意图理解层

### Concept Extraction / 概念提取

```python
def extract_concepts(query):
    concepts = []
    
    # 1. Domain keyword matching / 领域关键词匹配
    for domain, keywords in DOMAIN_KEYWORDS.items():
        for kw in keywords:
            if kw in query:
                concepts.append(domain)
                concepts.append(kw)
    
    # 2. N-gram extraction (Chinese) / N-gram提取（中文）
    concepts.extend(re.findall(r'[\u4e00-\u9fa5]{2,4}', query))
    
    # 3. LLM enhancement (optional) / LLM增强（可选）
    if use_llm:
        concepts.extend(llm_extract(query))
    
    return unique(concepts)
```

### Intent Detection / 意图检测

| Intent | Patterns (EN) | Patterns (CN) |
|--------|---------------|---------------|
| question | how, why, what, which | 怎么, 如何, 为什么, 什么是, 有哪些, ? |
| request | help me, please, find | 帮我, 请, 查一下, 找一下 |
| statement | I think, I believe | 我想, 我认为, 我觉得 |

---

## Semantic Similarity Engine / 语义相似度引擎

### Embedding-Based / 基于嵌入（可用时）

```python
def compute_similarity(query_embedding, neuron_embedding):
    # Cosine similarity / 余弦相似度
    dot = sum(a * b for a, b in zip(query_embedding, neuron_embedding))
    norm_a = sqrt(sum(a * a for a in query_embedding))
    norm_b = sqrt(sum(b * b for b in neuron_embedding))
    return dot / (norm_a * norm_b)
```

### Keyword-Based / 基于关键词（回退）

```python
def keyword_similarity(query, neuron):
    score = 0.0
    
    # Name matching / 名称匹配
    if neuron.name.lower() in query.lower():
        score += 0.8
    
    # Tag matching / 标签匹配
    for tag in neuron.tags:
        if tag.lower() in query.lower():
            score += 0.3
    
    # Content matching / 内容匹配
    query_words = set(query.lower().split())
    content_words = set(neuron.content.lower().split())
    overlap = len(query_words & content_words)
    score += 0.1 * overlap
    
    return min(score, 1.0)
```

---

## Synapse Types / 突触类型

| Type | Weight | Description (EN) | Description (CN) |
|------|--------|------------------|------------------|
| domain_related | 0.7-0.9 | Same knowledge domain | 同一知识领域 |
| shared_tag | 0.3-0.6 | Share common tags | 共享标签 |
| similarity | 0.5-0.8 | Semantic similarity | 语义相似 |
| causality | 0.6-0.8 | Cause-effect relationship | 因果关系 |
| example | 0.4-0.6 | Illustrative example | 示例说明 |

---

## Memory Consolidation / 记忆巩固

### Reinforcement / 强化

```python
def reinforce_synapse(synapse, delta=0.1):
    synapse.weight = min(1.0, synapse.weight + delta)
    synapse.reinforcementCount += 1
    synapse.lastReinforced = now()
```

### Decay / 衰减

```python
def decay_synapse(synapse, factor=0.95):
    synapse.weight *= factor
    # Prune if below threshold / 低于阈值时修剪
    if synapse.weight < 0.1:
        delete_synapse(synapse)
```

### Maintenance / 维护

**English**: Run periodically to maintain memory health.

**中文**: 定期运行以维护记忆健康。

```python
module.run_maintenance()
# - Decay old synapses / 衰减旧突触
# - Prune low-confidence connections / 修剪低置信度连接
# - Optimize storage / 优化存储
```

---

## Performance Considerations / 性能考虑

### Memory Usage / 内存使用

- Hot cache / 热缓存: ~1KB per neuron / 每个神经元约1KB
- Index / 索引: ~100 bytes per neuron / 每个神经元约100字节
- Full storage / 完整存储: Depends on content size / 取决于内容大小

### Query Latency / 查询延迟

| Mode | Typical Latency / 典型延迟 |
|------|---------------------------|
| exact | <10ms |
| smart (local) | 50-100ms |
| smart (LLM) | 500-2000ms |

### Optimization Tips / 优化建议

1. Increase hot cache size for frequent access patterns / 增加热缓存大小以适应频繁访问模式
2. Pre-compute embeddings for semantic search / 预计算嵌入以进行语义搜索
3. Define domain relationships for accurate spreading / 定义领域关系以实现准确扩散
4. Run maintenance regularly to prune weak connections / 定期运行维护以修剪弱连接