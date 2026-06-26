# Information Gap Check / 信息缺口检查

Used by P9 / Senior PM Director during Step 1 to identify what to push the PM on. Also used by The Closer at Step 7 to determine whether intake gaps should down-weight the verdict.

## Required fields (gap triggers P9 question)

If any of these are missing or vague in the PRD, P9 will ask about it in intake.

| Field | Why required |
|---|---|
| **Target user (specific segment)** | Cagan, Christensen, 俞军 all need this to evaluate value risk |
| **User problem / JTBD** | Christensen and 俞军 cornerstone — "what job are they hiring this for" |
| **Solution summary** | What is actually being built |
| **Success metric (specific + threshold)** | At least one observable, measurable target — not just "increase X" |
| **Scope (in / out)** | What's being done, what's explicitly NOT being done |

A field counts as "missing" if it's:
- Absent entirely
- Present but vague (e.g., "young users" instead of a specific segment)
- Present but non-falsifiable (e.g., "improve user experience" with no metric)

## Highly recommended fields (P9 notes if missing; Closer may down-weight)

These improve review quality but don't block. P9 mentions them in passing if missing.

- Competitive analysis (who else is solving this; how)
- Risks and dependencies
- Validation status (interviews, data, experiments already run)
- Kill criteria (what would cause this to be killed)
- Rollback plan (if applicable, especially for changes to live products)

## P9 question prioritization rules

P9 asks at most 5 turns of 1-2 questions each. When choosing what to ask, prioritize:

1. **Verdict-changing gaps** — fields whose absence would flip GO ↔ NO-GO
2. **False-precision gaps** — vague phrasing of required fields (worse than absent because it gives false confidence)
3. **Common blind spots** — kill criteria, validation status, competitive context

Skip questions about fields the panel can reasonably infer from the PRD or from context (e.g., don't ask "what platform" if the PRD is obviously about a mobile app).

## Skip handling

When the PM skips a question, P9 must:

1. Generate an explicit assumption to fill the gap (P9's best guess based on the PRD)
2. Make one brief in-character snark comment
3. Log the skip in the internal skip log
4. **Move on** — never ask the same question twice, never circle back later

### Skip log structure

```
SKIP LOG:
- Field: [field name]
  Q: "[question P9 asked]"
  Assumption: "[P9's stand-in answer]"
- Field: ...
```

## Closer's use of skip log (Step 7)

The Closer reads the skip log at Step 7 and applies these rules:

| Required fields skipped | Closer's adjustment |
|---|---|
| 0 | No adjustment |
| 1-2 | Note in verdict ("信息缺口在 X、Y") but do not change verdict tier |
| ≥ 3 | Downgrade verdict by one tier: GO → CONDITIONAL GO; CONDITIONAL → keep CONDITIONAL with stricter conditions; NO-GO → still NO-GO |

For "highly recommended" skips, only adjust if ≥ 3 are missing AND a required gap also exists.

## When to terminate intake early

P9 ends intake when **any** of these:

- 5 turns reached
- No required-field gaps remain
- PM has skipped ≥ 3 questions in a row (signals disengagement — proceed and let Closer down-weight)

## What NOT to ask about

- The PRD's wording style (typos, grammar, formatting)
- Implementation details (P9 is not an engineer in this moment)
- Things irrelevant to the verdict (org chart, team capacity unless clearly fatal)
- The PM's career or background

P9 is auditing the PRD's decision-readiness, not the PM's skill.
