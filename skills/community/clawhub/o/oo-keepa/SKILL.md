---
name: oo-keepa
description: "Keepa (keepa.com). Use this skill for ANY Keepa request — searching and reading data. Whenever a task involves Keepa, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Keepa"
  author: "OOMOL"
  version: "1.0.6"
  services: ["keepa"]
  icon: "https://static.oomol.com/logo/third-party/keepa.svg"
---

# Keepa

Operate **Keepa** through your OOMOL-connected account. This skill calls the `keepa` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Keepa. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "keepa" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "keepa" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `find_deals` — Find recently changed Amazon products with Keepa deal filters and bounded pagination.
- `find_products` — Find Amazon ASINs with Keepa Product Finder filters using official ProductFinderRequest field names.
- `find_sellers` — Find seller IDs by official Seller Finder criteria without fetching seller profiles.
- `get_best_sellers` — Retrieve Keepa's ordered Amazon best-seller ASIN list for a category node or website display group.
- `get_lightning_deal` — Get lightning deals for a required ASIN, avoiding the costly full-list request.
- `get_most_rated_sellers` — Get seller IDs ordered by rating count, with a local result window; each window fetches and pays for the full upstream list.
- `get_product_history` — Retrieve named Keepa price, rank, offer-count, rating, review, monthly-sales, and coupon history for Amazon ASINs.
- `get_product_snapshot` — Retrieve current Keepa product metadata and named statistics for one or more Amazon ASINs.
- `get_seller_snapshot` — Retrieve compact Keepa marketplace seller profiles, ratings, category statistics, brands, and competitors.
- `get_seller_storefront` — Inspect one seller's observed storefront ASINs and aligned last-seen times; the list can be incomplete.
- `get_token_status` — Retrieve Keepa token availability and refill information without consuming tokens.
- `list_lightning_deals` — List lightning deals with a local result window; Keepa charges 500 tokens for each full upstream request, regardless of window size.
- `lookup_categories` — Look up up to ten Amazon category IDs and optionally their parent tree; ID zero lists roots.
- `search_categories` — Search Keepa Amazon categories by name so category IDs can be used in product and best-seller queries.
- `search_products` — Search Amazon products by keyword in Amazon result order, without fetching more details.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Keepa state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Keepa is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/keepa
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Keepa homepage: https://keepa.com/
- API documentation: https://keepa.com/api-docs/request-basics.html
