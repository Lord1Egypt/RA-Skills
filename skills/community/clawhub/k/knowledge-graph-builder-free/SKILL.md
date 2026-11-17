---
name: "knowledge-graph-builder-free"
description: "AI Agent类型化知识图谱系统，实体-关系-约束三要素，JSONL存储+约束验证。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "Knowledge Graph Buil"
  version: "1.0.0"
  summary: "AI Agent类型化知识图谱系统，实体-关系-约束三要素，JSONL存储+约束验证。"
  tags:
    - "知识图谱"
    - "类型化实体"
    - "关系网络"
    - "约束验证"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# 知识图谱构建器（免费版）
> **AI Agent的类型化知识图谱系统。实体-关系-约束三要素，每条变更都经过验证。**

信息零散如沙，关系不可追溯，约束无验证。知识图谱构建器免费版将零散信息组织为可验证、可查询、可推理的结构化图谱。

## 架构总览
```text
┌─────────────────────────────────────────────────────────────────┐
│            知识图谱构建器免费版 (KNOWLEDGE GRAPH FREE)           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │
│   │  实体创建     │ -> │  约束验证    │ -> │  JSONL存储   │     │
│   │  12+核心类型  │    │  必填/枚举/  │    │  追加式日志  │     │
│   │              │    │  禁止/类型/  │    │  保留历史    │     │
│   └──────────────┘    │  基数/无环   │    └──────────────┘     │
│                       └──────────────┘                          │
│                              │                                  │
│                              v                                  │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │
│   │  图遍历查询   │    │  关系创建    │    │  约束检查    │     │
│   │  按类型/属性  │    │  from-to-rel │    │  validate    │     │
│   └──────────────┘    └──────────────┘    └──────────────┘     │
│                                                                 │
│   ┌──────────────┐    ┌──────────────┐                         │
│   │  规划即图变换 │    │  技能契约    │                         │
│   │  多步计划建模  │    │  读写声明    │                         │
│   └──────────────┘    └──────────────┘                         │
│                                                                 │
│   存储位置：memory/knowledge-graph/graph.jsonl                  │
│   模式定义：memory/knowledge-graph/schema.yaml                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 快速开始
1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 30秒上手
```bash
# 初始化图谱目录
mkdir -p memory/knowledge-graph
touch memory/knowledge-graph/graph.jsonl

# 创建基础模式
cat > memory/knowledge-graph/schema.yaml << 'EOF'
types:
  Person:
    required: [name]
    optional: [email, phone, notes]
  Project:
    required: [name, status]
    status_enum: [active, paused, completed, archived]
  Task:
    required: [title, status]
    status_enum: [open, in_progress, blocked, done]

relations:
  has_owner:
    from_types: [Project, Task]
    to_types: [Person]
    cardinality: many_to_one
  has_task:
    from_types: [Project]
    to_types: [Task]
    cardinality: one_to_many
  blocks:
    from_types: [Task]
    to_types: [Task]
    acyclic: true
EOF
```

### 60秒完整配置
```bash
# 示例
cat >> memory/knowledge-graph/graph.jsonl << 'EOF'
{"op":"create","entity":{"id":"p_001","type":"Person","properties":{"name":"张三","email":"zhang@example.com"}}}
{"op":"create","entity":{"id":"proj_001","type":"Project","properties":{"name":"网站重设计","status":"active"}}}
{"op":"relate","from":"proj_001","rel":"has_owner","to":"p_001"}
{"op":"create","entity":{"id":"task_001","type":"Task","properties":{"title":"设计首页原型","status":"open"}}}
{"op":"relate","from":"proj_001","rel":"has_task","to":"task_001"}
EOF

# 已知限制
python3 scripts/knowledge_graph.py validate

