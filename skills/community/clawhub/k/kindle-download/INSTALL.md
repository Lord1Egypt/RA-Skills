# 安装说明

本文档详细说明如何安装 kindle-download skill 的所有依赖。

## 系统要求

- **操作系统**: Linux / macOS / Windows (WSL)
- **Node.js**: v18.0.0 或更高版本
- **Python**: 3.8.0 或更高版本
- **内存**: 至少 2GB 可用内存
- **磁盘**: 至少 500MB 可用空间（用于 Chromium 浏览器）

## 安装步骤

### 1. 安装 Node.js

#### Linux (Ubuntu/Debian)
```bash
# 使用 NodeSource 仓库
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# 或使用 NVM（推荐）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 20
nvm use 20
```

#### macOS
```bash
# 使用 Homebrew
brew install node@20

# 或使用 NVM
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.zshrc
nvm install 20
nvm use 20
```

### 2. 安装 Playwright 和 Chromium

```bash
# 安装 Playwright
npm install -g playwright

# 安装 Chromium 浏览器
npx playwright install chromium

# 如果需要安装所有依赖（推荐）
npx playwright install-deps chromium
```

> **注意**: Playwright Chromium 浏览器大约需要 300-400MB 磁盘空间。

### 3. 安装 Python 依赖

大多数 Python 安装已包含 `requests` 库。如果未安装：

```bash
pip3 install requests>=2.28.0
```

### 4. 配置凭证

您有两种方式配置凭证：

#### 方式 A: 使用环境变量（推荐）

将以下内容添加到您的 `~/.bashrc` 或 `~/.zshrc`：

```bash
export KINDLE_SMTP_EMAIL="your_email@163.com"
export KINDLE_SMTP_AUTH_CODE="your_smtp_auth_code"
export KINDLE_RECEIVER_EMAIL="your_kindle@kindle.com"
export KINDLE_ZLIB_EMAIL="your_zlibrary_email@example.com"
export KINDLE_ZLIB_PASSWORD="your_zlibrary_password"

# 可选配置
export KINDLE_SMTP_SERVER="smtp.163.com"  # 默认值
export KINDLE_SMTP_PORT="465"              # 默认值
export KINDLE_PROXY_SERVER="http://127.0.0.1:7890"  # 如果需要代理
```

然后执行：
```bash
source ~/.bashrc  # 或 source ~/.zshrc
```

#### 方式 B: 使用配置文件

```bash
# 创建配置目录
mkdir -p ~/.config/kindle-download

# 创建配置文件
cat > ~/.config/kindle-download/auth.json << 'EOF'
{
    "email": "your_email@163.com",
    "auth_code": "your_smtp_auth_code",
    "smtp_server": "smtp.163.com",
    "smtp_port": 465,
    "send_kindle_email": "your_kindle@kindle.com",
    "library_account_email": "your_zlibrary_email@example.com",
    "library_password": "your_zlibrary_password",
    "proxy_server": ""
}
EOF

# 设置安全权限（重要！）
chmod 600 ~/.config/kindle-download/auth.json
```

### 5. 安装 Skill

```bash
# 进入 OpenClaw skills 目录
cd ~/.openclaw/workspace/skills/

# 克隆或复制 skill
git clone https://github.com/xiehaixin/kindle-download.git
# 或者直接复制项目目录
```

## 验证安装

### 验证 Node.js
```bash
node --version  # 应显示 v18.x.x 或更高
```

### 验证 Playwright
```bash
npx playwright --version  # 应显示版本号
```

### 验证 Python
```bash
python3 --version  # 应显示 Python 3.8.x 或更高
```

### 测试 Skill

在 OpenClaw 中执行：
```
kindle 下载 三体
```

如果看到 "第一步登录已完成"，说明安装成功。

## 故障排除

### Playwright 找不到浏览器

**错误信息**: `Executable doesn't exist at ...`

**解决方案**:
```bash
# 重新安装 Chromium
npx playwright install chromium

# 或指定浏览器路径
export PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/path/to/chrome
```

### 权限问题

**错误信息**: `EACCES: permission denied`

**解决方案**:
```bash
# 检查配置文件权限
ls -la ~/.config/kindle-download/auth.json
# 应显示: -rw------- (600)

# 如果权限不正确
chmod 600 ~/.config/kindle-download/auth.json
```

### 网络问题

如果无法访问 Z-Library：

```bash
# 配置代理
export KINDLE_PROXY_SERVER="http://127.0.0.1:7890"

# 或在 auth.json 中设置
```

## 依赖清单

| 依赖 | 版本要求 | 用途 |
|------|---------|------|
| Node.js | >=18.0.0 | 运行 Playwright 自动化脚本 |
| Playwright | >=1.40.0 | Web 自动化框架 |
| Chromium | - | Playwright 浏览器（约 300MB） |
| Python | >=3.8.0 | 发送邮件 |
| requests | >=2.28.0 | HTTP 库（下载文件） |

## 安全建议

1. **使用环境变量**: 推荐使用环境变量存储敏感凭证
2. **文件权限**: 配置文件权限应设置为 `600`
3. **不要提交凭证**: 确保 `auth.json` 在 `.gitignore` 中
4. **使用专用邮箱**: 建议为 Kindle 发送创建专用邮箱账户
