---
name: oo-cartes
description: "Cartes.io (cartes.io). Use this skill for ANY Cartes.io request — reading, creating, updating, and deleting data. Whenever a task involves Cartes.io, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Cartes.io"
  author: "OOMOL"
  version: "1.0.4"
  services: ["cartes"]
  icon: "https://static.oomol.com/logo/third-party/cartes.png"
---

# Cartes.io

Operate **Cartes.io** through your OOMOL-connected account. This skill calls the `cartes` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Cartes.io. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "cartes" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "cartes" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_map` — Create a Cartes.io map. [write]
- `create_marker` — Create a marker on one Cartes.io map. [write]
- `create_marker_location` — Append a new location point to one Cartes.io marker. [write]
- `delete_map` — Delete one Cartes.io map. [destructive]
- `delete_marker` — Delete one marker from a Cartes.io map. [destructive]
- `get_current_user` — Get the current Cartes.io user for the connected API token.
- `get_map` — Get one Cartes.io map.
- `get_marker` — Get one marker from a Cartes.io map.
- `get_user` — Get one public Cartes.io user.
- `list_categories` — List Cartes.io marker categories.
- `list_maps` — List public Cartes.io maps, optionally including maps owned by the account.
- `list_markers` — List markers on one Cartes.io map.
- `list_public_markers` — List public Cartes.io markers across public maps.
- `list_related_maps` — List Cartes.io maps related to one map.
- `list_users` — List public Cartes.io users.
- `search_maps` — Search public Cartes.io maps.
- `update_map` — Update one Cartes.io map. [write]
- `update_marker` — Update one marker on a Cartes.io map. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Cartes.io state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Cartes.io is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/cartes
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Cartes.io homepage: https://cartes.io/
- API documentation: https://docs.cartes.io/developers/api/
