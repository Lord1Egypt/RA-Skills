---
name: oo-buildkite
description: "Buildkite (buildkite.com). Use this skill for ANY Buildkite request — reading, creating, and updating data. Whenever a task involves Buildkite, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Buildkite"
  author: "OOMOL"
  version: "1.0.1"
  services: ["buildkite"]
  icon: "https://static.oomol.com/logo/third-party/Buildkite.svg"
---

# Buildkite

Operate **Buildkite** through your OOMOL-connected account. This skill calls the `buildkite` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Buildkite. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "buildkite" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "buildkite" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `cancel_build` — Cancel a Buildkite build by build number. [write]
- `create_build` — Create a new Buildkite build for a pipeline. [write]
- `get_build` — Get a single Buildkite build by organization, pipeline slug, and build number.
- `get_current_access_token` — Inspect the current Buildkite API access token, including scopes and owner summary.
- `get_current_user` — Get the Buildkite user account that owns the current API access token.
- `get_organization` — Get a single Buildkite organization by slug.
- `get_pipeline` — Get a single Buildkite pipeline by organization and pipeline slug.
- `list_builds_for_organization` — List builds across all pipelines in a Buildkite organization.
- `list_builds_for_pipeline` — List builds for a single Buildkite pipeline.
- `list_organizations` — List Buildkite organizations accessible to the current API token.
- `list_pipelines` — List Buildkite pipelines for an organization.
- `rebuild_build` — Rebuild a Buildkite build by build number.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Buildkite state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Buildkite is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=buildkite
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Buildkite homepage: https://buildkite.com
