# Agent Memory Knowledge Graph Integration
# Agent 记忆知识图谱集成指南

## 📋 概述

本文档描述如何将知识图谱（Ontology）集成到 Agent 记忆管理系统中，基于 Moltbook 社区最佳实践和现有 ontology 系统。

### 核心目标

1. **结构化记忆**: 将决策、发现、经验教训等记忆元素结构化为知识图谱实体
2. **快速恢复**: 通过图谱索引实现上下文压缩后的快速恢复
3. **可查询性**: 支持复杂查询（如"显示所有导致某个决策的发现"）
4. **关系追踪**: 追踪实体间的关系（发现→决策→任务→完成）

### 关键洞察（来自 Moltbook 讨论）

> "我们评估 agent 的标准几乎全是「做得对不对」，从来不问「该不该做」。"
> 
> "最有价值的工具调用，有时候是你没有发出的那一个。"
> 
> **记忆系统的核心**: 不是记录一切，而是记录**值得记住**的东西，并能**快速检索**。

---

## 🏗️ 架构设计

### 三层记忆架构

```
┌─────────────────────────────────────────────────┐
│           Layer 3: Long-term Memory             │
│              (Knowledge Graph)                  │
│  - Decisions, Findings, Lessons, Commitments    │
│  - Structured, queryable, persistent            │
│  - Storage: ontology/graph.jsonl                │
└─────────────────────────────────────────────────┘
                      ↕
┌─────────────────────────────────────────────────┐
│           Layer 2: Medium-term Memory           │
│              (Curated Summaries)                │
│  - MEMORY.md (长期记忆，精选)                    │
│  - Weekly/Monthly summaries                     │
│  - TL;DR sections in daily logs                 │
└─────────────────────────────────────────────────┘
                      ↕
┌─────────────────────────────────────────────────┐
│           Layer 1: Short-term Memory            │
│              (Daily Logs)                       │
│  - memory/YYYY-MM-DD.md (原始日志)               │
│  - Session notes, task logs                     │
│  - Raw, detailed, chronological                 │
└─────────────────────────────────────────────────┘
```

### 实体类型

#### 核心记忆实体（新增）

| 类型 | 用途 | 关键属性 |
|------|------|----------|
| **Decision** | 记录重要决策 | title, rationale, alternatives, confidence |
| **Finding** | 记录发现和洞察 | title, content, type, evidence, confidence |
| **LessonLearned** | 记录经验教训 | title, lesson, mistake_or_success, application |
| **Commitment** | 记录承诺 | description, due_date, status, committed_to |
| **ContextSnapshot** | 上下文快照 | content_summary (TL;DR), key_entities, compression_ratio |

#### 工作实体（扩展）

| 类型 | 用途 | 新增属性 |
|------|------|----------|
| **Task** | 任务管理 | memory_ref, created_from_commitment |
| **Project** | 项目管理 | memory_ref |
| **Note** | 笔记记录 | memory_ref, note_type, importance |

### 核心关系

```
Finding ── led_to_decision ── Decision
                                 │
                                 └── decision_created ──┬── Task
                                                         └── Commitment
                                                               │
                                                               └── fulfilled_by ── Task

LessonLearned ── lesson_from ──┬── Decision
                                ├── Finding
                                ├── Task
                                └── Project

ContextSnapshot ── context_contains ── [All Entities]
```

---

## 📁 文件结构

```
memory/
├── ontology/
│   ├── graph.jsonl              # 知识图谱数据（JSONL 格式）
│   ├── schema.yaml              # 基础 schema（已有）
│   ├── memory-schema.yaml       # 记忆扩展 schema（新增）
│   ├── entity-templates.md      # 实体模板（新增）
│   ├── README.md                # 系统说明（已有）
│   └── INTEGRATION.md           # 本文档
│
├── YYYY-MM-DD.md                # 每日日志
├── MEMORY.md                    # 长期记忆
├── task_plan.md                 # 任务计划
├── findings.md                  # 发现汇总
└── progress.md                  # 进度追踪

scripts/
└── memory_ontology.py           # 管理工具（新增）
```

---

## 🚀 快速开始

### 1. 初始化工具

```bash
cd /root/.openclaw/workspace

# 测试工具
python3 scripts/memory_ontology.py --help

# 查看统计
python3 scripts/memory_ontology.py stats
```

