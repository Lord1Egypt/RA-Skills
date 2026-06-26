---
name: oo-affinity
description: "Affinity (affinity.co). Use this skill for ANY Affinity request — searching and reading data. Whenever a task involves Affinity, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Affinity"
  author: "OOMOL"
  version: "1.0.1"
  services: ["affinity"]
  icon: "https://static.oomol.com/logo/third-party/affinity.svg"
---

# Affinity

Operate **Affinity** through your OOMOL-connected account. This skill calls the `affinity` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Affinity. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "affinity" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "affinity" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_company` — Get one Affinity company by ID with optional field selectors.
- `get_current_user` — Get the authenticated Affinity user, tenant, and API grant summary.
- `get_list` — Get one Affinity list by ID.
- `get_opportunity` — Get one Affinity opportunity by ID.
- `get_person` — Get one Affinity person by ID with optional field selectors.
- `get_saved_view` — Get one Affinity saved view by list ID and saved view ID.
- `list_companies` — List Affinity companies with optional ID and field selectors.
- `list_company_fields` — List non-list-specific Affinity company field metadata.
- `list_company_list_entries` — List all Affinity list entries for one company across lists.
- `list_company_lists` — List the Affinity lists that contain one company.
- `list_list_entries` — List the Affinity list entries for one list with optional field selectors.
- `list_list_fields` — List the field metadata for one Affinity list.
- `list_lists` — List the Affinity lists visible to the authenticated user.
- `list_opportunities` — List Affinity opportunities with optional ID filtering.
- `list_person_fields` — List non-list-specific Affinity person field metadata.
- `list_person_list_entries` — List all Affinity list entries for one person across lists.
- `list_person_lists` — List the Affinity lists that contain one person.
- `list_persons` — List Affinity persons with optional ID and field selectors.
- `list_saved_view_list_entries` — List the Affinity list entries returned by one saved view.
- `list_saved_views` — List the saved views configured on one Affinity list.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Affinity state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Affinity is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=affinity
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Affinity homepage: https://www.affinity.co
