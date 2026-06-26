---
name: "hermes-deployer"
version: "1.0.0"
description: "在 Linux 服务器上安装、配置、部署和运维 Hermes Agent（Nous Research 出品的自我改进 AI Agent）。触发词：hermes、hermes agent、部署 hermes、安装 hermes、hermes gateway、hermes 运维、hermes 排障、hermes 配置、hermes 重启、微信 bot 部署、企微 bot 部署、聊天机器人部署。"
---

# Hermes Deployer — 服务器部署与运维 Skill

## 概述

Hermes Agent 是 Nous Research 开源的自我改进 AI Agent，支持接入微信、企微、Telegram、Discord 等平台，通过 Gateway 模式在服务器上 24/7 运行。

本 Skill 覆盖从零部署到日常运维的全流程。

## 前提条件

| 项目 | 要求 |
|------|------|
| 操作系统 | Ubuntu 22.04+ / Debian 12+ |
| Python | 3.11+ （推荐 3.12） |
| 内存 | ≥ 1GB（轻量应用服务器即可） |
| 网络 | 需要访问 GitHub、PyPI、LLM API |
| SSH 访问 | 需要能 SSH 到目标服务器 |

## 安装流程

### Phase 1: 环境准备

```bash
# 1. 确认 Python 版本
python3 --version  # 需要 3.11+

# 2. 安装系统依赖
sudo apt update && sudo apt install -y python3-venv python3-pip git nodejs npm

# 3. 克隆 hermes-agent
cd /home/$USER
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent

# 4. 创建 venv 并安装
python3 -m venv venv
source venv/bin/activate
pip install -e .

# 5. 验证安装
hermes --version
```

### Phase 2: 配置 LLM Provider

Hermes 支持多种 LLM provider。**推荐方式是 `provider: "custom"` + 环境变量**。

#### 创建 ~/.hermes/.env

```bash
mkdir -p ~/.hermes

cat > ~/.hermes/.env << 'ENV'
# === LLM Provider ===
# 方式一：OpenAI 兼容接口（腾讯云 LKEAP、DeepSeek、智谱 等）
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_BASE_URL=https://api.lkeap.cloud.tencent.com/v3

# 方式二：智谱 AI 原生（免费额度）
# GLM_API_KEY=your-glm-api-key

# 方式三：Anthropic
# ANTHROPIC_API_KEY=sk-ant-xxx

# === 平台配置（按需启用）===
# -- 微信 iLink --
# WEIXIN_ACCOUNT_ID=xxx@im.bot
# WEIXIN_TOKEN=xxx@im.bot:token
# WEIXIN_BASE_URL=https://ilinkai.weixin.qq.com
# WEIXIN_CDN_BASE_URL=https://novac2c.cdn.weixin.qq.com/c2c
# WEIXIN_DM_POLICY=open
# WEIXIN_GROUP_POLICY=open
# WEIXIN_HOME_CHANNEL=user_openid@im.wechat
# GATEWAY_ALLOW_ALL_USERS=true

# -- Telegram --
# TELEGRAM_BOT_TOKEN=xxx
# TELEGRAM_ALLOWED_USERS=user_id
# TELEGRAM_HOME_CHANNEL=user_id
ENV
```

#### 创建 ~/.hermes/config.yaml

```yaml
# Hermes Agent Configuration

model:
  default: "glm-5"           # 模型名
  provider: "custom"          # 使用 custom provider
  base_url: "https://api.lkeap.cloud.tencent.com/v3"  # API 地址

permissions:
  mode: bypassPermissions     # 服务器部署建议 bypass

# 模型别名（可选，方便在聊天中用 /model flash 切换）
model_aliases:
  flash:
    model: glm-4-flash
    provider: zai
  think:
    model: glm-z1-flash
    provider: zai

# 消息平台
platforms:
  weixin:
    enabled: true
    extra:
      dm_policy: "open"
      group_policy: "open"
  # wecom:
  #   enabled: true
  #   extra:
  #     bot_id: "your-bot-id"
  #     secret: "your-bot-secret"
  #     websocket_url: "wss://openws.work.weixin.qq.com"
  #     dm_policy: "open"
  #     group_policy: "open"

# System prompt
system_prompt: |
  你是一个有用的 AI 助手。

# 技能系统
skills:
  auto_create: true
  auto_improve: true

# 记忆系统
memory:
  enabled: true
  provider: local

context:
  memory_char_limit: 20000
  user_char_limit: 3000
```

### Phase 3: 测试运行

```bash
# 前台运行测试（Ctrl+C 停止）
cd /home/$USER/hermes-agent
./venv/bin/hermes gateway run -v
```

确认看到：
- `✓ weixin connected`（或其他平台）
- `Gateway running with N platform(s)`
- 手机上发消息能正常收到回复

### Phase 4: 创建 systemd 服务

