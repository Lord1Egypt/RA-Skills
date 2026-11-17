---
name: modellix
description: Integrate Modellix's unified API for AI image, video, and audio workflows. Use this skill whenever the user wants to generate or edit images, create or transform videos, synthesize speech, transcribe audio, clone a voice, do virtual try-on, or call any Modellix model API. Also trigger when the user mentions Modellix, model-as-a-service for media generation, or providers such as Qwen, Wan, Seedream, Seedance, Kling, Hailuo, MiniMax, Whisper, or CosyVoice through a unified API, or when they ask for a Modellix model's request schema, OpenAPI contract, or required input fields. Prefer modellix-cli (model get-schema, model run --wait, task download, doctor, model list) over hand-rolled REST polling whenever the CLI is available.
license: MIT
compatibility: Requires network access and Node.js 18.17+; Python 3.10+ enables automatic CLI updates and bundled helpers.
metadata:
  author: Modellix
  version: "3.10.0"
  modellix-primary-credential: MODELLIX_API_KEY
  modellix-hermes-tags: creative,image-generation,video-generation,audio-generation,speech-to-text,modellix,cli,api
---

# Modellix Skill

Modellix is a Model-as-a-Service (MaaS) platform for asynchronous image, video, and audio workflows. Prefer the official CLI (`modellix-cli`) so submit, wait, and download stay one coherent workflow. Host-specific persistent session guardrails also ship under `rules/*.mdc`.

## Official Docs

- AI Onboarding: https://docs.modellix.ai/get-started.md
- REST API: https://docs.modellix.ai/ways-to-use/api.md
- Full Models Index: https://docs.modellix.ai/llms.txt
- Docs MCP (search / read docs): https://docs.modellix.ai/mcp
- CLI package (source of truth for CLI behavior): https://www.npmjs.com/package/modellix-cli

### Documentation lookup policy

This plugin may expose the **Modellix Docs MCP** (`.mcp.json` → `https://docs.modellix.ai/mcp`). It is a **read-only documentation** server (`search_modellix`, docs filesystem query, optional feedback). It does **not** submit generation tasks, poll, download, or handle API keys.

When looking up product/API/install docs vs request-body schema:

1. For **request/response schema**, use `modellix-cli model get-schema <slug>` (JSON is the default; the endpoint is public and needs no API key). If CLI is unavailable, use Docs MCP, then `docs_url` from `model describe` or https://docs.modellix.ai/llms.txt.
2. For **product/install narrative**, prefer Docs MCP when the host has it connected (search, then read the matching page). Else use `model describe <slug> --json` → `docs_url`, or browse `llms.txt` and fetch the model `.md`.
3. For **CLI command syntax and flags**, prefer this skill, `references/cli-playbook.md`, the npm README, or `modellix-cli --help` — do **not** trust website CLI pages over the CLI package (docs can lag).

If the Docs MCP exposes a skill resource, treat **this** `SKILL.md` as the execution policy source of truth (CLI-first, defaults, paid-submit safety).

Do not rely on the website CLI guide page for command syntax.

## Execution Policy (CLI-first)

Choose the path in this order:

1. **CLI** after `scripts/preflight.py --json` resolves it. Preflight checks public npm `latest`, installs only a newer exact version before execution, and keeps an existing CLI when update infrastructure is unavailable.
2. **REST** only when CLI is not installed, unsuitable, or missing a needed capability.
3. Prefer machine-readable output (`--json` or `--quiet`) for automation.

Canonical single-task flow:

```bash
python3 scripts/preflight.py --json
modellix-cli doctor --json
modellix-cli model get-schema <provider/model>
modellix-cli model run \
  --model-slug <provider/model> \
  --body '<json>' \
  --wait --timeout 5m --json
modellix-cli task download <task_id> --output-dir ./outputs --json
```

Skip `get-schema` when the skill default plus the example below already lists the required fields, or the user supplied a complete body.

`model invoke` is a compatibility alias of `model run`. New commands should use `model run`.

Do not reinvent polling loops when CLI wait is available. Do not invent deprecated flags (for example `--model-type`). Use `--help` only when behavior is unclear.

## Default Models

When the user does **not** name a model, use these defaults immediately (do not scan the catalog first):

| Task Type | Default Model Slug |
|---|---|
| Text-to-image (T2I) | `google/nano-banana-2-lite` |
| Text-to-video (T2V) | `bytedance/seedance-2.0-mini-t2v` |
| Image editing / I2I | `google/nano-banana-2-lite-edit` |
| Image-to-video / I2V | `bytedance/seedance-2.0-fast-i2v` |
| Video-to-video (V2V) | `bytedance/seedance-2.0-fast-v2v` |
| Text-to-speech (TTS) | `alibaba/qwen-audio-3.0-tts-flash` |
| Speech-to-text (STT) | `openai/whisper-1` |
| Speech-to-speech (STS) | `alibaba/cosyvoice-clone` |

