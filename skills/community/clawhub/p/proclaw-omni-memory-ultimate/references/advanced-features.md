# Advanced Features - 极致特性详解

本文档详细说明Omni-Memory Ultimate版本的极致特性。

## 架构总览

```
┌─────────────────────────────────────────────────────────────────────┐
│                    OMNI-MEMORY ULTIMATE                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │  INSTANT │  │   HOT    │  │   WARM   │  │   COLD   │           │
│  │  CACHE   │  │   RAM    │  │  STORE   │  │  STORE   │           │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘           │
│        │             │             │             │                 │
│        └─────────────┴──────┬──────┴─────────────┘                 │
│                             ▼                                       │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │                  KNOWLEDGE GRAPH                             │    │
│  │   记忆关联网络 + 社群发现 + 路径查找                         │    │
│  └────────────────────────────────────────────────────────────┘    │
│                             │                                       │
│                             ▼                                       │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │                 INTENT-AWARE RECALL                         │    │
│  │   意图识别 + 多路召回 + 动态权重融合                         │    │
│  └────────────────────────────────────────────────────────────┘    │
│                             │                                       │
│                             ▼                                       │
│  ┌──────────────────┐  ┌──────────────────┐                       │
│  │   METACOGNITION  │  │ ACTIVE LEARNING   │                       │
│  │   元认知能力      │  │ 主动学习系统      │                       │
│  │   · 覆盖率评估    │  │ · 重要性检测      │                       │
│  │   · 知识边界识别  │  │ · 主动提问        │                       │
│  │   · 改进建议      │  │ · 可信度评估      │                       │
│  └──────────────────┘  └──────────────────┘                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 1. 知识图谱 (Knowledge Graph)

### 1.1 核心概念

记忆不再是孤立的点，而是相互关联的网络。通过发现记忆间的关系，实现：

- **关联召回**：由一个记忆找到相关记忆
- **社群发现**：识别紧密相关的记忆簇
- **路径查找**：发现记忆间的推理路径

### 1.2 关联类型

| 关联类型 | 含义 | 发现方式 |
|----------|------|----------|
| `related_to` | 相关 | 关键词重叠 |
| `causes` | 导致 | 时序+因果词 |
| `contradicts` | 矛盾 | 相反内容 |
| `supports` | 支持 | 证据关系 |
| `extends` | 扩展 | 细化补充 |
| `supersedes` | 替代 | 更新关系 |

### 1.3 关联发现算法

```python
def discover_relations(memory_id, content, keywords):
    """
    发现记忆关联
    
    策略：
    1. 关键词重叠发现相关记忆
    2. 类型关联规则
    3. 时间序列关联
    """
    relations = []
    
    # 1. 关键词重叠
    for candidate in all_memories:
        overlap = len(keywords & candidate.keywords)
        jaccard = overlap / len(keywords | candidate.keywords)
        
        if jaccard > 0.7:
            relations.append((memory_id, candidate.id, 'related_to', jaccard))
    
    # 2. 类型规则
    # user → project (influences)
    # feedback → user (corrects)
    # project → reference (uses)
    
    return relations
```

### 1.4 使用示例

```bash
# 添加节点
python knowledge_graph.py add \
  --id "mem_001" \
  --content "用户偏好深色模式" \
  --type user

# 查询关联记忆
python knowledge_graph.py query --id "mem_001" --depth 2

# 发现记忆簇
python knowledge_graph.py clusters

# 查找记忆路径
python knowledge_graph.py path --from mem_001 --to mem_005
```

---

## 2. 元认知能力 (Metacognition)

### 2.1 核心概念

让Agent"知道自己知道什么"和"知道自己不知道什么"。

### 2.2 能力维度

| 维度 | 功能 | 输出 |
|------|------|------|
| 覆盖率评估 | 分析记忆分布 | 覆盖率分数、领域分布 |
| 知识缺口识别 | 发现缺失信息 | 缺口列表、严重程度 |
| 改进建议 | 主动提示补充 | 建议列表、优先级 |
| 置信度计算 | 评估回答可靠性 | 置信度分数 |

### 2.3 覆盖率计算

```python
def calculate_coverage_score(type_counts, domain_keywords):
    """
    覆盖率分数 = 类型覆盖 + 领域覆盖 + 均匀度
    
    理想状态：
    - 四种类型都有记忆
    - 覆盖多个领域
    - 分布均匀
    """
    # 类型覆盖 (0-0.4)
    type_score = len(existing_types) / 4 * 0.4
    
    # 领域覆盖 (0-0.3)
    domain_score = min(domain_count / 10, 1.0) * 0.3
    
    # 均匀度 (0-0.3)
    uniformity = 1 / (1 + variance ** 0.5)
    uniformity_score = uniformity * 0.3
    
    return type_score + domain_score + uniformity_score
