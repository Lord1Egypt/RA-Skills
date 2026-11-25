---
name: oo-piloterr
description: "Piloterr (piloterr.com). Use this skill for ANY Piloterr request — searching and reading data. Whenever a task involves Piloterr, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Piloterr"
  author: "OOMOL"
  version: "1.0.0"
  services: ["piloterr"]
  icon: "https://static.oomol.com/logo/third-party/piloterr.svg"
---

# Piloterr

Operate **Piloterr** through your OOMOL-connected account. This skill calls the `piloterr` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Piloterr. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "piloterr" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "piloterr" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `amazon_search` — Search an Amazon marketplace and get products with ASIN, title, price, rating and review count.
- `crunchbase_company` — Get a company's Crunchbase profile by name, permalink or URL, or by website domain: description, size, categories, locations, investors and products.
- `detect_technologies` — Detect the technologies a website runs, such as its CMS, frameworks, analytics, CDN and hosting.
- `ebay_get_listing` — Get an eBay listing by item ID or URL, with its price, condition, availability, seller, shipping and item specifics.
- `ebay_search` — Search eBay listings by keyword or search URL and get their price, condition, buying format, shipping and seller.
- `fetch_html` — Fetch a public web page over fast HTTP, without running JavaScript, and get its HTML.
- `google_search` — Search Google and get organic results with their position, title, link and snippet, and the estimated total.
- `linkedin_company` — Get a LinkedIn company's profile by page URL, slug or ID, or by website domain: industry, size, headquarters, specialties and followers.
- `render_html` — Render a JavaScript-heavy page in a headless browser and get the HTML after rendering.
- `screenshot` — Capture a public web page as a PNG, JPEG, WebP image or a PDF, by viewport, full page or CSS selector, and store it as a file.
- `zillow_property` — Get a Zillow home from its homedetails URL: address, price, Zestimate, status, size, rooms, year built and photos.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Piloterr state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Piloterr is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/piloterr
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Piloterr homepage: https://www.piloterr.com
- API documentation: https://docs.piloterr.com
