# Telegram 渠道配置指南

## 步骤

### 1. 创建 Bot

1. 打开 Telegram，搜索 `@BotFather`
2. 发送 `/newbot` 命令
3. 设置机器人名称（如：`My Assistant Bot`）
4. 设置机器人用户名（如：`my_assistant_bot`，必须以 `bot` 结尾）

### 2. 获取 Token

BotFather 会返回类似以下信息：
```
Use this token to access the HTTP API:
123456789:ABCdefGHIjklMNOpqrsTUVwxyz

Keep your token secure and store it safely.
```

### 3. 配置 OpenClaw

```bash
openclaw configure --section telegram
```

按提示输入 Token。

### 4. 测试

在 Telegram 中搜索你的机器人用户名，发送 `/start` 测试。

## 常见问题

### Q: 机器人没有响应？
A: 检查 Gateway 是否运行：`openclaw gateway status`

### Q: Token 无效？
A: 重新从 BotFather 获取 Token，确保没有多余空格。

### Q: 如何删除 Bot？
A: 在 BotFather 发送 `/deletebot`，选择要删除的机器人。

## 参考链接

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [OpenClaw Telegram 文档](https://docs.openclaw.ai/channels/telegram)
