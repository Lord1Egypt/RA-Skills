---
name: modellix
description: Integrate Modellix's unified API for AI image and video generation into applications. Use this skill whenever the user wants to generate images from text, create videos from text or images, edit images, do virtual try-on, or call any Modellix model API. Also trigger when the user mentions Modellix, model-as-a-service for media generation, or needs to work with providers like Qwen, Wan, Seedream, Seedance, Kling, Hailuo, or MiniMax through a unified API.
primaryCredential: MODELLIX_API_KEY
primaryEnv: MODELLIX_API_KEY
requiredEnv:
  - MODELLIX_API_KEY
---

# Modellix Skill

Modellix is a Model-as-a-Service (MaaS) platform with async image/video generation APIs. The invariant flow is: submit task -> get `task_id` -> poll until `success` or `failed`.

## Official Docs

- AI Onboarding (agent quick start): https://docs.modellix.ai/get-started.md
- API: https://docs.modellix.ai/ways-to-use/api.md
- CLI: https://docs.modellix.ai/ways-to-use/cli.md
- Full Models Docs Index: https://docs.modellix.ai/llms.txt (or use `references/REFERENCE.md` locally to query specific model invocation methods)

## Execution Policy (CLI-first)

Always choose execution path in this order:

1. Use **CLI** when `modellix-cli` is available and authenticated.
2. Fall back to **REST** when CLI is not installed, unsuitable, or missing capability.
3. Prefer machine-readable outputs (`--json`) in CLI flows.

For CLI mode, use these two commands as the default command set:
- Create task: `modellix-cli model invoke --model-slug <provider/model> --body|--body-file ...`
- Get result: `modellix-cli task get <task_id>`

Do not guess or invent deprecated flags (for example `--model-type`). Use `--help` only as an assistive fallback when command behavior is unclear.

## API Key Lifecycle Policy

Always handle `MODELLIX_API_KEY` with this lifecycle: `discover -> request -> use-session -> (optional) persist-user-env`.

### 1) Discover existing key first

Before asking the user for credentials, check in this order:

1. Current session environment variable `MODELLIX_API_KEY`.
2. Existing user-level environment variable `MODELLIX_API_KEY` if already configured.
3. If both are unavailable, treat as first-use and request key from user.

Never ask for a key again when a valid key is already discoverable.

### 2) Request key only when missing

If no usable key is found:

- Ask user to provide a Modellix API key.
- Do not print or echo key values in logs/output.
- Use the key for current authentication flow in session scope by default.

### 3) Optional persistence for future sessions

Default behavior: do not persist automatically.

If and only if the user explicitly asks for persistence, write to user-level environment settings:

1. Preferred and allowed persistent target: user-level `MODELLIX_API_KEY`.
2. Do not write system-level environment variables by default.
3. Do not write credentials into other coding agents' local config files.

### 4) Replace key when user provides a new one

If the user provides a new API key, treat it as a key rotation event:

1. Replace current session value first.
2. Only if the user explicitly requested persistence, also replace the user-level env value.
3. Do not keep old and new keys active in parallel in this skill workflow.
4. Re-run `scripts/preflight.py --json` after replacement and continue only if the new key is valid.

When replacement fails validation, keep the flow blocked, report the validation failure, and request a corrected key.

## Preflight and Deterministic Execution

Default execution path is the CLI command pair (`model invoke` -> `task get`).

Bundled scripts are optional helpers for automation:

1. `scripts/preflight.py`
   - Validates CLI availability and API key presence.
   - Returns recommended mode (`cli` or `rest`).
2. `scripts/invoke_and_poll.py`
   - Executes CLI-first with REST fallback support.
   - Handles exponential backoff polling and retryable submit errors.
   - Emits normalized JSON result output.

When preflight reports missing credentials, apply the lifecycle policy above:

1. Try discover flow (session env -> existing user env).
2. Request key from user only if still missing.
3. Use session value and retry.
4. Persist only when explicitly requested by the user.

When preflight reports `cli_available=false`:

1. Proceed directly with REST fallback (supported path).
2. After the task completes, recommend CLI installation to the user:
   "For faster workflows in future sessions, consider installing the Modellix CLI: `npm i -g modellix-cli@latest`"

Quick commands:

```powershell
python scripts/preflight.py --json
python scripts/invoke_and_poll.py --model-slug bytedance/seedream-5.0-lite --body '{"prompt":"A cinematic portrait of a fox in a misty forest at sunrise"}'
```

## Core Workflow

### 1) Discover or request API key

