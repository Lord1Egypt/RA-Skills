<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Validation Rules

## Purpose

This document defines the cross-check rules applied AFTER generation (Step 4 of Full Generation) and AFTER reconciliation (before signaling downstream). Every generated workspace must pass these validations before being presented to the user.

---

## Validation Categories

```
┌──────────────────────────────────────────────────────────────────┐
│  VALIDATION PIPELINE                                              │
├──────────────────────────────────────────────────────────────────┤
│                                                                    │
│  V1: COMPLETENESS    — Is everything generated that should be?     │
│  V2: TRACEABILITY    — Can every rule be traced to an AP source?   │
│  V3: CONSISTENCY     — Do files agree with each other?             │
│  V4: CONDITIONAL     — Are conditional files correctly included/   │
│                        excluded?                                    │
│  V5: STRUCTURE       — Does folder layout match C4 L3?             │
│  V6: PRESCRIPTIVE    — Are rules actionable, not just descriptive? │
│  V7: NO INVENTION    — Nothing generated that AP doesn't justify?  │
│                                                                    │
└──────────────────────────────────────────────────────────────────┘
```

---

## V1: Completeness Validation

**Question:** "Is everything generated that should be?"

### Always-Generated Files (19 steering + operational + config)

Every workspace MUST contain these. Missing = validation failure.

| Category | Files | Check |
|----------|-------|-------|
| Steering (core) | 19 always-generated steering files | Each file exists in `rules/` |
| Operational docs | PROJECT_INSTRUCTIONS.md, DEFINITION_OF_DONE.md, CONTRIBUTING.md, TEAM_AGREEMENTS.md, ONBOARDING.md | Each file exists at workspace root |
| Config files | .gitignore, .editorconfig, docker-compose.yml, CODEOWNERS, README.md | Each file exists at workspace root |
| PR template | .github/pull_request_template.md | File exists |
| Planning templates | templates/session-planning.md, sprint-planning.md, estimation-guide.md | Each file exists in templates/ |
| Folder structure | At least one module folder in src structure | Folders exist matching C4 L3 modules |

### Completeness Check Format

```
V1: COMPLETENESS CHECK
  Steering files:  {n}/19 always-generated ✅|❌
  Conditional:     {n} generated (of {m} applicable) ✅|❌
  Operational:     {n}/5 ✅|❌
  Config:          {n}/5 ✅|❌
  Planning:        {n}/3 ✅|❌
  PR template:     ✅|❌
  Folder structure: {n} modules created ✅|❌
```

---

## V2: Traceability Validation

**Question:** "Can every rule in the steering files be traced to a specific AP artifact?"

### Rules

1. Every rule statement in a steering file MUST correspond to at least one of:
   - An explicit principle from Architecture Vision (P1, P2, etc.)
   - A constraint from the Constraints table
   - A technology decision from Technology Stack or an ADR
   - A design pattern from Component Design, API Architecture, etc.
   - A quality attribute requirement

2. Provenance markers MUST be present:
   ```markdown
   <!-- AI-DWG generated | source: {AP artifact name} | date: {date} -->
   ```

3. No "orphan rules" — if a rule cannot be traced to an AP source, it must be removed or flagged.

### Traceability Check

For each steering file, verify:

| Check | Pass Criteria |
|-------|--------------|
| Has provenance header | `<!-- AI-DWG generated | source: ... -->` present |
| Rules trace to AP | Every MUST/MUST NOT/NEVER/ALWAYS statement has an AP source |
| ADR references valid | Any ADR-NNN reference corresponds to an actual ADR |
| Technology names match | Technology names in steering match Technology Stack exactly |

### Exceptions (Rules Without Direct AP Source)

Some rules are DERIVED (not directly stated in AP but logically implied). These are acceptable IF:
- They follow directly from a stated principle or constraint
- They are industry best practice for the selected technology
- They are marked as derived: `<!-- derived from: {principle/constraint} -->`

---

## V3: Consistency Validation

**Question:** "Do all generated files agree with each other?"

### Cross-File Consistency Checks

