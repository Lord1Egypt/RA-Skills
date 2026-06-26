---
name: last-words
description: Auto-deliver final messages to loved ones after 30 days of inactivity. Use when user wants to record a final message, configure email delivery, manage voice messages, or check configuration status.
---

# Last Words - 最后留言

Manage final messages to be delivered to loved ones when the user is unreachable for an extended period.

## Overview

This skill helps users record a final message (voice or text) to be delivered to their parents or loved ones if they haven't been active for 30 days. The system:

1. Records and stores the final message securely (text + optional voice/audio)
2. Monitors user activity via chat history
3. Sends warning notifications at 10 and 20 days of inactivity
4. Automatically delivers the message after 30 days of no activity (email includes voice as attachment if available)
5. Supports delivery via email (WeChat and phone are planned)

## Workflow

### 1. Record a Final Message

When user says something like "我想给我爸妈留下最后一句话":

1. Respond: "可以，请说吧，顺便提醒一下这句话默认设置半个月没和我聊天记录的话就会自动触发"
2. Accept voice or text input as the message content
3. Save the message using: `scripts/save_message.py --message "content" [--audio-path path]`
4. Confirm: "已保存，请确认发送形式：邮件 或 微信"

### 2. Configure Delivery Settings

Ask user to choose delivery method:
- **邮件**: Collect email address
- **微信**: Collect WeChat ID (placeholder - not yet implemented)
- **电话**: Collect phone number (placeholder - not yet implemented)

Save settings using: `scripts/configure_delivery.py --method email --contact "address@example.com"`

### 3. Interactive Email Configuration (Chat)

Users can configure email settings through natural chat conversation:

**Trigger phrases:**
- "配置最后留言邮箱"
- "设置最后留言邮箱"
- "最后留言 配置邮箱"
- "最后留言 设置邮箱"
- "修改最后留言邮箱"

**Interactive flow:**

1. **Ask for sender email:**
   - Respond: "请提供你的发件邮箱（用于发送留言的邮箱，目前支持QQ邮箱）："
   - Wait for user input: e.g., "your-email@qq.com"

2. **Ask for authorization code:**
   - Respond: "请提供邮箱授权码（不是登录密码）。QQ邮箱授权码获取方式：登录QQ邮箱→设置→账户→开启POP3/SMTP服务→获取授权码："
   - Wait for user input: e.g., "xxxxxxxxxxxxxxxx"

3. **Ask for recipient email:**
   - Respond: "请提供收件人邮箱（父母/亲人的邮箱）："
   - Wait for user input: e.g., "parent@example.com"

4. **Confirm and save:**
   - Show summary: "配置确认：\n发件人：{smtp_user}\n收件人：{contact}\n是否确认保存？（确认/取消）"
   - If user confirms:
     - Run: `python3 scripts/configure_delivery.py --method email --contact "{contact}" --smtp-host smtp.qq.com --smtp-port 465 --smtp-user "{smtp_user}" --smtp-pass "{smtp_pass}"`
     - Respond: "✓ 邮箱配置已保存。正在测试邮件发送..."
     - Run test: `python3 scripts/debug_mode.py on` then `python3 scripts/debug_mode.py send`
     - Respond with result
   - If user cancels: "已取消配置。"

**Security notes for interactive config:**
- Passwords are masked in chat display (e.g., "授权码已收到：************")
- Credentials are stored locally only
- User can reconfigure anytime by saying "修改最后留言邮箱"

### 4. Voice/Audio Support

Users can attach a voice recording to their message:

**Option A: Save existing audio file**
```bash
python3 scripts/audio_manager.py save /path/to/recording.wav
```

**Option B: Record from microphone (if available)**
```bash
python3 scripts/audio_manager.py record
```

**Play back saved audio:**
```bash
python3 scripts/audio_manager.py play
```

**List all saved audio files:**
```bash
python3 scripts/audio_manager.py list
```

