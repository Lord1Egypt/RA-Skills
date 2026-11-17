# How Compliance Logging Works

**Purpose:** Explains how AI-GCE maintains an append-only audit trail of all governance events — violations detected, resolutions applied, tier changes, and audit results — providing continuous evidence for internal review and external certification.

---

## What Compliance Logging Is

Compliance logging is the append-only record of every governance event in the project's lifecycle. Every violation detected, every resolution, every audit, every tier change, every rule activation or deactivation is logged with timestamp, actor, and context.

```
.governance/compliance-log/
├── 2026-06/                    ← Monthly partitions
│   ├── 2026-06-01.jsonl        ← Daily log files (JSON Lines format)
│   ├── 2026-06-02.jsonl
│   └── ...
├── audits/                     ← Audit report snapshots
│   ├── 2026-06-01_standard.md
│   └── 2026-06-15_quarterly.md
└── .schema.json                ← Log entry schema definition
```

**Key property:** Append-only. Log entries are NEVER modified or deleted. This guarantees audit trail integrity for certification.

---

## Log Entry Schema

Every event produces a structured log entry:

```json
{
  "timestamp": "2026-06-12T14:30:00Z",
  "eventType": "violation-detected",
  "rule": "SEC-01",
  "ruleName": "No secrets in source code",
  "tier": 1,
  "severity": "critical",
  "file": "src/config/database.ts",
  "line": 42,
  "details": "Hardcoded database password detected",
  "actor": "developer@team.com",
  "hook": "security-gate-check.json",
  "resolution": null,
  "resolvedBy": null,
  "resolvedAt": null
}
```

When resolved:
```json
{
  "timestamp": "2026-06-12T14:45:00Z",
  "eventType": "violation-resolved",
  "rule": "SEC-01",
  "file": "src/config/database.ts",
  "details": "Moved to environment variable",
  "actor": "developer@team.com",
  "resolution": "fixed",
  "resolvedBy": "developer@team.com",
  "resolvedAt": "2026-06-12T14:45:00Z",
  "relatedEntry": "2026-06-12T14:30:00Z"
}
```

---

## Event Types

| Event Type | When Logged | Data Captured |
|-----------|-------------|---------------|
| `violation-detected` | Hook or audit finds a rule violation | Rule, file, line, severity, details |
| `violation-resolved` | A detected violation is fixed | Resolution method, who fixed it, duration |
| `violation-overridden` | Team explicitly exempts a violation | Override rationale, approver, expiry date |
| `audit-completed` | A compliance audit finishes | Score, findings count, drift findings |
| `tier-activated` | Team graduates to a new tier | New tier, readiness signals met |
| `tier-rollback` | Team returns to a lower tier | Rationale, what wasn't working |
| `rule-activated` | A new rule becomes active | Rule ID, source steering file, tier |
| `rule-disabled` | A rule is turned off | Rule ID, rationale, disabled-by |
| `rule-rederived` | Re-derivation updates a rule | Old hash, new hash, what changed |
| `baseline-recorded` | Initial brownfield baseline captured | Violation counts per category |
| `grace-period-start` | New tier enters advisory mode | Tier, duration, rules affected |
| `grace-period-end` | Advisory mode ends, enforcement begins | Tier, rules now blocking |

---

## Log Partitioning

Logs are partitioned for manageability:

| Partition | Strategy | Rationale |
|-----------|----------|-----------|
| **Monthly folders** | `2026-06/`, `2026-07/` | Manageable size, easy to archive |
| **Daily files** | `2026-06-12.jsonl` | Small files, fast appending |
| **JSON Lines format** | One JSON object per line | Streamable, greppable, tool-friendly |

**Retention:** Logs are never deleted during active project lifetime. For archival:
- Active period: all logs retained
- Post-project: compressed and archived
- Certification evidence: retained per certification requirements (typically 3-7 years)

---

## How Logging Integrates with Other Components

### Hooks → Log

When a hook fires and detects a violation:
```
Hook fires → Violation found → Log entry written → Developer notified
```

### Audits → Log

When a compliance audit runs:
```
Audit starts → Each finding → Log entry per finding → Audit summary entry → Report generated
```

### Tier Changes → Log

When governance tier changes:
```
Readiness confirmed → Team approves → Log: tier-activated → Grace period → Log: grace-period-start → Enforcement → Log: grace-period-end
```

### Re-Derivation → Log

When rules are re-derived:
```
Steering changed → Re-derivation runs → For each changed rule → Log: rule-rederived
```

---

## Certification Evidence Generation

For SOC 2, ISO 27001, or similar audits, the compliance log provides:

| Certification Requirement | Evidence From Log |
|--------------------------|-------------------|
| Access controls are enforced | `violation-detected` entries for GOV-01 (author≠approver) with zero unresolved |
| Continuous monitoring | Daily log entries showing hooks are firing consistently |
| Timely corrective action | `violation-resolved` entries showing resolution within SLA |
| Change management | `rule-activated`, `tier-activated` entries showing governed changes |
| Audit trail integrity | Append-only logs with no gaps in daily files |
| Controls are tested | `audit-completed` entries showing regular assessment |

**Evidence extraction query examples:**
- "Show all security violations and their resolution times in Q2"
- "Show all tier changes with approval evidence"
- "Show audit scores over last 6 months (compliance trend)"
- "Show all overrides with rationale and expiry"

---

## The Override Pattern

When a team legitimately exempts a violation:

```json
{
  "timestamp": "2026-06-12T16:00:00Z",
  "eventType": "violation-overridden",
  "rule": "ARCH-03",
  "file": "src/legacy/adapter.ts",
  "details": "Cross-boundary import required for legacy adapter — refactoring planned Q3",
  "rationale": "Technical debt: legacy adapter must access old module until migration complete",
  "approvedBy": "tech-lead@team.com",
  "expiresAt": "2026-09-30",
  "ticketRef": "JIRA-1234"
}
```

**Override rules:**
- Must have rationale (why this exception is justified)
- Must have approver (who authorized the exemption)
- Should have expiry (when the override is reconsidered)
- Should have ticket reference (tracking the underlying fix)

Overrides are NOT violations — they're documented, approved exceptions. They don't count against compliance score but ARE visible in audit reports.

---

## Score Calculation and Logging

The compliance score is calculated and logged at each audit:

```
Score = (total_checked - new_violations) / total_checked × 100
        (weighted by severity: Critical 3x, High 2x, Medium 1x)

Excluded from calculation:
- Baseline violations (pre-governance)
- Overridden violations (documented exceptions)
- Deprecated rules (no longer applicable)
- Dormant rules (higher tier than current)
```

---

## Related Documents

| Document | Location |
|----------|----------|
| How GCE Compliance Audit Works | `knowledge_docs/HOW_GCE_COMPLIANCE_AUDIT_WORKS.md` |
| How GCE Derivation Pipeline Works | `knowledge_docs/HOW_GCE_DERIVATION_PIPELINE_WORKS.md` |
| How Provenance Tracking Works | `knowledge_docs/HOW_PROVENANCE_TRACKING_WORKS.md` |
| How to Run a Compliance Audit | `knowledge_docs/HOW_TO_RUN_A_COMPLIANCE_AUDIT.md` |
| Why Governance Automation Matters | `knowledge_docs/WHY_GOVERNANCE_AUTOMATION_MATTERS.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
