# Notification Configuration

This skill is **platform-agnostic**. It does not hardcode any notification channel. Users configure their own notification method based on their platform.

> **Note**: The examples below use OpenClaw's built-in cron system, which is the simplest way to set up reminders. If you're using a different platform, adapt the examples accordingly.

## Option 1: OpenClaw Built-in Cron (Recommended)

If you're running OpenClaw, use its built-in cron system. It supports all configured channels automatically.

### Setup

```bash
openclaw cron add \
  --name "med-{member}-{drug}" \
  --schedule "0 8 * * *" \
  --agent-id your-agent \
  --message "⏰ 用药提醒\n\n💊 {药品名}\n剂量：{剂量}\n用法：{饭前/饭后}\n\n请按时服药！"
```

### Common Schedules

| Schedule | Cron | Example |
|----------|------|---------|
| Daily morning | `0 8 * * *` | 每天早上 8:00 |
| Twice daily | `0 8 * * *` + `0 20 * * *` | 早 8 点 + 晚 8 点 |
| Three times daily | `0 8 * * *` + `0 12 * * *` + `0 20 * * *` | 早中晚 |
| Weekly expiry check | `0 9 * * 1` | 每周一 9:00 |
| Monthly inventory | `0 9 1 * *` | 每月 1 号 9:00 |

### Target Channels

OpenClaw supports multiple channels. Set the `--target` based on your channel:

| Channel | Target Format | Example |
|---------|--------------|---------|
| Feishu | `feishu:{open_id}` | `feishu:ou_xxxxx` |
| Telegram | `telegram:{chat_id}` | `telegram:-1001234567` |
| QQ Bot | `qqbot:c2c:{openid}` | `qqbot:c2c:xxxxx` |
| Discord | `discord:{channel_id}` | `discord:123456789` |

> **Tip**: Omit `--target` to send to the current conversation (auto-detected).

### Management Commands

```bash
# List all medication reminders
openclaw cron list

# Remove a reminder
openclaw cron remove med-zhangsan-amoxicillin

# Pause a reminder (disable without deleting)
openclaw cron disable med-zhangsan-amoxicillin

# Resume a paused reminder
openclaw cron enable med-zhangsan-amoxicillin
```

## Option 2: Webhook Notifications

If you have a webhook-based notification service (e.g., DingTalk, WeChat Work, Slack):

```
POST YOUR_WEBHOOK_URL
Content-Type: application/json

{
  "msgtype": "text",
  "text": {
    "content": "⏰ 用药提醒\n\n💊 {药品名}\n剂量：{剂量}\n\n请按时服药！"
  }
}
```

### Webhook Templates (for reference)

#### DingTalk (钉钉)
```json
POST https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN

{
  "msgtype": "markdown",
  "markdown": {
    "title": "用药提醒",
    "text": "### ⏰ 用药提醒\n\n- **药品**：{药品名}\n- **剂量**：{剂量}"
  }
}
```

#### WeChat Work (企业微信)
```json
POST https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY

{
  "msgtype": "text",
  "text": {
    "content": "⏰ 用药提醒\n\n💊 {药品名}\n剂量：{剂量}"
  }
}
```

#### Slack
```json
POST https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK

{
  "text": ":pill: Medication Reminder",
  "blocks": [
    {"type": "header", "text": {"type": "plain_text", "text": "⏰ 用药提醒"}},
    {"type": "section", "text": {"type": "mrkdwn", "text": "*药品*\n{药品名}"}}
  ]
}
```

## Agent Implementation Guide

When implementing reminders, the AI agent should:

### 1. Detect the User's Platform

Check the current conversation context to determine the channel:
- If Feishu → use `message` tool or OpenClaw cron with feishu target
- If Telegram → use Telegram bot API or cron
- If QQ → use qqbot_remind/qqbot_cron
- If webchat → suggest setting up a notification method

### 2. Store Notification Config in Member Profile

Add to `data/members/{name}.md`:

```markdown
## Notification Settings
| Setting | Value |
|---------|-------|
| Channel | feishu / telegram / webhook / custom |
| Target | {user_openid or chat_id} |
| Preferred Times | 08:00, 20:00 |
| Quiet Hours | 22:00 - 07:00 |
```

### 3. Create Reminders with User Confirmation

Before creating any reminder:

1. Show the user the proposed schedule
2. Confirm the notification method
3. Create the reminder
4. Test it (send one immediately to verify)
5. Record in the member profile

### 4. Handle Missed Reminders

If a user reports missing a dose:

1. Log it in `data/logs/YYYY-MM-DD.md` with status `missed`
2. Check if the reminder cron is still active
3. If needed, recreate the reminder
4. Ask if the reminder time needs adjustment

## Notification Content Templates

### Standard Medication Reminder
```
⏰ 用药提醒

💊 {药品名}
剂量：{剂量}
用法：{饭前/饭后/随餐}
成员：{姓名}

请按时服药！
```

### Expiry Alert
```
⚠️ 药品过期预警

📦 {药品名} [{批次号}]
过期日期：{过期日期}
剩余天数：{天数} 天
当前库存：{数量}{单位}

建议：{尽快使用 / 准备替换 / 立即丢弃}
```

### Course Completion Reminder
```
✅ 疗程即将结束

💊 {药品名}
已服用：{已用天数}/{总天数}
预计结束：{结束日期}

{如果还没吃完，请完成整个疗程}
{如果已吃完，请记录并更新库存}
```

## Configuration File (Optional)

Create `data/config/notifications.yaml` for centralized notification settings:

```yaml
# Default notification channel
default_channel: feishu

# Channel-specific targets
channels:
  feishu:
    target: "ou_xxxxx"
  telegram:
    chat_id: "-1001234567"
  webhook:
    url: "https://example.com/webhook"

# Global quiet hours (no notifications during this time)
quiet_hours:
  start: "22:00"
  end: "07:00"

# Retry settings
retry:
  max_attempts: 3
  interval_minutes: 5
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Reminders not being sent | Check if cron job is active: `openclaw cron list` |
| Wrong channel | Verify `--target` parameter matches your channel |
| Message not delivered | Check channel permissions and bot status |
| Duplicate reminders | Check for duplicate cron entries |
| Timezone issues | Ensure system timezone matches your local timezone |
