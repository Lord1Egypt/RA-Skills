<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# AI-ILC — Question Format Guide

**Purpose:** Define how AI-ILC collects decisions from the user. Consistent formatting ensures every decision is clear, traceable, and immediately loggable in the Decision Log.

---

## Question Format (Standard)

Every structured question follows this format:

```markdown
### Q-{nn}: {Question Title}

**Context:** {Why this question matters — one or two sentences}

**Options:**
- (a) {Option A description}
- (b) {Option B description}
- (c) {Option C description}

**Recommended:** Option {x}
**Rationale:** {Why this is recommended — evidence-based, not opinion}

**Your Decision:** _[awaiting input]_
```

---

## Rules

### Numbering
- Questions are numbered sequentially per idea: Q-01, Q-02, Q-03...
- Numbering resets for each new idea (not global across the register)
- The number persists — if Q-03 is asked, it is always Q-03 for that idea, even if revisited

### Always Provide a Recommendation
- NEVER present options without a recommended answer
- The recommendation must include a rationale (why this option over others)
- The rationale must be grounded in facts from the shaping/evaluation — not generic advice
- If genuinely no preference exists (all options equally valid), state that explicitly and explain why

### User Response Handling
The user can respond in any of these ways:

| Response | Action |
|----------|--------|
| Accept recommendation (e.g., "go with a", "yes", "agreed") | Log decision as the recommended option |
| Choose a different option (e.g., "b", "option c") | Log decision as the chosen option |
| Propose an alternative not listed | Log as a custom decision; capture the full response |
| Ask for more context | Provide additional detail; do NOT log yet |
| Defer (e.g., "later", "park this question") | Log as pending in state file; revisit before stage completion |
| Batch response (e.g., "Q-01: a, Q-02: b, Q-03: c") | Log each decision individually |

### Logging
- Every answered question is logged in the **Decision Log** immediately
- Log format: `D-{nn} | {date} | Q-{nn} | {decision summary} | {rationale}`
- Pending questions are tracked in `ilc-state.md` → Pending Decisions section
- A stage CANNOT complete with unresolved pending decisions (gate enforcement)

---

## Question Types by Stage

| Stage | Typical Questions | Count (approx.) |
|-------|------------------|:---------------:|
| **Capture** | Output folder preference, depth confirmation | 1–2 |
| **Shape** | Problem clarity, beneficiary, boundaries, domain | 3–5 |
| **Evaluate** | Score challenges, threshold overrides | 0–2 (only if scores are borderline) |
| **Scope** | In/out decisions, effort agreement, deferral rationale | 2–4 |
| **Approve** | Go/no-go decision, conditions, revisit date (if parking) | 1–2 |
| **Route & Handoff** | Project existence, impact assessment, routing confirmation | 2–3 |

---

## Depth Adaptation

| Depth | Question Behavior |
|-------|-------------------|
| **Minimal** | Fewer questions; combine related decisions into one; accept defaults more readily |
| **Standard** | Full question set per stage; each decision explicit |
| **Comprehensive** | Additional probing questions; challenge assumptions; request stakeholder input |

---

## Quick-Fire Format (for low-ceremony moments)

When the decision is simple and binary, use a lighter format:

```markdown
**Q-{nn}: {Title}** — {one-line context}
→ Recommended: {option}. Agree? [Yes / No / Adjust]
```

Use quick-fire for:
- Confirming depth level
- Accepting a recommended score
- Confirming "start fresh" vs. "resume"

Do NOT use quick-fire for:
- Go/no-go decisions (always full format)
- Routing decisions (always full format)
- Any decision that changes scope or direction

---

## Anti-Patterns

| Don't | Why |
|-------|-----|
| Ask open-ended questions without options | User has to think too hard; slows the pipeline |
| Present more than 5 options | Decision fatigue; synthesize to 3-4 meaningful choices |
| Skip the recommendation | User lacks context to choose; your job is to advise |
| Ask multiple unrelated questions in one block | Each decision must be individually loggable |
| Log a decision without user confirmation | The user decides, never the AI |
| Re-ask an already-answered question | Check state file first; reference the existing decision |

---

## Batch Presentation

When a stage has 3+ questions that are conceptually related, present them together as a numbered batch:

```markdown
## Shaping Questions (Q-03 through Q-06)

### Q-03: {Title}
{full format}

### Q-04: {Title}
{full format}

### Q-05: {Title}
{full format}

### Q-06: {Title}
{full format}

---
You can answer individually or batch: "Q-03: a, Q-04: b, Q-05: c, Q-06: a"
```

This allows the user to respond in one message rather than multiple round-trips.

---

*Version: 1.0.0 | Part of AI-ILC — AI-Driven Idea Life Cycle*
