---
name: oo-giphy
description: "GIPHY (giphy.com). Use this skill for ANY GIPHY request — searching and reading data. Whenever a task involves GIPHY, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "GIPHY"
  author: "OOMOL"
  version: "1.0.1"
  services: ["giphy"]
  icon: "https://static.oomol.com/logo/third-party/giphy.png"
---

# GIPHY

Operate **GIPHY** through your OOMOL-connected account. This skill calls the `giphy` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected GIPHY. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "giphy" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "giphy" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_gif` — Get a GIPHY GIF by GIF Object id. This is not the random_id value.
- `get_random_gif` — Fetch a random GIPHY GIF, optionally filtered by tag.
- `get_random_id` — Create a GIPHY random_id value for personalization across requests.
- `get_random_sticker` — Fetch a random GIPHY sticker, optionally filtered by tag.
- `list_categories` — List GIPHY content categories.
- `list_gifs_by_ids` — Fetch multiple GIPHY GIFs by id.
- `list_related_tags` — List GIPHY tags related to a term.
- `list_trending_gifs` — List trending GIPHY GIFs.
- `list_trending_stickers` — List trending GIPHY stickers.
- `list_trending_tags` — List trending search terms on GIPHY.
- `search_gifs` — Search GIPHY GIFs by query text.
- `search_stickers` — Search GIPHY stickers by query text.
- `search_tags` — Autocomplete GIPHY tags for a partial query.
- `translate_gif` — Translate a phrase into a single best-match GIPHY GIF.
- `translate_sticker` — Translate a phrase into a single best-match GIPHY sticker.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change GIPHY state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — GIPHY is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=giphy
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- GIPHY homepage: https://giphy.com
