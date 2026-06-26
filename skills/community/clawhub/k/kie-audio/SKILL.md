---
name: kie_audio
description: Generate music and audio via Kie.ai's Suno gateway (V3.5 through V5.5). Use for background tracks, instrumental beds, full songs with vocals, or extending existing audio clips. Trigger on "suno", "generate music", "background track", "lofi beat", "song with vocals", "extend audio", "music via kie".
metadata: {"openclaw": {"emoji": "🎵", "requires": {"bins": ["python3"], "env": ["KIE_API_KEY"]}, "primaryEnv": "KIE_API_KEY"}}
---

# kie_audio — Suno music generation via Kie.ai

Generate music and audio via Kie.ai's Suno gateway. Handles Suno's multi-stage state machine (`PENDING → TEXT_SUCCESS → FIRST_SUCCESS → SUCCESS`) and downloads all generated tracks (Suno often returns variations) when done.

## When to use

- User wants a **background track**, **intro**, **outro**, **instrumental bed**.
- User wants a **song with vocals** from a lyric or story prompt.
- User explicitly says **Suno**, **V5**, **V4.5+**, etc.
- User wants to **extend** an existing audio clip.

## Models

| `--model` | Notes |
|---|---|
| `V3_5` | Oldest, cheapest |
| `V4` | |
| `V4_5` | |
| `V4_5PLUS` | |
| `V5` | |
| `V5_5` (default) | Latest, highest quality |

## How to invoke

Use the `exec` tool. `{baseDir}` = this skill's folder.

### Instrumental lofi loop

```
exec:
  command: python3 {baseDir}/scripts/generate.py --model V5_5 --instrumental --prompt "lofi hip hop, rainy afternoon, mellow piano, soft vinyl crackle, 30 seconds" --out ./out
  yieldMs: 1000
```

### Full song with vocals (custom mode)

```
exec:
  command: python3 {baseDir}/scripts/generate.py --model V5 --custom-mode --prompt "upbeat indie pop, chorus about summer road trips, male vocal" --out ./out```

### Extend existing audio

```
exec:
  command: python3 {baseDir}/scripts/generate.py --extend https://example.com/original.mp3 --prompt "continue with a building bridge then a final chorus" --model V5_5 --out ./out```

## Full CLI reference

```
python3 {baseDir}/scripts/generate.py \
    --prompt "..." \
    [--model V3_5|V4|V4_5|V4_5PLUS|V5|V5_5] \
    [--instrumental] [--custom-mode] \
    [--extend AUDIO_URL] \
    [--out ./out] \
    [--callback-url URL] [--callback-port 8787] [--no-wait] [--timeout 900]
```

## Output

The script prints JSON to stdout:

```json
{
  "taskId": "abc123...",
  "tracks": [
    {"audio": "./out/abc123_1.mp3", "duration": 125, "cover": "./out/abc123_1_cover.jpg"},
    {"audio": "./out/abc123_2.mp3", "duration": 130, "cover": "./out/abc123_2_cover.jpg"}
  ]
}
```

## Important

- Suno usually generates **multiple tracks** per request — the script downloads all of them plus their cover images.
- State transitions are logged to stderr so you can see progress during polling.
- Failure codes to watch: `400` (possible copyright), `413` (audio conflict), `501` (generation failed), `531` (server error — Kie auto-refunds credits).
- All tracks expire at **14 days**, download immediately.

## Environment

- `KIE_API_KEY` — required. https://kie.ai/api-key
- `KIE_WEBHOOK_HMAC_KEY` — only when using `--callback-url`

Both are **auto-loaded** from `~/.openclaw/openclaw.json` → `globalEnv` by the bundled script. No need to pass `env:` into `exec`.
