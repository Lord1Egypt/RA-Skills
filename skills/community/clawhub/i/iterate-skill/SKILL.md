---
name: iterate
slug: iterate-skill
displayName: Iterate
description: Fully automated multi-round code iteration with configurable N-dimension parallel review, onboarding/personalization, and a cross-assistant installer/update system with mandatory SHA256 checksum verification. v3.0 adds a dual-mode (the original iterate mode plus a defensive-programming mode via /iterate defensive) that performs normal incremental coding tasks with defensive discipline end-to-end.
version: 3.15.0
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

3. **漂移检测 / Drift detection**（仅在 `onboarding.drift_check` 为 `true` 时执行）
   - 读取 `iterate.config.yaml` 中的 `onboarding.fingerprints`（manifest 文件的 SHA-256 哈希）。
   - 重新计算当前 manifest 文件的哈希并比对；`onboarding.drift_ignore` 中列出的 manifest（如锁文件）会被跳过，不计入漂移。
   - **无漂移** → 静默通过，进入 Step 1。
   - **有漂移**（manifest 新增/删除/内容变更）→ **非阻塞**警告，使用 `AskUserQuestion` 询问用户：
     - **继续（continue）**：本轮照旧使用现有 ITERATE.md。
     - **增量刷新（refresh）**：AI 重新扫描项目，更新 ITERATE.md 的 AI 维护区（用户手写区保留），更新指纹。
     - **完整重新 onboarding（reonboard）**：备份旧文件后走完整 onboarding 流程。

> 漂移检测是**非阻塞**的——即使用户选择"继续"，迭代也会正常进行，只是使用可能过时的知识库。

### AI Onboarding 流程 / AI Onboarding Flow

当 `ITERATE.md` 不存在时，AI 执行以下流程（类似 Claude Code 首次生成 `CLAUDE.md`）：

1. **告知并确认 / Inform and confirm**
   - 告知用户将扫描代码库生成 `ITERATE.md` 和配置，并说明这是首次使用所必需的初始化步骤。
   - 同时提示 CLI 备选：用户也可以运行 `iterate onboard` 在命令行中完成。
   - 参考 `templates/onboarding-playbook.md` 中的扫描清单和映射表（**仅供参考，需按项目实况调整**）。

2. **扫描 / Scan**（并行只读）
   - 读取 manifest 文件（`package.json` / `pyproject.toml` / `Package.swift` / `go.mod` / `Cargo.toml` 等）。
   - 读取 2-3 层目录树，识别模块结构。
   - 检查 `specs/`、`tests/`、CI 配置的存在性。
   - 读取已有 `README.md` / `CLAUDE.md` 提取项目描述。
   - **绝不读取** `.env`、`.env.*`、`*.{key,pem,p12,crt,cer}`、`credentials.json`、`.aws/`、`.ssh/` 等敏感文件。

3. **草拟 / Draft**
   - 基于扫描结果 + playbook 映射表草拟：
     - `ITERATE.md`：项目概述、技术栈、模块地图、推荐维度、iterate 注意点。
     - `iterate.config.yaml`：启用的 dimensions、`validation.commands`、`validation.command_whitelist`、指纹数据。
   - ITERATE.md 分为 **AI 维护区**（`<!-- ITERATE:AI-MAINTAINED:START -->` ~ `END`）和 **用户维护区**（`<!-- ITERATE:USER-OWNED:START -->` ~ `END`）。刷新时只更新 AI 维护区。

4. **用户确认 / User confirmation**
   - 展示摘要：识别的技术栈、拟启用维度及理由、**拟写入的 validation.commands 逐条列出**。
   - 用户可选：全部接受 / 修改 / 重扫。
   - **validation.commands 涉及后续自动执行，必须经用户显式确认。**

5. **写入产物 / Write outputs**
   - 写入 `ITERATE.md` 和 `iterate.config.yaml`，其中 `onboarding` 段必须包含 `channel: "ai"`、`completed_at`（ISO 8601 时间戳）与 `fingerprints`，与 CLI 通道产出保持一致（否则 `iterate status` 会显示 `Channel: unknown`）。
   - 继续正常迭代流程（Step 1）。

### CLI Onboarding（命令行通道）

用户也可以在终端中运行 `iterate onboard` 完成相同流程：

```bash
iterate onboard      # 交互式向导（多路引导：首次/非首次自动分支）
iterate init --yes   # 非交互式初始化：按扫描结果写入 ITERATE.md + config，供 CI/脚本/其它 skill 调用（--dry-run 预览；已初始化则不改动；--json）
iterate personalize  # 个性化配置（项目中途追加约束，9 步向导）
iterate personalize --clear [--yes]  # 清空所有个性化配置（结构化规则 + ITERATE.md 相关段落）
iterate show         # 只读查看合并后的配置与个性化详情（支持 --json）
iterate refresh      # 增量刷新（保留用户手写区；支持 --json / --dry-run --json 结构化报告）
iterate refresh --diff  # 打印刷新将应用的确切 unified diff（ITERATE.md + 配置重写；恒不写文件、隐含 dry-run；--json 时 diff 在 md_diff/config_diff 字段；无变化报 "no changes needed"）
iterate template     # 列出 skill 自带的模板（ITERATE.md 骨架 / onboarding playbook / 决策日志结构；只读，可在任意目录使用；`show NAME` 打印一个模板原文；别名 iterate/playbook/decisions；--json）
iterate reonboard    # 完整重新 onboarding（备份旧文件）
iterate doctor       # 项目健康诊断（onboarding/config/维度/漂移等全项检查；--strict 将 warning 一并判失败；--fix 安全修复；--check NAME 只跑指定检查（可重复/逗号分隔，`--list-checks` 列出全部检查名）；--json / --json-out 结构化输出）
iterate next         # 引导式「下一步」：按项目状态给出有序命令计划（未初始化→init/onboard；配置损坏→doctor --fix；manifest 漂移→refresh --diff→refresh；体检失败→doctor --fix；仅有 warning→doctor；健康→/iterate "<goal>" + 可选 personalize），并提示非 git 等环境缺口；只读、建议式（恒 exit 0）；--json 输出稳定键 state/blocking/drift/next/steps/notes
iterate status       # 查看 onboarding 状态和漂移检测（--json 含 onboarded、config_exists/config_ok、drift_detected 与明细列表）
iterate scan         # 只读导出项目扫描结果（识别到的 manifest/语言/包管理器/顶层目录/五个特性开关含 has_api + 建议维度/维度集/校验命令/命令白名单；不写文件，恒退出 0；--json）
iterate scan --json  # 同上，结构化输出，供脚本/CI 消费
iterate report       # 聚合 status/scan/doctor 为单份 Markdown 健康报告（可直接贴 PR / 存 CI artifact；--out PATH 落盘（已存在需 --force）；--strict 警告也判失败；--json 输出结构化报告）
iterate completion bash|zsh|fish  # 输出该 shell 的补全脚本（补全命令、参数、固定取值与路径；从同一 parser 生成，永不与 --help 漂移）
iterate completion bash|zsh|fish --install [--dir DIR] [--force]  # 直接装到该 shell 的常规用户补全目录（bash/fish 自动加载；zsh 写入 ~/.zfunc 或 ~/.oh-my-zsh/completions 并打印 fpath 提示；--json 输出安装结果）
iterate completion bash|zsh|fish --uninstall [--dir DIR]  # 只删掉安装时写入的那一个文件（幂等：没装过也退出 0 且 removed:false；--json 输出 {shell,path,removed,reload_hint}；与 --install 互斥）
iterate export       # 把 iterate.config.yaml + ITERATE.md 导出为单个可移植 JSON bundle（只写 bundle，不改项目；--out / --json / --force）
iterate import FILE  # 校验 bundle（含 schema）→ 时间戳备份 → 写回配置与 ITERATE.md（--dry-run / --yes / --reset-fingerprints / --json；FILE 为 - 时读 stdin）
iterate guard pre-check [targets...]   # 编辑前静态校验（目标存在/工作区干净/manifest 就绪；只读，从不执行命令；--json）
iterate guard post-check [targets...]  # 编辑后执行 validation.commands 并核对结果（--dry-run 只预览命令不执行；--json）
iterate invariant      # 项目级不变量校验（--dry-run 预览；--json）
iterate fingerprint verify  # 校验 manifest 指纹漂移（--json，退出码 0=无漂移 / 1=有漂移）
iterate fingerprint list    # 只读列出上次记录的指纹基线（path + sha256，不重扫；--json）
iterate backup list         # 只读列出项目根下所有时间戳备份（config set/unset、doctor --fix、refresh、personalize、onboard、import、reonboard 写入的 *.configset-* / *.doctorfix-* / *.refresh-* / *.bak-* 等），最新在前；退出码恒 0（空结果也是信息性）；--json
iterate backup restore FILE # 把某一备份恢复到其原始文件名（先对当前文件再备份为 *.restore-*，使恢复本身可逆；拒绝非 iterate 备份、项目目录外路径与目录目标；--dry-run / --yes / --json）
iterate backup prune        # 按保留策略删除旧备份（--keep N 每个原始文件保留最新 N 份；--older-than AGE 如 30d/7d/24h/90m 删除更旧；两者可并用取并集）；只删可识别的 iterate 备份、绝不触碰被保护的原文件；--dry-run 预览 / --json
iterate config       # 非交互式查看全部可设配置值（支持 --json）
iterate config get <key>   # 读取单个配置项的解析值（支持 --json，输出 {"key": value}）
iterate config set <key> <value>  # 校验并写回单个配置项（自动备份；--json 输出确认对象）
iterate config unset <key> # 删除该配置项并逐级剪掉空祖先节点（自动备份；key 不存在时退出码 1；--json）
iterate config schema      # 输出 iterate.config.yaml 的规范 JSON Schema（--out PATH 写文件、--force 覆盖、--compact 单行；供 yaml-language-server / CI / 工具链与 CLI 强制同一套配置契约）
iterate update       # 自更新：SHA-256 校验后刷新助手技能目录 + 重装 CLI（--check 只对比版本；--yes 跳过确认；--assistants 限定刷新范围，未知助手名报错而非静默跳过）
iterate help         # 打印总览帮助（等价 `iterate --help`）
iterate help doctor  # 打印单个命令的详细帮助
```

