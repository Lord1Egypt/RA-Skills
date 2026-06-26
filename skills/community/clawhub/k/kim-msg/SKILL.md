---
name: kim-msg
description: 快手 Kim 即时通讯消息发送。支持 Webhook（群聊）和消息号（指定用户）两种方式，内置智能密钥加载和 fallback 机制。适用于通知、告警、日报等场景。官网：https://kim.kuaishou.com/
---

# Kim 消息发送（快手 IM）

## 概述

Kim 是快手的企业即时通讯工具，支持两种发送消息的方式：

1. **Webhook 方式** - 需要 Kim 机器人 Token，向机器人所在的群聊发送消息
2. **消息号方式** - 需要 appKey + secretKey，可以直接发送给指定用户（快手邮箱前缀）

官方网站：https://kim.kuaishou.com/

## 首次配置

首次使用前，需要选择一种方式并配置相应的凭证：

### Webhook 方式
需要从 Kim 机器人获取 Webhook Token，告诉晴晴帮你配置。

### 消息号方式
需要提供：
- **appKey**: Kim 应用 Key
- **secretKey**: Kim 应用 Secret
- **用户名**: 要发送消息的目标用户（必须是快手邮箱前缀，如 `wangyang`，不是完整邮箱 `wangyang@kuaishou.com`）

## 使用方法

### 方式一：Webhook 发送

```bash
# 发送 Markdown 消息到群聊
kim-msg/webhook.sh "**标题**\n\n正文内容"

# 发送纯文本
kim-msg/webhook.sh "Hello World" --text
```

### 方式二：消息号发送

**推荐：使用包装脚本（自动加载密钥）**
```bash
# 发送消息给指定用户（用户名必须是邮箱前缀，如 wangyang）
kim-msg/send.sh -u <邮箱前缀> -m "消息内容"

# 示例
kim-msg/send.sh -u wangyang -m "**提醒**：今天有会议"
```

**或直接调用 Node 脚本（需自行设置环境变量）**
```bash
export KIM_APP_KEY=your_app_key
export KIM_SECRET_KEY=your_secret_key
kim-msg/message.js -u <邮箱前缀> -m "消息内容"
```

> ⚠️ 首次使用如果遇到权限错误，运行：`chmod +x scripts/*.sh`

## API 详情

### Webhook
- **URL:** `https://kim-robot.kwaitalk.com/api/robot/send?key=<key>`
- **Method:** POST
- **Body:**
```json
{
  "msgtype": "markdown",
  "markdown": {"content": "消息内容"}
}
```

### 消息号
- **获取 Token:** `https://is-gateway.corp.kuaishou.com/token/get?appKey=<appKey>&secretKey=<secretKey>`
- **发送消息:** 自动尝试以下两个接口：
  - 单用户：`/openapi/v2/message/send`（`username` 单个用户）
  - 批量：`/openapi/v2/message/batch/send`（`usernames` 数组）
  - **自动重试：** 优先尝试单用户接口，失败则尝试批量接口
- **Headers:** `Authorization: Bearer <token>`
- **Body:**
```json
{
  "msgType": "markdown",
  "markdown": {"content": "消息内容"},
  "usernames": ["用户名"]
}
```

## 密钥配置方式

### 优先级：环境变量 > 密钥文件

脚本内置智能密钥加载机制，按以下优先级查找：

1. **环境变量**（最高优先级）
   - `KIM_WEBHOOK_TOKEN`（Webhook 方式）
   - `KIM_APP_KEY` / `KIM_SECRET_KEY`（消息号方式）

2. **密钥文件**（自动 fallback）
   
   如果环境变量未设置或发送失败，脚本会自动从以下位置查找密钥（按优先级）：
   - `~/.openclaw/.secrets`（OpenClaw 统一密钥管理）
   - `~/.kim_credentials`（Kim 专用密钥文件）
   - `./kim_credentials`（项目本地密钥文件）

   **文件格式：**
   ```
   KIM_APPKEY=your_app_key
   KIM_SECRET=your_secret_key
   ```

   **Webhook Token 格式：**
   ```
   KIM_WEBHOOK_TOKEN=your_webhook_token
   ```

> 💡 **提示：**
> - 密钥文件权限建议设置为 `600`（仅所有者可读写）：`chmod 600 ~/.openclaw/.secrets`
> - 触发 fallback 时，脚本会输出警告提示，但不会暴露密钥文件路径
> - 推荐本地开发使用密钥文件，CI/CD 使用环境变量

## 注意事项

- 不硬编码任何 API Key/Token
- 消息内容需合规
- API 异常时检查凭证和网络
- 用户名必须是快手邮箱前缀（如 `wangyang`），不是完整邮箱

## 源码

GitHub: https://github.com/LeeGoDamn/kim-msg-skill
