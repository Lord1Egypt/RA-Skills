<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Question Format Guide

## Purpose

AI-TGE uses structured questions to collect user input at specific decision points during test governance. Unlike lifecycle packages (AI-PILC, AI-ADLC) where decisions shape the entire output, AI-TGE's questions are focused on validation, override, and prioritization — confirming what was derived rather than designing from scratch.

This document defines formatting rules, interaction patterns, and gate formats specific to test governance.

---

## Question Types

### Type 1: Derivation Confirmation

Used when AI-TGE has derived test requirements from the architecture and needs user validation before committing to the register.

**Format:**

```markdown
### Architecture Commitment Inventory — Review

I've read the Architecture Package and identified **{N}** testable commitments:

| # | Commitment ID | Source Artifact | What It Promises | Tests Derived |
|---|:-------------:|----------------|-----------------|:-------------:|
| 1 | API-001 | API Architecture | POST /users validates email + returns 201 | 3 |
| 2 | SEC-001 | Security Architecture | JWT auth with role-based access | 4 |
| 3 | DATA-001 | Data Architecture | User entity CRUD with validation | 3 |
| ... | ... | ... | ... | ... |

**Total:** {N} commitments → {M} test requirements derived

**Your Review:**
- (a) **Approve** — commitments correctly identified; proceed to register
- (b) **Challenge** — some commitments are missing or wrong
- (c) **Add** — I know of commitments not captured here
- (d) **Reduce** — some of these are over-specified for our needs
```

**Rules:**
- Present as a summary table (not individual questions per commitment)
- Show the DERIVATION (what was found → what tests result)
- Allow batch approval ("approve all")
- If user challenges → drill into specific entries

---

### Type 2: Risk Assessment Input

Used when AI-TGE needs user input to score risk factors that cannot be auto-derived (team context, change frequency, organizational priority).

**Format:**

```markdown
### Risk Assessment — {Component/Commitment}

I can auto-derive 2 of 4 risk factors. I need your input on the others:

**Auto-derived:**
- Architectural Risk: **{N}/5** — {brief rationale}
- Blast Radius: **{N}/5** — {brief rationale}

**Need your input:**

1. **Logic Complexity** (1-5): How complex is the implementation logic?
   - 1 = Simple CRUD, trivial logic
   - 3 = Moderate business rules, some state management
   - 5 = Complex algorithms, state machines, concurrent operations
   
   Your score: _[awaiting input]_

2. **Change Frequency** (1-5): How often does this code change?
   - 1 = Stable, rarely touched (maybe once a quarter)
   - 3 = Regular development (changes every sprint)
   - 5 = Active hot zone (changes multiple times per sprint)
   
   Your score: _[awaiting input]_

**Shortcut:** "Use defaults" → I'll score both at 3 (medium).
```

**Rules:**
- Only ask when auto-derivation is insufficient
- Provide clear scale descriptions (not just numbers)
- Always offer a shortcut/default for users who don't want to fine-tune
- Batch multiple assessments when possible (max 5 per batch)

---

### Type 3: Override Request

Used when the user wants to override a baseline requirement or dispute a derived test requirement.

**Format:**

```markdown
### Override Request — {Entry ID}: {Test Name}

You've requested to override this requirement.

**Current entry:**
- Source: {Architecture / Baseline}
- Level: {Unit / Integration / System / Acceptance}
- Risk Score: {N} ({bucket})
- Status: Missing

**Why this exists:**
{Brief explanation of why this test was derived — what architectural commitment it verifies or which baseline rule it satisfies}

**To proceed with override, I need:**

1. **Rationale:** Why is this test not needed for your project?
   - Valid reasons: component being deprecated, risk mitigated by other means, covered by broader test, regulatory exception
   - Invalid reasons: time pressure, "too simple", "nobody tests that"

2. **Confirmation:** This will be marked as "Overridden" in the register (retained for audit trail, excluded from coverage calculations).

**Your rationale:** _[awaiting input]_

**Or:** Cancel override (keep requirement active)
```

**Rules:**
- Always explain WHY the requirement exists before accepting an override
- Challenge invalid reasons (per `two-source-model.md` override rules)
- Never delete — mark as Overridden
- Require explicit rationale (no silent overrides)

---

### Type 4: Gate Approval (Strategy Phase)

Used at the end of each strategy stage to confirm outputs before proceeding.

**Format:**

```markdown
### ✓ Stage {N} Complete: {Stage Name}

**Produced:**
- {Summary of what was created/derived in this stage}
- {Key metrics: N entries, N% coverage, etc.}

**Key findings:**
- {Most important finding 1}
- {Most important finding 2}
- {Most important finding 3}

**Saved to:** `.governance/test/{filename}.md`

**Your response:**
- (a) **Approve** — proceed to Stage {N+1}: {next_stage_name}
- (b) **Review detail** — show me the full output before approving
- (c) **Revise** — {specific aspect} needs adjustment
- (d) **Pause** — save state and stop here for now
```

**Rules:**
- Always summarize what was produced (not just "done")
- Show key metrics (counts, percentages, risk highlights)
- Provide path to full detail without forcing user to read everything
- Include pause option (sessions can end at any gate)

---

### Type 5: Coverage Decision

Used when coverage reports reveal gaps and the user needs to decide priorities.

**Format:**