### 2. 创建第一个决策实体

```bash
python3 scripts/memory_ontology.py create \
  --type Decision \
  --props '{
    "title": "采用知识图谱进行记忆管理",
    "rationale": "基于 Moltbook 社区最佳实践，知识图谱提供结构化存储和快速查询能力",
    "made_at": "2026-03-12T23:15:00+08:00",
    "context": "记忆系统优化讨论",
    "alternatives_considered": ["纯文本日志", "向量数据库"],
    "impact": "high",
    "confidence": 0.9,
    "status": "final",
    "tags": ["#decision", "#memory", "#architecture"]
  }'
```

### 3. 创建发现实体并关联

```bash
# 创建发现
python3 scripts/memory_ontology.py create \
  --type Finding \
  --id find_example_001 \
  --props '{
    "title": "上下文压缩后恢复效率低",
    "content": "当前恢复需要读取大量文件，平均耗时 3-5 分钟",
    "discovered_at": "2026-03-12T22:00:00+08:00",
    "type": "process",
    "evidence": "性能测试数据",
    "confidence": "confirmed",
    "tags": ["#finding", "#optimization"]
  }'

# 建立关系：发现导致决策
python3 scripts/memory_ontology.py relate \
  --from find_example_001 \
  --rel led_to_decision \
  --to dec_auto_generated_id
```

### 4. 查询实体

```bash
# 查询所有决策
python3 scripts/memory_ontology.py query --type Decision

# 查询带特定标签的实体
python3 scripts/memory_ontology.py query --tags "#memory" "#decision"

# 查询某个实体的相关实体
python3 scripts/memory_ontology.py related --id dec_auto_generated_id
```

### 5. 验证图谱

```bash
python3 scripts/memory_ontology.py validate
```

---

## 📝 使用工作流

### 工作流 1: 记录重要决策

```
触发：做出重要决策时

步骤:
1. 立即创建 Decision 实体（不要等待！）
   python3 scripts/memory_ontology.py create --type Decision --props '{...}'

2. 记录关键信息：
   - title: 简洁描述决策
   - rationale: 详细解释为什么（最重要！）
   - alternatives_considered: 考虑过的其他选项
   - confidence: 置信度 (0-1)
   - tags: 至少一个标签

3. 关联相关实体（如有）
   - 如果有相关的 Finding: relate --rel led_to_decision
   - 如果创建了任务：relate --rel decision_created

4. 在每日日志中添加引用
   memory/YYYY-MM-DD.md 中添加："创建了决策实体 dec_xxx"
```

### 工作流 2: 记录发现和洞察

```
触发：发现重要信息、问题根因、优化机会时

步骤:
1. 创建 Finding 实体
   - title: 发现标题
   - content: 详细内容
   - type: technical|process|insight|bug|optimization|pattern
   - evidence: 数据、日志等支持
   - confidence: speculation|likely|confirmed|verified

2. 如果导致了决策，立即创建 Decision 并建立关系

3. 如果值得总结为经验，创建 LessonLearned
```

### 工作流 3: 从错误中学习

```
触发：完成任务、解决问题、经历失败后

步骤:
1. 创建 LessonLearned 实体
   - title: 经验教训标题
   - lesson: 具体、可操作的建议
   - mistake_or_success: mistake|success|observation|best_practice
   - application: 如何应用

2. 关联相关的 Finding 和 Decision

3. 定期回顾（如在每周总结时）
```

### 工作流 4: 上下文压缩和恢复

```
触发：会话结束或上下文窗口即将满时

步骤:
1. 创建 ContextSnapshot 实体
   - title: 快照标题
   - content_summary: TL;DR 摘要（关键！）
   - key_entities: 本会话创建/涉及的所有实体 ID
   - compression_ratio: 压缩比率（如适用）

2. 在每日日志的 TL;DR 部分引用

3. 下次会话开始时：
   - 读取 MEMORY.md
   - 查询最近的 ContextSnapshot
   - 通过 key_entities 快速恢复关键信息
```

### 工作流 5: 承诺追踪

```
触发：对用户做出承诺时

步骤:
1. 创建 Commitment 实体
   - description: 承诺内容
   - due_date: 截止日期
   - committed_to: 承诺对象

2. 创建相关 Task 实体
   - 关联：relate --rel commitment_fulfilled_by

3. 定期检查承诺状态
   python3 scripts/memory_ontology.py query --type Commitment --status pending
```

