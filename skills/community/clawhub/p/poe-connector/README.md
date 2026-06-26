# Poe Connector — OpenClaw Skill

An [OpenClaw](https://github.com/openclaw/openclaw) skill that connects your agent to [Poe.com](https://poe.com)'s API, giving it access to **100+ AI models** through a single API key.

## Why This Exists

I've been a Poe user since it first launched — there's always a new model to try and I genuinely enjoy the platform. Last year I accidentally subscribed to a pretty expensive plan, and I've never been able to use up all the credits. So I figured: why not hook it up to OpenClaw and see if that burns through them a bit faster?


## Features

- **Text Chat** — Talk to Claude, GPT, Gemini, Grok, Llama, and hundreds more via `/v1/chat/completions`
- **Image Generation** — GPT-Image-1, Imagen-4, Flux-Kontext, Seedream-3.0
- **Video Generation** — Veo-3, Runway-Gen-4-Turbo, Kling-2.1
- **Audio / TTS** — ElevenLabs, Lyria
- **Multimodal File Input** — Send images, PDFs, audio, video alongside your prompt
- **Model Discovery** — List and search all available Poe models
- **Streaming** — Real-time token-by-token output
- **Auto Retry** — Exponential backoff on rate-limit (429) errors

## Quick Start

### 1. Get your Poe API key

Go to https://poe.com/api/keys and create an API key.

### 2. Configure the API key

Add your key to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "poe-connector": {
        "env": { "POE_API_KEY": "your-key-here" }
      }
    }
  }
}
```

The skill reads the key from this file at runtime. No environment variable needed.

### 3. Install dependency

```bash
pip install openai
```

### 4. Use it

```bash
# Chat (uses default model from poe_config.json, streams by default)
python src/poe_chat.py --message "Hello!"

# Chat with a specific model
python src/poe_chat.py --model GPT-5.2 --message "Write a haiku"

# Generate an image (default: GPT-Image-1)
python src/poe_media.py --type image --prompt "A cat astronaut" --aspect 1:1

# List models
python src/poe_models.py --list

# Search models
python src/poe_models.py --search "claude"
```

### 5. Customize defaults

Edit `poe_config.json` to set your preferred models:

```json
{
  "defaults": {
    "chat": "claude-sonnet-4",
    "image": "GPT-Image-1",
    "video": "Veo-3",
    "audio": "ElevenLabs"
  }
}
```

## Project Structure

```
poe-connector/
├── SKILL.md              # OpenClaw skill definition
├── poe.sh                # Wrapper script (simplifies agent calls)
├── claw.json             # ClawHub publishing manifest
├── instructions.md       # Agent usage guide
├── requirements.txt      # Python dependencies
├── src/
│   ├── poe_utils.py      # Auth, error handling, file encoding
│   ├── poe_chat.py       # Text chat (streaming, multi-turn, file input)
│   ├── poe_media.py      # Image / video / audio generation
│   └── poe_models.py     # Model listing and search
└── examples/
    └── basic_usage.md    # Usage examples
```

## CLI Reference

### poe_chat.py

| Flag | Description |
|---|---|
| `--model, -m` | Model name (optional, defaults from poe_config.json) |
| `--message, -M` | User message |
| `--messages` | Full conversation as JSON array |
| `--system, -s` | System prompt |
| `--stream` | Stream output token by token |
| `--files, -f` | Attach files (images, PDFs, audio, video) |
| `--max-tokens` | Max response tokens |
| `--temperature` | Sampling temperature (0–2) |
| `--extra` | Custom params as JSON (`{"thinking_budget": 10000}`) |

### poe_media.py

| Flag | Description |
|---|---|
| `--type, -t` | `image`, `video`, or `audio` (required) |
| `--model, -m` | Model name (defaults per type) |
| `--prompt, -p` | Generation prompt (required) |
| `--output, -o` | Output file path |
| `--aspect` | Aspect ratio (e.g. `1:1`, `3:2`, `16:9`) |
| `--quality` | Quality level (`low`, `medium`, `high`) |
| `--extra` | Additional params as JSON |

### poe_models.py

| Flag | Description |
|---|---|
| `--list, -l` | List all available models |
| `--search, -s` | Search by keyword |
| `--info, -i` | Detailed info for a model |
| `--json` | Output as JSON |

## OpenClaw Installation

```bash
clawhub install dzwalker/poe-connector
```

Or manually copy to `~/.openclaw/workspace/skills/poe-connector/`.

## Requirements

- Python 3.9+
- `openai` >= 1.0.0
- Poe account with API key


## License

MIT