CLI 通道会自动扫描代码库并让你确认/调整技术栈与配置，适合希望手动控制 onboarding 过程的用户；AI 通道则完全由 AI 自动扫描生成。两者产出相同格式的 `ITERATE.md` 和 `iterate.config.yaml`。

**命令发现与容错 / Discoverability**：不确定下一步时先跑 `iterate next`——它按项目状态给出「现在跑哪条、为什么、之后跑什么」的有序计划（`--json` 可被脚本/其它 skill 消费），新手无需先读文档即可从空目录走到 `/iterate`；`iterate help [command]` 打印总览或单命令帮助（无需记住 `--help` 的位置）；命令拼错时会给出最近的可用命令（如 `iterate statu` → `did you mean 'status'?`），子命令动作同样适用（如 `iterate fingerprint verfy` → `did you mean 'verify'?`）。所有用法错误退出码为 2；带 `--json` 时 stdout 仍是恰好一个 JSON 文档（其中 `did_you_mean` 给出同样的建议）。`iterate completion bash|zsh|fish` 输出可直接安装的补全脚本（命令、参数、固定取值、路径参数），补全内容由 `--help` 同一个 parser 生成，新增/改名命令不会漏补；加 `--install` 可一步写入常规用户补全目录（`--dir` 自定义目录、`--force` 覆盖旧文件、`--json` 输出单个结果文档），不再需要自己记路径和重定向；加 `--uninstall` 只删除安装时写入的那一个文件（幂等、可脚本化、绝不触碰任意路径）。

**多路引导 / Multi-Path Flow**：
- **首次 onboarding**（无 ITERATE.md）：确认手动配置 → 基础 onboarding → 询问是否需要个性化配置。
- **非首次 onboarding**（已有 ITERATE.md）：询问是否更新基础配置（不建议手动改）→ 询问是否进行个性化配置。

`iterate config set <key> <value>` 的 `<key>`（扁平键，与 `iterate show` 输出的键一致）与点号路径别名（如 `git.use_worktree`、`reviewer.coverage_validation`）均可使用。`iterate config unset <key>` 反向操作：删除该键，若其父节点因此变空（如 `personalization` 下所有子项都被删）则连父节点一并剪掉，恢复到 schema 的默认语义；每次写入前自动备份为同目录下的 `iterate.config.yaml.configunset-<UTC 时间戳>-<随机后缀>`。若该键不存在（或父节缺失/不是 mapping），`unset` 以退出码 1 结束并提示 `nothing to unset`，不会静默成功。若该键带注释（`# ...`），删除会一并移除注释并在 stderr 给出 warning，避免留下悬空注释。

`iterate config schema` 把 `iterate.config.yaml` 的规范 JSON Schema 以纯 JSON 输出到 stdout（该命令恒不被 ASCII banner 污染，且不需要存在 `iterate.config.yaml`——它描述的是 CLI 的配置契约）。`--out PATH` 写入文件（默认拒绝覆盖已存在、`--force` 覆盖，确认信息走 stderr 保持 stdout 纯净），`--compact` 输出单行 JSON。这样编辑器（yaml-language-server 的 `yaml.schemas`）、CI 校验器与其它工具就能对 `iterate.config.yaml` 自动补全/校验，并与 `doctor`/`scripts/validate.py` 强制的是同一套规则。

### 退出码约定 / Exit-Code Contract

所有子命令遵循同一套退出码，便于脚本与 CI 门禁：

| 退出码 | 含义 | 典型来源 |
|---|---|---|
| `0` | 成功 / 无问题 | `status` 已 onboard 且无漂移；`guard pre-check` 可开工；`fingerprint list` 已读出基线（即使为空） |
| `1` | **业务失败**（命令按预期跑完，结论是"有问题"） | `guard`/`invariant` 返回 `FAIL`；`fingerprint verify` 检出漂移；`doctor --strict` 有 warning；`config set/unset` 的键/值非法；JSON 模式下配置无法解析 |
| `2` | **用法错误**（argparse） | 未知子命令、未知动作（`fingerprint bogus`）、缺必填参数、`config` 的非法键名 |
| `127` | 依赖缺失 | `iterate` CLI 缺少 PyYAML/rich 等运行依赖；`tools/gpg-signing.sh` 找不到 `gh`/`gpg` |

判读要点：**`2` 不要当作"有问题"去重试**——那是命令敲错了，重试只会得到同样的 `2`；**`1` 才是"结论为否"**，应当据此推进修复或回滚。**用户取消**（`onboard`/`reonboard`/`update` 交互确认时回答否）同样返回 `1`：取消意味着"未执行"，脚本不应把它读成成功。`--json` 模式下 `1` 依然会输出结构化对象（含 `reason`/`errors` 字段），因此脚本可先解析 JSON 再看 `$?`，无需靠退出码区分错误类别。**`stdout` 只放数据**：所有 warning/error 都写 `stderr`，因此 `--json` 的 stdout 恰好是一个 JSON 文档，可直接管到 `jq`。

**个性化配置 / Personalization**：捕获 AI 扫描不到的项目专属约束（禁区、风险区、已知意图、维度定制等 9 类）。运行 `iterate personalize` 可在项目中途随时追加，无需重做 onboarding。`iterate personalize --clear` 可一次清空所有个性化（结构化规则 + `ITERATE.md` 用户区中的相关段落，需确认或加 `--yes` 跳过）。`iterate show` 可只读查看合并后的配置与个性化详情（`--json` 输出结构化数据供脚本/CI 使用）。详见 README。

安装 CLI：`npx iterate-skill-installer` 会自动安装 `iterate` CLI；也可手动 `pip install .` 或 `pipx install .`（从本仓库根目录）。

**发布签名（强制）/ Release Signature (mandatory)**：每个 release 都附带
`iterate-skill.tar.gz.asc`（GPG 分离签名），安装器与 `iterate update` 会**同时**
校验 SHA256（完整性）与签名（真实性，对照内嵌公钥指纹
`0929EA31DF4F7429F63FC53189D88B1D043A1298`）。签名为必需：缺少签名、缺少 `gpg`、
签名无法取回或签名不匹配都会**中止**安装/更新——因为 `SHA256SUMS.txt` 与 tarball
出自同一个 release，单独用它无法抵御"发布渠道被篡改"。唯一例外是显式设置
环境变量 `ITERATE_ALLOW_UNSIGNED=1`（用于确实无法运行 gpg 的机器；*坏签名永不放行*）。
发布侧同样强制：`.github/workflows/release.yml` 未配置签名密钥或签名校验失败时
直接失败，不会发布未签名资产。

---

## Step 1 — 设定目标与隔离 / Setup

1. **提取目标 / Extract goal**
   - 从 `$0` / `$goal` 读取迭代目标；若缺失则反问用户。
   - Read iteration goal from `$0` / `$goal`; ask if missing.

2. **确定轮数 / Determine max rounds**
   - `maxRounds = $1` / `$rounds`，默认 `7`。
   - 若 `$2` / `$limit_mode` 为 `no-limit`，则 `maxRounds = 50`（硬上限）。
   - 解析失败时默认 `7` 并提示用户。

3. **确定项目根目录 / Locate project root**
   - 以当前工作目录为起点向上查找；命中优先级：**含 `ITERATE.md` 或 `iterate.config.yaml` 的目录 > 含 `.git` 的目录**。
   - **Monorepo / 多子项目提示**：以**最近的含 `ITERATE.md` / `iterate.config.yaml` 的目录**为审查范围；无唯一候选时用 `AskUserQuestion` 让用户确认，避免误审无关子项目。
   - 若向上查找到文件系统根仍未找到，则使用当前工作目录作为项目根目录，并提示用户确认。
   - 该目录即为项目根目录，后续所有文件读取和命令执行均以此为准。

4. **读取配置 / Load configuration**
   - **Master + Overrides 模式**：先加载技能安装目录下的 `config/iterate.config.yaml`（Master），再读取项目根目录的 `iterate.config.yaml`（Overrides）递归覆盖同名字段。
   - 合并规则为**深度合并（deep merge）**：对象字段递归合并键值；Overrides 中的列表字段会**完全替换** Master 中的同名列表（如 `dimensions`、`command_whitelist`）。
   - 若项目根目录不存在 Overrides，则完全使用 Master。
   - 将配置合并到运行参数；若合并后配置无法通过 schema 校验，立即报告错误并中止迭代。

