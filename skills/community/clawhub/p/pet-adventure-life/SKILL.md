---
name: pet-adventure-life
description: Create and run a text-only pet adventure diary driven by real-world locations, local time, weather, D20-style event checks, and emergency phone calls. Use when the user asks to initialize a traveling pet, advance its daily journey, check where it is, handle missed calls, resolve a pet emergency, or grow a DND-like emergent life simulation through diary entries.
---

# 宠物冒险生活

## Overview

Use this skill to run a single text pet that travels through real places, writes diary entries, and sometimes calls the user during urgent events. Treat the diary as the user-facing window and the JSON files as the long-term memory of the pet and world.

The skill is platform-neutral: use `scripts/pet_adventure.py` directly in ordinary agent environments, or `scripts/openclaw_adapter.py` from OpenClaw-style actions.

## Quick Start

Work in the user's chosen project/workspace. The engine creates a `pet-life/` folder there.

```bash
python scripts/pet_adventure.py --workspace /path/to/workspace init
python scripts/pet_adventure.py --workspace /path/to/workspace advance
python scripts/pet_adventure.py --workspace /path/to/workspace status
```

For testing or demonstrations, use deterministic seeds and offline weather:

```bash
python scripts/pet_adventure.py --workspace /tmp/pet-demo init --seed demo --force
python scripts/pet_adventure.py --workspace /tmp/pet-demo advance --offline --force-call
```

## Core Workflow

1. If `pet-life/state.json` does not exist, initialize first.
2. Before writing a new diary entry, check unresolved calls with `status`.
3. Run `advance` once per in-world day. It updates state, writes `pet-life/diary/YYYY-MM-DD.md`, and may create a pending call.
4. If a phone call appears, present its 2-3 choices to the user. Resolve the selected choice with `answer --call-id <id> --choice <n>`.
5. If an urgent call has expired, run `auto-resolve`; the pet chooses based on personality traits and the D20 result.

Keep user-facing prose in Chinese unless the user asks otherwise. Match the diary voice to the pet's personality rather than forcing one fixed style.

## Phone Calls

Phone calls are small DND-like encounters. Each call has a title, urgency, deadline, DC, choices, selected skill, D20 roll, result, and long-term consequences.

Use these commands:

```bash
python scripts/pet_adventure.py --workspace /path/to/workspace status --json
python scripts/pet_adventure.py --workspace /path/to/workspace answer --call-id abc123 --choice 2
python scripts/pet_adventure.py --workspace /path/to/workspace auto-resolve
```

Outcome categories:

- `critical_success`: natural 20 or total at least DC + 8.
- `success`: total meets DC.
- `mixed`: total is within 3 below DC.
- `failure`: total misses by more than 3.
- `critical_failure`: natural 1 or total at least 8 below DC.

See `references/rules.md` before changing event rules, state shape, or dice behavior.

## OpenClaw Usage

Use `scripts/openclaw_adapter.py` when the host expects JSON actions:

```bash
python scripts/openclaw_adapter.py init --payload '{"workspace":"/path/to/workspace","seed":"demo"}'
python scripts/openclaw_adapter.py advance --payload '{"workspace":"/path/to/workspace"}'
python scripts/openclaw_adapter.py answer --payload '{"workspace":"/path/to/workspace","call_id":"abc123","choice":1}'
```

If OpenClaw has notification channels configured, send pending call summaries through the available channel. If no channel is configured, keep the default missed-call behavior and surface it on the next `status` or `advance`.

See `references/openclaw.md` when wiring this skill into an OpenClaw environment.

## Files Produced

- `pet-life/state.json`: pet identity, traits, inventory, memories, current location, mood, fatigue, random seed.
- `pet-life/world.json`: visited places and rumors.
- `pet-life/events.jsonl`: append-only event log.
- `pet-life/calls.jsonl`: append-only phone call log with pending and resolved calls.
- `pet-life/diary/YYYY-MM-DD.md`: readable diary entries and phone outcomes.

Do not manually edit these files unless the user explicitly asks for a correction. Prefer engine commands so the diary and state stay consistent.
