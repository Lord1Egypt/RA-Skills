# Gateway Watchdog Discord

Discord-first read-only watchdog skill for OpenClaw Gateway health monitoring and recovery notification.

## 🛠️ Installation

### 1. Ask OpenClaw (Recommended)
Tell OpenClaw: *"Install the gateway-watchdog skill."* Loading persistence or configuring Discord remains an explicit operator action.

### 2. Manual Installation (CLI)
If you prefer the terminal, run:
```bash
openclaw skills install @jonathanjing/openclaw-gateway-watchdog-skill
```

## What This Skill Does

- Monitors Gateway health with a state machine (`healthy`, `degraded`, `critical`)
- Probes configured Spark, Local API Hub, and Dashboard loopback health endpoints on every run
- Sends Discord incident messages (`ALERT`, `RECOVERED`)
- Deduplicates noisy failures using threshold + cooldown
- Does not rewrite config, promote baselines, run `doctor --fix`, or restart services
- Runs via two paths:
  - Internal OpenClaw cron (normal operations)
  - External macOS LaunchAgent fallback (when Gateway is unhealthy)

## Why Two Paths

- **Cron path** is the native OpenClaw scheduler route and easy to manage with `openclaw cron`.
- **LaunchAgent path** is a fallback that can still run even when OpenClaw Gateway scheduling is impaired.

Using both gives better resilience than cron-only monitoring.

## Skill Layout

- `SKILL.md` - Agent-facing skill instructions
- `scripts/gateway-watchdog.sh` - Core watchdog logic
- `scripts/install-launchd.sh` - LaunchAgent installer helper
- `references/com.openclaw.gateway-watchdog.plist.template` - launchd template
- `references/cron-agent-turn.md` - Isolated cron prompt template

## Runtime Data Isolation

All runtime artifacts stay in:

`~/.openclaw/watchdogs/gateway-discord/`

Files:

- `state.json` - current watchdog state
- `events.jsonl` - append-only event history
- `backups/state-*.json` - rolling state backups
- `config.env` - local deployment config (tokens/channel ids)

This avoids touching OpenClaw core files for normal watchdog operation.

The script writes separate state files for Gateway, Spark, Local API Hub, and
Dashboard plus an append-only event log. `config.env` is parsed through an
allowlist and is not sourced as shell code. If `SPARK_API_TOKEN` is not already
configured, the script may read only that named value from
`~/.openclaw/.env`.

## Detection Logic

The watchdog checks:

- `openclaw gateway status --json`
- `openclaw health --json --timeout <ms>`
- `${SPARK_API_URL:-http://127.0.0.1:17070}/status`
- `${LOCAL_API_URL:-http://localhost:3456}/health`
- `http://localhost:${DASHBOARD_PORT:-18793}/health`

Failure classes:

- `runtime_stopped`
- `rpc_probe_failed`
- `health_unreachable`
- `auth_mismatch`
- `config_invalid`
- `gateway_check_failed`

Alerting rules:

- Alert only after `GW_WATCHDOG_FAIL_THRESHOLD` consecutive failures
- Suppress repeated alerts during `GW_WATCHDOG_COOLDOWN_SECONDS`
- Send `RECOVERED` once when transitioning back to healthy
- Alert body is human-readable (reason label + observed symptom + suggested action)

## Prerequisites

- OpenClaw CLI installed and available (`openclaw`)
- Python 3 available (`python3`)
- macOS (for LaunchAgent mode)
- Discord delivery config (webhook or bot token)

## Delivery Modes

Priority order:

1. `DISCORD_WEBHOOK_URL`
2. `DISCORD_BOT_TOKEN` + `DISCORD_CHANNEL_ID`

If webhook is set, webhook is used first. Otherwise bot API is used.

## Quick Start

Run once manually:

```bash
bash "{baseDir}/scripts/gateway-watchdog.sh"
```

Optional env:

```bash
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
export DISCORD_BOT_TOKEN="<your_discord_bot_token>"
export DISCORD_CHANNEL_ID="<your_discord_channel_id>"
export GW_WATCHDOG_SOURCE="manual"
export GW_WATCHDOG_FAIL_THRESHOLD=2
export GW_WATCHDOG_COOLDOWN_SECONDS=300
```

## Install LaunchAgent Fallback

Install and load with 30s interval:

```bash
bash "{baseDir}/scripts/install-launchd.sh" --interval 30 --load
```

Check status:

```bash
launchctl list | grep "com.openclaw.gateway-watchdog"
```

## Configure Internal OpenClaw Cron

```bash
openclaw cron add \
  --name "gateway-watchdog-internal" \
  --cron "*/1 * * * *" \
  --session isolated \
  --message "Run bash /absolute/path/to/scripts/gateway-watchdog.sh. Announce only state changes." \
  --announce \
  --channel discord \
  --to "channel:<your_channel_id>" \
  --best-effort-deliver
```

## Configuration Reference

Common variables:

- `GW_WATCHDOG_BASE_DIR` (default: `~/.openclaw/watchdogs/gateway-discord`)
- `GW_WATCHDOG_FAIL_THRESHOLD` (default: `2`)
- `GW_WATCHDOG_COOLDOWN_SECONDS` (default: `300`)
- `GW_WATCHDOG_HEALTH_TIMEOUT_MS` (default: `10000`)
- `GW_WATCHDOG_SOURCE` (default: `unknown`)

Binary overrides:

- `OPENCLAW_BIN`
- `PYTHON_BIN`

## Test Checklist

Use this before production rollout:

1. **Syntax checks**
   - `bash -n "{baseDir}/scripts/gateway-watchdog.sh"`
   - `bash -n "{baseDir}/scripts/install-launchd.sh"`
2. **Manual smoke run**
   - `GW_WATCHDOG_SOURCE=test bash "{baseDir}/scripts/gateway-watchdog.sh"`
3. **Discord delivery test**
   - verify one test message arrives in your target channel
4. **Failure test**
   - stop/impair Gateway and verify `ALERT`
5. **Recovery test**
   - restore Gateway and verify `RECOVERED`

## Troubleshooting

- **No Discord messages**
  - Check `config.env` values and token/channel correctness
  - Validate bot has permission to post in target channel
- **`watchdog lock exists, exiting`**
  - Another run is active; this is expected for overlap protection
- **Repeated suppressed events**
  - Cooldown/threshold is working; lower values for aggressive alerting
- **Gateway healthy but still alerting**
  - Re-run `openclaw gateway status --json` and `openclaw health --json`
  - Ensure `OPENCLAW_BIN` resolves to the expected OpenClaw install

## Security Notes

- Do not commit `config.env` (contains credentials/ids in real deployments)
- Use minimum required Discord permissions for the bot
- Prefer webhook mode for simple one-channel alerting
- Discord alerts disclose bounded operational status to a third party; use a private allowlisted destination

## Publishing Notes

This repository is structured for ClawHub publishing:

```bash
clawhub skill publish . \
  --slug openclaw-gateway-watchdog-skill \
  --name "Gateway Watchdog Discord" \
  --version <x.y.z> \
  --changelog "..."
```
