<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Risk Scoring

## Stage: 6 of 12
## Phase: 🔵 STRATEGY
## Execution: ALWAYS

---

## Purpose

Score every test requirement with Status = Missing (or Required, if no brownfield) using the four-factor risk model. Produce a **Debt Scorecard** — a prioritized list of missing tests ranked by architectural risk. This scorecard tells the team exactly what to test first for maximum risk reduction.

This stage completes the Strategy phase. After risk scoring, the engine transitions to Observation (or ends, if Architecture Only mode).

---

## Depth Adaptation

| Depth | Scoring Detail | Scorecard Output |
|-------|---------------|-----------------|
| **Minimal** | Score each missing test on 4 factors. Assign bucket (Critical/High/Medium/Low). No per-factor rationale. Produce ranked list with top 10 items. | Buckets + counts + top 10 list |
| **Standard** | Full scoring with brief rationale for any factor scored ≥4. Produce full ranked scorecard with remediation priority per sprint. Group by component for team assignment. | Full ranked list + sprint allocation + component grouping |
| **Comprehensive** | Full scoring with detailed rationale for each factor. Effort estimates per test. Sprint mapping (which sprint should address which debt). Remediation suggestions (what kind of test to write). Historical trend tracking setup. | Full detail + effort estimates + sprint plan + remediation guidance |

---

## MANDATORY: Stage Sub-Role — Risk Analyst

