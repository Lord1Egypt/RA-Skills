---
name: oo-doppler
description: "Doppler (doppler.com). Use this skill for ANY Doppler request — reading, creating, updating, and deleting data. Whenever a task involves Doppler, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Doppler"
  author: "OOMOL"
  version: "1.0.1"
  services: ["doppler"]
  icon: "https://static.oomol.com/logo/third-party/Doppler.svg"
---

# Doppler

Operate **Doppler** through your OOMOL-connected account. This skill calls the `doppler` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Doppler. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "doppler" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "doppler" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `clone_config` — Clone a Doppler branch config and its secrets.
- `create_change_request` — Create a Doppler change request with one or more units. [write]
- `create_config` — Create a branch config under a Doppler project and environment. [write]
- `create_environment` — Create an environment under a Doppler project. [write]
- `create_project` — Create a Doppler project in the current workplace. [write]
- `create_service_token` — Create a new service token for a specific project and config. [write]
- `create_sync` — Create a Doppler secrets sync for a project config. [write]
- `delete_config` — Delete a Doppler config. [destructive]
- `delete_environment` — Delete an environment from a Doppler project. [destructive]
- `delete_project` — Delete a Doppler project from the current workplace. [destructive]
- `delete_secret` — Delete a single secret for a specific project and config. [destructive]
- `delete_service_token` — Delete a service token for a specific project and config. [destructive]
- `delete_sync` — Delete a Doppler secrets sync. [destructive]
- `download_secrets` — Export secrets from a Doppler config in a specific format.
- `get_auth_me` — Get identity, principal, and workplace summary information for the current Doppler token.
- `get_change_request` — Get the details of a Doppler change request.
- `get_config` — Get the details of a single Doppler config.
- `get_config_log` — Get the details of a specific config change log entry.
- `get_environment` — Get the details of a single Doppler environment.
- `get_integration` — Get the details of a Doppler integration.
- `get_project` — Get the details of a single Doppler project.
- `get_secret` — Get the value and metadata of a single secret for a specific project and config.
- `get_sync` — Get the details of a Doppler secrets sync. [write]
- `issue_dynamic_secret_lease` — Issue a short-lived lease for a Doppler dynamic secret.
- `list_change_requests` — List Doppler workplace change requests.
- `list_config_logs` — List config change logs for a specific project and config.
- `list_configs` — List configs under a specific Doppler project.
- `list_environments` — List environments under a Doppler project.
- `list_integrations` — List Doppler integrations available in the workplace.
- `list_projects` — List the projects visible in the current Doppler workspace.
- `list_secret_names` — List only the secret names for a Doppler project and config.
- `list_secrets` — List all secrets and their metadata for a specific project and config.
- `list_service_tokens` — List service tokens for a specific project and config.
- `review_change_request_unit` — Submit an approving review for one Doppler change request unit.
- `revoke_dynamic_secret_lease` — Revoke a lease issued for a Doppler dynamic secret. [destructive]
- `set_config_inheritable` — Update whether a Doppler config can be inherited by other configs. [write]
- `update_change_request` — Update a Doppler change request's metadata or units. [write]
- `update_change_request_assignees` — Replace the reviewers assigned to a Doppler change request. [write]
- `update_change_request_unit_status` — Update the status of one Doppler change request unit. [write]
- `update_config` — Rename a Doppler config. [write]
- `update_environment` — Rename a Doppler environment or update personal config settings. [write]
- `update_project` — Update a Doppler project's name or description. [write]
- `update_secret_note` — Update the note for a specific secret. [write]
- `update_secrets` — Create or update secrets in bulk for a specific project and config. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Doppler state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Doppler is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=doppler
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Doppler homepage: https://www.doppler.com
