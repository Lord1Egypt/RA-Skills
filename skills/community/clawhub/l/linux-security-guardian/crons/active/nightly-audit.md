---
name: nightly-security-audit
type: permanent
schedule: "30 19 * * *"
schedule_ist: "01:00 IST daily"
schedule_utc: "19:30 UTC daily"
timezone: Asia/Kolkata
purpose: Full multi-client Linux server security audit — iterate all clients → all servers → 18 modules via SSH MCP, CVE scan, auto-fix safe issues, queue critical for confirm, per-server report via email plugin
fire_once: false
auto_delete: false
status: active
---

# Nightly Security Audit — 1:00 AM IST

Fires every night at 01:00 IST (19:30 UTC previous day).
Execute hooks/audit-runner.md in full.

## Orchestration Flow
```
1. Parse SERVER_PROFILE.md → all ## Client: sections
2. For each client → iterate all servers in their fleet
3. Per server:
   - SSH MCP connect
   - Pre-audit snapshots
   - Run all 18 audit modules
   - Auto-actions phase
   - Compile per-server report → reports/<client>/<server>/daily/
   - SSH MCP disconnect
4. Compile per-client summary → reports/<client>/summary-YYYY-MM-DD.md
5. Compile master report → reports/master-YYYY-MM-DD.md
6. Send reports via email plugin (per-server, per-client, master)
```

## OpenClaw Cron Registration
```
# In OpenClaw config / crontab:
30 19 * * * openclaw run linux-security-guardian audit-runner
# OR via AgentTurn cron:
30 19 * * * agentturn trigger linux-security-guardian nightly-audit
```

## Expected Duration
- ~15-30 min per server depending on size and CVE scan
- 7 servers (client-1): ~2-3.5 hours
- CISA KEV + OSV.dev: ~30s per server
- NVD API (without key, 10 packages): ~60s per server
- Full audit with all sources: ~15-25 min per server
- Report delivered via email plugin after each server

## THIS FILE MUST NEVER BE DELETED.
