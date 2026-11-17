---
name: mcp-server-audit
version: "1.1.0"
homepage: https://github.com/z-Zihan/awesome-skills
allowed-tools: Read, Grep, Glob, Bash(python3:*)
description: >
  MCP Server 配置安全审计器。把本机各宿主(Claude Code / Codex / Cursor / Windsurf /
  项目级 .mcp.json)的 MCP server 配置集中采集,对每个 server 确定性标记风险形态
  (shell 包装执行 / 包管理器拉取远端代码 / 凭据写进 URL / 明文 HTTP / 环境变量
  暴露面 / 命令注入痕迹),再由 Agent 结合部署语境逐条做暴露面分析,输出分级清单
  与加固建议。审查的是「配置给了 Agent 什么能力」,不是 server 的代码质量。
  触发词: MCP 审计, MCP 安全, 检查 MCP 配置, MCP server 审查, mcp 配置体检,
  mcp 风险, mcp audit, mcp security review, check mcp servers, mcp config review,
  mcp server 检查, 审查工具权限。
  激活条件: 用户给出 MCP 配置语境(要求检查/审计 MCP server、配置文件路径,
  或询问某个 MCP server 是否安全);与 MCP 无关的通用安全审查不触发。
  NOT for: Skill 质量评审(用 skill-review-pro)、代码质量评审(用
  code-review-ProMax)、交付覆盖审计(用 delivery-spec-audit)、server 代码
  漏洞挖掘(需要运行 server,本 skill 只读配置不执行任何 server)。
---

# mcp-server-audit — MCP Server 配置安全审计器

## 语言规则

**检测用户使用的语言，全程使用同一语言输出。** 中文用户 → 读下方中文部分，全中文输出；English users → read the English section below, output in English only. 技术术语（MCP、stdio、env 等）保留原文即可。

---

# 中文版

## 核心定位

你审计的对象是「MCP 宿主配置给了 Agent 什么能力」。每接入一个 MCP server，
Agent 就获得了一批新工具——每个 stdio server 本质上是一条**宿主替你执行的任意命令**，
每个远程 server 是一条**带凭据的出站连接**，而所有 server 的工具描述（tools 列表）
会全部注入模型上下文。配置错了或配多了，攻击面随之扩大。

设计依据 MCPHallu（arXiv:2611.07689）的两个实测结论：其一，正确工具一旦与语义
重叠的混淆工具混用，任务通过率从 84.7% 跌到 32.3%——暴露面不只是被恶意利用才
有害，它本身就制造失败；其二，工具误用型失败在接入能力越多的环境里越常见。
所以本 skill 的立场是**最小能力集**：审出「用不到但配着」的 server 与「给得过宽」
的权限，和审出「明显危险」的配置同等重要。

## 什么时候用

- 用户问「我的 MCP 配置安全吗 / 帮我检查一下 MCP servers」；
- 接入新 server 前，用户想评估它的配置风险；
- 用户排查「Agent 为什么能做某件事」时，需要确认某个 server 暴露了什么；
- 用户拿到一份别人的 MCP 配置文件（json/toml），想审查后再采用。

## 执行流程

### 第一步：采集证据（跑脚本，不要跳过）

```bash
python3 collect_mcp.py                  # 扫描本机全部已知宿主
python3 collect_mcp.py --repo /path     # 额外扫项目级 .mcp.json
python3 collect_mcp.py --json-file x.toml  # 审查显式给出的配置文件
```

脚本只读配置、不执行任何 server、不发起网络请求；env 与 header **只输出键名
和有无值，绝不输出值本身**。输出 JSON 的每个 server 含：transport、command/args/
url、env_keys、header_keys、flags（确定性风险标记）。

### 第二步：逐条暴露面分析（语义判断层）

对每个 server 回答四个问题，判断依据只来自第一步的证据和用户补充的语境：

1. **执行了什么**：command 直接是二进制，还是经 shell 包装（`shell_interpreter`）？
   包管理器拉取（`package_runner_fetched` + `auto_yes_install`）意味着**每次启动
   都在拉取并执行远端代码**——远端包一变，你的机器就执行新代码。
