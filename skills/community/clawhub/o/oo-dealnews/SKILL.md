---
name: oo-dealnews
description: "DealNews (dealnews.com). Use this skill for ANY DealNews request — searching and reading data. Whenever a task involves DealNews, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "DealNews"
  author: "OOMOL"
  version: "1.0.4"
  services: ["dealnews"]
  icon: "https://static.oomol.com/logo/third-party/dealnews.svg"
---

# DealNews

Operate **DealNews** through your OOMOL-connected account. This skill calls the `dealnews` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

DealNews needs no account connection. Assume the oo CLI is installed and signed in. **Do not run `oo auth login` proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "dealnews" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "dealnews" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `list_blog_posts` — Get blog posts from the official DealNews RSS feed. Keep the returned content and referral-coded links unchanged, attribute public displays to DealNews, and do not use the feed in a publicly available browser extension.
- `list_category_deals` — Get deals from an official DealNews category RSS feed. Keep the returned content and referral-coded links unchanged, attribute public displays to DealNews, and do not use the feed in a publicly available browser extension.
- `list_editors_choice_deals` — Get Editors' Choice deals from the official DealNews RSS feed. Keep the returned content and referral-coded links unchanged, attribute public displays to DealNews, and do not use the feed in a publicly available browser extension.
- `list_latest_deals` — Get the most recent deals from the official DealNews RSS feed. Keep the returned content and referral-coded links unchanged, attribute public displays to DealNews, and do not use the feed in a publicly available browser extension.
- `list_popular_deals` — Get the most popular deals from the official DealNews RSS feed. Keep the returned content and referral-coded links unchanged, attribute public displays to DealNews, and do not use the feed in a publicly available browser extension.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change DealNews state — confirm the exact payload and effect with the user before running.**
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

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- DealNews homepage: https://www.dealnews.com/
- API documentation: https://www.dealnews.com/pages/rss.html
