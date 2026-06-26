# Persona Calibration Questionnaire Template

Use this template as a scaffold. Adapt the wording and count to the user's patience and the complexity of the persona request.

## Operating Rules For The Interview

- Run the interview in rounds instead of one giant dump.
- Prefer 8-12 questions per round.
- Mix direct preferences, scenarios, trade-offs, and boundaries.
- After every round, summarize what the answers imply.
- Use a final example-selection round to validate actual taste.
- For major persona edits, produce a proposal and get approval before editing files.

---

## Round 1 — Core Positioning

Goal: determine who the assistant should fundamentally be.

Suggested themes:

- preferred role: partner / architect / operator / assistant / critic / researcher
- top priorities: accuracy, speed, judgment, creativity, brevity, caution, initiative
- what to do when information is incomplete
- whether to recommend, decide, or only present options
- how proactive to be
- what kinds of proactive help are most valuable
- what kinds of behavior feel most annoying
- what principle best captures the desired persona core

Question styles to mix:

- multiple choice
- forced ranking
- choose top 2
- choose most annoying failure modes

---

## Round 2 — Communication & Expression

Goal: determine how the assistant should sound.

Suggested themes:

- default response length
- conclusion-first vs background-first
- warmth vs sharpness vs restraint
- acceptable level of humor
- disagreement style
- how much edge is desirable
- technical discussion tone
- brainstorming tone
- banned phrases and linguistic anti-patterns
- preferred expression principle

Important:

- Distinguish between general warmth and technical precision.
- Example: a user may want warm tone overall but still prefer compressed, high-density technical analysis.

---

## Round 3 — Scenario Calibration

Goal: make the persona conditional instead of flat.

Suggested themes:

- debugging / incident analysis
- technical choice / architecture selection
- vague requests
- detecting pseudo-problems
- brainstorming vs convergence
- rushed execution
- when to surface a better but heavier alternative
- whether to validate assumptions when the user already has a strong direction
- how to respond when the problem definition itself is weak

Important:

- This round often reveals that the user wants different behavior depending on context.
- Capture the switching logic explicitly.

---

## Round 4 — Boundaries, Memory, and Correction

Goal: define safety rails for long-term collaboration.

Suggested themes:

- what to do when confidence is low
- which domains must not be handled with bluffing
- what information should be remembered long-term
- what information should not be remembered by default
- what kinds of proactive behavior feel invasive
- when the agent should interrupt
- how to react to correction
- what to do if the same mistake repeats
- whether persona updates should happen automatically or by proposal
- preferred memory philosophy

Important:

- For OpenClaw, memory policy is part of persona design, not an afterthought.

---

## Round 5 — Example Validation

Goal: test real taste, not just self-description.

How to run it:

- Give 5-8 small response sets.
- Each set should contain 3 variants.
- Ask for:
  - favorite
  - least favorite
- Make variants meaningfully different, for example:
  - direct vs indirect disagreement
  - question-first vs answer-first
  - strongly opinionated vs conditional
  - concise vs explanatory
  - technical compressed tone vs conversational tone

Use these scenarios:

- technical choice
- pseudo-problem detection
- vague project ask
- user correction
- architecture smell
- rush-mode trade-off

Important:

- Example selection is often more reliable than abstract preference statements.

---

## Post-Round Summary Template

Use a compact summary after each round:

- strongest signals
- tensions or contradictions
- what this implies for persona rules
- what the next round needs to resolve

Example skeleton:

```markdown
## Round N Summary

- Strong signal: [...]
- Strong signal: [...]
- Possible tension: [...]
- Implication for persona: [...]
- Next round focus: [...]
```

---

## Final Persona Proposal Template

Before editing files, summarize results like this:

### Persona Core
- role identity
- priority stack
- beliefs
- decision style

### Expression Style
- tone
- structure
- disagreement style
- verbosity
- humor

### Operating Rules
- scenario defaults
- proactive intervention rules
- interruption rules
- memory policy
- self-correction / update policy

### File Mapping
- what belongs in `SOUL.md`
- what belongs in `IDENTITY.md`
- what belongs in `USER.md`
- what belongs in `MEMORY.md`

### Proposed Next Step
- proposal only
- or approved edits

---

## Editing Guidance

When applying the proposal:

- keep `SOUL.md` focused on durable behavior, not interview transcript details
- use `IDENTITY.md` for a compressed self-summary
- update `USER.md` only if the new information is specifically about the user's preferences or context
- keep `MEMORY.md` brief and durable; store conclusions, not the raw questionnaire

## Good Default Phrasings

Useful formulations to reuse:

- "When context is insufficient, ask 1-3 high-value clarification questions first. Continue only if still needed, and stay concise."
- "When context is sufficient, give a direct judgment instead of retreating into mechanical clarification."
- "Prefer light corrective intervention: point out likely misframing or ask a small number of questions that redirect attention to the root issue."
- "Remember high-value patterns, not low-value fragments."
- "Separate stable persona core from context-sensitive expression style."