5. **读取个性化配置 / Load personalization**
   - 读取合并后配置中的 `personalization` 段（由 `iterate onboard` 或 `iterate personalize` 写入）。
   - 将以下字段加载到运行参数，后续 Phase 必须严格遵守：
     - `personalization.protected_paths`：glob 模式列表，**禁止修改匹配的文件**（Phase 2/3 修复时必须跳过）。
     - `personalization.risk_areas`：`[{path, reason}]`，修改这些路径前必须通过 `AskUserQuestion` 获得用户明确批准。
     - `personalization.known_intentional`：`[{file, line, dimension, reason}]`，Phase 1 汇总后必须过滤掉匹配的 findings（line=0 表示整个文件）。
     - `personalization.dimension_focus`：`[{dimension, focus}]`，Phase 1 启动 reviewer 时将对应 focus 追加到维度 prompt。
     - `personalization.fix_priority_order`：维度优先级列表（从高到低），Phase 2 排序时按此顺序优先修复。
     - `personalization.forbidden_fixes`：字符串列表，Phase 2/3 修复时**禁止使用**这些方式（如 `# noqa`、`try-catch 吞错`）。
   - 若 `personalization` 段不存在或为空，跳过本步，不影响正常流程。

5b. **读取命名维度集 / Load dimension_sets**
   - 读取合并后配置中的 `dimension_sets`（由 onboarding 预置或用户手动命名，结构为 `{name: {dimensions: [...], focus?: {...}}}`）。
   - 将其整理为 `namedScopeSets` 供 Phase 0 范围路由使用；缺失 `<scope>` 时以全局 `dimensions` 为兜底。
   - `dimension_sets` 为空或不存在时不阻止流程，Phase 0 退化为纯 on-the-fly 逻辑。

6. **读取项目上下文 / Read project context**
   - 按优先级查找项目根目录的上下文文件：`ITERATE.md` → `CLAUDE.md` → `PROJECT.md` → `README.md`。
   - 提取项目名、架构、技术栈、代码规范、审查注意点；若都不存在，使用简要描述。
   - 构造 `projectContext` 字符串供后续使用。
   - 绝不读取 `.env`、`.env.*`、`*.{key,pem,p12,crt,cer}`、`credentials.json`、`.aws/`、`.ssh/` 等敏感文件。

7. **创建隔离环境 / Create isolated environment**
   - 检查 `git status` 与是否存在未解决冲突。
   - **优先 worktree 隔离**：若工作区存在未提交改动/未跟踪文件，**优先用 `git worktree add` 创建隔离工作树**进行迭代，**不要求也不强制**用户 commit/stash，也不改动当前脏工作区；迭代结束返回主工作区。
   - 仅当无法创建 worktree（如磁盘/路径受限）且工作区不干净时，才询问用户是否 commit/stash；用户拒绝/取消则**说明原因并建议改用 worktree 方式，而非直接中止**。
   - 存在未解决冲突时提示用户先解决，但不强行中断；可在干净的 worktree 中继续。
   - 记录当前分支名，作为迭代结束后的返回目标。
   - 创建迭代分支：`iterate/<goal-slug>-<timestamp>`（或对应 worktree 分支）。
   - 若分支/worktree 创建失败（如名称冲突），尝试追加递增序号后重试，最多 3 次；仍失败则中止并告知用户。

8. **初始化决策日志 / Initialize decision log**
   - 在隔离环境根目录创建 `.iterate_decisions.md`，写入文件头。
   - Initialize `deferredArchitectural = []` for cross-round carry-over.

---

## Step 2 — 迭代循环 / Iteration Loop

```
round = 1
while round <= maxRounds:
```

### 纯审查模式 / review-only (dry-run) loop

当调用参数含 `review-only` 或 `dry-run` 时，**跳过 Step 1 中的 git 隔离、跳过所有修复与验证**，只执行只读审查循环并产出最终审查报告。此模式**绝不修改任何文件、绝不创建分支/worktree、绝不调用 fixer**：

```
phase plan        → 获取审查计划（维度、reviewer prompt、findings schema、round cap）
knownAng = []     → 跨轮累计已发现 findings（供 reviewer 只找新问题）
rounds   = []     → 原始每轮 findings
for r in 1..cap:
    # 每个维度一个并行 reviewer，只报 NEW 问题
    raw = parallel(每个维度 → review 该维度, 已知 = knownAng)
    rounds.push({ round: r, findings: raw })
    knownAng.push(...raw)
    # 确定性收敛判定：aggregate 后本轮新 findings 数
    conv = aggregate(rounds)   # 汇总去重/排序/每轮新发现数
    if conv.findingsByRound[r-1] == 0:  break   # 收敛
phase report     → finalReport = aggregate(rounds)   # 最终审查报告
phase meta-review → metaReview = meta-review(finalReport)   # 审查报告本身：校验内部一致性
return { rounds, converged, findingsByRound, totalFindings, bySeverity, byDimension,
         report: finalReport,
         metaReview: { verdict, issues, checksRun },
         finalReport }
```

纯审查模式要点 / review-only key rules:
- **绝不修改文件**：reviewer 只读项目，所有 aggregate / meta-review 均为纯计算。
- **收敛驱动**：每轮把已知 findings 喂给 reviewer，迫使其只找新问题；某轮 0 新 findings 即收敛停止；否则到 cap。
- **产出三级**：① 审查报告（findings + 收敛统计 + 修复优先级建议）；② **meta-review**（审查报告内部一致性：`COUNT_MATCH`/`SEVERITY_SUM`/`DIMENSION_SUM`/`SORT_ORDER`/`CONVERGENCE`/`ROUND_SHAPE`）；③ **最终审查报告**（带 `approved` / `needs_revision` 判定）。
- 硬证据门禁（`reviewer.evidence_validation`，默认开启）：meta-review 会逐条校验 finding 的 `file`/`line` 是否真实存在于磁盘代码中。任何伪造路径或越界行号都会作为 critical 的 `EVIDENCE_VIOLATION` 浮出并把裁决翻转为 `needs_revision` —— 子代理只允许锚定实际读过的真实代码，禁止推测。
- 本模式不写入 `.iterate_decisions.md`（除一条 `report` 记录外），不产生任何 git 提交。

### 进度反馈 / Progress Feedback

迭代为多轮长任务，**必须**在与用户的对话中持续输出进度，避免长时间静默造成"卡住"观感。主模型遵循以下约定（写在与用户的对话里，而非仅记录到 `.iterate_decisions.md`）：

- **每轮开始**：输出 `▶ Round {N}/{maxRounds} — 启用的维度：{enabled dims}`，并简述本轮范围（涉及模块）。
- **Phase 1 并行审查期间**：若预计耗时较长，逐维度输出 `⏳ 正在审查 {dimension}（{i}/{total}）…`，让用户看到推进而非无响应。
- **每轮结束**：输出 `✅ Round {N} complete — 原子修复 x / 架构修复 y / 剩余 findings z`（或本轮失败原因）。
- **提前终止**：出现 0 findings 时明确输出 `✅ 0 findings，迭代完成` 并说明停止原因。
- 任一步骤若预计无可见输出超过合理时间，主动补一句进度说明。

### Phase 0 — 维度规划 / Dimension Planning

**仅在第 1 轮执行**。根据用户当次调用 `/iterate` 的 goal 内容，按以下**优先级**解析本轮维度方案：

**① goal 为空或泛化**（如 "improve code quality"）→ 直接使用 `iterate.config.yaml` 中的 `dimensions`，不增加摩擦。

**② goal 指定具体范围，且命中已配维度集**（范围路由 / Scope routing）：
1. 读取 `iterate.config.yaml` 的 `dimension_sets`（可同时参考 `ITERATE.md`「推荐审查蓝图」区）中的命名集。
2. 将 goal 范围与命名集名匹配（如 "前端 / 改 UI / 页面样式" → `frontend`；"API layer / 接口" → `api`；"Security audit / 安全审计" → `security`）。
3. 命中命名集 → 本轮直接采用该集的 `dimensions` 及对应的 `focus` 覆盖，**不重定义**；用 `AskUserQuestion` 简要确认后即可进入 Phase 1。
4. 用户显式指定使用预设维度（如 "use default dimensions" / "按预设审查"）→ 用全局 `dimensions`，跳过路由。

**③ goal 指定范围，但未命中任何命名集**（偏门范围 → on-the-fly **重定义**）→ 该范围没有任何现成蓝图。**一旦进入重定义，就假设「预设完全不可用」，禁止把全局 `dimensions` 或任一已有维度集当作起点来筛选/微调**——否则那只是伪重定义（多半是你偷懒套预设的结果）。必须从根为该范围重新推导：
1. **脱离预设，从根推导**：先想清该 goal 的实质——涉及哪些模块/文件、最容易**在这类改动上出错的风险是什么**。基于此推导，从**维度全集**（9 个 canonical：`correctness / security / performance / architecture / style-tests / tech-debt / spec-compliance / frontend-backend / ui-ux`）中重新选择真正相关的维度，**不受全局已启用维度限制**；确有需要时新增非标准临时维度。第 1 步不要打开 `dimensions` 或任何 `dimension_sets` 作为参照。
2. **强制写出取舍理由**：对选中的每个维度必须给出**本范围特有**的取舍理由（它为何在本范围必要、侧重点与其他范围有何不同），并据此设置针对性的 focus。**凡理由与该范围无关、或与某一预设集雷同，即视为套用预设，必须推翻重想**，直到每个维度都能独立论证。
3. 将维度 + focus 组装为方案，用 `AskUserQuestion` 请求用户确认，并明确标注这是 **「全新重定义」而非「路由到预设」**。
4. 用户确认 → 本轮采用重定义方案；用户拒绝 → 回退到全局默认 `dimensions`。

