---
name: screen-narrator
description: Live narration of your macOS screen activity with Gemini vision + ElevenLabs speech.
homepage: https://github.com/buddyh/narrator
metadata:
  {
    "openclaw":
      {
        "emoji": "🎙️",
        "requires": {
          "bins": ["python3", "tmux", "peekaboo"],
          "env": ["GEMINI_API_KEY", "ELEVENLABS_API_KEY"]
        },
      },
  }
---

# Screen Narrator

This skill maps to the upstream `narrator` repo implementation.

It runs Gemini-vision narration styles (sports, nature, horror, noir, reality_tv, asmr, wrestling) and ElevenLabs TTS, with optional dual-lane narration and live control via JSON files.

## Source of truth

Use the repo install:

```bash
cd /Users/buddy/narrator
/Users/buddy/narrator/.venv/bin/python -m narrator sports --help
```

## Setup

```bash
cd /Users/buddy/narrator
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Required environment:

- `GEMINI_API_KEY`
- `ELEVENLABS_API_KEY`
- optional: `ELEVENLABS_VOICE_ID`

## Runtime control commands

Start live narration in a tmux session (preferred):

```bash
tmux new-session -d -s narrator "cd /Users/buddy/narrator && /Users/buddy/narrator/.venv/bin/python -m narrator sports --control-file /tmp/narrator-ctl.json --status-file /tmp/narrator-status.json"
```

Start with timer:

```bash
tmux new-session -d -s narrator "cd /Users/buddy/narrator && /Users/buddy/narrator/.venv/bin/python -m narrator wrestling --time 5m --control-file /tmp/narrator-ctl.json --status-file /tmp/narrator-status.json"
```

Change style on the fly:

```bash
echo '{"command": "style", "value": "horror"}' > /tmp/narrator-ctl.json
```

Set profanity:

```bash
echo '{"command": "profanity", "value": "low"}' > /tmp/narrator-ctl.json
```

Pause / resume:

```bash
echo '{"command": "pause"}' > /tmp/narrator-ctl.json
echo '{"command": "resume"}' > /tmp/narrator-ctl.json
```

Stop:

```bash
tmux kill-session -t narrator
```

Check status:

```bash
cat /tmp/narrator-status.json
```

## Notes

- macOS only (screen capture + TTS/audio).
- This OpenClaw skill wrapper is aligned to the `/Users/buddy/narrator` implementation to avoid drift between docs and runtime.
