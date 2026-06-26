# Alert Gateway Architecture

_Status: **Planning complete** — implementation not started (as of 2026-04-05)_

---

## Problem

Multiple alert sources (Zabbix, Graylog, potentially more) currently deliver webhooks directly to OpenClaw hooks endpoint. Issues:

- Too many entries in web interface — hard to find the right channel
- No alert history or pattern analysis
- No intelligent filtering to suppress noise
- No persistent queue — events lost if OpenClaw is down
- Intrusion detection (Graylog) could flood on port scans

---

## Proposed Architecture

```
┌─────────┐  ┌─────────┐  ┌──────────────┐
│ Zabbix  │  │ Graylog │  │Future sources│
└────┬────┘  └────┬────┘  └──────┬───────┘
     │            │              │
     └────────────┼──────────────┘
                  │ HTTP POST
     ┌────────────▼──────────────┐
     │   Alert Gateway           │
     │  (Python / FastAPI)       │
     │  https://alerts.example.com │
     │  Port 8090 (MB-OPENCLAW)│
     │                           │
     │  1. Validate (HMAC → IP)  │
     │  2. Store raw to DB       │
     │     (+ local buffer if    │
     │      DB unreachable)      │
     │  3. Run rules             │
     │  4. Find/create incident  │
     │     (correlates by host)  │
     │  5. Escalate → Telegram   │
     │  6. LLM filter (last)     │
     └────────┬──────────────────┘
              │ escalation
              ▼
        ┌─────────────┐     ┌─────────┐
        │ Telegram    │────→│ Owner   │
        │ (direct)    │     │ (phone) │
        └─────────────┘     └────┬────┘
                                  │
                           "what details?"
                                  │
                          ┌───────▼──────┐
                          │  Query DB    │
                          │  (I look)    │
                          └──────────────┘
```

---

## Design Decisions

