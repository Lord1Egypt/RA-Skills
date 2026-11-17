---
name: oo-orbit
description: "Orbit (orbitsearch.com). Use this skill for ANY Orbit request — reading, creating, updating, and deleting data. Whenever a task involves Orbit, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Orbit"
  author: "OOMOL"
  version: "1.0.2"
  services: ["orbit"]
  icon: "https://static.oomol.com/logo/third-party/orbit.png"
---

# Orbit

Operate **Orbit** through your OOMOL-connected account. This skill calls the `orbit` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Orbit. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "orbit" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "orbit" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `batch_enrich` — Apply one enrichment operation to between 1 and 20 known Orbit profile IDs. Requires the `search:read` scope. Requests that include profiles also require `profile:read`. [write]
- `bulk_search` — Requires search:read and profile:read when any item includes profiles. Accepted items are queued and retry temporary execution failures automatically. [write]
- `cancel_bulk_search` — Cancel Undispatched Bulk Items. [destructive]
- `create_watcher` — Start watching a profile. Orbit checks it on the schedule you choose and adds what it finds to the profile. Each profile has one watcher per organization; creating a watcher for a profile you already watch updates that watcher and turns it back on. Requires the `watchers:write` scope. [write]
- `create_webhook` — Registers an HTTPS URL to receive signed event deliveries. The response includes the signing `secret` once. Requires the `webhooks:write` scope. [write]
- `delete_watcher` — Deletes the watcher and its schedule. Pausing keeps the configuration for later; deleting removes it. Requires the `watchers:write` scope. [destructive]
- `delete_webhook` — Deletes the endpoint. Deliveries stop immediately and the signing secret is invalidated. Requires the `webhooks:write` scope. [destructive]
- `detect_faces` — Store a photo privately and return every face in it, left to right. Requires the `search:read` scope. [write]
- `enrich_profile` — Read, upgrade, or regenerate one known Orbit profile. Requires the `search:read` scope. Requests that include the profile also require `profile:read`. [write]
- `get_batch_enrichment` — Read all accepted child enrichment requests in one call. Keep the request_ids from batch_enrich; completed_with_errors retains successful profiles and failed child details.
- `get_bulk_results` — Read Bulk Search Results.
- `get_bulk_search` — Read Bulk Search Progress.
- `get_enrichment` — Return the latest snapshot for one profile enrichment request. Poll while the status is `running`. Requires the `search:read` scope. Requests that include the profile also require `profile:read`.
- `get_search` — Return the latest search snapshot. Poll while the status is `running`. Requires the `search:read` scope. Searches that include profiles also require `profile:read`.
- `get_watcher` — One watcher, with its schedule and run counters. Requires the `watchers:write` scope.
- `list_watcher_runs` — The watcher's refresh runs, newest first: outcome, the events each run added with their sources, and what was billed. Requires the `watchers:write` scope.
- `list_watchers` — All your watchers. Requires the `watchers:write` scope.
- `list_webhooks` — Your registered endpoints, with masked signing secrets. Requires the `webhooks:write` scope.
- `quote_population` — What it costs to search everyone at a company or everyone who attended a school. Requires the `search:read` scope.
- `read_profile` — Read the current public profile for an Orbit profile ID, known alias ID, or public profile slug. When the stored profile is stale, the read can schedule a background refresh. Use POST /v3/enrich/{profile_id} to request a specific depth or regeneration. Requires the `profile:read` scope. Optional format=markdown returns compact factual USER.md, a manifest and populated section Markdown files in a JSON package; format=json is the default. Both representations use the same public-profile filtering, billing and refresh behavior.
- `search` — Find people, optionally discover additional candidates, and build every selected result to the requested profile depth. Requires the `search:read` scope. Requests that include profiles also require `profile:read`. [write]
- `search_face_index` — Return the Orbit profiles whose photos show the picked face. Requires the `search:read` scope.
- `search_population` — Search everyone at a company or everyone who attended a school. People are added to the results as the search finds them. Reserves the quoted credits. Requires the `search:read` scope. [write]
- `test_webhook` — Delivers one signed test event to the endpoint so you can verify your handler without waiting for a real event. The body is your most recent event of this type when you have one and the documented example payload otherwise; either way the envelope carries `"test": true` and an `evt_test_` event ID. Test deliveries are free, are never retried, and are not recorded in your delivery history. Requires the `webhooks:write` scope and is rate limited more tightly than other routes. [write]
- `update_watcher` — Pause, resume, retime or rescope a watcher. Send the fields you want to change. Requires the `watchers:write` scope. [destructive]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Orbit state — confirm the exact payload and effect with the user before running.**
- **Actions tagged `[destructive]` remove or overwrite data — always confirm the target and get explicit approval first.**

## First-time setup

These are **one-time** steps — do not repeat them on every call. Run a step only when a command fails for the matching reason.

- **`oo: command not found`** — install the oo CLI (other platforms: <https://cli.oomol.com/install-guide.md>):

  ```bash
  curl -fsSL https://cli.oomol.com/install.sh | bash    # macOS / Linux
  ```

  ```powershell
  irm https://cli.oomol.com/install.ps1 | iex           # Windows PowerShell
  ```

- **Not signed in / authentication error** — sign in to your OOMOL account once:

  ```bash
  oo auth login
  ```

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Orbit is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/orbit
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Orbit homepage: https://orbitsearch.com
- API documentation: https://docs.orbitsearch.com/authentication
