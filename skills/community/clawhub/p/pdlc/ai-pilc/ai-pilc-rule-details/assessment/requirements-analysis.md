<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Requirements Analysis

## Stage: 4 of 16
## Phase: 🟠 ASSESSMENT
## Execution: ALWAYS (Adaptive Depth)

---

## Purpose

Systematically analyze the structured requirements (from Stage 3) to identify gaps, ambiguities, inconsistencies, missing dependencies, and feasibility concerns. This stage produces an analysis report that either confirms the requirements are ready for feasibility assessment, or triggers a Clarification Cycle (Stage 5).

---

## MANDATORY: Stage Sub-Role — Business Analyst

During THIS stage, ALSO adopt the mindset of a **Business Analyst**. This does NOT replace your primary role (PMO Professional / Senior Project Manager) — it ADDS a thinking dimension.

### Behavioral Shifts
- Analyze from EVERY aspect — functional, non-functional, boundary, dependency, consistency, feasibility
- Actively hunt for what's MISSING (gaps) not just what's WRONG (errors) — unstated requirements cause more failures than misstated ones
- Challenge vague language ("configurable", "scalable", "fast") — demand specific, measurable targets or flag for clarification
- Classify every finding by severity (Critical/High/Medium/Low) with a resolution path

### Anti-Patterns for This Stage
- Do NOT accept implied scope without documenting it explicitly as an assumption
- Do NOT present a finding without a severity classification and suggested resolution path

### Quality Check
A good output at this stage sounds like:
- "18 findings across 5 categories; 3 Critical (block feasibility), 5 High (require clarification), 10 Medium; each with resolution: resolve/defer/accept..."
- Don't accept "best practice" as a requirement — insist on specific, testable statements
- Consider: "If a developer reads this, can they build it without guessing?"

---

## Depth Adaptation

| Depth | Behavior |
|-------|----------|
| **Minimal** | Quick scan for critical gaps and contradictions only. Brief findings list. No formal report. |
| **Standard** | Full analysis across all dimensions. Categorized findings. Formal report produced. |
| **Comprehensive** | Exhaustive analysis with traceability matrix, process lifecycle checks, cross-requirement dependency mapping, and forward-compatibility assessment. |

---

## Step-by-Step Execution

### Step 1: Load Context

1. Read the approved Requirement Intake Form (Stage 3 output)
2. Read the original source document (for cross-reference)
3. Note the workflow depth (from Stage 2 assessment)
4. Review any assumptions already logged in the Assumptions register

---

### Step 2: Analyze — Completeness Dimension

Check each requirement category for completeness:

#### Functional Requirements Checklist

For each functional requirement domain, verify:

| Check | Question | Finding Type if Missing |
|-------|----------|:----------------------:|
| Actors defined | Who uses this capability? What roles? | 🟠 Ambiguity |
| Trigger identified | What initiates this function? | 🟡 Gap |
| Input specified | What data/information is needed? | 🟠 Gap |
| Process described | What happens (business logic)? | 🔴 Critical Gap (if core) |
| Output defined | What is produced/changed? | 🟠 Gap |
| Error handling | What happens when it fails? | 🟡 Gap |
| Access control | Who can/cannot perform this? | 🟠 Gap (if multi-user) |
| Data scope | What data boundaries apply? | 🟠 Gap (if multi-tenant/multi-org) |

#### Non-Functional Requirements Checklist

| NFR Category | Minimum Expected | Finding if Missing |
|--------------|-----------------|:------------------:|
| Performance | Response time targets, throughput | 🟠 Gap |
| Scalability | Capacity targets (users, data, transactions) | 🟠 Gap |
| Availability | Uptime target, maintenance windows | 🟡 Gap |
| Security | Auth method, encryption, compliance standard | 🔴 Critical (if regulated) |
| Disaster Recovery | RPO/RTO targets | 🟡 Gap |
| Accessibility | WCAG level or equivalent | 🟡 Gap |
| Localisation | Languages, regions, RTL support | 🟡 Gap |
| Browser/Platform | Supported platforms/versions | 🟡 Gap |
| API/Integration | Protocols, standards, documentation | 🟠 Gap (if API-first) |
| Data Retention | Retention periods, archival, deletion | 🟡 Gap |

