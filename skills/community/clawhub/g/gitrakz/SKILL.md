---
name: gitrakz
description: Drive a self-hosted gitrakz instance — the tool that syncs a GitHub user's activity into local SQLite, renders a filterable timeline and derived work sessions, and runs deterministic programmatic templates that export to CSV/PDF/JSON. Install or run it with Docker, then query its bearer-protected REST API under /api/v1 (owners, repos, timeline, sessions, sync + sync status, templates CRUD, LLM template generation, run, export) — or drive the same capabilities as MCP tools over streamable HTTP (/mcp) or stdio (`gitrakz mcp`). Use when the user wants to set up gitrakz, trigger or check a GitHub activity sync, pull a timeline or work-sessions timesheet, or run and export a template.
homepage: https://github.com/psyb0t/gitrakz
user-invocable: true
metadata:
  openclaw:
    emoji: "🛰️"
    primaryEnv: GITRAKZ_URL
    requires:
      bins: [bash, curl, docker, gh]
permissions:
  network: "Outbound HTTP only to the user-configured GITRAKZ_URL (the local gitrakz server). gitrakz itself shells out to the GitHub CLI and reaches api.github.com to sync activity; point it only at a gitrakz instance the user runs."
  shell: "bash, curl, and the docker / gitrakz-wrapper commands shown in references/setup.md, for user-requested setup or verification. gitrakz reads its GitHub token from `gh auth token`."
  filesystem: "Normal use reads GITRAKZ_URL and GITRAKZ_AUTH_TOKEN from the environment. Setup writes only the owner-only ~/.config/gitrakz/.env and docker-compose.yml."
---

# gitrakz

gitrakz is a self-hosted GitHub activity tracker. It syncs a user's `gh`
activity into a local SQLite database, renders a filterable timeline and derived
work sessions, and runs **programmatic templates** — deterministic transform
pipelines over the timeline that export to CSV, PDF, or JSON. One Go binary with
the Svelte UI embedded; no external services required.

For setup — the installer, the direct-Docker path, config, and auth — read
[references/setup.md](references/setup.md) before touching a stack.

## Security and safety

- This skill drives a gitrakz instance the user already runs. Take `GITRAKZ_URL`
  (e.g. `http://127.0.0.1:8080`) and, if set, `GITRAKZ_AUTH_TOKEN` from the
  environment or ask — do not hunt the workspace for tokens.
- gitrakz authenticates to GitHub with a token from `gh auth token`, injected at
  runtime and never written to disk. It reads activity only; mount a read-scoped
  token where you control the scope.
- `POST /api/v1/sync` starts a GitHub sync (network + rate-limit spend) and
  `POST /api/v1/run` may call an LLM if the template uses `describe-work` or a
  prose block. Only trigger these for the task the user named.
- `GITRAKZ_ELELEM_BASE_URL` receives commit titles / diffs when LLM steps run.
  Point it only at endpoints the user trusts. Template output is typed display
  blocks, never author-supplied HTML.
- gitrakz also exposes its capabilities as MCP tools (see "MCP" below), over the
  same two surfaces: streamable HTTP at `/mcp` (Bearer-gated exactly like
  `/api/v1` when `GITRAKZ_AUTH_TOKEN` is set) and stdio via the binary's `mcp`
  subcommand. Every MCP tool wraps the same read-mostly service layer as the
  REST API above — same sync/LLM cost caveats apply to `gitrakz_trigger_sync`
  and `gitrakz_run_template`.

## Use it for

- Installing or running gitrakz and confirming it is up.
- Triggering an incremental sync (`POST /api/v1/sync`) and checking progress
  (`GET /api/v1/sync/status`).
- Pulling a filtered timeline or a derived work-sessions timesheet.
- Listing, creating, editing, and running templates, and exporting a run to
  CSV / PDF / JSON.
- Any of the above through MCP tools instead of raw REST calls, when the
  driving client speaks MCP (see "MCP" below).

## Do not use it for

- Writing to GitHub — gitrakz only reads activity.
- Any instance the user does not run and trust.
- Treating `/api/v1/run` output as HTML — it is a typed block document.

## Talk to a running instance

All endpoints are under `/api/v1`, JSON, camelCase. When `GITRAKZ_AUTH_TOKEN` is
set on the server, send `Authorization: Bearer <token>`; when it is empty the API
is open (single-user / trusted network). The SPA at `/` needs no token.

