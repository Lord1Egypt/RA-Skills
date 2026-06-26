---
name: ping-me
description: "One-shot reminders via natural language. Auto-detects channel and timezone. Say 'remind me...' in any language and get pinged when it's time. Works with every channel."
metadata: {"openclaw":{"emoji":"⏰","requires":{"bins":["openclaw","python3"]}}}
---

# ping-me ⏰

Set one-shot reminders through natural language. The reminder fires once, delivers to the user's current chat channel, then auto-deletes.

**Response flow**: Call the script first, then confirm with one short sentence. Keep it concise — no preamble, no time calculations, just the confirmation.

## How It Works

User says something like:
- "Remind me in 30 minutes to take a break"
- "提醒我明天下午3点交作业"
- "3分後にお風呂に入ることを思い出させて"
- "rappelle-moi dans 2 heures de rappeler Marie"

You parse the **time** and **message**, then call the script SILENTLY.

## Channel & Delivery Target

The script auto-detects which channel the user is chatting from.

- You do NOT need to pass `--channel` unless the user explicitly asks for a different channel
- **Only pass `--channel` when the user explicitly says** "remind me on telegram" / "发到飞书" / etc.

### Delivery target (`--to`)

Some channels (e.g. QQ Bot) require a full delivery target for announce mode. The script resolves `--to` automatically from:

1. `$OPENCLAW_TO` environment variable (if gateway sets it)
2. `$OPENCLAW_SESSION_KEY` (extracts target from session key format)
3. `config.json` → `"to"` field (user-configured)

**If reminders fail with "requires target" error**, the user needs to configure their target once:
```bash
bash {baseDir}/scripts/ping-me-config.sh --set to=qqbot:c2c:<openid>
```

You can also pass `--to` explicitly when calling the script.

## Commands

### Set a reminder

```bash
bash {baseDir}/scripts/ping-me.sh [options] <time> <message>
```

**Time formats:**

| User says | You pass as `<time>` |
|-----------|---------------------|
| "3分钟后" / "in 3 minutes" | `3m` |
| "30分钟后" / "in 30 minutes" | `30m` |
| "2小时后" / "in 2 hours" | `2h` |
| "明天" / "tomorrow" | `1d` |
| "明天下午3点" / "tomorrow at 3pm" | ISO 8601: `2026-03-11T15:00` (no tz offset needed, script uses configured tz) |
| "周五晚上8点" / "Friday 8pm" | ISO 8601 with calculated date |

**IMPORTANT**: For relative times (N分钟后, N小时后, in N minutes/hours), ALWAYS use the short form (`3m`, `2h`, `1d`). Do NOT convert to ISO timestamp.

**Options:**
- `--channel <ch>` — override delivery channel (only when user explicitly requests)
- `--to <dest>` — override delivery target (e.g. `qqbot:c2c:<openid>`)
- `--tz <tz>` — override timezone for this reminder
- `--emoji <e>` — custom emoji prefix

**Examples:**
```bash
bash {baseDir}/scripts/ping-me.sh 30m "Take a break"
bash {baseDir}/scripts/ping-me.sh 2h "Team meeting"
bash {baseDir}/scripts/ping-me.sh "2026-03-11T15:00" "Submit homework"
bash {baseDir}/scripts/ping-me.sh --channel telegram 1d "Renew subscription"
```

### List active reminders

```bash
bash {baseDir}/scripts/ping-me-list.sh
```

### Cancel a reminder

```bash
bash {baseDir}/scripts/ping-me-cancel.sh <job-id>
```

### View / change settings

```bash
bash {baseDir}/scripts/ping-me-config.sh                        # Show settings
bash {baseDir}/scripts/ping-me-config.sh --set tz=Asia/Tokyo     # Change timezone
bash {baseDir}/scripts/ping-me-config.sh --set channel=qqbot     # Change default channel
bash {baseDir}/scripts/ping-me-config.sh --set to=qqbot:c2c:<openid>  # Set delivery target
bash {baseDir}/scripts/ping-me-config.sh --set emoji=🔔          # Change emoji
bash {baseDir}/scripts/ping-me-config.sh --set lang=zh           # Change language
bash {baseDir}/scripts/ping-me-config.sh --reset                 # Reset to defaults
```

## Your Job (Agent Instructions)

### Creating Reminders

1. Detect reminder intent in any language
2. Extract **time** and **message**
3. For relative times → use short form (`3m`, `2h`, `1d`). For absolute times → ISO 8601 without tz offset
4. Do NOT pass `--channel` or `--to` unless user explicitly requests a specific channel, or the script fails without it
5. Call `ping-me.sh` with the parsed arguments
6. After the script succeeds, confirm with one short sentence in the user's language

### Response Style

Keep responses concise. Call the script first, then confirm briefly:
- "⏰ Got it, pinging you in 30 minutes to take a break."
- "⏰ 好的，3分钟后提醒你洗澡。"
- "⏰ 已设置，明天下午3点提醒你交作业。"
- "⏰ 3分後にリマインドします。"

No need to explain time conversion or timezone logic to the user — just confirm the reminder.

### Listing & Cancelling

- "what reminders do I have" / "我有哪些提醒" → run `ping-me-list.sh`
- "cancel reminder X" / "取消提醒" → run `ping-me-cancel.sh <id>` (get ID from list first)

### Changing Settings (Interactive)

When user wants to change settings, use `ping-me-config.sh`:

- "change timezone to Tokyo" / "改时区到东京" → `--set tz=Asia/Tokyo`
- "默认发到飞书" / "send reminders to feishu by default" → `--set channel=feishu`
- "设置QQ投递目标" → `--set to=qqbot:c2c:<openid>`
- "show my settings" / "看看设置" → run without args
- "reset settings" / "重置设置" → `--reset`

After changing settings, confirm with ONE sentence.

### First-Time Setup Hint

If the first reminder fails with a "requires target" or "multiple channels" error, guide the user to configure:
1. Default channel: `ping-me-config.sh --set channel=qqbot`
2. Delivery target: `ping-me-config.sh --set to=qqbot:c2c:<openid>`

The user's openid can be found in their QQ Bot session key or gateway logs.

## Notes

- Reminders auto-delete after firing (`--delete-after-run`)
- Channel auto-detection: `$OPENCLAW_CHANNEL` → config → empty
- Delivery target auto-detection: `$OPENCLAW_TO` → session key extraction → config → empty
- Timezone auto-detection: config.tz → system tz → UTC
- No API keys or external services needed
- Settings stored in `{baseDir}/config.json`
