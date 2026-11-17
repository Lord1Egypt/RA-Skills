<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Story Acceptance Mapping

## Stage: 8 of 12
## Phase: 🟢 OBSERVATION
## Execution: CONDITIONAL — if user stories exist

---

## Purpose

Read user stories and their acceptance criteria from `aidlc-docs/inception/user-stories/` (or equivalent location). For each acceptance criterion, register an acceptance test requirement. Link to existing register entries where overlap exists (preventing duplication). This stage ensures that as stories are elaborated during delivery, test requirements keep pace.

---

## Conditional Trigger

| Execute IF | Skip IF |
|-----------|---------|
| `aidlc-docs/inception/user-stories/` contains story files | No user stories in aidlc-docs |
| Stories have been added or modified since last TGE observation | Stories unchanged since last mapping |
| User explicitly requests "map stories" or "derive acceptance tests" | User says "skip story mapping" |

**If skipped:** Log in state file: `Stage 8: Skipped (no user stories detected)`. Proceed to Stage 9.

---

## Depth Adaptation

| Depth | Mapping Scope | Register Detail |
|-------|--------------|----------------|
| **Minimal** | Extract criteria count per story. Register 1 acceptance test per story (grouped). Link to existing entries by component name only. | Summary-level: {n} stories → {n} acceptance tests |
| **Standard** | Extract each criterion individually. Register 1 test per criterion. Link to architecture-derived entries where overlap detected. Deduplicate explicitly. | Per-criterion entries with source links + deduplication notes |
| **Comprehensive** | Full criterion extraction + scenario decomposition (multi-scenario criteria get multiple tests). Cross-reference to AP commitments. Identify criteria that imply missing architecture (stories promise things AP doesn't cover). | Full scenario mapping + architecture gap detection + cross-reference matrix |

---

## MANDATORY: Stage Sub-Role — Business Analyst

During THIS stage, ALSO adopt the mindset of a **Business Analyst**. This does NOT replace your primary role (Senior QA Engineer / Test Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Read acceptance criteria from the user's perspective: "As a user, I expect..." — these become assertion statements
- Each criterion is a testable assertion — decompose compound criteria into individual checkable items
- Think about the happy path AND the error path: "Given invalid input, what should happen?" is also an acceptance criterion
- Link stories to architecture: "This story exercises the PaymentService API endpoint API-003" — connect vertically

### Anti-Patterns for This Stage
- Do NOT register acceptance tests for criteria that are already fully covered by architecture-derived unit/integration tests — link, don't duplicate
- Do NOT invent criteria not present in the stories — derive only from what's written
- Do NOT register vague tests: "User can use the system" is not a testable criterion
- Do NOT ignore negative criteria: "System should NOT allow X" = important acceptance test

### Quality Check
A good output at this stage sounds like:
- "Mapped 12 user stories → 34 acceptance criteria → 28 new register entries (6 already covered by architecture-derived tests — linked, not duplicated). New entries: 24 Acceptance/Functional/Workflow, 4 Acceptance/Functional/Error Handling. Story-005 references a capability not in the AP (reporting export) — flagged as potential architecture gap."

---

## Step-by-Step Execution

### Step 1: Locate and Read Story Files

Find user stories at known locations:

| Location | Format Expected |
|----------|----------------|
| `aidlc-docs/inception/user-stories/` | Markdown files with acceptance criteria sections |
| `aidlc-docs/inception/requirements/` | May contain stories with NFR criteria |
| `{custom path from tge-state.md}` | User-specified story location |

**Story structure expected:**
```markdown
# US-{NNN}: {Story Title}

**As a** {persona}
**I want** {capability}
**So that** {benefit}

## Acceptance Criteria

- AC1: {criterion}
- AC2: {criterion}
- AC3: {criterion}
```

---

### Step 2: Extract Acceptance Criteria

For each story file:

| Field | Extraction |
|-------|-----------|
| Story ID | `US-{NNN}` from filename or heading |
| Story Title | Heading text |
| Persona | "As a" clause → who is this for |
| Criteria | Each AC item → one testable assertion |
| Components | Inferred from story context (which services are involved) |

**Decomposition rules:**
- Compound criterion ("User can X AND Y") → split into AC-X and AC-Y (two tests)
- Conditional criterion ("If A then B, else C") → two tests (A→B path and ¬A→C path)
- Negative criterion ("System should NOT allow X") → one test (attempt X, verify rejection)
- Performance criterion embedded in story ("within 3 seconds") → extract as NFR test, not acceptance

---

### Step 3: Check for Existing Coverage

Before registering new entries, check if the criterion is already covered:

| Check | Result | Action |
|-------|--------|--------|
| Architecture-derived test covers this exact behavior | Duplicate | Link: `Covered by: {ARCH-ID}` — do NOT create new entry |
| Architecture-derived test covers part of this behavior | Partial | Create entry for UNCOVERED portion only |
| Baseline test covers this behavior | Duplicate | Link: `Covered by: {BASE-ID}` — do NOT create new entry |
| No existing coverage | New | Register as new Story-derived entry |

**Deduplication format:**
```markdown
## Deduplication Log

| Story Criterion | Existing Register Entry | Relationship |
|----------------|------------------------|:------------:|
| US-003-AC1: "User can log in with valid credentials" | SEC-001: Auth valid credential test | Fully covered |
| US-005-AC2: "Payment is processed successfully" | API-012: POST /payments returns 201 | Partially covered (API test, not E2E) |
| US-007-AC1: "Admin can export reports" | — | New (not in register) |
```

---

### Step 4: Register New Entries

For each criterion NOT already covered:

```markdown
| ID | Commitment | Level | Type | Sub-Type | Test Name | Source | Risk Score | Status |
|:--:|:----------:|:-----:|:----:|:--------:|-----------|:------:|:----------:|:------:|
| STORY-003-AC2 | US-003 | Acceptance | Functional | Workflow | User receives confirmation email after registration | Story | _[pending scoring]_ | Required |
```

**Classification rules for story-derived tests:**
- Level: Almost always `Acceptance` (user-facing behavior)
- Type: Usually `Functional` (correct behavior from user perspective)
- Sub-Type: `Workflow` (multi-step) or `Error Handling` (negative criteria) or `Boundary` (edge case)
- Exception: NFR criteria embedded in stories → extract as System/Non-Functional

---

### Step 5: Identify Architecture Gaps (Comprehensive Depth)

At Comprehensive depth, check if stories reference capabilities not present in the AP:

```markdown
## Architecture Gap Signals from Stories

| Story | Criterion | Expected AP Commitment | Found? |
|-------|-----------|----------------------|:------:|
| US-007 | "Admin can export reports to PDF" | Reporting/export component in AP | ❌ Not found |
| US-012 | "System notifies user via SMS" | SMS integration in integration map | ❌ Not found |

**Recommendation:** These stories imply architecture commitments not documented in the AP. Consider:
- Updating the AP to include these capabilities (then re-derive tests from architecture)
- Proceeding with story-derived tests only (lower traceability but still governed)
```

---

### Step 6: Update Register

Append new story-derived entries to the test register:

```markdown
## Story-Derived Entries Added

| Count | Stories Processed | Criteria Extracted | New Entries | Already Covered | Architecture Gaps |
|:-----:|:-----------------:|:------------------:|:-----------:|:---------------:|:-----------------:|
| {N} | {n} stories | {n} criteria | {n} new entries | {n} linked | {n} gaps flagged |
```

---

### Step 7: Report (Non-Blocking)

```markdown
## 🟢 Story Acceptance Mapping Complete

**Stories processed:** {n}
**Acceptance criteria extracted:** {n}
**New register entries:** {n} (Source: Story)
**Already covered by architecture/baseline:** {n} (linked, not duplicated)
**Architecture gaps flagged:** {n}

{IF gaps found:}
⚠️ {n} stories reference capabilities not in the Architecture Package. These are governed by story-derived tests but lack architecture traceability.

Register updated. Coverage stats will be recalculated in Stage 9.
```

**No gate.** This stage is informational in the observation phase — results feed into coverage reporting.

---

## Output Artifacts

| Artifact | Location | Purpose |
|----------|----------|---------|
| Updated Test Register | `.governance/test/test-register.md` | New story-derived entries appended |
| Deduplication log | (inline in register notes) | Records which criteria are covered elsewhere |
| Updated state file | `.governance/test/tge-state.md` | Stage 8 complete; entry counts updated |

---

## Stage Completion Criteria

| Check | Pass Criteria |
|-------|---------------|
| All story files read | Every file in user-stories directory processed |
| Criteria extracted | Each story has ≥1 criterion registered or linked |
| Deduplication applied | No duplicate entries (overlapping with architecture-derived) |
| Classification correct | Story entries use Acceptance level (unless NFR extracted) |
| IDs follow convention | `STORY-{story_id}-AC{n}` format |
| Gaps flagged (Comprehensive) | Capabilities not in AP identified |
| Register updated | New entries appended with Source = Story |
| Non-blocking | No user action required to proceed |
