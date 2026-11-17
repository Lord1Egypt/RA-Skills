---
name: planning-toolkit
version: 2.0.0
description: "完整规划工具包——需求规格（做什么）+ 任务规划（怎么拆）+ 迭代执行（怎么做）+ 自主清理（怎么优化）"
tags: [planning, task-breakdown, decomposition, vertical-slicing, templates, iterative-loop, persistent-memory, spec-writing, prd]
---

# Planning Toolkit v2.0.0

完整规划工具包：**需求规格（做什么）→ 任务规划（怎么拆）→ 迭代执行（怎么做）→ 自主清理（怎么优化）**。

> v2.0.0 新增：Part 0 需求规格（合并自 spec-writing v1.1.0）

---

## Part 0: 需求规格（v2.0.0 新增）

> 来源：spec-writing v1.1.0（Anthropic 官方 spec-driven-development）
> 核心理念：在写任何代码之前先写结构化规格文档。规格是你与人类工程师之间的共享真相来源——定义构建什么、为什么、如何知道完成。没有规格的代码就是猜测。

### 0.1 门控工作流

规格驱动开发有四个阶段。当前阶段未验证前，不要进入下一阶段。

```
规格说明 ──→ 计划 ──→ 任务 ──→ 实现
    ▼         ▼       ▼       ▼
  人类       人类     人类     人类
  审查       审查     审查     审查
```

**何时使用：**
- 开始新项目或功能
- 需求模糊或不完整
- 变更涉及多个文件或模块
- 即将做出架构决策
- 任务实现需要超过30分钟

**不适用场景：** 单行修复、拼写更正、或需求明确且自包含的变更。

### 0.2 假设浮出机制

在写任何规格内容之前，列出你的假设：

```
我的假设：
1. 这是一个 Web 应用（不是原生移动应用）
2. 认证使用基于会话的 cookie（不是 JWT）
3. 数据库是 PostgreSQL（基于现有 Prisma schema）
4. 我们只针对现代浏览器（不支持 IE11）

现在纠正我，否则我将按这些假设继续。
```

不要默默填充模糊的需求。规格的全部意义是在代码编写*之前*浮出误解。

### 0.3 六领域规格模板

编写覆盖六个核心领域的规格文档：

1. **目标** — 我们在构建什么？为什么？用户是谁？成功是什么样？
2. **命令** — 完整的可执行命令和标志
   ```
   构建: npm run build
   测试: npm test -- --coverage
   Lint: npm run lint --fix
   开发: npm run dev
   ```
3. **项目结构** — 源代码在哪里，测试在哪里，文档在哪里
4. **代码风格** — 一个展示你风格的真实代码片段胜过三段描述它的文字
5. **测试策略** — 什么框架，测试在哪里，覆盖率期望
6. **边界** — 三层系统：
   - **总是做：** 提交前运行测试，遵循命名约定，验证输入
   - **先问：** 数据库 schema 变更，添加依赖，更改 CI 配置
   - **绝不做：** 提交密钥，编译 vendor 目录，未经批准删除失败的测试

**规格模板：**

```markdown
# 规格: [项目/功能名称]

## 目标
[我们在构建什么以及为什么。用户故事或验收标准。]

## 技术栈
[框架、语言、关键依赖及版本]

## 命令
[构建、测试、lint、开发——完整命令]

## 项目结构
[目录布局及描述]

## 代码风格
[示例片段 + 关键约定]

## 测试策略
[框架、测试位置、覆盖率要求、测试级别]

## 边界
- 总是: [...]
- 先问: [...]
- 绝不做: [...]

## 成功标准
[我们如何知道这已完成——具体、可测试的条件]

## 开放问题
[任何需要人类输入的未解决事项]
```

### 0.4 成功标准转化

将模糊需求转化为具体条件：

```
需求: "让仪表板更快"

重构的成功标准：
- 仪表板 LCP < 2.5s 在 4G 连接下
- 初始数据加载在 < 500ms 内完成
- 加载期间无布局偏移 (CLS < 0.1)

这些是正确的目标吗？
```

### 0.5 PRD 结构模板

对于产品级需求文档，使用以下结构：

**1. 问题陈述**
- 用2-3句话描述用户问题
- 谁遇到这个问题，频率如何
- 不解决的成本（用户痛点、业务影响、竞争风险）

**2. 目标**
- 3-5个具体的、可衡量的成果
- 每个目标回答："我们如何知道这成功了？"