```bash
sudo tee /etc/systemd/system/hermes-gateway.service > /dev/null << 'SVC'
[Unit]
Description=Hermes Agent Gateway
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$USER
Group=$USER
WorkingDirectory=/home/$USER/hermes-agent
ExecStart=/home/$USER/hermes-agent/venv/bin/hermes gateway run --replace
Environment=HOME=/home/$USER
Environment=PATH=/home/$USER/hermes-agent/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
Environment=HERMES_HOME=/home/$USER/.hermes
Restart=on-failure
RestartSec=15
KillMode=mixed
KillSignal=SIGTERM
TimeoutStopSec=30
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
SVC

sudo systemctl daemon-reload
sudo systemctl enable hermes-gateway.service
sudo systemctl start hermes-gateway.service
```

> ⚠️ **关键注意事项**：
> - `ExecStart` **必须用 venv 内的绝对路径**（如 `/home/$USER/hermes-agent/venv/bin/hermes`），不要用系统 Python
> - 上面模板中的 `$USER` 需要替换为实际的 Linux 用户名（如 `ubuntu`）
> - `--replace` 参数确保旧进程残留时能自动接管
> - `Restart=on-failure` + `RestartSec=15`：失败时重试，间隔 15 秒避免 crash 风暴
> - 如果依赖其他服务（如 API proxy），用 `Wants=`（软依赖），**绝对不要用 `Requires=`**（硬依赖会连带杀进程）

### Phase 5: 验证部署

```bash
# 检查服务状态
sudo systemctl status hermes-gateway.service

# 查看日志
tail -30 ~/.hermes/logs/agent.log

# 查看错误日志
tail -20 ~/.hermes/logs/errors.log

# 确认进程存活
ps aux | grep 'hermes.*gateway' | grep -v grep
```

## 配置参考

### Provider 配置方式

Hermes 支持以下 provider：

| Provider slug | 说明 | 认证方式 |
|--------------|------|---------|
| `openai` | OpenAI 官方 | OPENAI_API_KEY |
| `anthropic` | Anthropic Claude | ANTHROPIC_API_KEY |
| `openrouter` | OpenRouter 聚合 | OPENROUTER_API_KEY |
| `zai` | 智谱 AI (ZhipuAI) | GLM_API_KEY |
| `custom` | 自定义 OpenAI 兼容接口 | OPENAI_API_KEY + base_url |

#### ⚠️ 自定义 Provider 的正确配置方式

**方式一（推荐）**：在 model 段直接写 `provider: "custom"` + `base_url`

```yaml
model:
  default: "glm-5"
  provider: "custom"
  base_url: "https://api.lkeap.cloud.tencent.com/v3"
```

**方式二**：用 `custom_providers` 列表（注意是**列表**格式！）

```yaml
custom_providers:
  - name: "Tencent Cloud LKEAP"
    base_url: "https://api.lkeap.cloud.tencent.com/v3"
    key_env: "OPENAI_API_KEY"

model:
  default: "glm-5"
  provider: "custom:tencent-cloud-lkeap"   # slug = custom: + 小写连字符化的 name
```

**❌ 错误方式**：不要用 `providers:` 字典格式

```yaml
# 这样写 hermes 不认！会报 "Unknown provider"
providers:
  tencent-cloud:
    name: "xxx"
    api: "xxx"
```

### 消息平台配置

#### 微信（Weixin iLink）

