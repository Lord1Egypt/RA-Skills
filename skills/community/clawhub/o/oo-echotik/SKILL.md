---
name: oo-echotik
description: "EchoTik (echotik.live). Use this skill for ANY EchoTik request — searching and reading data. Whenever a task involves EchoTik, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "EchoTik"
  author: "OOMOL"
  version: "1.0.5"
  services: ["echotik"]
  icon: "https://static.oomol.com/logo/third-party/echotik.png"
---

# EchoTik

Operate **EchoTik** through your OOMOL-connected account. This skill calls the `echotik` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected EchoTik. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "echotik" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "echotik" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_category_overview` — Get EchoTik's T+1 market-size, sales, GMV, product, creator, price, and live-commerce overview for one first-level category.
- `get_category_trend` — Get EchoTik offline daily sales and GMV trend snapshots for a region and optional first-, second-, or third-level category filters.
- `get_influencer_details` — Get EchoTik's offline creator profiles for up to 10 TikTok user IDs or handles in one request.
- `get_live_details` — Get EchoTik's offline audience and commerce profiles for up to 10 TikTok live rooms in one request.
- `get_product_details` — Get EchoTik's detailed offline commerce profile for up to 10 TikTok Shop products in one request.
- `get_product_trend` — Get up to 180 days of EchoTik offline price, sales, GMV, creator, video, and live snapshots for one product.
- `get_shop_details` — Get EchoTik's offline TikTok Shop profile for a seller discovered through product or proxy workflows.
- `get_video_details` — Get EchoTik's offline engagement and commerce profiles for up to 10 TikTok videos in one request.
- `list_product_categories` — List EchoTik's localized TikTok Shop category dictionary at the first, second, or third level.
- `list_product_comments` — List EchoTik's offline TikTok Shop product reviews with optional integer rating filters.
- `list_product_influencers` — List creators associated with an EchoTik product, including estimated attributed sales and GMV.
- `list_product_lives` — List offline live sessions associated with an EchoTik product, including audience and estimated sales performance.
- `list_product_rankings` — List EchoTik daily, weekly, or monthly TikTok Shop product rankings by sales or creator promotion growth.
- `list_product_videos` — List offline commerce videos associated with an EchoTik product, including engagement and estimated sales performance.
- `list_products` — Browse EchoTik's T+1 TikTok Shop product dataset with category, sales, GMV, price, commission, store, and ranking filters.
- `resolve_product_id` — Resolve a TikTok product share URL to the stable product ID used by EchoTik product actions.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change EchoTik state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — EchoTik is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/connections/echotik
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- EchoTik homepage: https://echotik.live/zh/api-service
- API documentation: https://opendocs.echotik.live/introduction
