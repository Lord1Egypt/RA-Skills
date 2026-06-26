---
name: oo-swaggerhub
description: "SwaggerHub (swagger.io). Use this skill for ANY SwaggerHub request — searching and reading data. Whenever a task involves SwaggerHub, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "SwaggerHub"
  author: "OOMOL"
  version: "1.0.1"
  services: ["swaggerhub"]
  icon: "https://static.oomol.com/logo/third-party/Swaggerhub.svg"
---

# SwaggerHub

Operate **SwaggerHub** through your OOMOL-connected account. This skill calls the `swaggerhub` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected SwaggerHub. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "swaggerhub" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "swaggerhub" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_api_definition` — Fetch a SwaggerHub API definition in JSON or YAML format, with optional resolved and flattened output.
- `get_domain_definition` — Fetch a SwaggerHub domain definition in JSON or YAML format.
- `get_project` — Fetch a single SwaggerHub project by owner and project identifier.
- `get_template_definition` — Fetch a SwaggerHub template definition in JSON or YAML format, with optional flattening.
- `list_api_versions` — List the versions available for a specific SwaggerHub API.
- `list_domain_versions` — List the versions available for a specific SwaggerHub domain.
- `list_owner_apis` — List SwaggerHub APIs that belong to a specific owner.
- `list_owner_domains` — List SwaggerHub domains that belong to a specific owner.
- `list_projects` — List SwaggerHub projects for a specific owner.
- `list_template_versions` — List the versions available for a specific SwaggerHub template.
- `list_templates` — List SwaggerHub templates, optionally filtered by owner.
- `search_apis` — Search SwaggerHub APIs using the registry search endpoint.
- `search_domains` — Search SwaggerHub domains using the registry search endpoint.
- `search_registry_specs` — Search SwaggerHub registry items across APIs, domains, and templates using the unified /specs listing.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change SwaggerHub state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — SwaggerHub is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=swaggerhub
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- SwaggerHub homepage: https://swagger.io/tools/swaggerhub/
