# Deployment

MoneySharks supports fully autonomous 24/7 deployment in `autonomous_live` mode.
This means real money, real orders, continuous operation.

## Prerequisites

- Aster DEX API key and secret with **Futures trading permissions enabled**
- Python 3.11+
- `ASTER_API_KEY` and `ASTER_API_SECRET` in the service environment (never in config files)
- `config.json` with `mode=autonomous_live`, `autonomous_live_consent=true`
- `state.json` and `trades.json` writable by the service process
- `logs/` directory writable by the service process

## Setup

```bash
# 1. Clone / install to your target path
cp config.example.json config.json
# Edit config.json with your risk parameters

# 2. Validate config
python3 scripts/validate_config.py < config.json

# 3. Set credentials in environment (do NOT put them in config.json)
export ASTER_API_KEY="your_api_key"
export ASTER_API_SECRET="your_api_secret"

# 4. Dry-run (paper mode) first
python3 scripts/autonomous_runner.py config.json

# 5. Run one live cycle manually to confirm
# (only after setting mode=autonomous_live and autonomous_live_consent=true)
python3 scripts/autonomous_runner.py config.json
```

## macOS — launchd (24/7 via plist)

Use `deploy.launchd.plist` as the template.
- Replace all `/ABSOLUTE/PATH/TO/...` with real paths
- Set `ASTER_API_KEY` and `ASTER_API_SECRET` in the `EnvironmentVariables` section
- Load with: `launchctl load ~/Library/LaunchAgents/com.moneysharks.scan.plist`
- Unload with: `launchctl unload ~/Library/LaunchAgents/com.moneysharks.scan.plist`

## Linux — systemd

Use `deploy.systemd.service` + `deploy.systemd.timer` as templates.
- `moneysharks.service`: runs `autonomous_runner.py` on demand
- `moneysharks.timer`: triggers the service every 2 minutes
- Set `ASTER_API_KEY` and `ASTER_API_SECRET` in a credentials env file (e.g. `/etc/moneysharks/env`), chmod 600
- Enable: `systemctl enable --now moneysharks.timer`
- Stop: `systemctl stop moneysharks.timer moneysharks.service`

## OpenClaw cron (recommended for OpenClaw deployments)

Use the templates in `openclaw-cron-templates.json`:
- **`autonomous_live_scan`** — every 2 min, runs the full autonomous execution cycle
- **`autonomous_review`** — every 30 min, reviews trade journal and updates metrics
- **`autonomous_daily_summary`** — daily at 00:00, announces full day summary
- **`halt_check`** — every 15 min, alerts if circuit breaker or halt is active

Enable via OpenClaw cron after updating the `/ABSOLUTE/PATH/TO/moneysharks` placeholder.

## Emergency stop

From chat: "halt moneysharks" / "kill switch" / "switch to paper mode"

These set `state.json → halt=true`, which the runner checks at the start of every cycle.
See `references/emergency-controls.md` for the full halt sequence.

## Path placeholders

Replace `/ABSOLUTE/PATH/TO/moneysharks` with the actual install path in:
- `deploy.launchd.plist`
- `deploy.systemd.service`
- `deploy.systemd.timer`
- `moneysharks-scan.service`
- `openclaw-cron-templates.json`
- `logrotate.moneysharks.conf`
- `newsyslog.moneysharks.conf`

## Production checklist

- [ ] Config validated (`validate_config.py` returns ok=true)
- [ ] Credentials in env, NOT in config.json
- [ ] `state.json` exists and writable
- [ ] `trades.json` exists and writable (or will be auto-created)
- [ ] `logs/` directory writable
- [ ] Paper mode dry-run passed
- [ ] Manual single live cycle tested
- [ ] All `/ABSOLUTE/PATH/TO/...` replaced in templates
- [ ] Emergency halt tested (set state.json halt=true, confirm cycle stops)
- [ ] Cron/service enabled and health checks configured
