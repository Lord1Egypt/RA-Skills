# Kim 消息发送 Skill 🤖

快手 Kim 即时通讯消息发送 AI Skill，支持 Webhook 和消息号两种方式，内置智能密钥加载和 fallback 机制。

适用于向 Kim 推送通知、告警、日报等场景。

## 📱 什么是 Kim？

Kim 是快手的企业即时通讯工具，官网：https://kim.kuaishou.com/

## 🚀 支持的 AI 平台

| 平台 | 支持 |
|------|------|
| OpenClaw | ✅ |
| Cursor | ✅ |
| Claude Code | ✅ |
| VS Code AI | ✅ |
| 其他能执行命令的 AI | ✅ |

## 📦 安装方式

### 方式一：OpenClaw / ClawHub

```bash
clawhub install kim-msg
```

### 方式二：GitHub 克隆

```bash
git clone https://github.com/LeeGoDamn/kim-msg-skill.git
```

## ⚙️ 配置

### 方式一：Webhook（向群聊发消息）

**环境变量：**
```bash
export KIM_WEBHOOK_TOKEN="your-webhook-token"
```

**密钥文件（推荐）：**
在以下任一位置创建密钥文件：
- `~/.openclaw/.secrets`
- `~/.kim_credentials`
- `./kim_credentials`

文件格式：
```
KIM_WEBHOOK_TOKEN=your-webhook-token
```

### 方式二：消息号（向指定用户发消息）

**环境变量：**
```bash
export KIM_APP_KEY="your-app-key"
export KIM_SECRET_KEY="your-secret-key"
```

**密钥文件（推荐）：**
在以下任一位置创建密钥文件：
- `~/.openclaw/.secrets`
- `~/.kim_credentials`
- `./kim_credentials`

文件格式：
```
KIM_APPKEY=your-app-key
KIM_SECRET=your-secret-key
```

> 💡 **提示：**
> - 脚本内置智能密钥加载，优先使用环境变量，自动 fallback 到密钥文件
> - 密钥文件权限建议设置为 `600`：`chmod 600 ~/.openclaw/.secrets`
> - 触发 fallback 时会输出警告，但不会暴露文件路径

## 📖 使用方法

### Webhook 方式

```bash
# 发送 Markdown 消息到群聊
./scripts/webhook.sh "**标题**\n\n正文内容"

# 发送纯文本
./scripts/webhook.sh "Hello World" --text
```

### 消息号方式

```bash
# 发送消息给指定用户（必须是邮箱前缀，如 wangyang）
./scripts/send.sh -u wangyang -m "**提醒**：今天有会议"

# 或直接调用 Node 脚本
export KIM_APP_KEY="your-app-key"
export KIM_SECRET_KEY="your-secret-key"
./scripts/message.js -u wangyang -m "消息内容"
```

> ⚠️ 如果遇到 "permission denied" 错误，先运行：`chmod +x scripts/*.sh`

## 🔐 安全特性

- **智能密钥加载** - 环境变量优先，自动 fallback 到密钥文件
- **不硬编码密钥** - 所有凭证通过环境变量或密钥文件传递
- **敏感信息不上传** - 密钥只存在于本地，不会发布到仓库
- **多路径支持** - 自动查找常用密钥文件位置

## 🔧 故障排查

### 发送失败：用户不在可见范围
- 确认用户名是快手邮箱前缀（如 `wangyang`，不是 `wangyang@kuaishou.com`）
- 确认对方已授权此 Kim 应用
- 联系应用管理员添加用户到可见范围

### 找不到密钥
- 检查环境变量是否正确设置
- 检查密钥文件是否存在且格式正确
- 确认密钥文件权限：`chmod 600 ~/.openclaw/.secrets`

## 📝 License

MIT

---

Made with ❤️ by [LeeGoDamn](https://github.com/LeeGoDamn)
