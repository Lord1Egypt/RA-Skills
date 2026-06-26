# MiniMax Tools Skill

An OpenClaw skill for calling MiniMax multimodal APIs directly through local Python wrappers.

Instead of relying on the official MiniMax MCP server, this repository provides a maintained, script-first skill that is easy to use from OpenClaw, shell workflows, and local automation.

## What this skill does

This skill currently supports:

- **Speech synthesis (TTS)**
  - synchronous TTS
  - built-in default Chinese and English voices
  - explicit `voice_id` support
  - speed / volume / pitch / emotion controls

- **Voice cloning**
  - upload clone audio
  - upload optional prompt audio
  - create cloned voices
  - optionally download preview audio (`demo_audio`)
  - one-shot `clone-from-files` workflow

- **Image generation**
  - text-to-image
  - reference-image generation via `subject_reference`
  - local image path / URL / Data URL support

- **Video generation**
  - text-to-video
  - image-to-video
  - first/last-frame video generation
  - async task query / wait / download flow

- **Music generation**
  - prompt + lyrics song generation
  - instrumental generation
  - lyrics optimizer support

## What is not implemented yet

At the moment, this repository does **not** include:

- subject-reference-to-video (`s2v`)
- video agent templates
- voice design
- voice listing / management helpers
- async long-text TTS wrappers
- full MiniMax file management coverage beyond what this skill needs today

## Why this skill exists

MiniMax exposes a broad multimodal API surface, but not every workflow is convenient to use through raw HTTP or an aging MCP integration.

This skill is designed for:

- direct local control
- predictable file outputs
- reproducible script-based workflows
- easy reuse inside OpenClaw skills and automations

## Repository structure

```text
.
├── SKILL.md
├── README.md
├── LICENSE
├── references/
│   └── api-notes.md
└── scripts/
    ├── common.py
    ├── minimax.py
    ├── minimax_tts.py
    ├── minimax_voice.py
    ├── minimax_image.py
    ├── minimax_video.py
    └── minimax_music.py
```

## Requirements

### Runtime

- Python 3
- `requests`

Install dependency if needed:

```bash
pip install requests
```

### Environment variables

Required:

```bash
export MINIMAX_API_KEY=your_api_key_here
```

Optional:

```bash
export MINIMAX_BASE_URL=https://api.minimaxi.com
```

## Install

### From ClawHub

```bash
clawhub install minimax-tools
```

### From GitHub

Clone this repository and copy or symlink it into your OpenClaw `skills/` directory.

Example:

```bash
ln -s /home/yangtao/repos/minimax-tools-skill <workspace>/skills/minimax-tools
```

## Unified CLI

Use the single entrypoint:

```bash
python3 scripts/minimax.py <subcommand> ...
```

Available top-level subcommands:

- `tts`
- `voice`
- `image`
- `video`
- `music`

## Quick examples

### TTS with default Chinese voice

```bash
python3 scripts/minimax.py tts \
  --text "你好，欢迎使用 MiniMax。"
```

### TTS with default English voice

```bash
python3 scripts/minimax.py tts \
  --text "Hello, welcome to MiniMax." \
  --voice-lang en
```

### Clone a voice in one step

```bash
python3 scripts/minimax.py voice clone-from-files \
  --clone-file ./voice.wav \
  --voice-id MyVoice001 \
  --text "你好，欢迎使用我的复刻音色。" \
  --download-demo
```

### Text-to-image

```bash
python3 scripts/minimax.py image \
  --prompt "Cyberpunk city at night, cinematic lighting, dense details" \
  --aspect-ratio 16:9
```

### Reference-image generation

```bash
python3 scripts/minimax.py image \
  --prompt "Same character standing in a rainy neon street" \
  --subject-reference ./character.png \
  --aspect-ratio 16:9
```

### Text-to-video

```bash
python3 scripts/minimax.py video create \
  --prompt "An orange cat watching rain by the window, cinematic, soft light" \
  --wait --download
```

### Image-to-video

```bash
python3 scripts/minimax.py video i2v \
  --first-frame-image ./cat.png \
  --prompt "Slow push-in, the cat blinks, rain outside the window" \
  --wait --download
```

### First/last-frame video

```bash
python3 scripts/minimax.py video fl2v \
  --first-frame-image ./young.jpg \
  --last-frame-image ./old.jpg \
  --prompt "A person slowly grows older, stable camera" \
  --wait --download
```

### Music generation

```bash
python3 scripts/minimax.py music \
  --prompt "indie folk, warm, late night city walk" \
  --lyrics "[Verse]\nNight wind slips across the street lights..."
```

## TTS defaults

Current built-in defaults:

- Chinese voice: `Chinese (Mandarin)_Lyrical_Voice`
- English voice: `English_Graceful_Lady`
- Model: `speech-2.8-turbo`
- Format: `mp3`
- Sample rate: `32000`
- Bitrate: `128000`

## Voice cloning constraints

### Clone source audio

- formats: `mp3`, `m4a`, `wav`
- duration: 10 seconds to 5 minutes
- size: <= 20 MB

### Prompt audio

- formats: `mp3`, `m4a`, `wav`
- duration: under 8 seconds
- size: <= 20 MB

MiniMax docs note that cloned voices are temporary unless used in real TTS within 7 days.

## Image generation notes

The current image wrapper supports:

- text-to-image
- reference-image generation through `subject_reference`

This is closer to reference-driven generation / character consistency than a full mask-based editor workflow.

## Video generation notes

Video generation is asynchronous. The typical flow is:

1. create a task
2. query or wait for completion
3. download the final file

The wrapper already supports the full create/query/wait/download path.

## Output behavior

Scripts print JSON to stdout for easy automation.

Typical fields include:

- `ok`
- `trace_id`
- `voice_id`
- `task_id`
- `file_id`
- `id`
- `path`
- `paths`
- `meta`

## ClawHub publishing notes

This skill declares its required environment variable in `SKILL.md` metadata:

- `MINIMAX_API_KEY`

That helps ClawHub understand the skill’s external requirements and reduces the chance of publish-time flagging.

## License

MIT-0
