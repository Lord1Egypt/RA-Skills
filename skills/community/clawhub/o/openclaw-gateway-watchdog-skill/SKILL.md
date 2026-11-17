---
name: gateway-watchdog
description: Monitor the OpenClaw Gateway plus configured Spark, Local API Hub, and Dashboard loopback health endpoints with a read-only watchdog state machine, local state files, cooldown dedupe, and optional Discord alerts on macOS. Use for explicitly configured foreground checks, cron execution, LaunchAgent installation, recovery notification, and low-noise incident reporting; it does not rewrite OpenClaw config or restart services.
metadata:
  openclaw:
    version: "1.0.4"
    emoji: "🚨"
    homepage: https://clawhub.ai/jonathanjing/openclaw-gateway-watchdog-skill
    os: [macos]
    requires:
      bins: [bash, python3, openclaw, curl]
    envVars:
      - name: DISCORD_WEBHOOK_URL
        required: false
        description: Optional Discord webhook used for incident notifications.
      - name: DISCORD_BOT_TOKEN
        required: false
        description: Optional Discord bot token used with DISCORD_CHANNEL_ID.
      - name: DISCORD_CHANNEL_ID
        required: false
        description: Optional allowlisted Discord destination.
      - name: SPARK_API_URL
        required: false
        description: Optional Spark status endpoint; defaults to loopback http://127.0.0.1:17070.
      - name: SPARK_API_TOKEN
        required: false
        description: Optional bearer token for the configured Spark status endpoint.
      - name: LOCAL_API_URL
        required: false
        description: Optional Local API Hub base URL; defaults to loopback http://localhost:3456.
      - name: DASHBOARD_PORT
        required: false
        description: Optional loopback Dashboard health port; defaults to 18793.
---

# Gateway Watchdog (Discord)

Discord-first watchdog for OpenClaw gateway incidents.

## 🛠️ Installation

### 1. Ask OpenClaw (Recommended)
Tell OpenClaw: *"Install the gateway-watchdog skill."* Loading a LaunchAgent or configuring Discord delivery remains an explicit operator action.

### 2. Manual Installation (CLI)
If you prefer the terminal, run:
```bash
openclaw skills install @jonathanjing/openclaw-gateway-watchdog-skill
```

## Isolation model

- Watchdog data is isolated under `~/.openclaw/watchdogs/gateway-discord/`.
- No edits to `openclaw.json` are required.
- The shipped watchdog is read-only: it does not rewrite `openclaw.json`, run `doctor --fix`, promote baselines, or restart services.
- Discord delivery exports a bounded incident summary to a third party; use an allowlisted private channel.
- A foreground run probes four targets: OpenClaw Gateway, Spark status, Local API Hub health, and Dashboard health. The latter three default to loopback endpoints and may be overridden with the declared environment variables.
- The script writes per-target state plus an append-only event log under the watchdog data directory. It creates background persistence only when the operator explicitly runs the cron or LaunchAgent installation commands below.
- `config.env` is parsed as data using an allowlist; it is never sourced or executed. For Spark only, the script may read the single `SPARK_API_TOKEN` value from `~/.openclaw/.env` when that token is not already configured.

## Files in this skill

- `scripts/gateway-watchdog.sh` - health checks + state machine + Discord notification.
- `scripts/install-launchd.sh` - installs a user LaunchAgent from template.
- `references/com.openclaw.gateway-watchdog.plist.template` - launchd template.
- `references/cron-agent-turn.md` - isolated cron prompt template.

## Health checks

Every run performs these checks:

```bash
openclaw gateway status --json
openclaw health --json --timeout <ms>
curl "${SPARK_API_URL:-http://127.0.0.1:17070}/status"
curl "${LOCAL_API_URL:-http://localhost:3456}/health"
curl "http://localhost:${DASHBOARD_PORT:-18793}/health"
```

Pass criteria:

- gateway runtime is `running`
- RPC probe is healthy (when present)
- health snapshot returns successfully

Failure classes:

- `runtime_stopped`
- `rpc_probe_failed`
- `health_unreachable`
- `auth_mismatch`
- `config_invalid`
- target-specific Spark, Local API Hub, or Dashboard connectivity failure

## Quick start (manual run)

```bash
bash "{baseDir}/scripts/gateway-watchdog.sh"
```

Optional env:

```bash
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
export DISCORD_BOT_TOKEN="discord_bot_token"
export DISCORD_CHANNEL_ID="<your_discord_channel_id>"
export GW_WATCHDOG_SOURCE="manual"
export GW_WATCHDOG_FAIL_THRESHOLD=2
export GW_WATCHDOG_COOLDOWN_SECONDS=300
```

Delivery priority:

1. `DISCORD_WEBHOOK_URL`
2. `DISCORD_BOT_TOKEN + DISCORD_CHANNEL_ID`

## macOS background mode (LaunchAgent)

Install LaunchAgent (does not edit OpenClaw core config):

```bash
bash "{baseDir}/scripts/install-launchd.sh" --interval 30 --load
```

Check status:

```bash
launchctl list | rg "com.openclaw.gateway-watchdog"
```

## OpenClaw cron mode (internal path)

Use isolated job and keep messaging in one channel:

```bash
openclaw cron add \
  --name "gateway-watchdog-internal" \
  --cron "*/1 * * * *" \
  --session isolated \
  --message "Run bash {baseDir}/scripts/gateway-watchdog.sh and report state changes only." \
  --announce \
  --channel discord \
  --to "channel:<your_channel_id>" \
  --best-effort-deliver
```

## Backup and audit artifacts

- state file: `~/.openclaw/watchdogs/gateway-discord/state.json`
- state backups: `~/.openclaw/watchdogs/gateway-discord/backups/state-*.json`
- event log: `~/.openclaw/watchdogs/gateway-discord/events.jsonl`

The script rotates old backups and keeps recent history for rollback/debugging.