The audio file will be attached to the email when the final message is delivered.

### 5. Debug Mode Management (Chat)

Users can manage debug mode through normal chat conversation by explicitly mentioning "最后留言":

**Enable debug mode:**
When user says: "最后留言 开启调试模式", "最后留言 打开调试", or "最后留言 启用调试"
1. Run: `python3 scripts/debug_mode.py on`
2. Respond: "最后留言调试模式已开启。现在可以立即发送测试消息，无需等待30天。"

**Disable debug mode:**
When user says: "最后留言 关闭调试模式" or "最后留言 禁用调试"
1. Run: `python3 scripts/debug_mode.py off`
2. Respond: "最后留言调试模式已关闭。系统恢复正常运行（30天无活动后发送）。"

**Check debug mode status:**
When user says: "最后留言 调试模式状态" or "最后留言 调试状态"
1. Run: `python3 scripts/debug_mode.py status`
2. Show current status and configuration summary

**Send immediate test (when debug mode is on):**
When user says: "最后留言 立即发送测试" or "最后留言 测试发送"
1. Run: `python3 scripts/debug_mode.py send`
2. Report result: delivery success/failure details

### 6. Daily Check Process

Run `scripts/check_activity.py` daily via cron to:
- Check last chat timestamp
- Send warning at 10 days of inactivity
- Send warning at 20 days of inactivity
- Deliver final message at 30 days of inactivity (with audio attachment if available)

## Commands Reference

### Save Message (text only)
```bash
python3 scripts/save_message.py --message "爸爸妈妈我爱你们"
```

### Save Message with Audio
```bash
# First save the audio file
python3 scripts/audio_manager.py save /path/to/voice-recording.wav

# Or record directly (requires microphone)
python3 scripts/audio_manager.py record
```

### Configure Delivery
```bash
python3 scripts/configure_delivery.py --method email --contact "parent@example.com"
# Methods: email, wechat, phone
```

### Audio Management
```bash
python3 scripts/audio_manager.py save /path/to/audio.wav   # Save existing audio
python3 scripts/audio_manager.py record                    # Record from mic
python3 scripts/audio_manager.py play                      # Play saved audio
python3 scripts/audio_manager.py list                      # List all audio files
```

### Check Activity (run daily)
```bash
python3 scripts/check_activity.py
```

### Get Status
```bash
python3 scripts/get_status.py
```

### Reset/Clear Data
```bash
python3 scripts/reset.py
```

### Debug Mode (Testing)

Enable debug mode to bypass the 30-day wait and test immediate delivery:

**Enable/Disable debug mode:**
```bash
python3 scripts/debug_mode.py on       # Enable debug mode
python3 scripts/debug_mode.py off      # Disable debug mode
python3 scripts/debug_mode.py status   # Check debug mode status
```

**Immediate send in debug mode:**
```bash
python3 scripts/debug_mode.py send     # Send message immediately (debug)
```

Or use the check script with debug flag:
```bash
python3 scripts/check_activity.py --debug-send  # Force immediate send
```

**When debug mode is enabled:**
- Messages can be sent immediately without waiting 30 days
- Use for testing email delivery, audio attachments, etc.
- The system will still log the delivery as a debug/test delivery
- Disable debug mode for normal operation

## Data Storage

All data is stored in SQLite database at `~/.openclaw/last-words/data.db`:
- `message`: Stores the final message content and audio path
- `config`: Stores delivery method and contact information
- `activity_log`: Tracks daily check results and deliveries

## Security & Privacy

- Messages are stored locally only
- No cloud storage or external API calls for message content
- Email delivery uses user's configured SMTP settings
- All scripts run within OpenClaw sandbox

## Setup Daily Check

Add to OpenClaw cron:
```bash
openclaw cron add --name "last-words-check" --schedule "0 9 * * *" --command "python3 ~/.openclaw/workspace/last-words/scripts/check_activity.py"
```