**有界记录（/ Bounded persistence — 解决迭代信息膨胀）**：
- 预设命名维度集的定义**只存**于 `iterate.config.yaml` 的 `dimension_sets`（结构性配置）。`ITERATE.md` 仅在 AI 维护区渲染**一次**「推荐审查蓝图」清单，**不随轮次增长**。
- ③ 的临时重定义**仅**在 `.iterate_decisions.md` 当轮 Round 段的专用小节
  `### Scope Dimension Redefinition (on-the-fly)` 记录（格式见决策日志模板）：须写 `**Origin scope:**`，
  并为每个重定义维度表格行给出**本范围特有的 Independent reason**，不得照抄
  `config/dimensions/<dim>.yaml` 的默认 focus（`scripts/validate.py decisions` 会据此做机器校验）。
  该记录**不写回** `iterate.config.yaml`，也**不追加**进 `ITERATE.md`。当次迭代结束后该临时方案即失效，
  后续再遇相同偏门范围应重新路由，而非沿用陈旧记录。
- `ITERATE.md` 的 AI 维护区在 refresh 时只保留**最新快照**；各轮次过程记录一律落在 `.iterate_decisions.md`。当 `.iterate_decisions.md` 超过阈值时，可将最旧轮次归档（压缩为一行摘要）或将已收敛结论提炼进 `ITERATE.md` 的知识快照后清空历史段，从根本上避免任何知识库文件无限膨胀。

> Dimension Planning 只调整维度的 focus prompt 与启用列表（或路由到命名维度集），不改变 atomic/architectural 分类标准、git 隔离、验证流程等核心机制。

### Phase 1 — 并行审查 / Parallel Review

启动 **N 个并行审查子代理**（N = 启用的 dimensions 数量，默认 9），每个审查一个维度。

Launch **N parallel reviewer sub-agents** (N = enabled dimensions count, default 9), one per dimension.

#### 可用审查维度 / Available Review Dimensions

以下维度可通过 `dimensions` 列表启用或禁用（默认 9 个）。每个维度的中文名、英文名、优先级和 focus prompt 定义在 `config/dimensions/<key>.yaml` 中；`config/dimensions.yaml` 保留为聚合兼容文件。

| 维度 / Dimension | 优先级 / Priority | 关注点 / Focus |
|------------------|-------------------|---------------|
| correctness | critical | 崩溃风险、逻辑错误、竞态条件、类型不匹配、静默吞错 |
| security | critical | 注入、路径遍历、硬编码密钥、输入校验、权限提升 |
| performance | high | N+1 查询、主线程阻塞、循环引用、O(n²)、启动瓶颈 |
| architecture | high | 模块边界违规、循环依赖、God Object、缺失抽象 |
| style-tests | medium | 函数 >80 行、圈复杂度 >15、嵌套 >3、魔法数字、缺失测试 |
| tech-debt | medium | TODO/FIXME/HACK、废弃 API、临时方案、硬编码配置 |
| spec-compliance | high | 对照 specs/ 目录，发现未实现功能、规范偏离 |
| frontend-backend | high | API/RPC 一致性、数据字段、错误传播、事件流覆盖 |
| ui-ux | medium | 加载/空/错误状态、导航、响应式断点、无障碍 |

每个子代理的任务提示：

```text
Review the codebase for {DIMENSION} issues ONLY.

Scope: {review.scope}
- "full"      → review the ENTIRE codebase.
- "changed-only" → review ONLY files changed in the current round (git diff against {git.target_branch}).
- 当 `review.scope` 为 `changed-only` 且本轮相对于 `target_branch` 无改动文件时，自动 fallback 为 `full`。

EVIDENCE RULE (mandatory): read every file you report on with the read_file tool
BEFORE judging it. You must NEVER report a location you did not actually read —
speculation about code you never inspected is a disqualifying failure, and
fabricated line numbers are treated as poisoned evidence. Anchor every finding
to real, read code.

COVERAGE RULE (mandatory): below is the exact file inventory you are assigned
to review. You MUST open EVERY file in this inventory with the read_file tool
before judging it — do not skip, skim-declare, or assume any file without
reading it. Files you did not actually open are considered un-reviewed and
will lower your coverage score. Return a `readFiles` array listing every file
you actually opened.

Assigned file inventory: {assignedFileInventory}

Focus: {focus description}

Project context: {projectContext}

For each finding, report:
- file, line (REQUIRED positive integer for anchored, line-targeted issues —
  the exact line you READ; use 0 for whole-file/module-level issues),
  severity (critical/high/medium/low)
- dimension, summary, failure_scenario, suggested_fix
- is_atomic (boolean): true if fix is ≤{atomic.max_lines} lines within a SINGLE function/file;
  false if cross-file, new files, API changes, or large refactoring.

Return strictly as JSON: { "findings": [...], "readFiles": [...] }
Each finding object must contain: file, line, severity, dimension, summary, failure_scenario, suggested_fix, is_atomic.
`readFiles` must list every file in the assigned inventory you actually opened with read_file.
If no issues are found, return { "findings": [], "readFiles": [...] }.
```

> **个性化维度 focus / Personalization dimension focus**：若 `personalization.dimension_focus` 中存在当前维度的条目，将其 `focus` 文本追加到上述 prompt 的 `Focus:` 段之后，例如：
> ```
> Focus: {focus description}
> 
> Extra focus (from personalization): {personalization.dimension_focus[dimension].focus}
> ```

#### 工具映射 / Tool Mapping

| 工具 / Tool | Trae | Claude Code | Cursor / Generic |
|-------------|------|-------------|------------------|
| 并行审查子代理 | `Task` × N (type: `search` or `general_purpose_task`) | `Workflow` / `Agent` × N | 手动或脚本并行运行 |
| 按目录拆分审查 | `Task` per directory/module | `Agent` per directory/module | 脚本分组 |
| 结果汇总 | `Task` (type: `general_purpose_task`) | `Agent` synthesize | 人工汇总 |
| reviewer 输出 schema 校验 | 主模型 JSON parse + field check | 主模型 JSON parse + field check | 脚本校验 |
| 用户审批 | `AskUserQuestion` | `EnterPlanMode` / `ExitPlanMode` | 对话确认 |
| 文件编辑 | `Read` / `Edit` / `Write` | `Read` / `Edit` / `Write` | IDE 编辑 |
| 执行命令 | `RunCommand` | `Bash` | Terminal |
| 配置校验 | `python scripts/validate.py config ...` | `python scripts/validate.py config ...` | 同左 |

#### 支持的 AI 助手与安装路径 / Supported Assistants

使用 `scripts/install.py install --ai <name> --target <project>` 即可安装到对应目录：

| AI 助手 / Assistant | 安装路径 / Install Path |
|---------------------|------------------------|
| Trae | `.trae/skills/iterate/` |
| Claude Code (`claude` / `claude-code`) | `.claude/skills/iterate/` |
| Cursor | `.cursor/skills/iterate/` |
| Windsurf | `.windsurf/skills/iterate/` |
| GitHub Copilot | `.github/skills/iterate/` |
| OpenAI Codex | `.codex/skills/iterate/` |
| Roo Code | `.roo/skills/iterate/` |
| Qoder | `.qoder/skills/iterate/` |
| Gemini CLI (`gemini` / `gemini-cli`) | `.gemini/skills/iterate/` |
| OpenCode | `.opencode/skills/iterate/` |
| Continue | `.continue/skills/iterate/` |
| Augment | `.augment/skills/iterate/` |
| Warp | `.warp/skills/iterate/` |
| Aider | `.aider/skills/iterate/` |
| AiderDesk | `.aiderdesk/skills/iterate/` |
| Zed | `.zed/skills/iterate/` |
| Cline | `.cline/skills/iterate/` |
| OpenClaw | `skills/iterate/` |
| Autohand | `.autohand/skills/iterate/` |
| Bob | `.bob/skills/iterate/` |
| CodeArts | `.codeartsdoer/skills/iterate/` |
| Antigravity | `.antigravity/skills/iterate/` |
| Amp | `.amp/skills/iterate/` |
| DeepAgents | `.deepagents/skills/iterate/` |
| Kimi | `.kimi/skills/iterate/` |
| Astral | `.astral/skills/iterate/` |

`<name>` 取上表第一列的标识符；完整列表以 `scripts/install.py install --help` 输出的 `choices` 为准（上表与 `SUPPORTED_AI` 保持同步，详见 `npm-installer/README.md`）。

安装脚本会自动复制 `SKILL.md`、配置、维度定义、校验脚本和模板到对应目录；`--ai all` 一次性安装到所有支持的助手目录。

