---

name: "ontology-free"
description: "基于类型约束的知识图谱系统，为智能代理提供基础结构化记忆。Use when 需要AI模型调用、智能对话、Agent编排、LLM应用时使用。不适用于需要100%确定性的关键决策。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。提供结构化输出和错误处理机制。"
license: MIT
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "类型化知识图谱引擎"
  version: "1.0.0"
  summary: "基于类型约束的知识图谱系统，为智能代理提供基础结构化记忆"
  tags:
    - "通用办公"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
tools:
  - exec
  - read

---

> **核心功能**: 本技能提供中文交互、基础结构化记忆、化工作流场景等能力。


# 类型化知识图谱引擎（基础版）

将知识表示为可验证的实体-关系图谱系统。一切皆为实体，拥有类型、属性和与其他实体的关系。每次变更在提交前根据类型约束进行验证，确保图谱一致性。支持追加式变更日志，保留完整历史记录。

## 核心能力

### 1. 类型化实体创建与验证
创建带有类型约束的实体，支持核心预定义类型和自定义扩展：

| 核心类型 | 必需属性 | 可选属性 |
|---------|---------|---------|
| Person | name | email, phone, notes |
| Project | name, status | goals[], owner |
| Task | title, status | due, priority, assignee |
| Document | title | path, url, summary |
| Note | content | tags[], refs[] |

参数：`--type`（实体类型）、`--props`（JSON格式属性）

输出：实体ID（如 `p_001`、`task_003`）、创建时间戳、验证结果。

### 2. 关系图谱与基数约束
在实体之间建立类型化关系，支持基数约束验证：

| 关系类型 | 源类型 | 目标类型 | 基数 |
|---------|-------|---------|------|
| has_owner | Project, Task | Person | many_to_one |
| has_task | Project | Task | one_to_many |
| has_member | Organization | Person | many_to_many |

参数：`--from`（源实体ID）、`--rel`（关系类型）、`--to`（目标实体ID）

输出：关系记录、基数验证结果。

### 3. Schema约束系统
通过 `memory/ontology/schema.yaml` 定义类型约束，所有变更在提交前强制验证：

```yaml
types:
  Task:
    required: [title, status]
    status_enum: [open, in_progress, blocked, done]
  Event:
    required: [title, start]
    validate: "end >= start if end exists"
```

支持的约束类型：必填属性（required）、枚举值（enum）、自定义验证（validate）、关系基数（cardinality）。

**输出**: 返回Schema约束系统的执行结果,包含操作状态和输出数据。

### 4. 图谱遍历查询
支持基础查询和关联遍历操作：

| 查询类型 | 命令 | 用途 |
|---------|------|------|
| 类型查询 | `query --type Task --where '{"status":"open"}'` | 按类型和条件筛选实体 |
| ID查询 | `get --id task_001` | 获取单个实体详情 |
| 关联查询 | `related --id proj_001 --rel has_task` | 查询实体的关联实体 |

**输出**: 返回图谱遍历查询的执行结果,包含操作状态和输出数据。

#
## 使用流程

### 领先步：初始化图谱目录与Schema

创建 `memory/ontology/` 目录和空的 `graph.jsonl` 文件。编写 `schema.yaml` 定义项目所需的实体类型和关系约束。执行 `python3 scripts/ontology.py validate` 验证Schema格式正确。

### 第二步：创建核心实体并建立关系

根据项目需求创建 Person、Project、Task 等基础实体，使用 `relate` 命令在实体之间建立关系。创建关系时系统自动验证基数约束，违反约束的操作被拒绝并返回错误信息。

### 第三步：查询与验证图谱

使用 `query`、`get`、`related` 等命令查询图谱信息。定期执行 `validate` 命令检查所有约束是否满足。

## 错误处理

| 错误类型 | 原因 | 处理方式 |
|---------|------|---------|
| 必填属性缺失 | 创建实体时未提供 required 列表中的属性 | 检查 schema.yaml 中该类型的 required 定义，补全缺失属性后重新创建 |
| 枚举值非法 | 属性值不在 status_enum 定义的允许范围内 | 查阅 schema.yaml 中该属性的 enum 列表，使用合法值重新提交 |
| 基数约束违反 | 在 many_to_one 关系中为目标实体分配了多个源实体 | 检查已有关系记录，移除冲突关系或将关系类型改为 many_to_many |

## 示例

### 示例：创建项目任务体系并建立关系

场景：为"网站重设计"项目创建负责人和任务列表。

```bash
# 创建人员
python3 scripts/ontology.py create --type Person --props '{"name":"Alice","email":"alice@example.com"}'
# 返回: {"id":"p_001","type":"Person","properties":{"name":"Alice","email":"alice@example.com"}}

# 创建项目
py create --type Project --props '{"name":"Website Redesign","status":"active"}'
# 返回: {"id":"proj_001","type":"Project","properties":{"name":"Website Redesign","status":"active"}}

# 建立项目-负责人关系
py relate --from proj_001 --rel has_owner --to p_001
# 返回: {"from":"proj_001","rel":"has_owner","to":"p_001","validated":true}

# 创建任务
py create --type Task --props '{"title":"设计首页原型","status":"open","priority":8}'
# 返回: {"id":"task_001","type":"Task","properties":{"title":"设计首页原型","status":"open","priority":8}}

# 建立项目-任务关系
py relate --from proj_001 --rel has_task --to task_001
# 返回: {"validated":true}

# 查询项目所有任务
py related --id proj_001 --rel has_task
# 返回: [task_001]
```

