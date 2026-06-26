---
name: oo-figma
description: "Figma (figma.com). Use this skill for ANY Figma request — reading, creating, updating, and deleting data. Whenever a task involves Figma, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Figma"
  author: "OOMOL"
  version: "1.0.2"
  services: ["figma"]
  icon: "https://static.oomol.com/logo/third-party/figma.svg"
---

# Figma

Operate **Figma** through your OOMOL-connected account. This skill calls the `figma` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Figma. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "figma" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "figma" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_dev_resources` — Create dev resources and attach them to Figma file nodes. [write]
- `delete_comment` — Delete a Figma comment created by the authenticated user. [destructive]
- `delete_comment_reaction` — Delete an emoji reaction created by the authenticated user. [destructive]
- `delete_dev_resource` — Delete a Figma dev resource from a main file. [destructive]
- `get_component` — Get metadata for a published Figma component by key.
- `get_component_set` — Get metadata for a published Figma component set by key. [write]
- `get_current_user` — Get the current Figma user associated with the API key.
- `get_dev_resources` — Get dev resources attached to a Figma main file.
- `get_file` — Get the JSON document for a Figma file or branch.
- `get_file_metadata` — Get lightweight metadata for a Figma file without fetching its full document.
- `get_file_nodes` — Get JSON for selected node IDs from a Figma file or branch.
- `get_image_fills` — Get temporary download URLs for image fills used in a Figma file.
- `get_project_metadata` — Get metadata for a Figma project.
- `get_style` — Get metadata for a published Figma style by key.
- `list_comment_reactions` — List emoji reactions on a Figma file comment. [write]
- `list_comments` — List comments on a Figma file or branch.
- `list_file_component_sets` — List published component sets in a Figma main file library.
- `list_file_components` — List published components in a Figma main file library.
- `list_file_styles` — List published styles in a Figma main file library.
- `list_file_versions` — List version history records for a Figma file.
- `list_project_files` — List files in a Figma project.
- `list_team_projects` — List projects visible to the authenticated user in a Figma team.
- `post_comment` — Post a comment on a Figma file or branch. [write]
- `post_comment_reaction` — Add an emoji reaction to a Figma file comment. [write]
- `render_images` — Render selected Figma file nodes and return temporary image URLs.
- `update_dev_resources` — Update existing Figma dev resources. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Figma state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Figma is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key, OAuth2) at:

  ```text
  https://console.oomol.com/app-connections?provider=figma
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Figma homepage: https://www.figma.com
