# Kinema's Skill Making Pipeline Onboarding

> 本文档指导 AI Agent 配置跨平台 Skill 开发与发布环境。只安装本次任务实际需要的平台工具；Codex 插件开发和安装不依赖 Node.js。

## Prerequisites | 前置条件

- Git >= 2.30
- GitHub CLI (`gh`) >= 2.0：仅 GitHub 仓库、tag 和 release 操作需要
- Codex CLI：仅 Codex plugin 验证、安装和更新需要
- Claude Code CLI：仅 Claude plugin 验证、安装和更新需要
- Node.js >= 18：仅 ClawHub CLI 需要，不是 Codex 前置条件

## Step 1: Git 身份配置

### 检测

```bash
git --version
git config user.name
git config user.email
```

### 配置

若身份为空，必须询问用户提供姓名和邮箱，再按用户选择配置仓库级或全局身份。不要猜测：

```bash
git config user.name "<用户名>"
git config user.email "<邮箱>"
```

如用户明确要求全局配置，再加 `--global`。

### 验证

```bash
git config user.name && git config user.email
```

## Step 2: GitHub CLI

### 检测

```bash
gh --version
gh auth status
```

### 安装与登录

只在任务需要 GitHub 操作且命令缺失时安装：

```bash
# Windows
winget install GitHub.cli

# macOS
brew install gh
```

Linux 使用 GitHub CLI 官方软件源。安装后由用户交互执行 `gh auth login`；Agent 不索取或记录 token。

### 验证

```bash
gh auth status
```

## Step 3: Codex CLI（按需）

### 检测

```bash
codex --version
codex plugin --help
```

### 处理

- 命令可用：继续 Codex manifest、marketplace 和安装验证。
- 命令不可用：若本次仅开发 Claude/OpenClaw skill，记录后跳过；若用户要求 Codex 适配，停止安装验证并引导用户按 OpenAI 官方 Codex 安装说明完成安装。
- 不用 `npm` 安装或运行 Codex plugin；不要把 Node.js 作为 Codex plugin 的依赖。

### 验证

```bash
codex plugin marketplace list
codex plugin list
```

## Step 4: Claude Code CLI（按需）

### 检测

```bash
claude --version
```

命令缺失但本次不发布 Claude plugin 时记录并跳过；需要 Claude plugin 操作时按 Anthropic 官方安装说明配置，再验证 `claude plugin list`。

## Step 5: ClawHub CLI（按需）

### 检测

```bash
node --version
npm --version
clawhub whoami
```

### 安装与登录

只有用户要求发布或更新 ClawHub 时才需要 Node.js。Node/npm 已存在但 `clawhub` 缺失时：

```bash
npm install -g clawhub
```

登录由用户交互执行 `clawhub login`。如果用户没有 Node.js 且本次不涉及 ClawHub，直接跳过，不阻塞 Codex/Claude plugin 工作。

### 验证

```bash
clawhub whoami
```

## Step 6: 最终检查

按本次目标运行对应子集：

```bash
git status
gh auth status
codex plugin list
claude plugin list
clawhub whoami
```

只要求目标平台通过；未安装且不在任务范围的平台标记为跳过。

## Troubleshooting | 故障排除

| 错误 | 原因 | 解决方案 |
| --- | --- | --- |
| `gh: command not found` | GitHub CLI 未安装 | 用系统包管理器安装 `gh` |
| `gh auth status` 未登录 | GitHub 认证未完成 | 用户交互执行 `gh auth login` |
| `codex: command not found` | Codex CLI 未安装 | 使用 OpenAI 官方 Codex 安装说明；不要用 ClawHub/Node 流程替代 |
| Codex marketplace 有条目但插件不可安装 | 远程仓库尚未发布有效 `.codex-plugin/plugin.json`，或 source/ref 错误 | 先发布插件仓库，再刷新 marketplace 并重试 `codex plugin add` |
| Codex 更新后仍加载旧 skill | 当前对话已加载旧上下文 | 新开 Codex 对话 |
| `claude: command not found` | Claude Code 未安装 | 按 Anthropic 官方说明安装，或跳过非目标平台 |
| `clawhub: command not found` | ClawHub CLI 未安装 | 仅在需要 ClawHub 时安装 Node.js，然后 `npm install -g clawhub` |
| `npm` 不存在 | Node.js 未安装 | 不影响 Codex plugin；仅 ClawHub 任务需要安装 Node.js |
| CLI 登录需要浏览器 | 交互认证尚未完成 | 将 CLI 输出的官方授权链接交给用户操作，不代填凭据 |