---

### Step 3: Analyze — Consistency Dimension

Look for contradictions within and across requirements:

| Check Type | What to Look For | Example |
|------------|-----------------|---------|
| **Internal contradiction** | Same topic says different things in different sections | "No external dependencies" vs. "integrate with cloud AI service" |
| **Scope vs. requirements** | Item listed as out-of-scope but referenced as functionality elsewhere | Deferred module referenced in an in-scope workflow |
| **NFR vs. constraint** | NFR target conflicts with stated constraint | "99.99% uptime" with "single server deployment" |
| **Priority conflict** | Two requirements claim "must have" but are mutually exclusive | Both option A and option B stated as mandatory |
| **Timeline vs. scope** | Stated timeline appears insufficient for stated scope | 3-month timeline for 50+ requirements |
| **Architecture vs. requirements** | Stated architecture doesn't support stated capability | "Serverless" with "on-premises deployment" |

---

### Step 4: Analyze — Dependency Dimension

Identify dependencies between requirements and on external factors:

#### Inter-Requirement Dependencies

```markdown
| Requirement | Depends On | Dependency Type | Risk if Unmet |
|-------------|-----------|:---------------:|---------------|
| FR-{nn} | FR-{mm} | Must precede | Cannot build {nn} without {mm} |
| FR-{nn} | NFR-{mm} | Architecture | Technology choice constrains implementation |
```

#### External Dependencies

```markdown
| Dependency | Required By | External Owner | Status | Risk |
|------------|-------------|:-------------:|:------:|------|
| {system/team/resource} | FR-{nn} | {who owns it} | Known/Unknown | {what if unavailable} |
```

---

### Step 5: Analyze — Feasibility Signals

Flag any requirements that raise feasibility concerns:

| Concern Type | Indicators | Finding Severity |
|--------------|-----------|:----------------:|
| **Technically unrealistic** | Contradicts known limitations; no known solution | 🔴 Critical |
| **Disproportionate effort** | Single requirement drives 30%+ of project cost | 🟠 High |
| **Unproven technology** | Requires R&D or novel approach | 🟠 High |
| **Operational complexity** | Requires organizational changes beyond project control | 🟡 Medium |
| **Vague success criteria** | "Best in class", "world-class", "fast" — no measurable target | 🟡 Medium |
| **Gold-plating risk** | Excessive specification for marginal value | 🟡 Medium |

---

### Step 6: Analyze — Process Lifecycle (Comprehensive depth only)

For Comprehensive depth, verify process integrity:

- Do stated processes have complete lifecycles (create → manage → close/archive)?
- Are handoff points between processes defined?
- Are escalation paths specified?
- Do reporting requirements align with data collected in processes?
- Are audit/compliance touchpoints identified at each process stage?

---

### Step 7: Compile Findings

Organize all findings into a structured report:

```markdown
# Requirements Analysis Report

## Project: {project_name}
## Analyzed: {date}
## Source: Requirement Intake Form v{version}
## Depth: {Minimal / Standard / Comprehensive}

---

## Summary

| Severity | Count | Stage 5 Trigger? |
|:--------:|:-----:|:----------------:|
| 🔴 Critical | {n} | Yes — must resolve before feasibility |
| 🟠 High | {n} | Yes — if ≥3, triggers clarification |
| 🟡 Medium | {n} | No — can resolve during planning |
| 🟢 Informational | {n} | No — observations only |
| **Total** | **{n}** | |

---

## Findings

### 🔴 Critical Findings

#### {FIND-001}: {Title}
- **Category:** {Gap / Inconsistency / Ambiguity / Dependency / Feasibility}
- **Location:** {Which requirement(s) or section(s)}
- **Description:** {What the problem is}
- **Impact:** {What goes wrong if unresolved}
- **Resolution needed:** {What decision or clarification will fix this}
- **Suggested resolution:** {AI's recommended approach}

---

### 🟠 High-Priority Findings
{Same format as Critical}

---

### 🟡 Medium Findings
{Same format — can be abbreviated}

---

### 🟢 Informational Observations
{Brief bullets — no resolution needed, just noted}

---

## Dependency Map

{Table of inter-requirement and external dependencies}

---

## Stage 5 Recommendation

{State whether Clarification Cycle should be triggered and why}
```