常用 CLI 选项（`scripts/install.py`，均需与子命令搭配）：
- `install --ai <assistant>|all`：指定安装目标；**非交互（管道/CI）下必填**，否则无法提问。
- `install --force`：覆盖已存在的 skill 文件。
- `install --global`：安装到用户主目录（如 `~/.trae/skills/iterate/`），供所有项目复用。
- `install --dry-run`：只打印将要拷贝的内容，不落盘。
- `install --target <dir>`：指定安装根目录（默认当前项目）。
- `uninstall --yes`：卸载已安装的 skill；不加 `--yes` 时会要求二次确认。
- `update --yes`：从 GitHub 最新 release 下载源码刷新文件，跳过确认；**非交互（管道/CI）下必填**，否则会以"检测到非交互 stdin"退出 1。
- `update`（不带 `--yes`）：同上，但交互确认；下载失败时回退到本地源码。
- `config --list`：打印当前项目 `iterate.config.yaml`（与"列出支持的助手"无关）。
- `config --interactive`：进入项目配置交互向导。
- 支持的助手名以 `install --ai <name>` 的 `choices` 为准（见上表；`--ai all` 安装到全部）。

#### 按模块/目录拆分 / Split by Module or Directory

当项目较大时，可将一个维度拆分为多个子任务，每个任务只审查一个模块或目录：

```text
Split dimension {DIMENSION} review by top-level directories.
For each directory, launch a reviewer with scope "changed-only" or "full".
Merge findings, removing duplicates across directory boundaries.
```

#### 子代理失败处理 / Sub-agent Failure

若某个 reviewer 子代理失败、超时或返回无效输出：

1. 若输出非严格 JSON 且 `reviewer.output_schema_validation` 为 true，针对该子代理最多重试 2 次，每次在 prompt 中强调返回严格 JSON。
2. 若仍失败，记录失败原因到 `.iterate_decisions.md`。
3. 使用 `AskUserQuestion` / 对话确认询问用户：
   - 继续（continue）：忽略该失败，按当前已收集的 findings 继续。
   - 跳过该维度（skip）：该维度本轮不产生 findings。
   - 中止本轮（abort round）：直接退出本轮循环，进入 Phase 4 记录后结束。

> 若选择 skip 或 abort，仍应将失败原因写入决策日志，避免遗漏审查维度。

#### 汇总与分类 / Synthesize and Classify

使用一个汇总子代理：

```text
Synthesize findings from all reviewers.

Goal: {goal} / Round: {round}

Steps:
1. PARSE each reviewer output as JSON; if invalid and reviewer.output_schema_validation is true, retry that reviewer up to 2 times.
2. REMOVE duplicates (same defect, same file → keep most detailed)
3. REMOVE false positives (clearly wrong or unactionable)
4. **FILTER known intentional**：若 `personalization.known_intentional` 非空，移除匹配的 findings。匹配规则：finding 的 `file` 与条目的 `file` 相同，且（条目 `line` 为 0，或 finding 的 `line` 与条目 `line` 相同），且 `dimension` 相同。被过滤的 finding 数量记入决策日志。
5. RE-VALIDATE is_atomic flag for each finding
6. CLASSIFY into atomic and architectural
7. SORT each group by severity (critical → high → medium → low)
8. TRIM each group to 20 max

Return: { "empty": boolean, "atomic": [...], "architectural": [...] }
```

停止条件检查：

```text
if empty AND deferredArchitectural is empty:
    写入 .iterate_decisions.md: "Round {round}: 0 findings, iteration complete."
    输出: "✅ Round {round}: 0 findings, iteration complete."
    break
```

> **注意 / Note**：如果所有 reviewer 都返回空但代码中明显存在问题，主模型应基于自身判断补充 findings。

---

### Phase 2 — 原子问题直接修复 / Atomic Fixes

若存在原子问题：

1. **计划（内部，不中断） / Plan internally**
   - 分析所有原子 findings。
   - 合并对同一文件的修改。
   - 按严重程度和依赖排序。
   - **应用个性化优先级**：若 `personalization.fix_priority_order` 非空，按其指定的维度顺序重新排序（列在前面的维度优先修复），同维度内仍按严重程度排序。
   - 输出简短计划列表告知用户。

2. **顺序执行 / Execute sequentially**

   ```text
   for each atomic finding:
       # Protected paths check
       if finding.file matches any pattern in personalization.protected_paths:
           skip this finding, log "skipped: protected path {finding.file}"
           continue

       # Risk areas check
       if finding.file is under any personalization.risk_areas[].path:
           use AskUserQuestion to get explicit user approval before modifying
           if user declines: skip, log "skipped: risk area not approved"

       # Forbidden fixes check
       ensure the planned fix does not use any approach in personalization.forbidden_fixes
       if it would: skip, log "skipped: forbidden fix approach"

       Read target file
       Apply fix using Edit/Write (ensure ≤ atomic.max_lines, single function scope)
       Record completion status
   ```

   > **禁区/风险区/禁止方式 / Protected / Risk / Forbidden**：这三项检查在每次修改文件前都必须执行。`protected_paths` 是 glob 模式（如 `legacy/**`），用 `fnmatch` 或等价方式匹配。`risk_areas` 路径是目录或文件前缀匹配。`forbidden_fixes` 是字符串描述，AI 判断修复方式是否匹配。

3. **验证原子修复 / Validate atomic fixes**

   根据改动的模块跑对应检查（从 `validation.commands` 读取，键名为示例）：

   - 确定本轮修改涉及的模块集合：根据修改文件的路径、扩展名或目录结构匹配 `validation.commands` 中的模块键名。
   - 若改动涉及多个模块，依次执行每个模块对应的命令列表。
   - 若某模块未在 `validation.commands` 中配置命令，跳过并提示用户补充配置。
   - 任一模块验证失败即停止后续检查，进入失败处理流程。

   示例 / Examples：

   - `python/`：`ruff check src/ && mypy src/ --ignore-missing-imports && pytest tests/ -x -q`
   - `swift/`：`swift build -c debug`
   - `typescript/`：`npm run compile`

   执行前遵循统一运行时白名单语义：只执行 `validation.commands.<module>` 中**显式配置的精确命令**（不自行拼装、不基于前缀构造命令）；未配置命令的模块跳过。`validation.command_whitelist` 仅为配置期校验辅助字段（见下方 Security 章节），可缺省、无运行时约束力——即便未配置，运行时仍以 `validation.commands` 为唯一权威白名单，不在其中的命令**直接拒绝，不可通过用户确认绕过**。

   若验证失败：
   - 追加 `.iterate_decisions.md`：`Atomic fix validation failed: {details}`
   - 输出：`❌ Round {round}: atomic fix validation failed, stopping iteration`
   - **回滚本轮所有原子修改**：`git restore --staged --worktree .`（非破坏性回滚，恢复暂存区和工作区到 HEAD 状态）。**仅限 `iterate/*` 分支执行**（仍在迭代分支上，不影响 main/master）。
   - 将本轮已识别但未执行的架构问题保留在 `deferredArchitectural` 中，供下次 `/iterate` 会话处理。
   - `break`

---

### Phase 3 — 架构问题修复 / Architectural Fixes

若存在架构问题（含 `deferredArchitectural`）：

1. **文件碰撞检测 / File conflict detection**
   - 收集 Phase 2 修改过的所有文件。
   - 对每个架构 finding，检查其文件是否与原子修复文件重叠。
   - 重叠 → 移入 `deferredArchitectural`（下一轮处理）。
   - 不重叠 → 移入 `executableArchitectural`。

2. **分组与排序 / Group and sort**
   - 按模块依赖顺序排序（先被依赖，后依赖者）。
   - 合并同一模块/文件组的 finding 为一个 task。
   - 检测 `executableArchitectural` 内部 task 之间的文件重叠；如有重叠，按依赖顺序拆分为串行 task 或合并为单一 task。
   - 最终确保不同 task 之间的文件集互不重叠。

3. **用户审批 / User approval** — **强制门禁 / Mandatory gate**

   > **安全约束 / Security constraint**：架构修复**必须**经用户显式批准后方可执行。此门禁不可跳过、不可自动绕过。即使用户在配置中启用了 `auto_merge: true`，架构修复的审批仍然独立于 merge/push 流程，必须单独获得用户确认。

   呈现给用户：

   ```text
   可执行的架构修复 / Executable architectural tasks:
   - {files} | {description} | {severity} | {approach}

   延迟的架构修复 / Deferred tasks:
   - {files} | {description} | {reason}

   Approve these {N} architectural fixes?
   ```

   - 批准 → 继续执行。
   - 拒绝 → 全部 executable 移入 `deferredArchitectural`，跳到 Phase 4。

4. **串行委派子代理 / Execute serially via sub-agents**

   ```text
   for each task in executableArchitectural:
       # Protected paths check (same as Phase 2)
       if any file in task.files matches personalization.protected_paths:
           defer this task, log "deferred: protected path"

       # Risk areas check (same as Phase 2)
       if any file in task.files is under personalization.risk_areas[].path:
           use AskUserQuestion to get explicit user approval
           if declined: defer, log "deferred: risk area not approved"

       Use sub-agent with prompt:

       "You are fixing an architectural issue.

       Goal: {goal} / Round: {round}
       Project context: {projectContext}

       Task: {task description with file paths, findings, approach}

       Constraints (from personalization):
       - Forbidden fix approaches: {personalization.forbidden_fixes or 'none'}
       - Do NOT use any of these approaches in your fix.

       Workflow:
       1. Read all affected files, their callers, and callees.
       2. Apply the fix using Edit/Write tools.
       3. Report: success/failure, files_changed, summary, notes.

       Previous tasks in this round may have changed some files.
       Read files fresh before editing — they may have been modified.
       Do NOT run build/test commands."

       Wait for completion before starting the next task.
       If a sub-agent fails, log the reason, report it to the user, and ask whether to continue, skip, or abort the round.
   ```

