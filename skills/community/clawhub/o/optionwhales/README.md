# OptionWhales Intelligence — OpenClaw Skill

An [OpenClaw](https://openclaw.ai/) agent skill that provides real-time option flow intelligence and AI-powered trade analysis from [OptionWhales](https://www.optionwhales.io).

## What It Does

This skill teaches AI agents two capabilities:

- **Option Flow** — real-time institutional option flow data: intent momentum, abnormal trades, direction bias, and momentum rankings across all major US equity tickers
- **AI Reports** — on-demand 22-node LLM pipeline producing BUY/SELL/HOLD recommendations with market analysis, fundamentals, news sentiment, bull/bear debate, and risk assessment

## Quick Start

### 1. Install the Skill

```bash
clawhub install option_whales
```

### 2. Get API Keys

- **Option Flow:** Sign up at [optionwhales.io](https://www.optionwhales.io) — free keys issued instantly (no credit card required)
- **AI Reports:** Contact the system administrator for a Bearer token

### 3. Configure

Add your keys to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "option_whales": {
        "enabled": true,
        "env": {
          "OPTIONWHALES_API_KEY": "ow_free_your_key_here",
          "AI_API_TOKEN": "your_bearer_token_here"
        }
      }
    }
  }
}
```

> `AI_API_TOKEN` is optional — the skill works with just `OPTIONWHALES_API_KEY` for flow data.

### 4. Use It

Ask your agent:
- *"What's the option flow on AAPL today?"*
- *"Show me the top momentum tickers"*
- *"Any unusual options activity?"*
- *"Is TSLA bullish or bearish right now?"*
- *"Generate an AI report for TSLA"*
- *"Show my report history"*
- *"Check my report quota"*

## API Tiers

### Option Flow

| Feature | Free | Pro |
|---------|------|-----|
| Tickers returned | Top 3 | All |
| Abnormal trades | Last 5 | All |
| Rate limit | 10/min, 200/day | 60/min, 5000/day |
| Historical sessions | ❌ | ✅ |
| WebSocket streaming | ❌ | ✅ |
| Momentum history | ❌ | ✅ |

### AI Reports

| Tier | Credits/Day | Can Generate? |
|------|-------------|---------------|
| FREE | 0 | No |
| TRIAL | 5 | Yes |
| PRO | 5 | Yes |
| ADMIN | Unlimited | Yes |

## CLI Helpers

Two standalone Python scripts are included for direct API access. No dependencies beyond Python 3.7+ standard library.

### Option Flow

```bash
export OPTIONWHALES_API_KEY="ow_free_your_key_here"

python3 scripts/optionflow.py flow                    # Current flow rankings
python3 scripts/optionflow.py flow --ticker AAPL       # Specific ticker detail
python3 scripts/optionflow.py momentum --top 5         # Top momentum tickers
python3 scripts/optionflow.py abnormal                 # Abnormal trades
python3 scripts/optionflow.py sessions                 # System health / sessions
python3 scripts/optionflow.py usage                    # Account usage
```

### AI Reports

```bash
export AI_API_TOKEN="your_bearer_token_here"

python3 scripts/aireport.py generate --ticker TSLA --user-id user@example.com --user-tier PRO
python3 scripts/aireport.py status --job-id abc-123
python3 scripts/aireport.py report --job-id abc-123 --format markdown
python3 scripts/aireport.py summary --user-id user@example.com --trading-day 2026-03-25
python3 scripts/aireport.py history --ticker TSLA --trading-day 2026-03-25
python3 scripts/aireport.py quota --user-id user@example.com --tier PRO
python3 scripts/aireport.py health
```

## Endpoints

### Option Flow

| Endpoint | Description |
|----------|-------------|
| `GET /v1/flow/current` | Current session intent rankings |
| `GET /v1/flow/current/{ticker}` | Ticker detail with clusters + time series |
| `GET /v1/flow/sessions` | System health and session status |
| `GET /v1/flow/{session}` | Historical session rankings |
| `GET /v1/flow/{session}/{ticker}` | Historical ticker detail |
| `GET /v1/momentum/rankings` | Momentum-sorted rankings |
| `GET /v1/momentum/{ticker}/history` | Ticker momentum history |
| `GET /v1/abnormal-trades/current` | Current session abnormal trades |
| `GET /v1/abnormal-trades/{session}` | Historical abnormal trades |
| `GET /v1/account/usage` | Rate limit & usage stats |
| `WS /v1/ws/abnormal-trades` | Real-time abnormal trade stream (Pro) |

### AI Reports

| Endpoint | Description |
|----------|-------------|
| `POST /reports` | Enqueue report generation |
| `GET /reports/{job_id}` | Poll job status |
| `GET /reports/by-id` | Fetch report by metadata |
| `GET /reports/{job_id}/artifact/md` | Fetch report as Markdown |
| `GET /reports/{job_id}/artifact/json` | Fetch report as JSON |
| `GET /reports/history` | Report history for ticker+day |
| `GET /reports/history/summary` | Per-ticker summary |
| `GET /quotas` | Credit usage |
| `POST /eligibility` | Pre-check generation eligibility |
| `GET /health` | Service health check |

## Links

- **Website:** https://www.optionwhales.io
- **API Docs:** https://www.optionwhales.io/developers
- **Flow API Base:** https://api.optionwhales.io
- **AI Report API Base:** https://ai-service-production-b44b.up.railway.app

## License

MIT
