# WhatsApp 渠道配置指南

## 步骤

### 1. 启动配置

```bash
openclaw configure --section whatsapp
```

OpenClaw 会显示一个二维码。

### 2. 扫描二维码

1. 打开手机 WhatsApp
2. 点击右上角菜单（Android）或设置（iOS）
3. 选择 **已连接的设备**
4. 点击 **连接设备**
5. 扫描二维码

### 3. 确认连接

扫描成功后，WhatsApp 会显示"已连接"，OpenClaw 会显示配置成功。

## 注意事项

- ⚠️ 二维码 60 秒后过期，超时需重新生成
- ⚠️ 确保手机和网络连接正常
- ⚠️ 不要同时在多个设备登录同一 WhatsApp 账号

## 常见问题

### Q: 二维码无法扫描？
A: 检查屏幕亮度，确保摄像头清晰。

### Q: 连接后断开？
A: 检查网络，重新运行配置命令。

### Q: 如何断开连接？
A: 在手机 WhatsApp 的"已连接的设备"中点击断开。

## 参考链接

- [OpenClaw WhatsApp 文档](https://docs.openclaw.ai/channels/whatsapp)
