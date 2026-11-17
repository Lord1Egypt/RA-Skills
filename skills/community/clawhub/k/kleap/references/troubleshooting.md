# Kleap troubleshooting

Every failure exits `1` and prints `✗ CODE: message (HTTP n, METHOD /path)` on
stderr, plus a `→ hint` line when there is a fix. With `--json`:
`{"error":{"code","message","status","details","request_id","hint"}}` on stdout.
Retry budget: fix and retry **at most twice**, then tell the user exactly what
the error said. Never retry a non-transient error unchanged.

| Code | Meaning | What to do |
|---|---|---|
| `not_authenticated` | No key and no login on this machine | `kleap auth login`, or set `KLEAP_API_KEY` / `kleap auth key <KEY>` |
| `UNAUTHORIZED` (401) | Key wrong, revoked or expired | Ask the user for a valid key (https://kleap.co/settings/api-key) |
| `INSUFFICIENT_SCOPE` (403) | The key predates this feature (`details.required_scope`, e.g. `database:write`, `domains:checkout`, `forms:read`). `db sql` always needs `database:write`, even for a SELECT | The user must **create a new API key with the Full preset** and use it. Retrying with the same key never works. |
| `INSUFFICIENT_CREDITS` (402) | Not enough credits (create needs ≥5, edit ≥2) | `kleap credits`; ask the user to top up. Do not retry. Deterministic `files …` + `publish` cost no credits. |
| `PLAN_REQUIRED` (403) | Paid plan needed (e.g. `domains connect`) | Tell the user; they upgrade at https://kleap.co/pricing |
| `RATE_LIMITED` (429) | Too many requests | Wait ~60 s (the CLI already honors `Retry-After` twice), then retry once |
| `DATABASE_NOT_PROVISIONED` (409) | This app has no Kleap Database | `kleap edit <app> "add a database"`, wait for it, then retry the `db` command |
| `UNSUPPORTED_STATEMENT` (400) | `db sql` got a statement the API does not run (EXPLAIN, SHOW, COPY, CALL, PREPARE/EXECUTE, a multi-statement script with a query or RETURNING, `WITH … DELETE … RETURNING`, raw writes on a DB with rewrite rules) | Send one supported statement, or use `db rows / insert / update / delete` |
| `RLS_REQUIRED` (422) | SQL created/changed a public table without row level security | Re-run with `ALTER TABLE <t> ENABLE ROW LEVEL SECURITY;` (+ policies) in the same SQL |
| `VALIDATION_ERROR` (400) | Bad input (empty prompt, bad JSON, missing `where`…) | Fix the input named in the message |
| `NOT_FOUND` (404) | Unknown app/task/domain, or `domains check` on a domain Kleap doesn't manage | `kleap list --q <name>` to find the app; for a domain, it isn't registered/connected yet |
| `CONFLICT` (409) on publish | A deploy is already running | Handled: `kleap publish` follows the running deploy |
| `FILE_TOO_LARGE` | A file over 512 KB | Compress/resize it (images: use `.webp`) |
| `usage` | Wrong command shape | Read the `usage:` line and fix the arguments |

## Truncated results

`db rows` returns at most 5 MB per call and `db sql` at most 500 rows / 5 MB;
a `… truncated by the API row cap` line (`"truncated": true` in JSON) means
there is more. Page `db rows` with `--offset`, or tighten `--where` / the query.
A single value over 256 KB comes back as `{"__kleap_value_too_large": true, "bytes": N}`.

## Task failures (`kleap task`, `create`, `edit`)

| `error.code` | Meaning | Action |
|---|---|---|
| `TASK_TIMEOUT` / `STALE_TASK` | The build stalled (transient) | `kleap task retry <task_id> --wait` — up to 2 times |
| `TASK_FAILED` | Generation failed | Read the message; `kleap task retry <task_id> --wait` once, else rephrase the request with `edit` or stop and report |

## Publish refused

Kleap keeps the previous working version live when a new build is visibly
broken (blank hero, unstyled page, build error). Fix the cause with
`kleap edit <app> "fix: <what the error said>"` or `kleap files edit …` +
`kleap publish <app>`. Re-running `publish` unchanged fails the same way.

## Domains

- `domains buy` only creates a checkout link. If the user says they paid but
  `domains check` still returns `NOT_FOUND`, wait a minute and check again;
  never report it as bought before `check` answers.
- `pending DNS`: the A record isn't visible yet (5-60 min, sometimes hours) —
  relay the message, check again later.
- `aaaa_conflict`: the user must delete the AAAA (IPv6) record at their registrar.
