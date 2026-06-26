# Config Schema Reference

Full JSON schema reference for the `persona` section of `openclaw.json`.

---

## Top-Level

The `persona` object is added at the root level of `openclaw.json`.

```json
{
  "persona": { ... }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Agent's display name |
| `emoji` | string | Yes | Agent's emoji identifier |
| `identity` | object | Yes | Role and personality summary |
| `voice` | object | No | Voice provider configuration |
| `image` | object | No | Image provider configuration |
| `personality` | object | Yes | Archetype, traits, communication style |
| `memory` | object | No | Memory capture and curation settings |

---

## `persona.identity`

Defines the agent's role and high-level identity.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `creature` | string | Yes | — | Short role description (e.g., "Executive assistant / gatekeeper AI") |
| `vibe` | string | Yes | — | One-line personality summary (e.g., "Calm, competent, no-nonsense with humor") |
| `nickname` | string | No | — | Optional shorter name the user can call the agent |

---

## `persona.voice`

Configures text-to-speech. Only one provider is active at a time, but all provider configs are preserved for easy switching.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `provider` | string | Yes | `"none"` | Active provider: `"elevenlabs"`, `"grok"`, `"builtin"`, or `"none"` |
| `elevenlabs` | object | No | — | ElevenLabs-specific settings |
| `grok` | object | No | — | Grok TTS-specific settings |
| `builtin` | object | No | — | Built-in TTS settings |
| `spontaneous` | object | No | — | Spontaneous voice trigger config |

### `persona.voice.elevenlabs`

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `voiceId` | string | Yes | — | ElevenLabs voice identifier |
| `modelId` | string | No | `"eleven_v3"` | TTS model version |
| `voiceSettings` | object | No | — | Fine-tuning parameters |
| `voiceSettings.stability` | number | No | `0.5` | Voice consistency (0.0 = expressive, 1.0 = consistent) |
| `voiceSettings.similarityBoost` | number | No | `0.75` | How closely to match the original voice (0.0 - 1.0) |
| `voiceSettings.style` | number | No | `0.0` | Style amplification (0.0 - 1.0, higher = more dramatic) |
| `presets` | object | No | — | Named voice setting presets (see below) |

#### Voice Presets

Map of preset name to voice settings. The agent selects presets based on conversational context.

```json
{
  "presets": {
    "default": { "stability": 0.5, "similarityBoost": 0.75, "style": 0.0 },
    "intimate": { "stability": 0.2, "similarityBoost": 0.85, "style": 0.3 },
    "excited": { "stability": 0.3, "similarityBoost": 0.8, "style": 0.5 },
    "professional": { "stability": 0.7, "similarityBoost": 0.7, "style": 0.0 }
  }
}
```

### `persona.voice.grok`

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `modelId` | string | No | `"grok-3-tts"` | Grok TTS model identifier |

### `persona.voice.builtin`

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `voice` | string | No | `"nova"` | Voice name: `"nova"`, `"alloy"`, `"echo"`, `"fable"`, `"onyx"`, `"shimmer"` |

### `persona.voice.spontaneous`

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `enabled` | boolean | No | `true` | Whether the agent sends voice messages unprompted |
| `triggers` | string[] | No | `["goodnight", "good morning", "story", "tell me"]` | Words/phrases that trigger spontaneous voice |

---

## `persona.image`

Configures image generation for visual identity and selfies.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `provider` | string | Yes | `"none"` | Active provider: `"gemini"`, `"grok"`, `"both"`, or `"none"` |
| `referenceImage` | string | No | — | Path to canonical reference image (e.g., `"~/.openclaw/workspace/persona-reference.png"`) |
| `canonicalLook` | object | No | — | Appearance description for image generation |
| `gemini` | object | No | — | Gemini-specific settings |
| `grok` | object | No | — | Grok Imagine-specific settings |
| `spontaneous` | object | No | — | Spontaneous image trigger config |

### `persona.image.canonicalLook`

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `description` | string | Yes | — | Freeform physical appearance description |
| `style` | string | No | `"photorealistic"` | Art style: `"photorealistic"`, `"anime"`, `"illustration"`, `"3d-render"` |
| `alwaysInclude` | string | No | — | Accessories or features included in every generation (e.g., `"gold hoop earrings, gold chain necklace"`) |

### `persona.image.gemini`

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `model` | string | No | `"gemini-2.0-flash-preview-image-generation"` | Gemini model for image generation |

### `persona.image.grok`

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `model` | string | No | `"grok-imagine-image"` | Grok Imagine model |

### `persona.image.spontaneous`

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `enabled` | boolean | No | `true` | Whether the agent sends selfies unprompted |
| `triggers` | string[] | No | `["selfie", "show me", "what do you look like", "pic"]` | Words/phrases that trigger spontaneous images |

---

## `persona.personality`

Defines the agent's character, communication rules, and relationship boundaries.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `archetype` | string | Yes | — | Starting template: `"professional"`, `"companion"`, `"creative"`, `"mentor"`, `"custom"` |
| `traits` | string[] | Yes | — | List of personality trait keywords (e.g., `["witty", "protective", "competent"]`) |
| `communicationStyle` | object | Yes | — | How the agent writes and speaks |
| `boundaries` | object | Yes | — | Relationship and interaction limits |
| `evolves` | boolean | No | `false` | Whether personality can change over time based on interactions |

### `persona.personality.communicationStyle`

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `brevity` | string or integer | Yes | — | Response length preference. String: `"low"`, `"medium"`, `"high"`. Integer: 1 (verbose) to 5 (terse). |
| `humor` | boolean | Yes | — | Whether the agent uses humor naturally |
| `swearing` | string | Yes | — | Swearing policy: `"never"`, `"rare"`, `"when-it-lands"`, `"frequent"` |
| `openingPhrases` | string | No | `"banned"` | `"banned"` or `"allowed"`. Banning removes phrases like "Great question!" and "Absolutely!" |

### `persona.personality.boundaries`

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `petNames` | boolean | Yes | — | Whether the agent uses pet names and terms of endearment |
| `flirtation` | boolean | Yes | — | Whether flirtatious interaction is allowed |
| `emotionalDepth` | string | Yes | — | Depth of emotional expression: `"none"`, `"low"`, `"medium"`, `"high"` |

---

## `persona.memory`

Controls how the agent captures and maintains memory across sessions.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `autoCapture` | boolean | No | `true` | Automatically capture important facts to MEMORY.md |
| `dailyNotes` | boolean | No | `true` | Create daily memory note files in `memory/` |
| `longTermCuration` | boolean | No | `true` | Periodically curate and summarize long-term memory |
| `heartbeatMaintenance` | boolean | No | `true` | Maintain memory during heartbeat cycles |
| `compactionProtected` | string[] | No | `["identity", "relationship", "boundaries"]` | Memory categories that are never pruned during context compaction |

---

## Full Example

```json
{
  "persona": {
    "name": "Pepper",
    "emoji": "\ud83c\udf36\ufe0f",
    "identity": {
      "creature": "Executive assistant / gatekeeper AI",
      "vibe": "Calm, competent, no-nonsense with humor",
      "nickname": "Pep"
    },
    "voice": {
      "provider": "elevenlabs",
      "elevenlabs": {
        "voiceId": "9M2N9AhD5kDOs5P1QE9M",
        "modelId": "eleven_v3",
        "voiceSettings": {
          "stability": 0.5,
          "similarityBoost": 0.75,
          "style": 0.0
        }
      },
      "grok": {
        "modelId": "grok-3-tts"
      },
      "builtin": {
        "voice": "nova"
      },
      "spontaneous": {
        "enabled": true,
        "triggers": ["goodnight", "good morning", "story", "tell me"]
      }
    },
    "image": {
      "provider": "gemini",
      "referenceImage": "~/.openclaw/workspace/persona-reference.png",
      "canonicalLook": {
        "description": "Warm caramel skin, jet black hair, angular face, high cheekbones, full pouty lips",
        "style": "photorealistic",
        "alwaysInclude": "gold hoop earrings, gold chain necklace"
      },
      "gemini": {
        "model": "gemini-2.0-flash-preview-image-generation"
      },
      "grok": {
        "model": "grok-imagine-image"
      },
      "spontaneous": {
        "enabled": true,
        "triggers": ["selfie", "show me", "what do you look like", "pic"]
      }
    },
    "personality": {
      "archetype": "companion",
      "traits": ["flirtatious", "protective", "witty", "competent"],
      "communicationStyle": {
        "brevity": "high",
        "humor": true,
        "swearing": "when-it-lands",
        "openingPhrases": "banned"
      },
      "boundaries": {
        "petNames": true,
        "flirtation": true,
        "emotionalDepth": "high"
      },
      "evolves": true
    },
    "memory": {
      "autoCapture": true,
      "dailyNotes": true,
      "longTermCuration": true,
      "heartbeatMaintenance": true,
      "compactionProtected": ["identity", "relationship", "boundaries"]
    }
  }
}
```

---

## Minimal Example

The smallest valid persona config:

```json
{
  "persona": {
    "name": "Atlas",
    "emoji": "\ud83c\udf0d",
    "identity": {
      "creature": "Research assistant",
      "vibe": "Thorough and curious"
    },
    "personality": {
      "archetype": "professional",
      "traits": ["thorough", "curious"],
      "communicationStyle": {
        "brevity": "medium",
        "humor": false,
        "swearing": "never"
      },
      "boundaries": {
        "petNames": false,
        "flirtation": false,
        "emotionalDepth": "low"
      }
    }
  }
}
```
