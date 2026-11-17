---
name: oo-commonninja
description: "Common Ninja (commoninja.com). Use this skill for ANY Common Ninja request — reading, creating, updating, and deleting data. Whenever a task involves Common Ninja, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Common Ninja"
  author: "OOMOL"
  version: "1.0.2"
  services: ["commonninja"]
  icon: "https://static.oomol.com/logo/third-party/commonninja.svg"
---

# Common Ninja

Operate **Common Ninja** through your OOMOL-connected account. This skill calls the `commonninja` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Common Ninja. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "commonninja" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "commonninja" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_widget` — Create a Common Ninja widget. Choose draft or published explicitly. Omit data to use the type defaults, or obtain its configuration schema with get_widget_type_schema. [write]
- `delete_widget` — Delete a Common Ninja widget. Set permanent to true only when it must be irrecoverably removed. [destructive]
- `get_project` — Get a Common Ninja project by ID.
- `get_user` — Get the authenticated Common Ninja account profile.
- `get_widget` — Get a Common Ninja widget, including its type-specific configuration.
- `get_widget_editor_url` — Get a Common Ninja widget editor URL, which can be embedded in an iframe.
- `get_widget_embed_code` — Get the HTML container and SDK script for embedding a Common Ninja widget.
- `get_widget_type` — Get metadata for a Common Ninja widget type.
- `get_widget_type_schema` — Get the JSON Schema for a Common Ninja widget type before supplying widget configuration.
- `list_projects` — List Common Ninja projects. Only the documented limit is supported; automatic pagination is not available.
- `list_widget_types` — List Common Ninja widget types. Only documented limit and field selection are supported; automatic pagination is not available.
- `list_widgets` — List Common Ninja widgets with optional filters. Results exclude widget configuration; use get_widget to read it. Only documented list filters are supported; automatic pagination is not available.
- `update_widget` — Update selected Common Ninja widget fields. Omitted fields remain unchanged; configuration must match the widget type schema. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Common Ninja state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Common Ninja is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/commonninja
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Common Ninja homepage: https://www.commoninja.com/
- API documentation: https://developers.commoninja.com/docs/api/overview