| Check | Files Involved | What to Verify |
|-------|---------------|----------------|
| Technology names | `tech-stack.md` vs. all other steering files | Same technology referred to by same name everywhere |
| Module names | `module-structure.md` vs. `CODEOWNERS` vs. folder structure | Module list is identical across all three |
| API conventions | `api-standards.md` vs. `error-handling.md` | Error format in api-standards matches error-handling rules |
| Database references | `database-rules.md` vs. `tech-stack.md` | Database technology name matches |
| Security model | `security-rules.md` vs. `api-standards.md` | Auth approach consistent between security and API |
| Tenant isolation | `multi-tenancy.md` vs. `database-rules.md` vs. `security-rules.md` | Isolation approach consistent across all three |
| Naming conventions | `naming-conventions.md` vs. `module-structure.md` vs. `api-standards.md` | No conflicting naming rules |
| Git workflow | `git-workflow.md` vs. `info/CONTRIBUTING.md` | Branching strategy matches in both |
| DoD criteria | `DEFINITION_OF_DONE.md` vs. `testing-strategy.md` | Test requirements in DoD align with testing strategy |
| Observability | `observability-logging.md` vs. `observability-sensitive.md` | Sensitive data rules don't contradict logging requirements |

### Consistency Check Format

```
V3: CONSISTENCY CHECK
  Technology naming:     ✅|❌ {details if failure}
  Module naming:         ✅|❌
  API conventions:       ✅|❌
  Security model:        ✅|❌
  Tenant isolation:      ✅|❌ (or N/A)
  Naming conventions:    ✅|❌
  Git workflow:          ✅|❌
  DoD alignment:         ✅|❌
  Observability:         ✅|❌
```

---

## V4: Conditional Generation Validation

**Question:** "Are conditional files correctly included/excluded based on AP content?"

### Validation Matrix

For each conditional file, verify the trigger was correctly evaluated:

| Conditional File | Trigger Condition | Verification Method |
|-----------------|-------------------|-------------------|
| `multi-tenancy.md` | Multi-Tenancy Architecture doc exists in AP | Check AP file inventory |
| `api-versioning.md` | API Architecture specifies multi-version strategy | Search API doc for version strategy section |
| `resilience-standards.md` | >3 integrations OR distributed OR Microservices/Resilience extension | Count integrations in Integration doc; check extensions |
| `observability-tracing.md` | Tracing tool in Infrastructure OR Microservices extension | Search Infrastructure doc for Jaeger/Zipkin/OTEL; check extensions |
| `performance-standards.md` | Latency targets (p95/p99) in Quality Attributes | Search Architecture Vision for quantified SLOs |
| `workflow-engine.md` | Workflow/state-machine in Component Design | Search C4 L3 for workflow component |
| `frontend-standards.md` | UI containers in C4 L2 OR BFF extension | Search Container diagram for SPA/UI; check extensions |
| `event-sourcing.md` | Event Sourcing/CQRS extension active | Check adlc-state.md extensions |
| `feature-flags.md` | Feature Flags extension active | Check adlc-state.md extensions |

### Rules

1. **Never generate a conditional file without valid trigger** — bloat prevention
2. **Never skip a conditional file when trigger IS met** — completeness
3. **Extension overrides are documented** — if extension forced generation, note it in the output summary
4. **Log skipped conditionals with reason** — transparency

### Conditional Check Format

```
V4: CONDITIONAL GENERATION CHECK
  Generated (with justification):
    ✅ multi-tenancy.md — AP contains Multi-Tenancy Architecture doc
    ✅ resilience-standards.md — Microservices extension active (override)
    
  Skipped (with reason):
    ⏭️ workflow-engine.md — No workflow component in C4 L3
    ⏭️ performance-standards.md — No quantified SLOs in AP
    
  Validation: All triggers correctly evaluated ✅|❌
```

---

## V5: Structure Validation

**Question:** "Does the generated folder structure match the C4 L3 component design?"

### Checks

| Check | Pass Criteria |
|-------|--------------|
| Every C4 L3 module has a folder | Module list from Component Design = folder list in src structure |
| Folder naming matches module naming | Names in `module-structure.md` match actual folder names |
| Shared kernel (if exists) has its own folder | If C4 L3 defines shared components, they have a dedicated folder |
| No extra folders beyond C4 L3 | No invented modules that aren't in the architecture |
| Layer structure within modules (if defined) | If C4 L3 specifies internal layers, they're reflected |
| CODEOWNERS maps to real folders | Every path in CODEOWNERS corresponds to an actual folder |

### Structure Check Format

```
V5: STRUCTURE CHECK
  Modules in C4 L3:     {n}
  Folders created:       {n}
  Match:                 ✅|❌ {mismatches if any}
  CODEOWNERS valid:      ✅|❌
  Extra folders:         {none | list}
```

---

## V6: Prescriptive Quality Validation

**Question:** "Are the steering rules actionable and enforceable, not just descriptive?"

### The Prescriptive Test

Every steering file must pass this quality bar:

