# Capability Matrix

Use this matrix to switch between CLI and REST without changing task semantics.

| Capability | CLI | REST | Notes |
| --- | --- | --- | --- |
| Resolve/update CLI and diagnose env/auth | `scripts/preflight.py --json` → `modellix-cli doctor --json` | N/A (manual key + probe) | Update check runs before paid work; failure keeps a working installed CLI |
| List / describe models | `model list`, `model describe <slug>` | Browse `llms.txt`, then fetch model `.md` | Prefer CLI when installed; `describe` is catalog metadata (`docs_url`, pricing, featured) |
| Get request / response schema | `model get-schema <slug>` (JSON default; public, no API key) | Fetch model `.md` OpenAPI via Docs MCP / `docs_url` / `llms.txt` | Use CLI schema before building `--body` when the slug is non-default or the body is non-trivial |
| Look up product / API / install docs | Docs MCP (`search_modellix` / docs filesystem) when connected via portable `mcp.json` or host adapter `.mcp.json` | Fetch `docs_url` or `llms.txt` → model `.md` | Docs MCP is read-only documentation — not generation. CLI flags still prefer npm / `--help` over website CLI pages |
| Submit async task | `modellix-cli model run --model-slug <provider/model> --body/--body-file ...` | `POST /api/v1/{provider}/{model_id}/async` | `model invoke` is an alias of `model run` |
| Wait for terminal status | `model run --wait` or `task wait <task_id>` | Poll `GET /api/v1/tasks/{task_id}` | Prefer CLI wait; do not hand-roll poll loops when CLI exists |
| Read task once | `task get <task_id>` | `GET /api/v1/tasks/{task_id}` | Same status lifecycle: `pending` / `processing` / `success` / `failed` |
| Download resources | `task download <task_id> --output-dir ...` | Download URLs from `result.resources` | CLI path preferred (safe filenames, limits) |
| Batch submit | `model batch <file.jsonl> --max-tasks N` | Multiple REST POSTs | CLI validates all lines before first paid POST |
| Local task recovery | `task history` | N/A | Never stores API keys or bodies |

CLI command policy:

- Canonical single-task flow: `model run --wait` → `task download`.
- Resolve the CLI once through `preflight.py` before the first command; do not update it after a paid submit begins.
- Split flow when needed: `model run --output task-id` → `task wait` → `task download`.
- Do not use deprecated guessed flags (for example `--model-type`).
- Use `--help` only when behavior is unclear.
- `preflight.py` owns automatic CLI refresh; `invoke_and_poll.py` pins the resolved executable for its complete workflow.
- Paid POST submissions must not be blindly retried on unknown outcomes.

## Slug Mapping

- `model-slug` uses `provider/model` format for both CLI and REST.
- REST path transformation:
  - Input: `google/nano-banana-2-lite`
  - Derived path parts: `provider=google`, `model_id=nano-banana-2-lite`

## Default Models (when user omits model)

| Task Type | Default slug |
| --- | --- |
| T2I | `google/nano-banana-2-lite` |
| T2V | `bytedance/seedance-2.0-mini-t2v` |
| I2I | `google/nano-banana-2-lite-edit` |
| I2V | `bytedance/seedance-2.0-fast-i2v` |
| V2V | `bytedance/seedance-2.0-fast-v2v` |
| TTS | `alibaba/qwen-audio-3.0-tts-flash` |
| STT | `openai/whisper-1` |
| STS | `alibaba/cosyvoice-clone` |

## Fallback Rules

Use REST when any condition is true:

- `modellix-cli` unavailable after automatic preflight/update
- CLI auth unavailable
- CLI command surface does not expose required behavior

If no CLI is usable after preflight, use REST directly when `MODELLIX_API_KEY` is available and report the update warning once.

Otherwise use CLI-first.
