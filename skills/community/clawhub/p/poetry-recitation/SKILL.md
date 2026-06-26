---
name: poetry-recitation
description: >
  Generate poetry recitation videos using a cloned voice or system voice with starry background and Chinese subtitles.
  Use when: (1) User asks to recite a poem, (2) User says "朗诵", "诗朗诵", "读一首诗", (3) User wants
  a video with voice + subtitles for any poem or literary text. NOT for: AI-generated video backgrounds,
  music generation, or non-poetry text-to-speech.
---

# Poetry Recitation

Generate a video: voice recitation + starry background + timed Chinese subtitles.

## Prerequisites

- TTS pipeline at `~/.openclaw/skills/tts-gen-pipeline/` with at least one cloned voice
- Dependencies: `dashscope`, `websockets`, `moviepy`, `pillow`, `numpy`
- Font: NotoSerifCJK at `/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc`

## Quick Start

```bash
python3 scripts/poetry_recitation.py --poem "床前明月光\n疑是地上霜" --title "静夜思"
# or specify a voice:
python3 scripts/poetry_recitation.py --poem "..." --title "静夜思" --voice 章彦博
```

## Arguments

| Arg | Required | Description |
|-----|----------|-------------|
| `--poem` | Yes | Poem text, use `\n` for line breaks |
| `--title` | No | Title displayed at top of video |
| `--voice` | No | Voice name: cloned voice (e.g. 章彦博) or system voice (cherry/serena/ethan/chelsie). Default: first cloned voice |
| `--output` | No | Output video path (default: `~/workspace/audio/<title>_朗诵.mp4`) |

## Available Voices

**Cloned voices:** Check with `python3 ~/.openclaw/skills/tts-gen-pipeline/scripts/generate.py list-local`

**System voices:** cherry (甜美女声), serena (温柔女声), ethan (沉稳男声), chelsie (磁性男声)

## Workflow

1. Accept poem text from user (and optional `--voice` preference)
2. Run `poetry_recitation.py` with the poem
3. Send the resulting video to user via MEDIA path — no extra confirmation needed

## Voice Resolution

- If `--voice` matches a local cloned voice name → uses cloned voice model
- If `--voice` matches a system voice name → uses system voice model
- If not specified → uses first available cloned voice

## Output

Generated video (1920x1080, 24fps, H.264 + AAC) saved to `~/workspace/audio/`.
