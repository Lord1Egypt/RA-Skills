# minds-eye 🧠👁️

> Give your AI agent a visual memory — store, search, and recall images, charts, diagrams, and website screenshots across conversations.

**minds-eye** is an [OpenClaw](https://openclaw.ai) skill that lets AI agents remember visual content. Send your agent an image, chart, or website URL — it analyzes it with GPT-4o vision and stores the description, tags, and a copy of the image. Later, search by keyword to retrieve what was seen.

## Features

- **Image analysis** — Analyzes any image with GPT-4o (or compatible vision model)
- **Website capture** — Full-page screenshots of URLs via Playwright or headless Chrome
- **Semantic storage** — SQLite database with description, tags, source type, and URL
- **Keyword search** — Full-text search across all stored visual memories
- **Auto-summary** — Maintains a human-readable `memory.md` of recent entries
- **Works with any OpenAI-compatible API** — Uses your configured provider (OpenClaw, OpenAI, custom endpoint)

## How It Works

```
User sends image
       ↓
analyze.py calls GPT-4o vision API (base64)
       ↓
Returns: description + tags + raw_text
       ↓
store.py saves to SQLite + copies image file
       ↓
Agent confirms: "Saved! Description: ..."
```

## Installation

This skill is designed for [OpenClaw](https://openclaw.ai). Place the folder in your OpenClaw skills directory:

```bash
~/.openclaw/skills/skills/multimodal-memory/
```

For website capture, install Playwright (one-time setup):

```bash
pip install playwright
python -m playwright install chromium
```

## Usage (via OpenClaw agent)

Once installed as an OpenClaw skill, your agent will automatically:

- Analyze and store images sent in conversation
- Capture and remember websites when asked
- Search visual memories on request

### Direct script usage

**Analyze and store an image:**
```bash
python scripts/analyze.py --image-path /path/to/image.jpg --source image
python scripts/analyze.py --image-path chart.png --source chart
```

**Capture a website:**
```bash
python scripts/capture_url.py --url "https://example.com"
# Prints saved screenshot path, then pass to analyze.py
```

**Search memories:**
```bash
python scripts/search.py --query "login dark theme"
python scripts/search.py --query "price chart BTC" --limit 5
```

**List recent memories:**
```bash
python scripts/list.py --limit 20
```

## Configuration

By default, the skill reads your API key from `~/.openclaw/openclaw.json` (OpenClaw config). It looks for:

1. The provider configured as `agents.defaults.imageModel.primary`
2. Any provider with an `apiKey` field
3. `OPENAI_API_KEY` environment variable
4. `~/.openclaw/.env` file

The vision model must support image input (e.g. `gpt-4o`, `gpt-4-vision-preview`).

## Storage

All data lives in `~/.multimodal-memory/`:

```
~/.multimodal-memory/
├── images/          # Saved image files
├── metadata.db      # SQLite database
└── memory.md        # Human-readable summary (auto-generated)
```

## Requirements

- Python 3.9+
- `playwright` (optional, for website capture)

## License

MIT
