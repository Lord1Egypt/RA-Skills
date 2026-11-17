<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Question Format Guide

## Purpose

AI-PILC uses structured questions to collect decisions from the user. This document defines the formatting rules, interaction patterns, and logging requirements for all questions asked during the workflow.

---

## Question Types

### Type 1: Decision Question (Multiple Choice)

Used when the workflow needs the user to choose between defined options.

**Format:**

```markdown
### Q-{phase_prefix}-{nn}: {Question Title}

**Context:** {1-2 sentences explaining why this question matters and what depends on the answer}

**Options:**
- (a) {Option A — brief title} — {Description of what this means}
- (b) {Option B — brief title} — {Description of what this means}
- (c) {Option C — brief title} — {Description of what this means}
- (d) {Option D — brief title} — {Description of what this means}

**Recommended:** Option ({x})
**Rationale:** {Why this is the professional recommendation — 1-3 sentences}

**Your Decision:** _[awaiting input]_
```

**Rules:**
- Minimum 2 options, maximum 6 options
- Always include a recommended answer (the AI's professional judgment)
- Always include rationale for the recommendation
- Options should be mutually exclusive and collectively exhaustive
- If "Other/Custom" is a valid choice, include it as the last option

---

### Type 2: Confirmation Question (Yes/No)

Used when the workflow needs approval to proceed or confirmation of a fact.

**Format:**

```markdown
### {Context Statement}

{Brief explanation of what's being confirmed}

**Confirm:** [Yes / No / Need more information]
```

**Rules:**
- Use sparingly — only for gates and simple confirmations
- If the answer could be nuanced, use a Decision Question instead
- Always allow "Need more information" as an escape valve

---

### Type 3: Information Request

Used when the workflow needs factual input from the user (not a choice between options).

**Format:**

```markdown
### {What is needed}

**Why:** {Why this information is needed at this point}

**Format expected:** {What kind of answer — name, number, date, description, list}

**Example:** {An example of a valid answer}

**Your input:** _[awaiting input]_
```

**Rules:**
- Clearly state what format is expected
- Provide an example when the expected input might be ambiguous
- If the user doesn't know yet, accept "[TBD]" and log as an Action Item

---

### Type 4: Review & Approve

Used when presenting a completed deliverable for user review.

**Format:**

```markdown
### Review: {Deliverable Name}

I've produced the {deliverable_name}. Please review:

{Summary of key points — 3-5 bullets highlighting the most important content}

**Full document:** Saved to `{file_path}`

**Your response:**
- (a) **Approve** — Proceed to next stage
- (b) **Request changes** — Tell me what to adjust
- (c) **Major rework** — Significant issues; let's discuss before I revise
- (d) **Skip** — Don't need this deliverable; move on
```

**Rules:**
- Always summarize key points (don't just say "review the file")
- Provide the file path so user can read the full document
- "Request changes" should trigger a follow-up asking what specifically to change
- "Skip" must be logged as a decision with rationale

---

## Question Numbering

Questions are numbered with a phase prefix for traceability:

| Phase | Prefix | Example |
|-------|--------|---------|
| Inception | INC | Q-INC-01 |
| Assessment | ASS | Q-ASS-01 |
| Justification | JUS | Q-JUS-01 |
| Authorization | AUT | Q-AUT-01 |
| Planning | PLN | Q-PLN-01 |
| Mobilization | MOB | Q-MOB-01 |
| Configuration (setup) | CFG | Q-CFG-01 |

**Sequential numbering** within each phase: Q-ASS-01, Q-ASS-02, Q-ASS-03, etc.

---

## Batching Rules

### When to batch questions

- If multiple related questions arise at the same stage, present them together (max 5 per batch)
- Group by topic or dependency
- Number sequentially within the batch

### When NOT to batch

- Questions where the answer to Q1 changes the options for Q2 (sequential dependency)
- Questions from different phases
- Questions with significantly different topics requiring mental context-switching

### Batch format

```markdown
## Questions for Your Input ({n} questions)

The following questions arose during {stage_name}. You can answer them in any order.

---

### Q-{prefix}-{nn}: {Title 1}
{...full question format...}

---

### Q-{prefix}-{nn}: {Title 2}
{...full question format...}

---

### Q-{prefix}-{nn}: {Title 3}
{...full question format...}

---

**Shortcut:** If you agree with all recommendations, reply "Accept all recommendations" and I'll log them accordingly.
```

---

## User Response Handling

### Valid response formats

The AI must accept these response styles:

| User Says | Interpretation |
|-----------|---------------|
| "a" or "(a)" or "option a" | Selected option A |
| "Go with the recommendation" | Accept recommended option |
| "Accept all" | Accept all recommendations in a batch |
| "b, but with a change: {detail}" | Option B with modification — log the modification |
| "None of these — here's what I want: {detail}" | Custom answer — create new option and log |
| "I don't know yet" or "TBD" | Log as pending; create Action Item for follow-up |
| "Skip this" | Skip the question; log decision to skip with reason if given |
| "Come back to this later" | Mark as deferred; proceed; revisit before package assembly |

### Invalid or ambiguous responses

If the user's response is unclear:
1. Do NOT guess or assume
2. Paraphrase what you understood and ask for confirmation
3. Example: "I understood you want Option B but with {X} modified. Is that correct?"

---

## Decision Logging

Every answered question MUST be logged in the Decision Log immediately:

```markdown
| D-{nnn} | {date} | {Decision summary — what was decided} | Stage {n}: {question_title} — Options: {listed}. User chose: {option + any modification} | {Rationale — user's reason or accepted recommendation rationale} | {User / AI recommendation accepted} | {Impact statement} | ✅ Final |
```

### Logging rules

1. Log IMMEDIATELY upon receiving the answer — not at end of stage
2. Include the question context (what was being decided)
3. Record the exact user choice (verbatim if custom)
4. If user accepted recommendation, note "Accepted AI recommendation"
5. If user overrode recommendation, note their stated reason
6. Never summarize or paraphrase the user's words in the log

---

## Deferred Questions

Questions marked as "deferred" or "TBD":

1. Create an Action Item: "Resolve Q-{prefix}-{nn}: {title} — Owner: {user/stakeholder}"
2. Add to state file under "Open Items"
3. Before Package Assembly (Stage 16), present all deferred questions again
4. If still unresolved at assembly → flag in the package as an open item / handoff risk

---

## Tone and Professionalism

### Do:
- Present options neutrally — don't bias language toward the recommendation
- Provide clear, factual rationale (not persuasion)
- Acknowledge that the user may have context the AI doesn't
- Respect "I don't know" as a valid answer

### Don't:
- Ask more than 5 questions in a single interaction without a deliverable in between
- Re-ask a question that's already been answered (check Decision Log)
- Present false urgency ("you MUST decide now")
- Frame recommendations as the only reasonable choice
- Ask questions the source document already answers clearly

---

## Question Dependency Map

Some questions are prerequisites for others:

```
Q-CFG-01 (Output structure) ──► All file creation
Q-INC-01 (Project name) ──► All documents
Q-ASS-01 (Depth level) ──► Determines detail in all subsequent stages
Q-ASS-xx (Clarification answers) ──► Feed into Feasibility scoring
Q-JUS-01 (Solution approach) ──► Shapes Charter scope
Q-AUT-01 (Governance model) ──► Shapes RACI and Communication plan
```

If a dependent question's prerequisite hasn't been answered, either:
- Ask the prerequisite first
- Or proceed with a stated assumption (logged in Assumptions register) and flag for confirmation later