```bash
: "${GITRAKZ_URL:=http://127.0.0.1:8080}"
auth=(); [ -n "${GITRAKZ_AUTH_TOKEN:-}" ] && auth=(-H "Authorization: Bearer $GITRAKZ_AUTH_TOKEN")

# Is it up? (SPA, unauthenticated)
curl -fsS "$GITRAKZ_URL/" >/dev/null && echo "gitrakz is up"

# Trigger a sync, then poll status.
curl -fsS "${auth[@]}" -X POST "$GITRAKZ_URL/api/v1/sync"
curl -fsS "${auth[@]}" "$GITRAKZ_URL/api/v1/sync/status"

# Distinct owners, then repos under one.
curl -fsS "${auth[@]}" "$GITRAKZ_URL/api/v1/owners"
curl -fsS "${auth[@]}" "$GITRAKZ_URL/api/v1/repos?owner=OWNER"

# Timeline (paginated with hasMore — never a total) and derived sessions.
curl -fsS "${auth[@]}" "$GITRAKZ_URL/api/v1/timeline?owner=OWNER&from=2025-01-01&perPage=50"
curl -fsS "${auth[@]}" "$GITRAKZ_URL/api/v1/sessions?owner=OWNER"
```

## Endpoints

Everything the SPA does is one of these calls:

- `GET  /api/v1/owners` — distinct owners.
- `GET  /api/v1/repos?owner=` — repos under an owner.
- `GET  /api/v1/timeline?owner=&repo=&type=&from=&to=&page=&perPage=` — events;
  `type` is one of `commit|pr|review|issue|release`. Paginated with `hasMore`.
- `GET  /api/v1/sessions?…` — sessionized view + heuristic hours.
- `POST /api/v1/sync` — trigger an incremental sync.
- `GET  /api/v1/sync/status` — last sync status.
- `GET  /api/v1/templates` — list (built-in + custom).
- `POST /api/v1/templates` — create a custom template.
- `PUT  /api/v1/templates/{id}` — edit (built-ins clone-on-edit).
- `DELETE /api/v1/templates/{id}` — delete a custom template.
- `POST /api/v1/templates/generate` — LLM-compose a template draft from a prompt.
- `POST /api/v1/run` — run a template over a filter → a typed block document.
- `POST /api/v1/export` — export a document / run to `csv | pdf | json`.

The OpenAPI spec at `api/api.yml` in the repo is the source of truth for request
and response shapes.

## MCP

gitrakz exposes the same capabilities above as MCP (Model Context Protocol)
tools — no REST calls needed if the client speaks MCP. Both transports serve
identical tools against the same running instance's SQLite data.

### Tools

- `gitrakz_list_owners` — every owner with ingested activity. No input.
- `gitrakz_list_repos` — repos under `owner` (required).
- `gitrakz_list_templates` — every saved template (built-in + custom). No input.
- `gitrakz_get_template` — one template by `id` (required).
- `gitrakz_run_template` — run `templateId` (required) over an optional
  `filter` (`owner`/`repo`/`type`/`from`/`to`) and `formValues`; returns the
  rendered document as typed display blocks (never HTML).
- `gitrakz_trigger_sync` — trigger one incremental `gh` sync. No input. Same
  network + rate-limit cost as `POST /api/v1/sync`.
- `gitrakz_get_sync_status` — current sync status. No input.
- `gitrakz_list_sessions` — derived work sessions over an optional
  `owner`/`from`/`to` filter.
- `gitrakz_query_timeline` — one page of the filtered, newest-first event
  timeline (`owner`/`repo`/`type`/`from`/`to`/`page`/`perPage`).

### Streamable HTTP — same host as the REST API

Mounted at `/mcp` on the running instance, alongside `/api/v1`. Bearer-gated
the same way: send `Authorization: Bearer <token>` when `GITRAKZ_AUTH_TOKEN`
is set on the server.

```json
{
  "mcpServers": {
    "gitrakz": {
      "type": "http",
      "url": "http://127.0.0.1:8080/mcp",
      "headers": { "Authorization": "Bearer <GITRAKZ_AUTH_TOKEN>" }
    }
  }
}
```

Omit `headers` when the server has no `GITRAKZ_AUTH_TOKEN` set.

### stdio — local Claude Code use

The Go binary's `mcp` subcommand (not the shell wrapper's `gitrakz start` /
`stop` / etc. commands) opens the exact same SQLite database and runs the MCP
server over stdio. Since gitrakz ships as a container, run it through Docker
with `-i` for a live stdin/stdout pipe, against the same named data volume the
stack already uses:

```json
{
  "mcpServers": {
    "gitrakz": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-e", "GH_TOKEN",
        "-v", "gitrakz-data:/data",
        "psyb0t/gitrakz:vX.Y.Z", "mcp"
      ],
      "env": { "GH_TOKEN": "<gh auth token>" }
    }
  }
}
```

Pin the same released tag the running stack uses. `GH_TOKEN` is only needed
for `gitrakz_trigger_sync`; every read-only tool works without it.

## Setup

Everything about installing, running with Docker directly, configuring
`~/.config/gitrakz/.env`, and the `GH_TOKEN` auth model lives in
[references/setup.md](references/setup.md).
