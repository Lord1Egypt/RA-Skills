---
name: kleap
description: "Ship and run a live website or web app end-to-end — hosting, database, auth, forms/leads, analytics, custom domains — driven from this agent via the kleap CLI (npx, no install)."
version: 1.1.0
metadata:
  openclaw:
    requires:
      bins:
        - npx
    primaryEnv: KLEAP_API_KEY
    envVars:
      - name: KLEAP_API_KEY
        required: false
        description: "kleap_live_sk_... API key (create it with the Full preset) for headless/CI use. Not needed if `kleap auth login` already ran once (token cached in ~/.kleap/config.json)."
    emoji: "🌐"
    homepage: "https://kleap.co/mcp"
---

# Kleap — ship and run a live business from this agent

Kleap turns a prompt into a **live, hosted site** — hosting, database, auth,
forms and TLS included — and every publish is **verified-live** (a URL is only
reported once the new version is provably serving).

Every command is `npx -y kleap-cli@latest <command>` (below: `kleap <command>`).
Output is 1-3 lines; add `--json` for the full structured result (errors too:
`{"error":{"code","message","hint",...}}`). Exit `0` = success, `1` = failure.
`<app>` accepts an app id, a `slug.kleap.io` URL, a bare slug or a connected
custom domain.

## Setup (once per machine)

- Interactive: `kleap auth login` (browser, no key to paste).
- Headless / CI: `KLEAP_API_KEY=kleap_live_sk_...` in the env, or
  `kleap auth key <KEY>`. Create the key at https://kleap.co/settings/api-key with
  the **Full** preset (older keys lack the database/checkout scopes).
- Check: `kleap auth status` (exit 0 = signed in). `kleap credits` shows the balance.

## Build and change a site

| Goal | Command |
|---|---|
| New site (blocks 1-15 min, prints the live URL) | `kleap create "<rich prompt: business, audience, tone, sections>"` |
| Change it with Kleap's AI | `kleap edit <app> "<one concrete change>"` |
| Don't block | add `--no-wait --json` → `{task_id, app_id}`; later `kleap task <task_id> --wait` |
| Failed / stalled task | `kleap task retry <task_id> --wait` (new task id; TASK_TIMEOUT/STALE_TASK ≤2×, TASK_FAILED 1×, then stop and tell the user) |
| State of a site | `kleap status <app>` · `kleap list [--q name]` · `kleap screenshot <app>` · `kleap messages <app>` |
| Rename (URL never changes) | `kleap rename <app> <new name>` |

`create` and `edit` deploy by themselves — no `publish` needed after them.

## Exact edits with your own code (deterministic, no Kleap credits)

1. `kleap files ls <app>` → `kleap files cat <app> <path...>` (read before changing).
2. Change: `kleap files edit <app> <path> --find "<old>" --replace "<new>" [--all]`,
   or `kleap files write <app> <path> --file <local> | --stdin | --content "<text>"`
   (images/fonts/PDF are sent base64 automatically; 512 KB max),
   or `kleap files rm <app> <path...>` (never blank a file to delete it),
   or `kleap image <app> public/hero.webp "<vivid prompt>" [--hd]`.
3. **Then `kleap publish <app>`** — files do not go live until you publish.

## Leads, traffic, search

- `kleap forms <app> [--since 2026-09-01T00:00:00Z] [--limit 50]` — form
  submissions, newest first; `--json` gives flat objects (`name`, `email`, …,
  `submission_id`, `submitted_at`, `app_id`). Empty on a new site is normal.
- `kleap analytics <app> [--period 7d|30d|90d]` — visitors, pageviews, top pages
  (only after the site has been published).
- `kleap search-console <app> [--period 7d|28d|30d|90d]` — Google clicks/impressions/CTR/position. Not
  connected → `kleap search-console connect <app>` prints a consent link the
  **user** opens (needs a custom domain first).

## Database (the app's own Postgres)

- `kleap db schema <app>` — tables, columns and an ESTIMATED row count (`~N`; use `db sql` `count(*)` for an exact one).
- `kleap db rows <app> <table> [--where '{"status":"new"}'] [--limit 100] [--order-by created_at --order desc]`
- `kleap db insert <app> <table> '{"email":"a@b.co"}'` (object or array, or `--file rows.json`)
- `kleap db update <app> <table> --where '{"id":12}' --set '{"status":"done"}'`
- `kleap db delete <app> <table> --where '{"id":12}'` — `--where` is mandatory; read the rows first.
- `kleap db sql <app> "select count(*) from leads where status = \$1" --params '["new"]'`
  — owner-level: always needs `database:write`, even for a SELECT. One statement
  (no EXPLAIN/SHOW/COPY/CALL → `UNSUPPORTED_STATEMENT`); results are capped at
  500 rows / 5 MB (a `… truncated` line tells you). To just read, prefer `db rows`.

No database yet (`DATABASE_NOT_PROVISIONED`) → `kleap edit <app> "add a database"` first.

## Domains

- `kleap domains search <name> [--tlds .com,.fr]` — available names + price.
- `kleap domains buy <domain> [--years 1] [--app <app>]` — prints a **checkout
  link the user must open and pay**. The domain is **not bought** until they
  pay; with `--app` it is connected to that site once paid. Give the user the
  link, then confirm later with `kleap domains check <domain>`.
- `kleap domains connect <domain> <app>` — a domain the user **already owns**
  (paid plan): relay the printed A record; TLS follows DNS propagation
  ("minutes to a few hours", never "instant").
- `kleap domains check <domain>` — `active`, `pending DNS` (relay the message) or an AAAA conflict.

## Rules

1. **Golden rule — never claim a site is live** until a command confirmed it:
   the `✓ … — <url>` line of `create`/`edit`/`publish`, a completed `task`, or
   `status` showing a live URL. A build *starting* is not a site *online*.
2. **Buying a domain = a checkout link the user pays.** Never say a domain is
   bought, registered or live before `domains check` shows it.
3. On any `✗ CODE: message`, read the `→` hint line (or `error.hint` in JSON)
   and act on it; fix-and-retry at most twice, then tell the user exactly what
   the error said. See `references/troubleshooting.md`.
4. Prefer `edit` / `files edit` over recreating a site — it keeps what works.

See `references/recipes.md` for complete flows (lead capture → read leads,
database CRUD, buy + connect a domain, non-blocking builds).
