# CLI Playbook

Use this reference when `modellix-cli` is available and authenticated.

## Install

```bash
npm install -g modellix-cli@latest
modellix-cli --version
```

## Authentication

Preferred:

```bash
export MODELLIX_API_KEY="your_api_key"
```

Session-first policy:
- Default to session-only usage for safety.
- Persist to user-level environment only when the user explicitly requests persistence.
- Do not write system-level environment variables or other agent config files.

PowerShell:

```powershell
$env:MODELLIX_API_KEY="your_api_key"
```

Alternative per-command:

```bash
modellix-cli ... --api-key <your_api_key>
```

## Core Command Flow

Command-first policy:
- Treat the CLI as a two-command workflow: `model invoke` then `task get`.
- Do not guess parameters from memory (for example, do not add deprecated `--model-type`).
- Use `--help` as an assistive fallback when command behavior is unclear:
  - `modellix-cli --help`
  - `modellix-cli model invoke --help`
  - `modellix-cli task get --help`

### PowerShell reliable payload patterns

Use one of these patterns to avoid quote escaping issues in PowerShell.

`--body` with object-to-JSON conversion:

```powershell
$payload = @{
  prompt = "A beautiful Mother's Day poster design with elegant typography."
  aspectRatio = "3:4"
} | ConvertTo-Json -Compress

modellix-cli model invoke --model-slug google/nano-banana --body $payload
```

`--body-file` for complex prompts (recommended on Windows):

```powershell
$payload = @{
  prompt = "A beautiful Mother's Day poster design with elegant typography."
  aspectRatio = "3:4"
}

$payload | ConvertTo-Json -Depth 10 | Set-Content -Path ".\poster_body.json" -Encoding UTF8
modellix-cli model invoke --model-slug google/nano-banana --body-file ".\poster_body.json"
```

1) Invoke async task:

```bash
modellix-cli model invoke \
  --model-slug bytedance/seedream-5.0-lite \
  --body '{"prompt":"A cinematic portrait of a fox in a misty forest at sunrise"}'
```

`--model-slug` is required and must use `provider/model` format, for example:
- `bytedance/seedream-5.0-lite`
- `alibaba/qwen-image-edit`

The response includes a `get_result` section with the polling endpoint:

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "status": "pending",
    "task_id": "task-abc123",
    "model_id": "model-123",
    "get_result": {
      "method": "GET",
      "url": "https://api.modellix.ai/api/v1/tasks/task-abc123"
    }
  }
}
```

2) Poll task result:

```bash
modellix-cli task get <task_id>
```

If `modellix-cli` is missing:
- Skip CLI and use the REST playbook fallback directly.
- After task completion, recommend the user install CLI: `npm i -g modellix-cli@latest`.

## Polling Guidance

- Start with 1-2s delay
- Use exponential backoff (`1s -> 2s -> 4s`, cap near 10s)
- Stop on `success` or `failed`

## Error Handling

The CLI surfaces API errors directly:
- `400`: invalid request body or parameters
- `401`: invalid/missing API key
- `402`: balance/billing issue
- `404`: invalid task or model slug
- `429`: retry with backoff
- `500`/`503`: retry up to 3 times with backoff

## Platform Notes

- Prefer `--json` output for machine-readable parsing.
- On Windows PowerShell, set env vars with `$env:VAR_NAME="value"`.
