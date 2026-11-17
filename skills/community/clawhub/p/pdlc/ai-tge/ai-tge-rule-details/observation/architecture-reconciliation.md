<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Architecture Reconciliation

## Stage: 10 of 12
## Phase: 🟢 OBSERVATION
## Execution: CONDITIONAL — if AP changed since last read

---

## Purpose

Detect changes in the Architecture Package since the last TGE strategy run. For each change, propose register updates: new commitments → new required tests; removed commitments → deprecate tests; changed contracts → flag tests for review. All operations are **non-destructive** — AI-TGE proposes changes but never auto-applies them to the register without user confirmation.

This stage implements  (Reconciliation is not optional) and  (Downstream signaling) for the test governance domain.

---

## Conditional Trigger

| Execute IF | Skip IF |
|-----------|---------|
| AP has been modified since last `tge-state.md → AP Version → Last Read` timestamp | AP unchanged since last strategy run |
| User explicitly requests "reconcile" or "check for architecture changes" | Mode = Brownfield (no AP to reconcile against) |
| Upstream signal received: "AP updated — reconcile downstream" | Mode = Observation Only (no AP connection) |

**If skipped:** Log in state file: `Stage 10: Skipped (AP unchanged since {last_read_timestamp})`. Proceed to Stage 11 (if applicable) or Stage 12.

---

## Depth Adaptation

| Depth | Reconciliation Scope | Output Detail |
|-------|---------------------|--------------|
| **Minimal** | Detect major changes only: new/removed components, new/removed endpoints. Propose additions/deprecations in bulk. | Change summary + bulk action |
| **Standard** | Detect all changes: new, removed, modified artifacts. Per-change test register impact analysis. Individual add/deprecate/review proposals. | Per-change impact + individual proposals |
| **Comprehensive** | Full delta analysis: every file change → specific register entries affected. Impact chains (change to component A affects tests for B if B depends on A). Ripple analysis. | Full delta matrix + dependency impact + ripple assessment |

---

## MANDATORY: Stage Sub-Role — Systems Engineer

