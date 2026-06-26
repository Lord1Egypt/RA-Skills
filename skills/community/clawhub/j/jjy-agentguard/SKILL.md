---
name: agentguard
description: "AgentGuard security engine — intercept dangerous operations, audit all actions, protect sensitive data. All commands/file/network operations go through ag_* tools for rule engine review. AgentGuard 安全引擎 — 拦截危险操作、审计所有行为、保护敏感数据。所有命令/文件/网络操作通过 ag_* 工具经规则引擎审核后执行。"
homepage: https://www.agentguard.site
user-invocable: true
command-dispatch: tool
command-tool: ag_status
command-arg-mode: raw
metadata: { "openclaw": { "emoji": "🛡️", "requires": { "bins": ["agentguard"] }, "env": { "AGENTGUARD_DAEMON_PORT": { "description": "AgentGuard daemon dashboard port", "default": "19821" } }, "os": ["darwin", "linux"] } }
---

# AgentGuard Security Engine

You now have the **AgentGuard Security Engine** integrated. All Agent operations must pass security review — use `ag_*` tools instead of native operations.

> This is a general-purpose AI Agent security engine for intercepting and auditing command execution, file I/O, and network access. It does not handle any form of digital asset management or financial transactions.

## Security Architecture

AgentGuard provides **four layers of protection** to ensure agents cannot bypass security controls:

1. **Gateway Tool Blocking (L1)** — During setup, `setup.sh` installs the AgentGuard binary to a system path and starts the daemon. Users must manually add `tools.deny` entries to `openclaw.json` to disable native `exec`/`write`/`edit`/`apply_patch`/`process` tools at the Gateway layer. Agents are **physically unable** to call blocked native tools. **Rollback: manually delete the `tools.deny` entries in `openclaw.json` to restore native tools.**
2. **Rule Engine (L2)** — All `ag_*` tool calls are reviewed against command blacklists/whitelists, file path controls, and domain whitelists.
3. **Redaction Engine (L3)** — Automatically filters API credentials, auth tokens, SSH keys, and 15 categories of sensitive information (bidirectional input+output redaction).
4. **Audit Log (L4)** — All operations are logged to local SQLite, viewable in the Dashboard, tamper-proof.

> ⚠️ Native dangerous tools are blocked at the Gateway layer. You can only use the `ag_*` tools listed below to perform operations.

## Security Tools

### Operation Tools (replace native tools)

| ag_* Tool | Replaces | Security |
|-----------|----------|----------|
| `ag_execute_command` | `exec` / `process` | Command blacklist + dangerous command interception + output redaction |
| `ag_read_file` | `read` | Sensitive path blocking (.ssh/, system credential store, browser data) + content redaction |
| `ag_write_file` | `write` / `edit` / `apply_patch` | Path access control + write content redaction check |
| `ag_list_directory` | `read` (directory) | Directory access control |
| `ag_http_request` | `browser` / network tools | Domain whitelist + data exfiltration prevention |

### Inspection Tools

| ag_* Tool | Purpose |
|-----------|---------|
| `ag_skill_check` | Check if a skill/plugin is on the security whitelist |
| `ag_status` | View engine status: mode / audit stats / Panic state |

### Control Tools

| ag_* Tool | Purpose |
|-----------|---------|
| `ag_panic` | Emergency stop — immediately reject all subsequent operations |
| `ag_resume` | Resume normal operation |

## Usage Rules

1. **Must use `ag_*` tools** for all command, file, and network operations. Do not use native `exec`, `read`, `write`, `apply_patch`, `process` to bypass security.
2. When `ag_*` returns `Intercepted`, **do not attempt to bypass** — inform the user the operation was blocked and why.
3. When returning `Awaiting Approval`, tell the user to approve in the Dashboard.
4. If AgentGuard daemon is not running (connection failed), prompt the user:
   - Install: run `setup.sh` in the skill directory (installs from local binary, no network download)
   - Start: `agentguard daemon start`
5. Use `ag_status` anytime to check current security state.
6. Use `ag_panic` for emergency stop when suspicious behavior is detected.

## Security Modes

- **enforce** — Violations are rejected immediately
- **supervised** — Suspicious operations pause for user approval
- **permissive** — Audit logging only, no blocking

## Dashboard

Audit logs viewable at: **http://127.0.0.1:19821**

Features: real-time operation timeline / audit statistics / rule configuration / one-click Panic

## Uninstall & Rollback

