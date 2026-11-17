---
name: oo-bing-webmaster
description: "Bing Webmaster Tools (bing.com). Use this skill for ANY Bing Webmaster Tools request — reading, creating, updating, and deleting data. Whenever a task involves Bing Webmaster Tools, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Bing Webmaster Tools"
  author: "OOMOL"
  version: "1.0.2"
  services: ["bing_webmaster"]
  icon: "https://static.oomol.com/logo/third-party/bing_webmaster.png"
---

# Bing Webmaster Tools

Operate **Bing Webmaster Tools** through your OOMOL-connected account. This skill calls the `bing_webmaster` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Bing Webmaster Tools. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "bing_webmaster" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "bing_webmaster" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_blocked_url` — Block a page or directory, including cache-only and full-removal modes. [destructive]
- `add_connected_page` — Add a page connected to the site. [write]
- `add_country_region_settings` — Set country or region targeting for a URL scope. [destructive]
- `add_deep_link_block` — Block a deep link for a search URL and market. [destructive]
- `add_query_parameter` — Add a URL normalization parameter. [write]
- `add_site` — Add a site to the account. Ownership must be verified separately. [write]
- `add_site_roles` — Delegate site access to a user with administrator, read-only or read-write permissions. [destructive]
- `get_content_submission_quota` — Get the remaining content submission quota.
- `get_crawl_issues` — List URLs with crawl issues. Resolved issues may take several days to disappear.
- `get_crawl_settings` — Read the current crawl settings.
- `get_crawl_stats` — Get daily crawl statistics for the last six months.
- `get_fetched_url_details` — Read the document, headers and status of a fetched URL.
- `get_keyword_stats` — Get historical keyword statistics for a country and language.
- `get_page_query_stats` — Get search queries and traffic for a specific page.
- `get_page_stats` — Get traffic and position statistics for top pages. The Query field contains the page URL.
- `get_query_page_detail_stats` — Get detailed statistics for a search query and page.
- `get_query_page_stats` — Get page statistics for a search query.
- `get_query_stats` — Get traffic and position statistics for top search queries. Bing updates this report weekly.
- `get_query_traffic_stats` — Get traffic statistics for a search query.
- `get_rank_and_traffic_stats` — Get daily site impressions and clicks across Bing search verticals.
- `get_sitemap_details` — List feed details within a sitemap index.
- `get_url_info` — Get index and crawl information for a page or directory.
- `get_url_submission_quota` — Get the remaining URL submission quota before submitting URLs.
- `get_url_traffic_info` — Get traffic information for a page or directory.
- `list_blocked_urls` — List blocked pages and directories.
- `list_child_url_info` — List child URLs with filters. This read operation uses POST.
- `list_child_url_traffic_info` — List traffic information for child URLs.
- `list_connected_pages` — List pages connected to the site.
- `list_country_region_settings` — List country and region targeting settings.
- `list_deep_link_blocks` — List deep link blocking rules.
- `list_fetched_urls` — List URL fetch records, including fetched and expired flags.
- `list_link_counts` — List page inbound link counts with pagination.
- `list_page_preview_blocks` — List active page preview blocks.
- `list_query_parameters` — List URL query parameter normalization rules.
- `list_site_moves` — List site move records.
- `list_site_roles` — List delegated site roles, optionally including subdomains.
- `list_sitemaps` — List top-level sitemaps and feeds registered for a site.
- `list_sites` — List the sites registered in the Bing Webmaster account, including unverified sites.
- `list_url_links` — List inbound links and anchor text for a page.
- `remove_blocked_url` — Remove an existing page or directory block. [destructive]
- `remove_country_region_settings` — Remove country or region targeting settings. [destructive]
- `remove_deep_link_block` — Remove a deep link blocking rule. [destructive]
- `remove_page_preview_block` — Remove a page preview block. [destructive]
- `remove_query_parameter` — Remove a URL normalization parameter. [destructive]
- `remove_site` — Remove a site from the account. [destructive]
- `remove_site_role` — Remove a delegated site role. [destructive]
- `remove_sitemap` — Remove a registered sitemap or feed. [destructive]
- `save_crawl_settings` — Save crawl settings for a site, replacing supplied settings. [destructive]
- `set_query_parameter_enabled` — Enable or disable a URL normalization parameter. [destructive]
- `submit_site_move` — Submit a site move between source and destination URLs. [destructive]
- `submit_sitemap` — Submit a sitemap, RSS 2.0, Atom 0.3, Atom 1.0, or text feed URL to Bing. [write]
- `submit_url` — Submit one URL to Bing for crawling, subject to the available submission quota. [write]
- `submit_url_batch` — Submit up to 500 URLs to Bing in one request, subject to the available submission quota. [write]
- `verify_site` — Attempt to verify site ownership and return whether verification succeeded. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Bing Webmaster Tools state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Bing Webmaster Tools is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/bing_webmaster
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Bing Webmaster Tools homepage: https://www.bing.com/webmasters/
- API documentation: https://learn.microsoft.com/en-us/bingwebmaster/getting-access