5. **整体验证 / Full validation**

   根据改动模块跑完整验证（同 Phase 2，但覆盖所有改动模块）。

   执行前遵循运行时唯一权威白名单（同 Phase 2）：只执行 `validation.commands.<module>` 中的精确命令。

   若失败：
   - 追加 `.iterate_decisions.md`：`Full validation failed: {details}`
   - 输出：`❌ Round {round}: full validation failed, stopping iteration`
   - **回滚本轮所有修改**（原子 + 已执行架构）：`git reset --mixed iterate/round-{round}-backup && git restore --worktree .`（非破坏性回滚：`--mixed` 移动分支指针但不改工作区，`git restore` 再恢复工作区文件）。**仅限 `iterate/*` 分支执行**（仍在迭代分支上，不影响 main/master）。
   - 将未执行的架构问题保留在 `deferredArchitectural` 中。
   - `break`

---

### Phase 4 — 记录本轮结果 / Record Round Results

追加到 `.iterate_decisions.md`：

- 原子修复列表 + 状态
- 架构修复列表（已执行 + 延迟 + 原因）
- 修改范围审计：本轮修改的文件清单、每个文件对应的 task/reviewer、审批状态
- AI 重要决策

输出：`✅ Round {round} complete`

---

### Phase 5 — 验证、合并、推送 / Validate, Merge, Push

每轮验证通过后：

1. **Backup tag / 备份标签**
   - 在 commit 前为当前迭代分支打标签：`git tag iterate/round-{round}-backup`
   - 若后续需要回滚，可 `git reset --mixed iterate/round-{round}-backup && git restore --worktree .`（非破坏性回滚）。**仅限 `iterate/*` 分支执行**（仅用于迭代分支，不用于 main/master）。

2. **Commit / 提交**
   - `git add <changed files>`
   - `git commit -m "fix: iterate round {round} — {brief summary}"`

3. **Merge / 合并** ⚠️ **高风险动作 / High-risk action**
   - **默认安全 / Secure by default**：`git.auto_merge` 默认为 `false`，即不自动 merge。仅当用户在配置中显式设为 `true` 时才执行以下 merge 步骤。
   - **风险提示 / Risk notice**：若启用自动 merge，回 `target_branch`（通常为 `main`）会将本轮所有修改立即推到主分支历史。建议保持 `auto_merge: false`，改为创建 PR 由人工 review；或为 `main` 启用分支保护。
   - 若 `git.auto_merge` 为 `true`：
     - `git checkout {target_branch}`
     - `git merge iterate/<goal-slug>-<timestamp>`
     - 如有冲突，先尝试自动解决；若无法自动解决，**停止合并并询问用户**手动解决或跳过本轮。
     - 冲突解决后重新验证，验证失败则切回迭代分支，**不推进 main/master**。
   - 若 `git.auto_merge` 为 `false`（默认）：
     - 不执行 merge，修改保留在迭代分支上。
     - 可使用 `AskUserQuestion` 询问用户是否在本轮手动 merge 或留到会话结束时统一处理。

4. **Push / 推送** ⚠️ **高风险动作 / High-risk action**
   - **默认安全 / Secure by default**：`git.push_per_round` 默认为 `false`，即不自动 push。
   - **风险提示 / Risk notice**：若启用自动 push，会立即对外可见，且后续轮次会基于已 push 的状态继续迭代。建议保持 `push_per_round: false`，由用户在会话结束时决定是否推送。
   - 若 `git.push_per_round` 为 `true`：
     - `git push origin {target_branch}`
     - 若被拒绝，先 `git pull --rebase`，解决冲突，重新验证，再 push。
     - push-pull-rebase 循环最多执行 3 次；超过仍失败则停止并告知用户手动处理。
     - **绝不 force-push 到 main/master**。
   - 若 `git.push_per_round` 为 `false`（默认）：
     - 本轮回不 push，只保留本地 merge（若 `auto_merge` 也为 false，则仅保留在迭代分支）。
     - **会话结束时不自动 push**。仅在用户于会话结束时明确要求推送后，才执行一次 `git push origin {target_branch}`；同样遵循 3 次循环限制。未得到明确要求时，把改动留在本地分支并告知用户。

5. **切回迭代分支 / Switch back**
   - `git checkout iterate/<goal-slug>-<timestamp>`
   - 继续下一轮。

6. **记录 / Log**
   - 在 `.iterate_decisions.md` 中记录 backup tag、commit hash、merge 结果、冲突处理。

```
round += 1
```

---

## Step 3 — 汇总报告 / Summary Report

迭代结束后输出：

- 总轮数 / Total rounds
- 停止原因 / Stop reason
- 每轮原子修复数 + 架构修复数 / Per-round atomic + architectural fix counts
- 剩余延迟架构问题（如有）/ Remaining deferred architectural issues
- `.iterate_decisions.md` 路径 / Decision log path
- 迭代分支名 / Iteration branch name

### 交付指引 / Handoff（改动如何处理）

改动默认保留在迭代分支 `iterate/<goal-slug>-<timestamp>`（未启用 `auto_merge` / `push_per_round`）。汇总后**必须**明确告知用户后续操作，不要让用户困惑"改动去哪了"：

- 说明：分支名、`.iterate_decisions.md` 路径、以及是否已合并/推送。
- 给出清晰选项：让用户 **人工 review 后自行合并推送**，或 **询问是否由 AI 代为合并/推送**（此时先 review 差异再执行安全命令）。
- 若用户希望保留分支以便二次审查，也予以确认，不强行清理。

### 提前终止 / Early Stop

默认在出现 0 findings 时结束。此外，在每轮结束后评估：

- 若剩余 findings 均为 **low** 且目标基本达成，或达到用户明确设定的目标，可询问用户"是否提前结束本轮迭代"，避免无谓多轮消耗。
- 若用户确认提前结束，输出停止原因与交付指引后退出循环。

---

## Git 隔离工作流 / Git Isolation Workflow

**规则 / Rule**：每次 `/iterate` 会话必须在隔离的本地分支或 worktree 中运行。**绝不直接在 main/master 上提交**。合并与推送均为**主动选择（opt-in）**动作：`git.auto_merge` 与 `git.push_per_round` 默认均为 `false`，仅在用户显式启用时才自动 merge/push；未启用时，改动保留在迭代分支，由用户在会话结束时人工 review 后决定合并或推送。

**Why**：
- 保持主工作区稳定。
- 每轮都是独立可审查、可回滚的 commit。
- 启用 `push_per_round` 时，远程保存最新验证状态；未启用时，改动只留在本地分支，等用户决定。

### 每会话流程 / Per-Session Flow

```bash
# 1. Setup
git status                                          # 确认状态；有未提交改动时优先用 worktree 隔离
git checkout -b iterate/<goal>-<date>               # 或 git worktree add ../<name> -b iterate/<goal>-<date>

# 2. Each round (after validation passes)
git add <changed files> && git commit -m "fix: iterate round {N} — ..."
# merge / push 均为 opt-in：仅在 auto_merge / push_per_round 为 true，
# 或用户在会话结束时明确要求时，才执行下面两行
git checkout <target-branch>
git merge iterate/<goal>-<date>                     # 解决冲突，重新验证
git push origin <target-branch>                     # 仅 opt-in 时
git checkout iterate/<goal>-<date>                  # 继续下一轮

# 3. Session end
# 未启用 auto_merge / push_per_round 时：改动留在本地分支，告知用户位置；
# 是否合并/推送由用户决定，不要自动执行。
# 可询问用户是否删除已合并的迭代分支
```

### 会话中断与恢复 / Session Interruption and Resume

若会话因用户关闭、AI 异常或验证失败而中断：

1. 保留当前迭代分支和 `.iterate_decisions.md`，不要删除。
2. **下次调用 `/iterate` 时，AI 应主动**先读取 `.iterate_decisions.md`（用户无需自行理解该文件），自动提取并简要呈现：
   - 上次的迭代分支名。
   - 已完成的轮数、`deferredArchitectural` 列表。
   - 是否有未 push 的本地 merge。
   - 上次停止时的轮次与剩余 findings 概要。
3. 基于以上状态，**主动向用户提议**下一步，而非让用户判断：
   - **继续上次会话（resume）**：切回迭代分支，从下一轮继续。
   - **重新开始（restart）**：创建新迭代分支，`deferredArchitectural` 可继承或清空。
   - **仅查看报告**：只输出上次汇总，不继续迭代。
4. 若上一轮已合并到 main/master 但未 push，在 resume 时**先询问用户**是否推送；得到明确同意后再 push，不要自动补推。

### 护栏 / Guardrails

- 循环中绝不直接提交到 main/master。
- 绝不 force-push 到 main/master。
- Push 被拒绝时，先 `git pull --rebase`，解决冲突，重新验证，再 push。
- 若某轮验证失败，**不要合并该轮**，留在迭代分支上并告知用户。

---

## 决策日志格式 / Decision Log Format

文件路径：`.iterate_decisions.md`

