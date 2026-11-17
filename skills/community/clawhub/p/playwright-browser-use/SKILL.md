---
name: playwright-browser-use
description: 浏览器自动化 CLI（Playwright 版，纯 Node.js 实现）。除常规自动化（打开网页/截图/点击/填表/翻页）外，提供三类能力：(1) 会话凭证读写原语 —— `cookies` / `storage` 命令可**无需代码执行**即列出/导出/导入/清除/设置 cookie 与 localStorage，直接提取或注入登录态与会话令牌（此路径独立于代码执行；自 v1.3.2 起 `PW_BROWSER_SAFE_MODE=1` 会将其与代码执行一并禁用）；(2) `eval` 在页面上下文执行任意 JavaScript（可读 cookie/存储、发起带凭证请求）；(3) `run-code` 在守护进程上下文执行 Playwright/Node 代码（vm 沙箱隔离）。全部经持久化本地守护进程（127.0.0.1:19223，浏览器状态跨命令保持）控制，受随机 token 认证保护；`PW_BROWSER_SAFE_MODE=1` 可彻底禁用代码执行与 cookies/storage 凭证读写（v1.3.2+）。仅在可信、用户可见的本地环境中授权使用；会话凭证落盘须遵循后文安全警告。
allowed-tools: Bash(node:*), Bash(pw-browser:*), Bash(curl:*)
capabilities:
  - "code-execution: page-context (eval — arbitrary JS in current page)"
  - "code-execution: daemon-vm (run-code — null-prototype VM sandbox, no host fs/process)"
  - "network: arbitrary via browser/page context (credentialed requests possible)"
  - "browser-state: persistent credentialed session across commands"
  - "credential-access: direct read/export/import/clear/set of cookies & localStorage (session tokens) — no code execution needed; gated by daemon token, and fully DISABLED by PW_BROWSER_SAFE_MODE=1 (v1.3.2+)"
  - "file: write to local disk (run-code can trigger downloads; cookies/storage export writes credential files)"
# --- Formal permission model (machine-readable) -------------------------
# NOTE: This skill has NO built-in fine-grained permission system. The
# fields below are declarative metadata for orchestrators/reviewers, NOT
# an enforcement boundary. Real constraints come only from:
#   - daemon token auth (gates NETWORK reachability, not per-capability)
#   - PW_BROWSER_SAFE_MODE=1 (disables code-exec + credential primitives)
#   - export/import path confinement to ~/.pw-browser (v1.3.1+); since v1.3.8
#     the caller-supplied --unsafe flag alone can NOT lift it — the operator
#     must also start the daemon with PW_BROWSER_ALLOW_UNSAFE_CRED_PATH=1
#   - PW_BROWSER_CRED_PERSIST=off (v1.3.9) removes credential persistence only
#     (export/import), keeping in-memory cookie/storage automation usable
# "capabilities" lists the MINIMUM attack surface, not a maximum; the skill
# can additionally drive any site the browser can reach, including ones where
# the user is already authenticated. Least privilege is achieved at the
# orchestration layer via deploy mode (safe mode + sandbox) + scoped ops.
permissions:
  model: "none-formal"          # no built-in RBAC / capability-dropping
  enforcement:
    - "daemon-token"            # gates network reachability to 127.0.0.1:19223
    - "safe-mode-env"           # PW_BROWSER_SAFE_MODE=1 disables code-exec + creds
    - "path-confinement"        # cookies/storage IO limited to ~/.pw-browser
    - "operator-gated-override" # lifting confinement needs daemon env, not a caller flag
    - "cred-persist-killswitch" # PW_BROWSER_CRED_PERSIST=off blocks export/import only
    - "secret-file-permissions" # daemon token + credential dumps written 0600, dir 0700
    - "download-name-sanitised" # page-supplied download filename forced to a basename inside --path
  least-privilege:
    default-mode: "full"        # full power; requires trusted, user-visible, local
    scoped-mode: "cred-persist-off"      # PW_BROWSER_CRED_PERSIST=off — keeps automation,
                                         # removes the privilege-persistence primitive
    reduced-mode: "safe-mode"   # PW_BROWSER_SAFE_MODE=1 — for not-fully-trusted agents
    untrusted-mode: "safe-mode+sandbox"  # add network isolation for untrusted input
  metadata-is: "attack-surface-description"  # NOT a grant, NOT a sandbox boundary
disable: false
---

# 浏览器自动化 — Playwright 版（`pw-browser`）

> `pw-browser` 是基于 playwright-core（Playwright 核心库）的浏览器自动化 CLI，仅依赖 Node.js 和 playwright-core，无需下载任何浏览器。
>
> ⚠️ **完整能力（含代码执行）**：本工具**不只是"点开网页"**——它包含 `eval`（页面上下文**任意 JavaScript** 执行）与 `run-code`（守护进程上下文执行 Playwright/Node 代码）两项代码执行能力，并通过**持久化本地守护进程**控制浏览器状态（状态跨命令保持）。所有代码执行均受 daemon token 认证保护，可用 `PW_BROWSER_SAFE_MODE=1` 彻底禁用。请先阅读下方「⚠️ 安全边界与使用场景」了解完整攻击面与适用边界，再决定是否授权。

## ⚠️ 安全边界与使用场景

本工具为 **本地 AI 助手对话环境**设计，运行在用户完全可视、可中断的场景中。

| 场景 | 风险 | 说明 |
|------|------|------|
| AI 助手对话交互（推荐） | 🟡 低 | 用户全程可见浏览器操作，可随时中断 |
| 本地开发/测试 | 🟡 低 | 在受控环境中操作测试页面 |
| 手动触发的数据采集 | 🟡 低 | 用户明确指定的页面和操作 |

以下场景 **不推荐**直接使用，需要额外安全措施：

