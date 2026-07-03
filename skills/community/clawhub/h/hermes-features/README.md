# Hermes Features for OpenClaw

Hermes-style self-improvement and memory management for OpenClaw agents — learning loop, skill system, persistent memory with overflow archive.

## Overview

This repository contains the documentation and implementation of Hermes Agent's core capabilities integrated into OpenClaw agents:

1. **Closed Learning Loop** — Periodic self-review, pattern extraction, skill creation
2. **Skill System** — Auto-create skills from experiences, progressive disclosure
3. **Persistent Memory** — Capacity-limited with hard write-block and overflow archive

## Features

### Closed Learning Loop

- `hermes-style-self-review` cron job (every 30 min)
- Reviews recent sessions, extracts reusable patterns
- Creates skills or memory entries automatically
- Uses GPT-5.5 with high thinking for quality

### Skill System

- `auto-skill-builder` — detects when to save workflows as skills
- Progressive disclosure (summary → full content → references)
- Skill proposals via `skill_workshop` for approval

### Persistent Memory

- 4 memory files with strict character limits:
  - MEMORY.md: 5,000 chars (core agent memory)
  - USER.md: 1,375 chars (user profile)
  - memory/YYYY-MM-DD.md: 3,000 chars (daily journal)
  - working-buffer.md: 1,000 chars (active work buffer)
- Hard write-block prevents overflow
- Overflow archive prevents data loss:
  - MEMORY.md → `vault/30-knowledge/MEMORY-overflow.md`
  - USER.md → `vault/30-knowledge/USER-overflow.md`
  - daily journals → `vault/10-journal/YYYY-MM-DD.md`
  - working-buffer → `vault/30-knowledge/working-buffer-overflow.md`

## Installation

This skill is part of Aquila's core workspace. No separate installation needed.

## Usage

The system runs automatically:

- Cron job every 30 minutes
- Heartbeat integration for real-time nudges
- Memory overflow prevents data loss
- Skill creation from complex tasks

## Related Files

- `vault/30-knowledge/aquila-hermes-features.md` — Full documentation
- `vault/30-knowledge/MEMORY-overflow.md` — Archived memory details
- `vault/30-knowledge/USER-overflow.md` — Archived user profile details
- `vault/10-journal/` — Daily journal archives