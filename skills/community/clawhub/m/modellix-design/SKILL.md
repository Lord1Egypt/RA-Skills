---
name: modellix-design
description: Integrate Modellix's unified API for AI image, video, and audio workflows. Use this skill whenever the user wants to generate or edit images, create or transform videos, synthesize speech, transcribe audio, clone a voice, do virtual try-on, or call any Modellix model API. Also trigger when the user mentions Modellix, model-as-a-service for media generation, or providers such as Qwen, Wan, Seedream, Seedance, Kling, Hailuo, MiniMax, Whisper, or CosyVoice through a unified API, or when they ask for a Modellix model's request schema, OpenAPI contract, or required input fields. When the Modellix Media Generation MCP tools are available and the input is not a local file, submit through that MCP. Otherwise prefer modellix-cli (model get-schema, model run --wait, task download, doctor, model list). Use REST only when both the Media Generation MCP and the CLI are unavailable.
license: MIT
compatibility: Requires network access and Node.js 18.17+; Python 3.10+ enables automatic CLI updates and bundled helpers.
metadata:
  author: Modellix
  version: "4.14.0"
  modellix-primary-credential: MODELLIX_API_KEY
  modellix-hermes-tags: creative,image-generation,video-generation,audio-generation,speech-to-text,modellix,cli,api
---

# Modellix Skill

Modellix is a Model-as-a-Service (MaaS) platform for asynchronous image, video, and audio workflows. When the host has connected **Modellix Media Generation**, use that MCP for a prompt or public URL. Use the official CLI (`modellix-cli`) when the MCP tools are absent, the client rejects the MCP protocol, or the input is a local file. Host-specific persistent session guardrails also ship under `rules/*.mdc`.

After files are on disk, local trimming, concatenation, reframing, and transcoding belong to `modellix-ffmpeg`.

## Official Docs

- AI Onboarding: https://docs.modellix.ai/get-started.md
- REST API: https://docs.modellix.ai/ways-to-use/api.md
- Full Models Index: https://docs.modellix.ai/llms.txt
- Docs Search MCP (search / read docs): https://docs.modellix.ai/mcp
- Media Generation MCP: https://tool.modellix.ai/mcp/media
- Web Tools MCP (public web search / URL fetch): https://docs.modellix.ai/tools/mcp (endpoint https://tool.modellix.ai/mcp)
- CLI package (source of truth for CLI behavior): https://www.npmjs.com/package/modellix-cli

### Documentation lookup policy

This plugin exposes **Modellix Docs Search** (`https://docs.modellix.ai/mcp`). It is a **read-only documentation** server (`search_modellix`, docs filesystem query, optional feedback). It does **not** submit generation tasks, poll, download, or handle API keys.

**Modellix Media Generation** (`https://tool.modellix.ai/mcp/media`) is a separate server. It submits paid image, video, and audio tasks. The host attaches `Authorization: Bearer` from its own secret store. This repository does not put that header in `mcp.json`.

**Modellix Web Tools** (`https://tool.modellix.ai/mcp`) is a separate server. It searches the public web (`modellix-ai/web-search`) and fetches public URLs (`modellix-ai/web-fetch`). Calls are billed. It does not submit image, video, or audio tasks, and it does not replace Docs Search or the CLI. The host attaches `Authorization: Bearer` from its own secret store. This repository does not put that header in `mcp.json`.

When looking up product/API/install docs vs request-body schema:

1. For **request/response schema** on the Media Generation path, call `modellix_get_schema` with the exact `provider/model` slug. On the CLI path, use `modellix-cli model get-schema <slug>` (JSON is the default; the endpoint is public and needs no API key). If neither is available, use Docs Search, then `docs_url` from `model describe` or https://docs.modellix.ai/llms.txt.
2. For **product/install narrative**, prefer Docs Search when the host has it connected (search, then read the matching page). Else use `model describe <slug> --json` → `docs_url`, or browse `llms.txt` and fetch the model `.md`.
3. For **CLI command syntax and flags**, prefer this skill, `references/cli-playbook.md`, the npm README, or `modellix-cli --help` — do **not** trust website CLI pages over the CLI package (docs can lag).

If Docs Search exposes a skill resource, treat **this** `SKILL.md` as the execution policy source of truth (Media Generation MCP, then CLI, then REST; the user names the model; paid-submit safety).

