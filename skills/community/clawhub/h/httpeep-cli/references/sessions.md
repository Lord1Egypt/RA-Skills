<!-- GENERATED FILE: DO NOT EDIT DIRECTLY. -->
<!-- Source of truth: docs.httpeep.com/content/docs/cli/sessions.mdx -->
<!-- Generate with: node scripts/generate-httpeep-cli-skill-reference.mjs <references-dir> -->

# Sessions

The `sessions` subcommand lets you query every HTTP and HTTPS request that HTTPeep has captured. You can filter sessions by host, status code, HTTP method, path, or time window; inspect the full request and response of any session including headers, body, and timing breakdown; stream new sessions in real time; or clear old sessions to keep your workspace clean.

## sessions list

List captured sessions with optional filters. With no flags, returns the first page of captured sessions from the current session store, ordered newest first.

```bash
httpeep-cli sessions list
```

**Filter flags:**

| Flag | Description | Example |
|---|---|---|
| `--id <id>` | Filter by exact session ID | `--id abc123` |
| `--method <method>` | Filter by HTTP method | `--method POST` |
| `--status-code <code>` | Filter by status code | `--status-code 200` |
| `--process-id <pid>` | Filter by process ID | `--process-id 1234` |
| `--domain <domain>` | Filter by domain | `--domain api.example.com` |
| `--client-ip <ip>` | Filter by client IP | `--client-ip 127.0.0.1` |
| `--is-pinned` | Only pinned sessions | `--is-pinned` |
| `--is-important` | Only important sessions | `--is-important` |
| `--from-ts <ts>` | Sessions captured after timestamp | `--from-ts 1713000000` |
| `--to-ts <ts>` | Sessions captured before timestamp | `--to-ts 1714000000` |
| `--url-like <pattern>` | Fuzzy match URL | `--url-like "/api"` |
| `--path-like <pattern>` | Fuzzy match path | `--path-like "/v2"` |
| `--domain-like <pattern>` | Fuzzy match domain | `--domain-like "example"` |
| `--process-name-like <pattern>` | Fuzzy match process name | `--process-name-like "curl"` |
| `--keyword <keyword>` | Keyword search across URL, domain, method, status, and process name | `--keyword login` |

**Pagination and output flags:**

| Flag | Description | Example |
|---|---|---|
| `--page <number>` | Return a 1-based page number | `--page 2` |
| `--page-size <number>` | Number of sessions per page | `--page-size 50` |
| `--limit <number>` | Backward-compatible alias for first-page size | `--limit 50` |
| `--fields <list>` | Comma-separated JSON fields to include in each returned session | `--fields id,method,url,status_code,timing` |

> **Note:**
> `--limit` is kept for older scripts and conflicts with `--page-size`. For new scripts, prefer `--page` and `--page-size`.

```bash
# Filter examples
httpeep-cli sessions list --method POST --status-code 200
httpeep-cli sessions list --domain api.example.com
httpeep-cli sessions list --keyword login
httpeep-cli sessions list --url-like "/api" --process-name-like "curl"
```

JSON output for scripting:

```bash
httpeep-cli --format json sessions list --keyword login
```

Use `--fields` with JSON output when you only need a small set of columns. This keeps large request and response payload metadata out of agent prompts, CI logs, and shell pipelines:

```bash
httpeep-cli --format json sessions list \
  --page 1 \
  --page-size 25 \
  --fields id,method,url,status_code,timing
```

Common field names include `id`, `session_no`, `created_at`, `method`, `url`, `domain`, `status_code`, `state`, `timing`, `process_id`, `process_name`, `client_ip`, `server_ip`, `request`, and `response`.

Example output (table format):

```text
ID           METHOD  URL                                    STATUS  DURATION
abc123def4   POST    https://api.example.com/v2/users       201     234ms
xyz789abc1   GET     https://api.example.com/v2/users/001   200     45ms
err456def7   GET     https://api.example.com/v2/reports     500     1840ms
```

> **Note:**
> To get the full JSON summary for a single session, use `sessions list --id <session_id>` with `--format json` and omit `--fields`.

## sessions watch

Stream new sessions to stdout in real time as they are captured. Press `Ctrl+C` to stop.

```bash
httpeep-cli sessions watch

# Filter the stream to a specific domain
httpeep-cli sessions watch --domain api.example.com

# Machine-readable stream — one JSON object per line (NDJSON)
httpeep-cli --format json sessions watch --keyword login
```

> **Tip:**
> Use `--format json` when piping the stream into a log processor or another tool. Each captured session is emitted as a single self-contained JSON object on its own line.

All filter flags from `sessions list` also work with `watch`.

## sessions delete

Delete sessions by specific IDs or by query conditions.

Delete by IDs:

```bash
httpeep-cli sessions delete --id abc123 --id def456
```

`sessions delete` accepts the same query filters as `sessions list`, except `--id` is reserved for exact repeated IDs. ID mode and query mode are mutually exclusive, so commands such as `sessions delete --id abc123 --keyword login` are rejected.

Delete by query conditions (with a dry-run preview first):

```bash
# Preview what would be deleted
httpeep-cli sessions delete --keyword login --dry-run

# Execute the deletion
httpeep-cli sessions delete --keyword login
```

## sessions clear

Clear all sessions from the session store.

```bash
# Preview before clearing
httpeep-cli sessions clear --all --yes --dry-run

# Execute
httpeep-cli sessions clear --all --yes
```

> **Warning:**
> `sessions clear --all --yes` permanently deletes all sessions without prompting. Use this flag in scripts only when you are certain you no longer need the captured data.

## jq pipeline examples

Use `--format json` with `jq` to analyze captured traffic programmatically.

```bash
# Find all slow requests (over 500 ms)
httpeep-cli --format json sessions list --fields id,method,url,status_code,timing | \
  jq '.[] | select(.timing.total_ms > 500) |
      {url, status_code, total_ms: .timing.total_ms}'

# Compute error rate across all captured sessions
httpeep-cli --format json sessions list --fields id,status_code | \
  jq '{ total: length, errors: [.[] | select(.status_code >= 400)] | length } |
       .error_rate = (.errors / .total * 100 | round)'

# List unique domains
httpeep-cli --format json sessions list --fields domain | \
  jq '[.[].domain] | unique | sort[]'

# Keep JSON compact for AI agents or CI logs
httpeep-cli --format json sessions list --fields id,method,url,status_code,timing | \
  jq '.[] | {id, method, url, status_code, timing}'

# Count requests by HTTP method
httpeep-cli --format json sessions list --fields method | \
  jq 'group_by(.method) | map({method: .[0].method, count: length})'
```
