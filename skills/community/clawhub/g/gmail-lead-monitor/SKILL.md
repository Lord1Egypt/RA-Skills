# Gmail Lead Monitor

Monitor any Gmail inbox and get instant Telegram alerts for important emails. Configure keywords to filter for leads, orders, or support inquiries. Zero dependencies beyond Python stdlib — no pip required.

## What It Does

- Connects to Gmail via IMAP (no OAuth, just app password)
- Checks for new emails every N minutes (configurable)
- Sends Telegram alert with sender, subject, and snippet
- Detects important emails by keyword matching
- Marks important emails with Gmail STAR flag
- Tracks seen emails to avoid duplicate alerts

## Setup

### 1. Enable Gmail App Password

1. Go to [myaccount.google.com/security](https://myaccount.google.com/security)
2. Enable 2-Step Verification
3. Go to App passwords → Generate new app password
4. Select "Mail" and your device → Copy the 16-char password

### 2. Create Config File

```bash
mkdir -p ~/.config/gmail_monitor
cat > ~/.config/gmail_monitor/config.json << 'EOF'
{
  "email": "you@gmail.com",
  "app_password": "xxxx xxxx xxxx xxxx",
  "telegram_token": "your_bot_token",
  "telegram_chat_id": "your_chat_id",
  "keywords": ["order", "purchase", "setup", "interested", "question", "invoice"],
  "check_interval_minutes": 5,
  "max_emails_per_check": 20
}
EOF
```

### 3. Get Telegram Bot Token

1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. `/newbot` → follow prompts
3. Copy the bot token
4. Get your chat ID from [@userinfobot](https://t.me/userinfobot)

## Usage

```bash
# Run once (check now)
python3 gmail_monitor.py --once

# Run in daemon mode (default interval from config)
python3 gmail_monitor.py

# Custom interval
python3 gmail_monitor.py --interval 10

# Run via cron every 5 minutes
*/5 * * * * python3 /path/to/gmail_monitor.py --once >> /tmp/gmail_monitor.log 2>&1
```

## Alert Example (Telegram)

```
📧 New Lead — Gmail
From: john@company.com
Subject: Question about your service
Time: 2025-03-15 14:22 PST

"Hi, I'm interested in your product and had a question about..."

⭐ Marked as important (keyword: question)
```

## Keyword Matching

Keywords match against: subject line + sender name + first 200 chars of body.
Case-insensitive. Add your own in config:

```json
"keywords": ["order", "purchase", "invoice", "urgent", "setup", "question", "interested", "trial"]
```

## Requirements

- Python 3.6+
- Gmail account with App Password enabled
- Telegram bot (free)
- Zero pip dependencies