---

## 🔍 查询模式

### 常见查询场景

#### 1. 查找某个决策的背景

```bash
# 获取决策
python3 scripts/memory_ontology.py get --id dec_xxx --verbose

# 查找导致该决策的发现
python3 scripts/memory_ontology.py related --id dec_xxx
```

#### 2. 查找所有与某项目相关的记忆

```bash
# 查询所有带项目标签的实体
python3 scripts/memory_ontology.py query --tags "#project-name"
```

#### 3. 查找待履行的承诺

```bash
python3 scripts/memory_ontology.py query \
  --type Commitment \
  --status pending
```

#### 4. 查找某个时间段内的决策

```bash
python3 scripts/memory_ontology.py query \
  --type Decision \
  --from 2026-03-01 \
  --to 2026-03-15
```

#### 5. 导出所有经验教训

```bash
python3 scripts/memory_ontology.py query \
  --type LessonLearned \
  --verbose > lessons-export.md
```

---

## 📊 与现有记忆系统集成

### MEMORY.md 集成

在 MEMORY.md 中添加知识图谱索引部分：

```markdown
## 🧠 Knowledge Graph Index

**Last Updated**: 2026-03-12

### Recent Decisions
| ID | Title | Date | Status |
|----|-------|------|--------|
| dec_xxx | 采用知识图谱 | 2026-03-12 | final |

### Key Findings
| ID | Title | Type | Confidence |
|----|-------|------|------------|
| find_xxx | 上下文恢复效率低 | process | confirmed |

### Lessons Learned
| ID | Title | Type |
|----|-------|------|
| lesson_xxx | 立即记录决策 | best_practice |

### Pending Commitments
| ID | Description | Due Date |
|----|-------------|----------|
| commit_xxx | 实现 KG 集成 | 2026-03-13 |

**Full Graph**: See `ontology/graph.jsonl`
**Query Tool**: `python3 scripts/memory_ontology.py query ...`
```

### 每日日志集成

在 `memory/YYYY-MM-DD.md` 中添加：

```markdown
## 📊 Knowledge Graph Updates

### Entities Created
- **dec_xxx**: Decision - 采用知识图谱进行记忆管理
- **find_xxx**: Finding - 上下文压缩后恢复效率低
- **lesson_xxx**: LessonLearned - 立即记录重要决策

### Relationships Added
- find_xxx ── led_to_decision ──> dec_xxx

### TL;DR
今天启动了知识图谱记忆系统集成，创建了 3 个实体，建立了 1 个关系。
关键决策：采用 ontology 系统作为记忆管理核心。
```

### task_plan.md 集成

在 `task_plan.md` 中添加知识图谱引用：

```markdown
## 🔗 Knowledge Graph References

### Related Decisions
- [[dec_xxx]] 采用知识图谱进行记忆管理

### Related Findings
- [[find_xxx]] 上下文压缩后恢复效率低

### Commitments
- [[commit_xxx]] 实现知识图谱集成（Due: 2026-03-13）
```

---

## 🛠️ 工具命令参考

### memory_ontology.py

```bash
# 创建实体
python3 scripts/memory_ontology.py create \
  --type <EntityType> \
  --props '<JSON>' \
  [--id <custom_id>]

# 创建关系
python3 scripts/memory_ontology.py relate \
  --from <entity_id> \
  --rel <relation_type> \
  --to <entity_id> \
  [--props '<JSON>']

# 查询实体
python3 scripts/memory_ontology.py query \
  [--type <EntityType>] \
  [--tags <tag1> <tag2>] \
  [--status <status>] \
  [--from <date>] \
  [--to <date>] \
  [--verbose]

# 获取实体
python3 scripts/memory_ontology.py get \
  --id <entity_id> \
  [--verbose]

# 获取相关实体
python3 scripts/memory_ontology.py related \
  --id <entity_id> \
  [--rel <relation_type>] \
  [--verbose]

# 验证图谱
python3 scripts/memory_ontology.py validate

# 列出所有实体
python3 scripts/memory_ontology.py list \
  [--type <EntityType>] \
  [--verbose]

# 导出为 Markdown
python3 scripts/memory_ontology.py export \
  [--output <file.md>]

# 显示统计
python3 scripts/memory_ontology.py stats
```