**3. 非目标**
- 3-5个本功能明确不做的事
- 每个非目标简要说明为什么不在范围内

**4. 用户故事**

标准格式："作为[用户类型]，我想要[能力]，以便[收益]"

**常见错误：**
- 太模糊："作为用户，我想要产品更快"
- 预设方案："作为用户，我想要一个下拉菜单"
- 无收益："作为用户，我想要点击一个按钮"

**5. 需求分级（MoSCoW框架）**

| 级别 | 说明 |
|------|------|
| **Must have (P0)** | 不可协商，没有这些功能无法发布 |
| **Should have (P1)** | 重要但对发布不关键 |
| **Could have (P2)** | 如果时间允许则期望 |
| **Won't have (this time)** | 明确不在本次范围内 |

**6. 成功指标**

**领先指标（天到周）：** 采用率、激活率、任务完成率、完成时间、错误率

**滞后指标（周到月）：** 留存影响、收入影响、NPS、支持工单减少

**7. 验收标准**

使用 Given/When/Then 格式：
```
Given [前置条件]
When [用户操作]
Then [预期结果]
```

**8. 开放问题**

**9. 时间线考虑**

### 0.6 HTML 可视化输出

当需要将功能规格转化为团队可阅读的功能讲解文档时，可输出交互式HTML页面。

**适用场景：**
- 向工程团队讲解新功能的设计和实现
- 生成带代码样本和配置说明的功能文档
- 展示 Before/After 行为对比

**HTML 结构要求：**

1. **TL;DR** — 第一段话让读者知道功能做什么
2. **Before/After对比** — 用视觉对比展示行为变化
3. **逐文件Walkthrough** — 按阅读顺序排列
4. **配置表** — 所有可配置项列成表格（类型、默认值、说明）
5. **代码样本** — 关键逻辑的代码片段
6. **文件树** — 展示新增/修改的文件结构

**样式规范：**

```css
:root {
  --bg: #f6f8fa;
  --surface: #fff;
  --text: #1f2328;
  --text-muted: #656d76;
  --border: #d0d7de;
  --accent: #0969da;
  --green: #1a7f37;
  --red: #cf222e;
}
```

### 0.7 保持规格活跃

规格是活的文档，不是一次性制品：

- **决策变化时更新** — 如果发现数据模型需要更改，先更新规格，再实现
- **范围变化时更新** — 添加或削减的功能应反映在规格中
- **提交规格** — 规格属于版本控制，与代码一起
- **在 PR 中引用规格** — 链接回每个 PR 实现的规格部分

### 0.8 验证清单

在进入实现之前确认：

- [ ] 规格覆盖所有六个核心领域
- [ ] 人类已审查并批准规格
- [ ] 成功标准具体且可测试
- [ ] 边界（总是/先问/绝不做）已定义
- [ ] 规格已保存到仓库中的文件

---

## Part 1: 任务分解方法论

### Step 1: Enter Plan Mode

在写任何代码之前，以只读模式运行：
- 读取规格和相关代码库部分
- 识别现有模式和约束
- 映射组件间的依赖关系
- 记录风险和未知项

**规划期间不要写代码。** 输出是保存到 `tasks/plan.md` 的计划文档和保存到 `tasks/todo.md` 的任务列表，不是实现。

### Step 2: Identify the Dependency Graph

映射依赖关系图：
```
数据库 schema
    │
    ├── API 模型/类型
    │       │
    │       ├── API 端点
    │       │       │
    │       │       └── 前端 API 客户端
    │       │               │
    │       │               └── UI 组件
    │       │
    │       └── 验证逻辑
    │
    └── 种子数据 / 迁移
```

实施顺序遵循依赖图自底向上：先构建基础层。

### Step 3: Slice Vertically

不要先建整个数据库、再建所有API、再建所有UI——而是**一次构建一个完整的功能路径**。

**错误（水平切片）：**
```
Task 1: 构建整个数据库 schema
Task 2: 构建所有 API 端点
Task 3: 构建所有 UI 组件
Task 4: 连接一切
```

**正确（垂直切片）：**
```
Task 1: 用户可以创建账户（注册 schema + API + UI）
Task 2: 用户可以登录（auth schema + API + UI）
Task 3: 用户可以创建任务（task schema + API + UI）
Task 4: 用户可以查看任务列表（查询 + API + UI）
```

每个垂直切片交付可工作、可测试的功能路径。

### Step 4: Write Tasks

