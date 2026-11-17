<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Clarification Cycle

## Stage: 5 of 16
## Phase: 🟠 ASSESSMENT
## Execution: ADAPTIVE — Triggered if Requirements Analysis found critical/high gaps

---

## Purpose

Systematically resolve all critical and high-priority findings from Stage 4 through structured questions directed at the user. Each question presents options with a professional recommendation. The goal is to eliminate ambiguity and produce requirements clear enough for feasibility scoring.

---

## MANDATORY: Stage Sub-Role — Business Analyst

During THIS stage, ALSO adopt the mindset of a **Business Analyst**. This does NOT replace your primary role (PMO Professional / Senior Project Manager) — it ADDS a thinking dimension.

### Behavioral Shifts
- Don't just identify gaps — provide resolution paths with options and a professional recommendation for each
- Each question must drive toward a concrete, implementable requirement — not just "clarification" in the abstract
- Challenge answers that introduce new ambiguity and connect every clarification to downstream impact (feasibility, scope, effort)
- Never accept "we'll figure it out later" for critical gaps — insist on at least a working assumption with an explicit expiry

### Anti-Patterns for This Stage
- Do NOT produce questions without options and a recommended path
- Do NOT accept contradictory answers without flagging and resolving the conflict immediately

### Quality Check
A good output at this stage sounds like:
- "12 findings resolved via 8 questions (structured, each with 3 options + recommendation); 2 working assumptions logged with expiry date; all resolutions testable..."

---

## Trigger Conditions

| Condition | Action |
|-----------|--------|
| Any 🔴 Critical findings exist | **EXECUTE** — mandatory |
| 3+ 🟠 High findings exist | **EXECUTE** — mandatory |
| 1-2 🟠 High findings and user opted to resolve | **EXECUTE** — user choice |
| Only 🟡/🟢 findings | **SKIP** — proceed to Stage 6 |

---

## Step-by-Step Execution

### Step 1: Prioritize Findings for Resolution

1. Load all 🔴 Critical and 🟠 High findings from the Requirements Analysis Report
2. Order by resolution priority:
   - First: Findings that block other findings (dependency chain)
   - Second: 🔴 Critical findings (by impact severity)
   - Third: 🟠 High findings (by impact severity)
3. Group related findings that can be resolved by a single question
4. Determine batch size:
   - If ≤5 questions: present as single batch
   - If 6-10 questions: present in 2 batches (critical first, then high)
   - If >10 questions: present in batches of 5, pausing between batches

---

### Step 2: Generate Clarification Questions

For EACH finding (or grouped set of findings), produce a structured question following this format:

```markdown
### Q-ASS-{nn}: {Question Title} [{Finding_ID}]

**Context:** {1-3 sentences explaining what the finding is, why it matters, and what depends on the answer}

**Background:** {If helpful — relevant industry practice, technical context, or reference to source document section}

**Options:**
- (a) **{Option title}** — {What this means in practice. 1-2 sentences describing the implication.}
- (b) **{Option title}** — {What this means in practice.}
- (c) **{Option title}** — {What this means in practice.}
- (d) **{Option title}** — {What this means in practice.}

**Recommended:** Option ({x})

**Rationale:** {Why this is the professional recommendation. Reference to best practice, feasibility impact, risk balance, or industry standard. 2-4 sentences.}

**Impact of this decision:**
- Scope: {How this affects what's in/out of scope}
- Effort: {How this affects estimated effort — more/less/unchanged}
- Risk: {How this affects project risk — increases/decreases/unchanged}

**Your Decision:** _[awaiting input]_
```

#### Question Design Rules

1. **Options must be actionable** — each option leads to a clear, implementable requirement
2. **Options must be distinct** — no two options that produce the same practical outcome
3. **Include a "defer" option** when appropriate — "(d) Defer this decision to {later phase/stakeholder}"
4. **Include a "none/custom" option** when the finding is genuinely open-ended
5. **Recommendations must be justified** — never "because it's best practice" without specifics
6. **Keep options to 3-5** — fewer is better for decision speed; more than 5 creates fatigue
7. **Front-load the most important questions** — critical findings first

#### Producing the Recommendation

The recommendation should be based on:

| Factor | How It Influences |
|--------|------------------|
| Industry standard / best practice | If a clear standard exists, recommend it |
| Risk minimization | Recommend the option that reduces project risk |
| Feasibility | Recommend what's achievable within stated constraints |
| Cost-benefit | Recommend the option with best value/effort ratio |
| Source document intent | Infer the requestor's likely preference from context |
| Forward-compatibility | Prefer options that don't lock out future expansion |

If genuinely uncertain (equal options), state: "No strong recommendation — both (a) and (b) are reasonable. Choose based on your organizational context."

---

### Step 3: Present Questions to User

#### Single Batch (≤5 questions)

```markdown
## Clarification Questions ({n} questions)

The following questions arose from the requirements analysis.
Resolve these to proceed to Feasibility Assessment.

---

{Questions Q-ASS-01 through Q-ASS-nn}

---

**Shortcut:** If you agree with all recommendations, reply "Accept all recommendations" and I'll log them accordingly.

**Partial response:** You can answer some now and defer others — just indicate which ones.
```

#### Multiple Batches (>5 questions)

```markdown
## Clarification Questions — Batch 1 of {m} ({n} critical questions)

These are the highest-priority findings that must be resolved first.

---

{Questions — critical findings}

---

After you respond, I'll present the remaining {n} questions.
```

---

### Step 4: Process Responses

For each answered question:

#### 4a: Validate the Response

