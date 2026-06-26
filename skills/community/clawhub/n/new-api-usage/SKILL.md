---
name: new-api-usage
description: Query usage statistics and quota from a user-specified new-api endpoint. Use when the user asks to check API quota, usage records, token consumption, model-level usage, or remaining balance. Requires explicit --base-url and --key input.
---

# New API Usage Query

Query quota and usage from a new-api deployment with explicit inputs.

## Safety Rules

- Require explicit `--base-url` and `--key`; never auto-read local config or keychain.
- Never print the full API key in output.
- Only perform read-only GET requests to usage endpoints.
- If the endpoint is unknown, ask user to confirm before querying.

## Usage

```bash
# Summary (today's records only)
uv run python scripts/query_usage.py \
  --base-url https://your-new-api.example.com \
  --key sk-xxxxx

# Quota only
uv run python scripts/query_usage.py \
  --base-url https://your-new-api.example.com \
  --key sk-xxxxx \
  --quota-only

# Model aggregation with all records
uv run python scripts/query_usage.py \
  --base-url https://your-new-api.example.com \
  --key sk-xxxxx \
  --all-records \
  --by-model
```

## Options

| Option | Description |
|--------|-------------|
| `--base-url` | Required. new-api base URL, e.g. `https://xxx.com` |
| `--key` | Required. API key |
| `--today` | Only keep today's records (default) |
| `--all-records` | Disable today's filter |
| `--limit N` | Number of records shown in table (default: 100) |
| `--by-model` | Show grouped usage by model |
| `--quota-only` | Only show quota/balance |
| `--json` | Print raw JSON payload |
| `--timeout` | HTTP timeout seconds (default: 15) |

## API Endpoints

- `GET /api/usage/token/`
- `GET /api/log/token?key={api_key}`

## Notes

- Quota conversion in script uses `500000 quota = $1`.
- `--today` uses local timezone date boundaries.