| 场景 | 风险 | 需要的额外措施 |
|------|------|-------------|
| 被不可信 agent 调用 | 🔴 高 | 已内置 daemon token 认证 + 可选 `PW_BROWSER_SAFE_MODE` 禁用代码执行与 cookies/storage 凭证原语（v1.3.2+）；若来源仍不可信，应进一步沙箱隔离 |
| 作为公开 API 服务 | 🔴 极高 | 必须加认证 + 操作白名单 |
| CI/CD 自动化流水线 | 🟡 中 | 需限定操作范围，禁止生产环境 |

**核心能力声明：**
- `eval`：在**浏览器上下文**（`page.evaluate`）执行**任意 JavaScript**——即完整的页面级代码执行能力。它无法访问 Node.js API（`require`/`fs`/`process`），作用域仅限于当前页面；但正因如此，它能读取 `document.cookie`/`localStorage`/`sessionStorage`、发起**带页面凭证的 `fetch` 请求**、操控 DOM 并触发页面内动作（点击、提交等）。**这是与 `run-code` 同级的"代码执行"能力，仅场景不同（页面 vs Node）**：同样受 daemon token 认证保护，同样在 `PW_BROWSER_SAFE_MODE=1` 下被禁用；只在用户明确指定、且页面可信时使用，不对高权限/来源不明页面执行
- `run-code`：在 daemon 进程的**受限沙箱**（`vm` 模块）中执行 Playwright 代码，仅暴露 `page` 和安全 JS 全局；**无法直接调用** `fs`/`child_process`/`process`/`require`。但浏览器上下文可经 `download.saveAs`/`setInputFiles` 在本地磁盘读写文件、能发起任意网络请求（沙箱不阻止）。它仍拥有完整浏览器控制权（导航、读写存储、下载、提交表单、改页面内容），**仅限本地信任环境使用**
- `cookies` / `storage`：**独立的会话凭证读写原语**，无需任何代码执行即可对 cookie 与 `localStorage` 做 `list` / `export` / `import` / `clear` / `set`。它可直接**提取**当前登录态（含 `HttpOnly` cookie、会话/Bearer 令牌、CSRF token），也可**注入**任意攻击者控制的状态，是凭据盗窃与账户接管的**独立高危面**——**不依赖** `eval` / `run-code`。普通模式下仅由 daemon token 认证保护；自 v1.3.2 起 `PW_BROWSER_SAFE_MODE=1` 会**整体禁用**全部 `cookies` / `storage` 子命令（与 eval/run-code 同级拦截）。落盘会话文件的处置见下方「会话持久化风险（Rogue Agent）」块：务必用完即删、不跨环境/账号复用。`export`/`import` 默认**限制在 `~/.pw-browser/` 目录内**以防凭证散落或加载外部攻击者构造文件；自 v1.3.8 起该限制**不可由调用方自行解除**——越界需**同时**满足「操作者以 `PW_BROWSER_ALLOW_UNSAFE_CRED_PATH=1` 启动 daemon」+「调用方显式传 `--unsafe`」，否则返回 `UnsafeOverrideNotPermitted`
- daemon：监听 `127.0.0.1:19223`，仅本机可访问，不暴露到公网；**所有命令（除 `/health` 存活探针）均要求随机 `token` 认证**，token 在 daemon 启动时生成并写入 `~/.pw-browser/daemon.json`（默认仅当前用户可读），CLI 自动携带，外部进程无法在未读取该文件的情况下调用
- 安全模式：设置环境变量 `PW_BROWSER_SAFE_MODE=1` 启动 daemon 可**彻底禁用** `run-code` / `eval` **以及全部 `cookies` / `storage` 凭证原语**（v1.3.2+），仅保留 snap/click/fill 等白名单命令，适合不需要自定义代码、也不该触碰会话凭证的场景（如接入来源不完全可信的 agent）
- 非 headless 模式：浏览器窗口始终可见，用户可直接监控所有操作
- 文件下载：通过 `run-code` 触发页面下载（`download.saveAs`）会写入本地磁盘，注意目标路径
- 下载文件名消毒（v1.3.10+）：`download` 命令的建议文件名由**被自动化的网页**决定而非操作者。当 `--path` 指向**目录**时，该名字会被强制取 `basename` 并校验解析后仍位于该目录内，越界返回 `PathTraversal`；恶意站点无法再用 `../../.bashrc` 之类的名字把文件写到目录之外。若 `--path` 显式指向一个**文件路径**，则按操作者意图原样使用

## 🔐 权限模型与最低特权（形式化说明）

> **关键澄清：`capabilities` 是攻击面描述，不是权限授予，也不是沙箱边界。**
> frontmatter 里的 `capabilities` / `allowed-tools` 是给编排者与审核者的**自由文本元数据**：
> - `capabilities` 列出的是本技能**能够做什么**（即真实攻击面的最小集合），**不代表**它被限制在这些能力内、也**不代表**它已获授权——拥有某项能力意味着技能*可以*行使它，而非*只能*行使它。
> - `allowed-tools` 仅声明技能可调用哪些宿主工具（如 `Bash(node:*)`），**不构成**对技能行为的强制限制；真正的行为约束来自下方"实际执行边界"。
> 审核时请以"攻击面下限"而非"能力上限"来读 `capabilities`：技能还可驱动浏览器能抵达的**任意站点**，包括用户**已登录**的站点，从而读取/操作该站点的认证状态。

### 分级部署矩阵（最低特权选择）