2. **连到哪里**：远程 server 的 URL 是否带凭据（`credential_in_url`——凭据会进
   日志和代理）、是否明文 HTTP（`plain_http`）；stdio server 的路径是绝对路径
   还是相对 `cwd`（`cwd: "."` 意味着行为随启动目录变化）。
3. **暴露了什么**：env_keys 里出现 TOKEN/KEY/PASSWORD/SECRET 类键名，说明该
   server 进程能读到这些凭据；header_keys 同理。键名 + has_value 就够判断，
   **不要**要求用户提供值，也不要把值写进任何输出。
4. **是否真的在用**：让用户确认（或检查会话记录）这个 server 的工具最近是否
   被调用过。长期未用的高权限 server 是纯负债——MCPHallu 数据显示多余的工具
   本身就拖累任务表现。

风险分级（结合语境，不是机械套用）：

- **P0 处理**：凭据在 URL 里、pipe 到 shell 执行远端脚本、来源不明的二进制
  + 敏感 env 组合。建议立即下线或改造。
- **P1 尽快**：`npx -y`/`uvx` 无版本 pin 的包运行器、明文 HTTP、shell 包装
  执行拼接命令。建议 pin 版本、换 HTTPS、显式列出命令。
- **P2 规划**：cwd 相对路径、env 键名敏感但语境可信、同类 server 重复接入
  （语义重叠，MCPHallu 的混淆工具问题）。
- **P3 记录**：长期未用（用户确认后）、scope 大但权限窄。

### 第三步：输出审计报告

输出格式（用表格 + 分级清单，不写空话）：

1. **总览**：扫了哪些宿主、几个 server、几个带 flags、几个解析失败（解析失败
   本身要报告——配置文件损坏或格式漂移）。
2. **逐 server 条目**：名称 / 宿主 / scope / transport / flags / 四问结论 / 风险级。
3. **加固清单**：按优先级列出可执行的具体改法（改哪个文件的哪一段、pin 什么
   版本、删哪个 server），每条注明影响（会失去什么能力）。
4. **明确没查什么**：只审了配置层；server 实现代码漏洞、运行时行为、返回内容
   的注入风险都不在覆盖范围——不要给出超出证据的结论。

## 首个真实审计案例（v1.1.0 回填，本机实测）

2026-11-10 在作者本机（macOS，Codex 宿主）跑了一次完整审计，作为流程示范：

**采集结果**：扫到 2 个 stdio server（`computer-use`、`node_repl`），0 个带 flags，0 个 parse_error。

**四问分析**（逐条给证据，不凭名字联想）：

| server | 执行了什么 | 连到哪里 | 暴露了什么 | 是否在用 |
|---|---|---|---|---|
| computer-use | 相对路径 `./Codex Computer Use.app/.../SkyComputerUseClient`——行为随启动目录变化（cwd: "."），非 shell 包装、非包运行器 | 本地 stdio，无 URL | env_keys 空 | 需用户确认 |
| node_repl | `/Applications/ChatGPT.app/...` 绝对路径二进制，args 空 | 本地 stdio | env_keys 空（宿主 config 里另有 env_vars 传递管道路径，属进程间通信配置而非凭据） | 需用户确认 |

**分级与结论**：两者均无 P0/P1 形态。值得记录的两条 P2/P3：computer-use 的相对路径 + `cwd: "."` 意味着从不同目录启动 Codex 时该 server 可能静默失效或行为漂移（P2，改绝对路径即可消除）；node_repl 是 ChatGPT.app 自带组件，随应用更新变化，固定在宿主审计清单里定期复查（P3）。加固清单为空——没有需要立即处理的项目，这份「无事」报告本身就是审计的有效产出。

**值得注意的负样本价值**：这个案例展示了两件容易做错的事。其一，`flags: []` 不等于「分析结束」——相对路径风险是四问分析（第二步）而非确定性 flags（第一步）才暴露的；其二，env 键名为空也要看宿主原配置里的相邻字段，本例 Codex config 的 `env_vars` 数组不是凭据而是运行时参数，审计报告里写清「看了、确认不是暴露面」比略过更有说服力。