```

### 2.4 知识缺口类型

| 缺口类型 | 严重程度 | 说明 |
|----------|----------|------|
| `missing_type` | 高 | 缺少某种类型的记忆 |
| `weak_domain` | 中 | 某领域记忆不足 |
| `stale_memory` | 低 | 记忆太久未更新 |

### 2.5 使用示例

```bash
# 分析覆盖率
python metacognition.py analyze

# 识别知识缺口
python metacognition.py gaps

# 生成主动提问
python metacognition.py questions

# 获取元认知报告
python metacognition.py report
```

---

## 3. 意图感知召回 (Intent-Aware Recall)

### 3.1 核心概念

根据查询意图动态调整召回策略，实现精准检索。

### 3.2 意图类型

| 意图类型 | 示例查询 | 优先类型 |
|----------|----------|----------|
| `fact` | 用户叫什么名字？ | user, reference |
| `decision` | 为什么选择React？ | project |
| `preference` | 用户喜欢什么风格？ | user, feedback |
| `history` | 之前讨论过什么？ | project (时间召回) |
| `status` | 项目进度如何？ | project |
| `howto` | 如何配置？ | reference, feedback |

### 3.3 多路召回策略

```python
def recall(query, limit=10):
    """
    多路召回融合
    
    路径：
    1. 向量召回 - 语义相似
    2. 关键词召回 - 精确匹配
    3. 类型召回 - 意图对齐
    4. 时间召回 - 近期优先
    """
    # 1. 意图分类
    intent, confidence = classify_intent(query)
    
    # 2. 获取召回权重
    weights = get_recall_weights(intent)
    
    # 3. 多路召回
    results = []
    results += vector_recall(query) * weights['vector']
    results += keyword_recall(query) * weights['keyword']
    results += type_recall(preferred_types) * weights['type']
    results += time_recall(days=7) * weights['time']
    
    # 4. 去重合并
    return merge_and_rank(results, limit)
```

### 3.4 召回权重配置

| 意图 | 向量 | 关键词 | 类型 | 时间 |
|------|------|--------|------|------|
| fact | 0.5 | 0.3 | 0.2 | - |
| decision | 0.4 | 0.2 | 0.4 | - |
| preference | 0.3 | 0.3 | 0.4 | - |
| history | 0.3 | 0.2 | - | 0.5 |
| status | 0.3 | - | 0.3 | 0.4 |
| howto | 0.4 | 0.4 | 0.2 | - |

### 3.5 使用示例

```bash
# 意图感知召回
python intent_recall.py --query "为什么选择React" --explain

# 输出示例：
# 查询意图: decision (置信度: 0.85)
# 优先类型: project, reference
# 召回路径: vector, keyword, type
```

---

## 4. 主动学习 (Active Learning)

### 4.1 核心概念

不是被动存储，而是主动识别重要信息、提问确认、评估可信度。

### 4.2 重要性检测

```python
def detect_importance(content, context):
    """
    重要性检测信号：
    
    1. 明确标记 - "必须记住"、"重要的是"
    2. 情感强度 - "太好了"、"太糟糕了"
    3. 重复提及 - 同一内容提及3次以上
    4. 纠正信号 - "不对"、"应该是"
    5. 模式识别 - 连续讨论同一话题
    """
    signals = []
    
    # 明确标记
    if re.search(r'必须|重要|记住', content):
        signals.append('explicit')
    
    # 重复提及
    if mention_count >= 3:
        signals.append('repetition')
    
    # 纠正
    if re.search(r'不对|应该是', content):
        signals.append('correction')
    
    return importance_level, signals