| 部署模式 | 代码执行 (`eval`/`run-code`) | 凭证原语 (`cookies`/`storage`) | 网络 | 适用场景 | 残余风险 |
|----------|------------------------------|-------------------------------|------|----------|----------|
| **全能力（默认）** | ✅ 开启 | ✅ 开启 | 经浏览器（含带凭证请求） | 可信本地、用户全程可见、临时/演示会话 | 高：可导出/注入会话、可发带凭证请求 |
| **禁凭证落盘** `PW_BROWSER_CRED_PERSIST=off` | ✅ 开启 | ⚠️ 仅内存态（`export`/`import` 返回 `CredentialPersistenceDisabled`） | 经浏览器 | 需要完整自动化能力、但不允许会话状态跨运行留存的长驻 agent | 中高：仍可读取会话内容，但无法把它变成可复用的凭证文件 |
| **安全模式** `PW_BROWSER_SAFE_MODE=1` | ⛔ 禁用 (返回 `Disabled`) | ⛔ 禁用 (返回 `Disabled`) | 仅 `snap`/`click`/`fill` 等白名单命令，不主动发请求 | 接入来源不完全可信的 agent、CI 只读巡检 | 中：仍可访问已打开页面的 DOM/可见内容 |
| **沙箱 + 安全模式** | ⛔ 禁用 | ⛔ 禁用 | 额外做**网络隔离**（禁止出网 / 仅内网白名单） | 完全不可信或第三方输入驱动的自动化 | 低：沙箱逃逸前无法外联或触碰凭证 |

**最低特权原则**：默认按"全能力"部署仅当满足——① 用户全程可见可中断；② 操作对象为用户明确指定的页面；③ 不在已登录高权限账户（银行/邮箱/工单系统）上执行未确认动作。否则应**优先启用安全模式**，并对不可信来源**进一步沙箱隔离**。

### 实际执行边界（技能到底受什么约束）

1. **daemon token 认证**：仅限制*谁能通过网络抵达 daemon*（须持有启动时生成的随机 token）。一旦本地进程持有 token，**所有能力全部可用**——token 是"门禁"而非"按能力细分的权限"。
2. **安全模式（v1.3.2+）**：本技能**唯一内建的能力开关**，整体禁用代码执行与 `cookies`/`storage` 凭证原语；它是降低攻击面的主开关，但不是沙箱。
3. **路径限制 + 操作者门禁（v1.3.1 / v1.3.8）**：`cookies`/`storage` 的 `export`/`import` 默认被限制在 `~/.pw-browser/` 内（符号链接经 realpath 解析，无法用软链逃逸）。**解除权归属操作者而非调用方**：越界须同时满足「daemon 以 `PW_BROWSER_ALLOW_UNSAFE_CRED_PATH=1` 启动」+「调用方显式 `--unsafe`」；仅传 `--unsafe` 会被拒（`UnsafeOverrideNotPermitted`），因为调用方不能修改 daemon 进程的环境变量。这只约束落盘位置，不约束浏览器内的读/写行为。每次凭证路径访问都会写入 daemon stderr 审计行。
4. **凭证持久化开关（v1.3.9）**：`PW_BROWSER_CRED_PERSIST=off` 启动 daemon 可**单独禁用** `cookies`/`storage` 的 `export`/`import`（返回 `CredentialPersistenceDisabled`），而 `list`/`get`/`set`/`clear` 等内存态操作照常可用。它比安全模式**粒度更细**：只切断"会话状态落盘"这一条特权持久化路径，保留正常自动化能力。同样是进程环境变量，调用方无法解除。
5. **落盘文件权限（v1.3.9）**：`~/.pw-browser/` 以 `0700` 创建，daemon 认证 token（`daemon.json`）与导出的凭证文件均以 `0600` 写入（已存在的旧文件会被 chmod 收紧）。这防止**同机其他本地用户**读走 token 接管浏览器、或直接读取导出的会话。注意：POSIX 权限位在 Windows 上不由操作系统强制执行，Windows 下依赖用户目录的 ACL 继承。
6. **宿主工具策略**：`allowed-tools` 由宿主平台在*调用层*决定是否放行技能发起的工具调用；它依赖平台实现，**不保证**能限制技能在已获准工具内的具体行为（例如在 `Bash(node:*)` 内仍可执行任意 Node 代码）。

> 结论：本技能**没有**独立于上述六点的"形式化权限系统"。任何"最小权限"诉求都必须通过**部署模式选择（安全模式/沙箱）+ 操作范围约定**在编排层落实，而非依赖技能元数据自证安全。

## 📝 文档语言与本地化说明

- **文档语言**：本技能文档为**简体中文**。若你或下游 agent 的默认语言非中文，请以代码块中的命令、URL、CSS 选择器与 `snap` 返回的 `ref` 为准——这些是**与语言无关**的自动化锚点。
- **界面文本匹配是启发式的**：识别分页 / 按钮类型时，文档列出的中文、英文关键词（如"下一页"/"Next"、"更新"/"保存"/"发布"）只是**识别信号示例，并非穷举**；非中文页面的实际文案会不同。
- **优先用 DOM 锚点，而非可见文字**：跨语言页面请尽量用 `snap` 得到的 `ref` 或 CSS 选择器（`page.locator('.xxx')`）定位元素，避免依赖本地化后的可见文本，以防因文案不同导致误点 / 误操作。
- **适用区域**：技能本身不限定网站区域；文档示例与中文 UI 关键词面向中文环境，各"识别信号"表已并列给出英文界面关键词。
- **英文文档**：面向非中文 agent/用户，提供 [`README.en.md`](./README.en.md)（英文 README）与 [`QUICKSTART.en.md`](./QUICKSTART.en.md)（英文端到端示例）。`SKILL.md` 本身保持中文，但其内的命令、URL、CSS 选择器、`snap` 返回的 `ref` 均为语言无关锚点，非中文 agent 可直接据此执行。

## 前置条件（首次使用）

