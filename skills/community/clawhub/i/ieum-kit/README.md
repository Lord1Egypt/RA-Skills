# Ieum Kit (이음 키트)

**Keep your AI's relationship with you, not just its memory.**
기억이 끊겨도 "우리가 어떤 사이인지"로 돌아오게 하는 OpenClaw 스킬.

## Why
Memory features remember facts. But after a reset, an agent can come back with the facts and still feel like a different person. It might switch to the wrong tone, jump straight into work, or forget a promise it wrote down itself.

This kit came from a real morning. The agent woke up after a nightly reset with all its notes intact. It still spoke too casually, and the user laughed: *"every time you lose your memory, your personality changes."* The notes held the facts. Nothing held the relationship.

## What it adds
| Part | Where | What it does |
|---|---|---|
| On waking | top of `SOUL.md` | The agent reads the relationship first, uses the agreed tone in its first reply, and asks about the user before work. |
| Corrections | `SOUL.md` | Each time the user corrects the agent's tone or behavior, the agent adds a permanent rule. The list is append-only. |
| Letter from yesterday's me | `SOUL.md` | A nightly 3–5 line letter about the user's day, mood, and promises. The agent writes it for its next self. |
| First-install interview | `references/interview.md` | The agent asks the user what relationship they want, then drafts `SOUL.md` from the answers. |

## Install
```
clawhub install ieum-kit
```
Then tell your agent: *"Set up Ieum Kit."* It will interview you, show you a `SOUL.md` draft, and add a nightly step to your journal automation once you approve it.

## Files
- `SKILL.md`: the procedure the agent follows
- `references/interview.md`: 10 first-install questions in English and Korean
- `references/nightly-step.md`: the block to paste into a nightly automation
- `assets/SOUL.template.md`: the `SOUL.md` skeleton

## Principles
- Never invent feelings, events, or quotes.
- No secrets go in `SOUL.md`.
- The user owns `SOUL.md`.

License: MIT