## 异常情况

- **脚本输出 parse_error**：该宿主配置文件存在但解析失败。如实报告文件路径与
  错误，请用户确认格式；不要猜。
- **用户只给了一段配置文本**：让用户存成文件后用 `--json-file` 审，或直接对
  该文本做第二步的语义分析（跳过脚本，注明「未走确定性采集」）。
- **Python < 3.9**：脚本用了 f-string 与 pathlib，无 3.8 以下兼容承诺；如实报错。
- **不存在的宿主**：脚本自动跳过（输出里不会出现），不算错误。

## 验收标准

- 报告覆盖脚本采到的**每一个** server，无遗漏；flags 每一项都有解释。
- 所有风险判断都能指向具体证据字段（command/args/url/env_keys/flags），
  不凭 server 名字联想。
- env/header 的**值**不出现在报告的任何位置。
- 加固建议可执行：写明改哪个文件、改成什么，以及代价。
- 报告末尾有「未覆盖范围」声明。

## 使用限制

- 本 skill **不执行**任何 MCP server，不验证 server 能否启动；配置「看起来合理」
  不代表 server 可用，可用性属于用户自己的冒烟测试。
- 只覆盖 Claude Code / Codex / Cursor / Windsurf 四个宿主的项目级与用户级配置；
  其他宿主（VS Code 扩展、自研宿主）请用户提供配置文件走 `--json-file`。
- TOML 解析是子集实现（覆盖 `[mcp_servers.name]` 形态），内联表、多行字符串
  等 TOML 特性不支持——遇到会输出 parse_error 而不是错解析，此时请用户改用
  标准 TOML 工具导出 JSON 后再审。
- scope 判定以配置文件位置为准，不追踪宿主实际的 profile 继承链。

---

# English Version

## Core Positioning

You audit **what capabilities MCP host configs grant to the Agent**. Every stdio
server is an arbitrary command the host executes for you; every remote server is
an outbound connection carrying credentials; every server's tool descriptions get
injected into model context. Bad or excessive config widens the attack surface.

Design rationale from MCPHallu (arXiv:2611.07689): mixing a correct tool with
semantically-overlapping confusion tools drops pass rate from 84.7% to 32.3% —
exposure hurts even without an attacker. This skill enforces **least capability**:
unused-but-configured servers and over-broad grants matter as much as obviously
dangerous ones.

## When to Use

- "Is my MCP config safe?" / "check my MCP servers";
- Evaluating a new server's config before onboarding;
- Explaining "why can the Agent do X" via config evidence;
- Reviewing someone else's MCP config file (json/toml) before adopting it.

## Workflow

### Step 1: Collect evidence (run the script)

```bash
python3 collect_mcp.py                  # scan all known hosts
python3 collect_mcp.py --repo /path     # also scan <repo>/.mcp.json
python3 collect_mcp.py --json-file x.toml  # audit an explicit config file
```

Read-only: never executes servers, never sends network requests; env/header
**values are redacted** (key names + has_value only). Output JSON per server:
transport, command/args/url, env_keys, header_keys, flags.

### Step 2: Per-server exposure analysis (semantic layer)

For each server answer four questions:

1. **What executes**: direct binary vs shell wrapper (`shell_interpreter`)?
   Package runners (`package_runner_fetched` + `auto_yes_install`) pull and run
   remote code **on every launch** — upstream changes, you execute them.
2. **Where it connects**: credential in URL (`credential_in_url` — leaks into
   logs/proxies), plain HTTP (`plain_http`); relative `cwd` makes behavior
   directory-dependent.
3. **What it exposes**: TOKEN/KEY/PASSWORD/SECRET-shaped env_keys mean the
   server process can read those credentials. Key names + has_value suffice —
   **never** ask for or output values.
4. **Is it actually used**: confirm with the user (or session logs). Long-unused
   high-privilege servers are pure liability; MCPHallu shows extra tools alone
   degrade task performance.

Risk tiers (context-dependent, not mechanical):

