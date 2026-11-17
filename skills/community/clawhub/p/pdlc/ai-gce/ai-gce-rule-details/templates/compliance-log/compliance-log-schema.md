<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-GCE
generatedVersion: "{version}"
source: "{upstream-steering-file}"
generatedOn: "{generation-date}"
ownership: generated
---
# Compliance Log Schema

## Purpose

Defines the JSONL event schema for the compliance logging infrastructure. This file is generated into the target workspace at `.governance/compliance-log/compliance-log-schema.md`.

---

## Log Structure

> **Project ID resolution:** Every log event includes `projectId` — the immutable family-wide correlation key. AI-GCE reads it from `rules/workspace-rules.md` → `## Project Identity` section (placed there by AI-DWG). This enables portfolio-level queries across multiple projects when AI-PPM aggregates compliance data via AI-FLO.

```
{project-root}/compliance-log/
├── events/
│   └── {YYYY-MM-DD}.jsonl          ← One file per day, append-only
├── exceptions/
│   └── active-exceptions.jsonl     ← Formal rule bypasses
├── remediations/
│   └── open-remediations.jsonl     ← Violation fix tracking
└── snapshots/
    └── {YYYY-MM-DD}-audit.json     ← Full audit state per run
```

---

## Event Types

### CHECK (Written by hooks after every fire)

```json
{
  "timestamp": "{ISO-8601-UTC}",
  "type": "check",
  "id": "chk-{YYYYMMDD}-{HHmmss}-{seq}",
  "projectId": "{project-id from rules/workspace-rules.md → Project Identity section}",
  "hook": "{hook-filename-without-extension}",
  "trigger": "{event-type: fileEdited|fileCreated|preToolUse|postTaskExecution|promptSubmit|agentStop|userTriggered}",
  "ruleId": "{RULE-ID checked}",
  "ruleSeverity": "{critical|high|medium|low}",
  "result": "{pass|fail|warn}",
  "message": "{one-line finding}",
  "sessionDedup": false
}
```

**Deduplication (Tier A hooks only):**
When `sessionDedup: true`, only the LAST event per `hook` + `file path` within a session window is retained.

### EXCEPTION (Written when a rule bypass is formally approved)

```json
{
  "timestamp": "{ISO-8601-UTC}",
  "type": "exception",
  "id": "exc-{YYYYMMDD}-{HHmmss}-{seq}",
  "projectId": "{project-id}",
  "ruleId": "{RULE-ID being bypassed}",
  "ruleSeverity": "{critical|high|medium}",
  "status": "active",
  "justification": "{why this rule is being bypassed — specific, not vague}",
  "requestedBy": "{person requesting}",
  "approvedBy": "{person approving — MUST differ from requestedBy for Critical}",
  "approvedAt": "{ISO-8601-UTC}",
  "expiresAt": "{ISO-8601-UTC — max 30d Critical, 90d High, 180d Medium}",
  "linkedTicket": "{ticket tracking resolution work}",
  "scope": "{what's covered — module, file pattern, or project-wide}"
}
```

### REMEDIATION (Written when a violation is being tracked to resolution)

```json
{
  "timestamp": "{ISO-8601-UTC}",
  "type": "remediation",
  "id": "rem-{YYYYMMDD}-{HHmmss}-{seq}",
  "projectId": "{project-id}",
  "ruleId": "{RULE-ID violated}",
  "ruleSeverity": "{critical|high|medium}",
  "status": "{open|in-progress|resolved}",
  "violationDate": "{ISO-8601-UTC — when first detected}",
  "assignedTo": "{person responsible for fix}",
  "sla": "{24h for Critical, 14d for High, 28d for Medium}",
  "resolvedAt": "{ISO-8601-UTC — when fixed, null if open}",
  "notes": "{resolution details}"
}
```

### AUDIT (Written by audit agent after each scan)

```json
{
  "timestamp": "{ISO-8601-UTC}",
  "type": "audit",
  "id": "aud-{YYYYMMDD}-{HHmmss}-{seq}",
  "projectId": "{project-id}",
  "phase": "{current_phase}",
  "tier": {current_tier},
  "score": {0-100},
  "rating": "{compliant|needs-attention|at-risk|non-compliant}",
  "totalRules": {count},
  "passing": {count},
  "failing": {count},
  "criticalFailures": {count},
  "highFailures": {count},
  "activeExceptions": {count},
  "openRemediations": {count},
  "triggeredBy": "{user|tier-activation|phase-transition}"
}
```

### REDERIVATION (Written by AI-GCE after Mode 2 completes)

```json
{
  "timestamp": "{ISO-8601-UTC}",
  "type": "rederivation",
  "id": "rdr-{YYYYMMDD}-{HHmmss}-{seq}",
  "projectId": "{project-id}",
  "trigger": "{list of changed steering files}",
  "rulesUpdated": {count},
  "hooksUpdated": {count},
  "newArtifacts": {count},
  "removedArtifacts": {count},
  "reason": "{brief description of what changed and why}"
}
```

---

## Key Rules

1. **Append-only:** Log files MUST NEVER be edited or deleted (GOV-LOG-002)
2. **Git-committed:** compliance-log/ MUST NOT be in.gitignore (GOV-LOG-009)
3. **IDs are unique:** Format ensures no collisions (date + time + sequence)
4. **Severity SLAs:** Critical = 24h remediation, High = 14d, Medium = 28d
5. **Exception expiry:** Critical = max 30 days, High = max 90 days, Medium = max 180 days
6. **Critical exception approval:** requestedBy ≠ approvedBy (GOV-LOG-004)
