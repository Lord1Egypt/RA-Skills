---
name: oo-meta
description: "Meta (Facebook) (business.meta.com). Use this skill for ANY Meta (Facebook) request — reading, creating, updating, and deleting data. Whenever a task involves Meta (Facebook), use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Meta (Facebook)"
  author: "OOMOL"
  version: "1.0.5"
  services: ["meta"]
  icon: "https://static.oomol.com/logo/third-party/meta.svg"
---

# Meta (Facebook)

Operate **Meta (Facebook)** through your OOMOL-connected account. This skill calls the `meta` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Meta (Facebook). **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "meta" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "meta" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_insights_report` — Start an asynchronous Meta Ads insights report. Use get_insights_report to poll and retrieve its first result page; report handles expire after 30 days. [write]
- `create_page_post` — Create a text, link, or attached-photo post on a managed Facebook Page, immediately, unpublished, or scheduled. Upload unpublished photos first to obtain attachment IDs. [write]
- `delete_page_post` — Delete a post from a managed Facebook Page. [destructive]
- `get_ad` — Retrieve one Meta ad and its creative reference.
- `get_ad_account` — Retrieve one Meta ad account.
- `get_ad_creative` — Retrieve one Meta ad creative.
- `get_ad_set` — Retrieve one Meta ad set including budget, targeting, and delivery settings.
- `get_campaign` — Retrieve one Meta advertising campaign.
- `get_current_user` — Retrieve the current Meta Graph API user for the connected access token.
- `get_insights` — Retrieve Meta Ads insights for an ad account, campaign, ad set, or ad object.
- `get_insights_report` — Check an asynchronous Meta Ads report and fetch a result page once complete. Pass the returned after cursor to retrieve further pages.
- `get_page` — Retrieve a managed Facebook Page using its Page access token.
- `get_page_post` — Retrieve a Facebook Page post using the owning Page access token.
- `list_ad_accounts` — List Meta ad accounts available to the connected access token.
- `list_ad_creatives` — List Meta ad creatives under an ad account.
- `list_ad_sets` — List Meta ad sets under an ad account.
- `list_ads` — List Meta ads under an ad account.
- `list_campaigns` — List campaigns under one Meta ad account with optional delivery status filters.
- `list_page_posts` — List posts from a managed Facebook Page feed, including visitor content where permitted. Inspect is_published to distinguish published and unpublished posts.
- `list_pages` — List Facebook Pages available to the connected user or system user, including assigned tasks. Access tokens are never returned.
- `publish_page_photo` — Publish or stage a photo on a managed Facebook Page from a public image URL. Meta downloads the image. Set published=false to obtain a photo ID for an attached-media post. [write]
- `update_page_post` — Update a Facebook Page post created by the same Meta app, including text, attachments, and publishing settings. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Meta (Facebook) state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Meta (Facebook) is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2, API key) at:

  ```text
  https://console.oomol.com/connections/meta
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Meta (Facebook) homepage: https://business.meta.com/
- API documentation: https://developers.facebook.com/docs/
