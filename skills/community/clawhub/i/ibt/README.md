# IBT v2.9 — Instinct + Behavior + Trust

IBT is an execution framework for agents that need both **initiative** and **discipline**.

It helps an agent:
- understand the real goal before acting
- verify before claiming success
- calibrate confidence and autonomy
- respect approval gates and boundaries
- recover cleanly when trust is damaged
- handle temporary failures without turning into chaos
- learn and apply human preferences automatically

## Core Loop

**Observe → Parse → Plan → Commit → Act → Verify → Update → Stop**

## What's new in v2.9

v2.9 adds **Preference Learning**:
- captures explicit preferences (stated directly)
- learns implicit preferences from patterns
- applies preferences automatically to reduce repeated clarifications
- stores preferences in USER.md (human-readable, human-editable, agent workspace)
- integrates with Observe/Parse/Act phases

## Security & Privacy

- Preferences stored in USER.md only (agent workspace)
- Never stores secrets, keys, credentials, or sensitive data
- Human can view/edit/delete preferences anytime
- Preferences are generic (communication style, task preferences, project context)
- No external services access preference data

## Who it’s for

Use IBT when you want an agent to be:
- proactive, but not reckless
- opinionated, but not contrarian for show
- trustworthy, not overconfident
- capable of recovery after mistakes

## Included files

- `SKILL.md` — full framework
- `POLICY.md` — concise doctrine
- `TEMPLATE.md` — drop-in policy
- `EXAMPLES.md` — practical examples

## Install

```bash
clawhub install ibt
```

## Short version

IBT’s job is simple:

**Be useful, calibrated, and trustworthy — not robotic, not reckless.**

## License

MIT
