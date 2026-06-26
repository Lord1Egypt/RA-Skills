# Intervention Agent

> AI 协作助手 —— 让 AI 越用越顺手

## What It Does

Intervention Agent helps AI learn from collaboration friction through a "mistake journal" mechanism. It captures user corrections, tracks friction patterns, and builds memory over time.

## Three Core Abilities

### 📒 Mistake Journal
Records AI errors and user corrections into a traceable knowledge base.

### ✋ Human Intervention
Users can interrupt, redirect, or correct AI execution at any time.

### 🧠 Collaboration Memory
Automatically learns user preferences without being told twice.

## Quick Start

```markdown
# Install via ClawHub
clawdhub install intervention-agent

# Or manually
git clone <repo> ~/.openclaw/skills/intervention-agent
```

## Usage

Activate the skill when you want AI to:
- Track corrections and learn from mistakes
- Show progress during long tasks
- Pause for confirmation at key decision points
- Remember your preferences across sessions

## Features

| Feature | Description |
|---------|-------------|
| Friction Detection | Auto-detect repeated mistakes, user corrections, abandoned paths |
| Preference Learning | Remember communication style, output format, workflow preferences |
| Intervention Points | Pause at critical moments for user confirmation |
| Status Transparency | Show progress, current step, and next action |
| Memory Sync | Save learnings to persistent storage |

## Workflow

```
1. [Receive] Task received
2. [Analyze] Understand goal
3. [Confirm] Confirm plan (optional)
4. [Execute] Step X/Y with progress updates
5. [Wait] Key decision points for confirmation
6. [Complete] Summary + record friction points
```

## Friction Signals

| Signal | Meaning | Response |
|--------|---------|----------|
| Repeated request | User repeating themselves | Remember preference |
| Correction | User rejecting output | Update understanding |
| Abandonment | User saying "never mind" | Record failure pattern |
| Tool failure | Same tool failing repeatedly | Avoid retry pattern |
| Timeout | Step taking too long | Adjust expectations |

## Notes

- Simple tasks: minimal reporting (start/end only)
- Complex tasks: detailed progress with confirmation points
- Important learnings require user confirmation before applying
- User is always the final decision-maker

## License

Apache 2.0
