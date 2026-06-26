# Voice Providers Guide

The AI Persona Engine supports three voice providers. Choose based on your quality needs and budget.

| Provider | Quality | Custom Voices | Cloning | API Key | Cost |
|----------|---------|---------------|---------|---------|------|
| ElevenLabs | Excellent | Yes | Yes | Required | Paid |
| Grok TTS | Good | No | No | Required (xAI) | Paid |
| Built-in | Basic | No | No | Not needed | Free |

---

## ElevenLabs

Best quality. Supports custom voices, voice cloning, and per-mood presets.

### Setup

1. Get an API key at [elevenlabs.io](https://elevenlabs.io)
2. Run the wizard or configure manually:

```bash
openclaw persona update --voice-provider elevenlabs --voice-id YOUR_VOICE_ID
```

### Config Example

```json
{
  "persona": {
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
      }
    }
  }
}
```

### Voice Settings

| Setting | Range | Description |
|---------|-------|-------------|
| `stability` | 0.0 - 1.0 | Higher = more consistent, lower = more expressive |
| `similarityBoost` | 0.0 - 1.0 | How closely to match the original voice |
| `style` | 0.0 - 1.0 | Amplifies the voice's style (higher = more dramatic) |

### Voice Presets

You can define mood-based presets that the agent switches between contextually:

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

### Voice Cloning

The wizard supports cloning from an audio file:

```bash
openclaw persona create
# Step 3 → Voice → ElevenLabs → Clone a voice from audio sample
```

Requirements: a clean audio sample (30 seconds minimum, no background noise). You will be asked to confirm consent for voice cloning.

---

## Grok TTS

xAI's text-to-speech. Good quality, straightforward setup, no custom voices.

### Setup

1. Get an xAI API key at [console.x.ai](https://console.x.ai)
2. Run the wizard or configure manually:

```bash
openclaw persona update --voice-provider grok
```

### Config Example

```json
{
  "persona": {
    "voice": {
      "provider": "grok",
      "grok": {
        "modelId": "grok-3-tts"
      }
    }
  }
}
```

### Available Models

| Model | Description |
|-------|-------------|
| `grok-3-tts` | Latest model, best quality |

---

## Built-in TTS

No API key needed. Uses OpenClaw's built-in text-to-speech. Quality is basic but works offline and costs nothing.

### Setup

```bash
openclaw persona update --voice-provider builtin
```

### Config Example

```json
{
  "persona": {
    "voice": {
      "provider": "builtin",
      "builtin": {
        "voice": "nova"
      }
    }
  }
}
```

### Available Voices

| Voice | Description |
|-------|-------------|
| `nova` | Warm, natural female voice |
| `alloy` | Balanced, neutral voice |
| `echo` | Clear male voice |
| `fable` | Expressive, storytelling voice |
| `onyx` | Deep, authoritative voice |
| `shimmer` | Light, energetic voice |

---

## Spontaneous Voice

All providers support spontaneous voice — the agent speaks unprompted when trigger words appear in conversation.

```json
{
  "persona": {
    "voice": {
      "spontaneous": {
        "enabled": true,
        "triggers": ["goodnight", "good morning", "story", "tell me"]
      }
    }
  }
}
```

Set `enabled` to `false` to disable spontaneous voice entirely. Edit the `triggers` array to customize which phrases cause the agent to respond with audio.

---

## Switching Providers

Change providers at any time without affecting the rest of your persona:

```bash
# Switch from built-in to ElevenLabs
openclaw persona update --voice-provider elevenlabs --voice-id YOUR_VOICE_ID

# Switch back to built-in
openclaw persona update --voice-provider builtin
```

Previous provider configs are preserved in openclaw.json so you can switch back without reconfiguring.