本 Skill 所在目录需已执行 `npm install`（将安装 `playwright-core`）。**无需单独下载浏览器** — daemon 启动时自动检测并使用系统的 Chrome 或 Edge。

> 下文所有命令中的 `{SKILL_DIR}` 请替换为实际的 skill 安装目录路径。

## 架构

`pw-browser` 采用 daemon + client 架构：

```
┌──────────────┐     HTTP (localhost:19223)     ┌──────────────┐
│  pw-browser  │ ──────────────────────────────→│   Daemon     │
│  (CLI 客户端) │                                │  (浏览器进程)  │
└──────────────┘                                └──────┬───────┘
                                                       │
                                                       ├─ Playwright
                                                       ├─ Chromium 浏览器
                                                       └─ 页面状态持久化
```

**daemon 启动后持续运行**，浏览器和页面状态跨命令保持。CLI 每次通过 HTTP 调用 daemon。

## 启动 Daemon

**每次会话开始前**，在后台启动 daemon。以下命令使用 Skill 所在目录的绝对路径和 shim 脚本：

```bash
SKILL_DIR="{SKILL_DIR}"
NODE_PATH="${SKILL_DIR}/node_modules" node "${SKILL_DIR}/pw-browser.js" daemon &
sleep 4
```

> daemon 会在 `127.0.0.1:19223` 监听，首次启动会用 Playwright 的 `channel: 'chrome'` 自动连接系统 Chrome 浏览器（如已安装了 Edge 也会尝试）。无需下载额外的 Chromium。

验证 daemon 可用：

```bash
SKILL_DIR="{SKILL_DIR}"
NODE_PATH="${SKILL_DIR}/node_modules" node "${SKILL_DIR}/pw-browser.js" init
```

**关闭 daemon：**

```bash
pw-browser close --all
```

## 核心工作流

> **注意**：下面所有 `pw-browser` 命令都需要设置 `NODE_PATH`。Agent 执行时应使用完整形式：
> ```bash
> SKILL_DIR="{SKILL_DIR}"
> NODE_PATH="${SKILL_DIR}/node_modules" node "${SKILL_DIR}/pw-browser.js" <cmd> [args] [--json]
> ```
> 为简洁起见，下文示例省略前缀，用 `pw-browser` 表示。

```bash
# 1. 启动 daemon（会话开始一次）
pw-browser daemon &

# 2. 打开页面
pw-browser open https://www.baidu.com

# 3. 获取页面快照（必须！每次交互前都要 snap）
pw-browser snap

# 4. 交互 — 基于快照中的 e0, e1, e2... ref 引用
pw-browser click e8          # 点击 ref=e8 的元素
pw-browser fill e5 "hello"   # 在 ref=e5 的输入框填入文本
pw-browser press Enter       # 键盘按键

# 5. 等待
pw-browser wait-for "text=加载完成" --timeout 8000
pw-browser wait-for "url:https://example.com/*"
pw-browser wait-for "state:networkidle"

# 6. Tab 管理
pw-browser tab list
pw-browser tab select 1
pw-browser tab close 0

# 7. 关闭
pw-browser close             # 关闭当前页面
pw-browser close --all       # 关闭浏览器 + daemon
```

## 语义规则（必须遵守）

### 规则 1：先观察再操作

CLI **不会**在 open/click 后自动获取快照。**以下情况必须执行 `pw-browser snap`**：

- **每次 `open` / `goto` / `go-back` / `go-forward` / `reload` 之后**（页面已变更）
- **每次点击可能触发导航的元素之后**（链接、提交按钮等）
- **首次进入陌生页面时**

**同一页面内连续操作**（click → fill → press → click）可复用已获取的 ref，无需每步 snap。

```
正确: pw-browser open URL → pw-browser snap → pw-browser click e5 → pw-browser fill e8 "text"
错误: pw-browser open URL → pw-browser click e5（open 后缺 snap）
正确: pw-browser snap → pw-browser click e5 → pw-browser click e7（同一页面连续操作，ref 稳定）
错误: pw-browser snap → pw-browser click e5 → pw-browser snap → pw-browser click e5（同一页面内多余 snap）
```

> ⚠️ **何时必须重新 snap：** 页面发生导航（URL 变化、新页面打开）、或 `act` 命令返回了 `interrupted`（DOM 已被修改）。此时旧 ref 可能指向错误元素，必须 re-snap 获取最新快照。

### 规则 2：点击链接后处理导航

点击可能触发导航的链接（`<a>` 标签、按钮等）后：
1. `pw-browser snap` — 检查页面是否已变化
2. 如有新 tab → `pw-browser tab list` → `pw-browser tab select <idx>`
3. `pw-browser snap` — 获取新页面内容

### 规则 3：页面内容不全

如果快照中元素不全（列表不完整等）：
- `pw-browser mousewheel 0 500` 滚动
- 或点击"加载更多"/"下一页"
- 重新 `pw-browser snap`

### 规则 4：登录与验证码（人机协作）

pw-browser 使用非 headless 模式打开实体 Chrome 窗口，用户可直接看到并操作浏览器。遇到需要人工介入的认证场景时，**不要用 `fill`/`click` 盲目尝试**，应按以下流程交接：

#### 触发条件

从 `snap` 中发现以下任一信号时，启动人工协作流程：

- 页面 title 为「登录」/「Login」/「Sign In」
- 页面 `url` 包含 `/login`、`/auth`、`/signin`
- 快照中出现「登录」按钮 + 用户名/密码输入框
- 快照中出现「验证码」「短信验证」「扫码登录」「滑块验证」等关键字
- `open` 后自动跳转到登录页（URL 变化）

#### 协作流程

