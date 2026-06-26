# ping-me ⏰

One-shot reminders via natural language for [OpenClaw](https://github.com/openclaw/openclaw).

Say "remind me..." in any language and get pinged when it's time. Works with every channel: QQ, Telegram, Discord, WhatsApp, Slack, iMessage, WeChat, Feishu, DingTalk, and more.

## Install

```bash
npx skills add Ethan-Shen-Individual-Lab/openshen-skills@ping-me -g -y
```

Or via ClawHub:

```bash
clawhub install ping-me
```

## Features

- **Any language** — English, 中文, 日本語, Français, Español, Deutsch, 한국어, and more
- **Auto-detect channel** — replies to the same channel the user messaged from (QQ → QQ, Telegram → Telegram, etc.)
- **Auto-detect timezone** — reads system timezone by default, configurable per-user
- **Relative & absolute times** — "in 30 minutes", "明天下午3点", "next Friday at 8pm"
- **Interactive config** — change timezone, default channel, language via chat
- **Zero external dependencies** — uses `openclaw cron` internally, no API keys needed
- **Auto-cleanup** — reminders self-delete after firing

## Usage

Just talk to your agent naturally:

```
User: remind me in 30 minutes to take a break
Agent: ⏰ Got it, pinging you in 30 minutes to take a break.

User: 提醒我明天下午3点交作业
Agent: ⏰ 已设置，明天下午3点提醒你交作业。

User: 3分後にお風呂に入ることを思い出させて
Agent: ⏰ 3分後にリマインドします。

User: rappelle-moi dans 2 heures de rappeler Marie
Agent: ⏰ C'est noté, rappel dans 2 heures.
```

### List & Cancel

```
User: what reminders do I have?
Agent: 📋 Active reminders:
       1. [abc123] in 25m — take a break
       2. [def456] tomorrow 15:00 — 交作业

User: cancel the first one
Agent: ✅ Reminder abc123 cancelled.
```

### Change Settings

```
User: change my timezone to America/New_York
Agent: ✅ Timezone set to America/New_York.

User: 把提醒默认发到飞书
Agent: ✅ 默认渠道已设为 feishu。

User: show my ping-me settings
Agent: ⚙️ Current settings:
       Timezone: America/New_York
       Default channel: feishu (override: auto-detect)
       Language: auto
```

## Requirements

- [OpenClaw](https://github.com/openclaw/openclaw) installed and running
- `python3` (for JSON parsing in shell scripts)

No API keys. No external services. No databases.

## How It Works

```
User message → Agent parses time + message
            → ping-me.sh creates openclaw cron job
            → Cron fires at scheduled time
            → OpenClaw delivers to the originating channel
            → Job auto-deletes
```

The skill detects which channel the user is chatting from via OpenClaw's `$OPENCLAW_CHANNEL` environment variable (set automatically by the gateway). If the variable isn't available, it falls back to the configured default channel.

## File Structure

```
ping-me/
├── README.md          # This file (for GitHub / ClawHub)
├── SKILL.md           # Skill definition (loaded by OpenClaw)
├── _meta.json         # Metadata (for ClawHub registry)
└── scripts/
    ├── ping-me.sh         # Create a reminder
    ├── ping-me-list.sh    # List active reminders
    ├── ping-me-cancel.sh  # Cancel a reminder
    └── ping-me-config.sh  # View/change settings
```

## Configuration

Settings are stored in `{baseDir}/config.json` and can be changed via chat or CLI:

| Setting | Default | Description |
|---------|---------|-------------|
| `tz` | system timezone | IANA timezone (e.g. `Asia/Shanghai`, `America/New_York`) |
| `channel` | `auto` | Default delivery channel. `auto` = detect from conversation |
| `lang` | `auto` | Confirmation message language. `auto` = match user's language |
| `emoji` | `⏰` | Emoji prefix for reminder messages |

### CLI Config

```bash
bash {baseDir}/scripts/ping-me-config.sh                    # Show current settings
bash {baseDir}/scripts/ping-me-config.sh --set tz=Asia/Tokyo
bash {baseDir}/scripts/ping-me-config.sh --set channel=qqbot
bash {baseDir}/scripts/ping-me-config.sh --set emoji=🔔
bash {baseDir}/scripts/ping-me-config.sh --reset
```

## Multi-Channel Behavior

| Scenario | Channel Used |
|----------|-------------|
| User messages from QQ | Reminder sent to QQ |
| User messages from Telegram | Reminder sent to Telegram |
| User messages from Feishu | Reminder sent to Feishu |
| `$OPENCLAW_CHANNEL` not available | Falls back to `config.channel` setting |
| User explicitly says "remind me on telegram" | Uses specified channel |

## Timezone Handling

1. If user specifies timezone in the message ("remind me at 3pm EST") → uses that
2. If `config.tz` is set → uses configured timezone
3. Falls back to system timezone (`timedatectl` / `$TZ`)
4. Last resort: UTC

## Contributing

PRs welcome. Please follow the OpenClaw skill conventions:

- Keep SKILL.md concise (token cost matters)
- Test with multiple channels before submitting
- Support at least English and Chinese in agent instructions

## License

MIT