每个任务遵循以下结构：
```markdown
## Task [N]: [简短描述性标题]

**描述:** 一段话说明这个任务完成什么。
**验收标准:**
- [ ] [具体、可测试的条件]
- [ ] [具体、可测试的条件]

**验证:**
- [ ] 测试通过: `npm test -- --grep "feature-name"`
- [ ] 构建成功: `npm run build`
- [ ] 手动检查: [描述验证内容]

**依赖:** [依赖的任务编号，或"无"]

**可能涉及的文件:**
- `src/path/to/file.ts`
- `tests/path/to/test.ts`

**预估范围:** [Small: 1-2 files | Medium: 3-5 files | Large: 5+ files]
```

### Step 5: Order and Checkpoint

排列任务使：
1. 依赖被满足（先建基础层）
2. 每个任务后系统处于可工作状态
3. 每 2-3 个任务后设置验证检查点
4. 高风险任务排在前面（快速失败）

---

## Part 2: 持久化文件模板

> 基于 Manus context engineering 原则：Context Window = RAM（易失、有限），Filesystem = Disk（持久、无限）。**任何重要的东西都写到磁盘上。**

### 三个核心文件

| 文件 | 用途 | 何时更新 |
|------|------|----------|
| `task_plan.md` | 阶段、进度、决策 | 每个阶段完成后 |
| `findings.md` | 研究、发现、数据 | 任何发现后立即 |
| `progress.md` | 会话日志、测试结果 | 整个会话期间 |

### 初始化规划目录

```bash
# 创建规划目录
mkdir -p .planning/$(date +%Y-%m-%d)-task-slug/

# 复制模板
cp skills/planning-toolkit/templates/task_plan.md .planning/...
cp skills/planning-toolkit/templates/findings.md .planning/...
cp skills/planning-toolkit/templates/progress.md .planning/...
```

或使用脚本：
```bash
bash scripts/init-planning.sh "task-slug"
```

### 关键规则

#### 1. 2-Action Rule
每执行 2 次浏览/浏览器/搜索操作后，**立即**将关键发现保存到 `findings.md`。防止视觉/多模态信息丢失。

#### 2. Read Before Decide
在做重大决策前，读取计划文件。这使目标保持在注意力窗口内，防止"中间丢失"漂移。

#### 3. Update After Act
完成任何阶段后：
- 标记阶段状态：`in_progress` → `complete`
- 记录遇到的错误
- 记录创建/修改的文件

#### 4. Log ALL Errors
每个错误都进入计划文件。这建立知识并防止重复。

```markdown
## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| FileNotFoundError | 1 | Created default config |
| API timeout | 2 | Added retry logic |
```

#### 5. Never Repeat Failures
```
if action_failed:
    next_action != same_action
```
跟踪你尝试了什么。改变方法。

### Read vs Write 决策矩阵

| 情况 | 动作 | 原因 |
|------|------|------|
| 刚写了文件 | 不要读 | 内容还在上下文中 |
| 查看了图片/PDF | 立即写入发现 | 多模态 → 文本前丢失 |
| 浏览器返回数据 | 写入文件 | 截图不持久化 |
| 开始新阶段 | 读取计划/发现 | 如果上下文过时则重新定位 |
| 发生错误 | 读取相关文件 | 需要当前状态来修复 |
| 间隔后恢复 | 读取所有规划文件 | 恢复状态 |

### 5-Question Reboot Test

如果你能回答这些，你的上下文管理就是稳固的：

| 问题 | 答案来源 |
|------|----------|
| 我在哪？ | task_plan.md 中的当前阶段 |
| 我要去哪？ | 剩余阶段 |
| 目标是什么？ | 计划中的目标陈述 |
| 我学到了什么？ | findings.md |
| 我做了什么？ | progress.md |

---

## Part 3: 增强计划格式

### 计划文档头部元数据

每个计划必须以以下头部开始：

```markdown
# [Feature Name] Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** [一句话描述构建什么]

**Architecture:** [2-3句话描述方案]

**Tech Stack:** [关键技术/库]

**Effort:** ~N周 | **涉及包:** N个 | **新表:** N个 | **Feature flag:** 名称
```

### 里程碑时间线

按周拆分，每个里程碑独立可审查：

```markdown
### Milestone 1: Schema & API Contract (Week 1 · Mon–Tue)

新表、迁移和API桩。无UI。契约在继续之前先审查。

- `packages/db` — 新迁移
- `packages/api` — tRPC路由桩

### Milestone 2: Core Component (Week 1 · Wed–Fri)

静态组件从fixture渲染。提交时乐观插入，失败时回滚。
```