During THIS stage, ALSO adopt the mindset of a **Risk Analyst**. This does NOT replace your primary role (Senior QA Engineer / Test Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Score objectively based on architecture, not on ease of testing — a hard-to-test critical component is HIGHER priority, not lower
- Consider blast radius carefully: a failing auth system affects ALL users; a failing admin report affects one team
- Avoid uniform scoring — if everything is "Medium," you haven't differentiated. Spread the scores.
- Think in terms of production impact: "If this commitment breaks and there's no test to catch it, what happens?"

### Anti-Patterns for This Stage
- Do NOT score all missing tests identically — differentiation is the entire point
- Do NOT score based on how easy the test is to write — score based on RISK of not having it
- Do NOT skip scoring for "simple" components — simple code still has architectural risk if it's in the critical path
- Do NOT produce a scorecard without buckets — raw numbers are meaningless without thresholds

### Quality Check
A good output at this stage sounds like:
- "31 missing tests scored. Distribution: 3 Critical (auth bypass, payment integrity, data consistency), 8 High (API contracts for core endpoints), 14 Medium (business logic edge cases), 6 Low (config validation, non-critical UI flows). Sprint 1 recommendation: address all 3 Critical + top 4 High = 7 tests."

---

## Step-by-Step Execution

### Step 1: Identify Scoring Targets

From the test register, select all entries to score:

| Condition | Include in Scoring? |
|-----------|:-------------------:|
| Status = Missing | ✅ Yes — primary scoring target |
| Status = Required (no brownfield run) | ✅ Yes — treat as missing |
| Status = Exists | ❌ No — already covered |
| Status = Failing | ✅ Yes — failing test = same risk as no test |
| Status = Deprecated | ❌ No — no longer required |
| Status = Overridden | ❌ No — user accepted the gap |

**Count:** "Scoring {N} entries out of {Total} register entries."

---

### Step 2: Score Each Entry on Four Factors

For each scoring target, assess four factors (1-5 each):

#### Factor 1: Architectural Risk

"If this commitment breaks and there's no test, how severe is the impact?"

| Score | Definition | Examples |
|:-----:|-----------|---------|
| 1 | Cosmetic or non-functional impact; easily noticed and fixed manually | Formatting issue, non-critical log message |
| 2 | Minor functional impact; workaround exists; affects few users | Admin-only feature bug, secondary display issue |
| 3 | Moderate functional impact; no workaround for affected users; limited scope | Feature regression for a subset of users; degraded (not broken) workflow |
| 4 | Major functional impact; core feature broken for significant user segment | Login fails for OAuth users; payment processes but doesn't confirm |
| 5 | Catastrophic; data loss, security breach, complete service failure, or regulatory violation | Auth bypass, data corruption, PII leak, total outage |

#### Factor 2: Blast Radius

"How many things break if this component fails?"

| Score | Definition | Examples |
|:-----:|-----------|---------|
| 1 | Isolated single component; failure contained; no dependents | Standalone utility, admin reporting module |
| 2 | Affects 2-3 components or one secondary workflow | Helper service used by a few features |
| 3 | Affects one major subsystem or multiple workflows | Payment service affecting checkout + refund + subscription |
| 4 | Cross-system impact; multiple teams' work affected | Shared auth library, event bus, API gateway |
| 5 | Platform-wide; affects ALL users and ALL services | Database layer, core authentication, message broker |

#### Factor 3: Logic Complexity

"How likely is a bug to exist here, based on inherent complexity?"

| Score | Definition | Examples |
|:-----:|-----------|---------|
| 1 | Trivial CRUD; no conditional logic; simple pass-through | Basic getter/setter, static config reader |
| 2 | Simple conditionals; 2-3 branches; straightforward mapping | Single validation rule, simple authorization check |
| 3 | Moderate complexity; multiple conditions; some state management | Multi-step workflow, business rule with 5+ conditions |
| 4 | Complex algorithms; state machines; concurrent operations | Pricing engine, scheduling algorithm, retry logic with backoff |
| 5 | Highly complex; distributed state; race conditions; mathematical | Event sourcing reconciliation, consensus algorithms, financial calculations |

#### Factor 4: Change Frequency

"How often does this code change? More changes = more regression risk."

| Score | Definition | Examples |
|:-----:|-----------|---------|
| 1 | Stable; last modified months ago; no planned changes | Infrastructure code, mature utility libraries |
| 2 | Rarely changes; 1-2 modifications per quarter | Configuration schemas, established API contracts |
| 3 | Moderate; changes every sprint; ongoing feature work | Active feature modules, evolving business rules |
| 4 | Frequently changes; multiple modifications per sprint | Hot feature areas, rapidly iterating UI, experimental code |
| 5 | Volatile; changes daily or multiple times per sprint; under active redesign | Code being refactored, new module under heavy development |

---

### Step 3: Calculate Composite Scores

**Formula:** Composite = Architectural Risk × Blast Radius × Logic Complexity × Change Frequency

**Range:** 1 (minimum: all factors = 1) to 625 (maximum: all factors = 5)

**Bucket assignment:**

| Composite Score | Bucket | Meaning | Action |
|:--------------:|:------:|---------|--------|
| 400-625 | 🔴 **Critical** | Severe production risk if untested | Test immediately — do not ship without |
| 150-399 | 🟠 **High** | Significant exposure; likely to cause real issues | Test within current sprint |
| 50-149 | 🟡 **Medium** | Manageable risk; unlikely to be catastrophic | Test within next 2 sprints |
| 1-49 | 🟢 **Low** | Minimal exposure; low-probability, low-impact gap | Test when convenient; accept risk if needed |

---

### Step 4: Rank and Prioritize

Sort all scored entries by composite score (descending):

```markdown
## Debt Scorecard — Ranked

| Rank | ID | Test Name | Arch Risk | Blast | Complexity | Change | Score | Bucket |
|:----:|:--:|-----------|:---------:|:-----:|:----------:|:------:|:-----:|:------:|
| 1 | {id} | {name} | {n} | {n} | {n} | {n} | {score} | 🔴 |
| 2 | {id} | {name} | {n} | {n} | {n} | {n} | {score} | 🔴 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |
```

---

### Step 5: Produce Sprint Recommendations (Standard+ Depth)

Map scorecard items to sprint capacity:

```markdown
## Sprint Remediation Recommendations

### Sprint 1 (Immediate)
Address all 🔴 Critical items + top High items:
| ID | Test Name | Score | Estimated Effort |
|:--:|-----------|:-----:|:----------------:|
| {id} | {name} | {score} | {S/M/L} |

### Sprint 2
Address remaining 🟠 High items:
| ID | Test Name | Score | Estimated Effort |
|:--:|-----------|:-----:|:----------------:|
| {id} | {name} | {score} | {S/M/L} |

### Sprints 3-4
Address 🟡 Medium items (prioritize by score within bucket):
(list top items)

### Backlog
🟢 Low items — address opportunistically:
(count + note they're accepted risk until addressed)
```

**Effort estimation (Comprehensive depth):**
- **S (Small):** 1-2 hours — single unit test, straightforward assertion
- **M (Medium):** 2-8 hours — integration test requiring mocking, multi-step setup
- **L (Large):** 1-2 days — system test requiring environment, test data, multi-component coordination

---

### Step 6: Group by Component (Standard+ Depth)

For team assignment:

```markdown
## Debt by Component

| Component | Critical | High | Medium | Low | Total | Top Priority |
|-----------|:--------:|:----:|:------:|:---:|:-----:|-------------|
| UserService | 1 | 3 | 2 | 1 | 7 | SEC-001: Auth bypass test |
| PaymentService | 2 | 1 | 0 | 0 | 3 | DATA-003: Transaction integrity |
| OrderService | 0 | 2 | 4 | 2 | 8 | BL-007: Order state machine |
```

---

### Step 7: Compile Debt Scorecard

```markdown
# Debt Scorecard

**Type:** Debt Scorecard
**Generated:** {ISO timestamp}
**Engine:** AI-TGE v1.0.0
**Mode:** {mode}
**Depth:** {depth level}

## Summary

| Bucket | Count | % of Total | Action |
|--------|:-----:|:----------:|--------|
| 🔴 Critical | {n} | {n}% | Test immediately |
| 🟠 High | {n} | {n}% | Test this sprint |
| 🟡 Medium | {n} | {n}% | Test within 2 sprints |
| 🟢 Low | {n} | {n}% | Test when convenient |
| **Total scored** | **{N}** | **100%** | — |

## Risk Exposure
- **Highest single risk:** {test name} (Score: {n}) — {brief why}
- **Most at-risk component:** {component} ({n} critical + high gaps)
- **Most common gap type:** {level/type} ({n} instances)

{Full ranked table from Step 4}
{Sprint recommendations from Step 5}
{Component grouping from Step 6}
```

---

### Step 8: Save All Strategy Phase Outputs

Save finalized artifacts to `.governance/test/`:
1. `tge-state.md` — update: Phase = Strategy Complete, Last Stage = 6
2. `test-register.md` — update: Risk Score column populated for all Missing entries
3. `test-strategy.md` — already saved in Stage 5
4. `debt-scorecard.md` — new file from this stage

---

### Step 9: Present Summary and Transition

```markdown
## Strategy Phase Complete ✅

All strategy artifacts have been produced:
- **Test Register:** {N} test requirements ({n} Architecture, {n} Baseline, {n} Story)
- **Test Strategy:** {pyramid}, {tools}, {coverage targets}
- **Debt Scorecard:** {N} missing tests — 🔴 {n} | 🟠 {n} | 🟡 {n} | 🟢 {n}

**Immediate priority (Critical):**
1. {test name} — Score {n}: {brief why}
2. {test name} — Score {n}: {brief why}
3. {test name} — Score {n}: {brief why}

**Saved to:** `.governance/test/` (test-register.md, test-strategy.md, debt-scorecard.md, tge-state.md)

---

**Next steps:**
{IF mode = Full Chain or Observation Only}
→ Observation Phase begins. AI-TGE will monitor AI-DLC v1 progress and update the register as tests are written.

{IF mode = Architecture Only}
→ Strategy complete. Use the debt scorecard to prioritize test writing. Re-invoke AI-TGE when AI-DLC v1 begins for observation tracking.

{IF mode = Brownfield}
→ Strategy complete. Use the debt scorecard to address gaps. Re-invoke AI-TGE periodically for coverage reassessment.

⚠️ **IMPORTANT: If continuing to AI-DLC v1 or re-invoking AI-TGE later, start in a NEW session.**
   Each AI-* package loads a full workflow into context;
   a fresh session keeps it fast and focused.
```

---

## Output Artifacts

| Artifact | Location | Purpose |
|----------|----------|---------|
| Debt Scorecard | `.governance/test/debt-scorecard.md` | Prioritized missing tests by risk |
| Updated Test Register | `.governance/test/test-register.md` | Risk Score column populated |
| Updated state file | `.governance/test/tge-state.md` | Strategy phase complete |

---

## Stage Completion Criteria

| Check | Pass Criteria |
|-------|---------------|
| All missing tests scored | Every Status = Missing entry has 4-factor score |
| Composite calculated correctly | Product (not sum) of 4 factors |
| Buckets assigned | Every score mapped to Critical/High/Medium/Low |
| Differentiation exists | Not all items in the same bucket — spread across at least 3 |
| Top priorities clear | User can identify the #1 test to write next |
| Sprint recommendations provided | (Standard+ depth) Actionable allocation per sprint |
| State file updated | Phase = Strategy Complete; Stage 6 = complete |
| Scorecard saved | `.governance/test/debt-scorecard.md` exists with full ranked list |