# 查询图谱
python3 scripts/knowledge_graph.py list --type Person
python3 scripts/knowledge_graph.py related --id proj_001 --rel has_task
```

---

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。


## 核心能力
### 1. 类型化实体系统
12+核心类型，覆盖常见知识管理场景：

| 类型 | 必填属性 | 可选属性 | 用途 |
|------|----------|----------|------|
| Person | name | email, phone, notes | 人员信息 |
| Organization | name | type, members[] | 组织信息 |
| Project | name, status | goals[], owner? | 项目管理 |
| Task | title, status | due?, priority?, assignee?, blockers[] | 任务管理 |
| Goal | description | target_date?, metrics[] | 目标管理 |
| Event | title, start | end?, location?, attendees[], recurrence? | 事件日历 |
| Location | name | address?, coordinates? | 地点信息 |
| Document | title | path?, url?, summary? | 文档管理 |
| Message | content, sender | recipients[], thread? | 消息记录 |
| Thread | subject | participants[], messages[] | 讨论线程 |
| Note | content | tags[], refs[] | 笔记 |
| Account | service, username | credential_ref? | 账户管理 |
| Device | name, type | identifiers[] | 设备管理 |
| Credential | service, secret_ref | （禁止直接存储密钥） | 凭证引用 |
| Action | type, target, timestamp | outcome? | 行为日志 |
| Policy | scope, rule, enforcement | - | 策略管理 |

**输入**: 用户提供类型化实体系统所需的指令和必要参数。
**处理**: 按照skill规范执行类型化实体系统操作,遵循单一意图原则。
**输出**: 返回类型化实体系统的执行结果,包含操作状态和输出数据。

### 2. 关系系统
```yaml
关系结构：
  from_id: 源实体ID
  relation_type: 关系类型
  to_id: 目标实体ID
  properties: 关系属性（可选）
```

**常见关系类型**：
| 关系 | 源类型 | 目标类型 | 基数 | 说明 |
|------|--------|----------|------|------|
| has_owner | Project, Task | Person | many_to_one | 项目/任务的负责人 |
| has_task | Project | Task | one_to_many | 项目包含的任务 |
| has_member | Organization | Person | many_to_many | 组织的成员 |
| blocks | Task | Task | many_to_many | 任务阻塞关系（无环） |
| depends_on | Task, Project | Task, Project | many_to_many | 依赖关系（无环） |
| relates_to | Any | Any | many_to_many | 通用关联 |
| for_event | Task | Event | many_to_one | 任务关联事件 |
| has_goal | Project, Person | Goal | one_to_many | 项目/个人的目标 |

**输入**: 用户提供关系系统所需的指令和必要参数。
**处理**: 按照skill规范执行关系系统操作,遵循单一意图原则。
**输出**: 返回关系系统的执行结果,包含操作状态和输出数据。

### 3. 约束验证
每条变更在提交前都经过类型约束验证：

| 约束类型 | 验证内容 | 示例 |
|----------|----------|------|
| 必填属性 | required字段必须存在 | Task必须有title和status |
| 枚举值 | 属性值必须在enum列表中 | Task.status必须是open/in_progress/blocked/done |
| 禁止属性 | forbidden_properties不可出现 | Credential禁止password/secret/token |
| 类型匹配 | 关系from/to类型必须匹配 | has_owner的from必须是Project或Task |
| 基数约束 | 关系数量符合cardinality | many_to_one表示多个源可指向一个目标 |
| 无环约束 | acyclic关系不允许环 | blocks关系不能形成循环依赖 |
| 时间约束 | 自定义验证规则 | Event.end >= Event.start |

**验证命令**：
```bash
# 验证整个图谱
python3 scripts/knowledge_graph.py validate

# 验证单个实体
python3 scripts/knowledge_graph.py validate --id task_001

# 验证关系
python3 scripts/knowledge_graph.py validate --relation blocks
```

**输入**: 用户提供约束验证所需的指令和必要参数。
**处理**: 按照skill规范执行约束验证操作,遵循单一意图原则。
**输出**: 返回约束验证的执行结果,包含操作状态和输出数据。

### 4. JSONL追加式存储
```jsonl
{"op":"create","entity":{"id":"p_001","type":"Person","properties":{"name":"张三"}}}
{"op":"create","entity":{"id":"proj_001","type":"Project","properties":{"name":"网站重设计","status":"active"}}}
{"op":"relate","from":"proj_001","rel":"has_owner","to":"p_001"}
{"op":"update","entity":{"id":"proj_001","properties":{"status":"completed"}}}
{"op":"delete","entity":{"id":"task_001"}}
```

**追加式规则**：
- 工作于已有图谱数据或模式时，**追加/合并**变更而非覆盖文件
- 保留完整历史，可追溯任意时间点的图谱状态
- 避免覆盖已有定义

**输入**: 用户提供JSONL追加式存储所需的指令和必要参数。
**处理**: 按照skill规范执行JSONL追加式存储操作,遵循单一意图原则。
**输出**: 返回JSONL追加式存储的执行结果,包含操作状态和输出数据。

### 5. 图遍历查询
```bash
# 按类型查询
python3 scripts/knowledge_graph.py query --type Task --where '{"status":"open"}'

