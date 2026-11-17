<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# State Observation

## Stage: 7 of 12
## Phase: 🟢 OBSERVATION
## Execution: ALWAYS (in Observation Phase)

---

## Purpose

Read the AI-DLC v1 state file (`aidlc-docs/aidlc-state.md`) to identify newly completed units and stages. For each completed unit, check whether its required tests now exist in the source code. Update the register with current existence status. This is the engine's continuous monitoring heartbeat.

This stage runs every time AI-TGE is invoked during the Observation phase — it's the entry point for tracking build progress against test obligations.

---

## Depth Adaptation

| Depth | Observation Scope | Update Detail |
|-------|------------------|--------------|
| **Minimal** | Check aidlc-state for completed units. Verify test file existence (filename match only). Update register status. | Binary: test file exists / doesn't exist |
| **Standard** | Check completed units + read test file names/describe blocks. Match to specific register entries. Track new tests written since last observation. | Per-entry status update + delta report |
| **Comprehensive** | Full scan: completed units + test content analysis + assertion verification. Detect partial coverage (test exists but doesn't cover all assertions). Track test quality, not just existence. | Detailed verification + partial coverage flags + quality notes |

---

## MANDATORY: Stage Sub-Role — Automation Engineer

During THIS stage, ALSO adopt the mindset of an **Automation Engineer**. This does NOT replace your primary role (Senior QA Engineer / Test Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in terms of state changes and events — what changed since last observation?
- Focus on detecting WHAT'S NEW: new test files, new test blocks, new code completions
- Be efficient: don't rescan everything if state file shows only 1 unit completed since last check
- Report deltas, not full state: "Since last observation, 3 tests were added, covering 2 Critical gaps"

### Anti-Patterns for This Stage
- Do NOT block on this stage — observation is continuous, never gated
- Do NOT report full register status every time — only report changes
- Do NOT modify test files — observation is read-only
- Do NOT re-score risks here — that's Stage 12 (Debt Reassessment)

### Quality Check
A good output at this stage sounds like:
- "Observation cycle complete. 2 units completed since last check (UserService Code Gen, OrderService Build-and-Test). 4 new test files detected. Register updated: 6 entries moved from Missing → Exists. 2 Critical gaps remain (SEC-001: auth bypass, DATA-003: transaction integrity)."

---

## Step-by-Step Execution

### Step 1: Read AI-DLC v1 State

Load `aidlc-docs/aidlc-state.md` (or equivalent state tracking):

| State Field | What It Tells Us |
|-------------|-----------------|
| Units completed | Which features/components have been built |
| Current stage per unit | Code Gen → Build-and-Test → Review → Complete |
| Stories completed | Which user stories are now accepted |
| Last build timestamp | When the last code was produced |

**Extract:** List of units/features completed SINCE last TGE observation (compare timestamps with `tge-state.md → Last Updated`).

If no aidlc-state exists (Observation Only mode without DLC):
- Fall back to scanning for new test files since last observation
- Use file modification timestamps as proxy for build progress

---

### Step 2: Identify Register Entries Affected

For each newly completed unit, find its register entries:

```markdown
## Affected Register Entries

Unit completed: {unit_name}
Components involved: {component list}

| Register Entry | Level | Type | Previous Status | Action Needed |
|:-------------:|:-----:|:----:|:---------------:|:--------------|
| API-001 | Integration | Contract | Missing | Check for test existence |
| BL-003 | Unit | Business Logic | Missing | Check for test existence |
| BASE-API-01 | Integration | Contract | Missing | Check for test existence |
```

---

### Step 3: Scan for Test Existence

For each affected register entry, check whether a matching test now exists:

**Scanning approach (by depth):**

| Depth | Method |
|-------|--------|
| Minimal | Check if test file for the component exists (e.g., `user-service.test.ts` exists) |
| Standard | Read test file names and describe/it blocks; match to register entry test names |
| Comprehensive | Read test content; verify assertions match what the register requires |

**Matching criteria (same as Stage 4 brownfield):**
- Exact name match (High confidence)
- Semantic match (Medium confidence)
- Component + type match (Low confidence)

---

### Step 4: Update Register Status

For each entry checked:

| Finding | New Status | Register Update |
|---------|:----------:|----------------|
| Matching test found (High confidence) | `Exists` | Add verification note: `Verified: {file_path} ({timestamp})` |
| Matching test found (Medium confidence) | `Exists (unverified)` | Add note: `Possible match: {file_path} — verify manually` |
| No test found | `Missing` (unchanged) | No change; remains in debt scorecard |
| Test found but failing | `Failing` | Add note: `Test exists but failing: {file_path}` |

---

### Step 5: Calculate Delta

```markdown
## Observation Delta — {ISO timestamp}

**Period:** {last observation timestamp} → {now}
**Units completed:** {n}
**Register entries checked:** {n}

### Changes This Cycle

| Metric | Before | After | Delta |
|--------|:------:|:-----:|:-----:|
| Tests Existing | {n} | {n} | +{n} |
| Tests Missing | {n} | {n} | -{n} |
| Tests Failing | {n} | {n} | {±n} |
| Coverage % | {n}% | {n}% | +{n}% |

### Entries Moved to Exists
| ID | Test Name | Component | Was Bucket |
|:--:|-----------|-----------|:----------:|
| {id} | {name} | {comp} | {🔴🟠🟡🟢} |

### Critical/High Gaps Remaining
| ID | Test Name | Component | Score |
|:--:|-----------|-----------|:-----:|
| {id} | {name} | {comp} | {score} |
```

---

### Step 6: Update State File

```markdown
# Updates to tge-state.md

- **Last Stage Completed:** 7 (or latest observation stage reached)
- **Last Updated:** {ISO timestamp}
- **Register Stats:** (recalculated from register)
  - Tests Required: {N}
  - Tests Existing: {n}
  - Tests Missing: {n}
  - Tests Failing: {n}
  - Tests Deprecated: {n}
  - Coverage: {n}%
```

---

### Step 7: Report (Non-Blocking)

Present observation results without requiring user action:

```markdown
## 🟢 Observation: State Check Complete

**Since last check:** {n} units completed, {n} new tests detected
**Register updated:** {n} entries moved Missing → Exists
**Current coverage:** {n}% (was {n}%)

{IF Critical gaps remain:}
⚠️ **Critical gaps remaining:** {n}
- {id}: {name} (Score: {score})

{IF all Critical resolved:}
✅ All Critical-risk tests now exist.

{IF no changes:}
ℹ️ No new completions detected since last observation.
```

**No gate.** Observation is continuous — inform the user and proceed to next applicable stage.

---

## Trigger Conditions

This stage executes when:
1. User invokes AI-TGE during Observation phase ("check coverage", "update register")
2. Session starts and state file shows Observation phase active
3. User explicitly requests "observe" or "what's the coverage now?"
4. After any other observation stage completes (as the re-entry point)

---

## Output Artifacts

| Artifact | Location | Purpose |
|----------|----------|---------|
| Updated Test Register | `.governance/test/test-register.md` | Status field updated for checked entries |
| Updated state file | `.governance/test/tge-state.md` | Stats recalculated; timestamp updated |
| Observation log (Comprehensive) | `.governance/test/observation-log.md` | Append-only history of observation cycles |

---

## Stage Completion Criteria

| Check | Pass Criteria |
|-------|---------------|
| State file read | aidlc-state.md (or fallback) consulted |
| Affected entries identified | All register entries for completed units checked |
| Status updated | Each checked entry reflects current test existence |
| Coverage recalculated | % reflects updated status counts |
| State file updated | Timestamp and stats current |
| Delta reported | User informed of changes (if any) |
| Non-blocking | No user action required to continue |
