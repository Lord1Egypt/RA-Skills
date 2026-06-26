# OpenClaw Discord Setup

10 分钟配置 Discord Bot 作为 OpenClaw 消息渠道。

## 为什么选 Discord？

- **社区友好**：适合团队/社区运营
- **免费无限制**：消息、语音、文件全免费
- **功能丰富**：Slash 命令、按钮、Embeds
- **开发者生态**：完善的 API 和 SDK

## 快速配置

### Step 1: 创建 Discord 应用

1. 访问 https://discord.com/developers/applications
2. 点击 "New Application"
3. 设置名称（如 "My AI Assistant"）
4. 进入 "Bot" 页面，点击 "Add Bot"
5. 保存 **Token**

### Step 2: 邀请 Bot 到服务器

在 "OAuth2" > "URL Generator" 中：
- Scopes: `bot`, `applications.commands`
- Permissions: 
  - Send Messages
  - Read Messages
  - Use Slash Commands

复制生成的链接，在浏览器打开，选择服务器授权。

### Step 3: 配置 OpenClaw

编辑 `~/.openclaw/config.yaml`:

```yaml
plugins:
  entries:
    - plugin: openclaw-discord
      config:
        botToken: "YOUR_BOT_TOKEN"
        clientId: "YOUR_CLIENT_ID"
        allowedGuildIds:
          - "123456789"  # 服务器 ID
```

### Step 4: 启动 Gateway

```bash
openclaw gateway start
```

### Step 5: 测试

在 Discord 频道 @你的 Bot，应该收到 AI 回复。

## 高级功能

### Slash 命令

```yaml
plugins:
  entries:
    - plugin: openclaw-discord
      config:
        botToken: "xxx"
        slashCommands:
          - name: "ask"
            description: "Ask AI a question"
          - name: "clear"
            description: "Clear conversation history"
```

### 多服务器支持

```yaml
allowedGuildIds:
  - "123456789"
  - "987654321"
```

### 私信支持

```yaml
allowDM: true
```

### Embed 消息（更美观）

OpenClaw 会自动格式化回复为 Embed 样式。

## 常见问题

### Q: Bot 不响应
A: 检查 Bot Token 是否正确，确保 Bot 在服务器中

### Q: "Missing Access" 错误
A: 重新生成邀请链接，确保勾选了必要权限

### Q: Slash 命令不显示
A: 命令注册需要时间（最多 1 小时），或重启 Gateway

### Q: 如何获取服务器 ID？
A: Discord 设置 > 高级 > 开发者模式，然后右键服务器 > 复制 ID

## 成本

- Discord Bot API：**完全免费**
- OpenClaw Gateway：本地运行，无费用
- AI 模型：按使用量计费

## 安全建议

1. **不要**公开 Bot Token
2. 定期重新生成 Token
3. 只允许信任的服务器 ID
4. 在生产环境使用环境变量

```bash
export DISCORD_BOT_TOKEN="your-token-here"
```

## 需要帮助？

- 微信：yanghu_ai
- Telegram: @yanghu_openclaw
- 免费远程配置（首次）

---

Version: 1.0.0
Created: 2026-03-21