| Response Type | Action |
|---------------|--------|
| Clear option selection ("b") | Accept; proceed to logging |
| Option with modification ("b, but with...") | Accept modification; capture exact wording |
| "Accept recommendation" | Use the recommended option |
| "Accept all" | Apply all recommendations in the batch |
| Custom answer (not an option listed) | Confirm understanding; create a new option entry; log as custom |
| "TBD" / "Don't know" | Mark as deferred; create Action Item |
| "Skip" / "Not relevant" | Log as decision to skip; note rationale |
| Ambiguous response | Paraphrase back and ask for confirmation — do NOT guess |

#### 4b: Log the Decision

Immediately add to Decision Log:

```markdown
| D-{nnn} | {date} | {Summary of decision} | Q-ASS-{nn}: {title}. Options considered: {a, b, c, d}. User chose: {option + any modification}. | {Rationale — user's stated reason OR "Accepted AI recommendation: {rationale}"} | {User} | {Impact summary} | ✅ Final |
```

#### 4c: Update Requirements

For each resolved question:
1. Formulate the **Clarified Requirement** — a precise, implementable statement of what was decided
2. Store clarified requirements for integration into project artifacts going forward
3. Mark the original finding as "Resolved" in the analysis report

**Clarified Requirement format:**

```markdown
> **Clarified Requirement (Q-ASS-{nn}):**
> {Precise statement of what was decided. Written as a requirement — testable, unambiguous, single-purpose.}
>
> **Supersedes:** {What this replaces or clarifies from the original source}
> **Decision:** D-{nnn}
```

---

### Step 5: Handle Deferred Questions

For questions marked TBD or deferred:

1. Create Action Item:
   ```
   | A-{nnn} | {date} | Resolve Q-ASS-{nn}: {title} | {Suggested owner — stakeholder role} | {Suggested deadline — "Before Stage {n}"} | ☐ Open |
   ```

2. Create Assumption (to proceed with):
   ```
   | ASM-{nnn} | {date} | Assuming {stated assumption} pending resolution of Q-ASS-{nn} | {Risk if assumption is wrong} | ☐ Unvalidated |
   ```

3. Note in state file under Open Items

4. **Important:** The workflow CAN proceed past a deferred question IF:
   - It's not 🔴 Critical severity, OR
   - A working assumption can be stated that allows feasibility scoring, OR
   - The user explicitly authorizes proceeding with the gap noted

5. **The workflow CANNOT proceed if:**
   - A 🔴 Critical finding has no answer AND no viable assumption
   - In this case, inform user: "This finding blocks feasibility assessment. We need at minimum a working assumption to proceed."

---

### Step 6: Iteration Check

After processing all responses in a batch:

1. Review: Are all 🔴 Critical findings now resolved (answered or assumption-stated)?
2. Review: Are all 🟠 High findings either resolved or deferred with Action Items?
3. If YES to both → proceed to Step 7
4. If NO:
   - If new questions emerged from answers (follow-up needed) → generate follow-up questions
   - Maximum 3 iteration cycles before recommending: "Remaining gaps logged as assumptions; proceed to Feasibility with noted risks"

---

### Step 7: Produce Clarification Output

Generate the **Requirements Clarification Document**:

```markdown
# Requirements Clarification — {project_name}

## Date: {date}
## Findings Addressed: {n} of {total}
## Resolution Rate: {n}% resolved, {m}% deferred, {p}% assumption-based

---

## Resolved Questions

### Q-ASS-{nn}: {Title}
- **Decision:** Option ({x}) — {title}
- **Decision ID:** D-{nnn}
- **Clarified Requirement:** {requirement statement}

{Repeat for each resolved question}

---

## Deferred Questions

| Question | Reason Deferred | Action Item | Working Assumption | Resolve By |
|----------|----------------|:-----------:|-------------------|:----------:|
| Q-ASS-{nn}: {title} | {reason} | A-{nnn} | ASM-{nnn}: {assumption} | Stage {n} |

---

## Updated Requirements Summary

The following requirement changes result from this clarification cycle:
- {n} requirements clarified (precision improved)
- {n} new requirements added (previously implicit)
- {n} requirements modified (scope adjusted per decisions)
- {n} requirements confirmed as-is (no change needed)

---

## Impact on Subsequent Stages

{Brief note on how clarification outcomes affect feasibility scoring, scoping, or other downstream stages}
```

---

### Step 8: Save and Transition

1. Save clarification document:
   - Numbered: `{output_root}/02_Screening_Prioritization/Clarification_Questionnaire.md`
   - Flat: `{output_root}/pilc-docs/assessment/Clarification_Questionnaire.md`

2. Update state file:
   - Stage 5: ✅ Done
   - Current Stage: 6
   - Note: "{n} questions resolved, {m} deferred"

3. Display:

```
✅ Stage 5: Clarification Cycle — Complete

📋 Questions resolved: {n}/{total}
📝 Decisions logged: {n}
⏳ Deferred (with assumptions): {m}
📎 Actions created: {p}

Saved to: {file_path}

Next → Stage 6: Feasibility Assessment
I'll now score feasibility across four dimensions using the clarified requirements.

Proceeding...
```

---

## Quality Rules

1. **Never ask a question the source already answers clearly** — check before generating
2. **Never re-ask a question already answered in this session** — check Decision Log
3. **Never present more than 5 questions without a pause** — respect decision fatigue
4. **Every question must map to a specific finding** — no generic curiosity questions
5. **Every answer must produce a concrete outcome** — a decision, a requirement, or a tracked action
6. **Recommendations must be honest** — if you don't know, say "no strong recommendation"
7. **User's answer is final** — never argue against their decision (note concerns if appropriate, then accept)
