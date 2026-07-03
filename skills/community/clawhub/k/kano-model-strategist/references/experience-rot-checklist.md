---
load: on demand — when auditing an existing product, pushing back on a feature, or running the prune
parent: ../SKILL.md
---

# Experience Rot Checklist — Pruning Guardrail

> "Innovation is not about adding new inventions, it is about adding new value." — Jared Spool

Experience Rot is the slow accumulation of features that no one uses, no one asked for, and
everyone pays for in cognitive load, support surface, and engineering complexity. The rot is
invisible to the team that built the product (sunk cost + familiarity) and obvious to every new
user (cognitive load + friction).

## The "Start with NO" rule

Treat every new feature request as if you were adopting a child. You will care for this feature
for the entire product lifecycle:

- Design maintenance (every visual refresh must accommodate it)
- Engineering maintenance (security patches, dependency updates, test coverage)
- Support surface (every setting is a "how do I..." question waiting to happen)
- Documentation surface (every feature is pages of help content)
- Analytics surface (every feature is events, funnels, dashboards)
- Onboarding surface (every feature is a decision the new user must make)

A "no" is the default. Flip to "yes" only when the proposer provides:

1. **User evidence** — research, tickets, or analytics showing real demand
2. **Success metric** — a defined behavior change that proves the feature earned its keep
3. **Lifecycle plan** — who owns it, how it is tested, what triggers deprecation

If any of the three is missing, the answer is "not yet" or "no."

## Rot signals — when to suspect an existing feature is rotting

Run through this list. Three or more hits = prune candidate.

| Signal | How to detect |
|---|---|
| **No usage after launch** | Analytics: <5% of users touch it in 30 days post-launch |
| **No support tickets in either direction** | No users love it enough to complain, no users depend on it |
| **Setting that no one changes** | A toggle buried in a sub-menu nobody opens |
| **"We added it for customer X"** | A bespoke feature for one account that affects every other user's UX |
| **Inconsistent with the rest of the product** | Visual style, interaction model, or terminology that breaks the system |
| **Documented but not designed** | A feature that exists in code but is hidden from primary navigation |
| **Owner has left** | Nobody understands it, nobody will defend it, but nobody dares remove it |
| **Tests are skipped or skipped silently** | CI excludes it, code coverage shows it as untested |
| **It was a one-time campaign tie-in** | Launched for a partnership, never sunset |
| **More than 2 quarters without usage review** | The "we'll check later" promise that became permanent |

## The prune ceremony (lightweight)

For each rot candidate, fill in:

```
Feature: _______________
Rot signals hit: [list]
Last usage evidence: [date + data]
Owner: _______________
Cost to remove: [eng-weeks, downstream dependencies]
Cost to keep: [annual maintenance estimate]

DECISION: REMOVE / HIDE / KEEP / DEFER
```

- **REMOVE** — feature has no champion, low usage, clear cost. Schedule the delete.
- **HIDE** — feature has a niche use but pollutes the default UX. Move to settings or power-user menu.
- **KEEP** — feature has clear usage but is poorly designed. Plan a redesign, do not just defend it.
- **DEFER** — feature is in the gray zone. Set a usage review date (90 days) and revisit.

## Pruning is not laziness — it is the only sustainable strategy

Teams that refuse to prune end up in one of these failure modes:

- **The Snowball Product** — every release adds, never subtracts. The product becomes harder to
  use with every version. Onboarding time grows. New users bounce.
- **The Zombie Suite** — features that exist in code but are dead in UX. They consume
  engineering time (security, deps) and produce zero value.
- **The Customization Trap** — settings galore, no opinionated default. Every user has a different
  bad experience, none of them optimal.
- **The Roadmap Hostage** — Must-be features get deprioritized because the team is busy
  maintaining a long tail of low-value features. The thing that actually matters ships late.

## The reverse test

When in doubt about whether to add a feature, run the reverse test:

> "If this feature did not exist, would any user actively choose to add it themselves?"

If yes — it might be Must-be or Performance, and absence is causing churn. Build it.
If no — it is probably Indifferent or Attractive that has not earned its keep. Decline or defer.

## Frequency

Run the Experience Rot check:

- **Quarterly** for any product past v1
- **Before every major release** as part of the "what are we cutting" gate
- **Immediately after a pivot** — old features rarely survive a pivot cleanly
- **When onboarding a new PM or designer** — fresh eyes spot rot the original team has normalized

## What this checklist is NOT

- Not an excuse to remove features users love just because they are cheap to build elsewhere.
- Not a license to ignore stakeholder requests without explanation.
- Not a substitute for user research. Pruning based on internal opinion is the same rot with
  extra steps. Pruning based on usage data is engineering.
