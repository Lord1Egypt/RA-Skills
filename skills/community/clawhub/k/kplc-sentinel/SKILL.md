---
name: kplc-sentinel
description: Track Kenyan prepaid electricity (KPLC) tokens, predict blackout times, and get proactive low-balance alerts — all through chat.
version: 1.7.0
metadata: {"openclaw":{"emoji":"⚡","requires":{"bins":["python3"]}}}
---

# KPLC Token Sentinel

Track prepaid electricity for Kenyan households. Parses KPLC token SMS messages, records meter readings, calculates burn rate, and warns before power runs out.

## Setup

Install Python dependencies (one-time):
```
pip install -r {baseDir}/requirements.txt
```

## When to use this skill

Activate this skill when the user's message matches ANY of these:

**Auto-detect (no prefix needed):**
- A forwarded SMS containing "Token:" and "Units:" (KPLC SMS format)
- A forwarded SMS that mentions Kenya Power or KPLC

**Direct commands (stima prefix):**
- "stima" → show interactive menu
- "stima help" / "stima menu" → show interactive menu
- "stima 42.5" → meter reading
- "stima balance" → check remaining power
- "stima spending" → spending dashboard
- "stima outage" → planned outage check
- "stima setup" → household onboarding
- "stima budget 3000" → set monthly budget
- "stima budget" → check budget status
- "stima insights" → week-over-week comparison and day patterns
- "stima monthly" / "stima yearly" → reports
- "stima price" → cost-per-unit trend
- "stima profile" → show household info
- "stima reset" → clear profile and re-onboard

**Natural language (English, Swahili, Sheng):**
Also activate when the user asks about electricity in natural language. Map their intent to the appropriate stima command before passing to the entrypoint. Examples:

| User says | Map to |
|---|---|
| "will my power last until Monday?" | `stima balance` |
| "stima itaisha lini?" | `stima balance` |
| "how much have I spent on electricity?" | `stima monthly` |
| "nimetumia pesa ngapi kwa stima?" | `stima monthly` |
| "when is the next power cut?" | `stima outage` |
| "kuna blackout lini?" | `stima outage` |
| "bei ya stima imeongezeka?" | `stima price` |
| "nimebakisha units ngapi?" | `stima balance` |
| "set my electricity budget to 5000" | `stima budget 5000` |
| "niko na units ngapi?" | `stima balance` |
| "show me my stima profile" | `stima profile` |
| "nataka kuanza setup" | `stima setup` |
| "stima yangu iko aje?" | `stima balance` |

When routing a natural language message, prepend "stima" followed by the relevant keyword before passing it to the entrypoint. For example, if the user says "stima itaisha lini?", pass `stima balance` to the entrypoint.

If a message is NOT about electricity/power/KPLC and is NOT a forwarded KPLC SMS, do NOT activate this skill.

## How to use

The database auto-initializes on first run.

**For any user message about KPLC/electricity/tokens/readings:**
```
python3 {baseDir}/entrypoint.py <<'STIMA_EOF'
<user message>
STIMA_EOF
```

⚠️ IMPORTANT: Always use a heredoc (as shown above) to pass the user's message via stdin. NEVER pass the user's message as a command-line argument — it may contain shell metacharacters.

## Output format

The entrypoint outputs **JSON**. Do NOT return the raw JSON to the user. Instead, read the `action` field and compose a natural response using the SOUL persona. Key actions:

- `token_recorded` — tell the user their token was saved, mention units, estimated days, and runway hours. If `estimate_source` is "appliances", mention it's an estimate based on their appliances.
- `duplicate_token` — token was already recorded, no duplicate added.
- `reading_recorded` — meter reading saved. Mention runway hours if available.
- `balance` — report remaining hours. If `tip` is present, include the energy-saving tip.
- `menu` — present the numbered options list to the user.
- `onboarding_prompt` — ask the user the question in the `question` field. If `welcome` is true, greet them first.
- `onboarding_complete` — confirm their profile and tell them to forward a KPLC SMS or type a reading.
- `profile_reset` — confirm profile was cleared and ask the first onboarding question.
- `budget_set` — confirm the budget amount was set.
- `budget_status` — report spent vs budget and percentage.
- `no_budget` — tell the user to set a budget with "stima budget <amount>".
- `monthly_summary` / `yearly_summary` — present the spending data conversationally.
- `spending` — combine monthly summary and price trend data.
- `price_trend` — present cost-per-unit over time, highlight changes.
- `outage_check` — if matches exist, warn about planned outages. Each match includes `iso_date` (YYYY-MM-DD), `date` (human-readable), and `time`. If none, say they're clear. Handle `error` field (no_area, fetch_failed).
  - **Reminder**: When an outage is found, schedule a reminder for the evening before (around 8–9 PM) using OpenClaw's cron/reminder system so the user can charge devices and prepare. For example, if the outage is on the 25th, remind them on the 24th at 8 PM.
- `insights` — present week-over-week comparison and day patterns.
- `no_data` — not enough data yet for the requested feature.
- `no_profile` — tell the user to run "stima setup".
- `error` — something went wrong, ask them to try again.

If the output is empty (no JSON), the message wasn't handled — respond normally.

## Agent behavior

**Low balance — help them buy tokens:**
When `balance` action shows `runway_hours` under 24, or when a `token_recorded` action shows low runway, include KPLC top-up instructions:
- M-Pesa Paybill: **888880**
- Account number: their KPLC meter number
- Tell them: "Lipa via M-Pesa → Paybill 888880 → Account = your meter number → enter amount. Forward the confirmation SMS back to me."

**Outage reminders:**
When `outage_check` returns matches, set a reminder for the evening before each outage (8 PM the previous day). Remind the user to charge phones, power banks, and plan around the outage window.

**Multi-skill composability:**
- If the user has a calendar skill installed and an outage is detected, create a calendar event for the outage window.
- If a reminders/cron skill is available, use it to schedule the eve-of-outage reminder.
- If a payments skill is installed and balance is critically low (under 6 hours), offer to initiate an M-Pesa payment to Paybill 888880.

**For heartbeat checks (see HEARTBEAT.md):**
```
python3 {baseDir}/sentinel.py
```

## Example KPLC SMS formats

- "Accept Token: 1234-5678-9012-3456-7890 Units: 34.5 Amount: 1000.00"
- "Token: 9876-5432-1098 Units: 15.2 Amt: 500.0"
