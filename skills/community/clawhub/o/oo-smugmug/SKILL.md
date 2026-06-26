---
name: oo-smugmug
description: "SmugMug (smugmug.com). Use this skill for ANY SmugMug request — searching and reading data. Whenever a task involves SmugMug, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "SmugMug"
  author: "OOMOL"
  version: "1.0.1"
  services: ["smugmug"]
  icon: "https://static.oomol.com/logo/third-party/SmugMug.svg"
---

# SmugMug

Operate **SmugMug** through your OOMOL-connected account. This skill calls the `smugmug` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected SmugMug. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "smugmug" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "smugmug" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_album` — Retrieve a SmugMug album by album key.
- `get_album_highlight_image` — Retrieve the highlight image for a SmugMug album.
- `get_album_image` — Retrieve a specific image within a SmugMug album context.
- `get_album_images` — List the images contained in a SmugMug album.
- `get_folder_albums` — List the direct albums under a SmugMug folder path.
- `get_folder_by_user_path` — Retrieve a SmugMug folder by user nickname and folder path.
- `get_folder_details` — Retrieve folder details for a SmugMug folder node by node ID.
- `get_folder_subfolders` — List the direct subfolders under a SmugMug folder path.
- `get_image` — Retrieve a SmugMug image by image key.
- `get_image_metadata` — Retrieve the metadata extracted from a SmugMug image file.
- `get_image_size_details` — Retrieve the full SmugMug image size details payload for an image.
- `get_image_sizes` — Summarize the usable image sizes for a SmugMug image from the official image size details payload.
- `get_node_highlight_image` — Retrieve the highlight image for a SmugMug node.
- `get_node_parent` — Retrieve the direct parent node of a SmugMug node.
- `get_node_parents` — Retrieve the breadcrumb trail of parent nodes for a SmugMug node.
- `get_user` — Retrieve a SmugMug user by nickname.
- `get_user_bio_image` — Retrieve the bio image for a SmugMug user.
- `get_user_featured_albums` — Retrieve the featured albums for a SmugMug user.
- `get_user_features` — Retrieve the feature and entitlement map for a SmugMug user.
- `get_user_profile` — Retrieve the public profile for a SmugMug user.
- `get_user_root_node` — Retrieve the root node for a SmugMug user.
- `list_child_nodes` — List the immediate child nodes under a SmugMug node.
- `search_user_content` — Search a SmugMug user's images by query text, with optional ordering and pagination.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change SmugMug state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — SmugMug is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=smugmug
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- SmugMug homepage: https://www.smugmug.com
