---
name: openclaw-deploy
description: OpenClaw/NEUXSBOT 全平台部署指南 - 支持 Mac、Windows、Linux 三平台一键安装。包含环境准备、安装配置、AI模型设置、消息平台对接、故障排除等完整流程。
metadata:
  version: "1.0"
  origin: "OpenClaw China + NEUXSBOT"
---

# OpenClaw 全平台部署指南

OpenClaw（NEUXSBOT）跨平台安装配置完整教程，支持 macOS、Windows、Linux 三平台实操。

---

## 📋 目录

1. [系统要求](#系统要求)
2. [macOS 部署](#macos-部署)
3. [Windows 部署](#windows-部署)
4. [Linux 部署](#linux-部署)
5. [AI 模型配置](#ai-模型配置)
6. [消息平台对接](#消息平台对接)
7. [故障排除](#故障排除)

---

## 系统要求

### 最低配置

| 项目 | 要求 |
|------|------|
| **操作系统** | Windows 10/11, macOS 10.15+, Ubuntu 20.04+ |
| **内存** | 4GB RAM |
| **磁盘空间** | 2GB 可用空间 |
| **网络** | 需要访问 AI 模型 API（或使用本地模型） |

### 推荐配置

| 项目 | 要求 |
|------|------|
| **操作系统** | Windows 11, macOS 12+, Ubuntu 22.04+ |
| **内存** | 8GB RAM 或更多 |
| **磁盘空间** | 5GB 可用空间 |
| **处理器** | 支持本地模型运行（如使用 Ollama） |

---

## macOS 部署

### 方法一：DMG 安装包（推荐）

**步骤 1：下载安装包**

```bash
# 访问 GitHub Releases 下载最新版
curl -LO https://github.com/Markovmodcn/openclaw-china/releases/latest/download/NEUXSBOT.dmg
```

**步骤 2：安装应用**

1. 双击打开 `NEUXSBOT.dmg`
2. 将 NEUXSBOT 图标拖拽到 Applications 文件夹
3. 等待复制完成

**步骤 3：首次运行**

```bash
# 方法 1：通过 Applications 打开
open /Applications/NEUXSBOT.app

# 方法 2：如果提示"无法验证开发者"
# 前往 系统设置 > 隐私与安全 > 允许打开
```

**绕过安全检查：**

1. 右键点击 NEUXSBOT.app
2. 选择"打开"
3. 在弹出的对话框中点击"打开"

### 方法二：脚本安装

```bash
# 一键安装脚本
curl -fsSL https://raw.githubusercontent.com/Markovmodcn/openclaw-china/main/scripts/install.sh | bash
```

### 方法三：Homebrew 安装（如可用）

```bash
# 添加 tap（如果官方提供）
brew tap openclaw/china

# 安装
brew install --cask nexusbot
```

### macOS 配置文件位置

```bash
# 配置文件
~/.nexusbot/config.yaml

# 日志文件
~/.nexusbot/logs/

# 数据文件
~/.nexusbot/data/

# 技能插件
~/.nexusbot/skills/
```

---

## Windows 部署

### 方法一：安装版（推荐）

**步骤 1：下载安装包**

```powershell
# 使用 PowerShell 下载
Invoke-WebRequest -Uri "https://github.com/Markovmodcn/openclaw-china/releases/latest/download/NEUXSBOT-Setup.exe" -OutFile "NEUXSBOT-Setup.exe"
```

或直接访问浏览器下载：
- 打开 https://github.com/Markovmodcn/openclaw-china/releases/latest
- 下载 `NEUXSBOT-Setup.exe`

**步骤 2：运行安装程序**

1. 双击 `NEUXSBOT-Setup.exe`
2. 如果提示"Windows 已保护你的电脑"：
   - 点击"更多信息"
   - 点击"仍要运行"
3. 按照安装向导操作
4. 选择安装位置（默认：`C:\Program Files\NEUXSBOT`）

**步骤 3：完成安装**

- 安装完成后会自动创建桌面快捷方式
- 双击快捷方式启动

### 方法二：绿色便携版

```powershell
# 下载便携版
Invoke-WebRequest -Uri "https://github.com/Markovmodcn/openclaw-china/releases/latest/download/NEUXSBOT-Portable.zip" -OutFile "NEUXSBOT-Portable.zip"

# 解压
Expand-Archive -Path "NEUXSBOT-Portable.zip" -DestinationPath "C:\Tools\NEUXSBOT"

# 运行
& "C:\Tools\NEUXSBOT\NEUXSBOT.exe"
```

### 方法三：PowerShell 脚本安装

```powershell
# 一键安装
iwr -useb https://raw.githubusercontent.com/Markovmodcn/openclaw-china/main/scripts/install.ps1 | iex
```

### Windows 配置文件位置

```powershell
# 配置文件
%USERPROFILE%\.nexusbot\config.yaml

# 日志文件
%USERPROFILE%\.nexusbot\logs\

# 数据文件
%USERPROFILE%\.nexusbot\data\
```

### Windows 防火墙设置

如果 NEUXSBOT 需要接收外部 webhook：

```powershell
# 以管理员身份运行 PowerShell
New-NetFirewallRule -DisplayName "NEUXSBOT" -Direction Inbound -Protocol TCP -LocalPort 3000 -Action Allow
```

---

## Linux 部署

### Ubuntu/Debian（推荐）

**步骤 1：下载 .deb 包**

```bash
# 下载最新版
wget https://github.com/Markovmodcn/openclaw-china/releases/latest/download/nexusbot_amd64.deb

# 或使用 curl
curl -LO https://github.com/Markovmodcn/openclaw-china/releases/latest/download/nexusbot_amd64.deb
```

**步骤 2：安装**

```bash
# 安装 .deb 包
sudo dpkg -i nexusbot_amd64.deb

# 如果提示依赖问题，修复依赖
sudo apt-get install -f
```

**步骤 3：启动**

```bash
# 命令行启动
nexusbot

# 或使用 systemd 服务
sudo systemctl enable nexusbot
sudo systemctl start nexusbot
```

### CentOS/RHEL/Fedora

```bash
# 下载 RPM 包（如提供）
wget https://github.com/Markovmodcn/openclaw-china/releases/latest/download/nexusbot_amd64.rpm

# 安装
sudo rpm -i nexusbot_amd64.rpm

# 或使用 dnf
sudo dnf install nexusbot_amd64.rpm
```

### 通用脚本安装（所有发行版）

```bash
# 一键安装脚本
curl -fsSL https://raw.githubusercontent.com/Markovmodcn/openclaw-china/main/scripts/install.sh | bash
```

### Docker 安装（跨平台）

```bash
# 使用 Docker 运行
docker run -d \
  --name nexusbot \
  -p 3000:3000 \
  -v nexusbot-data:/data \
  markovmodcn/nexusbot:latest

# 查看日志
docker logs -f nexusbot

# 停止
docker stop nexusbot

# 删除
docker rm nexusbot
```

### Docker Compose 部署

创建 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  nexusbot:
    image: markovmodcn/nexusbot:latest
    container_name: nexusbot
    restart: unless-stopped
    ports:
      - "3000:3000"
    volumes:
      - nexusbot-data:/data
      - ./config.yaml:/app/config.yaml:ro
    environment:
      - NODE_ENV=production
      - LOG_LEVEL=info

volumes:
  nexusbot-data:
```

启动：

```bash
docker-compose up -d
```

### Linux 配置文件位置

```bash
# 配置文件
~/.nexusbot/config.yaml

# 日志文件
~/.nexusbot/logs/

# 数据文件
~/.nexusbot/data/

# 全局配置（如使用 systemd）
/etc/nexusbot/config.yaml
```

### Linux 系统服务设置

创建 systemd 服务文件 `/etc/systemd/system/nexusbot.service`：

```ini
[Unit]
Description=NEUXSBOT AI Agent
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/home/your-username
ExecCommand=/usr/bin/nexusbot
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启用并启动：

```bash
sudo systemctl daemon-reload
sudo systemctl enable nexusbot
sudo systemctl start nexusbot

# 查看状态
sudo systemctl status nexusbot

# 查看日志
sudo journalctl -u nexusbot -f
```

---

## AI 模型配置

### 选项 A：本地模型（推荐）

#### 安装 Ollama

**macOS：**

```bash
# 下载安装
brew install ollama

# 或从官网下载
# https://ollama.com
```

**Windows：**

```powershell
# 下载安装包
# https://ollama.com/download/windows

# 或使用 Chocolatey
choco install ollama
```

**Linux：**

```bash
# 一键安装
curl -fsSL https://ollama.com/install.sh | sh
```

#### 下载模型

```bash
# 拉取模型（推荐 Qwen2.5 中文版）
ollama pull qwen2.5:7b

# 或其他模型
ollama pull llama3.2:8b
ollama pull deepseek-r1:7b
```

#### 配置 NEUXSBOT 连接 Ollama

编辑 `~/.nexusbot/config.yaml`：

```yaml
ai:
  provider: ollama
  ollama:
    host: http://localhost:11434
    model: qwen2.5:7b
    temperature: 0.7
```

### 选项 B：在线模型

#### DeepSeek（推荐）

```yaml
ai:
  provider: deepseek
  deepseek:
    api_key: your_api_key_here
    model: deepseek-chat
```

获取 API Key：https://platform.deepseek.com

#### Kimi（Moonshot）

```yaml
ai:
  provider: kimi
  kimi:
    api_key: your_api_key_here
    model: moonshot-v1-8k
```

获取 API Key：https://platform.moonshot.cn

#### 通义千问

```yaml
ai:
  provider: qwen
  qwen:
    api_key: your_api_key_here
    model: qwen-turbo
```

获取 API Key：https://dashscope.aliyun.com

---

## 消息平台对接

### 钉钉配置

**步骤 1：创建钉钉机器人**

1. 登录钉钉开放平台：https://open.dingtalk.com
2. 创建企业内部应用
3. 获取 `AppKey` 和 `AppSecret`
4. 配置机器人 webhook

**步骤 2：配置 NEUXSBOT**

```yaml
platforms:
  dingtalk:
    enabled: true
    app_key: your_app_key
    app_secret: your_app_secret
    webhook_port: 3000
```

### 飞书配置

**步骤 1：创建飞书应用**

1. 登录飞书开放平台：https://open.feishu.cn
2. 创建企业自建应用
3. 获取 `AppID` 和 `AppSecret`
4. 订阅消息事件

**步骤 2：配置 NEUXSBOT**

```yaml
platforms:
  feishu:
    enabled: true
    app_id: your_app_id
    app_secret: your_app_secret
    webhook_port: 3000
    encrypt_key: your_encrypt_key
    verification_token: your_verification_token
```

### 企业微信配置

**步骤 1：创建企业微信应用**

1. 登录企业微信管理后台
2. 应用管理 → 创建应用
3. 获取 `CorpID`、`AgentID`、`Secret`
4. 配置接收消息

**步骤 2：配置 NEUXSBOT**

```yaml
platforms:
  wecom:
    enabled: true
    corp_id: your_corp_id
    agent_id: your_agent_id
    secret: your_secret
    token: your_token
    aes_key: your_aes_key
    webhook_port: 3000
```

---

## 验证安装

### 检查服务状态

```bash
# 查看进程
# macOS/Linux
ps aux | grep nexusbot

# Windows
Get-Process | Where-Object {$_.Name -like "*nexusbot*"}
```

### 测试 AI 连接

```bash
# 查看日志
tail -f ~/.nexusbot/logs/app.log

# 应该看到
# "AI provider connected successfully"
# "Model: qwen2.5:7b"
```

### 测试消息平台

1. 在对应平台（钉钉/飞书/企微）找到机器人
2. 发送测试消息："你好"
3. 检查机器人是否回复

---

## 故障排除

### 常见问题

#### macOS "无法验证开发者"

**症状：** 提示"无法打开，因为无法验证开发者"

**解决：**

```bash
# 方法 1：右键打开
# 右键点击应用 → 打开 → 仍要打开

# 方法 2：命令行
xattr -d com.apple.quarantine /Applications/NEUXSBOT.app

# 方法 3：系统设置
# 系统设置 → 隐私与安全 → 允许从以下位置下载的应用 → 允许
```

#### Windows "Windows 已保护你的电脑"

**症状：** SmartScreen 阻止运行

**解决：**

1. 点击"更多信息"
2. 点击"仍要运行"
3. 或以管理员身份运行

#### Linux 依赖问题

**症状：** 提示缺少依赖库

**解决：**

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -f

# CentOS/RHEL
sudo yum install -y libstdc++6
```

#### AI 模型连接失败

**症状：** 提示"Failed to connect to AI provider"

**解决：**

```bash
# 检查 Ollama 是否运行
curl http://localhost:11434/api/tags

# 如果没有运行
ollama serve

# 检查配置
cat ~/.nexusbot/config.yaml | grep -A 5 ollama
```

#### Webhook 接收不到消息

**症状：** 机器人不回复

**解决：**

```bash
# 检查端口是否被占用
lsof -i :3000

# 检查防火墙
# macOS
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /Applications/NEUXSBOT.app

# Linux
sudo ufw allow 3000/tcp

# Windows
New-NetFirewallRule -DisplayName "NEUXSBOT" -Direction Inbound -LocalPort 3000 -Protocol TCP -Action Allow
```

### 日志查看

```bash
# macOS/Linux
tail -f ~/.nexusbot/logs/app.log

# Windows
Get-Content "$env:USERPROFILE\.nexusbot\logs\app.log" -Wait

# Docker
docker logs -f nexusbot
```

### 重置配置

```bash
# 备份并删除配置
mv ~/.nexusbot/config.yaml ~/.nexusbot/config.yaml.backup

# 重启应用，会自动生成默认配置
```

---

## 更新升级

### macOS

```bash
# 方法 1：应用内更新
# 点击菜单栏 → 检查更新

# 方法 2：重新下载安装
# 下载最新版 DMG，覆盖安装
```

### Windows

```powershell
# 方法 1：应用内更新
# 点击设置 → 检查更新

# 方法 2：下载新版安装包
# 运行新安装程序，会自动覆盖旧版
```

### Linux

```bash
# Ubuntu/Debian
sudo dpkg -i nexusbot_amd64.deb

# 或使用 apt（如配置了源）
sudo apt update
sudo apt upgrade nexusbot

# Docker
docker pull markovmodcn/nexusbot:latest
docker-compose up -d
```

---

## 下一步

- [技能市场使用指南](./skills-guide.md)
- [自定义技能开发](./custom-skill.md)
- [高级配置说明](./advanced-config.md)
- [API 接口文档](./api-reference.md)

---

## 参考资源

- 官网：https://www.neuxsbot.com
- 文档：https://www.neuxsbot.com/docs
- GitHub：https://github.com/Markovmodcn/openclaw-china
- 反馈：https://github.com/Markovmodcn/openclaw-china/issues

---

*本指南基于 NEUXSBOT/OpenClaw China 开源项目整理*
