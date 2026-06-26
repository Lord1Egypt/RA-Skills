---
name: oo-control-d
description: "Control D (controld.com). Use this skill for ANY Control D request — reading, creating, updating, and deleting data. Whenever a task involves Control D, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Control D"
  author: "OOMOL"
  version: "1.0.1"
  services: ["control_d"]
  icon: "https://static.oomol.com/logo/third-party/Control%20D.svg"
---

# Control D

Operate **Control D** through your OOMOL-connected account. This skill calls the `control_d` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Control D. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "control_d" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "control_d" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `delete_profile_rule` — Delete one root-folder custom DNS rule from a Control D profile. [destructive]
- `get_current_ip` — Return the current IP address and datacenter seen by the Control D API for troubleshooting API token allowed-IP issues.
- `get_profile` — Fetch one Control D profile by primary key.
- `list_profile_rules` — List the root-folder custom DNS rules configured on a Control D profile.
- `list_profiles` — List the Control D profiles available to the authenticated API token.
- `list_service_categories` — List the Control D service categories that can be used for service discovery.
- `list_services_by_category` — List the Control D services available in one service category.
- `upsert_profile_rule` — Create or replace root-folder custom DNS rules on a Control D profile for one or more hostname patterns. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Control D state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Control D is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=control_d
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Control D homepage: https://controld.com
