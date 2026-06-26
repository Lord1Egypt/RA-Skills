---
name: oo-tiktok-business
description: "TikTok Business (business.tiktok.com). Use this skill for ANY TikTok Business request — searching and reading data. Whenever a task involves TikTok Business, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "TikTok Business"
  author: "OOMOL"
  version: "1.0.1"
  services: ["tiktok_business"]
  icon: "https://static.oomol.com/logo/third-party/tiktok.svg"
---

# TikTok Business

Operate **TikTok Business** through your OOMOL-connected account. This skill calls the `tiktok_business` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected TikTok Business. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "tiktok_business" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "tiktok_business" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `check_gmv_max_shop_ad_usage` — Check whether a TikTok Shop store is already using custom shop ads and can promote all products with GMV Max.
- `get_gmv_max_bid_recommendation` — Get TikTok GMV Max budget and bid recommendations before campaign changes.
- `get_gmv_max_campaign_info` — Get detailed information for a TikTok GMV Max campaign.
- `get_gmv_max_custom_anchor_video_list` — Get TikTok GMV Max custom anchor videos for campaign creation discovery.
- `get_gmv_max_exclusive_authorization` — Get TikTok GMV Max exclusive authorization status for a store.
- `get_gmv_max_identities` — List TikTok identities available for a GMV Max store.
- `get_gmv_max_report` — Get TikTok GMV Max reporting rows for a store and date range.
- `get_gmv_max_sessions` — Get TikTok GMV Max campaign session details by session ID.
- `get_gmv_max_shop_video_anchors` — Get TikTok GMV Max shop video anchors for campaign creation discovery.
- `get_gmv_max_videos` — Get TikTok GMV Max videos available for a store, identity, or SPU filter.
- `list_advertisers` — List TikTok advertisers authorized for the connected TikTok Business user.
- `list_campaigns` — List TikTok campaigns for an advertiser so users can discover campaign IDs.
- `list_gmv_max_occupied_custom_shop_ads` — List custom shop ads occupying TikTok assets before GMV Max setup.
- `list_gmv_max_sessions` — List TikTok GMV Max campaign sessions for a campaign.
- `list_gmv_max_stores` — List TikTok Shop stores available to a TikTok GMV Max advertiser.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change TikTok Business state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — TikTok Business is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/app-connections?provider=tiktok_business
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- TikTok Business homepage: https://business.tiktok.com