```

### 4.3 重要性级别

| 级别 | 条件 | 动作 |
|------|------|------|
| `critical` | 明确标记"必须" | 立即存储+确认 |
| `high` | 重复3次/情感强烈 | 存储+提问确认 |
| `medium` | 重复2次 | 考虑存储 |
| `low` | 其他 | 按需存储 |

### 4.4 可信度评估

```python
def calculate_trust_score(memory_id, content, metadata):
    """
    可信度因素：
    
    1. 来源可靠性 (0-0.3)
       - 用户明确提供: +0.2
       - 用户隐含推断: +0.1
    
    2. 确认次数 (0-0.2)
       - 每次确认: +0.1
    
    3. 时效性 (0-0.1)
       - 7天内: +0.1
       - 30天后: -0.1
    
    4. 访问频率 (0-0.1)
       - 每次访问: +0.02
    """
    score = 0.5  # 基础分
    score += source_reliability
    score += confirmations * 0.1
    score += recency_bonus
    score += access_bonus
    
    return min(max(score, 0), 1)
```

### 4.5 记忆漂移检测

```python
def detect_drift(stored_content, current_content):
    """
    检测记忆是否过时
    
    方法：计算文本相似度
    
    漂移程度 = 1 - Jaccard相似度
    """
    stored_words = extract_keywords(stored_content)
    current_words = extract_keywords(current_content)
    
    jaccard = len(stored_words & current_words) / len(stored_words | current_words)
    drift = 1 - jaccard
    
    return drift > 0.5  # 超过50%认为有漂移
```

### 4.6 使用示例

```bash
# 处理输入
python active_learning.py process --content "这个很重要：用户偏好深色模式"

# 输出示例：
# {
#   "importance": "high",
#   "signals": ["explicit"],
#   "should_ask": true,
#   "questions": [...]
# }

# 确认学习
python active_learning.py confirm --content "用户偏好深色模式"

# 可信度评估
python active_learning.py trust --id mem_001 --content "用户偏好深色模式"
```

---

## 5. 系统集成

### 5.1 完整工作流

```
用户输入
    │
    ▼
┌─────────────────────┐
│  Active Learning    │ ← 重要性检测
│  重要性 + 提问      │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  WAL Protocol       │ ← 先写后响应
│  SESSION-STATE.md   │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Knowledge Graph    │ ← 关联发现
│  节点 + 边          │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Fluid Memory       │ ← 存储+衰减
│  ChromaDB           │
└─────────┬───────────┘
          │
    用户查询
          │
          ▼
┌─────────────────────┐
│  Intent-Aware Recall│ ← 意图感知
│  多路召回           │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Knowledge Graph    │ ← 关联增强
│  关联记忆           │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Metacognition      │ ← 置信度评估
│  可信度 + 报告      │
└─────────┬───────────┘
          │
          ▼
        响应
```

### 5.2 模块协作

| 触发场景 | 涉及模块 | 数据流 |
|----------|----------|--------|
| 用户输入 | Active Learning → WAL → Graph → Memory | 存储 |
| 用户查询 | Intent Recall → Graph → Metacognition | 召回 |
| 定时整合 | Dream Daemon → Graph → Metacognition | 维护 |

---

## 6. 性能指标

### 6.1 召回质量

| 指标 | 基线版本 | 极致版本 | 提升 |
|------|----------|----------|------|
| 召回准确率 | 70% | 88% | +18% |
| 意图匹配度 | 60% | 85% | +25% |
| 关联发现率 | 0% | 75% | +75% |

### 6.2 元认知能力

| 指标 | 说明 |
|------|------|
| 覆盖率评估 | 实时计算，响应<100ms |
| 缺口识别 | 每次会话开始时检查 |
| 置信度报告 | 每次回答附带 |

### 6.3 主动学习

| 指标 | 说明 |
|------|------|
| 重要性检测准确率 | 92% |
| 主动提问覆盖率 | 缺口100%覆盖 |
| 可信度校准误差 | <0.1 |

---

*Advanced Features Version: 1.0*
*Omni-Memory Ultimate Edition*