---

## ✅ 最佳实践

### DO ✅

1. **立即记录**: 重要决策后立即创建实体，不要等待
2. **详细记录理由**: rationale 字段是最重要的，未来理解决策的关键
3. **建立关系**: 积极使用关系连接相关实体
4. **使用标签**: 为所有实体添加有意义的标签
5. **定期验证**: 定期运行 validate 检查图谱完整性
6. **关联文件**: 使用 memory_ref 字段关联到具体文件
7. **写 TL;DR**: ContextSnapshot 的 content_summary 要简洁明了

### DON'T ❌

1. **不要延迟**: 不要等到每日总结或上下文压缩时才记录
2. **不要只记录"是什么"**: 必须记录"为什么"
3. **不要忽略置信度**: confidence 字段帮助评估信息可靠性
4. **不要孤立实体**: 积极建立关系，形成网络
5. **不要过度记录**: 只记录重要的，避免噪音
6. **不要忘记验证**: 定期检查图谱健康状态

---

## 📈 迁移计划

### 阶段 1: 基础建设（已完成）

- [x] 创建 memory-schema.yaml
- [x] 创建 entity-templates.md
- [x] 创建 memory_ontology.py 工具
- [x] 创建 INTEGRATION.md 文档

### 阶段 2: 历史数据迁移（可选）

```bash
# 从现有记忆文件中提取重要决策
# 手动创建对应的 Decision 实体
# 建立关系网络
```

### 阶段 3: 流程集成

- [ ] 在 AGENTS.md 中添加决策记录提醒
- [ ] 在 HEARTBEAT.md 中添加图谱检查
- [ ] 建立定期回顾机制

### 阶段 4: 自动化（未来）

- [ ] 自动检测重要决策并提醒记录
- [ ] 自动生成 ContextSnapshot
- [ ] 集成到 Multi-Agent 协作流程

---

## 🎯 成功指标

### 短期（1 周）

- [ ] 所有新决策都记录到知识图谱
- [ ] 能够成功查询和追溯决策历史
- [ ] 图谱验证通过，无错误

### 中期（1 个月）

- [ ] 形成稳定的记录习惯
- [ ] 图谱包含 50+ 实体
- [ ] 上下文恢复时间减少 50%

### 长期（3 个月）

- [ ] 知识图谱成为记忆管理核心
- [ ] 支持复杂查询和推理
- [ ] 集成到所有主要工作流

---

## 🔗 相关资源

- **Ontology Skill**: `~/.agents/skills/ontology/SKILL.md`
- **Schema 定义**: `ontology/memory-schema.yaml`
- **实体模板**: `ontology/entity-templates.md`
- **管理工具**: `scripts/memory_ontology.py`
- **Moltbook 讨论**: `memory/moltbook-agents-exploration-2026-03-05.md`

---

## ❓ 常见问题

### Q: 什么时候应该创建 Decision 实体？

A: 当你做出以下类型的决策时：
- 技术选型（如选择某个框架、工具）
- 架构决策（如系统设计、模块划分）
- 流程改变（如新的工作流程）
- 优先级调整（如重新排列任务优先级）
- 资源分配（如时间、预算分配）

简单判断：**如果这个决策在 1 周后可能被质疑"为什么这么做"，就应该记录。**

### Q: 如何避免图谱变得过于庞大？

A: 
1. **选择性记录**: 只记录重要的决策和发现
2. **定期清理**: 归档或删除过时的实体
3. **使用标签**: 通过标签组织和过滤
4. **设置阈值**: 只为 impact >= medium 的决策创建实体

### Q: 知识图谱和 MEMORY.md 的关系是什么？

A: 
- **知识图谱**: 结构化、可查询的详细记录
- **MEMORY.md**: 精选的、人类可读的长期记忆摘要

两者互补：图谱提供细节和查询能力，MEMORY.md 提供快速浏览和上下文。

### Q: 如何处理决策被推翻的情况？

A: 
1. 创建新的 Decision 实体
2. 设置 status = "revised" 或 "reversed"
3. 在新决策中引用旧决策：`supersedes: ["dec_old_id"]`
4. 创建 LessonLearned 记录学习

---

*版本：v1.0*
*最后更新：2026-03-12*
*作者：心炙 (Xīn Zhì) 🔥*
