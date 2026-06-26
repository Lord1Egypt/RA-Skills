---
name: oo-readme
description: "ReadMe (readme.com). Use this skill for ANY ReadMe request — reading, creating, updating, and deleting data. Whenever a task involves ReadMe, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "ReadMe"
  author: "OOMOL"
  version: "1.0.1"
  services: ["readme"]
  icon: "https://static.oomol.com/logo/third-party/readme.svg"
---

# ReadMe

Operate **ReadMe** through your OOMOL-connected account. This skill calls the `readme` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected ReadMe. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "readme" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "readme" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `ask_owlbot` — Ask ReadMe Owlbot a non-streaming question and return its answer with sources.
- `create_category` — Create a ReadMe guide or reference category. [write]
- `create_changelog` — Create a ReadMe changelog entry. [write]
- `create_custom_page` — Create a ReadMe custom page. [write]
- `create_doc` — Create a ReadMe doc page using a category ID or category slug. [write]
- `create_version` — Create a new ReadMe project version from an existing base version. [write]
- `delete_api_specification` — Delete one ReadMe API specification by ID. [destructive]
- `delete_category` — Delete one ReadMe category by slug. [destructive]
- `delete_changelog` — Delete one ReadMe changelog entry by slug. [destructive]
- `delete_custom_page` — Delete one ReadMe custom page by slug. [destructive]
- `delete_doc` — Delete one ReadMe doc page by slug. [destructive]
- `delete_version` — Delete one ReadMe project version by semver identifier. [destructive]
- `get_api_registry` — Retrieve one ReadMe API Registry entry by UUID.
- `get_category` — Get one ReadMe category by slug.
- `get_changelog` — Get one ReadMe changelog entry by slug.
- `get_custom_page` — Get one ReadMe custom page by slug.
- `get_doc` — Get one ReadMe doc by slug, optionally requesting the production doc version.
- `get_openapi_schema` — Get the OpenAPI definition for the ReadMe project.
- `get_project` — Get metadata for the ReadMe project associated with the API key.
- `get_version` — Get one ReadMe project version by semver identifier.
- `list_api_specifications` — List ReadMe API specification metadata with optional version and pagination.
- `list_categories` — List ReadMe guide and reference categories with optional version and pagination.
- `list_category_docs` — List the ReadMe docs that belong to a category slug.
- `list_changelogs` — List ReadMe changelog entries with optional pagination.
- `list_custom_pages` — List ReadMe custom pages with optional pagination.
- `list_outbound_ips` — List ReadMe outbound IP addresses used for webhook and Try It proxy requests.
- `list_versions` — List the versions configured for the ReadMe project.
- `search_docs` — Search ReadMe docs by text query.
- `update_category` — Update one ReadMe category by slug. [write]
- `update_changelog` — Update one ReadMe changelog entry by slug. [write]
- `update_custom_page` — Update one ReadMe custom page by slug. [write]
- `update_doc` — Update one ReadMe doc page by slug. [write]
- `update_version` — Update one ReadMe project version by semver identifier. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change ReadMe state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — ReadMe is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=readme
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- ReadMe homepage: https://readme.com
