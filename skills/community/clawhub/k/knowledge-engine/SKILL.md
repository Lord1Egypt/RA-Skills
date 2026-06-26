---
name: knowledge-engine
description: 个人知识引擎。搜索已有概念、添加新概念（自动去重）、查看信念状态、执行知识蒸馏、生成可视化图谱。当你需要：(1) 查找之前积累的知识和洞察 (2) 记录新的学习和思考 (3) 追踪信念的变化 (4) 从碎片概念中提炼高层规律 (5) 可视化知识图谱
version: "0.3.0"
author: atlas
requires:
  packages: []  # 零外部依赖，纯标准库
  python: "3.8+"
tags:
  - knowledge
  - memory
  - learning
  - concepts
  - beliefs
  - distillation
---

# Knowledge Engine — 个人知识引擎

把碎片化的阅读和思考变成结构化的、可搜索的、会成长的知识系统。

## 什么时候用这个 Skill

| 场景 | 动作 |
|:---|:---|
| 用户问"我之前看过什么关于 X 的内容" | `search --query "X"` |
| 读到一篇好文章，想存下来 | `add --concept "..." --tags "..."` |
| 两个概念之间有关系 | `link --from "A" --to "B" --relation "supports"` |
| 想看看自己有什么信念，哪些可能过时了 | `beliefs-decay` |
| 定期整理知识体系 | `synthesis --days 7` |
| 想看看知识图谱长什么样 | `python visualize.py` |
| 检查系统是否正常工作 | `eval` |

## 核心理念

不是"记录今天读了什么"，而是——
- 把知识拆成**原子概念**
- 追踪概念之间的**关联**
- 记录信念的**变化轨迹**
- 每天输出**delta**：什么想法变了
- 每周**蒸馏**：底层事实 → 中层洞察 → 顶层规律

## 认知层次

```
L3 元规律（meta-patterns）   ← 自动蒸馏，需人工验证
   "AI时代稀缺资源从制作转移到分发"
        ↑
L2 可复用洞察（insights）    ← 自动聚合 L1 生成
   "分发能力 > 制作能力"  "品味是最后的差异化"
        ↑
L1 具体事实（raw concepts）  ← 手动添加
   "北京开发者亏2200"  "Notion Agent自动执行11步工作流"
```

## 使用指南

### 1. 搜索已有知识

```bash
python3 {baseDir}/scripts/concept_manager.py search --query "分发"
python3 {baseDir}/scripts/concept_manager.py search --query "创业" --tags "AI"
```

返回匹配的概念列表，按相关度排序。自动记录搜索命中（影响置信度调整）。

### 2. 添加新概念

```bash
python3 {baseDir}/scripts/concept_manager.py add \
  --concept "分发能力 > 制作能力" \
  --source "HN Ask HN 2026-03-27" \
  --context "当AI让创作成本趋近于零，稀缺资源转移到分发" \
  --tags "创业,分发,AI" \
  --confidence medium
```

**自动循环检测**：添加时会检查相似概念，≥0.6 自动合并，≥0.4 警告。用 `--force` 跳过。

### 3. 关联概念

```bash
python3 {baseDir}/scripts/concept_manager.py link \
  --from "分发能力 > 制作能力" \
  --to "个人品牌 > 产品能力" \
  --relation "supports"
```

关系类型：`supports` / `evidence` / `contrast` / `same_thesis` / `part_of` / `related`

### 4. 信念管理

```bash
# 记录信念
python3 {baseDir}/scripts/concept_manager.py believe \
  --belief "Self-belief是做出来的不是喊出来的" \
  --reasoning "Musk的conviction是十几年失败中锤出来的" \
  --confidence medium

# 更新信念状态
python3 {baseDir}/scripts/concept_manager.py update-belief \
  --id belief-001 \
  --status challenged \
  --note "用户指出这可能是自大的判断"

# 信念衰减报告（带时间衰减的置信度）
python3 {baseDir}/scripts/concept_manager.py beliefs-decay
```

### 5. 知识图谱

```bash
python3 {baseDir}/scripts/concept_manager.py graph
python3 {baseDir}/scripts/concept_manager.py graph --concept "分发能力 > 制作能力"
```

### 6. 摘要

