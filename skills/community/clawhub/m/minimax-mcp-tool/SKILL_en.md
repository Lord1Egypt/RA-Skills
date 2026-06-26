# minimax-websearch 🦞

> A wrapper for MiniMax Token Plan's built-in web_search tool. Free, zero-configuration, no C: drive clutter.

---

## What Does This Skill Do?

MiniMax Token Plan includes a web_search tool, but running it via `uvx minimax-coding-plan-mcp` fails on Windows with an asyncio DLL error. This skill works around that, giving you MiniMax search directly inside OpenClaw.

**Highlights:**
- Completely free (uses your own subscription quota)
- Zero C: drive usage (venv + cache on E: drive)
- Credentials never hardcoded in files (injected via environment variables)
- Auto-fallback to Brave Search / Qwen Chat when subscription expires

---

## Prerequisites

### 1. Python Environment (if not already set up)

```powershell
# Create venv (E: drive, no C: usage)
python -m venv E:\.uv-venv

# Install MCP package
E:\.uv-venv\Scripts\pip.exe install minimax-coding-plan-mcp
```

### 2. Configure API Key

Add to `openclaw.json` under `env`:

```json
{
  "env": {
    "MINIMAX_API_KEY": "your MiniMax API Key"
  }
}
```

Restart the Gateway for changes to take effect.

---

## Status Configuration

```json
{ "enabled": true }
```

| Value | Behavior |
|-------|----------|
| `true` | Use MiniMax search |
| `false` | Fallback to Brave Search / Qwen Chat |

**Subscription expiry signal:** errors `401` / `403` / `authentication failed`
→ Switch to `enabled: false` to activate fallback; set back to `true` after renewing.

---

## Usage

### Web Search

```bash
node skills/minimax-mcp/scripts/minimax_mcp.js search "search query"
```

**Output format:**

```json
{
  "query": "LLM engineer salary China 2026",
  "count": 10,
  "results": [
    {
      "title": "...",
      "link": "https://...",
      "snippet": "...",
      "date": "2026-03-24"
    }
  ],
  "related": [{ "query": "related search term" }]
}
```

### Image Understanding

```bash
node skills/minimax-mcp/scripts/minimax_mcp.js image "analysis prompt" "image path or URL"
```

**Examples:**

```bash
# Local file
node skills/minimax-mcp/scripts/minimax_mcp.js image "describe what's in this screenshot" "E:\path\to\screenshot.png"

# Web image
node skills/minimax-mcp/scripts/minimax_mcp.js image "what does this image show?" "https://example.com/image.jpg"
```

**Supported formats:** JPEG, PNG, WebP (max 20MB)
**Returns:** Text description of the image

---

## Fallback Chain

When MiniMax subscription is unavailable, set `enabled: false` and the skill will route through:

1. **Brave Search** — OpenClaw's built-in `web_search` tool
2. **Qwen Chat** — Chrome Relay → chat.qwen.ai search

---

## Directory Structure

```
skills/minimax-mcp/
├── SKILL.md
├── SKILL_en.md
├── config.json          ← No keys, only HOST default
└── scripts/
    └── minimax_websearch.js
```

---

## Technical Details

| Item | Description |
|------|-------------|
| Python environment | `E:\.uv-venv` (Python 3.11, E: drive only) |
| Package cache | `E:\.uv-cache` (no C: usage) |
| MCP package | `minimax-coding-plan-mcp==0.0.4` |
| Credentials | Read from `MINIMAX_API_KEY` env var, never in files ✅ |
| Python path | Read from `MINIMAX_PYTHON` env var (default `E:\.uv-venv\Scripts\python.exe`) |
| Communication | stdio JSON-RPC, no OpenClaw port required |
| Tools | `web_search` (search) + `understand_image` (image understanding) |

---

## Known Issues

### `uvx` Has asyncio DLL Problems on Windows 🔴

`uvx minimax-coding-plan-mcp` fails with `_overlapped import failed`. Use `E:\.uv-venv\Scripts\python.exe -m minimax_mcp.server` instead — never uvx.

### `.uv-venv` SSL Certificate Issue

On some Windows environments the `.uv-venv` SSL certificate store may be empty, causing HTTPS errors. The script automatically sets `REQUESTS_CA_BUNDLE` to point to certifi's CA bundle — no manual action needed.

---

## Changelog

- **2026-03-24** v2.1: Added `understand_image` tool for image analysis (local files + URLs)
- **2026-03-24** v2: Fixed review issues (credentials via env vars, no hardcoded paths, SSL cert fix)

*🦞 Created by godiao — MIT License*
