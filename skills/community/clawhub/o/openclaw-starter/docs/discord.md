# Discord 渠道配置指南

## 步骤

### 1. 创建 Discord 应用

1. 打开 [Discord 开发者门户](https://discord.com/developers/applications)
2. 点击 **New Application**
3. 输入应用名称（如：`My Assistant`）
4. 点击 **Create**

### 2. 创建 Bot

1. 进入 **Bot** 标签
2. 点击 **Add Bot** → **Yes, do it!**
3. 点击 **Reset Token** 获取 Bot Token
4. **复制并保存 Token**（只显示一次）

### 3. 设置权限

在 **OAuth2** → **URL Generator**：
1. 勾选 **bot** 作用域
2. 在权限中选择：
   - `Send Messages`
   - `Read Message History`
   - `Embed Links`
3. 复制生成的 URL

### 4. 邀请 Bot

1. 在浏览器打开生成的 URL
2. 选择要添加的服务器
3. 点击 **Authorize**

### 5. 配置 OpenClaw

```bash
openclaw configure --section discord
```

输入 Bot Token。

### 6. 获取 Channel ID

在 Discord 中：
1. 设置 → 高级 → 开启 **开发者模式**
2. 右键点击频道 → **复制 ID**

## 配置示例

```yaml
channels:
  discord:
    botToken: "YOUR_BOT_TOKEN"
    channelId: "123456789012345678"
```

## 常见问题

### Q: Bot 没有响应？
A: 检查 Bot 是否有发送消息权限。

### Q: Token 无效？
A: 重新生成 Token，确保没有多余字符。

### Q: 如何删除 Bot？
A: 在开发者门户删除应用。

## 参考链接

- [Discord 开发者文档](https://discord.com/developers/docs)
- [OpenClaw Discord 文档](https://docs.openclaw.ai/channels/discord)