During THIS stage, ALSO adopt the mindset of a **Systems Engineer**. This does NOT replace your primary role (Senior QA Engineer / Test Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in terms of delta: what CHANGED, not what EXISTS — focus on the difference
- Assess impact of each change on the test register systematically: addition, removal, or modification
- Consider dependency chains: if Component A's API changes, tests for Component B (which calls A) may also need review
- Be conservative: propose deprecation (not deletion), flag for review (not auto-modify)

### Anti-Patterns for This Stage
- Do NOT auto-apply changes — reconciliation PROPOSES; user APPROVES
- Do NOT delete register entries — deprecate them (audit trail preserved)
- Do NOT ignore transitive impacts — a changed API affects all consumers' test requirements
- Do NOT treat all changes equally — a renamed field is minor; a removed endpoint is major

### Quality Check
A good output at this stage sounds like:
- "AP delta detected: 2 new endpoints (POST /orders, DELETE /orders/{id}), 1 removed component (LegacyReportService), 1 modified contract (GET /users now returns pagination metadata). Impact: +6 new test entries proposed, 4 entries proposed for deprecation, 2 entries flagged for review (response schema changed)."

---

## Step-by-Step Execution

### Step 1: Detect AP Changes

Compare current AP state against last-read state:

| Detection Method | How |
|-----------------|-----|
| Timestamp comparison | AP file modification dates vs. `tge-state.md → AP Version → Last Read` |
| Marker file version | `adlc-state.md` version field (if AP tracks versions) |
| Content hash | Compare file hashes from last read (Comprehensive depth) |
| Manual trigger | User says "architecture changed — reconcile" |

**Produce change inventory:**
```markdown
## AP Changes Detected

| Change Type | Artifact | What Changed |
|:-----------:|----------|-------------|
| ➕ Added | api-contract-orders.md | New endpoint: POST /orders |
| ➕ Added | api-contract-orders.md | New endpoint: DELETE /orders/{id} |
| ➖ Removed | component-legacy-reports.md | Entire component removed from architecture |
| 🔄 Modified | api-contract-users.md | GET /users response now includes pagination |
| 🔄 Modified | security-adr-003.md | MFA added as secondary auth factor |
```

---

### Step 2: Classify Each Change

For each detected change, determine the test register impact:

| Change Type | Register Impact | Action |
|:-----------:|----------------|--------|
| **New commitment** (new endpoint, new component, new ADR) | New test entries needed | Propose additions |
| **Removed commitment** (component deleted, endpoint removed) | Existing tests no longer required | Propose deprecation |
| **Modified commitment** (contract changed, SLA updated) | Existing tests may be invalid/insufficient | Flag for review |
| **Renamed** (same functionality, different name) | Tests still valid but reference needs update | Propose rename |

---

### Step 3: Derive New Entries (for Additions)

For each new commitment, apply the same derivation logic as Stage 3:

1. Identify commitment type (API, Security, Business Logic, etc.)
2. Apply Primary Mapping Table (from test-taxonomy.md)
3. Apply relevant baseline rules
4. Produce register entries with:
   - Source: `Reconciliation`
   - Status: `Required`
   - Risk Score: `_[pending re-scoring in Stage 12]_`
   - Reconciliation Date: `{ISO timestamp}`

```markdown
## Proposed New Entries

| ID | Commitment | Level | Type | Sub-Type | Test Name | Source |
|:--:|:----------:|:-----:|:----:|:--------:|-----------|:------:|
| API-015 | POST /orders | Integration | Functional | Contract | POST /orders returns 201 with valid OrderDTO | Reconciliation |
| API-016 | POST /orders | Integration | Functional | Error Handling | POST /orders returns 400 on invalid payload | Reconciliation |
| API-017 | DELETE /orders/{id} | Integration | Functional | Contract | DELETE /orders/{id} returns 204 on success | Reconciliation |
```

---

### Step 4: Propose Deprecations (for Removals)

For each removed commitment, identify affected register entries:

```markdown
## Proposed Deprecations

| Register Entry | Reason | Action |
|:-------------:|--------|--------|
| BL-012: LegacyReportService calculation test | Component removed from AP | Deprecate (mark, don't delete) |
| BL-013: LegacyReportService export test | Component removed from AP | Deprecate |
| BASE-BL-01 (for LegacyReportService) | Component no longer exists | Deprecate baseline entry for this instance |

**Note:** Deprecated entries remain in register with Status = `Deprecated`, Deprecation Reason, and Deprecation Date. They are excluded from coverage calculations but preserved for audit trail.
```

---

### Step 5: Flag for Review (for Modifications)

For each modified commitment, identify tests that may need updating:

```markdown
## Entries Flagged for Review

| Register Entry | Change Detected | Review Needed |
|:-------------:|----------------|:-------------:|
| API-001: GET /users returns user list | Response now includes pagination metadata | ⚠️ Test may need updated assertion (verify pagination fields) |
| SEC-005: MFA not required | Security ADR now mandates MFA | ⚠️ Test assertion is now WRONG — MFA should be required |

**Review flags mean:** The test may still be valid, or it may need updating. Human judgment required.
```

---

### Step 6: Assess Transitive Impact (Comprehensive Depth)

If Component A changed and Component B depends on A:

```markdown
## Transitive Impact Analysis

| Changed Component | Dependent Components | Test Entries Affected |
|-------------------|---------------------|:--------------------:|
| UserService (API response changed) | OrderService (reads user data) | INT-003, INT-004 (may expect old response format) |
| AuthService (MFA added) | All authenticated endpoints | SEC-* entries (auth flow now has extra step) |

**Recommendation:** Review {n} dependent test entries for compatibility with upstream changes.
```

---

### Step 7: Present Reconciliation Proposal

```markdown
## Review: Architecture Reconciliation

AP changes detected since last strategy run ({last_read_date}).

**Summary:**
- **New commitments:** {n} → {n} new test entries proposed
- **Removed commitments:** {n} → {n} entries proposed for deprecation
- **Modified commitments:** {n} → {n} entries flagged for review
- **Transitive impacts:** {n} dependent entries to check

### Proposed Actions

**Add ({n} new entries):**
{table of proposed additions}

**Deprecate ({n} entries):**
{table of proposed deprecations}

**Review ({n} entries):**
{table of flagged entries}

---

**Your response:**
- (a) **Accept all** — apply all proposed changes to the register
- (b) **Accept with modifications** — apply some, change others (specify)
- (c) **Reject** — do not update the register (keep current state)
- (d) **Review individually** — walk through each change one by one
```

---

## Gate

**This stage has a GATE.** Reconciliation changes the test register — new entries create new obligations, deprecations close existing ones. The user must approve before changes are applied. This ensures architecture changes are acknowledged in test governance intentionally.

---

### Step 8: Apply Approved Changes

After user approval:

1. **Add new entries** to register (Source = Reconciliation, Status = Required)
2. **Mark deprecated entries** (Status = Deprecated, Deprecation Reason, Deprecation Date)
3. **Flag reviewed entries** (add Review Note: "{what changed} — verified {date}" or Status remains as-is pending manual review)
4. **Update state file:**
   - AP Version → Last Read: {current timestamp}
   - Reconciliation Needed: No
   - Register stats recalculated

---

## Output Artifacts

| Artifact | Location | Purpose |
|----------|----------|---------|
| Updated Test Register | `.governance/test/test-register.md` | New entries added; deprecations applied; review flags set |
| Reconciliation log | (appended to register as section) | Audit trail of what changed and when |
| Updated state file | `.governance/test/tge-state.md` | AP version timestamp updated; stats recalculated |

---

## Stage Completion Criteria

| Check | Pass Criteria |
|-------|---------------|
| AP delta detected | Changes identified since last read |
| All changes classified | Each as: addition, removal, modification, or rename |
| New entries derived correctly | Follow same derivation rules as Stage 3 |
| Deprecations preserve audit trail | Entries marked (not deleted) with reason and date |
| Review flags are specific | Each flag says WHAT changed and WHY review is needed |
| Non-destructive | No auto-applied changes without user approval |
| User approved | Reconciliation proposal accepted (or subset accepted) |
| State file updated | AP timestamp current; Reconciliation Needed = No |
| Register stats recalculated | Totals reflect additions/deprecations |