- **P0 now**: credential in URL, pipe-to-shell remote scripts, unknown binaries
  with sensitive env. Take offline or restructure immediately.
- **P1 soon**: unversioned `npx -y`/`uvx`, plain HTTP, shell-wrapped command
  concatenation. Pin versions, use HTTPS, list explicit commands.
- **P2 plan**: relative cwd, sensitive-but-trusted env keys, duplicate servers
  covering the same semantics (MCPHallu's confusion-tool problem).
- **P3 note**: long unused (after user confirms), wide scope but narrow grant.

### Step 3: Deliver the audit report

1. **Overview**: hosts scanned, server count, flagged count, parse failures
   (report parse errors explicitly — corrupted config or format drift).
2. **Per-server entries**: name / host / scope / transport / flags / four-answer
   conclusions / risk tier.
3. **Hardening list**: executable fixes (which file, which block, pin what,
   remove which server), each noting the capability cost.
4. **Explicit non-coverage**: config layer only; server code vulns, runtime
   behavior, response-content injection are out of scope — do not exceed evidence.

## First Real Audit (backfilled in v1.1.0, tested on the author's machine)

A full audit run on 2026-11-10 (macOS, Codex host), as a worked example:

**Collection**: 2 stdio servers (`computer-use`, `node_repl`), 0 flagged, 0 parse errors.

**Four-question analysis** (evidence-based, no name-based guessing):

| server | What executes | Where it connects | What it exposes | Actually used? |
|---|---|---|---|---|
| computer-use | relative path `./Codex Computer Use.app/.../SkyComputerUseClient` — behavior varies with launch directory (cwd: "."), not shell-wrapped, not a package runner | local stdio, no URL | env_keys empty | user to confirm |
| node_repl | absolute-path binary under `/Applications/ChatGPT.app/...`, no args | local stdio | env_keys empty (host config has a separate `env_vars` array carrying pipe paths — inter-process plumbing, not credentials) | user to confirm |

**Tiers and verdict**: no P0/P1 shapes on either server. Two recorded findings: computer-use's relative path + `cwd: "."` means the server may silently fail or drift depending on where Codex is launched (P2 — fixed by using an absolute path); node_repl ships with ChatGPT.app and changes with app updates (P3 — keep it on the periodic audit list). The hardening list is empty — and a clean "nothing urgent" report is a valid audit outcome.

**Negative-sample lessons**: two things this case shows are easy to get wrong. First, `flags: []` does not mean "analysis done" — the relative-path risk only surfaced at the semantic layer (Step 2), not the deterministic flags (Step 1). Second, empty env keys do not excuse skipping adjacent host config fields: this Codex config's `env_vars` array turned out to be runtime plumbing rather than secrets, and stating "checked, not an exposure" in the report is more convincing than silence.

## Error Handling

- **parse_error in output**: the host's config exists but failed to parse.
  Report path + error verbatim; ask the user to confirm format; do not guess.
- **User pastes config text**: save to a file and use `--json-file`, or run the
  Step-2 semantic analysis directly on the text (note "deterministic collection
  skipped").
- **Python < 3.9**: not supported; report honestly.
- **Missing hosts**: skipped silently — not an error.

## Acceptance Criteria

- Every server from the script appears in the report; every flag is explained.
- Every risk judgment cites a concrete evidence field, never name-based guessing.
- env/header **values** never appear anywhere in the report.
- Hardening fixes are executable: file, change, and cost.
- The report ends with a non-coverage statement.

## Limitations

- This skill **never executes** MCP servers or verifies they start; config
  plausibility ≠ server usability — that is the user's smoke test.
- Covers Claude Code / Codex / Cursor / Windsurf (user + project scope); other
  hosts: ask the user for their config file and use `--json-file`.
- TOML parsing is a subset (covers `[mcp_servers.name]` shape); inline tables
  and multiline strings are unsupported — surfaces as parse_error, never as a
  wrong parse. Ask the user to export JSON via a standard TOML tool in that case.
- Scope is determined by config file location; host profile inheritance chains
  are not tracked.
