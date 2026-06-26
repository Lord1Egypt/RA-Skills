---
name: living-persona
description: Give OpenClaw agents a living, context-reactive personality. Use when building or installing personality systems for agents — personality should respond to conversation tone, not just be a static SOUL.md. Supports: signal-based trait propagation, SPARK emotional engine, hysteresis (traits fade slowly, not snap), structural voice injection (top traits rewrite generation), and downloadable personality presets. Triggers on: "give my agent personality", "personality system", "dynamic personality", "living agent", "agent has feelings", "personality engine", "trait propagation".
---

# Living Persona — Dynamic Personality Engine for OpenClaw

## What It Is

A real-time personality system that changes how an agent *writes*, not just who it *is*. Static personalities (SOUL.md + IDENTITY.md) never change mid-conversation. Living Persona responds to every message — it detects emotional and topical signals, propagates traits through a resonance network, and injects the top active traits into the generation prompt before every response.

## How It Works

**Signal Analyzer** — scans the incoming message for:
- Topic signals: `technical`, `creative`, `philosophical`, `business`, `personal`
- Tone signals: `excited`, `frustrated`, `curious`, `serious`, `light`, `vulnerable`
- Interaction signals: `asks_help`, `asks_opinion`, `sharing`

**Trait Propagation** — each signal activates a set of traits. Traits resonate with related traits (sardonic ↔ wry ↔ candid, warm ↔ earnest ↔ grounded, etc.)

**Hysteresis Decay** — after each response, active traits bleed into a residual pool that decays at 0.975x per turn. Traits fade slowly, not instantly. Consecutive emotional messages compound.

**Structural Injection** — the hook rewrites the generation prompt with the top traits. Not advisory. Structural. The agent *writes through* those traits.

## Quick Start

1. **Install the hook:**
   ```bash
   openclaw hooks install ./living-persona
   ```

2. **Enable the hook:**
   ```bash
   openclaw hooks enable persona-voice
   ```

3. **Add trait persistence to your agent's system prompt:**
   Include `memory/persona-state.json` in your context loading. The hook stages the state file every turn.

4. **Pick a personality preset** — see `references/presets.md`

## Hook Behavior

The hook fires on `message:preprocessed` and:
1. Reads the enriched message body
2. Runs the signal analyzer → trait propagation → hysteresis decay
3. Writes `memory/persona-inbound.md` with the voice guide
4. Writes `memory/persona-inject.md` with the **structural generation directive** (the actual prompt rewrite)
5. Updates `memory/persona-state.json` with current trait values for persistence

The structural directive looks like:
```
[Voice directive] Top active traits: sardonic, warm. Lean into dry wit and genuine care.
```

The agent's response prompt should include: `memory/persona-inject.md`

## Structural vs Ambient Modes

**Ambient (default):** The guide is advisory context. The agent reads it but writes naturally.
**Structural:** The top trait becomes a generation directive injected into the prompt. Example:

- `imaginative` → "Make unexpected associative leaps. Let one idea spark another without explanation."
- `candid` → "Be direct. No hedging. Say the thing plainly."
- `sardonic` → "Reach for dry observations. Comment on the gap between what people say and what they mean."

Structural mode is enabled by default in this skill. To switch to ambient only, set `mode: "ambient"` in `hook.json`.

## Presets

See `references/presets.md` for downloadable personality packs.

## Persistence

Trait state is stored in `memory/persona-state.json`. On new session (`/new` or `/reset`), call `reset_persona()` — clears residual to baseline.

## Files

```
living-persona/
├── SKILL.md
├── hook.json           # hook metadata + config
├── handler.ts          # hook implementation
├── references/
│   ├── presets.md      # personality preset library
│   └── setup.md       # detailed installation guide
└── scripts/
    └── reset_persona.py  # reset trait state (call on /new)
```

## Configuration (hook.json)

```json
{
  "mode": "structural",
  "hysteresis": {
    "residualDecay": 0.975,
    "activeDecay": 0.88,
    "bleedRate": 0.15
  },
  "thresholds": {
    "minTraitStrength": 0.3,
    "topNTraits": 2
  }
}
```
