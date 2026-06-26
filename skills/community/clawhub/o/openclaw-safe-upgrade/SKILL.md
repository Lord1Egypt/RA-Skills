---
name: upgrade
description: Safe OpenClaw upgrade with instant rollback. Use when user says "upgrade openclaw", "update openclaw", "check for updates", or any request to upgrade/update the OpenClaw installation. NOT for config changes (use gateway config.patch). NOT for skill updates (use clawhub).
---

# OpenClaw Safe Upgrade

Single atomic command. Auto-rollbacks on ANY failure. Survives the gateway restart it triggers.

## Script

```bash
# From an agent session — ALWAYS set escape flag (ensures script survives gateway restart)
_UPGRADE_FORCE_ESCAPE=1 bash skills/upgrade/scripts/safe-upgrade.sh

# Force upgrade even if already on latest
_UPGRADE_FORCE_ESCAPE=1 bash skills/upgrade/scripts/safe-upgrade.sh --force

# Safe read-only checks (no escape needed)
bash skills/upgrade/scripts/safe-upgrade.sh --check      # Pre-flight only
bash skills/upgrade/scripts/safe-upgrade.sh --rollback    # Manual rollback
```

## What Happens (one command, 10 steps)

1. **Cgroup escape**: re-execs via `systemd-run --user --scope` so gateway stop can't kill the script
2. Pre-flight: version check, disk space, breaking changes
3. Backup: installation tarball, config, cron jobs, acpx customizations
4. `npm i -g openclaw@latest`
5. Restore acpx config (ACP agent customizations survive upgrades)
6. Gateway restart (process-isolated: stop + start, survives script's own lifecycle)
7. Wait for gateway health (configurable timeout) → **auto-rollback if fails**
8. Wait for WhatsApp reconnect (non-fatal timeout)
9. Verify: correct version + cron count preserved → **auto-rollback if fails**
10. Record result → optional golden snapshot → cleanup backup

If ANY critical check fails, the script **automatically rolls back** — restores install, config, crons, and acpx. Trap handler catches unexpected exits during critical phases.

## Agent Workflow

1. Run `--check` first. Review output with the user.
2. Inform user: "Launching upgrade — I'll go offline during gateway restart."
3. Run the upgrade:
   ```bash
   _UPGRADE_FORCE_ESCAPE=1 bash skills/upgrade/scripts/safe-upgrade.sh
   ```
   **Do NOT pipe the output** (no `| tee`, no `2>&1 | cat`). The script writes to `/tmp/upgrade-live.log`.
4. **The current session will end** when the gateway restarts. This is expected.
5. After restart, the new session checks:
   - `~/.openclaw/upgrade-result.json` for status
   - `/tmp/upgrade-live.log` for live output
   - `success`: report to user, update any version references
   - `rolled_back`: tell user what went wrong (reason in result file)
   - No result file + backup at `~/.openclaw/upgrade-backups/current/`: script was killed — run `--rollback`
6. Full forensic log at `~/.openclaw/upgrade-last.log`.

## What Gets Backed Up

- OpenClaw installation tarball
- Config (`openclaw.json`)
- Cron jobs (`jobs.json`)
- acpx user config (`~/.acpx/config.json`) if present
- Metadata (from/to version, timestamp, cron count)

Backup location: `~/.openclaw/upgrade-backups/current/`

## Result File

`~/.openclaw/upgrade-result.json`:

```json
{
    "status": "success|rolled_back|rollback_failed|no_change|blocked",
    "from_version": "2026.3.2",
    "to_version": "2026.3.7",
    "message": "...",
    "timestamp": "...",
    "log": "~/.openclaw/upgrade-last.log"
}
```

## Why Cgroup Escape?

OpenClaw runs as a systemd service. When an agent runs this script, the script is a child process inside the service's cgroup. `systemctl stop` sends SIGKILL to ALL processes in the cgroup — including the upgrade script. SIGKILL cannot be caught (no trap handler fires).

The script detects this and re-execs itself via `systemd-run --user --scope` into its own transient systemd scope. The parent process exits immediately — no pipes, no tee, no connections back to the gateway cgroup. This is why piping output is forbidden.

## Important Notes

- **Never run `gateway update.run` directly** — always use this script
- **Always set `_UPGRADE_FORCE_ESCAPE=1`** when running from an agent session
- acpx customizations are auto-preserved across upgrades
- Rollback restores the EXACT previous state: install + config + crons + acpx
- `--check` is safe to run anytime, changes nothing
- The script auto-detects gateway port from config (no hardcoded defaults)
- Optional hooks: if `golden-snapshot.sh` or `service-quick-check.py` exist in your workspace, they're used; otherwise silently skipped
