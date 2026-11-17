---
name: oo-vercel
description: "Vercel (vercel.com). Use this skill for ANY Vercel request — reading, creating, updating, and deleting data. Whenever a task involves Vercel, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Vercel"
  author: "OOMOL"
  version: "1.0.7"
  services: ["vercel"]
  icon: "https://static.oomol.com/logo/third-party/Vercel.svg"
---

# Vercel

Operate **Vercel** through your OOMOL-connected account. This skill calls the `vercel` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Vercel. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "vercel" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "vercel" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_project_domain` — Add a domain to a Vercel project. [write]
- `assign_deployment_alias` — Assign an alias to a Vercel deployment, moving it from any deployment that currently owns it. [destructive]
- `cancel_deployment` — Cancel a Vercel deployment that is still in progress. [destructive]
- `create_file_deployment` — Create an asynchronous Vercel deployment from file references returned by upload_deployment_file_from_url. [destructive]
- `create_git_deployment` — Create an asynchronous Vercel deployment from a Git repository connected to the account. [destructive]
- `create_project` — Create a Vercel project. [write]
- `create_project_env` — Create a Vercel project environment variable. [write]
- `create_webhook` — Create a Vercel webhook. [write]
- `delete_deployment` — Permanently delete a Vercel deployment. [destructive]
- `delete_project_env` — Delete a Vercel project environment variable. [destructive]
- `delete_webhook` — Delete a Vercel webhook. [destructive]
- `get_auth_user` — Get the authenticated Vercel user.
- `get_deployment` — Get a Vercel deployment.
- `get_deployment_events` — Get Vercel deployment events.
- `get_deployment_file_contents` — Get one Vercel deployment file as base64-encoded content.
- `get_domain_config` — Get domain configuration guidance from Vercel.
- `get_latest_deployment_promotion_aliases` — Get alias mapping statuses for the latest production promotion of a project; results are project-global and are not correlated to a specific promote_deployment call.
- `get_project` — Get a Vercel project.
- `get_project_domain` — Get a Vercel project domain.
- `get_runtime_logs` — Get runtime logs for a Vercel deployment.
- `get_team` — Get a Vercel team by id or slug.
- `get_webhook` — Get a Vercel webhook.
- `list_deployment_aliases` — List aliases currently assigned to a Vercel deployment.
- `list_deployment_files` — List the source file tree stored for a Vercel deployment.
- `list_deployments` — List Vercel deployments.
- `list_project_domains` — List domains for a Vercel project.
- `list_project_envs` — List environment variables for a Vercel project.
- `list_projects` — List Vercel projects.
- `list_teams` — List Vercel teams available to the authenticated user.
- `list_webhooks` — List Vercel webhooks.
- `promote_deployment` — Request Vercel to point a project's production traffic to an existing deployment. [destructive]
- `redeploy_deployment` — Create an asynchronous Vercel deployment from an existing deployment's source and settings. [destructive]
- `rollback_deployment` — Roll back a Vercel project's production traffic to a previous deployment. [destructive]
- `update_deployment_integration_action` — Update the status and optional outcomes of a Vercel Marketplace integration action attached to a deployment. [destructive]
- `update_deployment_rollback_description` — Update the recorded reason for a Vercel production rollback. [write]
- `update_project` — Update a Vercel project. [write]
- `update_project_env` — Update a Vercel project environment variable. [write]
- `upload_deployment_file_from_url` — Download one public file through the Connector SSRF guard, calculate its SHA-1 digest when needed, and upload up to 1 GiB through the Connector to Vercel for a file-based deployment. [write]
- `verify_project_domain` — Verify a Vercel project domain.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Vercel state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Vercel is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/vercel
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Vercel homepage: https://vercel.com
- API documentation: https://vercel.com/docs/rest-api
