---
name: daily-brief
description: Send a daily operational brief from your self-hosted OpenClaw to Telegram — agent health, unresolved issues, and weekly evolution highlights, every morning.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - bash
        - curl
        - jq
        - docker
      env:
        - OPENCLAW_TOKEN
        - TELEGRAM_BOT_TOKEN
        - TELEGRAM_CHAT_ID
    primaryEnv: OPENCLAW_TOKEN
    emoji: "🗞️"
---

# Daily Brief

`daily-brief` packages a production-style daily report workflow for self-hosted OpenClaw users.

It generates a structured morning digest and sends it to Telegram, with focus on:

- Agent/system health signals from gateway logs
- Unfinished or risky items inferred from recent runtime behavior
- Capability evolution highlights from latest `evolver` logs

## Typical deployment scenario

Use this skill when your OpenClaw instance is self-hosted and you want a reliable daily operations snapshot at a fixed time (for example 08:05 every day).

## Required components

- `secretary` agent configured and available
- system cron enabled
- Telegram bot delivery configured
- OpenClaw gateway reachable at local endpoint

## Real script pattern (redacted example)

The following is a redacted usage example adapted from `daily_brief.sh`:

```bash
#!/bin/bash
BOT_TOKEN="${TELEGRAM_BOT_TOKEN}"
CHAT_ID="${TELEGRAM_CHAT_ID}"
OPENCLAW_TOKEN="${OPENCLAW_TOKEN}"

LOGS=$(docker logs openclaw-gateway --since 24h 2>&1 | tail -100)

EVOLVER_LOG=""
LATEST_EVOLVER=$(ls -t /tmp/evolver-*.log 2>/dev/null | head -1)
if [ -n "$LATEST_EVOLVER" ]; then
  EVOLVER_LOG=$(tail -50 "$LATEST_EVOLVER")
fi

PROMPT="You are the private secretary. Build a concise daily brief with:
1) system status
2) what happened today
3) issues found
4) resolved vs unresolved
5) items requiring executive attention

System logs:
${LOGS}

Evolution report:
${EVOLVER_LOG}"

RESPONSE=$(curl -s -X POST http://127.0.0.1:18789/v1/chat/completions \
  -H "Authorization: Bearer ${OPENCLAW_TOKEN}" \
  -H "Content-Type: application/json" \
  -H "x-openclaw-agent-id: secretary" \
  --max-time 180 \
  -d "{\"model\":\"openclaw\",\"messages\":[{\"role\":\"user\",\"content\":$(echo "$PROMPT" | jq -Rs .)}]}")

RESULT=$(echo "$RESPONSE" | jq -r '.choices[0].message.content // "Secretary unavailable"')

curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
  -d chat_id="${CHAT_ID}" \
  --data-urlencode text="${RESULT}"
```

## Cron example

```cron
5 8 * * * /Users/lihaochen/openclaw/daily_brief.sh
```
