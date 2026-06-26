---
name: gpt-image-2
description: Generate and edit images via OpenAI gpt-image-2 model. Agent-agnostic CLI — works with any AI agent (Hermes, Claude Code, Codex, OpenClaw, etc.). Supports configurable base_url/api_key, text-to-image and image-to-image editing.
version: 2.0.0
author: AI Agent Toolkit
license: MIT
metadata:
  tags: [image, generation, openai, gpt-image-2, text-to-image, image-editing, agent-agnostic]
  related_skills: [gemini-image-gen]
---

# gpt-image-2

Generate and edit images via OpenAI's gpt-image-2 model. **Agent-agnostic** — designed to work with any AI agent or standalone from the command line.

## Quick Start

```bash
# 1. Initialize config (one-time)
python3 gpt_image2.py config --init

# 2. Edit the config to set your API key
#    ~/.config/gpt-image-2/config.json

# 3. Generate
python3 gpt_image2.py generate "A cute cat on a windowsill" -o ~/cat.png --quality low

# 4. Edit
python3 gpt_image2.py edit input.png "Change the sofa to green" -o ~/output.png
```

## Configuration

Config priority: `--config` flag > `--base-url`/`--api-key` flags > config file > environment variables > defaults.

### Config File Locations (in priority order)

| Priority | Path | Notes |
|----------|------|-------|
| 1 | `$XDG_CONFIG_HOME/gpt-image-2/config.json` | XDG standard (recommended) |
| 2 | `~/.config/gpt-image-2/config.json` | Default XDG fallback |
| 3 | `~/.gpt-image-2-config.json` | Single-file fallback |
| 4 | `~/.hermes/gpt-image-2-config.json` | Legacy Hermes compat |

Use `python3 gpt_image2.py config --show` to see which config is active.

### Config File Format

```json
{
  "base_url": "https://api.openai.com/v1",
  "api_key_env": "OPENAI_API_KEY"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `base_url` | string | API base URL. Default: `https://api.openai.com/v1` |
| `api_key` | string | Plaintext API key (**not recommended** — visible in file) |
| `api_key_env` | string | Environment variable name holding the key (**recommended**) |

### Environment Variables (fallback when no config file)

| Variable | Purpose |
|----------|---------|
| `GPT_IMAGE2_API_KEY` | API key |
| `GPT_IMAGE2_BASE_URL` | API base URL |

### Config Management Commands

```bash
# Create template config
python3 gpt_image2.py config --init

# Show active config (keys are masked)
python3 gpt_image2.py config --show

# Overwrite config
python3 gpt_image2.py config --init --force
```

## CLI Reference

### generate — Text-to-Image

```bash
python3 gpt_image2.py generate "prompt" [options]
```

| Option | Default | Description |
|--------|---------|-------------|
| `-o, --output` | `~/gpt-image2-output.png` | Output file path |
| `--quality` | `auto` | `low` (~70s), `medium` (~120s), `high` (~276s) |
| `--size` | `auto` | `1024x1024`, `1536x1024`, `1024x1536` |
| `--format` | `png` | `png`, `jpeg`, `webp` |
| `--n` | `1` | Number of images (1-10) |
| `--timeout` | `600` | curl timeout in seconds |
| `--config` | auto-detect | Explicit config file path |
| `--base-url` | from config | Override API base URL |
| `--api-key` | from config | Override API key (visible in ps!) |

### edit — Image-to-Image

```bash
python3 gpt_image2.py edit <image_path> "edit prompt" [options]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--mask` | none | PNG mask (transparent=edit area) |
| `--moderation` | `auto` | `low` or `auto` |
| (all generate options also apply) | | |

### config — Manage Configuration

```bash
python3 gpt_image2.py config [--init] [--show] [--force] [--config PATH]
```

## Script Location

The script is at `scripts/gpt_image2.py` relative to this skill directory.

To find it programmatically from any agent:

```bash
# If installed as a Hermes skill:
SCRIPT="$(dirname "$(readlink -f "$0")")/../skills/creative/gpt-image-2/scripts/gpt_image2.py"

# Or copy/symlink it anywhere — it's self-contained with zero dependencies beyond stdlib + curl
cp scripts/gpt_image2.py /usr/local/bin/gpt-image2
```

