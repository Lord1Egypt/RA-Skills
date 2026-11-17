---
name: iterate
slug: iterate-skill
displayName: Iterate
description: Fully automated multi-round code iteration with configurable N-dimension parallel review, onboarding/personalization, and a cross-assistant installer/update system with mandatory SHA256 checksum verification. v3.0 adds a dual-mode (the original iterate mode plus a defensive-programming mode via /iterate defensive) that performs normal incremental coding tasks with defensive discipline end-to-end.
version: 0.0.7
permissions:
  file_read: true
  file_write: true
  shell: true
  git: true
  network: "github.com only (release tarball + checksum verification)"
  sensitive_files:
    skip: [".env", ".env.*", "*.key", "secrets/", "*.pem", "*.p12", "*.crt", "*.cer", "credentials.json", ".aws/", ".ssh/"]
---

# /iterate `<goal>` `[rounds]` `[no-limit]`

# /iterate defensive `<goal>`（防御式编程模式 / Defensive-Programming Mode）

> **面向人类读者**：本文件是供 AI 助手消费的 Skill 指令。若您是开发者或浏览者，欢迎前往 GitHub 仓库 [jingzhao-l/iterate-skill](https://github.com/jingzhao-l/iterate-skill) 阅读 README，详细了解本 Skill 及其附属生态（iterate-harness、iterate-plugin、CLI 等）。
>
> **For human readers (English)**: This file is a Skill manifest consumed by AI assistants. If you are a developer or a human visitor, welcome to the GitHub repository [jingzhao-l/iterate-skill](https://github.com/jingzhao-l/iterate-skill) — read the README to learn more about this Skill and its ecosystem (iterate-harness, iterate-plugin, CLI, etc.).

---

## 简介 / Overview

> 中文：全自动多轮代码迭代。每轮从 N 个已启用维度并行审查整个项目（默认 9 个），原子问题直接修复，架构问题经用户批准后由子代理串行执行，验证通过后（合并与推送为 opt-in，默认关闭）循环直到零 findings 或达到轮数上限。
>
> English: Fully automated multi-round code iteration. Each round launches N parallel dimension reviewers across the project (default 9), fixes atomic issues directly, executes architectural issues after user approval via serial sub-agents, validates, and loops until zero findings or max rounds (merge/push are opt-in and disabled by default).

**v3.0 双模式 / v3.0 dual-mode**：本 Skill 现为**双模式**——

- **iterate 模式**（原 `/iterate`，默认，v2 全部能力完整保留）：审查 → 修复 → 验证 → 收敛闭环。
- **防御式编程模式**（新增 `/iterate defensive`）：面向**用户让 AI 做正常增量式编程任务**的场景（新增功能、修 bug、重构等），宿主 AI 从动手前到收尾**从头至尾贯彻防御式编程理念**（四步协议：pre-check → 最小步进编码 → 每步 post-check → invariant + iterate 收敛门禁），以 iterate 闭环收尾作为**交付门禁**（不收敛不交付）。

> Defensive-Programming Mode (v3.0, via `/iterate defensive`): for the scenario where the **user asks the AI to do a normal incremental coding task** (add a feature, fix a bug, refactor). The host AI performs that task end-to-end with defensive discipline — a four-step protocol: `pre-check` before touching anything → minimal-step editing (validate at the trust boundary) → `post-check` after every edit → `invariant` + the iterate convergence loop as a **delivery gate** (no convergence, no delivery).

---

## 何时使用 / When to Apply

**iterate 模式**适用于以下场景：

- 需要系统性提升代码质量、修复潜在 bug 或安全漏洞。
- 项目进入重构、迭代收尾或发布前的审查阶段。
- 需要多维度（正确性、安全、性能、架构等）并行审查。
- 希望将原子问题自动修复，将架构问题经审批后修复。

**防御式编程模式**（`/iterate defensive`）适用于**用户让 AI 做正常增量式编程任务**的场景：

- 用户给一个**具体的增量式编程任务**：新增功能、修复 bug、重构模块、接入 API、补测试等。
- 该任务需要**动手改代码**（不是纯审查），且用户希望 AI **从头至尾按防御式编程纪律**完成——动手前校验、最小步进、每步后校验、收尾门禁。
- 典型场景：`/iterate defensive implement user-settings page`、`/iterate defensive fix the null-pointer bug in parser.py`、`/iterate defensive refactor auth to use a middleware`。
- **判断要点**：任务是"让 AI 干活产出代码"而非"让 AI 审查已有代码"，就应进入防御式编程模式；任务若需多轮并行审查收敛，仍可用 iterate 模式，二者以**本次调用的 goal 形态**区分。

**纯审查模式 / review-only mode**：当调用参数含 `review-only` 或 `dry-run` 时，本 Skill 只做**只读健康检查**，绝不修改任何文件：
- 反复多轮并行审查，直到某一轮出现 0 个新 findings（收敛）。
- 生成审查报告（含每轮收敛统计、按严重级别/维度汇总、修复优先级建议）。
- **再审查这份报告本身**（meta-review：校验报告内部一致性——总数匹配、严重级别汇总、维度汇总、排序、收敛数学），给出带 `approved` / `needs_revision` 判定的**最终审查报告**。meta-review 同时跑硬证据门禁：逐条校验 finding 的 `file`/`line` 是否真实存在，子代理只允许锚定实际读过的真实代码，伪造路径/行号即以 `EVIDENCE_VIOLATION` 判 `needs_revision`。
- 适用于发布前体检、代码质量审计、不想让 AI 动代码的场景。

This Skill is appropriate when:

- You need a systematic code quality improvement, bug fix, or security hardening pass.
- The project is in refactoring, pre-release, or iteration wrap-up phase.
- You want parallel multi-dimension review (correctness, security, performance, architecture, etc.).
- You want atomic issues fixed automatically and architectural issues fixed after approval.

**Defensive-Programming Mode** (`/iterate defensive`) applies when the **user asks the AI to do a normal incremental coding task**:
you are asked to implement a feature, fix a bug, refactor a module, integrate an API, or add tests —
and you must do that task end-to-end with defensive discipline (pre-check → minimal-step editing →
post-check after every edit → invariant + iterate convergence as a delivery gate).

**review-only / dry-run mode** applies when the invocation includes `review-only` or `dry-run`:
it performs a read-only health check that never modifies files — repeated parallel review rounds until a
round finds 0 new findings (convergence), produces a review report, then meta-reviews that report
(validating internal consistency) and emits a final report with an `approved` / `needs_revision` verdict.
The meta-review also runs the hard code-evidence gate: every finding's `file`/`line` is validated against
real files on disk, so reviewers may only anchor to code they actually read — fabricated paths or invented
line numbers surface as `EVIDENCE_VIOLATION` and force `needs_revision`.
Use it for pre-release health checks, audits, or any case where you do not want the AI to touch code.

## 何时跳过 / When to Skip

**iterate 模式**不适用于以下场景：

- 仅需要单次、简单的代码编辑（不需要多轮审查）——**此类场景应改用防御式编程模式 `/iterate defensive`**（正是为"让 AI 做正常增量式编程任务"而设）。
- 没有可用的验证命令（`validation.commands` 未配置）——防御式模式下 `guard post-check` / `invariant` 会依赖验证命令，缺失时校验退化。**自 v3.0.1 起**：若项目*已 onboarded*（存在非空 `iterate.config.yaml`）但 `validation.commands` 为空，`guard pre-check` 将 **fail-closed**（退出码 1、`PASS`/`FAIL` 为 `FAIL`）——因为它承诺的 post-check 必然失败，不应给出"可以开工"的绿灯；宿主 AI 收到 `FAIL` 应先补配置 `validation.commands`。全新项目（尚无配置）则正常降级放行。
- 只需要 UI/UX 设计建议（请使用 UI/UX Pro Max 等专业设计 Skill）。

Do **not** use this Skill in **iterate mode** when:

- A single, simple edit is sufficient (no multi-round review needed) — **use `/iterate defensive` instead** (that is exactly the incremental-coding-task scenario it serves).
- No validation commands are configured in `validation.commands`. **Since v3.0.1**: for an *onboarded* project (a non-empty `iterate.config.yaml` exists) with empty `validation.commands`, `guard pre-check` **fails closed** (exit code 1) instead of handing out a misleading "clear to start" green light — configure `validation.commands` first. A brand-new project with no config yet still degrades gracefully (pass).
- You only need UI/UX design advice (use a dedicated design Skill like UI/UX Pro Max).

---

## 参数 / Parameters

调用格式 / Invocation:

- **iterate 模式**：`/iterate <goal> [rounds] [no-limit]`
- **防御式编程模式**：`/iterate defensive <goal>`（v3.0 新增；可用 `iterate.config.yaml` 的 `mode: defensive` 设为本次调用默认，仍可用显式 `defensive` 覆盖）

参数通过 [Agent Skills](https://agentskills.io/) 标准占位符注入：

| 占位符 / Placeholder | 含义 / Meaning | 默认值 / Default |
|---------------------|----------------|------------------|
| `$goal` / `$0` | 迭代目标 / Iteration goal | required |
| `$rounds` / `$1` | 最大轮数 / Max rounds | `7` |
| `$limit_mode` / `$2` | 若设为 `no-limit`，则最大轮数为 50（硬上限）/ Set to `no-limit` for hard cap 50 | — |
| `$mode` / `$3` | `review-only` / `dry-run` → **纯审查模式**（反复审查直到零 findings，绝不修改文件）；`defensive` → **防御式编程模式**（按四步协议从头至尾完成增量式编程任务，iterate 闭环收尾作为交付门禁）/ `review-only`/`dry-run` → pure-review mode (never touches files); `defensive` → defensive-programming mode (four-step protocol on an incremental coding task, iterate loop as delivery gate) | 默认迭代模式 |
| `$ARGUMENTS` | 用户输入的全部参数原样字符串 / Raw argument string | — |

示例 / Examples：
- `/iterate improve error handling`
- `/iterate improve error handling 10`
- `/iterate improve error handling no-limit`
- `/iterate review the codebase review-only`（纯审查模式：只审查不改代码，反复审查到零 findings，出审查报告，再审查报告给出最终审查报告）
- `/iterate full health check --review-only`（同上，纯审查别名）
- `/iterate defensive implement user-settings page`（防御式编程模式：让 AI 正常写代码实现功能，从头至尾防御式纪律 + 收尾门禁）
- `/iterate defensive fix the null-pointer bug in parser.py`
- `/iterate defensive: refactor auth to middleware`

---

## 防御式编程模式 / Defensive-Programming Mode

> **本节仅描述防御式编程模式（`/iterate defensive`）的行为。iterate 模式（`/iterate`）行为与 v2 完全一致，零回归。**
>
> **适用场景**：用户让 AI 做**正常增量式编程任务**（新增功能、修 bug、重构、接入 API、补测试）——动手改代码、产出真实可运行结果，而非纯审查。宿主 AI 从动手前到收尾**从头至尾贯彻防御式编程理念**，以 iterate 闭环收尾作为交付门禁。

### 防御式编程心智模型 / The Defensive Mindset

防御式编程是**编码时的心智模型**（软件工程经典定义），不是"审查-修复-收敛"流程；iterate 本身就是防御式编程的一种实现（审查环节的防御），本模式把整套心智模型**前移到编码过程本身**：

1. **最小化假设 / Minimize assumptions**：假设事情会出错，主动预测并容忍问题，而非乐观假设"应该没事"。
2. **信任边界验证 / Validate at trust boundaries**：数据从"不可信来源"进入代码的那一刻必须验证；内部状态可信任，**外部输入必须验证**。
3. **快速失败、响亮失败 / Fail fast, fail loud**：错误一发生立即停止、报错、回滚，绝不带病继续。
4. **前置/后置条件 + 断言 / Pre/post-conditions + assertions**：每个函数声明要求什么（前置）、保证什么（后置），用断言守卫假设。

### 四步防御式协议 / Four-Step Defensive Protocol

| 阶段 / Phase | 防御式原则 / Principle | 落地动作 / Action |
|---|---|---|
| **① 动手前 / Before** | 最小化假设 + 前置条件 | 声明"我假设什么成立"（目标范围、文件存在、git 干净、依赖就绪）；跑 `iterate guard pre-check <paths...>` 做**确定性前置校验**；FAIL 则先处理（恢复干净起点）再动手，绝不带病开工 |
| **② 动手时 / During** | 信任边界验证 + 最小步进 | 每次只做**最小步进修改**；写入前验证目标路径在允许范围、命令在 `validation.commands` 精确白名单内；对外部输入在进入代码的边界处加校验；保持修改原子性（可回滚） |
| **③ 动手后 / After** | fail-fast + 后置条件 | **每次改动后**跑 `iterate guard post-check [module...]`（精确执行配置的验证命令）；FAIL 则立即修复或回滚，记录假设是否被证伪；不通过不进入下一步 |
| **④ 收尾 / Delivery** | 不变量守护 + 收敛门禁 | `iterate invariant` 检查项目级不变量（`invariants.ensure` 文件断言 + `invariants.commands`）；随后跑 **9 维度审查 → 修复 → 验证 → 收敛**（即 v2 完整 iterate 闭环）作为**交付门禁**——**不收敛不交付** |

### 防御式 CLI 确定性校验 / Deterministic CLI Enforcement

防御式理念必须靠 CLI 确定性校验落地（prompt 指令不可靠）。宿主 AI 在防御式模式下按下表调用：

| 命令 / Command | 时机 / When | 输出 / Output | 契约 / Contract |
|---|---|---|---|
| `iterate guard pre-check [paths...]` | 动手前 | `PASS/FAIL` + 逐项结果 | 目标存在、git 干净、依赖 manifest 就绪、验证命令配置安全、每个验证命令对应的可执行工具在 PATH 上（shell 内建除外）；退出码 0 = 可以开工，1 = 禁止开工 |
| `iterate guard post-check [module...]` | 每次改动后 | `PASS/FAIL` + 逐项结果 | 精确执行 `validation.commands.<module>`（运行时唯一权威白名单）；退出码 0 = 本次改动安全，1 = 必须先修复或回滚 |
| `iterate invariant` | 收尾交付前 | `PASS/FAIL` + 违反项明细 | 校验 `invariants.ensure` 文件断言 + `invariants.commands`；`ensure` 只接受项目根目录内的相对路径（拒绝绝对路径与越出项目根的 `../` 逃逸）；无 `invariants` 段时退化为 `validation.commands`；退出码 0 = 不变量成立，1 = 存在违反项 |

### 交付门禁 / Delivery Gate

- **不收敛不交付**：防御式模式的收尾必须跑完整 iterate 闭环（9 维度审查 → 修复 → 验证 → 收敛），任一维度仍有未解决 findings 或 `iterate invariant` 不通过，**不得交付**，必须继续修复直到收敛。
- **假设记录**：动手前声明的假设，在收尾时逐条回放——被证伪的假设必须说明如何被验证/修复。
- **输出交付总结**：改动清单、验证证据（各步 `guard` / `invariant` 结果）、残留风险与豁免。若某项不变量被有意豁免，在交付总结中**列明违反项与豁免理由**（仅作为报告小节记录，不写入配置——配置里不存在豁免键，schema 拒绝未知字段）。

---

## 问题分类标准 / Issue Classification

### 原子问题（Atomic） / Atomic Issues

满足以下**全部**条件：

- 改动在**单个文件**内。
- 改动在**单个函数/方法**内（或最多 3 个相邻的同类方法）。
- 预计改动 ≤ **20 行**（可通过配置调整）。

原子问题**不进入用户审批流程**，由主模型直接修复。

An issue is atomic when **all** of the following are true:

- Changes are within a **single file**.
- Changes are within a **single function/method** (or ≤3 adjacent similar methods).
- Expected changes are ≤ **20 lines** (configurable).

Atomic issues are **fixed directly by the main model** without user approval.

### 架构问题（Architectural） / Architectural Issues

满足以下**任一**条件：

- 跨多个文件。
- 涉及 API / 协议 / 数据模型变更。
- 需要新增类 / 模块 / 文件。
- 预计改动 > **20 行**。

架构问题**必须经用户批准后**才能执行，由子代理串行完成。

An issue is architectural when **any** of the following is true:

- Cross-file changes.
- API / protocol / data model changes.
- New classes / modules / files needed.
- Expected changes are > **20 lines**.

Architectural issues **require user approval** and are executed by sub-agents serially.

**关键原则 / Key Principle**：原子问题和架构问题同样重要，都必须修复。区别仅在于是否需要用户批准以及由谁执行。

---

## 核心流程 / Core Workflow

> **本节描述 iterate 模式（`/iterate`）的完整闭环，与 v2 完全一致。** 防御式编程模式（`/iterate defensive`）的执行请见上文「防御式编程模式」一节：其收尾阶段（第 ④ 步）即复用本节完整 iterate 闭环作为交付门禁，其余各步（① 动手前 / ② 动手时 / ③ 动手后）在编码过程中注入防御式纪律。

```text
Step 0 — Onboarding Check
  └─ Locate project root → check ITERATE.md → drift detection → (onboard if needed)

Setup
  └─ Extract goal → load config → read project context (ITERATE.md → CLAUDE.md → …) → create isolated branch/worktree

Loop (round = 1 .. max_rounds)
  ├─ Phase 0: Dimension Planning (route goal → dimension_sets | ad-hoc redefine, bounded record)
  ├─ Phase 1: N-dimension parallel review (N = enabled dimensions count, default 9)
  ├─ Phase 2: Atomic fixes (direct)
  ├─ Phase 3: Architectural fixes (approval → serial sub-agents)
  ├─ Phase 4: Record round results
  └─ Phase 5: Validate → merge → push

Summary
```

---

## Step 0 — Onboarding 检查 / Onboarding Check

每次调用 `/iterate` 时，**首先**执行 onboarding 检查。Onboarding 是为当前项目生成定制化知识库（`ITERATE.md`）和项目级配置（`iterate.config.yaml` 中的 `onboarding` 段）的过程。

### 为什么需要 Onboarding

- **validation.commands 精准化**：默认配置中的验证命令只是示例，onboarding 根据项目实际技术栈生成正确的命令。
- **维度定制化**：无前端的项目不需要 `ui-ux` 维度，无 specs/ 的项目不需要 `spec-compliance`——onboarding 避免空转浪费算力。
- **项目知识沉淀**：`ITERATE.md` 记录项目概述、技术栈、模块地图、审查注意点，供后续每轮审查参考。

### 检查流程

1. **定位项目根目录 / Locate project root**
   - 以当前工作目录为起点向上查找；命中优先级：**包含 `ITERATE.md` 或 `iterate.config.yaml` 的目录 > 包含 `.git` 的目录**。
   - **Monorepo / 多子项目提示**：若同时存在多个候选根（如外层 git 根 + 内层某子项目也含 manifest），以**最近的含 `ITERATE.md` / `iterate.config.yaml` 的目录**为准；若无明确唯一候选，用 `AskUserQuestion` 让用户确认审查范围，避免误审到无关子项目。
   - 若向上查找到文件系统根仍未找到，则使用当前工作目录作为项目根目录，并提示用户确认。

2. **检查 onboarding 状态 / Check onboarding status**
   - 检查项目根目录下是否存在 `ITERATE.md`。
   - **存在** → 进入漂移检测（下一步）。
   - **不存在** → **先向用户明确说明**"这是首次使用，将先进行项目初始化（Onboarding）"，再暂停迭代进入 **AI Onboarding 流程**（见下文）。不要让用户误以为 skill 失效或卡住；完成后继续 Step 1。
