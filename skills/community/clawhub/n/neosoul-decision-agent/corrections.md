# Decision Reversals Log — Template

> This file is created in `~/decision-making/reversals.md` when you first use the skill.
> Keeps a running log of overturned decisions and the lessons extracted.
> Replaces the original `corrections.md` — the equivalent of corrections for decision-making is a reversal.

## Example Entries

```markdown
# Decision Reversals Log

## 2026-03-20

### 14:32 — Tech / Strategic
- **Decision reversed:** Chose PostgreSQL over SQLite for the MVP
- **Why overturned:** Storage and infra overhead was too high at early scale
- **Lesson:** For MVPs with < 1000 users, SQLite is sufficient; revisit at scale
- **Domain lesson added:** domains/tech.md — "MVP storage: default SQLite, revisit at 1k users"
- **Count:** 1 (first occurrence of this type)

## 2026-03-15

### 09:15 — Product / Tactical  
- **Decision reversed:** Shipped feature X without user research
- **Why overturned:** User adoption was 4%, far below expectations
- **Lesson:** For product features affecting onboarding, always require ≥5 user interviews first
- **Domain lesson added:** domains/product.md — "onboarding-impacting features: require ≥5 interviews"
- **Count:** 2 (second occurrence — watch for 3rd to confirm pattern)
```

## Log Format

Each entry includes:
- **Timestamp** — When the reversal was acknowledged
- **Domain + Type** — Which namespace this belongs to
- **Decision reversed** — What was originally decided
- **Why overturned** — The actual cause (user-stated, not inferred)
- **Lesson** — The extracted reusable rule
- **Domain lesson added** — Whether it was written to a WARM file (and where)
- **Count** — How many times this type of reversal has occurred (for pattern promotion)

## Reversal Types

| Type | Example | Namespace |
|------|---------|-----------|
| Framework mismatch | "We used Pros/Cons but needed a matrix" | global or domain |
| Weight error | "We prioritized speed over quality — wrong call" | domain |
| Missing factor | "We didn't consider exit cost" | domain or type |
| Timing error | "Decided too fast without enough data" | global |
| Scope creep | "What we thought was tactical was actually strategic" | type |
| Assumption failure | "Our cost assumption was off by 3×" | domain |

## Pattern Promotion

After 3 similar reversals of the same type:
```
Agent: "I've noticed a recurring pattern: [description] has led to a reversal 3 times.
        Should I add this as a standing rule to your [domain] decision patterns?
        - Yes, add to domains/{domain}.md
        - Yes, add to memory.md (global)
        - No, keep case by case"
```
