# Decision Frameworks

This file is the **framework index**. It does NOT store step-by-step instructions — the agent generates those at runtime. It stores which frameworks exist, when to reach for them, and what the user prefers.

---

## Framework Registry

| Framework | Best For | Decision Type | Stakes Level | User Preference |
|-----------|----------|---------------|--------------|-----------------|
| **Pros / Cons** | Simple binary choices | Any | Low–Medium | — |
| **Decision Matrix** | Multi-criteria, multiple options | Tactical / Operational | Medium | — |
| **MECE Tree** | Decomposing complex problem space | Strategic | High | — |
| **Pre-mortem** | Stress-testing a plan before committing | Strategic / Tactical | High | — |
| **10 / 10 / 10** | Personal decisions with emotional weight | Personal | Any | — |
| **Second-Order Thinking** | Long-term consequence mapping | Strategic | High | — |
| **OODA Loop** | Fast-moving, iterative, time-pressured | Tactical / Operational | Variable | — |
| **Cost of Delay** | Prioritization across competing options | Product / Tech | Medium–High | — |
| **Reversibility Test** | Deciding how much analysis a decision warrants | Any | Any | — |
| **Weighted Scoring** | Quantifying qualitative tradeoffs | Tactical | Medium | — |
| **Devil's Advocate** | Challenging an already-leaning conclusion | Any | High | — |
| **Regret Minimization** | Long-horizon personal or career decisions | Personal / Strategic | High | — |

---

## Domain → Framework Defaults

> Populated from user signals. Initial values are reasonable defaults; update after 3 confirmed signals.

| Domain | Default Framework | Fallback |
|--------|------------------|---------|
| Product | Decision Matrix | Pros / Cons |
| Tech | Reversibility Test → Decision Matrix | MECE Tree |
| Business | Second-Order Thinking | Weighted Scoring |
| Personal | 10 / 10 / 10 | Regret Minimization |

---

## Type → Framework Defaults

| Decision Type | Preferred Depth | Default Framework |
|---------------|----------------|------------------|
| Strategic | Full analysis, surface long-term effects | MECE Tree → Second-Order |
| Tactical | Structured but efficient | Decision Matrix |
| Operational | Fast, minimal friction | Pros / Cons or OODA |

---

## User Framework Preferences (Learned)

> This section is written by the agent from decision signals. Do not edit manually.

```markdown
## Preferences
(empty until learned)

## Anti-preferences (frameworks user dislikes or finds slow)
(empty until learned)

## Context overrides
(e.g., "never use weighted scoring for personal decisions")
```

---

## Framework Selection Logic

When a user asks for help deciding, follow this priority:
1. Check HOT `memory.md` for explicit framework preference
2. Match domain → see Domain Defaults above
3. Match decision type (strategic / tactical / operational) → see Type Defaults
4. If ambiguous, default to **Pros / Cons** and offer to go deeper

Always state which framework you're using and why:
```
"I'll use a Decision Matrix here — you're comparing 3 options across 4 criteria,
and your past product decisions have responded well to structured scoring."
```

---

## Confidence-Enhancing Add-ons

After the main framework, consider adding one of these if stakes are high:

| Add-on | When | Trigger |
|--------|------|---------|
| Pre-mortem | After a recommendation, before commitment | Stakes = High |
| Devil's Advocate | When user seems already decided | Confirmation bias risk |
| Second-Order Check | After tactical decision with long-term effects | Domain = Business / Strategic |

---

## Framework Decay

If a framework has not been used or referenced in 90 days, move domain/type defaults to archive and reset the preference to neutral. Do not delete — archive with timestamp.