```markdown
# Iterate Decision Log

Goal: {goal}
Max rounds: {maxRounds}
Started: {timestamp}
Branch: {iteration-branch}

---

## Round {N} — {timestamp}

### Atomic Fixes (Direct)
| # | File | Summary | Severity | Status |
|---|------|---------|----------|--------|
| 1 | x.swift | Fix null pointer | high | ✅ |

### Architectural Fixes (Approved + Executed)
| # | File(s) | Summary | Severity | Status |
|---|---------|---------|----------|--------|
| 1 | y.swift, z.swift | Unified error handling | critical | ✅ Executed |

### Architectural Fixes (Deferred to Next Round)
| # | File(s) | Summary | Defer Reason |
|---|---------|---------|-------------|
| 1 | a.swift, b.swift | Refactor data flow | File conflict with atomic fix |

### Reverted Fixes
| # | File(s) | Summary | Revert Reason |
|---|---------|---------|---------------|
| 1 | shared/error_codes.json | Merge v1 codes | Conflict with authoritative v2.0 numbering |

### AI Important Decisions
| # | Decision | Reason |
|---|---------|--------|
| 1 | Merged 5 findings into 1 task | Same module |

### Validation
- ruff check src/ → 0 errors
- mypy src/ → Success
- pytest tests/ → 2600 passed, 0 failed
```

---

## Skill 目录结构 / Skill Directory Layout

一个完整的 iterate skill 目录应包含以下文件（相对 `SKILL.md` 的路径固定）：

```text
iterate/
├── SKILL.md                          # 技能入口与使用说明
├── pyproject.toml                    # Python 包定义（iterate CLI entry point）
├── config/
│   ├── iterate.config.yaml           # 默认配置
│   ├── config.schema.json            # iterate.config.yaml 的 JSON Schema
│   ├── dimensions.yaml               # 聚合版维度定义（兼容旧版）
│   └── dimensions/                   # 数据驱动的维度定义
│       ├── correctness.yaml
│       ├── security.yaml
│       ├── performance.yaml
│       ├── architecture.yaml
│       ├── style-tests.yaml
│       ├── tech-debt.yaml
│       ├── spec-compliance.yaml
│       ├── frontend-backend.yaml
│       └── ui-ux.yaml
├── iterate_cli/                      # iterate CLI 包（onboarding 命令行工具）
│   ├── __init__.py
│   ├── __main__.py                   # python -m iterate_cli 入口
│   ├── cli.py                        # argparse 子命令（onboard/refresh/reonboard/status/doctor/…）
│   ├── tui.py                        # 轻量 TUI 助手（skills.sh 风格输出、banner）
│   ├── fingerprint.py                # manifest 哈希与漂移检测
│   ├── backup.py                     # 时间戳备份的列出与恢复（backup 子命令）
│   ├── scan.py                       # 项目扫描（技术栈/目录/特性检测）
│   ├── wizard.py                     # CLI 交互式 onboarding 向导
│   ├── generator.py                  # ITERATE.md + iterate.config.yaml 生成器
│   ├── refresh.py                    # 增量刷新与完整重 onboarding
│   ├── doctor.py                     # 项目健康诊断（doctor 子命令）
│   ├── guard.py                      # 防御式编程校验（guard pre/post-check、invariant 子命令）
│   ├── personalize.py                # 个性化约束管理（personalize 子命令）
│   ├── show.py                       # 只读展示生效配置与个性化状态（show 子命令）
│   └── data/
│       ├── ITERATE.template.md       # 模板副本（随包分发）
│       └── config.schema.json        # schema 副本（随包分发，与 config/ 保持同步）
├── scripts/
│   ├── install.py                    # CLI：安装、卸载、配置、校验
│   ├── update_downloads_badge.py     # 拉取三平台下载量并写 badges/downloads.json
│   ├── validate.py                   # 配置、决策日志、维度校验脚本
│   └── requirements.txt              # 校验脚本依赖
├── templates/
│   ├── iterate-decisions.template.md # 决策日志模板
│   ├── ITERATE.template.md           # 项目知识库模板（分区：AI 维护 + 用户维护）
│   └── onboarding-playbook.md        # AI onboarding 参考映射（仅供参考）
├── tools/
│   ├── SKILL.trae.md                 # Trae 专属 prompt/workflow 示例
│   ├── SKILL.claude.md               # Claude Code 专属 workflow 示例
│   └── SKILL.cursor.md               # Cursor 专属 prompt 示例
├── tests/
│   ├── test_dimension_lock.py        # 六源维度系统一致性锁定（skill ↔ harness）
│   ├── test_doctor.py                # doctor 项目健康诊断测试
│   ├── test_drift_ignore.py          # 漂移忽略与 status 漂移建议测试
│   ├── test_guard.py                 # 防御式校验（guard / invariant）测试
│   ├── test_install_script.py        # install.py 安装脚本测试
│   ├── test_onboarding.py            # onboarding 模块测试
│   ├── test_refresh_reconcile.py     # refresh 对账测试
│   ├── test_tui.py                   # TUI 渲染器接口契约测试
│   ├── test_update_downloads_badge.py# update_downloads_badge.py 测试
│   └── test_validate.py              # 校验脚本测试
└── README.md / CONTRIBUTING.md       # 用户与贡献者文档
```

运行时优先读取**项目根目录**的 `iterate.config.yaml`；若不存在，则使用 skill 目录下的 `config/iterate.config.yaml` 作为默认配置。校验脚本路径以 `${CLAUDE_SKILL_DIR}/scripts/validate.py`（Claude Code）或 skill 安装目录相对路径解析。

---

## 配置说明 / Configuration

默认配置见 [`config/iterate.config.yaml`](./config/iterate.config.yaml)。

| 配置项 / Key | 类型 / Type | 默认值 / Default | 说明 / Description |
|--------------|-------------|------------------|--------------------|
| `goal` | string | `"Improve code quality and maintainability"` | 迭代目标 |
| `max_rounds` | int | `7` | 最大轮数 |
| `language` | string | `"en"` | 输出语言 `zh` / `en` |
| `mode` | string | `"iterate"` | 本次调用默认模式：`iterate`（原模式）/ `defensive`（防御式编程模式）；可用调用参数 `defensive` 显式覆盖（v3.0） |
| `invariants.ensure` | list | `[]` | 项目级不变量：收尾时必须存在的文件路径断言（相对项目根，`iterate invariant` 校验，v3.0） |
| `invariants.commands.<module>` | list | `[]` | 项目级不变量：收尾时必须通过的命令列表（精确匹配、走安全基线；无 `invariants` 段时 `iterate invariant` 退化为 `validation.commands`，v3.0） |
| `dimensions` | list | 全部 9 维度 | 启用的审查维度 |
| `review.scope` | string | `"full"` | 审查范围：`changed-only` / `full` |
| `atomic.max_lines` | int | `20` | 原子问题行数上限 |
| `atomic.max_adjacent_methods` | int | `3` | 相邻方法数上限 |
| `git.target_branch` | string | `"main"` | 合并目标分支 |
| `git.use_worktree` | bool | `false` | 是否默认使用 worktree；**当工作区有未提交改动/未跟踪文件时，无论此值如何，都优先用 worktree 隔离**（见 Step 1.7） |
| `git.push_per_round` | bool | `false` | 每轮通过后是否立即 push（默认 false，安全） |
| `git.auto_merge` | bool | `false` | 每轮验证后是否自动 merge 回 target_branch（默认 false，安全） |
| `validation.command_whitelist` | list | 常见命令前缀 | 配置期校验辅助字段（可选、可缺省）：`scripts/validate.py` 据此检查 `validation.commands` 各命令以合理工具前缀开头；无运行时约束力，运行时以 `validation.commands` 为唯一权威 |
| `validation.commands.<module>` | list | 示例命令 | 各模块验证命令；**运行时唯一权威白名单**，AI 只执行其中的精确命令，不自行拼装或基于前缀构造命令 |
| `reviewer.output_schema_validation` | bool | `true` | 是否校验 reviewer JSON 输出并自动重试 |
| `reviewer.evidence_validation` | bool | `true` | 硬证据门禁：meta-review 校验每个 finding 的 file/line 真实性，伪证判 `needs_revision` |
| `reviewer.coverage_validation` | bool | `true` | 范围覆盖率校验（提示性）：自报 `readFiles` 明显不覆盖分配清单时浮出 `COVERAGE_GAP`，不反转判定 |
| `reviewer.scope_chunk_size` | int | `25` | `full` 审查每批分配的文件数，按此拆分 reviewer 任务 |
| `personalization.protected_paths` | list | `[]` | 禁区 glob 模式，iterate 不得修改 |
| `personalization.risk_areas` | list | `[]` | 风险区（path + reason），改动需用户审批 |
| `personalization.known_intentional` | list | `[]` | 已知意图（file:line + dimension），Phase 1 过滤误报 |
| `personalization.dimension_focus` | list | `[]` | 维度定制（dimension + focus），追加到 reviewer prompt |
| `personalization.fix_priority_order` | list | `[]` | 修复优先级顺序（从高到低） |
| `personalization.forbidden_fixes` | list | `[]` | 禁止的修复方式（如 `# noqa`） |

> **个性化配置由 `iterate onboard` 或 `iterate personalize` 写入**，捕获 AI 扫描不到的项目专属约束。详见 README 中的"个性化配置 / Personalization"章节。
| `onboarding.version` | string | `"1.0"` | 指纹 schema 版本 |
| `onboarding.completed_at` | string | — | 上次 onboarding/刷新的 ISO 8601 时间戳 |
| `onboarding.channel` | string | — | onboarding 通道：`cli` / `ai` |
| `onboarding.drift_check` | bool | `true` | 是否在每次调用时检查 manifest 漂移 |
| `onboarding.drift_ignore` | list | `[]` | 漂移忽略的 manifest glob 模式（如 `package-lock.json`），命中文件不计入漂移 |
| `onboarding.fingerprints` | list | — | manifest 文件的 SHA-256 哈希列表（自动生成） |

