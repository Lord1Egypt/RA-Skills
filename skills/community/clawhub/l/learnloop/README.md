# LearnLoop — Continuous Learning Protocol for Claude

> Captures corrections, errors, and user preferences into Claude Code's native auto-memory so the next session remembers. Stop teaching Claude the same thing twice.

[![clawhub](https://img.shields.io/badge/clawhub-learnloop-blue)](https://clawhub.ai/skills/learnloop)
[![thinkstack](https://img.shields.io/badge/ThinkStack-5%2F5-purple)](https://clawhub.ai/skills/learnloop)
[![openclaw](https://img.shields.io/badge/openclaw-skill-orange)](https://openclaw.ai)

## The Problem

By default, Claude starts every session from zero. You correct a mistake — gone tomorrow. You explain your role — re-explained next week. A command fails with a known fix — re-debugged from scratch.

Smart in the moment. Amnesic over time. Your time gets spent re-teaching instead of advancing.

## What it does

**Detect** — recognizes the seven trigger moments worth remembering (corrections, errors, preferences, deadlines, validated wins, knowledge gaps, external pointers)

**Classify** — sorts each learning into one of four types: `user`, `feedback`, `project`, `reference`

**Persist** — writes to Claude Code's native auto-memory at `~/.claude/projects/<id>/memory/`, auto-injected into every future session

**Verify** — checks recalled memories against current reality before acting; stale memory is updated or removed, never trusted blindly

## Why Native Memory (Not `.learnings/`)

Older self-improvement skills write to a `.learnings/` folder. LearnLoop uses Claude Code's built-in memory system instead:

| | `.learnings/*.md` | LearnLoop → native memory |
|---|---|---|
| Loaded into next session | Manual, agent must remember | Auto-injected via MEMORY.md |
| Typed | No | Yes (user / feedback / project / reference) |
| Cross-references | No | `[[slug]]` links |
| Setup | Create folder + 3 files | Zero — the directory already exists |

Same loop, half the friction.

## When to Activate

| Trigger | Memory Type |
|---|---|
| User corrects you ("no", "actually", "wrong") | `feedback` |
| Command or tool fails unexpectedly | `project` or `feedback` |
| User shares role, expertise, or preferences | `user` |
| External system referenced (Linear, Grafana, Slack) | `reference` |
| Knowledge turned out outdated | `feedback` |
| Better approach found for a recurring task | `feedback` |
| Deadline or constraint mentioned | `project` |

If you'd say "I'll keep that in mind" — you can't. Save it.

## Installation

```bash
openclaw install learnloop
```

## ThinkStack

LearnLoop is the fifth member of the **ThinkStack** — meta-skills that make Claude smarter at every stage:

```
clarity-first  →  thinkdeep  →  honest-critic  →  task-pilot  →  learnloop
 understand        analyze        challenge         execute        remember
```

```bash
openclaw install clarity-first
openclaw install thinkdeep
openclaw install honest-critic
openclaw install task-pilot
openclaw install learnloop
```

## Keywords

continuous learning · persistent memory · auto-memory · learning loop · knowledge capture · self-improvement · memory protocol · Claude forgets · Claude repeats mistakes · AI forgets corrections · teach Claude twice · Claude has no memory · lost context · AI amnesia · AI agent · agentic · Claude Code · LLM memory · AI productivity · agentic memory · smarter Claude · make Claude better · Claude improvement · improve AI · agent improvement · 持续学习 · 自动记忆 · 智能记忆 · 不再重复错误 · AI记忆

---

Built for [OpenClaw](https://openclaw.ai) · Published on [clawhub.ai](https://clawhub.ai/skills/learnloop)
