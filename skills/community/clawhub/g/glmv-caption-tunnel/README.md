# GLM-V Caption (with Local File Tunnel)

> **Adapted from** [zai-org/GLM-skills/skills/glmv-caption](https://github.com/zai-org/GLM-skills/tree/main/skills/glmv-caption)

Generate captions and descriptions for images, videos, and documents using ZhiPu GLM-V multimodal models — **now with transparent local file support for videos and documents via Cloudflare Quick Tunnel**.

## Why This Fork

The [original skill](https://github.com/zai-org/GLM-skills/tree/main/skills/glmv-caption) requires videos and files to be provided as **public HTTPS URLs** — the GLM-V API does not accept local paths or base64 for these input types. In practice this means you need to manually upload your files somewhere and paste the URL.

This version eliminates that friction: **pass a local file path, and the script handles everything automatically**.

## What Changed

| | Original | This Version |
|---|---|---|
| **Videos** | URL only (local paths rejected with error) | URL **or local path** (auto-tunneled) |
| **Files** (pdf, docx, …) | URL only (local paths rejected with error) | URL **or local path** (auto-tunneled) |
| **Images** | URL, local path (base64), base64 string | Unchanged |
| **Dependencies** | `requests` only | `requests` + [`cloudflared`](https://github.com/cloudflare/cloudflared) (only when using local video/file paths) |
| **Structured output** | Not documented | Optional `--response-format` JSON mode + `--sys-prompt` |
| **New file** | — | `scripts/tunnel_server.py` — self-contained tunnel module |

### How the tunnel works

When you pass a local path for a video or file:

1. A temporary directory is created; your file is symlinked (or copied) into it — **only the files you specify are exposed, nothing else**
2. A Python HTTP server starts on a random port, serving only that temp directory
3. `cloudflared tunnel` (Cloudflare's free quick-tunnel, no account needed) exposes the server as a public HTTPS URL like `https://some-words.trycloudflare.com/your-file.mp4`
4. That URL is passed to the GLM-V API
5. After the API call completes, the tunnel is torn down, the HTTP server stops, and the temp directory is cleaned up

The entire lifecycle is managed by a Python context manager — see [`scripts/tunnel_server.py`](scripts/tunnel_server.py).

## Quick Start

### 1. Install dependencies

```bash
pip install requests
```

### 2. Set your API key

```bash
export ZHIPU_API_KEY="your-key-here"
```

Get a key at [bigmodel.cn](https://bigmodel.cn/usercenter/proj-mgmt/apikeys).

### 3. Run

```bash
# Image (local or URL — works exactly like the original)
python scripts/glmv_caption.py --images photo.jpg

# Video from URL (works like the original)
python scripts/glmv_caption.py --videos "https://example.com/clip.mp4"

# Video from local path — automatically tunneled (new!)
python scripts/glmv_caption.py --videos ./my-video.mp4

# Document from local path — automatically tunneled (new!)
python scripts/glmv_caption.py --files ./report.pdf

# Mix URLs and local paths
python scripts/glmv_caption.py --files "https://example.com/doc.docx" ./local-notes.txt

# Custom prompt
python scripts/glmv_caption.py --videos ./demo.mp4 --prompt "Describe the UI interactions shown in this video"

# Structured JSON output
python scripts/glmv_caption.py --images photo.jpg --response-format --sys-prompt 'Return JSON only: {"summary":"string","objects":["string"]}'
```

### 4. Install cloudflared (needed for local video/file paths only)

If you only use URLs, you don't need this.

**macOS:**
```bash
brew install cloudflared
```

**Windows:**
```bash
winget install Cloudflare.cloudflared
```

**Linux:**
```bash
curl -Lo /usr/local/bin/cloudflared https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x /usr/local/bin/cloudflared
```

Or download manually from [Cloudflare Downloads](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/).

## CLI Reference

```
python scripts/glmv_caption.py (--images IMG [...] | --videos VID [...] | --files FILE [...]) [OPTIONS]
```

| Parameter | Description |
|---|---|
| `--images`, `-i` | Image paths or URLs (multiple OK, base64 OK) |
| `--videos`, `-v` | Video paths or URLs (multiple OK, local paths auto-tunneled) |
| `--files`, `-f` | Document paths or URLs (multiple OK, local paths auto-tunneled) |
| `--prompt`, `-p` | Custom prompt |
| `--model`, `-m` | Model name (default: `glm-5v-turbo`) |
| `--temperature`, `-t` | Sampling temperature 0–1 (default: 0.8) |
| `--top-p` | Nucleus sampling 0.01–1.0 (default: 0.6) |
| `--max-tokens` | Max output tokens (default varies by model, max 32768) |
| `--thinking` | Enable thinking/reasoning mode |
| `--response-format` | Enable structured output; when present without a value, uses `json_object` |
| `--sys-prompt` | System prompt inserted before the user message; recommended for defining JSON shape |
| `--output`, `-o` | Save result JSON to file |
| `--pretty` | Pretty-print JSON output |
| `--stream` | Enable streaming output |

### Structured Output

Pass `--response-format` to include BigModel's OpenAI-compatible JSON mode payload:

```json
{
  "response_format": {"type": "json_object"}
}
```

For reliable results, pair it with `--sys-prompt` that states the exact JSON fields and types you expect. If `--response-format` is omitted, requests behave like before and no `response_format` field is sent.

## File Structure

```
├── SKILL.md                  # Skill manifest (for AI agent frameworks)
├── README.md                 # This file
└── scripts/
    ├── glmv_caption.py       # Main CLI script (modified from original)
    └── tunnel_server.py      # LocalTunnel context manager (new)
```

## Supported Input Types

| Type | Formats | Max Size | Local Path |
|---|---|---|---|
| Image | jpg, png, jpeg | 5MB / 6000×6000px | ✅ via base64 |
| Video | mp4, mkv, mov | 200MB | ✅ via tunnel |
| File | pdf, docx, txt, xlsx, pptx, jsonl | — | ✅ via tunnel |

## Security Notes

- The tunnel **only exists for the duration of the API call** (seconds to minutes), then is immediately destroyed
- **Only the files you explicitly pass** are exposed — no directory listing, no other files
- `cloudflared` does not run persistently or start on boot
- No Cloudflare account registration is required (uses free trycloudflare.com quick tunnels)

## Credit

Based on [zai-org/GLM-skills](https://github.com/zai-org/GLM-skills) — the original `glmv-caption` skill by the Zai team.

Changes are limited to:
- Adding `scripts/tunnel_server.py` (new file)
- Modifying `scripts/glmv_caption.py` to auto-tunnel local video/file paths instead of rejecting them
- Adding optional structured JSON output support via `--response-format` and `--sys-prompt`
- Updating `SKILL.md` to document the new capability and the cloudflared installation flow for AI agents

## License

The original GLM-skills repository does not specify a license. `cloudflared` is Apache 2.0 licensed by Cloudflare.