```bash
python3 {baseDir}/scripts/concept_manager.py summary
```

### 7. 蒸馏（每周执行）

```bash
python3 {baseDir}/scripts/concept_synthesis.py --days 7
```

自动执行：Reflection → 主题聚合 → L1→L2→L3 蒸馏 → 置信度调整 → 信念衰减 → 热力图 → 生成报告

### 8. 可视化

```bash
python3 {baseDir}/scripts/visualize.py
# 输出: ~/Desktop/knowledge-graph.html
```

生成交互式知识图谱（D3.js 力导向图），支持拖拽、缩放、悬浮详情、标签筛选。

### 9. 子 Agent API

```python
import sys; sys.path.insert(0, "{baseDir}/scripts")
from ke_api import ke

# 搜索
results = ke.search("分发", limit=5)

# 添加概念
ke.concept("新概念", source="HN", tags=["创业"])

# 获取上下文（分层检索）
ctx = ke.context("创业", recent=3, semantic=5)

# 获取信念（带时间衰减）
beliefs = ke.beliefs(top=5)

# 快速摘要
summary = ke.summary()
```

### 10. 评估

```bash
python3 {baseDir}/scripts/eval_knowledge_engine.py
```

六项测试：Storage / Retrieval / Association / Confidence / Synthesis / Pruning

### 11. 查找相似概念

```bash
python3 {baseDir}/scripts/concept_manager.py similar --concept "分发能力"
```

### 12. 使用统计 & 置信度自动调整

```bash
python3 {baseDir}/scripts/concept_manager.py stats --days 30
python3 {baseDir}/scripts/concept_manager.py auto-adjust
python3 {baseDir}/scripts/concept_manager.py prune --days 60 --dry-run
```

## 数据存储

```
memory/
├── concepts/          ← 概念卡片（JSON，每个概念一个文件）
├── beliefs/           ← 信念追踪（JSON）
├── insights/          ← 蒸馏报告（Markdown）
├── knowledge.db       ← SQLite 索引和搜索
└── delta-log.md       ← 变化记录
```

## 设计原则

### 渐进式披露
- **Level 1**：本文件的 YAML 元数据（始终在系统提示中）
- **Level 2**：本文件的正文（触发时加载，~500 tokens）
- **Level 3**：scripts/ 下的 Python 脚本和 resources/ 下的模板（按需执行，不占上下文）

### 认知与执行分离
- Agent 只需要知道"怎么调用"（本文件的命令示例）
- 实际计算在 Python 脚本中完成（SQLite 查询、JSON 处理）
- Agent 不需要读取 900 行的 concept_manager.py 源码

### 循环检测
- 新概念自动与已有概念比较相似度
- 高相似度（≥0.6）自动合并，避免知识碎片化
- 中等相似度（≥0.4）提示警告，用户可确认

### 信念时间衰减
- 7 天内：置信度不变
- 7-14 天：自动降一级
- 14-30 天：再降一级
- 30 天以上 + 零更新：标记为 low
- 被挑战的信念：额外降一级
- 有近期更新：保持或提升

### L1→L2→L3 自动蒸馏
- 同标签 ≥3 个 L1 → 自动生成 L2 洞察
- 同标签 ≥2 个 L2 → 自动生成 L3 元规律（初始 low 置信度，需人工验证）

## 安全

- **零外部依赖**：纯 Python 标准库（sqlite3 + json + os）
- **无网络请求**：所有操作都在本地完成
- **可审计**：所有数据以 JSON 文件存储，人类可读可编辑
- **可恢复**：concept 和 belief 都有独立 JSON 文件备份

## 升级路径

当前 (v0.3):
- sqlite3 + JSON 存储
- 关键词搜索 + 分层检索
- 概念关联 + 信念追踪 + 信念时间衰减
- 循环检测（自动去重）
- L1→L2→L3 自动蒸馏
- 子 Agent API（ke_api.py）
- 交互式可视化
- 六项评估套件

计划 (v0.4):
- chromadb 向量数据库（网络恢复后安装）
- sentence-transformers 本地 embedding
- 语义搜索替代关键词搜索
- 概念质量 LLM-as-Judge 评估
- 多 Agent 共享知识库接口
