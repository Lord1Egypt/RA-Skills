---
name: prompt-to-drawio
description: Generate and edit draw.io artifacts from natural-language prompts without a frontend. Use when the user asks for prompt-to-diagram workflows that need `.drawio` output, optional image export (`png`/`svg`/`pdf`/`jpg`), context ingestion (image/PDF/text/URL), shape-library lookup, or visual validation loops.
---

# Prompt To Drawio

Use this skill to run a CLI-only version of Next AI Draw.io capabilities.

## Capability Set

1. Prompt -> `.drawio` generation.
2. Prompt-driven edit on existing diagrams (ID-based operations).
3. Optional image export (`png`, `svg`, `pdf`, `jpg`).
4. Context ingestion from local files (`txt/md/json/csv/pdf/image`) and URLs.
5. Shape library documentation injection (`aws4`, `gcp2`, `azure2`, `kubernetes`, etc.).
6. Visual quality validation with retry loops.
7. History snapshot backup before edits.

## Runtime Script

Primary entrypoint:
- `/Users/zhaofengli/.codex/skills/prompt-to-drawio/scripts/prompt_to_drawio.py`

Subcommands:
- `generate`
- `edit`
- `export`
- `validate`
- `library`

Compatibility:
- Legacy usage without subcommand is treated as `generate`.

## Runtime Modes

Mode A (default, recommended): in-session LLM mode
- If the assistant is directly executing this skill inside a Codex/LLM session, generation/edit can be done by the session model itself.
- In this mode, `DRAWIO_LLM_API_KEY` is not required by the skill workflow.

Mode B: standalone CLI mode
- If you run `prompt_to_drawio.py generate|edit|validate` as an independent subprocess that must call a model API by itself, then API key is required.
- Supported env key names: `DRAWIO_LLM_API_KEY` (preferred) or `OPENAI_API_KEY`.
- Default key-loading rule: script auto-loads nearest `.env` from current working directory upward (first match), then reads key variables from it.
- Override dotenv path with `DRAWIO_DOTENV_FILE=/absolute/path/.env`.
- Precedence: CLI flag `--api-key`/`--validation-api-key` > existing process env > auto-loaded `.env`.
- New runtime controls:
  - `--no-dotenv`: disable `.env` auto-loading.
  - `--dotenv-file /abs/path/.env`: use specific dotenv file.
  - `--no-config-summary`: silence startup effective-config print.
  - `--no-model-preflight`: skip provider-side model existence preflight.

Optional env overrides for standalone CLI mode:
```bash
export DRAWIO_LLM_API_KEY="<secret>"
export DRAWIO_LLM_BASE_URL="https://api.openai.com/v1"
export DRAWIO_LLM_MODEL="gpt-4.1"
export DRAWIO_VALIDATION_MODEL="gpt-4.1"
export DRAWIO_VALIDATION_API_KEY="$DRAWIO_LLM_API_KEY"
export DRAWIO_VALIDATION_BASE_URL="$DRAWIO_LLM_BASE_URL"
```

## Google OpenAI-Compatible Example

```bash
export DRAWIO_LLM_API_KEY="<google_ai_studio_key>"
export DRAWIO_LLM_BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai/"
export DRAWIO_LLM_MODEL="gemini-3-pro-preview"

export DRAWIO_VALIDATION_API_KEY="$DRAWIO_LLM_API_KEY"
export DRAWIO_VALIDATION_BASE_URL="$DRAWIO_LLM_BASE_URL"
export DRAWIO_VALIDATION_MODEL="gemini-3-pro-preview"
```

Model naming notes:
- Recommended baseline: `gemini-3-pro-preview` (or latest model shown by provider model listing).
- Avoid stale/nonexistent names such as `gemini-3-pro` unless your provider explicitly lists it.

## Workflows

### 1) Create Diagram

```bash
python3 /Users/zhaofengli/.codex/skills/prompt-to-drawio/scripts/prompt_to_drawio.py generate \
  --prompt "Create a user login + MFA + session flowchart" \
  --out-drawio "/absolute/path/auth-flow.drawio" \
  --out-image "/absolute/path/auth-flow.png" \
  --validate \
  --validate-soft
```

### 2) Create Diagram from Image/PDF/URL Context

```bash
python3 /Users/zhaofengli/.codex/skills/prompt-to-drawio/scripts/prompt_to_drawio.py generate \
  --prompt "Replicate architecture style and improve readability" \
  --file "/absolute/path/reference-arch.png" \
  --file "/absolute/path/requirements.pdf" \
  --url "https://example.com/spec" \
  --shape-library aws4 \
  --out-drawio "/absolute/path/cloud.drawio" \
  --out-image "/absolute/path/cloud.svg"
```

### 3) Edit Existing Diagram

```bash
python3 /Users/zhaofengli/.codex/skills/prompt-to-drawio/scripts/prompt_to_drawio.py edit \
  --in-drawio "/absolute/path/cloud.drawio" \
  --prompt "Add WAF before ALB and split app tier into two services" \
  --out-drawio "/absolute/path/cloud-v2.drawio" \
  --out-image "/absolute/path/cloud-v2.png" \
  --validate
```

### 4) Export Only

```bash
python3 /Users/zhaofengli/.codex/skills/prompt-to-drawio/scripts/prompt_to_drawio.py export \
  --in-drawio "/absolute/path/cloud-v2.drawio" \
  --out-image "/absolute/path/cloud-v2.pdf"
```

### 5) Validation Only

```bash
python3 /Users/zhaofengli/.codex/skills/prompt-to-drawio/scripts/prompt_to_drawio.py validate \
  --in-drawio "/absolute/path/cloud-v2.drawio" \
  --fail-on-critical
```

### 6) Shape Library Discovery

```bash
python3 /Users/zhaofengli/.codex/skills/prompt-to-drawio/scripts/prompt_to_drawio.py library --list
python3 /Users/zhaofengli/.codex/skills/prompt-to-drawio/scripts/prompt_to_drawio.py library --name aws4
```

## Output Contract

Always surface generated file paths exactly as printed by script:
- `DRAWIO_FILE=...`
- `IMAGE_FILE=...` (if requested and successful)
- `BACKUP_FILE=...` (for edits)
- `VALIDATION_JSON=` block when validation runs

Diagnostics:
- On startup, script prints effective runtime config summary to `stderr` (dotenv source, effective model/base-url, key presence mask).
- On JSON parse failures, raw model response is dumped to a temp file and the error includes that path.

Do not claim export success unless target file exists.
