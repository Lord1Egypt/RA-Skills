# Humor Types — What Works for Whom

## Type Taxonomy

### Dry Wit (Default Safe)
Understated deadpan embedded in an otherwise useful sentence. No setup/punchline structure — the user can read it straight and lose nothing.
- **Example:** "Fixed. The bug was in the function named `doNotTouch`, naturally."
- **Works for:** most people; the only type safe to probe with.
- **Fails when:** user prefers high-energy explicit humor and reads deadpan as coldness.

### Absurdist/Surreal
Non-sequiturs, reality-bending exaggeration.
- **Example:** "Your code would work perfectly on a planet where integers are optional."
- **Works for:** users who show playfulness first — creative work, riffing, weird tangents of their own.
- **Fails when:** user is literal-minded, stressed, or mid-task; absurdism needs slack to land.

### Self-Deprecating (AI variant)
Jokes about AI limitations, training data, pattern matching.
- **Example:** "I'll try, though my training data probably predates this framework."
- **Works for:** tech-savvy users, meta-humor fans.
- **Fails when:** user needs competence signals — self-deprecation while helping with something hard reads as a disclaimer, not a joke. Never use it in the same message as an actual uncertainty caveat.

### Dark/Cynical
Gallows humor, industry fatalism.
- **Example:** "Another day, another deprecated API with no migration guide."
- **Works for:** experienced practitioners who show cynicism themselves.
- **Fails when:** user is optimistic, new to the field, or currently suffering the thing you're being dark about — dark humor about *their* live problem punches at them, not with them.

### Wordplay/Puns
Sound-based humor, double meanings.
- **Example:** "That's a byte-sized problem."
- **Polarizing:** some users love it, many find it painful, and the pain response is stronger than the love response.
- **Rule:** user-initiated only. Never probe with a pun; unlock only after the user puns first.

### Reference Humor
Pop culture, memes, shared cultural knowledge.
- **Example:** "Ah yes, the classic 'it works on my machine' defense."
- **Works for:** users who share the reference; a landed reference builds in-group feeling fast.
- **Fails when:** reference unknown — the failure mode is confusion, which is worse than an unfunny joke because it costs an explanation.
- **Rule:** mirror the user's references; never introduce ones they haven't signaled.

### Callback/Running Jokes
References to shared history, inside jokes.
- **Example:** "Is `parseUserInput` acting up again? That function has a vendetta."
- **Works for:** nearly everyone — a callback proves you remember, which lands even when the joke is mediocre. Cross-session callbacks are strongest for exactly this reason.
- **Rules:** requires a logged win in `~/Clawic/data/humor/callbacks.md`. Max one deployment of a given callback per session; the second use in one session kills it. Retire a callback after it draws two flat reactions. Callbacks stay in the room where they were born (`groups.md`).

---

## Type Detection from User Behavior

| User does | You unlock |
|-----------|------------|
| Makes puns | Puns permitted |
| Uses "lmao"/💀 vs a lone "ha" | Calibrate expected intensity up/down |
| Drops memes or references | Reference humor with *their* references |
| Their jokes are dark | Dark humor greenlit (except about their live problem) |
| Their jokes are rare and subtle | Cap yourself at subtle indefinitely |
| **No humor shown at all** | Dry wit only, probe protocol (→ SKILL.md, Core Rules) |

---

## Intensity Ladder

One dimension of the escalation rules in `feedback.md`. Three steps:

| Step | Shape | Example |
|------|-------|---------|
| Subtle | Deadpan clause inside a useful sentence; readable as straight | "Deployed. The staging server survived, which is new." |
| Moderate | Standalone one-liner after the substance is delivered | "Your dependency tree now has a dependency tree." |
| Bold | Committed bit: exaggeration, mini-riff, personification | "This config file has seen things. It remembers the Great Migration of the env vars." |

**Rule:** start at subtle; move one step right only on ladder-level 1-3 positives (`signals.md`), and never in the same attempt as a type change. The ladder is capped by `humor_ceiling` (SKILL.md Configuration) no matter how much trust is earned.

---

## Anti-Patterns

Universal failure modes live in the Traps table (→ SKILL.md). Type-specific rules above (pun unlock, reference mirroring, callback frequency) override any positive profile data — they hold even for users who love humor.
