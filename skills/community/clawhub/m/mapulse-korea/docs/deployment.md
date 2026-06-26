# Deployment Guide — Mapulse

## Prerequisites

- Python 3.10+ (3.12 recommended)
- Telegram Bot token (from @BotFather)

## 1. Install Dependencies

```bash
pip install python-telegram-bot pykrx requests beautifulsoup4
```

## 2. Environment Variables

```bash
# Required
export TELEGRAM_BOT_TOKEN=your_token_here

# Optional — AI analysis
export OPENROUTER_API_KEY=sk-or-xxx          # OpenRouter (recommended)
export ANTHROPIC_API_KEY=sk-ant-xxx          # or Anthropic direct

# Optional — Data
export DART_API_KEY=xxx                      # DART corporate disclosures
export MAPULSE_DB=/path/to/mapulse.db        # SQLite path (default: data/mapulse.db)

# Optional — Access control
export ALLOWED_GROUPS=-100xxx,-100yyy         # Restrict to specific groups
```

## 3. Start

```bash
cd bot && python3 mapulse_bot.py
```

## 4. Run as Service (systemd)

```ini
[Unit]
Description=Mapulse Telegram Bot
After=network.target

[Service]
Type=simple
WorkingDirectory=/path/to/mapulse/bot
ExecStart=/usr/bin/python3 -u mapulse_bot.py
Restart=always
RestartSec=10
EnvironmentFile=/path/to/mapulse/.env

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable mapulse-bot
sudo systemctl start mapulse-bot
```

## 5. Cron Jobs (optional)

```bash
# Morning briefing (Mon-Fri, 8:00 KST)
0 8 * * 1-5 cd /path/to/mapulse/scripts && python3 cron_briefing.py

# News aggregation (3x daily)
30 6 * * 1-5  cd /path/to/mapulse/scripts && python3 cron_news_aggregate.py
30 12 * * 1-5 cd /path/to/mapulse/scripts && python3 cron_news_aggregate.py
0 19 * * 1-5  cd /path/to/mapulse/scripts && python3 cron_news_aggregate.py
```

## 6. Database

Auto-initializes on first run. Manual init:

```bash
python3 scripts/db.py
```

## 7. Monitoring

```bash
sudo systemctl status mapulse-bot
sudo journalctl -u mapulse-bot -f
```
