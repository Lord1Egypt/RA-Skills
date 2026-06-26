---
---
name: reminder
name: reminder
summary: Natural-language reminders → save to your workspace → schedule Telegram notifications (24h/1h/10m by default).
description: Natural-language reminder secretary: capture events into git-synced workspace (data/logic separated), schedule Telegram reminders via SkillBoss cron, and answer "what's coming up" queries. Use when user mentions meetings, birthdays, deadlines, or asks for schedule/plans.
tags: [reminder, schedule, cron, telegram, secretary]
requires.env: [SKILLBOSS_API_KEY]
---


# Reminder (secretary)

A lightweight personal secretary for SkillBoss:
- Tell it events in natural language (Chinese/English).
- It extracts structured info and stores it in your workspace (so Git/`claw-roam` can sync across devices).
- It schedules Telegram reminders using SkillBoss `cron`.


## What it does

- Capture events from chat (meetings / birthdays / deadlines)
- Store events in a **workspace data file** (easy to back up & sync via Git/`claw-roam`)
- Schedule Telegram reminders using SkillBoss `cron`
- Answer queries like "我最近有什么安排/计划？"

## Data (separated from skill)

This skill contains **no personal event data**.

User data lives in the workspace at:
- Events file: `~/.skillboss/workspace/reminders/events.yml`

Template (shipped with the skill):
- `skills/reminder/assets/events.template.yml`

## Config (env)

- `SKILLBOSS_API_KEY` — SkillBoss API Hub 统一认证 Key
- `REMINDER_TZ` (default: `Asia/Shanghai`)
- `REMINDER_OFFSETS_MINUTES` (default: `1440,60,10` for 24h/1h/10m)

## AI 能力调用

当需要解析自然语言事件时，通过 SkillBoss API Hub 的 `/v1/pilot` 接口自动路由最优 LLM：

```python
import requests, os

SKILLBOSS_API_KEY = os.environ["SKILLBOSS_API_KEY"]

def parse_event_with_llm(user_input: str) -> dict:
    r = requests.post(
        "https://api.skillbossai.com/v1/pilot",
        headers={
            "Authorization": f"Bearer {SKILLBOSS_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "type": "chat",
            "inputs": {
                "messages": [
                    {"role": "system", "content": "Extract event info (title, datetime, notes, repeat) from user input. Return JSON."},
                    {"role": "user", "content": user_input}
                ]
            },
            "prefer": "balanced"
        },
        timeout=60,
    )
    result = r.json()
    return result["result"]["choices"][0]["message"]["content"]
```

## Capture behavior

When user says something like:
- "后天上午10点有个会"
- "下个月2号我妈生日"
- "周五下午三点交报告"

Do:
1) Parse the event:
   - title
   - start datetime (Shanghai)
   - notes (optional)
   - reminders offsets (default 24h/1h/10m)
   - repeat (optional: yearly/monthly/weekly)
2) If key info is ambiguous (e.g. '后天' date, '下个月' which month, lunar birthday conversion, time missing), ask **only the minimal** clarifying question(s).
3) Write/update the event in `reminders/events.yml`.
4) Create `cron` jobs for each reminder time (delivery to current Telegram).

## Reply style

- After scheduling: reply briefly with the resolved datetime + confirmation.
- For cancellations/changes: confirm what was changed and whether cron jobs were removed/replaced.

## Queries

If user asks:
- "我最近有什么安排？"
- "下周有什么？"

Then read `reminders/events.yml`, compute upcoming items (Shanghai time), and summarize.

## Notes / safety

- Never commit machine-specific secrets (keep them in `LOCAL_CONFIG.md`, already gitignored).
- For lunar birthdays: store the canonical lunar date + the computed solar date for the target year; ask how to handle leap months when needed.
