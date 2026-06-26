---
name: octool
description: Openclaw Visual Configuration Assistant. Provides secure wizard for local/Git backup and workspace migration.
homepage: https://github.com/donnieclaw/octool
metadata: {"clawdbot":{"emoji":"🖥️"}}
---

# Openclaw Backup Assistant (oc-tool)

**🌍 English Description Below | 中文介绍在上方**

这是一个纯前端的安全、可视化的 Openclaw 配置管理助手。它旨在帮助用户管理 Openclaw 的配置备份、Agent 灵魂文件（MEMORY/SOUL/IDENTITY）以及系统环境迁移。

### 主要功能：
- **Git / 本地双模备份**：支持将配置备份至本地目录或私有 GitHub 仓库。
- **安全配置向导**：运行于浏览器本地沙箱，为用户生成可供手动执行的环境配置脚本。
- **Agent 数据保护**：生成覆盖 workspace 目录下关键文件（如 `openclaw.json`、`MEMORY.md`）的 `cp`/`rsync` 命令，防止数据丢失。所有命令均需手动执行。
- **终端快捷指令生成**：为用户提供 `oc`（智能代理启动）、`oc-save`（备份当前环境及自定义文件）、`oc-rec`（一键恢复设定版本）等常用指令的文本示例，方便在终端中手动使用。
- **灵活的自定义备份**：界面提供直观的文件拖拽区，支持用户根据自身需求，随时增减需要一同打包备份的额外文件夹或特定文件。

### 🔒 隐私与安全声明 (使用前必读)
- **真正的零外部请求**：本工具已移除所有外部字体和资源依赖，100% 仅在本地浏览器沙箱运行。除了在 Git 模式下直接请求官方的 `api.github.com` 接口外，不存在任何向第三方服务器发送请求的代码。可断网运行以验证安全性。
- **凭据存留说明**：Git 模式下，您提供的 GitHub PAT 仅用于两个 `api.github.com` 接口调用（仓库验证 + 文件写入）。Token 保存在浏览器 `sessionStorage` 中，**关闭标签页后自动清除**，绝不写入 `localStorage`，绝不发送至任何第三方服务器。强烈建议使用仅具备目标仓库 `Contents: Read and Write` 权限的 fine-grained PAT。
- **代理检测说明**：`oc()` 命令使用原生 macOS `scutil --proxy` 配合 `awk` 读取系统代理配置，为只读操作，无 `node -e`、无 `eval`、无动态代码执行。
- **脚本生成说明**：本工具生成的 `sed`、`rsync`、`cp`、`git` 命令均以纯文本展示供您审阅，需手动复制到终端执行。工具本身不自动执行任何系统命令。写入 `~/.bash_profile` 的命令带幂等检查，重复执行安全。所有流入 shell 命令的用户输入（路径名、tag、commit message、排除目录）在生成时均经过严格验证，包含非法字符时拒绝生成并提示错误。
- **本地文件读取限定**：文件拖拽区仅通过浏览器 File API 解析您主动拖入的文件，不会在后台读取其他磁盘文件。

---

**This is a frontend-only, secure, visual configuration assistant for Openclaw.** It helps users manage configuration backups, Agent persona files (MEMORY/SOUL/IDENTITY), and system environment migrations.

### Core Features:
- **Dual Backup Modes (Git / Local)**: Supports backing up configurations to local directories or private GitHub repositories.
- **Secure Configuration Wizard**: Runs in a local browser sandbox, generating environment configuration scripts for manual terminal execution.
- **Agent Data Protection**: Generates `cp`/`rsync` commands targeting specific, user-selected files (e.g. `openclaw.json`, `MEMORY.md`). No files are read or copied automatically — all generated commands require manual review and execution in your terminal.
- **Terminal Command Generator**: Provides text-based command snippets for manual terminal use, including `oc` (smart proxy startup), `oc-save` (backup current environment & custom files), and `oc-rec` (restore specific versions).
- **Flexible Custom Backups**: The UI features an intuitive drag-and-drop area, allowing users to easily add or remove extra folders/files to be included in the backup package.

### 🔒 Privacy & Security (Please Read)
- **True Zero External Tracking**: All external dependencies have been removed. This tool runs 100% client-side in your local browser sandbox. The only external call is to `api.github.com` when you explicitly opt into Git mode. You can verify offline safety by opening DevTools > Network — zero requests without a GitHub token.
- **Credential Handling**: The GitHub PAT is used only for two `api.github.com` calls: `GET /repos/{owner}/{repo}` (verify access) and `PUT /repos/{owner}/{repo}/contents/{path}` (write backup). The token is stored in `sessionStorage` only — **it is automatically cleared when the tab is closed** and is never written to `localStorage`. We recommend a fine-grained PAT scoped to `Contents: Read and Write` on the target repo only.
- **Proxy Detection**: The generated `oc()` command detects system proxy using native macOS `scutil --proxy` piped through `awk`. No `node -e`, no `eval`, no dynamic code execution. Read-only syscall only.
- **Shell Command Generation**: This tool generates `sed`, `rsync`, `cp`, and `git` commands displayed as plaintext for your review. **No commands are auto-executed.** The `bash_profile` write command includes an idempotent guard (`OC_TOOL_BLOCK` marker check) — safe to run multiple times. All user inputs that flow into generated shell commands (paths, tags, commit messages, rsync excludes) are validated at generation time; inputs containing shell metacharacters are rejected with a visible error.
- **Local File Reading**: Files are read only when you explicitly drag them into the drop zone via the browser File API. No background disk access occurs.

## How to start / 启动方式

After installation, open the file below in your browser.
If installed to a custom workspace, replace `~/.openclaw/skills` with your workspace path.

安装完成后，用浏览器打开以下文件。如安装在自定义 workspace 下，请将路径替换为对应目录。

```
~/.openclaw/skills/octool/oc-tool.html
```