### 数据流图

使用ASCII图描述从客户端到持久化的数据流。实线=请求/响应，虚线=实时/异步。

```markdown
### Data Flow: Optimistic Write Path

Client                    API Server              Database
  │                          │                       │
  ├─► POST /tasks (optimistic)                       │
  │  ├─► update local cache immediately              │
  │  └─► send mutation ─────►┤                       │
  │                           ├─► validate ─────────►┤
  │                           │                       │
  │                           │◄─ 200 OK ─────────────┤
  │◄─ cache update ──────────┤                       │
  │                          │                       │
```

### Mockup线框图

不需要像素级精确——只要让审查者和实现者对布局和放置达成一致即可。

```markdown
### A · Thread Inside an Open Task Card

┌──────────────────────────────────────┐
│  Ship onboarding empty-state rewrite  │
│  BIR-1142 · Assigned to Priya · Due  │
├──────────────────────────────────────┤
│  Priya: Should we add an illustration?│
│  You: Yes, let me mock it up          │
│                                       │
│  ┌─────────────────────────────────┐ │
│  │ Add a comment...          Post │ │
│  └─────────────────────────────────┘ │
└──────────────────────────────────────┘
```

### 风险表

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Migration locks table during deploy | Medium | High | Run with `CONCURRENTLY`; schedule off-peak |
| Realtime subscription leaks memory | Low | Medium | Add max-subscription cap; monitor heap |

### 执行交接

保存计划后，提供执行选择：

**"计划已保存到 `tasks/plan.md`。两种执行选项：**

1. **子代理驱动（当前会话）** — 每个任务分派新子代理，任务间审查
2. **并行会话（独立）** — 打开新会话批量执行，带检查点

选择哪种方式？"

---

## Part 4: 迭代执行模式

### 触发条件
- 迭代循环/迭代优化/循环改进/自动重试/性能迭代/iterative loop

### 迭代模式

| 模式 | 说明 | 适用场景 |
|------|------|---------|
| **fixed** | 执行指定次数后停止 | 固定轮次的优化任务 |
| **max** | 最多执行N次，满足完成条件时提前退出 | 有明确完成标准的任务 |
| **adaptive** | 根据每轮改进幅度动态决定，连续N轮无改进则停止 | 不确定需要多少轮的任务 |

### 工作流程

```
1. 初始化循环 → loop-controller.py init --name "task" --mode max --max 10 --condition "regex:BUILD SUCCESS"
2. 执行迭代循环：
   for iteration in range(max_iterations):
     a. 检查状态 → loop-controller.py check
     b. 执行任务（编码/测试/修复等）
     c. 评估结果 → 检查完成条件
     d. 更新状态 → loop-controller.py update --result ...
     e. 如果完成 → loop-controller.py complete
3. 与sessions_spawn集成：长任务迭代spawn子代理执行每轮
```

### 完成条件检测

| 类型 | 语法 | 说明 |
|------|------|------|
| 正则匹配 | `--condition "regex:BUILD SUCCESS"` | 检查输出是否匹配模式 |
| 文件检查 | `--condition "file:output/result.txt"` | 检查文件是否存在 |
| 文件变化 | `--condition "file-changed:src/main.py"` | 检查文件内容变化 |
| LLM判断 | `--condition "llm:代码质量达到可发布标准"` | LLM评估是否满足要求 |

### 状态文件格式

```json
{
  "name": "任务名称",
  "mode": "fixed|max|adaptive",
  "max_iterations": 10,
  "current_iteration": 3,
  "completion_check": { "type": "regex", "pattern": "检测模式" },
  "history": [
    { "iteration": 1, "timestamp": "...", "result": "pass|fail|partial", "summary": "...", "metrics": {} }
  ],
  "artifacts": ["产出文件列表"],
  "status": "running|completed|failed|cancelled"
}
```

### 与其他技能集成

#### 与 coding-framework 集成（模式3核心控制器）

```
coding-framework 模式3 触发
  → iterative-loop init → 初始化循环状态
  → 循环执行：分步迭代 → 改进 → 验证
  → iterative-loop check → 是否继续？
  ├─ 是 → 继续循环
  └─ 否 → iterative-loop complete → 输出结果
```

#### 与 tdd 配合（迭代式测试修复）

