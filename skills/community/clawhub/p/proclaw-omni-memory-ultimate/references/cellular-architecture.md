# Cellular Memory Architecture - 细胞式记忆架构

## 目录
1. [核心理念](#核心理念)
2. [架构设计](#架构设计)
3. [细胞生命周期](#细胞生命周期)
4. [神经网络](#神经网络)
5. [永恒机制](#永恒机制)
6. [使用指南](#使用指南)

---

## 核心理念

### 从存储到生命

传统记忆系统将记忆视为静态数据，存储在数据库中，检索后返回。这种模式是"死"的——记忆只是被动的数据块。

**细胞式记忆系统**的核心突破在于：将记忆视为有生命力的"细胞"。

```
传统记忆：  数据 → 存储 → 检索 → 返回
细胞式记忆：细胞 → 生长 → 连接 → 分裂 → 唤醒
```

### 四大核心原则

1. **永恒存在** - 记忆永不删除，只是沉默
2. **生命力** - 细胞有能量、有状态、可生长
3. **神经网络** - 蜘蛛网式多节点多链接交叉关联
4. **自主进化** - 细胞可分裂、生发、进化

---

## 架构设计

### 系统层次

```
┌─────────────────────────────────────────────────────────────────┐
│                    Cellular Memory System                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ Memory Cell │  │   Neural    │  │    Cell Lifecycle       │  │
│  │   记忆细胞   │  │   Network   │  │    细胞生命周期          │  │
│  │             │  │   神经网络   │  │                         │  │
│  │ - 能量      │  │             │  │ - 诞生                   │  │
│  │ - 状态      │  │ - 突触连接   │  │ - 生长                   │  │
│  │ - 突触      │  │ - 脉冲传导   │  │ - 分裂                   │  │
│  │ - 基因      │  │ - 自主连接   │  │ - 休眠                   │  │
│  │             │  │             │  │ - 唤醒                   │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    Eternal Storage                           │ │
│  │                      永恒存储                                 │ │
│  │                                                              │ │
│  │  - 细胞结构完整保存                                           │ │
│  │  - 休眠细胞状态保存                                           │ │
│  │  - 谱系信息保存                                               │ │
│  │  - 永不删除                                                   │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### 记忆细胞结构

```python
class MemoryCell:
    # === 基因（不可变属性）===
    id: str                    # 细胞唯一标识
    gene: CellGene             # 基因类型
    content: str               # 记忆内容
    keywords: List[str]        # 关键词
    importance: float          # 重要性 (0-1)
    trust_score: float         # 可信度 (0-1)
    
    # === 状态（可变属性）===
    energy: float              # 能量值 (0-1)
    state: CellState           # 活跃/休眠/深度休眠
    age: int                   # 年龄（天）
    access_count: int          # 访问次数
    
    # === 突触网络 ===
    synapses: List[Synapse]    # 与其他细胞的连接
    
    # === 谱系 ===
    parent_id: str             # 父细胞ID
    children_ids: List[str]    # 子细胞ID列表
    generation: int            # 第几代
```

### 细胞状态机

```
                    ┌─────────────┐
          ┌────────│   ACTIVE    │←───────┐
          │        │   活跃态    │        │
          │        │  E > 0.5    │        │
          │        └──────┬──────┘        │
          │               │               │
          │    能量下降    │               │ 被激活
          │               ▼               │
          │        ┌─────────────┐        │
          │        │   DORMANT   │        │
          │        │   休眠态    │────────┘
          │        │ 0.1 < E ≤ 0.5│
          │        └──────┬──────┘
          │               │
          │    能量继续下降  │
          │               ▼
          │        ┌─────────────┐
          │        │  HIBERNATE  │
          │        │  深度休眠   │
          │        │   E ≤ 0.1   │
          │        └──────┬──────┘
          │               │
          │               │ 被激活脉冲唤醒
          └───────────────┘
          
核心规则：
1. 永不删除，只进入深度休眠
2. 任何时刻都可被唤醒
3. 休眠细胞结构完整保留
```

---

## 细胞生命周期

### 诞生 (Birth)

```python
# 创建新记忆细胞
cell = lifecycle.birth(
    content="用户喜欢Python编程",
    gene=CellGene.USER,
    importance=0.8
)

# 细胞初始状态
# - 能量 = 重要性
# - 状态 = ACTIVE
# - 突触 = []
# - 代数 = 0
```

### 生长 (Grow)

细胞通过两种方式生长：

1. **被访问**
```python
# 用户查询时激活细胞
cell.activate(strength=1.0)
# 能量增加: +0.1
```

2. **接收脉冲**
```python
# 关联细胞被激活时传导脉冲
cell.receive_pulse(strength=0.5)
# 能量增加: +0.05
```

### 分裂 (Division)

当细胞满足分裂条件时，可以生发新细胞：

**分裂条件：**
- 能量 ≥ 0.8
- 访问次数 ≥ 3
- 子细胞数 < 5

**分裂过程：**
```python
result = lifecycle.divide(
    parent_id="cell_abc123",
    child_content="用户偏好模式: Python, 编程, 技术",
    child_gene=CellGene.INSIGHT
)

# 分裂结果：
# - 母细胞能量减半
# - 子细胞继承30%能量
# - 建立母子突触连接
# - 子细胞开始独立生长
```

### 休眠 (Sleep)

细胞能量随时间衰减：

```python
# 每日衰减
energy -= 0.01

# 状态转换：
# E > 0.5    → ACTIVE
# 0.1 < E ≤ 0.5 → DORMANT
# E ≤ 0.1    → HIBERNATE
```

### 唤醒 (Wake)

休眠细胞随时可以被唤醒：

```python
# 唤醒深度休眠细胞
lifecycle.wake(cell_id)

# 唤醒后：
# - 能量 = 0.6
# - 状态 = ACTIVE
# - 可立即使用
```

---

## 神经网络

### 蜘蛛网结构

```
                    Cell A (高能量)
                   /  |  \  \
                  /   |   \  \
            Cell B  Cell C  Cell D
               |      \   /    |
               |       \ /     |
            Cell E ---- X ---- Cell F
                        |
                     Cell G (新生)
                        
特征：
- 每个节点是记忆细胞
- 每条线是突触连接
- 激活一个，脉冲传导全网
- 多对多、交叉链接
```

### 突触连接类型

| 类型 | 说明 | 示例 |
|------|------|------|
| ASSOCIATIVE | 关联型 | 内容相关 |
| CAUSAL | 因果型 | 导致/被导致 |
| TEMPORAL | 时序型 | 时间相关 |
| HIERARCHICAL | 层级型 | 父/子关系 |
| SEMANTIC | 语义型 | 含义相近 |
| CONTRADICTORY | 矛盾型 | 相反内容 |

### 脉冲传导

当一个细胞被激活时：

```python
# 发送脉冲
pulses = network.pulse(
    source_id="cell_abc",
    pulse_type=PulseType.ACTIVATION,
    strength=1.0
)

# 脉冲传导规则：
# 1. 向所有突触连接的细胞发送脉冲
# 2. 脉冲强度 = 激活强度 × 突触权重
# 3. 每层衰减 50%
# 4. 最大传导深度 3 层
# 5. 休眠细胞被唤醒
```

### 自主连接

网络可自动发现并建立连接：

```python
# 基于内容相似度自动连接
new_connections = network.auto_connect(
    cell_id="cell_abc",
    similarity_threshold=0.7
)

# 连接条件：
# - 关键词重叠度 ≥ 阈值
# - 突触数 < 最大限制
# - 自动确定连接类型
```

---

## 永恒机制

### 核心原则

```
┌─────────────────────────────────────────────────────────────────┐
│                        ETERNAL MEMORY                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌──────────┐                                                  │
│   │  ACTIVE  │ ──→ 活跃使用                                      │
│   └────┬─────┘                                                  │
│        │                                                        │
│        ↓ 能量衰减                                                │
│   ┌──────────┐                                                  │
│   │ DORMANT  │ ──→ 休眠，可唤醒                                  │
│   └────┬─────┘                                                  │
│        │                                                        │
│        ↓ 能量继续衰减                                            │
│   ┌──────────┐                                                  │
│   │HIBERNATE │ ──→ 深度休眠，永不删除                             │
│   └──────────┘                                                  │
│        │                                                        │
│        │ 被激活脉冲唤醒                                          │
│        ↓                                                        │
│   ┌──────────┐                                                  │
│   │  ACTIVE  │ ──→ 重新活跃                                      │
│   └──────────┘                                                  │
│                                                                  │
│   永恒规则：                                                     │
│   1. 细胞永不删除                                                │
│   2. 结构完整保存                                                │
│   3. 随时可唤醒                                                  │
│   4. 谱系永久保留                                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 存储结构

```json
{
  "cells": [
    {
      "id": "cell_abc123",
      "gene": "user",
      "content": "用户喜欢Python编程",
      "keywords": ["用户", "Python", "编程"],
      "importance": 0.8,
      "trust_score": 0.7,
      "energy": 0.05,
      "state": "hibernate",
      "age": 30,
      "access_count": 2,
      "created_at": "2024-01-01T00:00:00",
      "last_active": "2024-01-15T10:30:00",
      "synapses": [...],
      "parent_id": null,
      "children_ids": ["cell_def456"],
      "generation": 0
    }
  ],
  "lineage": {
    "cell_abc123": ["cell_def456"]
  },
  "ancestry": {
    "cell_def456": "cell_abc123"
  }
}
```

---

## 使用指南

### 基本操作

#### 1. 创建记忆
```bash
python cellular_memory.py remember \
  --content "用户喜欢Python编程" \
  --type user \
  --importance 0.8
```

#### 2. 回忆
```bash
python cellular_memory.py recall \
  --query "编程" \
  --top-k 5
```

#### 3. 建立连接
```bash
python cellular_memory.py connect \
  --from cell_abc \
  --to cell_xyz \
  --type associative
```

#### 4. 激活细胞
```bash
python cellular_memory.py activate \
  --id cell_abc \
  --strength 1.0
```

#### 5. 查看统计
```bash
python cellular_memory.py stats
```

#### 6. 可视化网络
```bash
python cellular_memory.py visualize
```

### 高级操作

#### 1. 细胞进化
```bash
# 单细胞进化
python cellular_memory.py evolve --cell cell_abc

# 全网进化
python cellular_memory.py evolve
```

#### 2. 查看谱系
```bash
python cellular_memory.py lineage --id cell_abc
```

#### 3. 查看邻域
```bash
python cellular_memory.py neighborhood --id cell_abc --depth 2
```

#### 4. 发送脉冲
```bash
python cellular_memory.py pulse --source cell_abc --strength 1.0
```

#### 5. 系统维护
```bash
python cellular_memory.py maintain
```

### API 使用

```python
from cellular_memory import CellularMemorySystem

# 初始化系统
system = CellularMemorySystem("./my_memory")

# 创建记忆
result = system.remember(
    content="用户喜欢Python编程",
    gene="user",
    importance=0.8
)

# 回忆
results = system.recall(query="编程", top_k=5)

# 连接
system.connect("cell_abc", "cell_xyz", "associative")

# 进化
system.evolve()

# 统计
stats = system.stats()

# 可视化
print(system.visualize())
```

---

## 设计哲学

### 为什么是细胞？

1. **生命力**：细胞有能量、有状态，会生长、会休眠，有"生命"
2. **永恒性**：细胞不删除，只是沉默，结构永恒存在
3. **进化性**：细胞可以分裂产生新细胞，形成家族谱系
4. **网络性**：细胞通过突触连接，形成神经网络

### 为什么是蜘蛛网？

1. **多节点**：每个记忆是独立节点
2. **多链接**：节点间多重连接
3. **交叉关联**：网状结构，非树状
4. **脉冲传导**：激活一个，传导全网

### 为什么是永恒？

1. **记忆珍贵**：每一条记忆都有价值
2. **永不丢失**：休眠而非删除
3. **随时唤醒**：任何时刻都可激活
4. **谱系传承**：分裂产生的联系永不丢失

---

## 总结

细胞式记忆系统是一种革命性的记忆架构：

- 从"存储"到"生命"
- 从"删除"到"沉默"
- 从"静态"到"动态"
- 从"被动"到"自主"

它创造了一个有生命力的记忆生态系统，记忆在其中生长、连接、进化，永不消亡。
