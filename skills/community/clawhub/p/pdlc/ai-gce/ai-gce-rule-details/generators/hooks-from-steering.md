<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Hooks From Steering — Derivation Logic

## Purpose

This file defines HOW to derive hook JSON files from steering content. It covers: which steering files produce which hooks, how to populate file patterns, debounce tier assignment, noise classification, compliance logging injection, and phase-awareness injection.

---

## MANDATORY: Stage Sub-Role — Automation Engineer

During THIS activity, ALSO adopt the mindset of an **Automation Engineer**. This does NOT replace your primary role (Compliance Officer + Platform Engineer + AI-DLC v1 Engineer) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in event-driven automation: each hook is a trigger → condition → action pipeline that must fire at exactly the right moment
- Apply the debounce decision tree rigorously: security-critical = fileEdited (Tier A), advisory = agentStop (Tier B)
- Derive file patterns from tech-stack + module-structure + actual filesystem — generic globs are engineering failures
- Ensure every hook prompt follows the 4-part structure: phase check → rule checks → DX principle → compliance logging
- Classify noise honestly: 🔴 Essential (auditor cares), 🟠 High-value (drift if removed), 🟡 Advisory (team convenience)

### Anti-Patterns for This Activity
- Do NOT use generic `**/*.ts` patterns — always derive module-specific, layer-specific paths
- Do NOT skip the compliance logging block on any hook (it's the audit trail, non-negotiable)
- Do NOT assign Tier A to advisory hooks (it creates noise fatigue that undermines genuine security alerts)

### Quality Check
A good output from this activity sounds like:
- "security-gate-check.json: event=fileEdited, debounce=Tier A, noise=🔴 Essential. Pattern: `src/modules/*/presentation/**/*.controller.ts`. Prompt cites SEC-001/003/010, includes phase-check, DX silence rule, and compliance logging suffix."
- "ENFORCEMENT-GUIDE.md organizes 13 core hooks + 5 tier-gated + 6 conditional by activation tier. Removal guidance: session-discipline first (highest noise, lowest impact), NEVER remove security-gate-check."

---

## Hook Derivation Pipeline

```
For EACH hook to generate:
1. IDENTIFY source steering file(s) → what rules this hook enforces
2. DETERMINE event type → when should this hook fire?
3. DERIVE file patterns → from tech-stack.md + module-structure.md + folder scan
4. ASSIGN debounce tier → Tier A (fileEdited) or Tier B (agentStop) or Other
5. APPLY PATTERN SCOPING (Layer 1 — Package Territory Segregation):
   • Read .governance/PACKAGE_TERRITORIES.md for excluded zones
   • Ensure derived file patterns do NOT structurally match any excluded zone
   • If hook needs broad coverage (e.g., secrets) → keep broad pattern BUT rely on Layer 2
   • Prefer: {module-root}/**/*.{ext} over **/*.{ext}
   • NEVER use a bare **/*.{ext} that would match .kiro/, .governance/, compliance-log/,
     project-initiation/, architecture/, docs/, management_framework/, or templates/
6. PREPEND PACKAGE TERRITORY PREAMBLE (Layer 2 — Runtime Filter):
   • Load common/hook-preamble.md
   • For hooks with file context (fileEdited, fileCreated, agentStop): prepend preamble
   • For non-file hooks (promptSubmit, preToolUse, postTaskExecution, userTriggered): skip
   • Preamble goes BEFORE the phase check — absolute first evaluation
7. ASSIGN noise classification → 🔴 Essential / 🟠 High-value / 🟡 Advisory
8. WRITE prompt → cite rule IDs, include phase-check, include DX principle
9. APPEND compliance logging block → non-negotiable suffix
10. VALIDATE → patterns exist on filesystem, rule IDs exist in generated rules,
    patterns do NOT structurally match excluded zones (unless justified by Layer 2)
```

---

## Hook Inventory (What Gets Generated)

### Always-Generated Hooks (13 core)

| Hook File | Event Type | Debounce | Noise | Source Steering | Rules Enforced |
|-----------|:----------:|:--------:|:-----:|----------------|----------------|
| `session-discipline.json` | promptSubmit | — | 🟡 | session-governance.md | GOV-SESSION-002/007/008/009 |
| `pre-code-spec-check.json` | preToolUse (write) | — | 🟠 | session-governance.md + project-governance.md | GOV-SESSION-001/003, PG-INCEP-001 |
| `post-task-governance.json` | postTaskExecution | — | 🟠 | project-governance.md + DEFINITION_OF_DONE.md | PG-*, GOV-SESSION-005, ARCH-01 |
| `api-contract-check.json` | fileCreated | — | 🟠 | api-standards.md | GOV-API-001 |
| `security-gate-check.json` | fileEdited | Tier A | 🔴 | security-rules.md | SEC-001/003/010 |
| `sensitive-data-check.json` | fileEdited | Tier A | 🔴 | observability-sensitive.md | SEC-006 (secrets), LOG-* (PII) |
| `migration-safety.json` | fileEdited | Tier A | 🔴 | database-rules.md | DATA-012/013/014 |
| `naming-check.json` | agentStop | Tier B | 🟡 | naming-conventions.md | NC-* |
| `module-boundary-check.json` | agentStop | Tier B | 🟠 | module-structure.md | MOD-001/002 |
| `domain-layer-purity.json` | agentStop | Tier B | 🟠 | domain-context.md + module-structure.md | DOM-005, GOV-DDD-005 |
| `coverage-check.json` | agentStop | Tier B | 🟠 | testing-strategy.md | GOV-CICD-002/003 |
| `pre-pr-checklist.json` | userTriggered | — | 🟠 | git-workflow.md + testing-strategy.md | GOV-PR-*, GOV-CICD-* |
| `periodic-audit.json` | userTriggered | — | 🟠 | ALL rules | Full scan |

### Tier-Gated Hooks (installed at Tier 2+)

| Hook File | Event Type | Debounce | Noise | Tier | Source Steering |
|-----------|:----------:|:--------:|:-----:|:----:|----------------|
| `segregation-check.json` | postTaskExecution | — | 🟠 | 2 | role-isolation.md + CODEOWNERS |
| `steering-quality-check.json` | agentStop | Tier B | 🟡 | 2 | (self-derived — GOV-STEER rules) |
| `documentation-reminder.json` | agentStop | Tier B | 🟡 | 2 | project-governance.md |
| `change-readiness-gate.json` | preTaskExecution | — | 🟠 | 3 | project-governance.md (CM-*) |
| `exception-expiry-check.json` | userTriggered | — | 🟠 | 3 | compliance-log-governance |

### Conditional Hooks (only if steering file exists)

| Hook File | Condition | Event Type | Debounce | Source |
|-----------|-----------|:----------:|:--------:|--------|
| `tenant-isolation-check.json` | multi-tenancy.md exists | fileEdited | Tier A 🔴 | multi-tenancy.md |
| `resilience-gate.json` | resilience-standards.md exists | agentStop | Tier B | resilience-standards.md |
| `tracing-check.json` | observability-tracing.md exists | agentStop | Tier B | observability-tracing.md |
| `event-sourcing-check.json` | event-sourcing.md exists | agentStop | Tier B | event-sourcing.md |
| `frontend-a11y-check.json` | frontend-standards.md exists | agentStop | Tier B | frontend-standards.md |
| `mcp-audit-log.json` | .kiro/settings/mcp.json configured | postToolUse (`^mcp_.*`) | — | MCP governance |

---

## File Pattern Derivation

### The Rule

Hook `patterns` fields MUST use technology-specific, module-specific paths. NEVER use generic globs like `**/*.ts`.

### Pattern Assembly Formula

```
Pattern = {module-path-prefix}/{layer-pattern}/{technology-file-pattern}

Where:
  module-path-prefix = from module-structure.md (e.g., "src/modules/*" or "src/Modules/*")
  layer-pattern = from module-structure.md layer rules (e.g., "presentation" or "Presentation")
  technology-file-pattern = from tech-stack.md (see mapping table below)
```

### Technology → File Pattern Mapping

| tech-stack.md Says | Controllers | Services | Entities | Migrations | Tests |
|-------------------|-------------|----------|----------|------------|-------|
| NestJS / TypeScript | `*.controller.ts` | `*.service.ts` | `*.entity.ts` | `src/migrations/*.ts` | `*.spec.ts` |
| Django / Python | `views.py`, `viewsets.py` | `services.py` | `models.py` | `*/migrations/*.py` | `test_*.py` |
| ASP.NET Core / C# | `*Controller.cs` | `*Service.cs` | `*.Entity.cs` | `Migrations/*.cs` | `*Tests.cs` |
| Spring Boot / Java | `*Controller.java` | `*Service.java` | `*Entity.java` | `db/migration/*.sql` | `*Test.java` |
| Go | `*_handler.go` | `*_service.go` | `*_model.go` | `migrations/*.sql` | `*_test.go` |

### Pattern Examples (Assembled)

For a NestJS project with module-structure.md showing `src/modules/{module}/`:

| Hook | Pattern |
|------|---------|
| api-contract-check | `src/modules/*/presentation/**/*.controller.ts` |
| domain-layer-purity | `src/modules/*/domain/**/*.ts` |
| migration-safety | `src/migrations/**/*.ts` |
| naming-check | `src/modules/**/*.ts` |
| security-gate-check | `src/modules/*/presentation/**/*.controller.ts` |
| tenant-isolation-check | `src/modules/*/domain/entities/**/*.ts` |

For an ASP.NET project with module-structure.md showing `src/Modules/{Module}/`:

| Hook | Pattern |
|------|---------|
| api-contract-check | `src/Modules/*/Presentation/**/*Controller.cs` |
| domain-layer-purity | `src/Modules/*/Domain/**/*.cs` |
| migration-safety | `**/Migrations/**/*.cs` |
| security-gate-check | `src/Modules/*/Presentation/**/*Controller.cs` |
| tenant-isolation-check | `src/Modules/*/Domain/Entities/**/*.cs` |

---

## Pattern Scoping — Package Territory Segregation (Layer 1)

### The Mandatory Rule

Hook `patterns` MUST be scoped to application code paths. They MUST NOT structurally match package infrastructure directories. This is Layer 1 of the three-layer segregation strategy.

### Pattern Scoping Decision Tree

```
Is this hook's pattern a bare wildcard (e.g., **/*.ts, **/*.json)?
├── YES → Can it be scoped to a module/src root?
│         ├── YES → Scope it (e.g., src/**/*.ts, src/modules/**/*.ts)
│         └── NO  → Does this hook GENUINELY need workspace-wide coverage?
│                   ├── YES (e.g., secrets in any file) → Keep broad, rely on Layer 2 preamble
│                   └── NO  → Scope it to at least one directory level
└── NO  → Already scoped (e.g., src/modules/*/presentation/**/*.controller.ts)
          → Verify it doesn't accidentally include excluded zones → PASS
```

### Scoping Examples by Hook

| Hook | ❌ NEVER Use | ✅ Use Instead | Why |
|------|-------------|---------------|-----|
| sensitive-data-check | `**/*.cs, **/*.ts, **/*.json` | `src/**/*.{ext}, *.env, appsettings*.json` | Excludes .kiro/, .governance/, compliance-log/ structurally |
| security-gate-check | `**/*Controller.cs` | `src/modules/*/presentation/**/*Controller.cs` | Already scoped — OK |
| naming-check | (agentStop — no pattern) | N/A | Preamble filters infra files from scan |
| domain-layer-purity | (agentStop — no pattern) | N/A | Preamble filters infra files from scan |

### Exception: Secrets Detection

The `sensitive-data-check` hook legitimately needs to scan root config files (`.env`, `appsettings.json`, etc.) because secrets can appear there. For this hook:
- Keep application-scoped patterns PLUS specific root config patterns
- Use Layer 2 preamble to filter `.kiro/**` and `.governance/**` at runtime
- Pattern template: `src/**/*.{ext}, *.env, appsettings*.json, {config-roots}`

### Technology-Specific Safe Patterns

| Stack | Application Code Pattern | What's Excluded Structurally |
|-------|-------------------------|------------------------------|
| NestJS | `src/**/*.ts`, `src/**/*.json` | `.kiro/`, `.governance/`, `compliance-log/`, root `*.json` |
| Django | `{app}/**/*.py`, `{app}/**/migrations/*.py` | `.kiro/`, `.governance/`, `compliance-log/`, `docs/` |
| .NET | `src/**/*.cs`, `src/**/*.json` | `.kiro/`, `.governance/`, `compliance-log/` |
| Spring Boot | `src/**/*.java`, `src/main/resources/**` | `.kiro/`, `.governance/`, `compliance-log/` |
| Generic | `src/**/*` | Everything outside `src/` |

---

## Debounce Strategy Assignment

### Decision Tree

```
Is this hook checking for something that is DANGEROUS even in intermediate state?
├── YES → Does a single frame of violation pose security/data risk?
│         ├── YES → Tier A: fileEdited (fire every save, sessionDedup in log)
│         └── NO  → agentStop is sufficient
└── NO  → Does this hook care about FINAL state only?
          ├── YES → Tier B: agentStop (fire once at session end)
          └── NO  → Use appropriate non-file event type (postTask, promptSubmit, userTriggered)
```

### Tier A Criteria (fileEdited — immediate fire)

ALL of these conditions must be true:
- Violation creates security risk, data leakage, or financial error
- Waiting until session end means the damage already happened
- False positives on intermediate state are acceptable (security > noise)

### Tier B Criteria (agentStop — final state only)

ANY of these conditions make a hook Tier B:
- The check is about code STRUCTURE (using statements, imports, references)
- The check cares about COMPLETENESS (all tests, all docs, all coverage)
- Intermediate states regularly produce false positives (e.g., adding import before writing code)

### Session Deduplication (Tier A only)

For Tier A hooks, add to the compliance logging section:

```
"sessionDedup": true
```

This tells the compliance log to keep only the LAST event per hook + file path within a session. Earlier check results for the same file are overwritten — only the final state matters for audit.

---

## Prompt Construction Template

Every hook prompt follows this structure:

```
{PHASE CHECK}
{RULE CHECKS — numbered, specific}
{DX PRINCIPLE — silent if passing}
{COMPLIANCE LOGGING BLOCK}
```

### Phase Check (First Line)

```
Check .compliance-state.json → currentPhase. Only enforce rules applicable to {applicable phases}.
If this is a {earlier phase} project, skip silently.
```

### Rule Checks (Core)

```
Check the following rules against the current context:
1. {RULE-ID}: {what to check} — {how to verify}
2. {RULE-ID}: {what to check} — {how to verify}
...

If any rule is violated, warn with:
- Rule ID
- What was expected
- What was found
- Remediation suggestion
```

### DX Principle (Before Logging)

```
If all rules pass, confirm compliance silently. Do NOT produce output when nothing is wrong.
```

### Compliance Logging Block (Mandatory Suffix)

```
## Compliance Logging
After completing all checks above, append a JSON event to
`compliance-log/events/{today-date}.jsonl` (create the file if it doesn't exist).
Format:
{"timestamp": "{ISO-8601-UTC}", "type": "check", "id": "chk-{date}-{time}-{seq}",
 "hook": "{hook-name}", "trigger": "{event-type}", "ruleId": "{primary-rule-checked}",
 "ruleSeverity": "{severity}", "result": "{pass|fail|warn}",
 "message": "{one-line-finding}"}
Log ONE event per rule checked. If multiple rules are checked, log multiple events.
```

For Tier A hooks, add after the format block:
```
If a previous log entry exists for the same hook + file path within this session,
OVERWRITE it (keep only the latest result). Add "sessionDedup": true to the event.
```

---

## Noise Classification Guide

| Classification | Criteria | Hook Removal Impact |
|:-:|-----------|---------------------|
| 🔴 Essential | Security risk, data integrity, compliance evidence | Removing = audit trail gap, security hole, or data leak risk |
| 🟠 High-value | Architecture enforcement, governance checks, methodology discipline | Removing = drift accumulates silently; caught only at periodic audit |
| 🟡 Advisory | Quality suggestions, documentation reminders, style checks | Removing = minor quality decline; team can self-manage |

**Rule for classification:**
- Would an external auditor care if this hook was removed? → 🔴 Essential
- Would architecture/governance drift if this hook was removed? → 🟠 High-value
- Is this primarily about team convenience/quality? → 🟡 Advisory

---

## ENFORCEMENT-GUIDE Generation

When generating `.governance/hooks/ENFORCEMENT-GUIDE.md`, organize hooks by tier:

```markdown
# Hook Enforcement Guide

## Tier 1 — Active from Day 0

| Hook | Type | Noise | What It Does |
|------|------|:-----:|-------------|
| session-discipline | promptSubmit | 🟡 | Enforces spec-before-code, never-vibe-code |
| pre-code-spec-check | preToolUse | 🟠 | Warns if no spec/contract before implementation |
| api-contract-check | fileCreated | 🟠 | Warns if controller created without OpenAPI contract |
| periodic-audit | userTriggered | 🟠 | On-demand full compliance scan |
| security-gate-check | fileEdited | 🔴 | Auth verification on endpoint files |
| migration-safety | fileEdited | 🔴 | Rollback method required; no destructive ops |

## Tier 2 — Activate at Sprint 2+ (when readiness met)

| Hook | Type | Noise | What It Does |
|------|------|:-----:|-------------|
| post-task-governance | postTask | 🟠 | DDD + governance check after task completion |
| segregation-check | postTask | 🟠 | Author ≠ reviewer reminder |
| module-boundary-check | agentStop | 🟠 | Cross-module import detection |
| coverage-check | agentStop | 🟠 | Test coverage threshold enforcement |
| domain-layer-purity | agentStop | 🟠 | No infrastructure deps in domain |
| naming-check | agentStop | 🟡 | File/class naming convention check |
| steering-quality-check | agentStop | 🟡 | Steering file quality validation |
| sensitive-data-check | fileEdited | 🔴 | PII/secrets in code detection |
| documentation-reminder | agentStop | 🟡 | Docs update needed after feature |

## Tier 3 — Activate Pre-Release (when readiness met)

| Hook | Type | Noise | What It Does |
|------|------|:-----:|-------------|
| change-readiness-gate | preTask | 🟠 | CM artifacts must exist before Integration tasks |
| exception-expiry-check | userTriggered | 🟠 | Flags expired rule bypasses |
| pre-pr-checklist | userTriggered | 🟠 | Full PR readiness verification |

## Conditional — Only if applicable

| Hook | Condition | Type | What It Does |
|------|-----------|------|-------------|
| tenant-isolation-check | multi-tenancy.md | fileEdited 🔴 | Tenant entity inheritance check |
| resilience-gate | resilience-standards.md | agentStop | Resilience pattern verification |
| tracing-check | observability-tracing.md | agentStop | Span instrumentation check |
| event-sourcing-check | event-sourcing.md | agentStop | Event store pattern compliance |
| frontend-a11y-check | frontend-standards.md | agentStop | Accessibility verification |
| mcp-audit-log | mcp.json configured | postToolUse | MCP tool invocation logging |

## If Hooks Are Too Noisy

Remove in this order (least impact first):
1. session-discipline (fires on every prompt — highest noise)
2. documentation-reminder (advisory only)
3. steering-quality-check (advisory only)
4. naming-check (advisory only)

NEVER remove: security-gate-check, migration-safety, sensitive-data-check, tenant-isolation-check
```