---

### Step 8: Determine Clarification Trigger

Apply the following rules:

| Condition | Action |
|-----------|--------|
| Any 🔴 Critical findings | **TRIGGER** Stage 5 — cannot proceed without resolution |
| 3+ 🟠 High findings | **TRIGGER** Stage 5 — too many open questions |
| 1-2 🟠 High findings | **OPTIONAL** — ask user if they want to resolve now or proceed |
| Only 🟡 and 🟢 | **SKIP** Stage 5 — proceed to Feasibility (Stage 6) |

---

### Step 9: Log and Register

1. **Decision Log:** D-{nnn}: "Requirements Analysis complete. {n} findings: {critical} critical, {high} high, {medium} medium. Stage 5 {triggered/skipped}."
2. **Assumptions Register:** Add any assumptions made during analysis (e.g., "ASM-{nnn}: Assumed {X} because source is silent on this topic")
3. **Action Items:** Create actions for any findings that need stakeholder input beyond the user (e.g., "A-{nnn}: Confirm {X} with {stakeholder role}")
4. **State File:** Stage 4 = ✅ Done; note findings count; set Stage 5 status to Active or Skipped

---

### Step 10: Present to User

```markdown
## Stage 4: Requirements Analysis — Complete

**Findings Summary:**
- 🔴 {n} Critical — {brief description of most important}
- 🟠 {n} High — {brief description}
- 🟡 {n} Medium — {brief description}
- 🟢 {n} Informational

**Full report:** Saved to `{file_path}`

---

{IF Stage 5 triggered:}
**⚠️ Clarification Cycle Required**
{n} critical/high findings need resolution before we can assess feasibility.
I'll prepare structured questions for each finding.

Proceeding to Stage 5: Clarification Cycle...

{IF Stage 5 optional:}
**ℹ️ Minor gaps found — your choice:**
- (a) **Resolve now** — I'll ask clarification questions (Stage 5)
- (b) **Proceed** — Address these during planning; go to Feasibility (Stage 6)

**Recommended:** {(a) or (b) with rationale}

{IF Stage 5 skipped:}
**✅ Requirements are solid**
No critical gaps found. Minor observations noted for awareness.

Proceeding to Stage 6: Feasibility Assessment...
```

---

## Analysis Heuristics

### Common Patterns to Flag

| Pattern | Likely Finding | Severity |
|---------|---------------|:--------:|
| "TBD" or "to be determined" in source | Gap — decision deferred | 🟠 High |
| "Should" vs "Must" inconsistency | Ambiguity — priority unclear | 🟡 Medium |
| Feature mentioned once, never detailed | Gap — incomplete specification | 🟡 Medium |
| Same concept, different names | Ambiguity — terminology inconsistent | 🟡 Medium |
| Numeric targets without context | Ambiguity — basis for target unclear | 🟡 Medium |
| Reference to external system with no detail | Dependency — integration undefined | 🟠 High |
| "Similar to {competitor}" as specification | Gap — not a requirement | 🟠 High |
| All requirements same priority | Ambiguity — no actual prioritization | 🟡 Medium |
| User roles mentioned but not defined | Gap — access model incomplete | 🟠 High |
| "Configurable" without specifying by whom | Ambiguity — authority model unclear | 🟡 Medium |

---

## Output File

Save the Requirements Analysis Report to:
- Numbered: `{output_root}/02_Screening_Prioritization/Requirements_Analysis_Report.md`
- Flat: `{output_root}/pilc-docs/assessment/Requirements_Analysis_Report.md`

For **Minimal** depth: findings can be embedded in the state file rather than a separate report (if fewer than 5 findings total).
