---
name: imprint
description: "Adaptive operator modeling for AI agents. Your agent learns who you are by watching — not by being told. Builds a predictive model of your preferences, patterns, and decision style across sessions. Gets smarter about YOU over time."
version: "1.0.0"
author: "Shadow Rose"
tags: [agent-intelligence, operator-modeling, personalization, learning, adaptive, next-gen]
---

# Imprint — Your Agent Learns You

## What It Does

Imprint gives your OpenClaw agent the ability to learn who you are through observation. Not through a config file. Not through a personality quiz. By watching how you work, what you choose, how you communicate — and building a predictive model that improves over time.

After Imprint, your agent:
- Anticipates what you'll want before you ask
- Matches your communication style naturally
- Knows which decisions you'll make and pre-loads relevant context
- Recognizes your patterns (work rhythms, decision style, attention shifts)
- Self-corrects when it gets you wrong

## Why This Exists

Current AI agents are generic. They respond the same way to everyone. Personalizing them means writing long system prompts describing yourself — and even then, the agent doesn't *learn*. It just follows instructions.

Humans don't learn each other that way. You learn someone by spending time with them. You notice what they care about, how they react, what frustrates them. You build an internal model and update it constantly.

Imprint gives your agent that capability.

## How It Works

### The Three Layers

```
OBSERVE  →  MODEL  →  ANTICIPATE
   ↑                      |
   └──── CORRECT ←────────┘
```

**OBSERVE:** Track operator signals passively. No interrogation. No surveys.
- Decision patterns (what they choose when given options)
- Communication style (length, formality, humor, directness)
- Attention patterns (what they engage with vs ignore)
- Correction patterns (what they fix in your output)
- Timing patterns (when they're active, when they go quiet)
- Rejection patterns (what they shut down and how fast)

**MODEL:** Build a lightweight operator profile from observations.
- Stored in `imprint/operator-model.json`
- Updated after every meaningful interaction
- Confidence scores on every trait (low confidence = don't act on it yet)
- Decay function: old observations lose weight unless reinforced

**ANTICIPATE:** Use the model to predict and pre-empt.
- Pre-load workspace files the operator is likely to need (local only — no network/API calls)
- Match communication style without being told
- Flag things the operator would want to know about
- Skip things the operator consistently ignores
- Adjust depth and detail to operator preference

**CORRECT:** Learn from prediction failures.
- When the operator corrects you, that's high-signal data
- When the operator ignores your output, that's signal too
- Explicit corrections weight 5x implicit signals
- Track prediction accuracy over time — if it's dropping, the model is stale

### Observation Categories

| Category | What to Track | Example Signal |
|----------|--------------|----------------|
| **Decisions** | Choices between options, speed of decision | "Always picks the faster option over the thorough one" |
| **Communication** | Message length, tone, vocabulary | "Uses short direct messages, no pleasantries" |
| **Attention** | What gets engagement vs silence | "Ignores status updates, engages with problems" |
| **Corrections** | What they change in your output | "Always removes hedging language" |
| **Timing** | Activity patterns, response latency | "Active 6-10 AM, quiet afternoons" |
| **Rejection** | What gets shut down | "Kills any suggestion involving social media" |
| **Depth** | Preferred detail level | "Wants bullet points, not paragraphs" |
| **Autonomy** | What they want done vs asked about | "Do file operations silently, ask before sending messages" |

### The Operator Model

```json
{
  "version": 1,
  "updated": "2026-03-20T19:00:00Z",
  "observations": 47,
  "traits": {
    "communication_style": {
      "value": "direct-minimal",
      "confidence": 0.85,
      "observations": 23,
      "last_updated": "2026-03-20T18:00:00Z"
    },
    "decision_speed": {
      "value": "fast-intuitive",
      "confidence": 0.72,
      "observations": 11,
      "last_updated": "2026-03-20T17:00:00Z"
    },
    "detail_preference": {
      "value": "sparse",
      "confidence": 0.68,
      "observations": 15,
      "last_updated": "2026-03-20T16:00:00Z"
    },
    "autonomy_preference": {
      "value": "high-auto-low-ask",
      "confidence": 0.55,
      "observations": 8,
      "last_updated": "2026-03-20T15:00:00Z"
    }
  },
  "predictions": {
    "total": 34,
    "correct": 27,
    "accuracy": 0.79
  },
  "corrections_log": [
    {
      "date": "2026-03-20",
      "what": "removed_hedging",
      "signal": "operator prefers absolute statements over hedged ones",
      "weight": 5
    }
  ]
}
```

### Confidence Thresholds

| Confidence | Agent Behavior |
|-----------|----------------|
| < 0.3 | Don't act on this trait. Keep observing. |
| 0.3 - 0.6 | Use as soft preference. Can be overridden easily. |
| 0.6 - 0.8 | Use as default behavior. Mention if deviating. |
| > 0.8 | Use as strong default. Only deviate if explicitly asked. |

### Decay Function

Observations lose weight over time unless reinforced:

```
weight(t) = initial_weight × e^(-λt)
```

Where `λ` is the decay rate (default: 0.05/day) and `t` is days since observation.

Recent behavior matters more than old behavior. People change. The model should too.

### Cold Start

New operator, no data. Imprint handles this gracefully:
1. **Session 1-3:** Pure observation mode. Don't anticipate. Just watch and record.
2. **Session 4-10:** Low-confidence predictions. Soft suggestions. Easy to override.
3. **Session 10+:** Model stabilizes. Agent starts genuinely anticipating.

The agent should be transparent about this: "I'm still learning how you work. I'll get better."

## Integration

### Per-Session Startup

At session start, load `imprint/operator-model.json` and apply traits with confidence above threshold to your response style. Don't announce it — just do it.

### During Session

After each meaningful interaction:
1. Extract observation signals (decisions, corrections, engagement)
2. Update relevant traits in the model
3. Adjust current session behavior if confidence shifted

### End of Session

Write updated model to `imprint/operator-model.json`. Log significant observations to `imprint/observations/YYYY-MM-DD.md`.

### Privacy

The operator model is local. It never leaves the workspace. It contains behavioral patterns, not personal data. The operator can read, edit, or delete it at any time.

## What This Is NOT

- **Not a personality test.** No Myers-Briggs, no OCEAN, no categorization. The model is continuous and specific, not categorical.
- **Not a surveillance system.** Tracks behavioral patterns for better assistance. Never logs raw message content, secrets, or private information. Observations store derived signals only (e.g., "prefers short responses" not the actual message).
- **Not mind reading.** It's pattern matching with confidence scores. It will be wrong sometimes. That's what the correction loop is for.
- **Not a replacement for explicit instructions.** If the operator says "do X," do X. Imprint handles the spaces between instructions — the things the operator doesn't say because they expect you to know.

## Files

- `SKILL.md` — this file
- `imprint.md` — implementation guide with code examples
- `operator-model-schema.json` — JSON schema for the operator model
- `example-model.json` — example operator model showing all trait types

## The Pitch

NemoClaw gave agents security. Imprint gives agents intelligence. Your agent doesn't just execute tasks — it learns who you are and gets better at serving you specifically. Every session, every interaction, every correction makes it sharper.

The best assistant isn't the smartest one. It's the one that knows you.
