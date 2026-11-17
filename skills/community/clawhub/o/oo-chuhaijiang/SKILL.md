---
name: oo-chuhaijiang
description: "Chuhaijiang (chuhaijiang.com). Use this skill for ANY Chuhaijiang request — searching and reading data. Whenever a task involves Chuhaijiang, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Chuhaijiang"
  author: "OOMOL"
  version: "1.0.5"
  services: ["chuhaijiang"]
  icon: "https://static.oomol.com/logo/third-party/chuhaijiang.svg"
---

# Chuhaijiang

Operate **Chuhaijiang** through your OOMOL-connected account. This skill calls the `chuhaijiang` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Chuhaijiang. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "chuhaijiang" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "chuhaijiang" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_product` — Retrieve a TikTok Shop product from Chuhaijiang with product, shop, pricing, sales, and category details.
- `list_most_promoted_products` — List TikTok Shop products most heavily promoted by creators, videos, and live streams in Chuhaijiang.
- `list_new_arrival_products` — List recently launched TikTok Shop products that are quickly gaining sales in Chuhaijiang.
- `list_product_creators` — List TikTok creators associated with a product in Chuhaijiang.
- `list_product_lives` — List TikTok live streams associated with a product in Chuhaijiang.
- `list_product_reviews` — List TikTok Shop reviews associated with a product in Chuhaijiang.
- `list_product_videos` — List TikTok videos associated with a product in Chuhaijiang.
- `list_similar_products` — List TikTok products similar to a selected product in Chuhaijiang.
- `list_top_selling_products` — List TikTok Shop products ranked by sales for a selected market and statistics period in Chuhaijiang.
- `search_products` — Search TikTok Shop products in Chuhaijiang by market, keyword, category, price, rating, sales, shipping, and sort order.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Chuhaijiang state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Chuhaijiang is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/chuhaijiang
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Chuhaijiang homepage: https://www.chuhaijiang.com/
- API documentation: https://openapi-doc.chuhaijiang.com/introduction
