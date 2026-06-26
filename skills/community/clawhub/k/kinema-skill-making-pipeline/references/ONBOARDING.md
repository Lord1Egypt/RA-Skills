# Kinema's Skill Making Pipeline Onboarding

> 本文档指导 AI Agent 完成首次环境配置。按顺序执行，遇到问题时参考 Troubleshooting。

## Prerequisites | 前置条件

- Git >= 2.30
- GitHub CLI (`gh`) >= 2.0
- Node.js >= 18（ClawHub CLI 依赖）

## Step 1: Git 身份配置

### 检测

```bash
git config user.name && git config user.email
```

**期望输出**: 用户名和邮箱（如 `LeeShunEE` / `lee@example.com`）

### 安装

若输出为空，需配置 Git 身份（必须询问用户提供用户名和邮箱）：

```bash
git config --global user.name "<用户名>"
git config --global user.email "<邮箱>"
```

### 验证

```bash
git config user.name && git config user.email
```

**期望输出**: 刚配置的用户名和邮箱

## Step 2: GitHub CLI 登录

### 检测

```bash
gh auth status
```

**期望输出**: `Logged in to github.com account <username>` 或类似信息

### 安装

若未安装 `gh`：

```bash
# macOS
brew install gh

# Windows (winget)
winget install GitHub.cli

# Linux
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list
sudo apt update && sudo apt install gh
```

若已安装但未登录（必须让用户在终端中交互执行）：

```bash
gh auth login
```

按提示选择：GitHub.com → HTTPS → 浏览器认证。

> **注意**：若 Agent 无法自动打开浏览器，将输出的授权链接提供给用户，由用户手动在浏览器中访问完成授权。

### 验证

```bash
gh auth status
```

**期望输出**: `Logged in to github.com account <username>`

## Step 3: ClawHub CLI 登录

### 检测

```bash
clawhub whoami
```

**期望输出**: 用户名或账户信息

### 安装

若 `clawhub` 命令不存在：

```bash
npm install -g clawhub
```

若已安装但未登录（必须让用户在终端中交互执行）：

```bash
clawhub login
```

按提示完成浏览器授权。

> **注意**：若 Agent 无法自动打开浏览器，将 `clawhub login` 输出的 `https://clawhub.ai/cli/auth?...` 链接提供给用户，由用户手动在浏览器中访问完成授权。

### 验证

```bash
clawhub whoami
```

**期望输出**: 当前登录的 ClawHub 用户名

## Step 4: 最终验证

依次运行以下命令，确认所有工具就绪：

```bash
git config user.name
gh auth status
clawhub whoami
```

**期望输出**: 三个命令均返回有效信息，无报错。

## Troubleshooting | 故障排除

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `gh: command not found` | 未安装 GitHub CLI | 按 Step 2 安装 `gh` |
| `clawhub: command not found` | 未安装 ClawHub CLI | `npm install -g clawhub` |
| `gh auth status` 显示未登录 | 未完成 GitHub 认证 | 执行 `gh auth login`，按提示操作 |
| `clawhub whoami` 返回错误 | 未登录 ClawHub | 执行 `clawhub login` |
| `git config user.name` 为空 | 未配置 Git 身份 | 按 Step 1 配置用户名和邮箱 |
| `clawhub login` 浏览器无法打开 | 无图形界面或浏览器不可用 | 尝试 `clawhub login --token` 使用 token 登录 |
| `npm install -g clawhub` 权限不足 | 全局安装需要权限 | macOS/Linux 使用 `sudo npm install -g clawhub`，或使用 nvm 管理 Node |
