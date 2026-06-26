# ElevenLabs Voice Options

## Current Voice (Default)

**Rachel**
- Voice ID: `21m00Tcm4TlvDq8ikWAM`
- Character: Warm, natural, friendly
- Best for: Casual conversation, storytelling, friendly updates
- Model: `eleven_turbo_v2_5` (fast, cost-effective)

## Popular Alternative Voices

**Alice**
- Voice ID: `Xb7hH8MSUJpSbSDYk0k2`
- Character: Confident, energetic
- Best for: Exciting announcements, enthusiastic delivery

**Domi**
- Voice ID: `AZnzlk1XvdvUeBnXmlld`
- Character: Strong, authoritative
- Best for: Serious topics, commanding presence

**Lily**
- Voice ID: `pFZP5JQG7iQjIQuC4Bku`
- Character: Soft, gentle
- Best for: Calm updates, soothing messages

**Charlotte**
- Voice ID: `XB0fDUnXU5powFXDhCwa`
- Character: Expressive, dynamic
- Best for: Storytelling, dramatic readings

## Voice Settings

**Model Options:**
- `eleven_turbo_v2_5` — Fast, cost-effective (recommended)
- `eleven_multilingual_v2` — Supports multiple languages
- `eleven_monolingual_v1` — Higher quality, slower

**Expressive Tags (for all voices):**
- `[laughs]` — Natural laughter
- `[sighs]` — Expressive sigh
- `[gasps]` — Surprised reaction
- `[excited]` — Energetic delivery
- `[whispers]` — Quiet, intimate tone
- `[pause]` — Brief silence

**Usage in script:**
```bash
scripts/send-voice-memo.sh "[excited] This is amazing!" +14169060839
```

## Changing Voice

Override in `~/.openclaw/.env`:
```bash
ELEVENLABS_VOICE_ID=Xb7hH8MSUJpSbSDYk0k2  # Alice
```

Or pass directly in script if modified to accept voice parameter.

## Cost

- ~$0.04 per 30-second voice memo
- 10 voice memos/day ≈ $12/month
- Worth it for bringing Amz to life 🎤
