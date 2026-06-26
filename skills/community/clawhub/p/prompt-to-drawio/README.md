# prompt-to-drawio

[English](README.md) | [简体中文](README.zh-CN.md)

A CLI-first Codex skill to generate/edit/export/validate draw.io diagrams from natural language prompts, without any frontend.

## Installation

### Option A: Multi-Agent via `npx skills` (Recommended)

Use [`npx skills`](https://github.com/vercel-labs/skills) if you want one installer entry across Codex / Claude Code / other supported agents.

Install for detected/default agent:

```bash
npx skills@latest add lzfxxx/prompt-to-drawio-skill
```

Install for Codex only:

```bash
npx skills@latest add lzfxxx/prompt-to-drawio-skill -a codex
```

Install for Claude Code only:

```bash
npx skills@latest add lzfxxx/prompt-to-drawio-skill -a claude-code
```

Global install (shared across projects):

```bash
npx skills@latest add lzfxxx/prompt-to-drawio-skill -g -y
```

Notes:

- `npx skills` is a community/open-source installer, not an official built-in command of every agent product.
- If your environment does not support it, use the manual installation section below.

### Option B: Manual Fallback (Codex Local Install)

```bash
mkdir -p "$HOME/.codex/skills"
git clone https://github.com/lzfxxx/prompt-to-drawio-skill.git "$HOME/.codex/skills/prompt-to-drawio"
```

### Update to latest

```bash
git -C "$HOME/.codex/skills/prompt-to-drawio" pull
```

## What This Skill Does

- Generate `.drawio` from prompt
- Edit existing `.drawio` by prompt
- Export to `png/svg/pdf/jpg`
- Ingest context from files / URLs / images / PDF
- Query draw.io shape library references
- Run visual validation with retry loop

## Repository Structure

- `SKILL.md`: skill instructions for Codex
- `scripts/prompt_to_drawio.py`: runtime CLI
- `references/`: capability and rendering notes
- `agents/openai.yaml`: assistant interface metadata

## Prerequisites

- Python `3.9+`
- draw.io CLI: `drawio`
- Network access to your model provider endpoint

Quick checks:

```bash
python3 --version
drawio --help
```

## Configuration

The script supports OpenAI-compatible APIs. Put env vars in your project `.env` or shell env.

### Google Gemini (OpenAI-compatible) example

```env
DRAWIO_LLM_API_KEY=YOUR_API_KEY
DRAWIO_LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
DRAWIO_LLM_MODEL=gemini-3-pro-preview

DRAWIO_VALIDATION_API_KEY=YOUR_API_KEY
DRAWIO_VALIDATION_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
DRAWIO_VALIDATION_MODEL=gemini-3-pro-preview
```

Model naming notes:

- Recommended baseline: `gemini-3-pro-preview`
- Avoid stale names such as `gemini-3-pro` unless provider model listing confirms availability

## Runtime Config Controls

- `--no-dotenv`: disable auto-loading `.env`
- `--dotenv-file /abs/path/.env`: use specified `.env`
- `--no-config-summary`: silence startup effective-config summary
- `--no-model-preflight`: skip `/models` preflight check

Dotenv behavior:

- By default, script searches nearest `.env` from current working directory upward
- Precedence: CLI args > existing process env > auto-loaded `.env`

## Usage

### Generate a new diagram

```bash
python3 "$HOME/.codex/skills/prompt-to-drawio/scripts/prompt_to_drawio.py" generate \
  --prompt "Create a login + MFA + session flow" \
  --out-drawio "/tmp/auth-flow.drawio" \
  --out-image "/tmp/auth-flow.pdf" \
  --validate \
  --validate-soft
```

### Generate with context files/URL/library

```bash
python3 "$HOME/.codex/skills/prompt-to-drawio/scripts/prompt_to_drawio.py" generate \
  --prompt "Replicate architecture style and improve readability" \
  --file "/abs/path/requirements.pdf" \
  --file "/abs/path/reference.png" \
  --url "https://example.com/spec" \
  --shape-library aws4 \
  --out-drawio "/tmp/cloud.drawio" \
  --out-image "/tmp/cloud.svg"
```

### Edit an existing diagram

```bash
python3 "$HOME/.codex/skills/prompt-to-drawio/scripts/prompt_to_drawio.py" edit \
  --in-drawio "/tmp/cloud.drawio" \
  --prompt "Add WAF before ALB and split app tier into two services" \
  --out-drawio "/tmp/cloud-v2.drawio" \
  --out-image "/tmp/cloud-v2.png" \
  --validate \
  --validate-soft
```

### Export only

```bash
python3 "$HOME/.codex/skills/prompt-to-drawio/scripts/prompt_to_drawio.py" export \
  --in-drawio "/tmp/cloud-v2.drawio" \
  --out-image "/tmp/cloud-v2.pdf"
```

### Validation only

```bash
python3 "$HOME/.codex/skills/prompt-to-drawio/scripts/prompt_to_drawio.py" validate \
  --in-drawio "/tmp/cloud-v2.drawio" \
  --fail-on-critical
```

### Shape library discovery

```bash
python3 "$HOME/.codex/skills/prompt-to-drawio/scripts/prompt_to_drawio.py" library --list
python3 "$HOME/.codex/skills/prompt-to-drawio/scripts/prompt_to_drawio.py" library --name aws4
```

## Output Contract

On success, runtime prints machine-readable lines:

- `DRAWIO_FILE=...`
- `IMAGE_FILE=...` (if requested)
- `BACKUP_FILE=...` (for edit)
- `VALIDATION_JSON=` block (when validation runs)

## Important Notes

- Startup prints effective runtime config (dotenv source, effective model/base URL, API key masked status)
- JSON parsing is hardened for fenced/truncated outputs; raw failing response is dumped to temp file on unrecoverable parse failure
- `--validate-soft` keeps `generate/edit` returning `0` if files were produced but validation request/parse failed
- Prefer exporting paper figures as `pdf/svg` for final publication quality

## Troubleshooting

### `HTTP 404 ... model not found`

- Check startup summary for effective model name
- Use model listed by provider
- For Gemini, try `gemini-3-pro-preview`

### `Network error calling model endpoint`

- Check DNS/network access to provider host
- In restricted environments/sandboxes, rerun with network-enabled permissions

### Looks like env is set but script uses different values

- Script auto-loads nearest `.env` unless `--no-dotenv` is set
- Use `--dotenv-file` for explicit selection
- Check startup config summary to verify effective values

## Attribution

This project is built on ideas and capabilities from the excellent upstream project:

- [DayuanJiang/next-ai-draw-io](https://github.com/DayuanJiang/next-ai-draw-io)

The current repository repackages and hardens the workflow for CLI/agent skill usage (Codex, Claude Code, and other agent environments), while preserving the prompt-to-diagram direction inspired by the upstream work.

## License

MIT
