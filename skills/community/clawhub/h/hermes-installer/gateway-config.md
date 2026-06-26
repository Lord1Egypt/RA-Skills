# 网关配置（飞书/Telegram/Discord）

---

## 飞书网关配置

### 1. 创建飞书应用

1. 访问 [飞书开放平台](https://open.feishu.cn/app)
2. 创建企业自建应用
3. 记录 App ID 和 App Secret

### 2. 配置应用权限

| 权限名称 | 权限标识 |
|---------|---------|
| 获取用户信息 | `contact:user.base:readonly` |
| 接收消息 | `im:message` |
| 发送消息 | `im:message:send_as_bot` |
| 获取群信息 | `im:chat:readonly` |

### 3. 配置事件订阅

- 请求网址：`https://your-server.com/webhook/feishu`
- 订阅事件：`im.message.receive_v1`

### 4. 安装依赖

```bash
uv pip install lark-oapi aiohttp websockets
```

### 5. 配置环境变量

```bash
# ~/.hermes/.env
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=xxx
FEISHU_ENABLED=true
GATEWAY_ALLOWED_USERS=ou_xxx
```

### 6. 启动网关

```bash
hermes gateway run
```

### 7. 配对用户

```bash
hermes pairing approve feishu PAIRING_CODE
```

---

## Telegram 网关配置

### 1. 创建 Telegram Bot

1. 在 Telegram 中搜索 `@BotFather`
2. 发送 `/newbot`
3. 按提示设置名称和用户名
4. 记录 Bot Token

### 2. 配置环境变量

```bash
# ~/.hermes/.env
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_ENABLED=true
```

### 3. 配对用户

```bash
hermes pairing approve telegram PAIRING_CODE
```

---

## Discord 网关配置

### 1. 创建 Discord Bot

1. 访问 [Discord Developer Portal](https://discord.com/developers/applications)
2. 创建应用 → Bot → Add Bot
3. 记录 Bot Token
4. 生成邀请链接（Scopes: bot, Permissions: Send/Read Messages）

### 2. 配置环境变量

```bash
# ~/.hermes/.env
DISCORD_BOT_TOKEN=xxx
DISCORD_ENABLED=true
```

### 3. 配对用户

```bash
hermes pairing approve discord PAIRING_CODE
```

---

## 多网关同时运行

```bash
# ~/.hermes/.env
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=xxx
FEISHU_ENABLED=true

TELEGRAM_BOT_TOKEN=xxx
TELEGRAM_ENABLED=true

DISCORD_BOT_TOKEN=xxx
DISCORD_ENABLED=true

GATEWAY_ALLOWED_USERS=ou_xxx,ou_yyy
```

---

## 用户白名单

```bash
# 多个用户用逗号分隔
GATEWAY_ALLOWED_USERS=ou_xxx,ou_yyy,ou_zzz
```

---

## 网关管理命令

| 命令 | 说明 |
|------|------|
| `hermes gateway status` | 查看网关状态 |
| `hermes gateway start/stop` | 启停网关 |
| `hermes pairing list` | 查看已配对用户 |
| `hermes pairing approve feishu CODE` | 批准飞书用户 |
| `hermes pairing approve telegram CODE` | 批准 Telegram 用户 |
| `hermes pairing approve discord CODE` | 批准 Discord 用户 |

---

## 故障排查

### 飞书连接失败

```bash
hermes gateway status
cat ~/.hermes/logs/agent.log
```

### 用户被拒绝

```bash
hermes config show | grep -A5 allowed
hermes pairing approve feishu CODE
```