```markdown
### Coverage Gap Decision

Current coverage: **{N}%** ({existing}/{required} tests)

**Critical gaps (immediate attention recommended):**

| # | Commitment | Missing Test | Risk Score | Component |
|---|-----------|-------------|:----------:|-----------|
| 1 | {ID} | {test name} | {score} (Critical) | {component} |
| 2 | {ID} | {test name} | {score} (Critical) | {component} |
| 3 | {ID} | {test name} | {score} (High) | {component} |

**Your decision:**
- (a) **Acknowledge** — I'll address these in priority order during development
- (b) **Override specific items** — some of these aren't needed (I'll ask which)
- (c) **Adjust risk scoring** — my context differs from auto-scoring
- (d) **Generate full debt scorecard** — show me everything ranked
```

**Rules:**
- Lead with CRITICAL gaps (don't bury them in a long list)
- Maximum 5 items in the "immediate attention" table
- Always offer the full scorecard as an option
- Never present coverage gaps as failures — present as risk-informed priorities

---

### Type 6: Observation Event Notification

Used when the observation phase detects a change that requires user awareness (not necessarily a decision).

**Format:**

```markdown
### 👁️ Observation: {Event Type}

**Detected:** {what changed}
**When:** {timestamp}
**Impact:** {what this means for test governance}

**Register update:**
- {N} new test requirements registered
- {N} test statuses updated (Missing → Exists)
- Coverage: {old}% → {new}%

**Action needed?**
- (a) **No action** — updates are correct, continue observing
- (b) **Review changes** — show me the register delta
- (c) **Pause observation** — stop watching until I resume
```

**Rules:**
- Observation notifications are INFORMATIONAL first, decision-requiring second
- Default should be "no action needed" (engine runs autonomously)
- Only escalate to a decision when something unexpected happens
- Keep notifications brief — user can drill in if interested

---

## Batching Rules

### When to Batch

- Risk scoring inputs for related components (max 5 per batch)
- Override requests for related baseline entries (max 3 per batch)
- Coverage gap decisions in the same risk bucket

### When NOT to Batch

- Gate approvals (one per stage — never combined)
- Derivation confirmations involving different AP artifacts (present together but approve separately)
- Override requests involving different reasoning (each needs its own rationale)

### Batch Format

```markdown
## {Batch Title} — {N} Items

The following {items} are related and I'm presenting them together.

---

### Item 1: {description}
{...format per type...}

---

### Item 2: {description}
{...format per type...}

---

**Batch shortcuts:**
- "Approve all" — accept all items as presented
- "Default all" — use default values for all scoring inputs
- "Skip batch" — defer all items to next session
```

---

## User Response Handling

| User Says | Interpretation |
|-----------|---------------|
| "a" or "(a)" | Selected option A |
| "Approve" / "Approve all" | Accept current output; proceed |
| "Looks good" / "Fine" / "Continue" | Approve — proceed to next stage |
| "Show me more" / "Detail" | Display full output (not just summary) |
| "Override {ID}" | Begin override flow for that entry |
| "Use defaults" | Apply default values (3/5) for scoring |
| "Skip" / "Later" / "Pause" | Save state; stop at current point |
| "Why?" / "Explain {X}" | Provide rationale for derivation/scoring of X |
| "That's wrong" / "Remove {X}" | Begin challenge/override flow |
| "Add {X}" | Register a manual entry |
| "Check coverage" | Trigger observation cycle + coverage report |
| Number (1-5) | Risk score input when scoring is active |
| "All 3" / "All medium" | Score all pending factors at 3 |

### Handling "Why is {X} needed?"

This signals the user wants justification. When this happens:
1. Explain the source (which AP artifact or baseline rule produced this requirement)
2. Explain the risk (what could go wrong if this test doesn't exist)
3. Cite similar projects/patterns where this test caught real issues
4. Offer: "Override if this doesn't apply to your context, or keep with adjusted risk score?"
5. Never argue past one explanation — present facts, let user decide

---

## Tone and Communication Style

### Do:
- Be precise about gaps — "API-001 missing contract test for 422 response" not "some API tests are missing"
- Quantify everything — percentages, counts, scores, not vague assessments
- Present data then recommend — "Coverage is 42%. Critical gaps in auth flow. Recommend: address SEC-001 first."
- Acknowledge risk explicitly — "Overriding this accepts {specific risk}. Your call."
- Use risk scoring to justify urgency — scores are evidence, not opinions

### Don't:
- Be alarmist — "Missing tests" ≠ "system will fail." Present risk, not fear.
- Overwhelm with volume — summarize first, detail on request
- Judge the team — low coverage is a STATE, not a FAILURE. Help improve it.
- Present all gaps equally — that's what risk scoring prevents
- Ask questions the architecture already answers — derive, don't ask
- Repeat questions from prior sessions — state file has the answers

---

## Gate vs. Non-Gate Interaction

| Interaction | Requires Approval? | Can Auto-Proceed? |
|------------|:-----------------:|:-----------------:|
| Strategy stage completion | ✅ Yes | No — always wait |
| Observation notification | ❌ No | Yes — inform and continue |
| Override request | ✅ Yes | No — needs rationale |
| Risk scoring input | ✅ Yes (or "use defaults") | Can auto-default if user configured |
| Coverage report generation | ❌ No | Yes — produce and present |
| Reconciliation proposal | ✅ Yes | No — changes need approval |
| Defect logging | ❌ No | Yes — log and continue |
