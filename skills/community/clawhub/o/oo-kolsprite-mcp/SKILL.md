---
name: oo-kolsprite-mcp
description: "KOLSprite MCP (kolsprite.com). Use this skill for ANY KOLSprite MCP request — searching and reading data. Whenever a task involves KOLSprite MCP, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "KOLSprite MCP"
  author: "OOMOL"
  version: "1.0.2"
  services: ["kolsprite_mcp"]
  icon: "https://static.oomol.com/logo/third-party/kolsprite_mcp.png"
---

# KOLSprite MCP

Operate **KOLSprite MCP** through your OOMOL-connected account. This skill calls the `kolsprite_mcp` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected KOLSprite MCP. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "kolsprite_mcp" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "kolsprite_mcp" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `asin_analysis_video` — Find TikTok video signals related to an Amazon ASIN and marketplace. Results do not establish Amazon sales attribution.
- `caption_extract_url` — Extract captions from a video URL through KOLSprite. Set is_southeast_asia for Southeast Asian videos.
- `creator_category_list` — List creator categories and their values for creator_search.
- `creator_search` — Search TikTok creators by keyword, audience, engagement, and sales. Query creator_category_list or product_category_list before selecting a category.
- `product_category_list` — List the product category tree used by product, shop, video, and creator searches.
- `product_related_creator` — List creators promoting a TikTok Shop product, with optional contact availability and sorting filters.
- `product_search` — Search TikTok Shop products by keyword, price, sales, ratings, and category. Query product_category_list for category IDs.
- `shop_search` — Search TikTok Shop stores by keyword, category, ratings, sales, and operating model.
- `video_search` — Search TikTok videos by keyword, IDs, engagement, sales, dates, and linked products or shops.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change KOLSprite MCP state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — KOLSprite MCP is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/kolsprite_mcp
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- KOLSprite MCP homepage: https://www.kolsprite.com
- API documentation: https://o.kolsprite.com/doc/api.html
