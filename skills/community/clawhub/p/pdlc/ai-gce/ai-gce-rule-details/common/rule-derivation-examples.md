<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Rule Derivation Pattern — Worked Examples

## Purpose

This file shows, end to end, how a steering-file decision becomes a concrete, technology-specific rule and hook. It is illustrative reference material — read it when you need a model for the steering → rule → hook derivation that Mode 1 (Full Generation) and Mode 2 (Re-Derivation) perform. The per-category derivation logic lives in `generators/*` (e.g. `api-compliance-generator.md`, `role-isolation-generator.md`).

---

## Example: API Contract Enforcement (NestJS workspace)

**Input from `api-standards.md`:**
```markdown
| Aspect | Approach |
|--------|----------|
| Spec format | OpenAPI 3.1 |
| Generation | Auto-generated from NestJS decorators |
| Location | /api/docs |
```

**Input from `module-structure.md`:**
```markdown
| Module | Path |
|--------|------|
| Incident | src/modules/incident/ |
| Change | src/modules/change/ |
| Asset | src/modules/asset/ |
```

**AI-GCE derives:**

Rule file (`.governance/rules/api-first-compliance.md`):
```markdown
### API-01: Contract Before Implementation
Severity: 🟠 High
Derived From: rules/api-standards.md → "OpenAPI 3.1 spec"
Rule: Every API endpoint MUST have an OpenAPI contract defined BEFORE
      controller implementation is written.
Verification:
- [ ] For each *.controller.ts in src/modules/*/presentation/ →
      a corresponding OpenAPI spec entry exists
File Patterns: src/modules/*/presentation/**/*.controller.ts
Anti-Pattern: Creating controller files before the API contract is reviewed
```

Hook file (`.governance/hooks/api-contract-check.json`):
```json
{
  "name": "API Contract Check",
  "version": "1.0.0",
  "when": {
    "type": "fileCreated",
    "patterns": ["src/modules/*/presentation/**/*.controller.ts"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "A controller file was created. Verify an OpenAPI contract exists for this endpoint per rule API-01 in .governance/rules/api-first-compliance.md. If the corresponding spec does not define this endpoint, warn the developer to create the API contract first before implementing the controller."
  }
}
```

**If the workspace were Django instead of NestJS:** The same derivation logic reads `tech-stack.md` ("Django"), reads `api-standards.md` (same OpenAPI 3.1 spec), and generates:
- File pattern: `**/views.py` or `**/viewsets.py`
- Different file glob — same rule concept and compliance intent

**This is why AI-GCE has zero manual configuration.** The workspace tells it everything.

## Example: Role Segregation Enforcement (Non-Architectural)

**Input from `role-isolation.md`:**
```markdown
## Segregation of Duties
| Decision Type | Approved By |
|--------------|-------------|
| Code changes | Peer + CODEOWNER |
| Security-sensitive changes | Security role |
| Steering file changes | Architect / Tech Lead |
```

**Input from `CODEOWNERS`:**
```
src/Modules/Finance/**    @finance-reviewer
src/Modules/Procurement/**  @procurement-reviewer
```

**AI-GCE derives (from built-in baseline + steering enrichment):**

Rule file (`.governance/rules/role-isolation.md`):
```markdown
### GOV-ROLE-004: Session Owner ≠ Reviewer
Severity: 🔴 Critical
Tier: 2
Derived From: rules/role-isolation.md → "Segregation of Duties" + Built-in Baseline
Rule: The person who wrote code (Session Owner) MUST NOT be the person who
      reviews/approves the PR. CODEOWNERS assigns a different reviewer per module.
Verification:
- [ ] PR author is never the PR approver
- [ ] CODEOWNERS file maps each module to a reviewer ≠ session owner
Anti-Pattern: Same person authoring and approving a PR
```

Hook file (`.governance/hooks/segregation-check.json`):
```json
{
  "name": "Segregation of Duties Reminder",
  "version": "1.0.0",
  "when": { "type": "postTaskExecution" },
  "then": {
    "type": "askAgent",
    "prompt": "A task was completed. Verify segregation of duties: the person who wrote this code MUST NOT be the reviewer. Check CODEOWNERS for the affected module to confirm a different person is assigned as reviewer. If all rules pass, confirm compliance silently.\n\n## Compliance Logging\nAppend to compliance-log/events/{today}.jsonl:\n{\"timestamp\":\"{ISO-8601}\",\"type\":\"check\",\"hook\":\"segregation-check\",\"trigger\":\"postTaskExecution\",\"ruleId\":\"GOV-ROLE-004\",\"ruleSeverity\":\"critical\",\"result\":\"{pass|warn}\",\"message\":\"{finding}\"}"
  }
}
```

**This example shows:** Even without technology-specific file patterns, governance rules are concrete and enforceable. The "built-in baseline" rule (author ≠ approver) is ENRICHED by steering (specific CODEOWNERS mapping) to become project-specific.
