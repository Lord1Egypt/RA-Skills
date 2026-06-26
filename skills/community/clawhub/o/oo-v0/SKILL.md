---
name: oo-v0
description: "v0 (v0.dev). Use this skill for ANY v0 request — reading, creating, updating, and deleting data. Whenever a task involves v0, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "v0"
  author: "OOMOL"
  version: "1.0.1"
  services: ["v0"]
  icon: "https://static.oomol.com/logo/third-party/V0.svg"
---

# v0

Operate **v0** through your OOMOL-connected account. This skill calls the `v0` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected v0. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "v0" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "v0" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `assign_project_to_chat` — Assign an existing v0 chat to a project container. [write]
- `create_chat` — Create a new v0 chat and immediately send the first message. [write]
- `create_deployment` — Create a deployment for a specific v0 chat version. [write]
- `create_env_vars` — Create one or more environment variables on a v0 project. [write]
- `create_hook` — Create a webhook hook in v0 for chat or message events. [write]
- `create_project` — Create a new v0 project container for chats, environment variables, and deployments. [write]
- `create_vercel_project` — Create and link a Vercel project from a v0 project. [write]
- `delete_chat` — Delete a v0 chat by chat ID. [destructive]
- `delete_env_vars` — Delete one or more environment variables from a v0 project. [destructive]
- `delete_hook` — Delete a webhook hook by hook ID. [destructive]
- `delete_project` — Delete a v0 project by project ID. [destructive]
- `favorite_chat` — Mark or unmark a v0 chat as favorite.
- `find_chats` — List chats in the connected v0 workspace with optional filters.
- `find_deployment_errors` — Get the current error summary for a v0 deployment.
- `find_deployment_logs` — List logs for a v0 deployment, optionally continuing from a previous timestamp.
- `find_deployments` — List deployments for a specific project, chat, and version combination.
- `find_env_vars` — List environment variables configured on a v0 project.
- `find_hooks` — List webhook hooks configured in the connected v0 workspace.
- `find_messages` — List messages for a v0 chat.
- `find_projects` — List v0 projects available to the connected account.
- `find_rate_limit` — Get current v0 rate-limit information for the workspace or a specific scope.
- `find_vercel_projects` — List Vercel projects linked to the connected v0 workspace.
- `find_versions` — List generated versions for a v0 chat.
- `fork_chat` — Fork an existing v0 chat into a new chat workspace.
- `get_billing` — Get current v0 billing and quota information.
- `get_chat` — Get a single v0 chat, including the current messages when v0 returns them.
- `get_deployment` — Get a single deployment by deployment ID.
- `get_env_var` — Get a single environment variable from a v0 project.
- `get_hook` — Get a single webhook hook by hook ID.
- `get_message` — Get a single message from a v0 chat.
- `get_plan` — Get the current subscription plan for the connected v0 user.
- `get_project` — Get a single v0 project by project ID.
- `get_project_by_chat` — Get the v0 project currently linked to a chat.
- `get_usage_report` — Get usage events and pagination information from the v0 usage report API.
- `get_user` — Get the authenticated v0 user profile for the connected API key.
- `get_user_scopes` — List workspaces and scopes accessible to the connected v0 user.
- `get_version` — Get a single v0 chat version, optionally including default deployment files.
- `init_chat` — Initialize a new v0 chat from files, a repository, a registry, a zip archive, or a template.
- `resume_message` — Resume a previously asynchronous v0 message generation. [write]
- `send_message` — Send a follow-up message to an existing v0 chat. [write]
- `update_chat` — Update a v0 chat's metadata such as its name or privacy. [write]
- `update_env_vars` — Update existing environment variables on a v0 project. [write]
- `update_hook` — Update an existing webhook hook in v0. [write]
- `update_project` — Update a v0 project's metadata, instructions, visibility, or linked Vercel project. [write]
- `update_version` — Update the files of an existing v0 chat version. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change v0 state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — v0 is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=v0
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- v0 homepage: https://v0.dev
