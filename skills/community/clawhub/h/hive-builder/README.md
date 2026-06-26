# Hive for OpenClaw

中文 | [English](#english)

## 中文

### 这是什么

Hive 是一套为 OpenClaw 设计的分层多角色编排技能集合。

它的目标不是把所有任务都强行拆成多智能体流程，而是让你在 **确实需要角色分工** 的时候，能够用一种可控、可审计、可逐步激活的方式组织工作。

Hive 的核心定位是：

- 一个 **母 skill**：`hive-builder`
- 一个 **运行时控制层**：`hive-ceo`
- 两个 **治理层**：`hive-hrm`、`hive-ops`
- 多个 **业务 specialist 层**：`hive-collector`、`hive-writer`、`hive-qa` 等

Hive 适合：
- 想在 OpenClaw 里搭一个“一人公司 / 小型虚拟组织”
- 希望主会话像 CEO 一样决策，必要时调度 specialist
- 希望保留边界，不想让技能安装后自动接管整个 workspace
- 希望有明确的 scaffold / activation / validation 区分

Hive 不适合：
- 所有事情都想自动多智能体化
- 期待安装后就无脑自治
- 不愿意区分规划、验证、激活三种状态

---

### 当前结构

本发布包包含：

- `hive-builder`
- `hive-ceo`
- `hive-hrm`
- `hive-ops`
- `hive-collector`
- `hive-writer`
- `hive-qa`

推荐理解顺序：

1. **`hive-builder`**
   - Hive 母 skill
   - 负责架构、脚手架、激活边界
   - 是整个 Hive 的公开入口

2. **`hive-ceo`**
   - 运行时控制层
   - 决定任务要不要进 Hive
   - 决定走哪条链，选择哪种 runtime
   - 负责最终对用户输出

3. **`hive-hrm` / `hive-ops`**
   - HRM：扩角色、设计 workflow chain
   - OPS：环境检查、版本对齐、能力校准

4. **specialist skills**
   - `hive-collector`：收集事实与原始材料
   - `hive-writer`：把输入整理为 draft
   - `hive-qa`：在交给 CEO 前做 review

---

### 核心原则

#### 1. 安装 ≠ 激活

安装 Hive skill 只是把能力放进 OpenClaw。

这 **不意味着**：
- 你的主会话自动变成 Hive CEO
- 所有任务以后都自动走多角色链
- workspace 文件会被自动重写

#### 2. Scaffold ≠ Broad Activation

Hive 支持：
- 先设计
- 再脚手架
- 再做 contained validation
- 最后再决定是否扩大 live routing

默认应该是 **谨慎激活**，不是一上来全面接管。

#### 3. 不是每个任务都要进 Hive

如果主会话直接完成更简单、更快、更好，就不该为了“像组织”而强行进 Hive。

#### 4. OpenClaw-first

Hive 不是要自己发明一整套平行 runtime。

在现代 OpenClaw 版本中（已在 2026.4.9 上校准验证），Hive 应优先对齐原生能力：
- `sessions_spawn`
- ACP runtime
- structured plan updates
- execution item events

如果平台已经有原生能力，优先使用原生能力，而不是重复造轮子。

---

### 推荐运行时策略

当前推荐顺序：

1. **主会话直接处理**
   - 当角色分工价值不大时

2. **contained/manual validation**
   - 当你在验证一条新链路时

3. **`sessions_spawn`**
   - 当 specialist 链路已经被证明可复用

4. **ACP runtime**
   - 当某个 specialist 明显更适合 coding / harness 型环境

5. **更持久的流程编排**
   - 只有真的需要 durable orchestration 时再考虑

---

### 4.9 校准说明

本包已经按现代 OpenClaw 运行时能力做过一轮架构校准，并在 OpenClaw 2026.4.9 上完成验证。

主要对齐点：

- 明确 runtime choice：
  - main session
  - contained validation
  - `sessions_spawn`
  - ACP runtime

- 明确 progress mode：
  - silent synthesis only
  - structured plan updates
  - execution item events

- 明确 ClawHub 发布边界：
  - `hive-builder` 是母 skill
  - modular `hive-*` skills 是可拆分的运行时层
  - 安装不等于激活
  - 激活不等于接管 workspace

---

### 建议使用方式

#### 方式 A：先只用 `hive-builder`

适合：
- 你还在规划 Hive
- 你想先看它如何设计脚手架
- 你不想立即激活 runtime

#### 方式 B：`hive-builder` + `hive-ceo`

适合：
- 你已经有 Hive 基础目录
- 想让主会话开始像 CEO 一样做运行时判断

#### 方式 C：完整分层使用

适合：
- 你已经接受 Hive 是一个长期组织结构
- 想进一步引入 HRM / OPS / specialist 链路

---

### 发布边界与注意事项

在当前版本里，这套 Hive skill：

**会做的事：**
- 帮你规划 Hive 架构
- 帮你决定任务是否进入 Hive
- 帮你设计 role chain、runtime choice、approval boundary
- 帮你把 specialist 分工讲清楚

**不会自动做的事：**
- 自动全局接管你的 OpenClaw
- 自动无审批地扩组织
- 自动修改关键 workspace 文件
- 自动把所有任务都切成多角色流程

---

### 推荐下一步

如果你刚安装这套 Hive skill，建议按这个顺序来：

1. 先读 `hive-builder`
2. 用 `hive-builder` 设计或检查你的 Hive scaffold
3. 再让 `hive-ceo` 管一个小而明确的任务
4. 再逐步引入 `hive-hrm` / `hive-ops`
5. 最后才扩大 specialist 使用范围

---

## English

### What this is

Hive is a layered multi-role orchestration skill set for OpenClaw.

Its goal is **not** to force every task into a multi-agent workflow.
Its goal is to let you introduce role separation in a controlled, auditable, gradually activatable way **when role separation actually helps**.

Hive is organized as:

- one **mother skill**: `hive-builder`
- one **runtime control layer**: `hive-ceo`
- two **governance layers**: `hive-hrm`, `hive-ops`
- several **business specialist layers**: `hive-collector`, `hive-writer`, `hive-qa`, and others

Hive is a good fit when you want:
- a one-person-company / virtual org structure inside OpenClaw
- a CEO-like main session that decides when specialists are needed
- explicit boundaries instead of automatic workspace takeover
- a clear distinction between scaffold, validation, and activation

Hive is **not** a good fit if you want:
- every task to become multi-agent by default
- immediate autonomy just because a skill was installed
- no distinction between planning, validation, and activation

---

### Package contents

This publish bundle includes:

- `hive-builder`
- `hive-ceo`
- `hive-hrm`
- `hive-ops`
- `hive-collector`
- `hive-writer`
- `hive-qa`

Recommended reading order:

1. **`hive-builder`**
   - the mother skill
   - architecture, scaffold, activation boundaries
   - the public entry point for Hive

2. **`hive-ceo`**
   - runtime control layer
   - decides whether Hive should handle a task
   - selects chain and runtime
   - owns final user-facing synthesis

3. **`hive-hrm` / `hive-ops`**
   - HRM: role expansion and workflow-chain design
   - OPS: environment review, release alignment, capability calibration

4. **specialist skills**
   - `hive-collector`: gathers facts and bounded raw input
   - `hive-writer`: drafts outputs from upstream inputs
   - `hive-qa`: reviews drafts before CEO handoff

---

### Core principles

#### 1. Installation is not activation

Installing Hive skills only makes the capability available.
It does **not** mean:
- your main session automatically becomes Hive CEO
- all tasks now route into multi-role chains
- your workspace files will be rewritten automatically

#### 2. Scaffold is not broad activation

Hive is designed to support:
- design first
- scaffold second
- contained validation next
- broader live routing only after explicit choice

Default behavior should be **cautious activation**, not immediate takeover.

#### 3. Not every task should enter Hive

If the main session can do the task more simply and more effectively, Hive should stay out of the way.

#### 4. OpenClaw-first

Hive should not invent a parallel runtime when OpenClaw already provides native primitives.

In modern OpenClaw releases, validated on 2026.4.9, Hive should align with:
- `sessions_spawn`
- ACP runtime
- structured plan updates
- execution item events

When the platform already supports something natively, Hive should usually reuse it instead of duplicating it.

---

### Recommended runtime policy

Recommended order:

1. **main-session direct handling**
   - when role separation adds little value

2. **contained/manual validation**
   - when proving a new chain shape

3. **`sessions_spawn`**
   - when a specialist chain has become reusable

4. **ACP runtime**
   - when a specialist is genuinely coding / harness oriented

5. **more durable orchestration**
   - only when a real product need exists

---

### OpenClaw 4.9 calibration

This bundle has been calibrated against modern OpenClaw runtime behavior and validated on OpenClaw 2026.4.9.

Main alignment points:

- explicit runtime choice:
  - main session
  - contained validation
  - `sessions_spawn`
  - ACP runtime

- explicit progress mode:
  - silent synthesis only
  - structured plan updates
  - execution item events

- explicit ClawHub publish boundary:
  - `hive-builder` remains the mother skill
  - modular `hive-*` skills remain decomposed runtime layers
  - installation does not imply activation
  - activation does not imply workspace takeover

---

### Recommended usage modes

#### Mode A: Start with `hive-builder` only

Best when:
- you are still planning Hive
- you want scaffold/design guidance first
- you do not want runtime activation yet

#### Mode B: `hive-builder` + `hive-ceo`

Best when:
- you already have a Hive subtree
- you want the main session to start behaving like a runtime CEO

#### Mode C: Full layered usage

Best when:
- you accept Hive as a longer-term operating structure
- you want HRM / OPS / specialist chains to matter in practice

---

### Publish boundary and safety notes

In its current form, this Hive bundle:

**Will do:**
- help design Hive architecture
- help decide whether a task should enter Hive
- help define role chains, runtime choices, and approval boundaries
- help keep specialist responsibilities clear

**Will not automatically do:**
- take over your OpenClaw setup globally
- expand the org without approval
- rewrite core workspace files automatically
- turn every task into a multi-role orchestration flow

---

### Recommended next steps

If you just installed this Hive bundle, a good order is:

1. read `hive-builder`
2. use it to design or inspect your Hive scaffold
3. let `hive-ceo` manage one small, explicit task
4. then gradually introduce `hive-hrm` / `hive-ops`
5. only later widen specialist usage
