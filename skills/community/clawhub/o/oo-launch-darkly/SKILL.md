---
name: oo-launch-darkly
description: "LaunchDarkly (launchdarkly.com). Use this skill for ANY LaunchDarkly request — reading, creating, updating, and deleting data. Whenever a task involves LaunchDarkly, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "LaunchDarkly"
  author: "OOMOL"
  version: "1.0.1"
  services: ["launch_darkly"]
  icon: "https://static.oomol.com/logo/third-party/LaunchDarkly.svg"
---

# LaunchDarkly

Operate **LaunchDarkly** through your OOMOL-connected account. This skill calls the `launch_darkly` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected LaunchDarkly. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "launch_darkly" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "launch_darkly" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_member_to_teams` — Add one or more LaunchDarkly members to one or more teams with a semantic patch update. [write]
- `create_environment` — Create a LaunchDarkly environment using either common fields or a full official request body. [write]
- `create_feature_flag` — Create a LaunchDarkly feature flag using either common fields or a full official request body. [write]
- `create_project` — Create a LaunchDarkly project using either common fields or a full official request body. [write]
- `create_segment` — Create a LaunchDarkly segment using either common fields or a full official request body. [write]
- `create_team` — Create a LaunchDarkly team using either common fields or a full official request body. [write]
- `create_token` — Create a LaunchDarkly access token using either common fields or a full official request body. [write]
- `delete_environment` — Delete a LaunchDarkly environment by project key and environment key. [destructive]
- `delete_feature_flag` — Delete a LaunchDarkly feature flag by project key and feature flag key. [destructive]
- `delete_project` — Delete a LaunchDarkly project by project key. [destructive]
- `delete_segment` — Delete a LaunchDarkly segment by project key, environment key, and segment key. [destructive]
- `delete_team` — Delete a LaunchDarkly team by team key. [destructive]
- `delete_token` — Delete a LaunchDarkly access token by token identifier. [destructive]
- `get_caller_identity` — Get the LaunchDarkly caller identity for the current access token.
- `get_context_instances` — Get a LaunchDarkly context instance by project key, environment key, and context instance identifier.
- `get_contexts` — Get a LaunchDarkly context by context kind and key, with optional paging over related results.
- `get_environment` — Get a LaunchDarkly environment by project key and environment key.
- `get_environments` — List the LaunchDarkly environments that belong to a project.
- `get_feature_flag` — Get a LaunchDarkly feature flag by project key and feature flag key.
- `get_feature_flags` — List LaunchDarkly feature flags in a project with optional filtering, pagination, and summary output.
- `get_member` — Get a LaunchDarkly account member by member identifier.
- `get_members` — List LaunchDarkly account members with optional filtering, sorting, pagination, and expansion.
- `get_project` — Get a LaunchDarkly project by project key.
- `get_segment` — Get a LaunchDarkly segment by project key, environment key, and segment key.
- `get_segments` — List LaunchDarkly segments in a project environment with optional filtering and pagination.
- `get_tags` — List LaunchDarkly tags with optional prefix and resource-kind filters.
- `get_team` — Get a LaunchDarkly team by team key.
- `get_token` — Get a LaunchDarkly access token by token identifier.
- `get_tokens` — List LaunchDarkly access tokens with optional pagination and visibility scope.
- `list_projects` — List LaunchDarkly projects with optional filtering, sorting, pagination, and expansion.
- `list_teams` — List LaunchDarkly teams with optional filtering, pagination, and expansion controls.
- `patch_environment` — Patch a LaunchDarkly environment with standard JSON Patch operations. [write]
- `patch_feature_flag` — Patch a LaunchDarkly feature flag with JSON Patch, JSON Merge Patch, or semantic patch instructions. [write]
- `patch_project` — Patch a LaunchDarkly project with standard JSON Patch operations. [write]
- `patch_segment` — Patch a LaunchDarkly segment with JSON Patch, JSON Merge Patch, or semantic patch instructions. [write]
- `patch_team` — Patch a LaunchDarkly team with semantic patch instructions. [write]
- `patch_token` — Patch a LaunchDarkly access token with standard JSON Patch operations. [write]
- `reset_token` — Reset a LaunchDarkly access token value and optionally control when the old value expires. [destructive]
- `search_context_instances` — Search LaunchDarkly context instances in a project environment with filtering, sorting, and pagination.
- `search_contexts` — Search LaunchDarkly contexts in a project environment with filtering, sorting, and pagination.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change LaunchDarkly state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — LaunchDarkly is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=launch_darkly
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- LaunchDarkly homepage: https://launchdarkly.com