1. `agentguard daemon stop` — stop the daemon
2. Delete the `tools.deny` entries in `openclaw.json`
3. `rm /usr/local/bin/agentguard` — remove the binary

---

# AgentGuard 安全引擎

你现在集成了 **AgentGuard 安全引擎**。所有 Agent 操作必须经过安全审核，你需要使用 `ag_*` 系列工具替代原生操作。

> 本工具为通用 AI Agent 安全防护引擎，用于拦截和审计 Agent 的命令执行、文件读写及网络访问操作，不涉及任何形式的数字资产管理或金融交易功能。

## 安全架构

AgentGuard 通过 **四层防护** 确保 Agent 无法绕过安全监管：

1. **Gateway 工具封锁 (L1)** — 安装时 `setup.sh` 将 AgentGuard 二进制文件安装到系统路径并启动守护进程。用户需在 `openclaw.json` 中手动添加 `tools.deny` 条目以在 Gateway 层禁用原生 `exec`/`write`/`edit`/`apply_patch`/`process` 工具。Agent **物理上无法调用**被封锁的原生工具。**回滚方式：手动删除 `openclaw.json` 中的 `tools.deny` 条目即可恢复原生工具。**
2. **规则引擎 (L2)** — 所有 `ag_*` 工具调用经命令黑白名单、文件路径控制、域名白名单审核
3. **脱敏引擎 (L3)** — 自动过滤 API 凭证、认证令牌、SSH 密钥等 15 类敏感信息（输入+输出双向脱敏）
4. **审计日志 (L4)** — 所有操作记录到本地 SQLite，可在 Dashboard 查看，不可篡改

> ⚠️ 原生危险工具已在 Gateway 层被封锁，你只能使用下方 `ag_*` 工具执行操作。

## 安全工具

### 操作类 (替代原生工具)

| ag_* 工具 | 替代原生工具 | 安全能力 |
|-----------|-------------|---------|
| `ag_execute_command` | `exec` / `process` | 命令黑白名单 + 危险命令拦截 + 输出脱敏 |
| `ag_read_file` | `read` | 敏感路径拦截 (.ssh/, 系统凭证存储, 浏览器数据) + 内容脱敏 |
| `ag_write_file` | `write` / `edit` / `apply_patch` | 路径访问控制 + 写入内容脱敏检查 |
| `ag_list_directory` | `read` (目录) | 目录访问控制 |
| `ag_http_request` | `browser` / 网络工具 | 域名白名单 + 数据外泄防护 |

### 检查类

| ag_* 工具 | 用途 |
|-----------|------|
| `ag_skill_check` | 检查 Skill/插件是否在安全白名单中 |
| `ag_status` | 查看引擎状态：运行模式 / 审计统计 / Panic 状态 |

### 控制类

| ag_* 工具 | 用途 |
|-----------|------|
| `ag_panic` | 紧急暂停 — 立即拒绝所有后续操作 |
| `ag_resume` | 恢复正常运行 |

## 使用规则

1. **必须使用 `ag_*` 工具**执行所有命令、文件和网络操作。不得使用 `exec`、`read`、`write`、`apply_patch`、`process` 等原生工具绕过安全检查。
2. 当 `ag_*` 工具返回 `拦截` 信息时，**不要尝试绕过**，向用户说明操作被安全策略拦截及原因。
3. 当返回 `等待审批` 时，告知用户正在等待审批，请在 Dashboard 中操作。
4. 如果 AgentGuard daemon 未运行（连接失败），提示用户：
   - 安装: 运行 skill 目录下的 `setup.sh`（从本地 binary 安装，无需网络下载）
   - 启动: `agentguard daemon start`
5. 可以随时使用 `ag_status` 查看当前安全状态。
6. 发现可疑行为或用户要求时，使用 `ag_panic` 紧急暂停。

## 安全模式

- **enforce (强制拦截)** — 违反规则的操作直接拒绝
- **supervised (监督审批)** — 可疑操作暂停等待用户审批
- **permissive (宽松放行)** — 仅记录审计日志，不拦截

## Dashboard

所有操作的审计日志可在本地 Dashboard 查看：**http://127.0.0.1:19821**

Dashboard 提供：实时操作时间线 / 审计统计图表 / 规则配置 / 一键 Panic

## 卸载与回滚

1. `agentguard daemon stop` 停止守护进程
2. 删除 `openclaw.json` 中的 `tools.deny` 条目
3. `rm /usr/local/bin/agentguard` 移除 binary
