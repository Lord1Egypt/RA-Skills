# Persian X Radar - OSINT Intelligence Radar

Persian X Radar monitors high-signal Persian content on X, translates it to English/Arabic/Chinese, detects trend spikes, computes an Iran escalation score, and sends operational alerts.

## Core Capabilities

- Persian X search with engagement thresholds and fallback tools
- Translation to `en` / `ar` / `zh`
- Trending signal detection using keyword spike ratio (`current / historical_average`)
- Iran escalation scoring (`0-100`) with LOW/MEDIUM/HIGH/CRITICAL levels
- Automatic Telegram alerting when escalation is high
- Daily 24-hour Iran intelligence briefing generation
- SkillPay billing with cooldown-based double-charge protection

## Pricing

Persian X Radar costs `$0.02` per scan.

Each scan triggers SkillPay billing.

If balance is insufficient, a payment link is returned.

## Project Structure

```text
persian-x-radar-skill/
├── README.md
├── logs/
│   ├── alerts.log
│   ├── billing.log
│   ├── escalation.log
│   └── trending.log
├── prompts/
│   └── system_prompt.md
└── skills/
    └── persian_x_radar/
        ├── __init__.py
        ├── agent.py
        ├── alerts.py
        ├── billing.py
        ├── cache.py
        ├── config.yaml
        ├── daily_briefing.py
        ├── escalation.py
        ├── search.py
        ├── telegram_alert.py
        ├── translator.py
        └── trending.py
```

## Requirements

- Python 3.10+
- PyYAML

Install:

```bash
pip install pyyaml
```

## Run

```bash
python -m skills.persian_x_radar.agent
```

Python usage:

```python
from skills.persian_x_radar.agent import PersianXRadarAgent, ToolRegistry

agent = PersianXRadarAgent(
    config_path="skills/persian_x_radar/config.yaml",
    tools=ToolRegistry(
        x_keyword_search=my_x_keyword_search,
        x_semantic_search=my_x_semantic_search,
        web_search=my_web_search,
        translate_text=my_translate_text,
        send_alert=my_send_alert,
    ),
)

result = agent.run_scan(command="run persian radar", user_id="user123")
print(result["report"])

# Daily briefing on demand
brief = agent.run_scan(command="daily briefing", user_id="user123").get("daily_briefing")
```

## Upgraded Workflow

1. Receive request
2. Billing check
3. Search tweets
4. Filter and normalize
5. Translate
6. Detect trending signals
7. Calculate escalation score
8. Trigger alerts (including Telegram)
9. Generate intelligence report and optional daily briefing

## Configuration

`skills/persian_x_radar/config.yaml` includes:

- `monitoring.*` search window, keywords, source accounts
- `trending.*` spike threshold and trend keywords
- `telegram.*` bot token and chat destination
- `billing.*` SkillPay skill id, per-call price, cooldown
- `alerts.*` row-level alert thresholds/channels

## Output

Scan report format:

- `Iran Intelligence Radar Report`
- `Scan window: last X hours`
- `Escalation score: N (LEVEL)`
- Tweet intelligence table
- Trending signals section

Daily briefing includes:

- Top trending keywords (24h)
- Highest engagement tweets
- Escalation score timeline
- English + Chinese summary