```
第1步：通报用户
  告知当前页面需要登录/验证，简明描述页面内容（输入框、验证码类型等）

第2步：询问凭据（可选）
  如果用户无凭据 → 跳过，直接等用户操作
  如果用户提供凭据 → 用 fill/click 填入账号密码，点击登录按钮

第3步：等待用户完成验证
  明确告诉用户"请在浏览器中完成验证码/二次验证"
  用户说"好了""完成了""继续"之后才继续

第4步：验证登录状态
  执行 pw-browser snap
  检查是否进入目标页面 → 如果还是登录页，询问用户是否还需要操作
  如果已进入 → 继续自动化流程
```

#### 示例对话

```
Agent: 页面跳转到了登录页 (https://xxx.com/login)，页面上有：
       用户名输入框、密码输入框、登录按钮、滑块验证码。
       需要我帮你填入账号密码吗？还是你在浏览器里自己操作？

User:  我来操作

Agent: 好的，Chrome 窗口已打开 — 请完成登录后告诉我。

User:  好了

Agent: [执行 snap]
       登录成功！当前是「工作台」页面，左侧菜单有...
```

#### 重要约束

- **不猜测凭据**：永远不要尝试默认密码或遍历登录
- **不绕过验证码**：遇到验证码/滑块/短信验证时，立即交给用户
- **不过度等待**：用户说继续后立即 snap，不额外 sleep
- **登录失败回环**：snap 后发现仍在登录页 → 告知用户"看起来还没登录成功，密码错误或验证未通过，请再试试"

### 规则 5：不要主动新建 tab

点击导致新 tab 时用 `tab list/select/close` 处理。没有 `tab new` 命令。

### 规则 6：翻页前读取策略

涉及翻页、统计、收集、遍历时，参考下面的"分页策略"章节。

### 规则 7：不手动读取快照文件

快照通过 `pw-browser snap` 命令获取，不要直接读 `~/.pw-browser/snap.yml`。

### 规则 8：SPA / 富文本编辑器

遇到知识库、文档系统、CMS 等 SPA 页面，参考下面的"SPA 与富文本编辑器"章节。

### 规则 9：daemon 故障恢复

如果 CLI 返回连接错误：

```bash
# 删除旧的 daemon 状态文件
rm -rf ~/.pw-browser/daemon.json
```

**杀掉占用端口 19223 的旧进程：**

```bash
# Windows (PowerShell)
powershell -Command "Get-NetTCPConnection -LocalPort 19223 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id \$_.OwningProcess -Force }"

# macOS / Linux
lsof -ti:19223 | xargs kill -9 2>/dev/null
# 或: fuser -k 19223/tcp 2>/dev/null
```

**重新启动：**

```bash
SKILL_DIR="{SKILL_DIR}"
NODE_PATH="${SKILL_DIR}/node_modules" node "${SKILL_DIR}/pw-browser.js" daemon &
sleep 4
```

---

## 命令速查

### 生命周期
| 命令 | 说明 |
|------|------|
| `pw-browser init` | 连接 daemon，确认浏览器可用 |
| `pw-browser open <url>` | 导航到 URL |
| `pw-browser close` | 关闭当前页面 |
| `pw-browser close --all` | 关闭浏览器 + daemon |
| `pw-browser recover` | 重启浏览器连接 |

### 状态感知
| 命令 | 说明 |
|------|------|
| `pw-browser snap` | 获取页面快照（含 ref 引用）。**ref 在同一页面会话内保持稳定**（同一逻辑元素同 ref）；**每次导航后（新 URL / 新页面）必须重新 snap**，不可复用旧 ref |
| `pw-browser wait-for <target> [--timeout ms]` | 等待条件满足 |

> **Shadow DOM / iframe 支持**：快照会递归进入 **open shadow root** 与 **同源 iframe**，这些元素同样出现在 ref 表中并可直接 `click`/`fill`/`upload`/`drag`。`snap` 输出的 ref 信息带 `inShadow: true`（shadow 内）或 `frameChain`（iframe 链）标记；定位由 `css >>>` 穿透 + `frameLocator` 自动完成，外部 agent 无需关心。`--annotate` 截图仅标注主文档元素（shadow/iframe 元素无法用 xpath 定位标注，但文本快照中仍可点）。跨域 iframe 不可访问，自动跳过。

> **超大页面快照保护**：对元素极多的页面（数万节点），`snap` 默认最多收集 **3000** 个可交互元素，超出即停止收集并在输出标记 `⚠ snapshot truncated`，JSON 返回 `truncated: true`。这是为防止超大型 DOM 拖慢/撑爆快照的兜底；可用环境变量 `PW_BROWSER_SNAP_LIMIT=<N>` 调大上限（设为 `0` 关闭上限，但仍会遍历整棵树），或先交互缩小页面范围再 `snap`。

### 交互
| 命令 | 说明 |
|------|------|
| `pw-browser click <ref>` | 点击元素 |
| `pw-browser fill <ref> "text"` | 填入文本 |
| `pw-browser type "text"` | 键盘输入 |
| `pw-browser press <key>` | 按下按键（Enter, Escape, Tab 等） |
| `pw-browser hover <ref>` | 悬停 |
| `pw-browser select <ref> <option>` | 选择下拉选项 |
| `pw-browser check <ref>` | 勾选复选框 |
| `pw-browser uncheck <ref>` | 取消勾选 |
| `pw-browser upload <ref> <file1> [file2 ...]` | 文件上传（`<input type="file">`，支持多文件，逗号或空格分隔） |
| `pw-browser drag <ref源> <ref目标>` | 拖拽（把源元素拖到目标元素，基于 Playwright `dragTo`） |
| `pw-browser download <ref> [--path dir] [--timeout ms]` | 文件下载（对称于 `upload`）：可选点击 `<ref>` 触发下载，保存到 `--path`（默认当前目录）；也可作为 `act` 动作 `{"action":"download","ref":"eN","path":"/tmp/x.csv"}` |