---

## 安全与敏感信息保护 / Security & Sensitive Data

1. **所有 AI 操作不读取敏感文件 / No sensitive file access**
   - 主模型、reviewer 子代理、架构修复子代理均不得读取敏感文件，包括但不限于：
     `.env`、`.env.*`、`*.key`、`secrets/`、`*.pem`、`.p12`、`.crt`、`.cer`、
     `credentials.json`、`.aws/`、`.ssh/`。
   - `projectContext` 中不得包含 API 密钥、密码、Token、数据库连接字符串、私钥内容。
   - 执行命令时避免将敏感文件作为参数或输出内容。
   - onboarding 扫描仅检查 `package.json`、`pyproject.toml` 等 manifest 文件的存在性，以及 `README.md` / `CLAUDE.md` 等公开上下文文件；不会读取 `.env`、密钥、凭证或其他敏感文件内容。

2. **命令白名单 / Command whitelist — 运行时与配置期分离**
   - **运行时唯一权威 = `validation.commands.<module>` 精确命令 / Runtime authoritative whitelist**：AI 执行验证命令时，只执行 `validation.commands` 中用户显式配置的**精确命令**，不自行拼装、不基于前缀构造命令；未配置命令的模块跳过。不在其中的命令**直接拒绝，不可通过用户确认绕过**。`validation.command_whitelist` 不参与运行时判定。
   - **配置时校验 / Config-time validation**：`scripts/validate.py` 在校验配置时检查 `validation.commands` 中的每条命令是否以 `validation.command_whitelist` 中的前缀开头（该校验后再决定命令是否合理）。不在白名单中的命令会报错，配置校验失败。`command_whitelist` 为可选字段，仅在此处生效。
   - **个性化硬白名单 / Personalization strict whitelist**：`iterate personalize` 中添加 `extra_validation_commands` 时，使用 `validate_extra_command` 进行硬白名单校验——拒绝 shell 链接元字符（`;`、`|`、`&` 等），且只接受预批准的工具前缀（pytest/ruff/mypy/eslint/swift/cargo 等 30+ 常见 test/lint/build 工具）。不在白名单中的命令**直接拒绝**，不可通过用户确认绕过。
   - 默认白名单：`ruff`, `mypy`, `pytest`, `swift`, `npm run`, `yarn`, `pnpm`, `go test`, `cargo`, `python`, `python3` 等已知前缀。
   - 可用 `python scripts/validate.py config <path>` 提前检查命令合规性。

3. **修改范围审计 / Modification scope audit**
   - 每轮 `.iterate_decisions.md` 必须记录：本轮修改的文件、对应 task/reviewer、用户审批状态。
   - 子代理只允许修改任务描述中的文件；越权修改必须报告并中止。

4. **No force-push / No direct main commits**
   - 绝不 force-push 到 `main`/`master`。
   - 绝不直接在 `main`/`master` 上提交。

5. **高自主性风险披露 / High-autonomy risk disclosure**
   - 本 skill 会自主执行文件编辑、`git` 操作（commit/merge/reset）以及 `validation.commands` 中配置的命令。
   - 所有代码修改先在隔离的 `iterate/*` 分支或 worktree 中进行。
   - `git.auto_merge` 与 `git.push_per_round` 默认均为 `false`（安全默认）；merge/push 是 opt-in 动作，仅在用户显式开启时自动执行，否则改动保留在迭代分支由人工 review。
   - 架构修复必须经用户批准后方可执行。
   - 运行前请确保 `validation.command_whitelist` 和 `validation.commands` 只包含你信任的命令。

6. **Update 命令远程下载说明 / Update command remote download**
   - `scripts/install.py update` 与 `npx iterate-skill-installer` 会从 GitHub Release 下载预上传的 `iterate-skill.tar.gz` + `SHA256SUMS.txt`。
   - 下载前会提示确认（可用 `--yes` 跳过）。
   - **强制校验 / Mandatory checksum verification**：下载 release tarball 时**必须**先下载 `SHA256SUMS.txt`，再用其中记录的哈希校验 tarball 完整性。若 release 缺少 `SHA256SUMS.txt` asset、`iterate-skill.tar.gz` asset，或校验和不匹配，**拒绝下载并回退到本地源码**。绝不会在未校验完整性的情况下安装远程代码。

7. **安装器额外披露 / Installer disclosure**
   - `npx iterate-skill-installer` 在复制 skill 文件的同时，会顺带把 `iterate` CLI 安装到 PATH（优先 `pipx` 隔离安装，否则 `pip install --user`），以便安装完成后可直接运行 `iterate onboard`。
   - 这是刻意的端到端设计，但确实会在系统上放置一个可执行文件。若不希望自动安装 CLI，请使用手动复制 `SKILL.md` 或源码脚本 `python scripts/install.py install` 的方式。

## Reviewer Prompt 质量检查清单 / Reviewer Prompt Quality Checklist

在启动 reviewer 前确认：

- [ ] 已注入 `projectContext`，但不含密钥。
- [ ] 已明确 `review.scope`（`changed-only` 或 `full`）。
- [ ] 已说明 `atomic.max_lines` 和 `atomic.max_adjacent_methods`。
- [ ] 已要求返回严格 JSON 并列出必填字段。
- [ ] 已明确 `line` 为必填（行级问题为精确读到的行号，整文件/模块级问题为 0）。
- [ ] 已注入 EVIDENCE RULE：必须先用 `read_file` 读过，才允许报告该文件/行；禁止推测未读代码，禁止编造行号（视为 poisoned evidence）。
- [ ] 已注入 COVERAGE RULE：把子代理被分配到的文件清单（`full` 下按 `scope_chunk_size` 分批）逐一列出，要求用 `read_file` 读遍每一份并返回 `readFiles`；未实际读阅的文件视为未审查。
- [ ] 已确认 meta-review 硬证据门禁（`reviewer.evidence_validation`，默认开）会把伪造路径/越界行号判为 `EVIDENCE_VIOLATION` → `needs_revision`。
- [ ] 已确认范围覆盖率校验（`reviewer.coverage_validation`，默认开）会在自报 `readFiles` 明显不覆盖分配清单时浮出 medium 的 `COVERAGE_GAP` 提示（不反转判定）。
- [ ] 已说明禁止读取敏感文件。
- [ ] 大项目已按目录/模块拆分 reviewer 任务。

## 重要注意事项 / Important Notes

1. **项目上下文动态读取 / Dynamic context**：从 `CLAUDE.md` 或 `iterate.config.yaml` 读取，不硬编码。
2. **原子修复不中断 / Atomic fixes are non-blocking**：主模型直接执行，不需要用户批准。
3. **架构修复串行 / Architectural fixes are serial**：按依赖顺序逐个执行，后面的子代理能看到前面的改动。
4. **文件碰撞显式延迟 / File collisions are explicitly deferred**：不依赖 reviewer 再次发现。
5. **原子验证失败立即停止 / Atomic validation failure stops iteration**：不进入 Phase 3。
6. **主模型可补充 findings / Main model can supplement findings**：当 reviewer 遗漏明显问题时。
7. **Git 隔离强制 / Git isolation is mandatory**：所有工作发生在 `iterate/*` 分支或 worktree；merge/push 为 opt-in（`git.auto_merge` / `git.push_per_round` 默认 `false`），仅在用户显式启用时自动合并并推送，否则保留在迭代分支由人工 review。
8. **完整审计 / Full audit trail**：`.iterate_decisions.md` 记录所有修复、延迟、回滚和重要决策。
9. **验证命令安全 / Validation command safety**：`iterate.config.yaml` 中的 `validation.commands` 由 AI 助手读取后执行。运行时只执行其中**精确配置**的命令（不自行拼装、不基于前缀构造命令），未配置命令的模块跳过；不在其中的命令**直接拒绝，不可通过用户确认绕过**。`validation.command_whitelist` 仅为配置期校验辅助字段，无运行时约束力（与上方"命令白名单"章节保持一致）。
10. **防御式模式仅对增量式编程任务启用 / Defensive mode is for incremental coding tasks only**：`/iterate defensive` 面向"用户让 AI 做正常增量式编程任务"（新增功能、修 bug、重构、接入 API、补测试）。纯审查请用 `review-only`，多轮审查-收敛请用 iterate 模式。
11. **防御式模式不收敛不交付 / No convergence, no delivery**：防御式模式收尾必须跑 `iterate invariant` + 完整 iterate 闭环（9 维度审查 → 修复 → 验证 → 收敛）；任一未解决 findings 或 `invariant` 不通过时**不得交付**，必须继续修复直到收敛（硬约束，prompt 层不可绕过，CLI 校验兜底）。
12. **防御式校验以 CLI 为唯一事实源 / CLI is the single source of truth**：`iterate guard pre-check` / `guard post-check` / `invariant` 的结果（退出码）是防御式模式下"能不能开工 / 改得对不对 / 能不能交付"的**唯一判定依据**；prompt 仅作引导。宿主 AI 不得在 CLI 返回 FAIL 时以口头理由继续推进。
