# Capability Matrix

Use this matrix to keep one task on one path. Prefer Media Generation when its tools are available and the input is not a local file. Use the CLI when they are not, or when the task needs a local file, a batch, or `task download`. Use REST only when both of those are unavailable.

| Capability | Media Generation MCP | CLI | REST | Notes |
| --- | --- | --- | --- | --- |
| Diagnose env/auth | Host attaches `Authorization` for `https://tool.modellix.ai/mcp/media`. No header is stored in this repo. | `scripts/preflight.py --json` → `modellix-cli doctor --json` | Manual key | Run preflight only on the CLI path. Update failure keeps a working installed CLI |
| List / describe models | `modellix_list_models` | `model list`, `model describe <slug>` | Browse `llms.txt`, then fetch model `.md` | Listing is for the user to choose. `describe` is catalog metadata (`docs_url`, pricing, featured) |
| Get request / response schema | `modellix_get_schema` (public, no API key) | `model get-schema <slug>` (JSON default; public, no API key) | Fetch model `.md` OpenAPI via Docs Search / `docs_url` / `llms.txt` | Use a schema before building a body the user did not already complete |
| Look up product / API / install docs | Docs Search (`search_modellix` / docs filesystem) at `https://docs.modellix.ai/mcp` | Same Docs Search server, or fetch `docs_url` | Fetch `docs_url` or `llms.txt` → model `.md` | Docs Search is read-only and does not receive the API key. CLI flags still prefer npm / `--help` over website CLI pages |
| Submit async task | `modellix_submit_task` once | `modellix-cli model run --model-slug <provider/model> --body/--body-file ...` | `POST /api/v1/{provider}/{model_id}/async` | One path per request. `model invoke` is an alias of `model run` |
| Wait for terminal status | `modellix_wait_task` (1–45 seconds per call) | `model run --wait` or `task wait <task_id>` | Wait with `GET /api/v1/tasks/{task_id}?wait=true&timeout=45` | `timed_out=true` is a snapshot. Do not hand-roll poll loops |
| Read task once | `modellix_get_task` | `task get <task_id>` | `GET /api/v1/tasks/{task_id}` | Terminal states: `success` / `failed` / `canceled` (CLI also reports `pending` / `processing`) |
| Persist resources | Save `data.result.resources` (or `task download` when the CLI is installed) | `task download <task_id> --output-dir ...` | Download URLs from `result.resources` | URLs expire in about 7 days. Local paths and private-network CDN retries stay on the CLI |
| Upload inputs | `modellix_upload_file` with a public `url` or `base64_content` plus `filename` | `file upload <path>` | REST file upload | MCP cannot read a local path. 16 MiB limit. Never auto-delete |
| Batch submit | Not available | `model batch <file.jsonl> --max-tasks N` | Multiple REST POSTs | CLI validates all lines before the first paid POST |
| Recover an unknown submit | `submission_unknown`: do not submit again | `task history` | Do not POST again | An unknown MCP submit must not continue as a CLI or REST submit |

CLI command policy:

- Canonical CLI flow, used when Media Generation is unavailable or the input is a local file: `model run --wait` → `task download`.
- Resolve the CLI once through `preflight.py` before the first CLI command; do not update it after a paid submit begins.
- Split flow when needed: `model run --output task-id` → `task wait` → `task download`.
- Do not use deprecated guessed flags (for example `--model-type`).
- Use `--help` only when behavior is unclear.
- `preflight.py` owns automatic CLI refresh; `invoke_and_poll.py` pins the resolved executable for its complete workflow.
- Paid submissions must not be blindly retried on unknown outcomes.

## Slug Mapping

- `model-slug` uses `provider/model` format for Media Generation, CLI, and REST.
- REST path transformation:
  - Input: `provider/model`
  - Derived path parts: `provider`, `model_id`

## Fallback Rules

Use the CLI when any condition is true:

- `modellix_submit_task` is not in the tool list
- The Media Generation client returns a protocol error or `401`
- The input is a local file path
- The task is a batch, needs `task download`, or the CDN host resolves into a private range

Use REST when the CLI path is selected and any condition below is also true:

- `modellix-cli` unavailable after automatic preflight/update
- CLI auth unavailable
- CLI command surface does not expose required behavior

If no CLI is usable after preflight, use REST directly when `MODELLIX_API_KEY` is available and report the update warning once. Do not switch a request that already called `modellix_submit_task` onto REST.
