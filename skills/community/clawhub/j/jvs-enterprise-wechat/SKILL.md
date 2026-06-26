# 企业微信 AI Bot 配置技能

**一键配置 OpenClaw 与企业微信 AI Bot 的对接**

---

## 📋 功能说明

此技能帮助你快速将 OpenClaw 机器人接入企业微信，使用 AI Bot 模式（WebSocket 长连接）。

**适用场景**：
- ✅ 企业微信用户需要 AI 助手
- ✅ 团队内部部署智能客服
- ✅ 个人工作助手

**无需**：
- ❌ 公网域名
- ❌ HTTPS 证书
- ❌ 回调配置

---

## 🚀 快速开始

### 步骤 1：安装技能

```bash
npx clawhub@latest install wecom-ai-bot-setup
```

### 步骤 2：在企业微信手机端创建 AI Bot

1. 打开 **企业微信 App**（手机）
2. 点击底部「**通讯录**」
3. 找到「**智能机器人**」
4. 点击进入后，选择「**手动创建**」
5. 选择「**API 创建**」方式
6. 填写基本信息：
   - **名称**：如 "HarryBot 助手"
   - **头像**：上传 Logo
   - **简介**：如 "智能工作助手"
7. 创建完成后，**立即生成凭证**

### 步骤 3：获取 Bot 凭证

创建成功后，页面上会显示：

| 字段 | 说明 |
|------|------|
| **Bot ID** | 机器人唯一标识 |
| **Secret** | 机器人密钥 |

⚠️ **重要**：
- **Secret 只显示一次，请立即复制保存！**
- 如果丢失，需要重新生成
- 建议立即保存到安全的地方

### 步骤 4：开通 API 权限（如需要）

如果提示需要开通权限：

1. 打开企业微信管理后台（电脑端）
2. 进入「应用管理」→ 找到你的 AI Bot
3. 开通相关 API 权限
4. 保存后生效

⚠️ **注意**：
- 基础功能手机端即可创建
- 部分高级权限需要在管理后台开通
- 具体权限要求以页面提示为准

### 步骤 4：运行配置脚本

```bash
python3 scripts/setup_wecom.py
```

按提示输入：
- Bot ID
- Secret

### 步骤 5：重启 Gateway

```bash
openclaw gateway restart
```

### 步骤 6：测试连接

1. 打开企业微信 App（手机或电脑）
2. 找到你的 AI Bot（在工作台或聊天列表）
3. 发送消息：`你好`
4. 查看回复

如果机器人回复了，说明配置成功！🎉

---

## 🔧 手动配置（可选）

如果不想用脚本，可以手动编辑配置文件：

### 编辑 `~/.openclaw/openclaw.json`

```json
{
  "channels": {
    "wecom": {
      "enabled": true,
      "botId": "你的 Bot ID",
      "secret": "你的 Secret",
      "model": "保持现有模型配置",
      "dmPolicy": "open"
    }
  }
}
```

然后重启 Gateway：
```bash
openclaw gateway restart
```

---

## 📝 配置参数说明

| 参数 | 必填 | 说明 | 默认值 |
|------|------|------|--------|
| `enabled` | ✅ | 是否启用通道 | `false` |
| `botId` | ✅ | 企业微信 Bot ID | - |
| `secret` | ✅ | 企业微信 Bot Secret | - |
| `model` | ✅ | 使用的模型 | 当前模型 |
| `dmPolicy` | ❌ | 直接消息策略 | `open` |

### dmPolicy 选项

| 值 | 说明 |
|---|------|
| `open` | 所有用户可以直接发消息（推荐） |
| `pairing` | 需要配对码验证 |
| `allowlist` | 只有白名单用户可以发消息 |
| `disabled` | 禁用直接消息 |

---

## 🔍 故障排查

### 问题 1：发送消息没回复

**检查日志**：
```bash
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep -i wecom
```

**可能原因**：
1. Gateway 没运行 → `openclaw gateway status`
2. Bot ID/Secret 错误 → 检查企业微信后台
3. 模型不可用 → 检查模型配置

### 问题 2：找不到 AI Bot

**解决方法**：
1. 打开企业微信 App
2. 「工作台」→「AI 助理」
3. 检查是否已创建
4. 重新打开企业微信 App

### 问题 3：提示"模型不可用"

**解决方法**：
1. 检查配置文件中的 `model` 是否正确
2. 查看当前模型状态：`/session_status`

### 问题 4：插件加载失败

**重新安装插件**：
```bash
openclaw plugins install @wecom/wecom-openclaw-plugin --force
openclaw gateway restart
```

---

## 📊 日志监控

### 实时查看企业微信日志

```bash
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep -i wecom
```

### 正常日志示例

```
[wecom] message received from: [用户 ID]
[wecom] processing message: 你好
[wecom] sending reply to: [用户 ID]
[wecom] Reply message sent via WebSocket, reqId: xxx
```

### 错误日志示例

```
[wecom] failed to connect: invalid botId
[wecom] authentication failed: wrong secret
```

---

## 🔐 安全建议

1. **保护 Secret**
   - 不要提交到 Git
   - 不要公开分享
   - 定期更换

2. **配置访问控制**
   - 生产环境使用 `dmPolicy: "allowlist"`
   - 配置 `allowFrom` 白名单

3. **监控日志**
   - 定期检查异常日志

---

## 📚 相关文档

- [企业微信 AI Bot 官方文档](https://open.work.weixin.qq.com/help?doc_id=21657)
- [OpenClaw 企业微信插件](https://github.com/WecomTeam/wecom-openclaw-plugin)
- [OpenClaw 通道配置](https://docs.openclaw.ai/channels/wecom)

---

## ✅ 配置检查清单

完成配置后，逐项检查：

- [ ] 企业微信 AI Bot 已创建
- [ ] Bot ID 和 Secret 已获取
- [ ] 插件已安装：`openclaw plugins install @wecom/wecom-openclaw-plugin`
- [ ] 配置文件已更新
- [ ] Gateway 已重启
- [ ] 测试消息已发送并收到回复
- [ ] 日志无错误

---

## 🆘 需要帮助？

如果遇到无法解决的问题：

1. **收集信息**：
   - 错误日志（最后 50 行）
   - 配置文件（隐藏 Secret）
   - OpenClaw 版本

2. **提交问题**：
   - GitHub Issues
   - Discord 社区

---

**版本**: 1.0.0  
**作者**: harrybot  
**许可**: MIT-0（免费使用，无需署名）
