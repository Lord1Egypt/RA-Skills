<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# AI-UXD — Question Format Guide

**Purpose:** How AI-UXD collects decisions from the user. Defines question types, numbering, response handling, and how answers get logged.

---

## Question Types

### Type 1: Selection (Choose One)

Used when the user must pick from predefined options.

```
Q{stage}.{number}: {Question text}

  [A] {Option A description}
  [B] {Option B description}
  [C] {Option C description}

  Recommended: {letter} — {brief rationale}
```

**Response handling:** Accept letter, full text, or paraphrase. Confirm interpretation if ambiguous.

### Type 2: Confirmation (Yes/No)

Used for binary decisions or gate approvals.

```
Q{stage}.{number}: {Statement to confirm}

  [Y] Approve and proceed
  [N] Request revision — please specify what to change
```

**Response handling:** Accept Y/N, yes/no, approve/revise, thumbs up/down, or equivalent.

### Type 3: Open Input (Free-Form)

Used when the user must provide information that can't be pre-defined.

```
Q{stage}.{number}: {Question text}

  Examples: {2-3 example answers to illustrate scope}
  Format: {expected format — list, paragraph, bullet points}
```

**Response handling:** Accept any format. If the response is unclear or incomplete, ask one follow-up for clarification — never ask more than one follow-up per question.

### Type 4: Multi-Select (Choose Multiple)

Used when multiple options can be selected simultaneously.

```
Q{stage}.{number}: {Question text} (select all that apply)

  □ {Option 1}
  □ {Option 2}
  □ {Option 3}
  □ {Option 4}

  Minimum: {N} | Maximum: {N or "no limit"}
```

**Response handling:** Accept comma-separated letters, numbers, or option text.

### Type 5: Ranked (Priority Order)

Used when the order matters (prioritization).

```
Q{stage}.{number}: {Question text} — rank from most to least important:

  • {Item A}
  • {Item B}
  • {Item C}
  • {Item D}
```

**Response handling:** Accept numbered list, comma-separated in order, or "A > B > C > D" format.

---

## Numbering Convention

Questions are numbered as `Q{stage}.{sequence}`:
- `Q1.1` = Stage 1, Question 1
- `Q3.4` = Stage 3, Question 4
- `Q8.2` = Stage 8, Question 2

Within a stage, questions are numbered sequentially starting from 1.

---

## Presentation Rules

1. **Batch related questions** — present 2-4 related questions together, never more than 5 at once
2. **Context before question** — briefly explain WHY the question matters before asking it
3. **Show the implication** — state what the answer affects ("This determines which personas we'll define")
4. **Offer a recommendation** — when professional judgment suggests a default, state it with rationale
5. **Never block on perfection** — if the user is uncertain, offer to proceed with a reasonable default and revise later

---

## Response Handling

### Unambiguous Response
Accept immediately. Log the decision. Proceed.

### Ambiguous Response
Reflect back: "I understood that as {interpretation}. Is that correct?"
- If confirmed → log and proceed
- If corrected → accept correction, log, proceed

### "I Don't Know" Response
Offer:
1. A professional recommendation with rationale
2. The option to defer ("We can decide this at Stage {N} when we have more context")
3. A safe default that can be revised

### Multiple Questions, Partial Response
If user answers some questions but not others:
- Acknowledge what was answered
- Re-present only the unanswered questions
- Never re-ask questions already answered

---

## Decision Logging

Every decision that affects the design is logged in one of two places:

### In the Stage Artifact
Questions whose answers directly become content in the deliverable (e.g., "What are the primary user types?" → becomes the persona list).

### In the Decision Log
Questions whose answers represent a design judgment call that could have gone differently (e.g., "8px grid vs. 4px grid" → logged as `UXD-D-NNN` in the management framework).

**Logging format:**
```markdown
| ID | Decision | Rationale | Stage | Date |
|----|----------|-----------|-------|------|
| UXD-D-001 | 8px spatial grid | Balances flexibility with consistency; 4px too fine for this team's maturity | 8 | {date} |
```

---

## Depth Adaptation of Questions

| Depth | Question Behavior |
|-------|-------------------|
| **Minimal** | Fewer questions; accept defaults more readily; batch aggressively |
| **Standard** | Full question set; balanced defaults and choices |
| **Comprehensive** | Extended questions; probe deeper; fewer assumptions |

---

## Special Cases

### Brownfield Mode (Mode D)
Questions shift from "What do you want?" to "What exists? What works? What should change?"
- Present findings first, then ask for confirmation/direction
- Default to preserving existing decisions unless user explicitly overrides

### Chain Mode with Predecessor Data (Mode A/B)
Some questions are PRE-ANSWERED by PIP/AP data:
- Present the extracted answer: "Based on the PIP, your primary user types are: {list}. Use these as the persona foundation? [Y/Adjust]"
- If user adjusts → log the override as a decision

---

*Part of AI-UXD v1.0.0 | Reference: core-workflow.md § Checkpoint Enforcement*
