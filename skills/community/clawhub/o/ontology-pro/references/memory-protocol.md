# 持久记忆协议 (Memory Protocol)

> 本文档定义了 ontology-pro 的知识持久化、增量更新和跨会话记忆管理机制。

---

## 1. 记忆架构

### 三层记忆模型

```
┌─────────────────────────────────────────┐
│         L1: 工作记忆（Working Memory）      │
│    当前会话的临时知识，会话结束即清除         │
│    存储：内存 / 会话上下文                   │
├─────────────────────────────────────────┤
│         L2: 图谱记忆（Graph Memory）        │
│    持久化知识图谱，跨会话持续积累             │
│    存储：JSON 文件                          │
├─────────────────────────────────────────┤
│         L3: 索引记忆（Index Memory）         │
│    知识元数据、统计摘要、快速检索索引          │
│    存储：MEMORY.md / 索引文件               │
└─────────────────────────────────────────┘
```

| 层级 | 生命周期 | 容量 | 用途 |
|------|---------|------|------|
| L1 工作记忆 | 单次会话 | 无限制 | 当前分析上下文 |
| L2 图谱记忆 | 永久 | 按需扩展 | 知识积累 |
| L3 索引记忆 | 永久 | 精简 | 快速定位 |

---

## 2. 存储格式

### L2 图谱记忆文件

路径：`{workspace}/.workbuddy/ontology/{domain}/graph.json`

```json
{
  "version": "1.0.0",
  "domain": "energy_storage",
  "created_at": "2026-03-30T16:00:00+08:00",
  "updated_at": "2026-03-30T16:00:00+08:00",
  "schema": "ontology-graph-v1",

  "entities": [
    {
      "id": "e001",
      "name": "储能系统",
      "type": "concept",
      "attributes": {
        "category": "能源基础设施",
        "aliases": ["ESS", "Energy Storage System"],
        "created_at": "2026-03-30T16:00:00+08:00",
        "updated_at": "2026-03-30T16:00:00+08:00",
        "source_session": "sess_001"
      }
    }
  ],

  "relations": [
    {
      "id": "r001",
      "source": "e001",
      "target": "e002",
      "type": "includes",
      "weight": 0.9,
      "evidence": "储能系统主要由电池组和PCS组成",
      "created_at": "2026-03-30T16:00:00+08:00",
      "source_session": "sess_001"
    }
  ],

  "changelog": [
    {
      "timestamp": "2026-03-30T16:00:00+08:00",
      "session_id": "sess_001",
      "action": "create",
      "summary": "初始化储能领域知识图谱",
      "entities_added": 23,
      "relations_added": 34
    }
  ],

  "metadata": {
    "total_entities": 45,
    "total_relations": 72,
    "total_sessions": 10,
    "domains": ["energy_storage", "power_market"],
    "entity_types": {
      "concept": 15,
      "organization": 8,
      "technology": 12,
      "policy": 10
    }
  }
}
```

### L3 索引记忆文件

路径：`{workspace}/.workbuddy/ontology/index.json`

```json
{
  "version": "1.0.0",
  "updated_at": "2026-03-30T16:00:00+08:00",
  "domains": {
    "energy_storage": {
      "path": ".workbuddy/ontology/energy_storage/graph.json",
      "entity_count": 45,
      "relation_count": 72,
      "last_updated": "2026-03-30T16:00:00+08:00"
    },
    "medical_fmt": {
      "path": ".workbuddy/ontology/medical_fmt/graph.json",
      "entity_count": 30,
      "relation_count": 48,
      "last_updated": "2026-03-28T10:00:00+08:00"
    }
  },
  "stats": {
    "total_entities": 75,
    "total_relations": 120,
    "total_domains": 2,
    "total_sessions": 18
  }
}
```

---

## 3. 增量更新协议

### 更新流程

```
新输入
  │
  ▼
加载已有图谱（L2）
  │
  ▼
执行 analyze（参照 cognitive-graph.md）
  │
  ▼
生成增量更新（add/update/conflict）
  │
  ▼
应用更新到图谱
  │
  ▼
写入 changelog
  │
  ▼
保存图谱（L2）
  │
  ▼
更新索引（L3）
```

### 增量更新操作

| 操作 | 说明 | 示例 |
|------|------|------|
| `add_entity` | 新增实体 | 发现新的公司/技术/政策 |
| `update_entity` | 更新实体属性 | 补充别名、修正分类 |
| `merge_entity` | 合并重复实体 | "ESS" 和 "储能系统" 是同一个 |
| `add_relation` | 新增关系 | 发现新的因果/依赖关系 |
| `update_relation` | 更新关系权重 | 基于新证据调整置信度 |
| `mark_conflict` | 标记冲突 | 新信息与已有知识矛盾 |
| `archive_relation` | 归档过时关系 | 旧政策已失效 |

