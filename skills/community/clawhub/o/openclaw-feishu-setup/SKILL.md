# OpenClaw 飞书 Setup

15 分钟配置飞书机器人作为 OpenClaw 消息渠道。

## 为什么选飞书？

- **企业首选**：字节跳动出品，国内企业广泛使用
- **功能强大**：消息、文档、日历、会议一体化
- **开放平台**：丰富的 API 和机器人能力
- **免费版够用**：小团队免费使用

## 快速配置

### Step 1: 创建飞书应用

1. 访问 https://open.feishu.cn/app
2. 点击 "创建企业自建应用"
3. 设置名称（如 "AI 助手"）
4. 保存 **App ID** 和 **App Secret**

### Step 2: 配置权限

在应用管理 > 权限管理中，开启：
- `im:message` - 获取与发送单聊、群组消息
- `im:message:send_as_bot` - 以应用身份发消息

### Step 3: 配置事件订阅

1. 在 "事件订阅" 页面启用
2. 配置 OpenClaw Gateway 的公网地址（需要内网穿透或云服务器）
3. 订阅事件：
   - `im.message.receive_v1` - 接收消息

### Step 4: 配置 OpenClaw

编辑 `~/.openclaw/config.yaml`:

```yaml
plugins:
  entries:
    - plugin: openclaw-feishu
      config:
        appId: "cli_xxxxxxxxxx"
        appSecret: "xxxxxxxxxxxxxx"
        encryptKey: "xxxx"  # 可选，用于消息加密
        verificationToken: "xxxx"  # 可选，用于验证
```

### Step 5: 发布应用

1. 在飞书开放平台提交审核
2. 审核通过后，添加到企业可用范围
3. 在飞书中搜索你的应用，开始对话

### Step 6: 启动 Gateway

```bash
openclaw gateway start
```

## 内网穿透方案

如果没有公网 IP，可以用：

### 方案 1：ngrok（推荐）

```bash
ngrok http 3000
# 将生成的 https://xxx.ngrok.io 配置到事件订阅
```

### 方案 2：cloudflared

```bash
cloudflared tunnel --url http://localhost:3000
```

### 方案 3：Tailscale Funnel

```bash
tailscale funnel 3000
```

## 高级功能

### 群聊支持

```yaml
plugins:
  entries:
    - plugin: openclaw-feishu
      config:
        appId: "xxx"
        appSecret: "xxx"
        enableGroupChat: true
        groupTriggerPrefix: "@AI助手"  # 群聊触发前缀
```

### 富文本消息

OpenClaw 自动将 Markdown 转换为飞书富文本卡片。

### 多租户支持

```yaml
tenants:
  - appId: "cli_xxx1"
    appSecret: "xxx1"
  - appId: "cli_xxx2"
    appSecret: "xxx2"
```

## 常见问题

### Q: 提示 "app not found"
A: 检查 App ID 是否正确，应用是否已发布

### Q: 收不到消息
A: 检查事件订阅是否配置正确，Gateway 是否运行

### Q: 提示 "permission denied"
A: 确保已开启 `im:message` 相关权限

### Q: 如何在群聊中使用？
A: 配置 `enableGroupChat: true`，并设置触发前缀

## 成本

- 飞书开放平台：**完全免费**
- OpenClaw Gateway：本地运行，无费用
- AI 模型：按使用量计费

## 安全建议

1. **不要**公开 App Secret
2. 启用消息加密（encryptKey）
3. 定期轮换密钥
4. 限制应用可用范围

## 需要帮助？

- 微信：yanghu_ai
- Telegram: @yanghu_openclaw
- 飞书配置服务：¥99（远程协助）

---

Version: 1.0.0
Created: 2026-03-21