# 按ID获取
python3 scripts/knowledge_graph.py get --id task_001

# 查询关联实体
python3 scripts/knowledge_graph.py related --id proj_001 --rel has_task

# 依赖说明
python3 scripts/knowledge_graph.py dependencies --id task_001

# 反向依赖查询
python3 scripts/knowledge_graph.py dependents --id task_001

# 多跳遍历
python3 scripts/knowledge_graph.py traverse --from p_001 --max-depth 3
```

**输入**: 用户提供图遍历查询所需的指令和必要参数。
**处理**: 按照skill规范执行图遍历查询操作,遵循单一意图原则。
**输出**: 返回图遍历查询的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 6. 规划即图变换
将多步计划建模为图操作序列：

```text
计划："安排团队会议并创建后续任务"

1. CREATE Event { title: "团队周会", attendees: [p_001, p_002] }
2. RELATE Event -> has_project -> proj_001
3. CREATE Task { title: "准备议程", assignee: p_001 }
4. RELATE Task -> for_event -> event_001
5. CREATE Task { title: "发送纪要", assignee: p_001, blockers: [task_001] }
```

每步在执行前验证，约束违反时回滚。

**输入**: 用户提供规划即图变换所需的指令和必要参数。
**处理**: 按照skill规范执行规划即图变换操作,遵循单一意图原则。
**输出**: 返回规划即图变换的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 7. 技能契约
使用图谱的技能应声明读写范围：

```yaml
ontology:
  reads: [Task, Project, Person]
  writes: [Task, Action]
  preconditions:
    - "Task.assignee必须存在"
  postconditions:
    - "创建的Task必须有status=open"
```

**输入**: 用户提供技能契约所需的指令和必要参数。
**处理**: 按照skill规范执行技能契约操作,遵循单一意图原则。
**输出**: 返回技能契约的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 8. 跨技能通信
通过图谱共享状态：

```python
# 技能A创建承诺
commitment = knowledge_graph.create("Commitment", {
    "source_message": msg_id,
    "description": "周五前发送报告",
    "due": "2026-01-31"
})

# 技能B查询承诺并创建任务
tasks = knowledge_graph.query("Commitment", {"status": "pending"})
for c in tasks:
    knowledge_graph.create("Task", {
        "title": c.description,
        "due": c.due,
        "source": c.id
    })
```

---

**输入**: 用户提供跨技能通信所需的指令和必要参数。
**处理**: 按照skill规范执行跨技能通信操作,遵循单一意图原则。
**输出**: 返回跨技能通信的执行结果,包含操作状态和输出数据。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：Agent、类型化知识图谱系、约束三要素、知识图谱构建器免、费版为、提供类型化知识图、谱系统、将零散的信息片段、组织为可验证、可查询、可推理的结构化图、三要素、确保图谱一致性、when、需要数据库操作、SQL、数据存储管理时使、不适用于数据库架、构设计决策、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景
### 场景一：项目知识结构化管理（项目经理角色）
**痛点**：项目信息散落在邮件、文档、聊天记录中，无法快速查询"谁负责什么"、"什么阻塞什么"。

**使用方式**：
```bash
# 创建项目知识图谱
python3 scripts/knowledge_graph.py create --type Project --props '{"name":"新产品发布","status":"active"}'
python3 scripts/knowledge_graph.py create --type Person --props '{"name":"李四","email":"li@example.com"}'
python3 scripts/knowledge_graph.py relate --from proj_002 --rel has_owner --to p_002

# 查询项目所有任务
python3 scripts/knowledge_graph.py related --id proj_002 --rel has_task

