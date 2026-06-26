---
name: imap-idle-sneder
description: 使用 IMAP IDLE 保持长连接实时监听新邮件，并发送给指定飞书账号。当需要：1）监听新邮件并实时推送通知，2）建立邮件推送服务，3）替代轮询检查新邮件时使用此 skill。
---

# IMAP IDLE 邮件监听

使用 IMAP IDLE 模式保持长连接，实时接收服务器推送的新邮件通知。

## 快速开始

### 1. 运行监听脚本

```bash
python ~/.openclaw/skills/imap-idle/scripts/imap_idle.py
```

脚本会在后台保持运行，收到新邮件时：
- 控制台打印通知
- 写入通知文件：`~/.openclaw/workspace/mail_notifications.json`

### 2. 配置自启动（可选）

使用 OpenClaw cron 定时检查通知文件，或配置系统服务开机启动。

## 配置修改

如需修改邮箱配置，编辑 `scripts/imap_idle.py`：

```python
IMAP_SERVER = "imap.qq.com"  # IMAP 服务器
IMAP_PORT = 993               # 端口
EMAIL = "你的邮箱@qq.com"      # 邮箱账号
PASSWORD = "你的授权码"        # 授权码
```

## 支持的邮箱

- QQ 邮箱 ✓
- Gmail（需使用 App Password）
- Outlook
- 其他支持 IMAP IDLE 的邮箱

## 通知文件格式

`mail_notifications.json` 内容示例：

```json
[
  {
    "subject": "邮件主题",
    "from": {
      "name": "发件人姓名",
      "email": "from@example.com"
    },
    "date": "Thu, 26 Feb 2026 10:30:00 +0800",
    "received_at": "2026-02-26T10:30:00"
  }
]
```

## 与飞书集成

新邮件到达时自动发送飞书通知（卡片消息）：
- 📧 显示发件人姓名和邮箱
- 📝 显示邮件主题
- 📄 显示邮件摘要（前200字）

**飞书配置**（从 openclaw.json 自动获取）：
- 发送给用户 飞书ID: `ou_febxxxxxxxxxxxxxxxx`

如需修改接收人，编辑 `scripts/imap_idle.py` 中的 `FEISHU_USER_ID`。

## 注意事项

- 需要邮箱开启 IMAP 服务
- QQ/Gmail 等需要使用**授权码**而非登录密码
- IDLE 超时后会自动重连
