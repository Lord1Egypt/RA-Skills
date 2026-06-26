## Inspection Requirements Confirmation

⚠️ **These steps MUST be executed in the following order. Do not skip or reorder any step.**

### Step 1: Parse User Intent

When user provides a target (e.g., "inspect 10.110.10.146 26257 8080"), extract and confirm:
- Node address(es)
- Database port (default 26257)
- Admin console port (default 8080)

**Do NOT proceed to Step 2 until target info is confirmed with user.**

---

### Step 2: Probe Connectivity

After confirming target info with user, verify reachability using appropriate tools (e.g., `nc`, `telnet`, `curl`, `ping`):
- Check database port (26257) and admin console port (8080)
- If ports unreachable: inform user and ask them to verify network/firewall/service
- Only proceed if ports are reachable

**Do NOT proceed to Step 3 until ports are confirmed reachable.**

---

### Step 3: TLS Mode Detection

Only after connectivity is confirmed, check TLS status:

**Must strictly use this exact command format, only replace `<host>` and `<admin-port>` with actual values:**
```
curl -k https://<host>:<admin-port>/health
```
- If output contains `error:0A00010B` or `wrong version number` → TLS not enforced, proceed
- If returns JSON health data with no error → TLS enabled, **inspection not supported** (stop here)

**Do NOT proceed to Step 4 until TLS mode is determined.**

---

### Step 4: Present Scope Menu

Read `references/report-template.md` and `references/anomaly-rules.md`, then show user:
- Full inspection scope (Sections 1-6)
- Default rules and configurable rules (only applied if user requests alerting)
- Ask user to confirm which metrics to inspect and whether to enable alerting

**Do NOT proceed to metrics collection until user confirms the scope.**