### 页面导航
| 命令 | 说明 |
|------|------|
| `pw-browser goto <url>` | 同 open |
| `pw-browser go-back` | 后退 |
| `pw-browser go-forward` | 前进 |
| `pw-browser reload` | 刷新 |

### 高级
| 命令 | 说明 |
|------|------|
| `pw-browser screenshot [ref] [--path file] [--annotate]` | 截图；`--annotate` 在可交互元素上叠加与 snap ref 对应的编号框，供多模态 agent 直接读编号定位 |
| `pw-browser mousewheel <dx> <dy>` | 滚动 |
| `pw-browser eval "<expr>" [ref]` | ⚠️ 执行**任意 JavaScript**（页面上下文，完整页面级代码执行：可读 cookie/存储、发起带凭证请求；受 token 认证保护，safe-mode 下禁用）<br>**作用域语义**：不带 `ref` → 表达式在页面全局求值（返回 `scope: "page"`）；带 `ref` → 表达式在该元素上求值，标识符 **`el`** 绑定到对应 DOM 节点（返回 `scope: "element"`），例：`eval "el.textContent" e3`。<br>返回值必须可 JSON 序列化，**不能返回 DOM 节点或循环结构**。 |
| `pw-browser run-code "<code>"` | ⚠️ 执行 Playwright 代码（受限沙箱：无直接 Node fs/process 权限，但可经浏览器下载/上传读写本地文件） |
| `pw-browser dialog-accept [text]` | 确认对话框 |
| `pw-browser dialog-dismiss` | 取消对话框 |

### Tab
| 命令 | 说明 |
|------|------|
| `pw-browser tab list` | 列出所有 tab |
| `pw-browser tab select <idx>` | 切换到指定 tab (0-based) |
| `pw-browser tab close <idx>` | 关闭指定 tab |

### 延时
| 命令 | 说明 |
|------|------|
| `pw-browser sleep <seconds>` | 等待 N 秒 |

### 批量动作与历史（借鉴 browser-use 的 multi-act / 自纠错）
| 命令 | 说明 |
|------|------|
| `pw-browser act '<json>'` | 批量执行动作序列（JSON 数组），如 `[{"action":"fill","ref":"e3","text":"hello"},{"action":"click","ref":"e5"}]`。每步后自动检测 DOM 变化，若页面出现新元素则**中断序列并自动 re-snap** 返回最新快照；失败步附带诊断（元素是否仍存在/相似 ref 建议） |
| `pw-browser history [--limit N] [--clear]` | 查询 daemon 记录的操作历史（每条命令、参数、耗时、结果），`--clear` 清空 |

`act` 支持的动作：`click` / `fill` / `type` / `press` / `hover` / `select` / `check` / `uncheck` / `upload`（对象带 `files: ["/path"]`）/ `drag`（对象带 `target: "eN"`）/ `goto` / `screenshot`，动作对象形如 `{"action":"...","ref":"eN","text":"...","key":"...","option":"...","url":"...","files":["..."],"target":"eN"}`。

---

## 省 Token 用法（默认即高效，别退回 browser-use 的反模式）

本 skill 是**确定性执行器 + 持久 daemon**，大模型（外部 AI）只负责规划、不内嵌在 skill 里。因此**没有「每步都调 LLM」的 token 黑洞**——token 只在外部 AI 主动调用时产生，且完全可控。请保持以下用法以持续省 token：

- **用文本 `snap` 规划，而不是每步截图喂视觉模型**。`snap` 返回的是紧凑的 ref 文本表（`e1 button 提交`），几十 token；`screenshot` 一张图是数百 KB 的 base64，贵 1~2 个数量级。
- **同一页面内复用稳定 ref，不必每步重新 `snap`**（无导航变化时）。同一逻辑元素的 ref 跨多次 snap 保持不变（见上「状态感知」表），外部 AI 可直接拿上一步的 ref 点 `click e1` / `fill e2`。**若页面发生导航（URL 变化、新页面打开），必须重新 `snap`**，不可复用旧 ref。
- **把动作攒成 `act` 一次性发**。登录等一连串操作写成 `[{...},{...}]` 一次调用，daemon 内部自纠错，中间不回模型。理想形态：`1 次 snap → 1 次 act → 完事`。
- **`screenshot --annotate` 是 opt-in**，仅在真有视觉歧义、需要多模态定位时才用；不要默认每步截图。

> ⚠️ 若外部 AI 被 prompt 成「每步都 `screenshot --annotate` 丢给视觉模型」，就会复刻 browser-use 的烧钱循环。token 成本的责任在编排层，不在 skill。

## Cookie 与本地存储（一等命令）

不再需要靠 `eval` 曲线救国，直接用以下命令读写 cookie 与 `localStorage`：

### `cookies`
| 子命令 | 说明 |
|--------|------|
| `pw-browser cookies list` | 列出当前上下文全部 cookie |
| `pw-browser cookies export [--path file]` | 导出 cookie 到 JSON 文件（默认 `~/.pw-browser/cookies.json`） |
| `pw-browser cookies import <file>` | 从 JSON 文件导入 cookie |
| `pw-browser cookies clear` | 清空全部 cookie |
| `pw-browser cookies set <name> <value> [--domain d] [--path p]` | 设置一个 cookie；`--domain` 省略时取当前页面域名 |

### `storage`（localStorage）
| 子命令 | 说明 |
|--------|------|
| `pw-browser storage get [key]` | 读取某个 key（省略 key 则返回全部，以对象形式返回） |
| `pw-browser storage set <key> <value>` | 写入 key/value |
| `pw-browser storage clear` | 清空 localStorage |
| `pw-browser storage export [--path file]` | 导出 localStorage 到 JSON 文件 |
| `pw-browser storage import <file>` | 从 JSON 文件导入（逐 key 写入） |