需要先在 [iLink 平台](https://ilinkai.weixin.qq.com) 注册 bot，获取 account_id 和 token。

```env
WEIXIN_ACCOUNT_ID=your_account@im.bot
WEIXIN_TOKEN=your_account@im.bot:your_token_hex
WEIXIN_BASE_URL=https://ilinkai.weixin.qq.com
WEIXIN_CDN_BASE_URL=https://novac2c.cdn.weixin.qq.com/c2c
WEIXIN_DM_POLICY=open
WEIXIN_GROUP_POLICY=open
WEIXIN_HOME_CHANNEL=user_openid@im.wechat
GATEWAY_ALLOW_ALL_USERS=true
```

config.yaml:
```yaml
platforms:
  weixin:
    enabled: true
    extra:
      dm_policy: "open"
      group_policy: "open"
```

#### 企业微信（WeCom）

需要在企微后台创建智能 bot，获取 bot_id 和 secret。

```yaml
platforms:
  wecom:
    enabled: true
    extra:
      bot_id: "your-wecom-bot-id"
      secret: "your-wecom-bot-secret"
      websocket_url: "wss://openws.work.weixin.qq.com"
      dm_policy: "open"
      group_policy: "open"
```

#### Telegram

```env
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_ALLOWED_USERS=your_user_id
TELEGRAM_HOME_CHANNEL=your_user_id
```

```yaml
platforms:
  telegram:
    enabled: true
```

## 日常运维

### 常用命令

```bash
# 查看服务状态
sudo systemctl status hermes-gateway.service

# 重启服务
sudo systemctl restart hermes-gateway.service

# 停止服务
sudo systemctl stop hermes-gateway.service

# 查看实时日志
tail -f ~/.hermes/logs/agent.log

# 查看错误日志
tail -f ~/.hermes/logs/errors.log

# 查看 systemd 日志
sudo journalctl -u hermes-gateway.service --no-pager -n 50

# 手动前台运行（调试用）
sudo systemctl stop hermes-gateway.service
/home/$USER/hermes-agent/venv/bin/hermes gateway run -v
```

### 升级 Hermes

```bash
sudo systemctl stop hermes-gateway.service
cd /home/$USER/hermes-agent
git pull
source venv/bin/activate
pip install -e .
hermes --version  # 确认新版本
sudo systemctl start hermes-gateway.service
```

### 切换模型

在聊天中发送 `/model` 查看当前模型和可用选项，或直接编辑 config.yaml。

## 排障指南

### 问题：Gateway 反复重启（5 秒循环）

**症状**：日志中快速出现 "Starting Hermes Gateway..." → "Stopping gateway..." 循环

**排查步骤**：

1. **检查是否有残留进程**：
   ```bash
   ps aux | grep 'hermes.*gateway' | grep -v grep
   ```
   如果有多个 gateway 进程，全部杀掉再重启：
   ```bash
   sudo systemctl stop hermes-gateway.service
   pkill -f 'hermes.*gateway'
   sleep 2
   pkill -9 -f 'hermes.*gateway'  # 强杀
   rm -f ~/.hermes/gateway.pid
   sudo systemctl start hermes-gateway.service
   ```

2. **检查依赖服务**：
   如果 service 配置了 `Requires=xxx.service`，xxx 挂了会连带杀 gateway。改成 `Wants=`：
   ```bash
   sudo systemctl status xxx.service
   # 如果 xxx 在 crash，先修它
   # 然后把 Requires 改成 Wants
   sudo sed -i 's/Requires=xxx.service/Wants=xxx.service/' /etc/systemd/system/hermes-gateway.service
   sudo systemctl daemon-reload
   ```

3. **检查端口冲突**（如有依赖服务）：
   ```bash
   sudo lsof -i :PORT
   # 杀掉占端口的残留进程
   sudo kill <PID>
   ```

### 问题："Unknown provider" / "Provider authentication failed"

**原因**：config.yaml 中 provider 配置语法错误

**修复**：
```yaml
# ✅ 正确 — 用 custom + base_url
model:
  default: "model-name"
  provider: "custom"
  base_url: "https://your-api.com/v1"

# ❌ 错误 — 不要用 providers 字典
providers:
  my-provider:
    ...
```

确保 .env 里有对应的 API key（`OPENAI_API_KEY` 用于 custom provider）。

### 问题："No response generated"

**可能原因**：
1. API key 无效或过期 → 检查 .env 中的 key
2. 模型名称写错 → 确认 API 支持该模型
3. API 额度用完 → 检查账户余额
4. Gateway 不稳定，处理消息前就被杀 → 参考上面的重启循环排查

**快速测试 API 连通性**：
```bash
curl -s https://api.lkeap.cloud.tencent.com/v3/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"glm-5","messages":[{"role":"user","content":"hi"}],"max_tokens":10}' | python3 -m json.tool
```

### 问题：systemd service 启动失败（exit-code 1）

**排查**：
```bash
# 查看详细错误
sudo journalctl -u hermes-gateway.service --no-pager -n 20

# 常见原因：
# 1. ExecStart 路径错误 — 必须用 venv 内的绝对路径
# 2. hermes_cli 找不到 — 不要用系统 Python
# 3. 权限问题 — User 字段要和文件所有者一致
```

### 问题：微信/企微连不上

1. 检查 token 是否过期（iLink 平台查看）
2. 检查 .env 中的配置是否完整
3. 检查 config.yaml 中 platforms 是否 enabled
4. 检查网络连通性（是否能访问 ilinkai.weixin.qq.com）

## 文件结构

```
/home/$USER/
├── hermes-agent/                 # 代码目录
│   ├── venv/                     # Python 虚拟环境
│   │   └── bin/hermes            # CLI 入口
│   ├── gateway/                  # Gateway 核心代码
│   ├── agent/                    # Agent 核心代码
│   ├── hermes_cli/               # CLI 命令
│   └── pyproject.toml
│
├── .hermes/                      # 运行时目录（HERMES_HOME）
│   ├── config.yaml               # 主配置
│   ├── .env                      # 环境变量（API keys）
│   ├── logs/
│   │   ├── agent.log             # 主日志
│   │   └── errors.log            # 错误日志
│   ├── sessions/                 # 会话存储
│   ├── memories/                 # 记忆存储
│   ├── skills/                   # 自学技能
│   ├── gateway.pid               # PID 文件
│   ├── gateway_state.json        # Gateway 状态
│   ├── state.db                  # SQLite 状态数据库
│   ├── SOUL.md                   # 人格文件（可选）
│   ├── IDENTITY.md               # 身份文件（可选）
│   └── USER.md                   # 用户档案（可选）
│
└── /etc/systemd/system/
    └── hermes-gateway.service    # systemd 服务文件
```