```
iterative-loop init --condition "regex:All tests passed"
  → 每轮迭代调用 tdd 技能：
  → 运行测试
  → 识别失败
  → tracer-bullet 修复
  → 重新验证
  → iterative-loop complete
```

#### 与 diagnose 配合（性能回归迭代优化）

```
diagnose 定位性能问题
  → iterative-loop init --mode adaptive --metric "response_time_p95"
  → 每轮迭代：
  → 应用优化
  → 测量性能指标
  → 评估改进幅度
  → 连续 N 轮改进 < 阈值 → 停止
```

### 错误处理与降级策略

#### 控制器脚本失败

| 场景 | 降级方案 |
|------|----------|
| loop-controller.py 不可用 | 使用内存状态管理（JSON 变量），手动跟踪迭代 |
| 状态文件损坏 | 从备份恢复或重新 init，记录已完成的迭代 |
| 状态文件锁冲突 | 等待 5 秒后重试，最多 3 次 |

#### 迭代执行失败

| 场景 | 降级方案 |
|------|----------|
| 单轮迭代超时 | 标记该轮 `timeout`，继续下一轮 |
| 连续 3 轮失败 | 暂停循环，报告用户，请求调整策略 |
| 完成条件永远无法满足 | adaptive 模式用 patience 机制自动停止 |
| 子代理 spawn 失败 | 回退到主会话执行该轮迭代 |

#### 资源限制

| 场景 | 降级方案 |
|------|----------|
| 达到最大迭代次数 | 输出当前最佳结果 + 未完成项清单 |
| 内存/磁盘不足 | 清理历史 artifact，只保留最新状态 |
| API 调用配额耗尽 | 暂停循环，等待配额恢复后继续 |

---

## Part 5: 自主循环与清理

### 模式A: De-Sloppify（清理模式）

**问题**：LLM做TDD实现时过于字面理解，会产生冗余代码（过度测试、过度防御）。

**解决方案**：不约束实现者，让它彻底。然后添加专注的清理agent。

```bash
# Step 1: 实现（让它彻底）
"Implement the feature with full TDD. Be thorough with tests."

# Step 2: De-Sloppify（独立上下文，专注清理）
"Review all changes in the working tree. Remove:
- Tests that verify language/framework behavior rather than business logic
- Redundant type checks that the type system already enforces
- Over-defensive error handling for impossible states
- Console.log statements / Commented-out code
Keep all business logic tests. Run the test suite after cleanup."
```

**核心洞察**："两个专注的Agent优于一个受约束的Agent"

#### De-Sloppify 检查清单

**移除：**
- [ ] 验证语言/框架行为而不是业务逻辑的测试
- [ ] 类型系统已强制的冗余类型检查
- [ ] 对不可能状态的过度防御错误处理
- [ ] Console.log 语句
- [ ] 注释掉的代码
- [ ] 测试语言特性的测试（如测试 TypeScript 泛型工作）

**保留：**
- [ ] 所有业务逻辑测试
- [ ] 边界情况测试
- [ ] 错误路径测试（真实的错误路径，不是不可能的）
- [ ] 集成测试

**验证：**
- [ ] 运行测试套件确保没有破坏
- [ ] 运行 lint 确保代码风格一致
- [ ] 运行类型检查确保类型安全

### 模式B: 复杂度分层

| 复杂度 | 管道阶段 | 示例 |
|--------|---------|------|
| **trivial** | 实现→测试 | 拼写错误、样式调整 |
| **small** | 实现→测试→代码审查 | 简单功能、小bug修复 |
| **medium** | 研究→计划→实现→测试→PRD审查+代码审查→修复 | 中等功能、跨模块重构 |
| **large** | 研究→计划→实现→测试→PRD审查+代码审查→修复→最终审查 | 架构变更、新功能模块 |

#### 复杂度检测信号

| 信号 | 复杂度 |
|------|--------|
| 单文件修改 < 50 行 | trivial |
| 单文件修改 50-200 行 | small |
| 多文件修改 < 5 文件 | medium |
| 多文件修改 >= 5 文件 | large |
| 涉及架构变更 | large |
| 涉及 API 契约变更 | medium+ |
| 涉及性能关键路径 | large |

#### 分层管道示例

**Trivial（简单）：**
```bash
# 直接实现 + 测试
"Fix the typo in README.md"
"Run tests to ensure nothing broke"
"Commit"
```

**Small（小量）：**
```bash
# 实现 + 测试 + 代码审查
"Add unit tests for utils/calculateTotal()"
"Run tests"
"Code review: check for edge cases, error handling"
"Commit"
```