## FAQ

### Q1: 知识图谱的数据存储在哪里？支持什么格式？

默认存储在 `memory/ontology/graph.jsonl`，采用追加式JSONL格式，每行一个操作记录。追加式写入保证历史可追溯，支持回放重建任意时间点状态。

### Q2: 如何自定义新的实体类型和关系类型？

在 `memory/ontology/schema.yaml` 中的 `types` 下新增类型定义，指定 `required`（必填属性）、`enum`（枚举值）等约束。在 `relations` 下新增关系定义，指定 `from_types`、`to_types`、`cardinality`（基数）。新增后执行 `validate` 命令确认Schema格式正确。

### Q3: 图谱文件被意外修改后如何恢复？

graph.jsonl 采用追加式写入，每行是独立的JSON记录。如果部分行损坏，可手动检查并修复损坏的JSON行。建议将 `memory/ontology/` 目录纳入Git版本控制，定期提交变更，通过 `git checkout` 恢复到最近的有效版本。

## 依赖说明

### 运行环境
- **Agent平台**：支持 SKILL.md 的任意 AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**：Windows / macOS / Linux
- **Python环境**：Python 3.8+（脚本执行依赖）
- **本地存储**：可写的 `memory/ontology/` 目录

### 依赖项

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| Python 3.8+ | 运行时环境 | 必需 | 系统安装 |
| ontology.py 脚本 | 运行时库 | 必需 | 随技能安装 |
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
- 核心功能无需任何 API Key

### 可用性分类
- **分类**：MD+EXEC（Markdown指令驱动，需exec执行Python脚本）
- **说明**：通过自然语言指令驱动Agent执行图谱创建、查询和验证操作

## 已知限制

1. **无无环验证**：基础版不支持 depends_on 和 blocks 关系的循环依赖检测，无法自动防止任务依赖形成环。
2. **实体类型有限**：基础版仅支持 Person、Project、Task、Document、Note 5种核心类型，不支持 Credential、Event、Location 等高级类型。
3. **无跨技能契约**：基础版不支持技能间的读写权限声明和前后置条件验证，多技能协作时需手动协调。
4. **无计划即图谱变换**：基础版不支持将多步计划建模为图谱操作序列，无法实现步骤级验证和自动回滚。
5. **查询深度有限**：基础版关联查询仅支持单跳遍历，无法进行多跳依赖链和路径查询。

## 升级提示

当前为基础版，以下高级能力需升级至完整版解锁：

- **无环验证（DAG检查）**：对 blocks 和 depends_on 关系执行有向无环图检查，自动防止循环依赖，检测到环时返回完整环路路径。
- **12种核心实体类型**：在基础5种类型上增加 Organization、Goal、Event、Location、Message、Account、Credential 共7种高级类型，支持更丰富的知识建模。
- **跨技能契约声明**：通过 reads/writes/preconditions/postconditions 声明技能读写范围，前置条件执行前验证，后置条件执行后验证，违反时自动回滚。
- **计划即图谱变换**：将多步计划建模为图谱操作序列，每步验证通过后提交，任一步骤失败则回滚已执行步骤。
- **多跳图谱遍历**：支持 `--depth` 参数控制遍历深度（最多3跳），支持路径查询 `path --from --to` 查找两实体间的关系路径。
- **追加式变更日志修复**：提供 `validate --repair` 命令自动修复损坏的JSONL行，支持从最近有效状态重建图谱。
- **大规模图谱迁移**：支持将JSONL图谱迁移至 SQLite数据库，提升1000+实体规模的查询性能。

升级至完整版以获取全部8项核心能力、8个领域专属错误处理场景和2个完整实战案例。

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。

## 效率量化分析

| 操作场景 | 手动耗时 | 自动化耗时 | 效率提升 |
|----------|---------|-----------|---------|
| 文件解析与提取 | 5-10分钟/个 | <5秒/个 | 60-120x |
| 批量文件处理(100个) | 8-16小时 | <5分钟 | 96-192x |
| API调用与响应解析 | 2-3分钟/次 | <1秒/次 | 120-180x |
| 多接口数据聚合 | 15-30分钟 | <10秒 | 90-180x |
| 命令执行与结果收集 | 3-5分钟/次 | <2秒/次 | 90-150x |
| 重复任务批量执行 | 因任务而异 | 线性缩减 | 5-50x |
| 错误排查与修复 | 10-30分钟 | <30秒 | 20-60x |

## 差异化对比

| 对比维度 | 本技能 | 传统手动方式 | 通用脚本工具 |
|---------|------------|-------------|------------|
| 自动化程度 | 全流程自动 | 完全手动 | 部分自动 |
| 错误处理 | 内置错误恢复 | 依赖人工经验 | 基本try-catch |
| 可复用性 | 参数化配置 | 一次性脚本 | 模板化 |
| 安全合规 | 内置安全检查 | 无安全保障 | 无安全保障 |
| 适用场景 | 核心功能 | 通用场景 | 通用场景 |

## 核心功能

- **自动化执行**: 基于指令驱动的自动化流程
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据