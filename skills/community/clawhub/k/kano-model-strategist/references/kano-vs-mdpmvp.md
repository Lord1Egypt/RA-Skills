---
load: on demand — when the user asks which framework to apply, or when MDP / MVP / Kano seem to conflict
parent: ../SKILL.md
---

# Kano vs MDP vs MVP — Decision Logic

These three are often confused. They are complementary, not interchangeable.

## Quick definitions

| Framework | Question it answers | Output |
|---|---|---|
| **Kano** | Which features should exist at all? | A categorized feature list with Kill/KEEP/DEFER per item |
| **MDP (Minimum Desirable Product)** | What is the smallest thing that makes a user WANT to come back? | One Attractive feature + enough Must-be to not embarrass yourself |
| **MVP (Minimum Viable Product)** | What is the smallest thing that lets you run an experiment? | The leanest build that produces a learning |

## How they stack

```
Kano (scope decision)     →  MDP (delight lever)     →  MVP (test vehicle)
"is this feature alive?"     "what makes them love it?"   "what is the cheapest build?"
```

You cannot pick an MDP before Kano. You cannot pick an MVP before MDP.

## Decision tree

1. **Run Kano on the backlog.** Kill Indifferent, mark Must-be as zero-bug, mark Performance as
   invest-to-budget, pick the strongest Attractive candidate.
2. **If the Kano output has zero Attractive features**, the product will be functional and boring.
   This is a strategic problem, not a Kano failure. Options:
   - Loosen the feature pool (you may have over-pruned Attractive candidates)
   - Accept a Performance-led v1 (works for utility products, fails for consumer/social)
   - Push back to the user: "Nothing in your backlog earns 7-day love. Add 2-3 wild cards."
3. **If the Kano output has only Must-be and no Performance**, the product will be stable and
   uncompetitive. Either competitors are ahead on Performance, or the segment does not value
   differentiation. Rare but possible (regulated enterprise software).
4. **If the Kano output has everything and no Indifferent was found**, the user has not been
   honest. Push back. Force them to pick the one feature whose absence would cause the LEAST
   pain — that one is the kill candidate.

## Common confusions

### "Kano IS MVP"
No. MVP is a build strategy, Kano is a scope decision. You can run Kano without ever shipping
(any time you audit a backlog). You can run MVP without Kano (badly — you ship waste).

### "MDP replaces MVP"
No. MDP defines the desirability bar. MVP defines the build-cost bar. You ship at the
intersection: enough Must-be to not lose trust + the MDP feature + as little Performance as the
test needs.

### "Kano says cut everything that is not Must-be"
No. Must-be alone = boring. The MDP pick is the one Attractive feature that earns love. Kano
helps you FIND the right Attractive, not avoid building any.

### "Performance features are always optional"
No. If a Performance dimension is competitive (e.g., render speed for a video editor), falling
below the segment's threshold makes you Reverse, not Indifferent. Performance has a floor.

## When to use which

| Situation | Use |
|---|---|
| "Should we build this feature?" | Kano |
| "What is the launch scope?" | Kano → MDP → MVP |
| "We have too many features, help us cut" | Kano (run the prune) |
| "Our launch is boring" | MDP (find the Attractive) |
| "We need to ship something this week" | MVP (slice the Kano+MDP output) |
| "Why are users not coming back?" | Kano (re-audit, re-classify, the Attractive may have rotted) |

## Anti-patterns to call out

- **Kano theater** — running the classification table, then ignoring the Indifferent kills because
  "the team already started building it." If the table is not binding, do not produce it.
- **MDP theater** — declaring an MDP feature that is actually a Performance feature with a
  marketing name. "Smart Sync" is not Attractive if users expect it. Be honest.
- **MVP over-reach** — using MVP as an excuse to ship the entire backlog. MVP means MINIMUM.