## API Key Lifecycle Policy

Handle credentials as: `discover -> request -> use-session -> (optional) persist`.

### 1) Discover existing key first

Before asking the user:

1. Session / process env `MODELLIX_API_KEY`
2. Saved CLI profile (`modellix-cli auth status` / `doctor` — key via `--profile` or `MODELLIX_PROFILE` or `currentProfile`)
3. If still missing, request a key from the user

Never ask again when a usable key is already discoverable. CLI key resolution order is: `--api-key` → `MODELLIX_API_KEY` → selected saved profile.

### 2) Request key only when missing

- Ask for a key from [Modellix Console](https://modellix.ai/console/api-key).
- Do not print or echo key values.
- Prefer session env for the current run.

### 3) Optional persistence

Default: do not persist automatically.

When the user explicitly asks to persist:

1. Preferred: `modellix-cli auth login` or `modellix-cli init` (CLI validates and stores the profile securely).
2. Alternative: user-level `MODELLIX_API_KEY` only if they insist on env persistence.
3. Do not write system-level env or other agents' config files.

### 4) Key rotation

If the user provides a new key: update session first; if they requested persistence, replace via `auth login`/`init` (or user-level env). Re-check with `modellix-cli doctor --json` (or `scripts/preflight.py --json`) before continuing.

## Preflight and Deterministic Execution

Required first-workflow check when Python 3 is available:

```bash
python3 scripts/preflight.py --json
```

Bundled helpers:

1. `scripts/preflight.py` — checks public npm `latest`, safely updates a missing/older global CLI before paid work, pins newer local installs instead of downgrading, wraps `doctor`, and recommends `cli`, `rest`, or `none`.
2. `scripts/invoke_and_poll.py` — performs the same resolution before submission, pins the resolved executable for the workflow, uses `model run --wait` on CLI, and otherwise keeps the REST submit+poll fallback.

Set `MODELLIX_CLI_AUTO_UPDATE=0` (also accepts `false` or `off`) only when the environment must keep its installed CLI version. A registry/install failure is non-destructive: use the existing CLI if it still passes doctor, or REST when no CLI is usable and a session API key exists. Never update or swap the CLI after a paid submission has started.

When preflight/doctor reports missing credentials, apply the lifecycle above.

When CLI is unavailable:

1. Use REST (`references/rest-playbook.md`).
2. Report the preflight update warning; do not repeatedly attempt installation inside the same paid workflow.

## Core Workflow

### 1) Ready the environment

- Discover or request API key (lifecycle above).
- Run `scripts/preflight.py --json`; continue only with the CLI path whose doctor check passed, or with an authenticated REST fallback.
- Continue only when auth and connectivity look healthy (or REST key is set).

### 2) Select model

1. If the user did not specify a model: use the **Default Models** table (do not scan the catalog first).
2. If they named a model or need discovery: `modellix-cli model list` / `modellix-cli model describe <slug>` (catalog metadata; describe returns `docs_url`).
3. For request body schema: `modellix-cli model get-schema <slug>` (JSON default; public, no API key). Call this when the user named a non-default slug, when the body needs fields beyond the documented examples, after HTTP `400`, or when reporting required fields. Skip when the skill default plus the example already lists required fields, or the user supplied a complete body.
4. If CLI is unavailable for schema or discovery: use Docs MCP or browse `llms.txt`, then fetch the target model `.md`. Do **not** invent slugs from filenames (decimals often matter, e.g. `bytedance/seedance-2.0-mini-t2v`).

### 3) Run and wait

Default (single task):

```bash
modellix-cli model run \
  --model-slug google/nano-banana-2-lite \
  --body '{"prompt":"A cinematic sunset over a futuristic city skyline"}' \
  --wait --timeout 5m --json
```

Split flow when useful (pipelines, concurrency):

```bash
TASK_ID=$(modellix-cli model run --model-slug ... --body '...' --output task-id)
modellix-cli task wait "$TASK_ID" --timeout 10m --json
```

Batch (paid guard required): `modellix-cli model batch tasks.jsonl --max-tasks N [--wait]`.

Manual REST: `references/rest-playbook.md`. Optional helper: `scripts/invoke_and_poll.py`.

### 4) Download results

```bash
modellix-cli task download <task_id> --output-dir ./outputs --json
```

If download fails with `Resource host resolves to a private or reserved network address` (common when a local proxy/VPN maps CDN hosts like `file.modellix.ai` into `198.18.0.0/15`), retry with `--allow-private-network` for trusted Modellix CDN hosts, or fall back to downloading the `result.resources[].url` with `curl`/`wget`.

Resource URLs expire in about 7 days — persist promptly. If downloading manually (REST path), name files:

```
modellix-{model_slug}-{timestamp}.{ext}
```

(replace `/` in the slug with `-`).

Examples:

- `modellix-google-nano-banana-2-lite-20260430-113000.png`
- `modellix-bytedance-seedance-2.0-mini-t2v-20260430-113500.mp4`

### Quick Examples

**T2I** (default model) — `prompt` required:

```bash
modellix-cli model run \
  --model-slug google/nano-banana-2-lite \
  --body '{"prompt":"A cinematic sunset over a futuristic city skyline"}' \
  --wait --timeout 5m --json
```

**T2V** (default model) — `prompt` required:

```bash
modellix-cli model run \
  --model-slug bytedance/seedance-2.0-mini-t2v \
  --body '{"prompt":"A cat playing in a sunny garden"}' \
  --wait --timeout 10m --json
```

**I2I** — `prompt` + `image` array:

```bash
modellix-cli model run \
  --model-slug google/nano-banana-2-lite-edit \
  --body '{"prompt":"Convert to watercolor style","image":["https://example.com/input.jpg"]}' \
  --wait --timeout 5m --json
```

**I2V** — at least one image param (`first_frame_image`, `last_frame_image`, or `reference_images`):

```bash
modellix-cli model run \
  --model-slug bytedance/seedance-2.0-fast-i2v \
  --body '{"prompt":"A cat playing in the garden","first_frame_image":"https://example.com/frame.jpg"}' \
  --wait --timeout 10m --json
```

**V2V** — `video_urls` array:

```bash
modellix-cli model run \
  --model-slug bytedance/seedance-2.0-fast-v2v \
  --body '{"video_urls":["https://example.com/source.mp4"]}' \
  --wait --timeout 10m --json
```

**TTS** (default model) — `text` + `voice` required (verify voice with `model get-schema` or the model doc; Flash voices only):

```bash
modellix-cli model run \
  --model-slug alibaba/qwen-audio-3.0-tts-flash \
  --body '{"text":"There is a large garden behind my house.","voice":"longanhuan_v3.6"}' \
  --wait --timeout 5m --json
```

**STT** (default model) — public audio `url` required:

```bash
modellix-cli model run \
  --model-slug openai/whisper-1 \
  --body '{"url":"https://example.com/meeting.mp3"}' \
  --wait --timeout 5m --json
```

**STS** (default model) — clone reference `url` + synthesis `text` + target CosyVoice `model`:

```bash
modellix-cli model run \
  --model-slug alibaba/cosyvoice-clone \
  --body '{"model":"cosyvoice-v3.5-plus","url":"https://example.com/reference.wav","text":"There is a large garden behind my house."}' \
  --wait --timeout 5m --json
```

### 5) Post-task CLI recommendation

If this session used REST because CLI was missing, suggest installing the CLI afterward.

## Progressive Reference Routing

Read only what the task needs:

- `references/cli-playbook.md` — install, auth, run/wait/download, batch, recovery
- `references/rest-playbook.md` — REST submit/poll when CLI is unavailable
- `references/capability-matrix.md` — CLI ↔ REST mapping and fallback rules

## Bundled Assets

- `assets/output/task-result.schema.json`

## Credential and Data Egress

- Primary credential: `MODELLIX_API_KEY` (also via CLI profiles).
- Network egress: `https://api.modellix.ai` (override only with trusted `--base-url` / `MODELLIX_BASE_URL`).
- User prompts and media inputs may be sent to Modellix during invocation.
- Never expose API keys in logs, screenshots, transcripts, or commits.
- Default to session-only credentials; persistent writes need explicit user approval.

## Error / Retry Policy

| Situation | Action |
|------|--------|
| HTTP/API `400` | Do not retry. Fix parameters or body (`model get-schema` when the contract is unclear). |
| `401` | Do not retry. Fix key (`doctor`, `auth login`). |
| `402` | Do not retry. Insufficient balance. |
| `404` | Do not retry. Verify `task_id` or model slug. |
| `429` / read-only `5xx` | CLI already retries safe GETs within deadline; do not blindly re-POST paid submits. |
| Paid submit outcome **unknown** | Do **not** immediately re-run the same `model run`. Check `task history`, console activity, and any printed task ID first. |
| Exit `124` | Local wait timeout; remote task may still run — recover with `task wait` / `task get`, then `task download`. |
| Exit `2` | Argument or safety guard (e.g. batch cost limit) — fix flags. |

## Verification Checklist

- [ ] Doctor/preflight passed or REST key ready
- [ ] Model chosen (default table or user/catalog)
- [ ] Body schema checked via `model get-schema` when non-trivial (or model doc when CLI is unavailable)
- [ ] Used `model run --wait` (or `task wait`) instead of hand-rolled poll loops
- [ ] Results downloaded (`task download` or manual persist before 7-day expiry)
- [ ] No blind retry after unknown paid submission
- [ ] REST used only when CLI path unavailable
