---
name: linux-security-guardian-audit-runner
description: Main audit orchestrator. Fires at 1 AM IST. Iterates all clients → all servers → runs 18 modules via SSH MCP, collects findings, applies auto-actions, queues confirmations, compiles per-server reports, compiles master report, sends via email plugin.
---

# Audit Runner — 1 AM IST

## Multi-Client Orchestration

SERVER_PROFILE.md may contain one or more `## Client:` sections.
The runner MUST iterate ALL clients → ALL servers.

```
for each client in parse_clients(SERVER_PROFILE.md):
  for each server in client.server_fleet:
    ssh_mcp_connect(server)
    run_all_18_modules(client, server)
    auto_actions_phase(client, server)
    compile_per_server_report(client, server)
    ssh_mcp_disconnect()
  compile_per_client_summary(client)
compile_master_report()
send_via_email_plugin()
```

---

## Phase 0 — Pre-Audit: Parse Client List

```
1. Read SERVER_PROFILE.md
2. Extract all ## Client: <name> sections
3. For each client, extract server fleet table (host, port, username, key_path)
4. Abort if zero clients found
5. Log: "CLIENTS: <list> | TOTAL_SERVERS: <count>"
```

---

## Phase 1 — SSH MCP Connection (per server)

```
For each (client, server):
  1. Verify SSH MCP tools available:
     → Required: ssh_conn, ssh_exec
     → If any missing → ABORT audit for this server, alert owner

  2. Read SERVER_PROFILE.md → Client/<client>/Server/<server> Connection ID
     → If connection_id is set:
       → Verify: ssh_conn(op="list") → grep for connection_id
       → If not found → log error, ABORT this server
     → If connection_id is empty but host/username/key_path are set:
       → ssh_conn(op="test", host, port, username, key_path) → verify reachable
       → If fails → ABORT this server: "Server <server> unreachable via SSH MCP"
       → ssh_conn(op="save", name="<client>-<server>", host, port, username, key_path) → save it
       → Get connection_id from returned data

  3. ssh_exec(op="open", connectionId) → returns sessionId
     → If fails → ABORT this server: "SSH MCP connection failed for <client>/<server>"
     → sessionId stored for ALL subsequent commands on this server

  4. Running commands in modules:
     → Prefer array commands: ssh_exec(op="run", sessionId, command=["cmd1", "cmd2", ...])
     → Retrieve output: ssh_exec(op="logs", commandId, stream="stdout")
```

---

## Phase 2 — Pre-Audit Checks (per server)

```
For each (client, server) with active sessionId:

  1. Check available tools:
     → ssh_exec(op="run", sessionId, command="which debsecan cvescan rkhunter aide fail2ban-client")
     → Log tool availability to audit/results/<client>/<server>/info/

  2. Take snapshots:
     → iptables-save → network/<client>/<server>/firewall-snapshots/YYYY-MM-DD-rules.txt
     → ss -tulpn → temp store for comparison in module 08
     → dpkg-query -W -f='${Package}\t${Version}\n' → cve/<client>/<server>/scan-results/installed-packages.txt
       OR rpm -qa --queryformat '...'

  3. Initialize per-server report structure
```

---

## Phase 3 — Module Execution (per server, modules 01-18)

```
For each module 01 through 18:
  For each command in module:
    → cmdId = ssh_exec(op="run", sessionId, command="<command>")
    → sleep 1-3s (adjust based on command duration)
    → output = ssh_exec(op="logs", commandId=cmdId, stream="stdout")
    → If ssh_exec fails (error or timeout):
      → retry once with increased wait
      → If still fails → log "[MODULE FAILED] <client>/<server> NN-<name>: <error>"
      → Continue to next module (never abort entire audit for one module failure)
    → Parse output → classify finding → write to audit/results/<client>/<server>/<severity>/
    → If CRITICAL finding → fire hooks/on-critical.md immediately (client, server context)
  Log: "module-NN complete | findings: N"
```

**For module 07, run external CVE scan before local methods:**
```bash
# External CVE sources (CISA KEV + OSV.dev + NVD API)
# Uses cve-scan.sh with client/server params
if [ -f "cve/$client/$server/scan-results/installed-packages.txt" ]; then
    bash cve/cve-scan.sh --client "$client" --server "$server" 2>&1
    # Output: cve/<client>/<server>/scan-results/YYYY-MM-DD.md
    # Advisories: cve/<client>/<server>/advisories/<CVE-ID>.md
    # Labels: KEV → CRITICAL, RANSOMWARE → 🔥 FIRE on-critical.md
fi
```

