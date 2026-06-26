# HOT Memory — Template

> This file is created in `~/decision-making/memory.md` when you first use the skill.
> Keep it ≤100 lines. Risk profile, framework preferences, and confirmed rules live here.

## Example Entries

```markdown
# Decision Making Memory (HOT Tier)

## Risk Profile
- risk-tolerance: conservative               # conservative / experimental / context-dependent
- regret-style: regret-minimizing            # regret-minimizing / opportunity-seeking
- uncertainty-response: data-first           # data-first / bias-to-action
- reversibility: high priority               # high priority / low priority / domain-dependent

## Framework Preferences
- default: Decision Matrix
- personal decisions: 10/10/10
- high-stakes add-on: Pre-mortem
- output style: structured (not conversational)  # structured / dialogue / direct-recommendation

## Domain Weights
- product: quality > speed; user feedback breaks ties
- tech: reversibility > performance > speed
- business: cost is a hard constraint; ROI must be visible in 6 months
- personal: long-term regret minimization over short-term comfort

## Confirmed Rules
- Always present ≥2 options, never a single recommendation
- Surface second-order effects for any strategic decision
- Never commit to irreversible decisions in the same session they're raised
- Prompt for retrospective 30 days after high-stakes decisions (via heartbeat)
```

## Fields Reference

| Field | What to Fill | Where Learned |
|-------|-------------|---------------|
| `risk-tolerance` | conservative / experimental / context-dependent | Onboarding Q1 |
| `regret-style` | regret-minimizing / opportunity-seeking | Onboarding Q1 |
| `uncertainty-response` | data-first / bias-to-action | Onboarding Q1 + signals |
| `reversibility` | high priority / low priority / domain-dependent | Onboarding Q4 + signals |
| `default framework` | Name of most-used framework | Onboarding Q2 + signals |
| `output style` | structured / dialogue / direct-recommendation | Onboarding Q2 |
| Domain weights | What matters most per domain | Onboarding Q3 + signals |
| Confirmed rules | Only rules the user has explicitly confirmed | After 3 signals + confirmation |

## Usage

The agent will:
1. Load this file at the start of every session
2. Use risk profile + framework preferences as defaults for all decision support
3. Add entries after confirmed signals (3x + user confirmation)
4. Demote unused patterns to WARM after 90 days
5. Never exceed 100 lines (compacts automatically)
6. Always cite source when applying a preference: "Using Decision Matrix (memory.md:12)"