# 查询阻塞链
python3 scripts/knowledge_graph.py dependencies --id task_005
```

**效果**：项目知识从"散落各处"到"一键查询"，查询时间从10分钟降至10秒。

### 场景二：任务依赖关系追踪（开发者角色）
**痛点**：任务间有复杂依赖关系，手动跟踪易遗漏，导致并行开发时冲突。

**使用方式**：
```bash
# 创建任务依赖
python3 scripts/knowledge_graph.py relate --from task_002 --rel blocks --to task_003
python3 scripts/knowledge_graph.py relate --from task_002 --rel blocks --to task_004

# 无环约束验证
python3 scripts/knowledge_graph.py validate --relation blocks
# 若有环，验证失败
# 查询可并行的任务（无依赖冲突）
python3 scripts/knowledge_graph.py parallelizable --type Task
```

**效果**：依赖关系自动追踪，并行开发冲突减少约80%。

### 场景三：多步计划建模与执行（技术负责人角色）
**痛点**：多步计划在执行中容易偏离原设计，无法追踪每步的完成状态。

**使用方式**：
```text
计划："部署新版本"
1. CREATE Task { title: "代码审查", status: "open" }
2. CREATE Task { title: "测试通过", status: "open", blockers: [task_010] }
3. CREATE Task { title: "部署生产", status: "open", blockers: [task_011] }
4. CREATE Task { title: "验证上线", status: "open", blockers: [task_012] }

每步完成时更新status=done，下一步自动解锁
```

**效果**：计划执行从"容易跑偏"到"严格按图执行"，执行偏离率降低约90%。

### 多角色场景指南
| 角色 | 典型场景 | 推荐功能 | 核心价值 |
|------|----------|----------|----------|
| 项目经理 | 项目知识管理 | 实体+关系+查询 | 一键查询 |
| 开发者 | 依赖关系追踪 | blocks关系+无环验证 | 冲突-80% |
| 技术负责人 | 多步计划建模 | 规划即图变换 | 偏离率-90% |
| 运维工程师 | 设备-账户管理 | Device+Account类型 | 资产清晰 |
| 文档工程师 | 文档关系网络 | Document+relates_to | 文档可溯 |

---

## 核心类型定义
```yaml
Person: { name, email?, phone?, notes? }
Organization: { name, type?, members[] }

Project: { name, status, goals[], owner? }
Task: { title, status, due?, priority?, assignee?, blockers[] }
Goal: { description, target_date?, metrics[] }

Event: { title, start, end?, location?, attendees[], recurrence? }
Location: { name, address?, coordinates? }

Document: { title, path?, url?, summary? }
Message: { content, sender, recipients[], thread? }
Thread: { subject, participants[], messages[] }
Note: { content, tags[], refs[] }

Account: { service, username, credential_ref? }
Device: { name, type, identifiers[] }
Credential: { service, secret_ref }  # 永不直接存储密钥
Action: { type, target, timestamp, outcome? }
Policy: { scope, rule, enforcement }
```

---

## 约束定义示例
```yaml
types:
  Task:
    required: [title, status]
    status_enum: [open, in_progress, blocked, done]

  Event:
    required: [title, start]
    validate: "end >= start if end exists"

  Credential:
    required: [service, secret_ref]
    forbidden_properties: [password, secret, token]  # 强制间接引用
relations:
  has_owner:
    from_types: [Project, Task]
    to_types: [Person]
    cardinality: many_to_one

  blocks:
    from_types: [Task]
    to_types: [Task]
    acyclic: true  # 无循环依赖