| Decision | Detail |
|---|---|
| **Deployment** | MB-OPENCLAW, port 8090, Caddy route `alerts.example.com`. Already provisioned with live cert. |
| **Database** | New `sysclaw_alerts` DB on MB-PGDB — 8 tables + `rule_suggestions`, typed columns + JSONB metadata. Ceph-backed with HA. |
| **Authentication** | HMAC signature validation is primary gate. IP allowlist is secondary/fallback. If `secret_hash` is NULL for a source, skip HMAC and fall back to IP-only (allows incremental onboarding). |
| **Incident correlation** | Host-only. `correlation_key = host` (normalized). One open incident per host across all sources. Source detail lives on individual `alerts` rows. |
| **LLM Filter** | LAST in chain. Rules/scripts do 95% of filtering. LLM handles edge cases only. Passive-first (observe + tag, no suppression) — activates after 50–100 alerts. Counter stored in `gateway_state`. See [LLM Role](#llm-role) section. |
| **Escalation** | Minimal Telegram ping directly from gateway. Example: `🚨 [CRITICAL] PiHole-01 DNS service down`. No extra info until requested. |
| **Major incident** | ≥4 escalations in 15 min → declare major incident, stop all further escalation messages, log to incident metadata. Manual intervention required. **Major incident always overrides quiet hours.** |
| **Multi-target** | Configurable notification targets via DB — multiple recipients, per-target quiet hours (overridden by major incident). |
| **Persistence** | ALL raw alerts stored. Retention is 500MB soft cap — review at limit, no auto-delete. |
| **Source validation** | HMAC first, IP allowlist second. Drop on either failure. |
| **Local buffer** | If DB unreachable: (1) send Telegram "⚠️ DB unreachable — buffering alerts" if targets in memory cache, (2) write alerts to `/opt/alert-gateway/buffer/`, (3) on recovery: send "✅ DB restored — X alerts buffered during outage", replay with `from_buffer=true` flag. Buffered alerts skip escalation but still correlate to incidents. |
| **Target memory cache** | Targets loaded from DB at startup, written to `/opt/alert-gateway/cache/targets.json`. If DB is down at startup, load from cache file. Enables DB-down Telegram notifications. |
| **Telegram rate limit** | Max 4 escalation messages per 15 min window. If exceeded → declare major incident, suppress further notifications. Retry: 30s × 5, then mark failed. |
| **Health endpoint** | `GET /healthz` returns JSON health check (DB connectivity, buffer status). Exempt from token authentication. |
| **Skill** | OpenClaw skill named `noise-maker` (verify availability on ClawHub before publishing). Self-contained under `~/.openclaw/skills/noise-maker/`. Runbook and scripts live inside the skill directory. Startup check written to skill dir by gateway on boot. |
| **Startup check** | Gateway writes `~/.openclaw/skills/noise-maker/startup-check.json` on boot: open incident count, buffer status, stale incidents (non-Zabbix, age > 72h). Skill `before_agent_start` hook injects a one-liner into context if anything needs attention. Zero context cost when clean. |

---

## Data Flow

```
1.  Raw webhook arrives at /ingest/{source_name}
2.  Validate HMAC signature (primary) → validate source IP (fallback)
    Drop immediately if either fails
3.  Store raw in alerts (always)
    - Compute dedup_key → if exists, drop duplicate
    - If DB unreachable → write to local disk buffer, send Telegram warning
4.  Run rules (priority ordered, first match or stack)
5.  Collect final action: escalate | suppress | defer | tag_only
    [LLM invoked here only if no rule matched or edge case]
6.  If escalate/summarize:
    a. Normalize host (strip domain suffix, lowercase)
    b. Find open incident for this HOST (correlation_key = normalized host)
    c. If found → increment alerts_count, update metadata, current_severity
    d. If not found → create new incident (starts open)
7.  Send Telegram escalation (if target exists + within rate limit + not from_buffer)
8.  Log rule execution
9.  If suppress/defer → stored in rule_executions for audit

Buffer replay (background):
- Check /opt/alert-gateway/buffer/ every 30s
- Sort by received_at before replay (order guarantee)
- If DB available → replay pending alerts with from_buffer=true
  - Skip escalation step for buffered alerts
  - Still correlate to incidents (increment count, update metadata)
  - Delete buffer file after successful write
- Log replay to database for audit
- On recovery: send Telegram summary "X alerts buffered during outage"
```

---

## Incident Lifecycle

| State | Detail |
|---|---|
| **Creation** | First escalated alert for a host creates incident. `correlation_key = normalized_host`. All sources, all alert types for that host group here. |
| **Active** | `incidents.ended_at IS NULL`. Should stay 0–3 normally. 10+ = something bad happened. |
| **Auto-close** | Zabbix sends `status=OK` → close only if no other alerts landed on this incident in the last N minutes (guards against multi-problem hosts). Sets `ended_at = NOW()` + Telegram "✅ Resolved" ping. |
| **Manual close** | All other incidents (port scans, Graylog events, anything without a Zabbix OK signal). Close via API or direct query. |
| **Stale** | Non-Zabbix incidents older than 72h with no activity — flagged in startup-check.json for agent review. |

> **Roadmap:** Smarter auto-close for multi-problem hosts — track open Zabbix problem IDs per incident, only close when all are resolved.

---

## Telegram Notification Flow

```
Incident escalated →
  ┌─ from_buffer=true? ──────────────────→ skip, done
  │
  ├─ Is there an enabled target? ── no ──→ log, done
  │ yes
  └─ Rate limit check (last 15 min)
       ├─ < 4 messages sent ──→ send Telegram
       │   ├─ success → update escalation_recipients (sent)
       │   └─ failed  → retry 30s × 5, then mark failed
       └─ ≥ 4 messages ──→ declare MAJOR INCIDENT
           stop all escalation messages
           override quiet hours
           log to incident metadata
           (manual intervention required)
```

---

## Host Normalization

Applied at ingest before computing `correlation_key`:

```python
import re

def normalize_host(raw: str) -> str:
    host = raw.strip().lower()
    # Strip FQDN suffix — keep first label only
    host = host.split(".")[0]
    # Strip common suffixes (extend as needed)
    host = re.sub(r"[-_](prod|dev|test|01|02|03)$", lambda m: m.group(0), host)
    return host

# Examples:
# "PiHole-01.home.lan" → "pihole-01"
# "GRAYLOG.internal"   → "graylog"
```

> Audit Zabbix and Graylog host field names in real payloads before finalizing — they may differ (`host`, `hostname`, `device`).

---

## Dedup Key Generation

```python
import hashlib, json

def compute_dedup_key(source_name: str, payload: dict) -> str:
    if source_name == "zabbix":
        event_id = payload.get("eventid") or payload.get("event_id")
        if event_id:
            return f"zabbix:{event_id}"

    if source_name == "graylog":
        notif_id = payload.get("check_result", {}).get("triggered_at") \
                   or payload.get("alert_id")
        stream_id = payload.get("stream", {}).get("id", "unknown")
        if notif_id:
            return f"graylog:{stream_id}:{notif_id}"

    # Generic fallback: hash normalized payload
    # WARNING: audit source payloads first — injected timestamps break this
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode()).hexdigest()[:16]
    return f"{source_name}:{digest}"
```

> `dedup_key` must be a **UNIQUE constraint** on the `alerts` table, not just an index.

---

## Database Schema

### sources
Config for each webhook source.
```sql
source_id      SERIAL PK
name           TEXT UNIQUE         -- zabbix, graylog, generic
type           TEXT
enabled        BOOLEAN DEFAULT true
allowed_ips    INET[]              -- fallback if secret_hash is NULL
secret_hash    TEXT                -- HMAC secret (primary auth). NULL = IP-only
config         JSONB               -- webhook path, headers, source-specific
created_at     TIMESTAMPTZ DEFAULT NOW()
updated_at     TIMESTAMPTZ
```

### rules
Filter + routing logic. Priority ordered.
```sql
rule_id        SERIAL PK
name           TEXT
source_id      INT REFERENCES sources(source_id)  -- NULL = all sources
priority       INT DEFAULT 100
conditions     JSONB          -- e.g. {"host": "pi-hole-*", "severity": "critical"}
action         TEXT           -- escalate, suppress, defer, tag_only
metadata       JSONB          -- LLM config, prompt if needed
status         TEXT DEFAULT 'active'  -- active, pending (awaiting approval), disabled
enabled        BOOLEAN DEFAULT true
created_at     TIMESTAMPTZ DEFAULT NOW()
```

### alerts
All raw events. Never lost.
```sql
alert_id       SERIAL PK
received_at    TIMESTAMPTZ DEFAULT NOW()
source_id      INT REFERENCES sources(source_id)
raw_payload    JSONB NOT NULL
normalized     JSONB          -- host, severity, status, message
dedup_key      TEXT UNIQUE    -- UNIQUE constraint, not just index
from_buffer    BOOLEAN DEFAULT false  -- true if replayed from disk buffer
correlated_id  INT            -- FK to incidents.incident_id
escalated      BOOLEAN DEFAULT false
escalated_at   TIMESTAMPTZ
```

### incidents
One open incident per host.
```sql
incident_id      SERIAL PK
started_at       TIMESTAMPTZ DEFAULT NOW()
ended_at         TIMESTAMPTZ   -- null = open
summary          TEXT
correlation_key  TEXT          -- normalized host name only (e.g. "pihole-01")
alerts_count     INT DEFAULT 0
current_severity TEXT          -- denormalized: worst severity seen, updated on each ingest
host             TEXT
tags             TEXT[]
metadata         JSONB
major_incident   BOOLEAN DEFAULT false
major_reason     TEXT
last_escalated_at TIMESTAMPTZ  -- denormalized for quick "recently escalated?" check
```

### escalations
Tracks escalation events per incident.
```sql
escalation_id  SERIAL PK
incident_id    INT REFERENCES incidents(incident_id)
channel        TEXT           -- telegram
created_at     TIMESTAMPTZ DEFAULT NOW()
metadata       JSONB
```

### escalation_recipients
Junction: which escalation went to whom.
```sql
escalation_id  INT REFERENCES escalations(escalation_id)
target_id      INT REFERENCES notification_targets(target_id)
status         TEXT           -- sent, failed, rate_limited, major_incident
sent_at        TIMESTAMPTZ DEFAULT NOW()
retry_count    INT DEFAULT 0
```

### notification_targets
Who to escalate to. Configurable.
```sql
target_id      SERIAL PK
channel        TEXT           -- telegram, slack, etc.
target_ref     TEXT           -- chat/user/channel ID
name           TEXT           -- "<name>", "ops-watch"
enabled        BOOLEAN DEFAULT TRUE
quiet_hours    JSONB          -- {"start":"23:00","end":"07:00","tz":"Europe/Copenhagen"}
created_at     TIMESTAMPTZ DEFAULT NOW()
```

### rule_executions
Audit trail: which rule fired for which alert.
```sql
rule_execution_id  SERIAL PK
alert_id           INT REFERENCES alerts(alert_id) ON DELETE CASCADE
rule_id            INT REFERENCES rules(rule_id)
matched_conditions JSONB
action_taken       TEXT
executed_at        TIMESTAMPTZ DEFAULT NOW()
```

### gateway_state
Runtime state. Lightweight key-value.
```sql
state_key      TEXT PRIMARY KEY
state_value    JSONB
updated_at     TIMESTAMPTZ DEFAULT NOW()
```
Used for: LLM passive counter (`{"alerts_processed": 42}`), rate limit windows (`{"last_escalations": [ts, ts, ...]}`), buffer replay status.

### rule_suggestions
LLM-proposed rules awaiting human review. Populated after passive phase (50–100 alerts).
```sql
suggestion_id    SERIAL PK
source_id        INT REFERENCES sources(source_id)  -- NULL = all sources
pattern          JSONB          -- conditions that would match, e.g. {"host": "*-test", "severity": "info"}
suggested_action TEXT           -- escalate, suppress, defer, tag_only
confidence       FLOAT          -- 0–1, based on pattern frequency
rationale        TEXT           -- LLM explanation
status           TEXT DEFAULT 'pending'  -- pending, approved, rejected, applied
approved_by      TEXT
applied_rule_id  INT REFERENCES rules(rule_id)  -- set when status = applied
reviewed_at      TIMESTAMPTZ    -- when status changed from pending
created_at       TIMESTAMPTZ DEFAULT NOW()
updated_at       TIMESTAMPTZ DEFAULT NOW()
```

---

## Indexes

```sql
alerts(received_at)                       -- retention pruning
alerts(dedup_key)                         -- enforced as UNIQUE constraint
alerts(source_id, received_at)            -- per-source queries
alerts(from_buffer)                       -- buffer audit queries
incidents(correlation_key, ended_at)      -- active incident lookup
incidents(host, ended_at)                 -- host-scoped queries
escalation_recipients(escalation_id)      -- escalation tracking
rule_executions(alert_id)                 -- audit trail
rule_suggestions(status)                  -- pending review queue
```

---

## Health Endpoint

`GET /healthz` returns:
```json
{
  "status": "ok",
  "database": "connected",
  "buffer": {"pending_files": 0},
  "uptime_seconds": 3600
}
```

Exempt from token authentication. Used for Caddy/uptime monitoring.

---

## Caddy Configuration

Already configured on MB-CADDY (CADDY_IP):
```
alerts.example.com {
    log {
        output file /var/log/caddy/alerts.example.com.log {
            roll_size 100M
            roll_uncompressed
            roll_local_time
            roll_keep 3
            roll_keep_for 48h
        }
    }
    reverse_proxy GATEWAY_IP:8090
}
```

---

## LLM Role

> "Rules are the bouncer, the LLM is the concierge."

The LLM role is intentionally narrow. Rules and scripts handle 95% of filtering. LLM is a plugin, added after real alert data is flowing.

**What the LLM does:**

1. **Edge case decisions** — When an alert matches no rule or hits conflicting rules, LLM picks the action (escalate, suppress, defer, tag). Acts as catch-all.
2. **Rich summarization** — For large incidents (e.g. 50 port scan entries), LLM writes a human-readable summary. Instead of "50 events on host X", you get "host X was port-scanned from 192.0.2.1 targeting ports 22, 3389, 5900 over 3 minutes — likely automated scanner."
3. **Cross-source correlation** — After data flows from both Zabbix and Graylog, LLM can link them across incidents. Requires read access to DB or a context-injection layer — different interface than single-alert decisions. Design separately.
4. **Adaptive noise learning** — After passive phase (50–100 alerts), LLM starts making suppress/defer suggestions via `rule_suggestions` table. First iteration always requires human review before anything is suppressed.

**What the LLM does NOT do:**
- Initial filtering (rules handle that)
- Dedup or IP/HMAC validation (scripts)
- Telegram formatting or sending (hardcoded templates)
- Escalate/no-escalate on known hosts or known alert types (rules)
- Anything during a flood (rate limits stop escalation before LLM is called)

**Implementation note:** Skip for initial build. Add as step 14 once real alert patterns are known. Schema groundwork is already in place (`tag_only` rule action, `gateway_state` counter, `rule_suggestions` table, `status = 'pending'` on rules).

**LiteLLM:** Route LLM calls through the existing LiteLLM instance for fallback, cost tracking, and model swapping.

---

## noise-maker Skill

OpenClaw skill for agent interaction with the gateway. Verify `noise-maker` is available on ClawHub before publishing.

**Location:** `~/.openclaw/skills/noise-maker/`

**Structure:**
```
noise-maker/
  SKILL.md          -- skill manifest
  runbook.md        -- full reference (loaded on demand, not in context by default)
  scripts/
    active_incidents.sh   -- list open incidents, one line each
    gateway_health.sh     -- db/buffer status
    close_incident.sh     -- close by incident_id
    toggle_rule.sh        -- enable/disable rule by rule_id
  startup-check.json      -- written by gateway on boot, read by before_agent_start hook
```

**Startup check:** Gateway writes `startup-check.json` on boot:
```json
{
  "open_incidents": 2,
  "stale_incidents": ["pihole-01 (4d)"],
  "buffer_pending": 0,
  "generated_at": "2026-04-06T08:00:00Z"
}
```
`before_agent_start` hook injects a one-liner if anything non-zero. Zero context cost when clean.

**Script design:** Minimal output, no raw JSON. Same philosophy as UniFi/SysClaw skills — stripped, human-readable lines the agent can act on without burning context.

**Runbook covers:** adding sources, modifying rules, reviewing `rule_suggestions`, manual incident triage, schema reference, buffer replay verification.

---

## Implementation Plan

1. PostgreSQL: Create `sysclaw_alerts` DB, schema, `sysclaw` role
2. Gateway service: FastAPI app with ingest endpoints + `/healthz`
3. Target cache: load from DB at startup, persist to `/opt/alert-gateway/cache/targets.json`
4. Rule engine: priority-ordered matching against rules table
5. Host normalization: strip FQDN, lowercase, before correlation
6. Incident correlation: host-only `correlation_key`, open/close logic
7. Telegram escalation: direct API calls with retry (30s × 5) + rate limiting
8. Local disk buffer: `/opt/alert-gateway/buffer/`, sorted replay, `from_buffer` flag
9. DB-down notifications: Telegram warning on disconnect, summary on recovery
10. LLM filter groundwork: passive counter in `gateway_state`, `rule_suggestions` table, `tag_only` action — no active LLM calls yet
11. Systemd unit: `alert-gateway.service`
12. Caddy config: verify `alerts.example.com` → `GATEWAY_IP:8090`
13. Migrate Zabbix webhook from OpenClaw hooks → Alert Gateway
14. Add Graylog webhook support
15. `noise-maker` skill: scripts + runbook + startup-check hook + `.gitignore` (whitelist-only, excludes `startup-check.json` and `cache/`) + `startup-check.example.json` (documents format for ClawHub consumers)
16. Test with real data (95% target), iterate based on behavior
17. Dashboards / queries for alert patterns
18. LLM filter plugin (after real alert patterns established)

**Roadmap (post-stable):**
- Smarter auto-close for multi-problem hosts (track Zabbix problem IDs per incident)
- Agent-initiated incident resolution (currently reactive only — agent acts when asked)
- Proactive agent monitoring once system proven stable and non-spammy

---

## Build Philosophy

**Build to 95%, test with real data.** Some edge cases (exact correlation logic, LLM filter behavior, rate limit thresholds) are best validated with actual alert patterns rather than speculating upfront. After initial implementation, feed Zabbix alerts through and observe. Iterate.

---

## Implementation State

| Step | Status | Notes |
|---|---|---|
| Design / planning | ✅ Done | Design complete |
| Convoy evaluated | ✅ Skipped | Overkill for 2 sources, no event summarization |
| PostgreSQL DB | Not started | Needs `sysclaw_alerts` DB on MB-PGDB |
| Gateway code | Not started | Awaiting implementation start |
| Zabbix integration | Not started | Existing hook fixed, migration pending |
| Graylog integration | Not started | Verify webhook notification support |
| LLM filter groundwork | Not started | Schema ready, no active LLM calls in initial build |
| Local disk buffer | Not started | `/opt/alert-gateway/buffer/` |
| noise-maker skill | Not started | Verify ClawHub name availability |
| Caddy config | ✅ Verified | `alerts.example.com` → `GATEWAY_IP:8090` confirmed |
| 95% test iteration | Pending | After initial build |

---

## Notes

- OpenClaw native hooks remain for lightweight integrations — not everything needs the full gateway
- Gateway is self-contained: sends Telegram directly, survives OpenClaw downtime
- Active incidents = `ended_at IS NULL` — should stay small (0–3 normal, 10+ = problem)
- Major incident detection: ≥4 escalations in 15 min → stop alerts, manual triage required
- Major incident always overrides quiet hours
- 500MB retention soft cap — review at limit, no auto-delete
- Local disk buffer provides resilience for DB outages; buffered alerts skip escalation
- Stale incident threshold: 72h for non-Zabbix incidents
- LLM calls routed through LiteLLM when implemented