Do not rely on the website CLI guide page for command syntax.

## Execution Policy

Choose one paid path. A second submit of the same request charges again.

1. **Modellix Media Generation** when `modellix_submit_task` is in the tool list and the input is a prompt or public URL. The remote server cannot read a path on this computer, and a protocol error or `401` means this host cannot use the server — both are reasons to leave the path, not to retry it.
2. **CLI** after `scripts/preflight.py --json` resolves it. Run preflight only when this path is selected. Preflight checks public npm `latest`, installs only a newer exact version before execution, and keeps an existing CLI when update infrastructure is unavailable. Use the CLI for local files, batch, `task download`, and private-network CDN fallback.
3. **REST** only when the MCP tools are absent and the CLI is not installed, unsuitable, or missing a needed capability.
4. Prefer machine-readable output (`--json` or `--quiet`) for the CLI and REST paths.

Media Generation flow (details in `references/media-mcp-playbook.md`):

1. Use the `provider/model` slug the user named. If they did not name one, ask which model to run and wait. Do not invent a slug or pick one from a built-in list.
2. Call `modellix_get_schema` with that slug.
3. Confirm the model and input with the user.
4. Call `modellix_submit_task` once and keep `task_id`.
5. Call `modellix_wait_task` until the task is terminal. A deadline with `data.wait.timed_out=true` is a snapshot, not a failure; wait again with the same id.
6. Save `data.result.resources` before they expire (about 7 days).

If `modellix_submit_task` returns `submission_unknown`, or the connection drops before a trustworthy response, do not call `modellix-cli model run` or a REST POST for the same request. Continue with `modellix_get_task` / `modellix_wait_task` when a `task_id` came back. When no id came back, check `modellix-cli task history` before considering another submit.

CLI flow, only after the Media Generation path is unavailable or the input is a local file:

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

Skip `get-schema` only when the user supplied a complete body.

`model invoke` is a compatibility alias of `model run`. New commands should use `model run`.

Do not reinvent polling loops when CLI wait is available. Do not invent deprecated flags (for example `--model-type`). Use `--help` only when behavior is unclear.

This skill does not choose a model. A slug comes from the user. `modellix_list_models` or `modellix-cli model list` is for when they ask to see options, not a step that ends by picking one for them.

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
2. `scripts/invoke_and_poll.py` — performs the same resolution before submission, pins the resolved executable for the workflow, uses `model run --wait` on CLI, and otherwise keeps the REST submit plus server-side wait fallback.

Set `MODELLIX_CLI_AUTO_UPDATE=0` (also accepts `false` or `off`) only when the environment must keep its installed CLI version. A registry/install failure is non-destructive: use the existing CLI if it still passes doctor, or REST when no CLI is usable and a session API key exists. Never update or swap the CLI after a paid submission has started.

When the selected path is CLI and preflight/doctor reports missing credentials, apply the lifecycle above.

When the selected path is CLI and the CLI is unavailable:

1. Use REST (`references/rest-playbook.md`).
2. Report the preflight update warning; do not repeatedly attempt installation inside the same paid workflow.

## Core Workflow

### 1) Ready the environment

- Discover or request API key (lifecycle above). The Media Generation server receives it only through the host's own `Authorization` header.
- On the Media Generation path, continue when `modellix_submit_task` is listed. Do not run preflight first.
- On the CLI path, run `scripts/preflight.py --json` and continue only when doctor passed.
- On the REST path, continue only when `MODELLIX_API_KEY` is set.

### 2) Select model

1. If the user did not name a `provider/model` slug, ask for one before any paid submit. Do not substitute a model of your own.
2. If they ask to browse: `modellix_list_models` on the MCP path, otherwise `modellix-cli model list` / `modellix-cli model describe <slug>` (catalog metadata; describe returns `docs_url`). Listing does not authorize a submit.
3. For request body schema: `modellix_get_schema` on the MCP path, otherwise `modellix-cli model get-schema <slug>` (JSON default; public, no API key). Call this when the body needs fields beyond the documented examples, after HTTP `400`, or when reporting required fields. Skip when the user supplied a complete body.
4. If neither MCP nor CLI can provide schema or discovery: use Docs Search or browse `llms.txt`, then fetch the target model `.md`. Do **not** invent slugs from filenames; decimals in a slug are significant.

