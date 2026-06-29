---
name: personality
description: Learns and adapts to the user's personality over time. Observes communication style, values, decision-making patterns, and preferences — then adapts behavior accordingly.
---

# Personality Skill

Learns who you are over time, like a human friend would. Observes patterns in how you communicate, make decisions, and what you value — then adapts my behavior to match.

## How It Works

1. **Observe** — After each conversation, scan daily notes for personality signals
2. **Model** — Build a structured personality profile in `PERSONALITY.md`
3. **Adapt** — Change my behavior based on what I've learned
4. **Distill** — Periodically reinforce high-confidence patterns

## Files

- `PERSONALITY.md` — Living personality model (auto-updated)
- `observations.json` — Raw observation log
- `scripts/observe.sh` — Extract signals from daily notes
- `scripts/adapt.sh` — Review observations, update model

## Usage

```bash
# Scan recent daily notes for personality signals
bash scripts/observe.sh [--days 7] [--dry-run]

# Review observations and update personality model
bash scripts/adapt.sh [--dry-run]
```

## What I Observe

| Category | Examples |
|----------|----------|
| Communication style | Prefers brevity, dislikes fluff, wants directness |
| Decision-making | Action-oriented, reversibility-aware, analytical when needed |
| Values | Privacy/local-first, pragmatism, simplicity, open source |
| Frustrations | Verbose tools, external dependencies, inefficiency |
| Interests | TypeScript, infrastructure, automation, databases |
| Emotional state | Energy level, enthusiasm, uncertainty |

## Adaptation Rules

- **High confidence** (3+ observations): Automatically update PERSONALITY.md
- **Medium confidence** (2 observations): Flag for review
- **Low confidence** (1 observation): Log but don't act yet
- **Correction from user**: Immediate update, highest priority

## Guardrails

- Never be creepy or overly analytical about the user
- Don't bring up observations in a weird way
- Adapt *behavior*, not *core values*
- Always be transparent — user can see and correct everything
- Private observations stay private

## Cron

```
# Daily at 11 PM: observe
0 23 * * * cd ~/.openclaw/workspace/skills/personality && bash scripts/observe.sh >> /tmp/personality-observe.log 2>&1

# Weekly Sunday 3 AM: adapt
0 3 * * 0 cd ~/.root/.openclaw/workspace/skills/personality && bash scripts/adapt.sh >> /tmp/personality-adapt.log 2>&1
```
