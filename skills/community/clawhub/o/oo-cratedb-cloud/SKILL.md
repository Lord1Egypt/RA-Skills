---
name: oo-cratedb-cloud
description: "CrateDB Cloud (cratedb.com). Use this skill for ANY CrateDB Cloud request — searching and reading data. Whenever a task involves CrateDB Cloud, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "CrateDB Cloud"
  author: "OOMOL"
  version: "1.0.4"
  services: ["cratedb_cloud"]
  icon: "https://static.oomol.com/logo/third-party/cratedb_cloud.svg"
---

# CrateDB Cloud

Operate **CrateDB Cloud** through your OOMOL-connected account. This skill calls the `cratedb_cloud` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected CrateDB Cloud. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "cratedb_cloud" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "cratedb_cloud" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_cluster` — Return one CrateDB Cloud cluster by ID.
- `get_current_user` — Return the CrateDB Cloud user associated with the connected API key.
- `get_organization` — Return one CrateDB Cloud organization by ID.
- `get_project` — Return one CrateDB Cloud project by ID.
- `list_clusters` — List CrateDB Cloud clusters, optionally scoped to one organization or filtered by project.
- `list_organizations` — List CrateDB Cloud organizations visible to the connected API key.
- `list_products` — List available CrateDB Cloud products, optionally filtered by product kind.
- `list_projects` — List CrateDB Cloud projects, optionally scoped to one organization.
- `list_regions` — List CrateDB Cloud regions, optionally scoped to one organization.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change CrateDB Cloud state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — CrateDB Cloud is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/cratedb_cloud
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- CrateDB Cloud homepage: https://cratedb.com/database/cloud
- API documentation: https://cratedb.com/docs/cloud/en/latest/organization/api.html