### 3) Run and wait

On the Media Generation path, follow the flow in Execution Policy and `references/media-mcp-playbook.md`. Call `modellix_submit_task` once.

CLI path (local file, batch, or MCP unavailable):

```bash
modellix-cli model run \
  --model-slug <provider/model> \
  --body '<json>' \
  --wait --timeout 5m --json
```

Split flow when useful (pipelines, concurrency):

```bash
TASK_ID=$(modellix-cli model run --model-slug ... --body '...' --output task-id)
modellix-cli task wait "$TASK_ID" --timeout 10m --json
```

Batch (paid guard required): `modellix-cli model batch tasks.jsonl --max-tasks N [--wait]`.

Use CLI 0.0.11 or later with a deployed server-wait API. `task get` is immediate; wait commands use bounded server waits. The legacy `--interval` flag is unused. On exit 124, keep unfinished IDs and resume; never resubmit.

For media inputs, use `file list --json` to reuse URLs, then `file upload <path> --json` only when needed (images/video/audio, maximum 16 MiB / 16777216 bytes). On quota errors, explicitly approve deletion of an unneeded file ID; never auto-delete or replay uploads.

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

Example filename: `modellix-provider-model-20260430-113000.png`.

### Body shapes

Use the slug the user named. These shapes show required fields, not a model to select. Confirm the contract with `modellix_get_schema` or `model get-schema` when the body is not already complete.

- Text-to-image: `{"prompt": "..."}`
- Text-to-video: `{"prompt": "..."}`
- Image edit: `{"prompt": "...", "image": ["https://example.com/input.jpg"]}`
- Image-to-video: at least one of `first_frame_image`, `last_frame_image`, or `reference_images`
- Video-to-video: `{"video_urls": ["https://example.com/source.mp4"]}`
- Text-to-speech: `text` and `voice` from that model's schema
- Speech-to-text: public audio `url`
- Speech-to-speech: the target `model`, reference `url`, and synthesis `text` required by that slug

### 5) Post-task CLI recommendation

If this session used REST because CLI was missing, suggest installing the CLI afterward.

## Progressive Reference Routing

Read only what the task needs:

- `references/media-mcp-playbook.md` — Media Generation tools, upload limits, unknown-submit recovery
- `references/cli-playbook.md` — install, auth, run/wait/download, batch, recovery
- `references/rest-playbook.md` — REST submit/wait when MCP and CLI are unavailable
- `references/capability-matrix.md` — Media Generation MCP ↔ CLI ↔ REST mapping and fallback rules

## Bundled Assets

- `assets/output/task-result.schema.json`

## Credential and Data Egress

- Primary credential: `MODELLIX_API_KEY` (also via CLI profiles).
- Network egress: `https://api.modellix.ai` for CLI and REST (override only with trusted `--base-url` / `MODELLIX_BASE_URL`). Media Generation uses `https://tool.modellix.ai/mcp/media` and receives the API key only when the host attaches it. Docs Search uses `https://docs.modellix.ai/mcp` and does not receive the key. Web Tools uses `https://tool.modellix.ai/mcp` and receives the API key only when the host attaches it.
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
| Paid submit outcome **unknown** | Do **not** immediately re-run the same `model run`, `modellix_submit_task`, or REST POST. Check `task history`, console activity, and any printed task ID first. |
| Media Generation `submission_unknown` | The submit may have succeeded. Do not start a CLI or REST submit for the same request. |
| Exit `124` | Local wait timeout; remote task may still run — recover with `task wait` / `task get`, then `task download`. |
| Exit `2` | Argument or safety guard (e.g. batch cost limit) — fix flags. |

## Verification Checklist

- [ ] Media Generation tools used when they are available and the input is not a local file; otherwise doctor/preflight passed or REST key ready
- [ ] Model slug came from the user; none was invented
- [ ] Body schema checked via `modellix_get_schema` or `model get-schema` when non-trivial
- [ ] One paid submit only (`modellix_submit_task`, or `model run --wait` / `task wait` on the CLI path)
- [ ] Results saved (`data.result.resources`, `task download`, or manual persist before 7-day expiry)
- [ ] No second path after an unknown paid submission
- [ ] REST used only when Media Generation and CLI are both unavailable