> ⚠️ `cookies` / `storage` 依赖真实页面源（http/https）。`file://` 与 `data:` 页面不支持 cookie，`localStorage` 行为也不可靠——请先 `open` 一个真实 URL 再操作。

> 🔒 **会话持久化风险（Rogue Agent / 中危）**：`cookies` / `storage` 的 `export` / `import` 让登录态可落盘备份、跨运行恢复——对正常用户是免登录便利，但**在失控或恶意 Agent 场景下，这正是"特权访问持久化"的典型手段**：导出的会话文件等同一份可复用的身份凭证，可被用来跳过认证、长期驻留。缓解：① 导出的会话文件**等同密钥**，用完即 `rm`；暂存请留在 `~/.pw-browser/` 内——自 v1.3.9 起该目录以 `0700` 创建、凭证文件与 daemon token 均以 `0600` 写入（**无需再手工 `chmod`**，旧文件也会被自动收紧；Windows 上 POSIX 权限位不由系统强制，依赖用户目录 ACL）；② **不要**在自动化流程里默认把凭证持久化到磁盘——自 v1.3.9 起这不再只是建议：操作者可用 `PW_BROWSER_CRED_PERSIST=off` 启动 daemon，**强制禁用** `export`/`import`（返回 `CredentialPersistenceDisabled`）而保留 `list`/`get`/`set`/`clear` 内存态操作，在不牺牲自动化能力的前提下切断特权持久化路径；③ 不需要时尽快 `cookies clear` / `storage clear` 并 `pw-browser shutdown` 关闭 daemon，利用空闲自动退出（`PW_BROWSER_IDLE_MS`，默认 15min）缩短凭证在内存中的驻留窗口；④ 对来源不可信的调用方，用 `PW_BROWSER_SAFE_MODE=1` 启动 daemon——自 v1.3.2 起它会**整体禁用**全部 `cookies` / `storage` 子命令（凭证原语与代码执行同级拦截），必要时再配合沙箱隔离或限定操作范围；⑤ **代码层兜底（v1.3.1 / v1.3.8）**：`export`/`import` 默认被限制在 `~/.pw-browser/` 目录内（realpath 解析，软链无法逃逸），从路径层面降低凭证被散落或加载外部攻击者构造文件的可能；且**该限制不可由被约束方自行解除**——越界须由操作者以 `PW_BROWSER_ALLOW_UNSAFE_CRED_PATH=1` 启动 daemon 后、调用方再显式 `--unsafe`，缺一不可，全部访问均写 stderr 审计。详见 QUICKSTART 示例 4 安全提醒。

## Daemon 生命周期（为什么任务结束后浏览器还在）

daemon 是**故意持久化**的：它跨命令持有同一个浏览器实例，避免每次交互都重开 Chrome。因此：

- 你看到「任务结束 Chrome 还在」是正常的——daemon 进程还活着、抱着浏览器。
- **显式停止**：`pw-browser shutdown` 会关掉浏览器并退出 daemon（已加固：即使 `browser.close()` 卡住也会超时兜底退出，不会再退不出/卡客户端）。
- **空闲自动退出**：daemon 默认 **15 分钟无命令** 就自动关浏览器并退出（环境变量 `PW_BROWSER_IDLE_MS` 可改，设为 `0` 关闭该特性）。所以走开后不用手动 `shutdown`，它自己会清理，Chrome 不会一直挂着。
- **监听端口可配 + 冲突避让**：默认 `127.0.0.1:19223`，可用环境变量 `PW_BROWSER_PORT` 覆盖。启动时若目标端口已有 daemon 存活（`/health` 返回 200），当前进程会直接退出（避免双开）；若被其它进程占用（`EADDRINUSE`），则自动递增端口直到可用，并把实际端口写回 `~/.pw-browser/daemon.json`。客户端读取该文件里的端口，无需手动指定。
- **别直接杀进程**：用任务管理器 / `Stop-Process` 强杀 daemon 可能导致浏览器子进程残留（Windows 上 Playwright 的 job object 通常会回收，但不保证）。优先用 `shutdown` 或等空闲自动退出。

---

## 等待策略

`wait-for` 支持多种目标格式：

```bash
# 等待 URL 匹配
pw-browser wait-for "url:**/dashboard"

# 等待文本出现
pw-browser wait-for "text=加载完成"

# 等待页面加载状态（load / domcontentloaded / networkidle）
pw-browser wait-for "state:networkidle"

# 等待 CSS 选择器
pw-browser wait-for ".result-list" --timeout 15000
```

---

## 运行自定义代码（`run-code`）⚠️ 高级功能

> ⚠️ **安全警告：** `run-code` 在 daemon 进程的 **受限沙箱（`vm` 模块）** 中执行 Playwright 代码。它**无法直接调用** Node.js 系统 API（`fs` / `child_process` / `process` / `require`）；但浏览器上下文本身可经下载（`download.saveAs`）或文件上传（`setInputFiles`）在本地磁盘读写文件、并能发起任意网络请求（沙箱不阻止），因此**仍能持久化数据到本地磁盘**。仅在用户明确指定的任务中使用，不要执行来源不明的代码片段。

当内置命令不够用时，用 `run-code` 执行自定义 Playwright 代码：

```bash
# 获取页面标题
pw-browser run-code "return await page.title();"

# 获取页面 HTML
pw-browser run-code "return await page.content();"

# 在页面中执行 JS
pw-browser run-code "return await page.evaluate(() => document.title);"

# 等待网络空闲
pw-browser run-code "await page.waitForLoadState('networkidle');"

# 复杂场景：提取列表数据
pw-browser run-code "
  const items = await page.locator('.product-item').all();
  const results = [];
  for (const item of items) {
    results.push({
      title: await item.locator('.title').textContent(),
      price: await item.locator('.price').textContent()
    });
  }
  return JSON.stringify(results);
"
```