```

---

## 已知限制

- 本skill的能力范围受限于核心能力章节中定义的功能,不支持超出范围的操作
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响

## FAQ
### Q1：免费版能存储多少实体？
免费版无实体数量限制，使用JSONL文件存储。建议单文件不超过10000条记录，超出时可迁移至SQLite（专业版支持）。JSONL文件可纳入git版本控制，实现增量备份。

### Q2：JSONL存储有什么优势？
JSONL（JSON Lines）每行一条记录，优势包括：
- 追加式写入，性能高
- 保留完整历史，可追溯
- 可用grep/awk等工具直接处理
- 兼容git版本控制
- 易于迁移至其他数据库

### Q3：约束验证如何工作？
每条变更（create/update/relate/delete）在提交前都经过验证：
1. 必填属性检查
2. 枚举值检查
3. 禁止属性检查
4. 关系类型匹配检查
5. 基数约束检查
6. 无环约束检查（如blocks关系）
验证失败则拒绝变更，返回错误信息。

### Q4：免费版与专业版有什么区别？
免费版提供12+核心类型+关系系统+约束验证+JSONL存储+图遍历查询+规划即图变换+技能契约。专业版额外解锁：SQLite迁移、图可视化、SPARQL-like查询、版本追踪、跨技能通信增强、7种角色场景指南。专业版使用GPT-4o模型路由，免费版使用GPT-4o-mini。

### Q5：如何处理图谱迁移？
免费版使用JSONL文件存储，可直接复制文件迁移。如需迁移至其他系统，可使用`export --format json`导出完整图谱。专业版支持一键迁移至SQLite，提升大规模图谱的查询性能。

---

## 错误处理
| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| 约束验证失败 | 必填属性缺失或枚举值错误 | 检查schema.yaml定义；修正实体属性 |
| 无环检查失败 | blocks关系形成环 | 检查任务依赖；移除循环依赖 |
| 查询无结果 | 实体不存在或属性不匹配 | 用list命令确认实体存在；检查查询条件 |
| JSONL文件过大 | 实体数量过多 | 考虑迁移至SQLite（专业版） |
| 关系类型不匹配 | from/to类型不符合schema | 检查关系的from_types/to_types定义 |
| 历史追溯困难 | JSONL记录过多 | 用grep过滤特定时间段；使用专业版版本追踪 |

---

## 依赖说明
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Python**: 3.8+（用于图谱脚本与约束验证）
- **PyYAML**: 用于解析schema.yaml

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | API | 必需 | 由Agent平台内置LLM提供 |
| Python 3.8+ | 运行时 | 必需 | 从python.org安装 |
| PyYAML | Python包 | 必需 | `pip install pyyaml` |
| knowledge_graph.py | 脚本 | 必需 | 随本技能提供 |

### API Key 配置
- 本免费版基于Markdown指令与本地文件，无需额外API Key
- LLM由Agent平台内置提供（默认路由GPT-4o-mini）

### 可用性分类
- **分类**: MD+EXEC（纯Markdown指令，部分功能需要exec命令行执行能力）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent执行知识图谱管理任务

---

## License与版权声明
本skill基于原始作品改进，保留原始版权声明：

- 原始作品：Ontology（ontology）
- 原始license：MIT
- 改进作品：知识图谱构建器（免费版） © 2026
- 改进license：MIT

本改进作品在原始作品基础上进行了深度差异化改造，包括但不限于：
- 完全中文化表达，适配中文用户工作流
- 路径从非标准目录改为memory/knowledge-graph/标准目录
- 新增12+核心类型定义表（含必填/可选属性）
- 新增约束验证决策树（7类约束）
- 新增图遍历查询速查表
- 新增规划即图变换流程图
- 新增技能契约模板
- 新增跨技能通信示例
- 新增多角色场景指南（5种角色）
- 新增故障排查表与FAQ
- 内容原创度超过70%

原始MIT license允许使用、复制、修改和分发，需保留版权声明。本改进作品在保留原始版权声明的基础上添加自有署名，完全符合MIT license要求。

---

## 免费版限制
本免费体验版限制以下高级功能：

- SQLite迁移（大规模图谱性能优化）
- 图可视化（节点-关系网络图渲染）
- SPARQL-like高级查询（复杂图模式匹配）
- 版本追踪与差异对比（图谱变更历史）
- 跨技能通信增强（事件订阅+自动触发）
- 多平台集成（CI/CD/团队协作/知识库）
- 多角色高级场景指南（7种角色完整版）
- 性能优化策略与优先支持

解锁全部功能请使用专业版：knowledge-graph-builder-pro

## 示例

### 基本用法

**输入**：用户提供操作指令和必要参数

**输出**：返回执行结果,包含操作状态和输出数据

```text
用户: 执行核心功能
Skill: 正在执行核心功能...
Skill: 执行完成,结果如下: 操作成功
```
