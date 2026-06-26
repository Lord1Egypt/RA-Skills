# Onboarding

Require onboarding before any private Aster action. The onboarding flow collects the minimum required information, fills in sensible defaults for everything else, and culminates in an **explicit autonomous trading consent gate**.

If the user accepts, the agent:
1. Writes `config.json` with `mode=autonomous_live`
2. Registers OpenClaw cron jobs for 24/7 operation
3. Starts the first live trading cycle immediately

## Secrets (collected, stored as env vars — never in config.json)
- `ASTER_API_KEY`
- `ASTER_API_SECRET`

## Required from user (minimum — everything else has defaults)
- Aster API key
- Aster API secret
- Allowed trading symbols (e.g. BTCUSDT, ETHUSDT)
- Base investment per trade (USD)
- Max leverage

## Optional overrides (defaults shown)
- Min leverage (default: 2)
- Max daily loss in USD (default: 10% of total exposure)
- Max total exposure in USD (default: base_value × 10)
- Max concurrent positions (default: 3)
- Allow short positions (default: yes)
- Scan interval in minutes (default: 2)

## Onboarding prompt template

Present this to the user when they first talk to MoneySharks:

```
Welcome to MoneySharks 🦈 — your autonomous Aster Futures trading agent.

I need just a few things to get started:

1. Aster API key:
2. Aster API secret:
3. Symbols to trade (e.g. BTCUSDT ETHUSDT SOLUSDT):
4. Base investment per trade in USD (e.g. 100):
5. Max leverage (e.g. 10):

Everything else (stop-loss, take-profit, position sizing, risk limits) 
is handled automatically using best-practice defaults.

You can customise further after setup if you want.
```

After collecting the 5 required fields, compute defaults:
- `min_leverage` = 2
- `max_notional_per_trade` = `base_value_per_trade` × `max_leverage`
- `max_total_exposure` = `base_value_per_trade` × 10
- `max_daily_loss` = `max_total_exposure` × 0.10
- `max_concurrent_positions` = 3
- `allow_short` = true
- `require_stop_loss` = true
- `require_take_profit` = true
- `min_reward_risk` = 1.5
- `risk_pct_per_trade` = 0.01 (1% of equity)
- `cooldown_after_close_sec` = 120
- `minimum_hold_sec` = 60
- `cron.scan_interval_minutes` = 2

## ⚠️ Autonomous Live Trading Consent Gate

Present this **after** collecting the parameters:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  AUTONOMOUS LIVE TRADING — READ CAREFULLY BEFORE ACCEPTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your setup summary:
  • Symbols: [symbols]
  • Base investment: $[base_value] per trade
  • Leverage: [min_lev]× – [max_lev]×
  • Max daily loss: $[max_daily_loss]
  • Max total exposure: $[max_total_exposure]
  • Scan interval: every [scan_interval] minutes

By typing ACCEPT below, you authorise MoneySharks to:

  • Place and manage REAL leveraged orders on Aster DEX using
    your API credentials, 24 hours a day, 7 days a week.
  • Execute trades automatically WITHOUT asking for your
    approval on each individual trade.
  • Manage, modify, and close open positions autonomously.
  • Operate continuously via background cron until you halt it.

Hard safeguards always active:
  • Max daily loss cap ✓
  • Stop-loss on every trade ✓
  • Take-profit on every trade ✓
  • Leverage capped at configured max ✓
  • Circuit breakers ✓

To stop at any time, say:
  "halt moneysharks" / "kill switch" / "switch to paper mode"

⚠️  Futures trading is HIGH RISK. You may lose your entire
    deposit. Past performance does not guarantee future results.

Type ACCEPT to enable autonomous live trading.
Type DECLINE to run in paper (simulation) mode instead.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### On ACCEPT:
1. Write `config.json` with all parameters + `mode=autonomous_live` + `autonomous_live_consent=true`
2. Set `cron.enabled=true`, `cron.scan_interval_minutes=2`
3. Set `execution.require_human_approval_for_live_orders=false`
4. Run `python3 scripts/register_crons.py config.json --skill-root <skill_dir> --mode autonomous_live`
   to generate `register_crons.json` with real paths substituted.
5. Register 4 OpenClaw cron jobs — read `register_crons.json` and call `cron(action="add", job=...)` for each:
   - `autonomous_live_scan`: every 2 min, sessionTarget=isolated, agentTurn, delivery.mode=none
   - `autonomous_review`: every 30 min, sessionTarget=isolated, agentTurn, delivery.mode=none
   - `autonomous_daily_summary`: daily 00:00 UTC, sessionTarget=isolated, agentTurn, delivery.mode=announce
   - `halt_check`: every 15 min, sessionTarget=isolated, agentTurn, delivery.mode=announce
6. Run first cycle immediately: `python3 scripts/autonomous_runner.py config.json`
7. Show status: `python3 scripts/status.py config.json`
8. Confirm to user:

```
✅ MoneySharks is now live and running autonomously.

Trading: [symbols]
Scan interval: every 2 minutes
Max daily loss: $[max_daily_loss]
Leverage: up to [max_lev]×

The agent will scan markets, compute signals, and execute trades 
24/7 without interrupting you. You'll get a daily summary each morning.

To stop at any time: "halt moneysharks"
To check status: "moneysharks status"
To see today's trades: "moneysharks trades"
```

### On DECLINE:
1. Write `config.json` with `mode=paper`, `autonomous_live_consent=false`
2. Enable paper-mode cron jobs only (`paper_market_scan`, `paper_review_cycle`)
3. Confirm: "Running in paper (simulation) mode. No real orders will be placed. Say 'go live' when you're ready to switch."

## Secret handling
- Store credentials in env vars (`ASTER_API_KEY`, `ASTER_API_SECRET`), not in `config.json`
- Instruct the user to set these in their shell profile or OpenClaw env config
- Never print the full secret — mask as `****xxxx` (last 4 chars only)
- Never log credentials to `trades.json`, `state.json`, or any log file