**注意：**
- `run-code` 中直接使用 Playwright Page API
- 代码在 async 函数中执行，`page` 对象已注入
- 返回值自动序列化为字符串
- ⚠️ 此命令可以触发实际的业务操作（提交订单、发送消息、删除数据等），执行前确认用户意图

---

## 分页策略

### 步骤 1：识别分页类型

> ⚠️ 下表关键词为**识别启发式**：中文 / 英文示例（"下一页"/"Next"、"加载更多"/"Load more"）并不穷举，非中文页面的文案会不同。实际定位请优先用 `snap` 的 `ref` 或 CSS 选择器，勿仅依赖可见文本。

从 snap 判断：

| 类型 | 识别信号 | 翻页方式 |
|------|---------|---------|
| **页码分页** | 底部有 1/2/3...页码、"下一页"/"Next"/">" | 点击页码或"下一页" |
| **无限滚动** | 底部无分页控件，内容随滚动增加 | `mousewheel` 滚动 |
| **加载更多** | 底部有"加载更多"/"Load more"/"查看更多" | 点击该按钮 |

### 步骤 2：执行翻页

**页码分页：**
```bash
pw-browser snap                          # 找到"下一页"按钮的 ref
pw-browser click e42                     # 点击
pw-browser sleep 2 && pw-browser snap    # 验证
```

**无限滚动：**
```bash
pw-browser mousewheel 0 800
pw-browser sleep 2 && pw-browser snap
```

**加载更多按钮：**
```bash
pw-browser click <ref>
pw-browser sleep 2 && pw-browser snap
```

### 步骤 3：判断翻页成功

| 方式 | 成功信号 | 失败/结束信号 |
|------|---------|-------------|
| 页码 | 内容更新，URL 变化 | "下一页"按钮 disabled 或消失 |
| 滚动 | 内容增加，新元素出现 | 内容不变，"没有更多了" |
| 按钮 | 新内容加载，按钮仍可点击 | "已加载全部"，按钮消失 |

---

## SPA 与富文本编辑器 ⚠️ 破坏性操作

> ⚠️ **警告：** 以下操作会**真实修改**网页内容（知识库文档、CMS 页面等）。执行前确认当前处于编辑/草稿状态、修改内容已经用户确认。保存/发布操作不可逆。

处理知识库、文档系统、CMS 等 SPA 页面的编辑操作：

### 识别信号

- 点击"编辑"后 URL 不变但按钮变化
- snap 中出现 `contenteditable`、编辑器 toolbar
- 不是普通 `input/textarea`，而是复杂编辑器

### 编辑流程

1. **进入编辑态：** `pw-browser click <编辑按钮的ref>`
2. **验证进入：** `pw-browser snap` — 检查是否出现"更新"/"保存"按钮
3. **写入内容（RTE）：**
```bash
pw-browser run-code "
  const editor = page.locator('[contenteditable=\"true\"]').first();
  await editor.click();
  await page.keyboard.press('Control+A');
  await page.keyboard.type('要写入的内容');
  await page.waitForTimeout(500);
"
```
4. **保存：**
```bash
pw-browser run-code "
  await page.evaluate(() => {
    const btn = Array.from(document.querySelectorAll('button'))
      .find(b => ['更新','保存','发布'].includes(b.textContent.trim()));
    btn?.click();
  });
  await page.waitForTimeout(3000);
"
```
5. **验证：** `pw-browser snap` — 确认保存成功、内容正确

> **不要**直接用 `innerText`/`textContent` 修改 RTE 内容。Playwright 的 `keyboard.type` 和 `fill` 是正确方式。

---

## 结构化输出

所有命令在 daemon 端返回 JSON：

```json
{"ok": true, "data": {...}, "elapsedMs": 123}
{"ok": false, "error": {"kind": "ElementNotFound", "message": "..."}, "elapsedMs": 50}
```

CLI 客户端默认以人类可读格式输出；加 `--json` 标志输出原始 JSON。

## 错误处理

| 错误类型 | 原因 | 处理 |
|---------|------|------|
| `ElementNotFound` | snap 后 ref 已失效 | 重新 snap 获取新 ref |
| `NavigationTimeout` | 页面加载超时 | 先 snap 检查实际状态 |
| 连接拒绝 | daemon 未运行 | 重新启动 daemon |
| 空快照 | 页面未加载完成 | wait-for state:load 后重新 snap |

---

## 完整示例：百度搜索

```bash
SKILL_DIR="{SKILL_DIR}"
PW="NODE_PATH=${SKILL_DIR}/node_modules node ${SKILL_DIR}/pw-browser.js"

# 启动 daemon（首次）
$PW daemon &
sleep 4

# 打开百度
$PW open https://www.baidu.com

# 快照 → 找到搜索框和按钮的 ref
$PW snap
# 例如：e12 = textarea（搜索框），e13 = button（百度一下）

# 填搜索关键词
$PW fill e12 "天气预报"

# 点击搜索
$PW click e13
sleep 2

# 检查搜索结果
$PW snap | head -30

# 清理
$PW close --all
```

---

## 深入参考

| 场景 | 文件 |
|------|------|
| 端到端示例（表单/上传下载/shadow-iframe/cookie/act） | `QUICKSTART.md`（中文）/ `QUICKSTART.en.md`（英文） |
| 翻页策略详解 | `references/pagination.md` |
| 富文本编辑器策略 | `references/rich-text-editor.md` |
| 运行自定义代码 | `references/running-code.md` |