### 冲突处理规则

| 冲突类型 | 处理方式 |
|----------|---------|
| 新信息 vs 旧信息（时间差异） | 保留新的，旧信息标记为 `deprecated` |
| 互相矛盾的信息 | 两者都保留，标记为 `conflict`，等待人工确认 |
| 分类/属性冲突 | 合并所有属性，保留更详细的版本 |
| 重复实体 | 合并为一个，保留所有属性和别名 |

---

## 4. 上下文注入协议

### 会话开始时的加载策略

当新会话启动且涉及 ontology-pro 时：

```
1. 检测用户输入的关键词/领域
   │
   ▼
2. 从索引（L3）查找匹配的图谱
   │
   ▼
3. 加载匹配图谱的摘要信息
   - 领域名称
   - 实体总数
   - 关键实体 Top 20
   - 最近更新时间
   │
   ▼
4. 如果用户明确提到"之前分析的内容"或"我记得..."
   → 加载完整图谱到 L1 工作记忆
   │
   ▼
5. 执行 analyze/think/strategy 时
   → 图谱上下文自动注入到推理 prompt 中
```

### 上下文预算控制

为避免 prompt 过长，加载时遵守以下预算：

| 场景 | 加载内容 | 预算 |
|------|---------|------|
| 快速问答 | 实体列表 + 直接关系 | < 500 tokens |
| 标准分析 | 相关子图（2跳以内） | < 2000 tokens |
| 深度推理 | 完整图谱 + changelog | < 5000 tokens |
| 全量图谱 | 仅在用户明确要求时 | 不限 |

### 子图提取策略

当图谱过大时，只加载与当前问题相关的子图：

```
1. 识别问题中的核心实体（关键词匹配）
2. 从核心实体出发，提取 2 跳以内的子图
3. 按权重排序，保留高置信度关系（weight ≥ 0.5）
4. 加入最近 3 次会话的 changelog 摘要
```

---

## 5. 记忆管理命令

### memory 命令 Prompt

```
你是 ontology-pro 的记忆管理器。请执行以下记忆管理操作。

【当前图谱状态】
{graph_state}

【用户指令】
{memory_command}

支持的操作：

1. list - 列出所有领域的图谱摘要
2. show {domain} - 显示指定领域的图谱详情
3. search {keyword} - 搜索包含关键词的实体和关系
4. stats - 显示全局统计信息
5. export {domain} - 导出指定领域图谱为 JSON
6. merge {source} → {target} - 合并两个领域的图谱
7. cleanup - 清理低置信度（<0.3）的关系和孤立实体
8. history {domain} - 显示指定领域的更新历史
```

---

## 6. 记忆维护规则

### 自动维护

| 操作 | 触发条件 | 说明 |
|------|---------|------|
| 置信度衰减 | 每 30 天 | 未被引用的关系 weight × 0.95 |
| 孤立实体清理 | 每 30 天 | 无任何关系的实体移入归档 |
| 索引重建 | 每次更新后 | 自动更新 L3 索引 |
| 版本快照 | 实体/关系数 > 200 | 创建历史快照，避免单文件过大 |

### 手动维护

| 操作 | 命令 | 说明 |
|------|------|------|
| 全量备份 | `memory export all` | 导出所有图谱 |
| 数据清理 | `memory cleanup` | 清理低质量数据 |
| 图谱重置 | `memory reset {domain}` | 清空指定领域图谱 |
| 冲突审查 | `memory conflicts {domain}` | 列出所有待解决的冲突 |

---

## 7. 多领域图谱管理

### 领域隔离

每个领域维护独立的图谱文件：

```
.workbuddy/ontology/
├── index.json                    ← 全局索引
├── general/                      ← 通用知识
│   └── graph.json
├── energy_storage/               ← 储能领域
│   └── graph.json
├── medical_fmt/                  ← FMT医疗领域
│   └── graph.json
└── ai_tech/                      ← AI技术领域
    └── graph.json
```

### 跨领域关联

当分析涉及多个领域时：

```
1. 分别加载相关领域的子图
2. 识别跨领域的共有实体（同名或别名匹配）
3. 通过共有实体建立跨领域连接
4. 在推理中同时考虑多领域信息
```

### 领域自动识别

基于输入文本自动判断领域：

```
关键词匹配 → 频率统计 → 最高频领域 = 主领域
次要关键词 → 辅助领域
```

| 关键词示例 | 领域 |
|-----------|------|
| 储能、光伏、电力现货、PCS、BMS | energy_storage |
| FMT、肠菌、菌群、移植、微生物 | medical_fmt |
| GPT、Transformer、RAG、Agent | ai_tech |