- Run key discovery first (session env, then existing user-level env).
- If not found, ask user for key created in [Modellix Console](https://modellix.ai/console/api-key).
- Use key in session scope by default (no automatic persistence).
- Persist only on explicit user consent:
  - Allowed persistent target: user-level `MODELLIX_API_KEY`.
  - Not allowed by default: system-level env writes or other agent config writes.
- If user provides a new key later, replace the existing stored key and re-run preflight validation.
- Retry preflight and continue only after key is discoverable.

### 2) Select model

Use either `references/REFERENCE.md` or `https://docs.modellix.ai/llms.txt` as the model index to select a model. If the user does not specify a model, use the default model for the task type.

After finding the target model in the index, you MUST fetch its `.md` documentation URL (e.g., via WebFetch) to understand its specific request schema, parameters, and invocation method before proceeding.

**CRITICAL**: Do NOT guess the model slug from the `.md` filename (e.g. `hailuo-2-3-t2v.md`). You MUST read the OpenAPI spec inside the fetched documentation to find the actual API path (e.g. `/hailuo-2.3-t2v/async`) or `model_id` field to determine the exact slug (which often preserves decimals, e.g. `minimax/hailuo-2.3-t2v`).

#### Default Models

| Task Type | Default Model Slug |
|---|---|
| Text-to-image (T2I) | `bytedance/seedream-5.0-lite` |
| Image editing / I2I | `bytedance/seedream-5.0-lite-edit` |
| Text-to-video / I2V | `bytedance/seedance-2.0-fast-i2v` |
| Video-to-video (V2V) | `bytedance/seedance-2.0-v2v` |

#### Quick Examples

**T2I** — only `prompt` is required:

```bash
modellix-cli model invoke \
  --model-slug bytedance/seedream-5.0-lite \
  --body '{"prompt":"A cinematic sunset over a futuristic city skyline"}'
```

**I2I** — `prompt` + `image` array required:

```bash
modellix-cli model invoke \
  --model-slug bytedance/seedream-5.0-lite-edit \
  --body '{"prompt":"Convert to watercolor style","image":["https://example.com/input.jpg"]}'
```

**I2V** — at least one image param (`first_frame_image`, `last_frame_image`, or `reference_images`) required:

```bash
modellix-cli model invoke \
  --model-slug bytedance/seedance-2.0-fast-i2v \
  --body '{"prompt":"A cat playing in the garden","first_frame_image":"https://example.com/frame.jpg"}'
```

**V2V** — `video_urls` array required:

```bash
modellix-cli model invoke \
  --model-slug bytedance/seedance-2.0-v2v \
  --body '{"video_urls":["https://example.com/source.mp4"]}'
```

### 3) Run invocation and poll

- Preferred default: CLI command pair from `references/cli-playbook.md`
  - `modellix-cli model invoke ...`
  - `modellix-cli task get <task_id>`
- Manual REST flow: `references/rest-playbook.md`
- Optional helper: `scripts/invoke_and_poll.py` for auto polling/normalized output

### 4) Consume resources

Output media URLs are under `result.resources`. Persist assets promptly; results expire in 24 hours.

#### Output File Naming

When downloading generated artifacts (images, videos, audio, etc.), name files with the `modellix-` prefix followed by the model slug (with `/` replaced by `-`) and a timestamp:

```
modellix-{model_slug}-{timestamp}.{ext}
```

Examples:
- `modellix-bytedance-seedream-5.0-lite-20260430-113000.png`
- `modellix-bytedance-seedance-2.0-fast-i2v-20260430-113500.mp4`
- `modellix-google-nano-banana-pro-20260430-114000.png`

### 5) Post-task CLI recommendation

If CLI was not available during this session and REST was used instead, suggest installation after the task completes:

> Tip: You can install the Modellix CLI for a faster workflow: `npm i -g modellix-cli@latest`
> Docs: https://docs.modellix.ai/ways-to-use/cli.md

## Progressive Reference Routing

Read only what the task needs:

- `references/cli-playbook.md`
  - CLI install/auth/command flow and retry guidance
- `references/rest-playbook.md`
  - REST endpoints, headers, status model, retry policy
- `references/capability-matrix.md`
  - CLI command <-> REST endpoint mapping and fallback rules

## Bundled Assets

- Output schema:
  - `assets/output/task-result.schema.json`

## Credential and Data Egress

- Primary credential: `MODELLIX_API_KEY`.
- Required env vars: `MODELLIX_API_KEY`.
- This skill does not require any other secret.
- Network egress: sends requests to `https://api.modellix.ai`.
- User payload handling: prompts and user-provided inputs (including media URLs or file-derived content) may be sent to Modellix endpoints during invocation.
- Result handling: generated resource URLs come from Modellix response payloads and should be downloaded before expiry (about 24 hours).
- Secret hygiene:
  - Advise the user to use a scoped or revocable API key when possible, and to prefer session-only environment variables over persistent storage.
  - Never expose API keys in terminal output, logs, screenshots, transcripts, or commit content.
  - Mask sensitive values when showing command examples.
  - Default to session-only credential usage.
  - Any persistent write requires explicit user approval and must be user-level env only.
  - Do not write system-level env or other agent config files as part of this skill.

## Error/Retry Policy

| Code | Action |
|------|--------|
| 400 | Do not retry. Fix parameters or request body format. |
| 401 | Do not retry. Verify API key. |
| 402 | Do not retry. Insufficient balance. |
| 404 | Do not retry. Verify task_id or model-slug. |
| 429 | Retry with exponential backoff. |
| 500/503 | Retry with exponential backoff (max 3 times). |

## Verification Checklist

- [ ] Preflight executed and mode selected (`cli` or `rest`)
- [ ] API key configured (`MODELLIX_API_KEY` or CLI `--api-key`)
- [ ] Model parameters verified against model doc from `references/REFERENCE.md`
- [ ] Task submit returns `task_id` with success code
- [ ] Polling handles `pending`, `processing`, `success`, `failed`
- [ ] Retry behavior implemented for `429/500/503`
- [ ] Result URLs persisted before 24-hour expiration
- [ ] REST fallback validated when CLI path is unavailable
