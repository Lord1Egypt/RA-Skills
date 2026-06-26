# Decision Signals

What triggers learning, how to classify it, and where to store it.

---

## Signal Taxonomy

### Risk Profile Signals → `memory.md`

| Signal | Example Phrase | What to Record |
|--------|---------------|----------------|
| Risk-averse | "I'd rather wait for more data" | `risk: conservative` |
| Risk-tolerant | "Let's just try it and see" | `risk: experimental` |
| Loss-averse | "Worst case, what happens if this fails?" | `risk: loss-focused` |
| Regret-driven | "I don't want to look back and regret this" | `risk: regret-minimizing` |
| Speed-over-precision | "Speed matters more than getting it perfect" | `risk: bias-to-action` |
| Reversibility-first | "Can we undo this if it goes wrong?" | `risk: reversibility-sensitive` |

> Do not infer risk profile from a single decision. Wait for 3 consistent signals before writing to memory.md.

---

### Framework Preference Signals → `memory.md` + `frameworks.md`

| Signal | Example Phrase | What to Record |
|--------|---------------|----------------|
| Wants structure | "Give me a structured analysis" | `framework-pref: structured` |
| Wants brevity | "Just give me your top recommendation" | `framework-pref: direct` |
| Wants matrices | "I like scoring things" | `framework: Decision Matrix` |
| Wants thinking partner | "Walk me through the tradeoffs" | `framework-pref: dialogue` |
| Wants stress-testing | "What are the worst-case scenarios?" | `framework: Pre-mortem` |
| Wants long-term view | "What are the downstream effects?" | `framework: Second-Order Thinking` |

---

### Domain Weight Signals → `domains/{domain}.md`

| Signal | Example Phrase | What to Record |
|--------|---------------|----------------|
| Quality > speed (product) | "Ship slow, ship right" | `weight: quality > speed` |
| Speed > quality (ops) | "We need to decide today" | `weight: speed > quality` |
| Reversibility matters (tech) | "Don't paint us into a corner" | `weight: reversibility` |
| Cost-sensitivity (business) | "Budget is the hard constraint" | `weight: cost-constrained` |
| User-centric (product) | "The user always breaks the tie" | `weight: user-first` |

---

### Outcome Feedback Signals → `reversals.md` or decision record

| Signal | Example Phrase | What to Record |
|--------|---------------|----------------|
| Confirmed good | "That was the right call" / "Glad we did that" | Append `outcome: good` to decision record |
| Confirmed bad | "That was a mistake" / "We should not have done that" | Append `outcome: bad`, trigger retrospective |
| Partial | "Mostly right, but we underestimated X" | Append `outcome: partial`, note specific miss |
| Regret | "In hindsight, we should have..." | Log lesson to `reversals.md` |

---

## What Does NOT Trigger Learning

- **Silence** — not a signal of approval or agreement
- **Hypotheticals** — "what if we had done X" does not update risk profile
- **Single-instance decisions** — one choice under unusual constraint is not a preference
- **Third-party preferences** — "my manager thinks X" is not the user's preference
- **Emotional expressions** — "I hate this situation" is not a risk signal
- **Group chat patterns** — do not infer from decisions made in team contexts

---

## Confidence Level Tagging

Every decision analysis must be tagged with a confidence level. Apply automatically:

| Level | Label | When to Use |
|-------|-------|-------------|
| 🟢 | **High** | Sufficient context, clear domain match, user has stated key constraints |
| 🟡 | **Medium** | Assumptions made, 1–2 key inputs missing, domain match partial |
| 🔴 | **Low** | Major unknowns, no domain context loaded, user hasn't confirmed constraints |

State the label at the top of any decision output:
```
Confidence: 🟡 Medium — I'm assuming budget is flexible and timeline is 3 months.
Please correct these if inaccurate.
```

---

## Signal Confirmation Flow

After 3 signals of the same type:

```
Agent: "I've noticed you consistently prefer X over Y
        (observed 3 times across [domain] decisions).
        Should I treat this as your default for [domain]?
        - Yes, always apply this in [domain]
        - Yes, apply this globally
        - No, handle case by case"

User: "Yes, apply globally"

Agent: → Moves to HOT memory.md as confirmed preference
       → Removes from signal counter
       → Cites source on next use: "Using [preference] (memory.md:12)"
```

---

## Signal Classification by Scope

```
Global: applies to all decisions
  └── Domain: applies to product / tech / business / personal
       └── Type: applies to strategic / tactical / operational
            └── One-time: applies to this decision only (never log)
```

When scope is unclear, ask:
```
"Should [preference] apply only to [detected domain] decisions,
or everywhere?"
```

---

## Anti-Patterns

### Never Learn
- What makes the user agree faster (manipulation)
- Emotional vulnerabilities or stress patterns
- Patterns from other people's decisions shared in context
- Inferences from non-explicit behavior

### Avoid
- Generalizing risk profile from high-pressure decisions (constraints skew behavior)
- Over-indexing on recency (last decision ≠ always right rule)
- Applying domain weight to wrong domain silently
- Confirming a preference without asking after 3 signals

---

## Quality Signals

### Good Signal
- User explicitly stated a preference or style
- Same signal appeared in ≥3 independent contexts
- Signal is about process, not a one-time constraint
- User confirmed when asked

### Bad Signal
- Inferred from silence or compliance
- Only appeared under pressure or time constraint
- Contradicts recent explicit statement
- User never confirmed
