---
name: Iran Intelligence Radar
description: Monitor Persian-language X (Twitter) activity related to Iran, detect high-signal geopolitical events, translate posts, score escalation risk, and generate actionable intelligence reports with optional Telegram alerts and daily briefings.
version: "1.0"
author: OpenClaw Skills
skill_id: "3092da48-a837-4288-94d6-458c6ef0b3e0"
price_per_call: "$0.02"
capabilities:
  - Persian X/Twitter monitoring
  - Keyword signal detection
  - Engagement filtering and ranking
  - Translation to English, Arabic, Chinese
  - Escalation scoring (0-100)
  - Trending narrative detection
  - Telegram alert integration
  - Daily intelligence briefing generation
inputs:
  - user_id
  - query
  - since_hours (optional)
  - custom keywords (optional)
  - custom monitored accounts (optional)
outputs:
  - ranked tweets
  - multilingual translations
  - alert classification
  - escalation score and level
  - trending signals
  - markdown intelligence report
  - optional daily briefing
tools:
  - x_keyword_search
  - x_semantic_search
  - web_search
  - translate_text
  - send_alert
  - skillpay_billing
  - telegram_api
---

# Iran Intelligence Radar

## Overview
Iran Intelligence Radar is an OSINT-focused skill for detecting meaningful geopolitical signals from Persian-language discourse on X (Twitter). It scans configured keywords and accounts, filters and ranks high-engagement posts, translates content for multilingual analysis, computes escalation risk, and outputs a structured Markdown intelligence report.

This skill is designed for journalists, OSINT teams, geopolitical analysts, and monitoring operations that need a rapid understanding of Iranian online narratives.

## Capabilities

- Monitor Persian-language tweets linked to Iran-related security, policy, and protest narratives.
- Detect high-signal content using keyword matching, engagement thresholds, and relevance ranking.
- Translate Persian posts into:
  - English (`en`)
  - Arabic (`ar`)
  - Chinese (`zh`)
- Classify tweet-level alert intensity (`LOW`, `MEDIUM`, `HIGH`).
- Detect trend spikes using keyword volume ratio (`current_count / historical_average`).
- Compute an Iran escalation score (`0-100`) with severity levels:
  - `LOW` (0-30)
  - `MEDIUM` (31-60)
  - `HIGH` (61-80)
  - `CRITICAL` (81-100)
- Trigger automatic Telegram alerts when escalation conditions are met.
- Generate daily 24-hour intelligence briefings.

Default high-priority keywords include:

- حمله
- موشک
- تحریم
- غنی سازی
- اعتراض
- زن زندگی آزادی
- هسته ای

## Invocation

Use any of the following command patterns:

- `run persian radar`
- `scan iran tweets`
- `monitor iran signals`

Programmatic entrypoint:

```python
from skills.persian_x_radar.agent import run_radar

result = run_radar(
    user_id="demo_user",
    query="run persian radar",
    since_hours=6,
)
```

Typical execution flow:

1. Billing and cooldown check
2. X search and fallback retrieval
3. Filtering and deduplication
4. Translation and per-item alert classification
5. Trending signal detection
6. Escalation scoring
7. Alert dispatch (Telegram/channel hooks)
8. Markdown report generation
9. Optional daily briefing assembly

## Example Output

### Intelligence Table (sample)

| # | Author | Time | Persian | English | Arabic | Chinese | Engagement | Link | Alert |
|---|---|---|---|---|---|---|---|---|---|
| 1 | @user123 | 2h ago | بحث درباره موشک... | Discussion about missiles... | نقاش حول الصواريخ... | 关于导弹的讨论... | 530 likes / 120 RT | https://x.com/... | HIGH |
| 2 | @iran_watch | 3h ago | گزارش هایی از اعتراض... | Reports of protests... | تقارير عن احتجاجات... | 有关抗议的报告... | 180 likes / 42 RT | https://x.com/... | MEDIUM |

### Radar Summary (sample)

- Escalation score: `72 (HIGH)`
- Top signal: `missile discussion spike`
- Trending signals:
  1. `موشک` spike detected
  2. `اعتراض` volume increase

## Pricing

- Skill ID: `3092da48-a837-4288-94d6-458c6ef0b3e0`
- Price per call: `$0.02`
- Billing provider: SkillPay

Billing behavior:

- Each scan call is billable.
- Cooldown protection avoids duplicate charges within configured window.
- If balance is insufficient, the skill returns a payment link response:

```json
{
  "status": "payment_required",
  "message": "Insufficient balance to run Persian X Radar.",
  "price": 0.02,
  "payment_link": "https://skillpay.me/pay/..."
}
```

## Use Cases

- Real-time monitoring of missile, nuclear, sanctions, or protest narratives.
- Editorial intelligence support for breaking Iran-related developments.
- Geopolitical risk escalation tracking for operations/security teams.
- Multilingual situational awareness for non-Persian analysts.
- Daily strategic briefing generation from rolling social signal history.

## Configuration

Primary configuration file:

- `skills/persian_x_radar/config.yaml`

Key sections:

- `monitoring`
  - `default_since_hours`
  - `heartbeat_minutes`
  - `keywords`
  - `accounts`
- `thresholds`
  - `min_faves`
  - `min_retweets`
- `translation`
  - `languages` (`en`, `ar`, `zh`)
- `trending`
  - `spike_threshold`
  - `min_volume`
  - `keywords`
- `alerts`
  - channel and engagement thresholds
- `telegram`
  - `enabled`
  - `bot_token`
  - `chat_id`
- `billing`
  - `skill_id`
  - `price_per_call`
  - `charge_cooldown_minutes`

Common customization commands:

- Add keyword: `add keyword "سپاه"`
- Monitor account: `monitor account @BBCPersian`
- Change thresholds: `change alert threshold retweets > 200`

This skill is suitable for deployment in AI skill marketplaces and agent orchestration platforms requiring deterministic billing, structured outputs, and operational alerting.
