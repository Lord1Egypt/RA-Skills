<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-GCE
generatedVersion: "{version}"
source: "ai-gce-rules/core-generator.md"
generatedOn: "{generation-date}"
ownership: generated
---
# Session-End Compliance Agent — Template

## Purpose

A consolidated session-end sweep that runs ALL advisory compliance checks in a single pass after a development session. Replaces individual `agentStop` hooks (module-boundary, domain-layer-purity, coverage, naming, steering-quality, documentation-reminder) with one agent that produces one report.

**Why an agent (not just a hook prompt):** The user can disable the hook and invoke this agent manually via `SEC__` whenever they choose — same checks, same report, user-controlled timing.

---

## Trigger

- **Shortcut:** `SEC__` (typed anywhere in a prompt — manual invocation)
- **Hook-triggered:** `session-end-compliance.json` fires this agent on `agentStop` (automatic)
- **Either path produces identical output.**

---

## Anatomy (per AGENT_GOVERNANCE_CONTRACT.md §4)

### When to Invoke
- Automatically after every agent session (via hook) — default
- Manually via `SEC__` when the hook is disabled or user wants an on-demand check
- Before a PR / before switching packages / before ending a work block

### Consequences of Skipping
- Module boundary violations accumulate unnoticed (cross-module imports creep in)
- Domain layer contamination goes undetected until a major refactor is needed
- Test coverage gaps grow silently
- Naming drift makes the codebase inconsistent

### Recovery
- Run `SEC__` at any time to get the current state
- Violations found retroactively are logged the same way — no data loss
- Fix violations then re-run to confirm

---

## Behavior (6 Checks)

### Pre-Check: Package Territory Exclusion (MANDATORY — evaluate FIRST)

Before performing any checks, verify each file's path in your scan.

**EXCLUDED ZONES (skip silently):**
- `.governance/hooks/` — hook infrastructure
- `rules/` — steering infrastructure
- `.governance/agents/` — agent infrastructure
- `.governance/` — governance rules/agents/logs
- `compliance-log/` — audit trail
- `project-initiation/` — AI-PILC output (provenance only)
- `architecture/` — AI-ADLC output (provenance only)
- `management_framework/` — shared governance spine
- `docs/compliance-*` — generated dashboards
- `templates/` — planning templates

For each file in your scan: if its path starts with ANY of the above prefixes, SKIP it silently. Only check files outside excluded zones.

### Pre-Check: Phase & Tier Awareness

Read `.compliance-state.json` → `currentPhase` and `currentTier`.
- Checks 1-4: apply from Tier 2+, Construction phase onward
- Checks 5-6: apply from Tier 3 only (Pre-Release)
- Skip checks that don't apply to the current tier/phase

---

### Check 1: Module Boundary (Tier 2+, Construction+)

For each file modified during this session that is within module source paths:

1. **Cross-module imports:** Does any file import/reference classes from another module directly? Cross-module communication MUST use events or APIs — not direct class references. (Rule: MOD-02/MOD-03)
2. **Layer direction:** Verify dependencies flow inward only (presentation → application → domain, infrastructure → domain). No outward dependencies.
3. **Shared kernel only:** If cross-module code is needed, it MUST come from the shared kernel — not from another module's internals.

---

### Check 2: Domain Layer Purity (Tier 2+, Construction+)

For each modified file in domain layer paths:

1. **No infrastructure dependencies:** Domain MUST NOT import DB clients, HTTP clients, framework-specific types, or ORM entities.
2. **Domain depends only on itself + shared kernel.**
3. If violation found: identify the specific dependency and suggest the inversion pattern. (Rule: DOM-005, severity: critical)

---

### Check 3: Test Coverage (Tier 2+, Construction+)

Check test coverage meets thresholds from `testing-strategy.md`:

1. **Unit test exists** for each modified business-logic file?
2. **Coverage metric** meets minimum threshold (if measurable from workspace config)?
3. If missing: warn with the specific file and expected test location. (Rule: GOV-CICD-002, severity: high)

---

### Check 4: Naming Conventions (Tier 1+, any phase)

For each modified file:

1. **File naming** matches conventions in `naming-conventions.md` (or `workspace-rules.md` naming section).
2. **Class/method naming** matches conventions (PascalCase/camelCase per tech stack).
3. **Consistent casing** per the declared tech stack standard. (Rule: NC-01, severity: medium)

---

### Check 5: Steering Quality (Tier 3 ONLY, Pre-Release)

If any `rules/*.md` files were modified during this session:

1. Still prescriptive (MUST/NEVER language)?
2. Provenance comment intact (`<!-- AI-DWG generated | source: ... -->`)?
3. No contradictions with `workspace-rules.md` golden rules?
4. Advisory only — warn, never block.

---

### Check 6: Documentation Reminder (Tier 3 ONLY, Pre-Release)

If public API endpoints or major business logic changed:

1. Were corresponding docs updated (README, API docs, inline docs)?
2. Advisory only — remind, never block.

---

## Output Format

### If ALL checks pass (silent-when-compliant):

```
✅ Session-end compliance: all checks pass.
```

One line. No noise. Done.

### If findings exist:

```
━━━━ Session-End Compliance Sweep (SEC__) ━━━━
Phase: {phase} | Tier: {tier} | Files scanned: {n}

✅ Module boundaries: PASS ({n} files)
✅ Domain purity: PASS ({n} files)
⚠️ Coverage: WARN — src/orders/PlaceOrder.cs missing unit test
✅ Naming: PASS ({n} files)

Summary: {pass} pass, {warn} warn, {fail} fail
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Compliance Logging

After completing all checks, append ONE summary event to `compliance-log/events/{today-date}.jsonl`:

```json
{
  "timestamp": "{ISO-8601-UTC}",
  "type": "sweep",
  "id": "swp-{date}-{time}",
  "agent": "session-end-compliance",
  "trigger": "{agentStop | manual}",
  "checksRun": {n},
  "pass": {n},
  "warn": {n},
  "fail": {n},
  "findings": [
    {"ruleId": "{id}", "severity": "{level}", "result": "{pass|fail|warn}", "message": "{finding}"}
  ]
}
```

---

## Related

| Agent | Relationship |
|-------|-------------|
| `compliance-audit-agent` (CAA__) | Full audit (all rules, all files). SEC__ is a lightweight session-scoped subset. |
| `pre-pr-checklist-agent` (PRC__) | Pre-PR gate. Overlaps with SEC__ checks but adds PR-specific items. |
| `dod-gate-agent` (DOD__) | Definition of Done validation. Checks different criteria (DoD items, not code rules). |

---

## Installation

1. Copy `session-end-compliance-agent.md` to `.governance/agents/` (Kiro) or equivalent
2. Add shortcut to workspace rules:

```markdown
**`SEC__` shortcut triggers Session-End Compliance.** When the user types `SEC__` (uppercase, with double underscore) anywhere in a prompt, immediately execute the Session-End Compliance protocol defined in this agent. Scan files modified during the session against all applicable Tier B compliance rules and produce a consolidated report. No further clarification needed.
```

3. Install `session-end-compliance.json` hook for automatic firing on `agentStop`
4. Users can disable the hook and rely on manual `SEC__` invocation if preferred

---

*Agent template for AI-GCE v1.0.0 | Shortcut: SEC__ | Replaces: 4-6 individual agentStop hooks*