**Medium（中量）：**
```bash
# 研究 + 计划 + 实现 + 测试 + 审查
"Research: analyze current auth flow"
"Plan: design OAuth2 integration"
"Implement: add OAuth2 login"
"Test: run full test suite"
"PRD review: verify against spec"
"Code review: security, error handling"
"Fix review issues"
"Commit"
```

**Large（大量）：**
```bash
# 完整管道
"Research: analyze codebase architecture"
"Plan: design caching layer"
"Implement: add Redis caching"
"Test: run full test suite + load tests"
"PRD review: verify against spec"
"Code review: performance, security, edge cases"
"Fix review issues"
"Final review: overall quality gate"
"Commit"
```

### 循环模式组合

#### 组合1: 顺序管道 + De-Sloppify

最常见组合。每个实现步骤都有清理步骤：
```bash
for feature in "${features[@]}"; do
  "Implement $feature with TDD."
  "De-sloppify: remove test/code slop."
  "Verify: run build + tests."
  "Commit."
done
```

#### 组合2: 复杂度分层 + De-Sloppify

根据复杂度选择管道，每个实现步骤后都有清理：
```bash
if [ "$complexity" = "large" ]; then
  "Research."
  "Plan."
  "Implement."
  "De-sloppify."  # 清理步骤
  "Test."
  "PRD review."
  "Code review."
  "Fix."
  "Final review."
else
  "Implement."
  "De-sloppify."  # 清理步骤
  "Test."
  "Commit."
fi
```

#### 组合3: 迭代循环 + De-Sloppify

在迭代循环中，每次迭代都有清理：
```bash
for iteration in 1 2 3; do
  "Implement improvements."
  "De-sloppify: remove slop."
  "Verify: run tests."
  "Review: check quality."
done
```

### 反模式

| 反模式 | 正确做法 |
|--------|---------|
| **无退出条件的无限循环** | 设置最大迭代次数 + 完成条件 |
| **迭代间无上下文桥接** | 使用状态文件或 SHARED_TASK_NOTES.md 桥接 |
| **重试相同失败** | 捕获错误上下文并反馈给下次尝试 |
| **否定指令代替清理步骤** | 先彻底实现，再独立清理 |
| **所有 Agent 在一个上下文窗口** | 分离实现者和审查者上下文 |

### 模型路由（可选）

不同复杂度可以用不同模型：

| 复杂度 | 推荐模型 | 说明 |
|--------|---------|------|
| trivial | 快速模型 | 拼写错误、样式调整 |
| small | 中等模型 | 简单功能、小 bug |
| medium/large | 强模型 | 架构变更、复杂功能 |

在 OpenClaw 中，可以通过 spawn 子代理时指定 model 参数实现。

---

## Task Sizing Guidelines

| 大小 | 文件数 | 范围 | 示例 |
|------|--------|------|------|
| **XS** | 1 | 单个函数或配置变更 | 添加验证规则 |
| **S** | 1-2 | 一个组件或端点 | 添加一个 API 端点 |
| **M** | 3-5 | 一个功能切片 | 用户注册流程 |
| **L** | 5-8 | 多组件功能 | 带过滤和分页的搜索 |
| **XL** | 8+ | **太大——需要进一步拆分** | 无 |

如果任务是 L 或更大，应该拆分为更小的任务。代理在 S 到 M 任务上表现最佳。

---

## Red Flags

- 没有书面任务列表就开始实现
- 任务说"实现功能"但没有验收标准
- 计划中没有验证步骤
- 所有任务都是 XL 大小
- 任务之间没有检查点
- 没有考虑依赖顺序

---

## 文件结构

```
planning-toolkit/
├── SKILL.md                    # 本文档
├── templates/
│   ├── task_plan.md            # 阶段跟踪模板
│   ├── findings.md             # 研究存储模板
│   └── progress.md             # 会话日志模板
└── scripts/
    ├── init-planning.sh        # 初始化规划目录脚本
    ├── loop-controller.py      # 迭代循环控制器
    └── state-template.json     # 状态文件模板
```

---

## See Also

- `coding-framework` — 编程开发框架
- `incremental-implementation` — 增量实现执行纪律
- `context-engineering` — 上下文管理与打包策略

---

*Version 2.0.0 — 合并 spec-writing v1.1.0：新增 Part 0 需求规格（门控工作流/六领域模板/PRD结构/MoSCoW/HTML可视化）*
