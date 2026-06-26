# Speaker Identification

Kiwi identifies speakers by their voiceprint using [pyannote](https://github.com/pyannote/pyannote-audio) neural embeddings. This enables personalized responses and voice-gated security.

## How it Works

1. When someone speaks, Kiwi extracts a 192-dimensional embedding vector from the audio
2. This vector is compared against stored voiceprints using cosine similarity
3. If the similarity exceeds the threshold, the speaker is identified
4. If no match is found, Kiwi treats the speaker as a new guest

## Priority System

Every speaker is assigned a priority level:

| Priority | Level | Access |
|----------|-------|--------|
| `OWNER` (0) | Highest | Full access. Cannot be blocked. |
| `FRIEND` (1) | High | Dangerous commands need Telegram approval |
| `GUEST` (2) | Default | All sensitive commands need approval |
| `BLOCKED` (99) | None | Completely ignored |

There's also a special `SELF` (-1) priority used internally for TTS echo filtering — Kiwi ignores its own voice output.

## Voice Commands

| Command | Action |
|---------|--------|
| *"Kiwi, remember my voice"* | Register as owner (first registration only) |
| *"Kiwi, this is my friend [name]"* | Add the current speaker as a friend |
| *"Kiwi, block them"* | Block the last unrecognized speaker |
| *"Kiwi, who is speaking?"* | Identify the current speaker |
| *"Kiwi, what voices do you know?"* | List all known voiceprints |

!!! note
    Voice commands are language-dependent. Set `language` in `config.yaml` to match your locale. See `kiwi/locales/*.yaml` for per-language command variants.

## Auto-Learning

When Kiwi encounters an unknown voice, it automatically stores the voiceprint as a guest. On subsequent interactions, the speaker is recognized without any manual registration.

The owner can then upgrade a guest to a friend or block them via voice commands.

## Voiceprint Storage

Voiceprints are stored as JSON files in the `voice_profiles/` directory:

```
voice_profiles/
├── owner.json          # Owner voiceprint + metadata
├── friend_alice.json   # Friend profile
└── guest_001.json      # Auto-learned guest
```

Each file contains the embedding vector, speaker name, priority level, sample count, and last seen timestamp.

**Reset all profiles:**

```bash
rm voice_profiles/*.json
# Restart Kiwi and re-register your voice
```

## Configuration

```yaml
speaker_priority:
  owner:
    name: "Owner"    # Your display name
```