| Criterion | Pass | Fail |
|-----------|------|------|
| Contains MUST/MUST NOT statements | "All queries MUST include tenant_id" | "Queries should include tenant_id" |
| Contains NEVER/ALWAYS constraints | "NEVER expose internal IDs in API responses" | "It's best not to expose internal IDs" |
| Contains specific patterns to follow | "Use Result<T, Error> for all service returns" | "Consider using a result pattern" |
| Contains specific anti-patterns to avoid | "Do NOT use try/catch for control flow" | "Try to avoid using exceptions for control flow" |
| Can be verified by AI-GCE (yes/no check) | Rule is binary — either followed or not | Rule is subjective — "good enough" ambiguity |

### Language Rules for Steering Files

| Use | Don't Use |
|-----|-----------|
| MUST | should |
| MUST NOT | should not |
| NEVER | avoid |
| ALWAYS | try to |
| DO | consider |
| DO NOT | it's recommended |
| Required | preferred |
| Forbidden | discouraged |

### Prescriptive Check

For each steering file, scan for weak language:

```
V6: PRESCRIPTIVE CHECK
  Files scanned:     {n}
  Weak language found:
    ❌ {file}: line {n} — "should" → replace with "MUST"
    ❌ {file}: line {n} — "consider" → replace with specific instruction
  
  All files prescriptive: ✅|❌
```

---

## V7: No-Invention Validation

**Question:** "Is everything generated justified by the AP? Nothing invented?"

### Rules

1. **No technology not stated in AP** — if AP says "PostgreSQL", don't add Redis unless AP explicitly includes it
2. **No patterns not decided in AP** — if AP doesn't mention CQRS, don't include CQRS rules
3. **No modules not in C4 L3** — folder structure = exactly what architecture defines
4. **No principles not in Architecture Vision** — workspace-rules reflect AP principles only
5. **No constraints not in AP** — DON'T rules come from AP constraints, not personal opinion

### Acceptable Derivations (Not "Invention")

| Acceptable | Why |
|-----------|-----|
| Deriving `.gitignore` patterns from technology stack | Industry standard for chosen technology |
| Deriving naming conventions from technology best practices | Technology-specific conventions are well-established |
| Including security best practices (OWASP) for the chosen stack | Universal security hygiene |
| Standard docker-compose structure for chosen technology | Infrastructure best practice |

### No-Invention Check

```
V7: NO-INVENTION CHECK
  Technologies in steering match AP:  ✅|❌
  Patterns in steering match AP:      ✅|❌
  Modules in structure match C4 L3:   ✅|❌
  Principles match AP Vision:         ✅|❌
  No unauthorized additions:          ✅|❌
```

---

## Full Validation Report Template

After running all checks, present consolidated report:

```
═══════════════════════════════════════════════════════════════
  AI-DWG VALIDATION REPORT
  Workspace: {name}
  Generated: {date}
═══════════════════════════════════════════════════════════════

V1: COMPLETENESS        {PASS|FAIL}  — {n}/{total} files generated
V2: TRACEABILITY        {PASS|FAIL}  — {n} rules, all traced
V3: CONSISTENCY         {PASS|FAIL}  — {n} cross-checks, {n} passed
V4: CONDITIONAL         {PASS|FAIL}  — {n} generated, {n} skipped (all justified)
V5: STRUCTURE           {PASS|FAIL}  — {n} modules match C4 L3
V6: PRESCRIPTIVE        {PASS|FAIL}  — No weak language found
V7: NO-INVENTION        {PASS|FAIL}  — All content AP-justified

───────────────────────────────────────────────────────────────
OVERALL:                {PASS|FAIL}

{If FAIL: list specific failures with remediation actions}
═══════════════════════════════════════════════════════════════
```

---

## When to Run Validation

| Scenario | Validation Scope |
|----------|-----------------|
| After Full Generation (Mode 1) | ALL checks (V1–V7) |
| After Delta Reconciliation (Mode 2) | V2, V3, V4, V7 on affected files only |
| After user requests "validate workspace" | ALL checks (V1–V7) |
| Before signaling AI-GCE | V1 + V3 minimum (ensure AI-GCE receives consistent input) |

---

## Validation Failures — Response

| Failure Type | Severity | Response |
|-------------|----------|----------|
| Missing required file (V1) | BLOCKING | Generate the missing file before completing |
| Untraceable rule (V2) | WARNING | Flag to user; remove or justify |
| Cross-file inconsistency (V3) | BLOCKING | Resolve before presenting to user |
| Wrong conditional (V4) | BLOCKING | Add missing file or remove unjustified file |
| Structure mismatch (V5) | BLOCKING | Align folders with C4 L3 |
| Weak language (V6) | WARNING | Rewrite to prescriptive form |
| Invented content (V7) | BLOCKING | Remove content or trace to AP source |

**BLOCKING** = must fix before output. **WARNING** = flag but can proceed.
