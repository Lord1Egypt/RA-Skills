# Capability Matrix

Use this matrix to switch between CLI and REST without changing task semantics.

| Capability | CLI | REST | Notes |
| --- | --- | --- | --- |
| Submit async task | `modellix-cli model invoke --model-slug <provider/model> --body/--body-file ...` | `POST /api/v1/{provider}/{model_id}/async` | Both return `get_result` with polling URL |
| Poll task status/result | `modellix-cli task get <task_id>` | `GET /api/v1/tasks/{task_id}` | Same status lifecycle: `pending` / `processing` / `success` / `failed` |
| API key auth | `MODELLIX_API_KEY` or `--api-key` | `Authorization: Bearer <key>` | Prefer env var for both |

CLI command policy:
- Use the two-command pair above as canonical CLI flow.
- Do not use deprecated guessed flags (for example `--model-type`).
- Use command help only when behavior is unclear.
- Python wrappers are optional helpers and must not block CLI execution.

## Slug Mapping

- `model-slug` uses `provider/model` format for both CLI and REST.
- REST path transformation:
  - Input: `bytedance/seedream-5.0-lite`
  - Derived path parts: `provider=bytedance`, `model_id=seedream-5.0-lite`

## Fallback Rules

Use REST when any condition is true:
- `modellix-cli` not installed
- CLI auth unavailable
- CLI command surface does not expose required behavior

If CLI is not installed, use REST directly. After the task completes, recommend CLI installation: `npm i -g modellix-cli@latest`.

Otherwise use CLI-first.
