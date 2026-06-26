# 常见问题

## 配对问题

### Q: 配对失败 "No pending pairing request found"

**原因**：配对码已过期（通常几分钟有效）

**解决**：
1. 在飞书中重新发起配对
2. 立即执行 `openclaw pairing approve feishu <新配对码>`

### Q: 配对成功但机器人不回复

**检查步骤**：
1. 确认 Gateway 正在运行：`openclaw gateway status`
2. 确认账号配置正确：`openclaw agents list --bindings`
3. 检查飞书应用是否开启了机器人能力

## 消息问题

### Q: 机器人收不到消息

**可能原因**：
1. 事件订阅未配置
2. 事件未发布
3. 机器人未添加到群聊

**解决**：
1. 飞书开放平台 → 应用 → 事件订阅
2. 添加 `im.message.receive_as_bot`
3. 点击「发布」

### Q: 机器人回复但显示来自另一个账号

**原因**：飞书账号配置错误，检查 `channels.feishu.accounts` 中的 appId/appSecret

## 配置问题

### Q: 如何修改现有 Agent 的绑定账号？

修改 `bindings` 中对应 Agent 的 `accountId`，然后重启 Gateway

### Q: 如何删除一个 Agent？

从 `agents.list` 中移除，从 `bindings` 中移除对应绑定，然后重启

### Q: 不同 Agent 可以使用不同模型吗？

可以，在 `agents.list` 中通过 `model` 字段指定

## 其他

### Q: Gateway 需要重启吗？

修改配置后需要重启：
```bash
openclaw gateway restart
```

### Q: 如何查看 Gateway 日志？

```bash
tail -f /tmp/openclaw/openclaw-2026-03-10.log
```
