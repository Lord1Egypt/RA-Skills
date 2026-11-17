# CLI Playbook

Use this reference when `modellix-cli` is available. Command behavior source of truth: npm package `modellix-cli` and `modellix-cli --help` (not the website CLI guide page).

## Automatic version preflight

```bash
python3 scripts/preflight.py --json
```

Run preflight before the first CLI command in each workflow. It compares the installed CLI with the public npm `latest` tag, installs the exact newer version before execution, never downgrades, and falls back to the working installed CLI if the registry or install is unavailable. Set `MODELLIX_CLI_AUTO_UPDATE=0` only to pin the installed version. If Python is unavailable, inspect/install `modellix-cli@latest` manually before `doctor`.

## Authentication and profiles

Key resolution order (independent of profile selection):

1. `--api-key`
2. `MODELLIX_API_KEY`
3. Selected saved profile

Profile selection order: `--profile` → `MODELLIX_PROFILE` → saved `currentProfile` → `default`.

Session-first policy:

- Default to session env for one-off agent runs.
- When the user asks to persist: prefer `modellix-cli auth login` or `modellix-cli init`.
- Do not write system-level env or other agent config files.

```bash
# Interactive / validated save
modellix-cli init
modellix-cli auth login
modellix-cli auth login --profile work

# Non-interactive
modellix-cli init --api-key "$MODELLIX_API_KEY" --yes --json
modellix-cli auth status --json
modellix-cli auth whoami --json
```

Session-only:

```bash
export MODELLIX_API_KEY="your_api_key"
```

```powershell
$env:MODELLIX_API_KEY = "your_api_key"
```

Avoid putting keys on the command line when possible (shell history). Status/config JSON never prints the credential value.

## Diagnose

```bash
modellix-cli doctor
modellix-cli doctor --json
```

Checks Node.js, key source (without printing the key), API connectivity, and balance when authenticated. Failed required checks exit non-zero.

## Discover models

```bash
modellix-cli model list
modellix-cli model list --type text-to-image --output slugs
modellix-cli model list --provider google --limit 20
modellix-cli model list --search banana
modellix-cli model describe <provider/model> --json
```

When the user did not name a `provider/model` slug, ask for one. Do not choose a model from this list.

`--model-slug` must be exact `provider/model` as returned by the catalog.

`model describe` is catalog metadata (pricing, `docs_url`, featured). For the request/response contract, use the public schema command (no API key):

```bash
modellix-cli model get-schema alibaba/qwen-image-3.0-pro
modellix-cli model get-schema alibaba/qwen-image-3.0-pro --output human
modellix-cli model get-schema alibaba/qwen-image-3.0-pro --quiet
```

JSON is the default and preserves `servers` plus the `post` OpenAPI-style contract — use it to build `--body`. Human output summarizes the inference endpoint, request body, and responses. Quiet prints only `servers[0].url`. Call `get-schema` when the body needs fields beyond a complete body the user already supplied, after HTTP `400`, or when reporting required fields. If CLI is unavailable, fall back to Docs Search or the model `.md` (`docs_url` / `llms.txt`). Do not keep a bundled model index — live CLI catalog + schema are the source of truth.

## Run a model (canonical)

Prefer `model run`. `model invoke` is a compatibility alias only.

Inline JSON:

```bash
modellix-cli model run \
  --model-slug <provider/model> \
  --body '{"prompt":"A cute cat"}' \
  --wait --timeout 5m --json
```

From file or stdin:

```bash
modellix-cli model run --model-slug <provider/model> --body-file ./payload.json --wait --timeout 5m --json
printf '%s' '{"prompt":"A cute cat"}' | modellix-cli model run --model-slug <provider/model> --body-file - --wait --timeout 5m --json
```

Task ID only (for pipelines):

```bash
modellix-cli model run --model-slug <provider/model> --body '{"prompt":"A cute cat"}' --output task-id
```

Notes:

- Use either `--body` or `--body-file`, not both.
- Default submit is async; `--wait` uses bounded server-side waits to a terminal status; `--no-wait` makes async explicit.
- Paid POST is **not** auto-retried. An unknown submission outcome must not be blindly repeated — check `task history` and any printed task ID first.
- If wait times out after a task ID was received, recover with `task wait` using that ID (exit `124`).

### PowerShell reliable payload patterns

`--body` with object-to-JSON:

```powershell
$payload = @{
  prompt = "A beautiful Mother's Day poster design with elegant typography."
  aspectRatio = "3:4"
} | ConvertTo-Json -Compress

modellix-cli model run --model-slug <provider/model> --body $payload --wait --timeout 5m --json
```

`--body-file` for complex prompts:

```powershell
$payload = @{
  prompt = "A beautiful Mother's Day poster design with elegant typography."
  aspectRatio = "3:4"
}
$payload | ConvertTo-Json -Depth 10 | Set-Content -Path ".\poster_body.json" -Encoding UTF8
modellix-cli model run --model-slug <provider/model> --body-file ".\poster_body.json" --wait --timeout 5m --json
```

## Wait and get

```bash
modellix-cli task get <task_id>
modellix-cli task wait <task_id>
modellix-cli task wait task-a task-b --timeout 10m --concurrency 8 --json
```

Durations accept values like `500ms`, `30s`, `5m`, `2h` (bare integers remain seconds). Overall wait timeout exit code: `124`. Multiple IDs return a stable `{ "tasks": [...] }` wrapper in input order.

## Download

```bash
modellix-cli task download <task_id> --output-dir ./outputs
modellix-cli task download <task_id> --output-dir ./outputs --json
```

Defaults preserve existing files; use `--overwrite` deliberately. JSON output includes local paths, not signed source URLs. Prefer this over hand-downloading CDN URLs when CLI is available.

If the CLI rejects the CDN host as a private/reserved address (for example under a local proxy that resolves `file.modellix.ai` to `198.18.x.x`), retry:

```bash
modellix-cli task download <task_id> --output-dir ./outputs --json --allow-private-network
```

Only use `--allow-private-network` / `--allow-insecure-http` for trusted Modellix result hosts, not arbitrary user-supplied URLs.

## Batch

JSONL: one object per line with `modelSlug` and `body`.

```bash
modellix-cli model batch tasks.jsonl --max-tasks 10 --concurrency 3
modellix-cli model batch tasks.jsonl --max-tasks 10 --wait --quiet
```

Require `--max-tasks` or `--yes` (paid-task guard). Do not use `--continue-on-unknown` unless the user accepts duplicate-charge risk after an unknown paid outcome.

## Local history

```bash
modellix-cli task history --limit 50 --json
modellix-cli task history --quiet
```

Stores task metadata only (never API keys or request bodies). Use after unknown submit outcomes or lost task IDs.

## Output and CI

- `--json` / `--output json` — machine-readable; failures use `{ "ok": false, "error": { "exitCode", "message" } }`
- `--quiet` / `-q` — primary value only (slug, task id, URL, path)
- `--output human` — readable summary
- Compatible: `--output slugs` (`model list`), `--output task-id` (`model run`)
- CI: `--no-color --no-progress`; `CI` env also suppresses update checks

Exit codes: `0` success, `1` operation/API failure, `2` args/safety guard, `124` local wait timeout, `127` unknown command.

## Error handling

| Code / case | Action |
|---|---|
| 400 | Fix body/params (`model get-schema` when the contract is unclear); do not retry as-is |
| 401 | Fix key (`doctor`, `auth login`) |
| 402 | Recharge balance |
| 404 | Verify slug / task id |
| 429 | Safe GETs are retried by CLI; do not blindly re-POST |
| 500/503 (read) | CLI retries within request deadline |
| Unknown paid submit | Check `task history`; do not immediate duplicate POST |
| Exit 124 | `task wait` / `task get`, then `task download` |

## Config helpers

```bash
modellix-cli config path
modellix-cli config show --json
modellix-cli config clear --profile work --yes
```

These never print the API key.

## Media Files and Server Wait

Use modellix-cli 0.0.11 or later for server wait and file listing, after the compatible task API is deployed. `task get` stays immediate; `task wait`, `model run --wait`, and `model batch --wait` use server wait. `--interval` is parsed for compatibility but unused. Exit 124 preserves completed results, unfinished IDs, and available unfinished snapshots; resume waiting on the same IDs.

```bash
modellix-cli file list --limit 20 --offset 0 --json
modellix-cli file upload ./reference.mp4 --json
modellix-cli file delete <explicit-file-id> --json
```

Supported image, video, and audio inputs have a 16 MiB (16777216-byte) CLI limit and must be regular files, not symlinks. Match the selected model schema before uploading. Reuse returned URLs; quota errors require explicit selection and deletion, never automatic cleanup. A 404 delete succeeds as `alreadyAbsent` and does not claim a new deletion.
