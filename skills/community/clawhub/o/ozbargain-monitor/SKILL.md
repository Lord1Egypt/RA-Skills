---
name: ozbargain-monitor
description: Manage OzBargain daily-deal automation in OpenClaw via cron. Use when creating/updating schedules, customizing topic priorities, enabling no-noise filtering, manual-triggering catch-up runs, routing delivery to chat groups, or troubleshooting failed delivery.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["openclaw"] }
      }
  }
---

# OzBargain Monitor

Manage OzBargain cron workflows end-to-end: creation, updates, manual runs, dedupe, and delivery troubleshooting.

## User-configurable profile (set these first)

- `jobId`: cron job id created for the user
- `schedule`: user-defined time + timezone
- `delivery`: user-defined channel + destination (group/chat id)
- `topics`: user-defined priority order
- `language`: user-defined output language

Never hardcode a specific person, group id, job id, or topic order.

## Default quality rules

Keep these rules in the cron `--message` prompt unless the user overrides them:

1. Keep only high-value deals
2. Keep output concise and structured
3. Include per item: title, price/benefit, why worth it, direct link
4. Read deal comments and include important comment-derived signals:
   - expiry / sold-out / dead-deal reports
   - better stacking paths (cashback + card offer + code)
   - hidden constraints (new-customer only, in-store only, min-spend, exclusions)
5. Add a short “comment insights” note when comments provide material extra value
6. If comments indicate likely expiry, label the deal as “可能过期（以楼主/最新评论为准）”
7. If nothing strong appears, explicitly output a “no high-value deals today” line
8. Avoid ad noise/low-value posts

## Dedupe state (required)

Use a user-specific state file, e.g.:

- `/home/<user>/.openclaw/workspace/data/ozbargain-sent-links.json`

Initial content if missing:

```json
{ "sent": [] }
```

Dedup key: canonical OzBargain link (`node`/`goto` preferred).

Required behavior per run:

1. Read state file first
2. Filter out links already in `sent`
3. Send only unseen links
4. Append newly sent links back to `sent` and save deduped state

## Operations

### Create a new job

```bash
openclaw cron add --name "<job-name>" --cron "<expr>" --tz "<timezone>" --session isolated --announce --channel <channel> --to "<destination>" --message "<prompt>"
```

### Manual catch-up run

```bash
openclaw cron run <job-id>
openclaw cron runs --id <job-id> --limit 1
```

Then report whether delivery succeeded (`delivered: true` / `deliveryStatus: delivered`).

### Update topic order / wording

```bash
openclaw cron edit <job-id> --message "..."
```

Only change schedule/channel when user asks.

### Change delivery destination

```bash
openclaw cron edit <job-id> --announce --channel <channel> --to "<destination>"
```

### Verify status

```bash
openclaw cron list --json
openclaw cron runs --id <job-id> --limit 5
```

## Troubleshooting

If cron run succeeded but delivery failed:

1. Check run history error text
2. Check logs for channel API errors
3. Send a probe directly to destination using `message.send`

Common causes:

- wrong/old destination id
- bot removed from group
- permissions/visibility restrictions
- temporary provider/API failures

Useful log grep:

```bash
grep -n "message failed\|sendMessage\|announce delivery failed\|forbidden\|chat not found" /tmp/openclaw/openclaw-$(date +%F).log
```
