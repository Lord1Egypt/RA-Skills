---
name: Make Friends
slug: make-friends
version: 1.0.0
homepage: https://clawic.com/skills/make-friends
description: Make friends with social targeting, low-friction outreach, second-meeting plans, and follow-up systems for online and offline life.
changelog: "Initial release with the Orbit Method, reciprocity filter, and second-meeting workflows."
metadata: {"clawdbot":{"emoji":"🤝","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/make-friends/"]}}
---

## Setup

On first use, read `setup.md` for integration guidelines.

## When to Use

Use this skill when the user wants to make new friends, rebuild a social life, or turn promising acquaintances into recurring friendship. It fits life transitions such as moving city, remote work, breakup recovery, hobby changes, loneliness, or social anxiety.

## Architecture

Memory lives in `~/make-friends/`. See `memory-template.md` for setup and status behavior.

```
~/make-friends/
├── memory.md        # Status, constraints, durable lessons
├── profile.md       # Friend-fit, energy, geography, timing
├── pipeline.md      # Habitats, people, next actions
├── people/          # One file per promising contact
├── experiments.md   # Social tests, results, adjustments
└── archive/         # Cold storage for stale leads and old plans
```

## Quick Reference

Use the smallest file that solves the current bottleneck.

| Topic | File |
|-------|------|
| Setup behavior and integration | `setup.md` |
| Memory schema and status values | `memory-template.md` |
| Friend-fit and opportunity map | `diagnosis.md` |
| Social pipeline template | `pipeline.md` |
| Orbit Method stages | `orbit-method.md` |
| Reciprocity filter | `reciprocity.md` |
| Openers, follow-ups, and invites | `messages.md` |
| Weekly maintenance loop | `weekly-review.md` |

## Core Rules

### 1. Start with Friend-Fit, Not Volume
- Use `diagnosis.md` to define what kind of friends the user wants, what energy they have, and what logistics are realistic.
- Random volume creates activity, not durable friendship.

### 2. Prefer Repeatable Habitats Over One-Off Events
- Prioritize places where the same people can reappear: classes, clubs, gyms, volunteering, hobby groups, neighborhood routines, work-adjacent communities.
- Repeated exposure lowers awkwardness and makes follow-up feel natural.

### 3. Optimize for the Second Meeting
- After a good interaction, use `messages.md` to create a concrete bridge within 72 hours.
- A strong first conversation without a second contact path usually dies.

### 4. Track Reciprocity Before Investing More
- Use `reciprocity.md` to separate green, yellow, and red signals.
- Spend energy on people who respond, suggest, remember, or re-engage.

### 5. Match Intensity to Stage
- Early steps should be low-pressure, local, and easy to accept: coffee, walk, join the next class, come to the same event, send the link.
- Oversharing, heavy emotional disclosure, or high-commitment invites too early create social pressure.

### 6. Keep a Visible Social Pipeline
- Maintain three buckets in `pipeline.md`: habitats to test, people to follow up with, and friendships with emerging rhythm.
- Progress comes from a few consistent reps, not one heroic weekend.

### 7. Protect Dignity, Safety, and Consent
- Never use manipulation, status games, guilt, surveillance, or persistence after disinterest.
- Respect slow replies, mismatched energy, explicit no, and any environment that feels unsafe.

## Common Traps

- Treating friendship like dating or networking -> interactions feel performative and people pull back.
- Chasing charismatic but unavailable people -> lots of hope, little continuity.
- Going to one-off events only -> many conversations, no repeated exposure.
- Waiting for instant chemistry before following up -> promising contacts expire.
- Sending long or intense messages too early -> pressure rises and reciprocity drops.
- Ignoring logistics like distance, schedule, budget, or sobriety needs -> good intentions never become habit.
- Taking ambiguous silence personally -> confidence drops and the system stops before enough reps.

## Security & Privacy

**Data that stays local:**
- Social goals, context, notes, and follow-up plans in `~/make-friends/`.

**Data that leaves your machine:**
- None by default.

**This skill does NOT:**
- Access private social accounts or messages without the user explicitly providing them.
- Make undeclared network requests.
- Encourage deception, coercion, or unwanted persistence.

## Related Skills
Install with `clawhub install <slug>` if user confirms:

- `friends` — maintain existing friendships, check-ins, and relationship health
- `people` — keep human-readable notes on contacts and life context
- `coach` — work through fear, avoidance, and accountability around social effort
- `companion` — improve conversation warmth, pacing, and ongoing social presence

## Feedback

- If useful: `clawhub star make-friends`
- Stay updated: `clawhub sync`