---

## Phase 4 — Auto-Actions Phase (per server)

```
For each finding with defined auto-action:
  Check SERVER_PROFILE.md → Client/<client>/auto-actions whitelist
  If whitelisted AND passes security checks:
    → Run hooks/pre-action.md (with client, server context)
    → Execute action via SSH MCP
    → Run hooks/post-action.md
    → Log to actions/<client>/<server>/auto-done/YYYY-MM-DD-<slug>.md
  Else:
    → Queue to actions/<client>/<server>/pending-confirm/<client>-<server>-<id>-<slug>.md
    → Include in per-server report under "NEEDS YOUR DECISION"
```

---

## Phase 5 — Scoring Phase (per server)

```
score = 100
score -= (critical_count × 20)
score -= (high_count × 10)
score -= (medium_count × 3)
score -= (low_count × 1)
score = max(0, score)
grade = A if score>=90 else B if score>=75 else C if score>=60 else F
```

---

## Phase 6 — Per-Server Report Compilation

```
Compile findings into reports/<client>/<server>/daily/YYYY-MM-DD.md

Format:
  Subject Header: <client> / <server> | YYYY-MM-DD
  Security Score: N/100 (Grade X)
  Critical: N | High: N | Medium: N | Low: N
  Auto-fixed: N | Pending confirm: N | Passed: N

  🔴 CRITICAL — [finding details]
  🟠 HIGH — [finding details]
  ⚡ AUTO-ACTIONS TAKEN — [auto-fixed items]
  🔑 NEEDS YOUR DECISION — [pending confirmations with IDs]
  📦 CVE REPORT — [merge from cve/<client>/<server>/scan-results/YYYY-MM-DD.md]
  🌐 NETWORK & FIREWALL — [port/firewall status]
  🟡 MEDIUM / LOW — [less urgent]
  🟢 PASSING — [all-checks-pass list]
```

---

## Phase 7 — SSH MCP Disconnect (per server)

```
→ ssh_exec(op="close", sessionId)
→ Verify: ssh_exec(op="list") → confirm sessionId is gone
→ If close fails → log "SSH MCP: disconnect error for <client>/<server>" (non-fatal)
→ Log "SSH MCP: disconnected <client>/<server> cleanly"
```

---

## Phase 8 — Per-Client Summary

```
After all servers in a client processed:
  Compile reports/<client>/summary-YYYY-MM-DD.md
  Include:
    - Servers audited / total
    - Aggregate scores (min, max, avg)
    - Total critical/high across all servers
    - Cross-server patterns (same vuln on multiple servers)
```

---

## Phase 9 — Master Report

```
After all clients processed:
  Compile master audit report
  Include:
    - Clients audited: N
    - Total servers: N
    - Overall security posture
    - Per-client summary table
    - Links to per-server reports
    - Pending confirmations across all clients
```

---

## Phase 10 — Email Phase

Use email plugin/skill to send reports (not implemented inline).

**Per-server email** → to client's notification_email from SERVER_PROFILE.md
```
Subject: "[Linux Guardian] <client>/<server> — YYYY-MM-DD | Score: N/100 (Grade X) | CRITICAL:N HIGH:N"
```

**Per-client summary email** → to client's notification_email
```
Subject: "[Linux Guardian] <client> Summary — YYYY-MM-DD | Servers: N/N | CRITICAL:N HIGH:N"
```

**Master report email** → to global notification email
```
Subject: "[Linux Guardian] Master Audit Report — YYYY-MM-DD | Clients:N | Servers:N"
```

→ Use default email account. Never specify --account admin.
→ If no email skill available → log to AUDIT_LOG.md, reports on disk.

---

## Phase 11 — Soul Update + Audit Log

```
Update soul sections with per-client and per-server audit data.
Append AUDIT_LOG.md: "YYYY-MM-DD 01:XX IST | audit_complete | clients:N | servers:N | score_avg:N | critical:N | high:N"
```

---

## Per-Server Execution Notes

- Each server gets its own sessionId — sessions do NOT overlap
- If a server is unreachable → log failure, continue to next server
- If a module fails → log "[MODULE FAILED]", continue to next module, never abort
- If SSH MCP fails mid-audit → try reconnect once, if fails → log error for findings so far, continue to next server
- All findings saved to per-server paths with <client>/<server> prefix