The script has **zero pip dependencies** — only Python 3.8+ stdlib and `curl`.

## API Reference

### Generations (Text-to-Image)

| Item | Value |
|------|-------|
| Endpoint | `POST {base_url}/images/generations` |
| Auth | `Authorization: Bearer {api_key}` |
| Content-Type | `application/json` |

### Edits (Image-to-Image)

| Item | Value |
|------|-------|
| Endpoint | `POST {base_url}/images/edits` |
| Auth | `Authorization: Bearer {api_key}` |
| Content-Type | `multipart/form-data` |

### Parameters

**Generations (JSON body):**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `model` | string | yes | `gpt-image-2` |
| `prompt` | string | yes | Text description |
| `n` | int | no | Number of images (default 1) |
| `size` | string | no | `1024x1024`, `1536x1024`, `1024x1536` |
| `quality` | string | no | `low`, `medium`, `high` (default `auto`) |
| `format` | string | no | `png`, `jpg`, `webp` (default `png`) |

**Edits (form-data):**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `model` | string | yes | `gpt-image-2` |
| `prompt` | string | yes | Edit instruction |
| `image` | file | yes | Source image (PNG, max 4 images) |
| `n` | int | no | Number of outputs (default 1) |
| `size` | string | no | `1024x1024`, `1536x1024`, `1024x1536`, or `auto` |
| `quality` | string | no | `low`, `medium`, `high` (default `auto`) |

## Agent Integration Guide

This skill is designed to be **agent-agnostic**. Any AI agent can use it by:

1. **Locate the script**: Find `gpt_image2.py` in the skill's `scripts/` directory
2. **Call via shell**: `python3 <path>/gpt_image2.py generate "prompt" -o output.png`
3. **Parse stdout**: The script prints `Saved: <path> (<size> KB)` on success

### Integration Examples

**Hermes / Claude Code / Codex / OpenClaw:**
```bash
python3 /path/to/gpt-image-2/scripts/gpt_image2.py generate "prompt" -o output.png --quality low
```

**From Python (any agent):**
```python
import subprocess, json
result = subprocess.run(
    ["python3", script_path, "generate", prompt, "-o", output_path, "--quality", "low"],
    capture_output=True, text=True, timeout=600
)
# Parse result.stdout for "Saved: <path>"
```

**From Node.js / TypeScript:**
```javascript
const { execSync } = require('child_process');
const output = execSync(`python3 ${scriptPath} generate "${prompt}" -o ${outputPath}`);
// Parse output.toString() for "Saved: ..."
```

## Workflow: Agent Generates Images

1. **Always use the CLI script** — handles config resolution, auth security, and response parsing
2. **Use low quality for drafts**, high quality for final output
3. **For edits**: `--size auto` preserves original dimensions (recommended)
4. **The script outputs**: HTTP status, time elapsed, output file path and size
5. **Parse the output**: look for `Saved: <path>` lines to find generated files

## Workflow: Agent Edits Existing Images

1. Save or locate the source image path
2. Call `gpt_image2.py edit <image_path> "<edit_prompt>" --output <output_path>`
3. Edit endpoint can accept up to 4 images via repeated `--image` flags
4. Use `--size auto` to preserve original dimensions

## Important Pitfalls

1. **`--api-key` flag is visible in shell history and `ps aux`** — prefer config file (`api_key_env`) or environment variables.
2. **The edits endpoint does NOT support `response_format`** — always returns b64_json regardless.
3. **gpt-image-2 generations may time out on some relay endpoints** — use `--timeout` flag (default 600s).
4. **Prompt with special characters** — the script writes prompts to temp files internally, avoiding shell escaping issues. No need to worry about quoting.
5. **Authorization header is never passed via `-H`** — the script uses curl `-K` temp config file, deleted immediately after use. Keys never appear in `ps aux`.
6. **Config file permissions** — the script warns if config has group/other read permissions. Run `chmod 600 <config>` to fix.
7. **Zero pip dependencies** — the script only requires Python 3.8+ stdlib and `curl`. No installation step needed.
8. **Chinese text in prompts may not render correctly** — gpt-image-2's Chinese rendering is unstable; it often ignores Chinese constraints and outputs English text in images. Consider using Gemini for Chinese text rendering.
