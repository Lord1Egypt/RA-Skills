---
name: oo-ipdata-co
description: "ipdata.co (ipdata.co). Use this skill for ANY ipdata.co request — searching and reading data. Whenever a task involves ipdata.co, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "ipdata.co"
  author: "OOMOL"
  version: "1.0.1"
  services: ["ipdata_co"]
  icon: "https://static.oomol.com/logo/third-party/ipdata_co.svg"
---

# ipdata.co

Operate **ipdata.co** through your OOMOL-connected account. This skill calls the `ipdata_co` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected ipdata.co. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "ipdata_co" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "ipdata_co" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `bulk_lookup` — Look up up to 100 IP addresses in a single ipdata bulk API request.
- `get_calling_code` — Look up the calling_code field for a specific IP address or the caller's current IP address.
- `get_carrier_by_ip` — Look up carrier data for a specific IP address or the caller's current IP address.
- `get_city` — Look up the city field for a specific IP address or the caller's current IP address.
- `get_company_by_ip` — Look up company data for a specific IP address or the caller's current IP address.
- `get_continent_code` — Look up the continent_code field for a specific IP address or the caller's current IP address.
- `get_continent_name` — Look up the continent_name field for a specific IP address or the caller's current IP address.
- `get_count` — Look up the count field for a specific IP address or the caller's current IP address.
- `get_country_code` — Look up the country_code field for a specific IP address or the caller's current IP address.
- `get_country_name` — Look up the country_name field for a specific IP address or the caller's current IP address.
- `get_currency_by_ip` — Look up currency data for a specific IP address or the caller's current IP address.
- `get_emoji_flag` — Look up the emoji_flag field for a specific IP address or the caller's current IP address.
- `get_emoji_unicode` — Look up the emoji_unicode field for a specific IP address or the caller's current IP address.
- `get_flag` — Look up the flag field for a specific IP address or the caller's current IP address.
- `get_ip` — Look up the IP field for a specific IP address or the caller's current IP address.
- `get_is_eu` — Look up the is_eu field for a specific IP address or the caller's current IP address.
- `get_languages_by_ip` — Look up language data for a specific IP address or the caller's current IP address.
- `get_latitude` — Look up the latitude field for a specific IP address or the caller's current IP address.
- `get_longitude` — Look up the longitude field for a specific IP address or the caller's current IP address.
- `get_postal` — Look up the postal field for a specific IP address or the caller's current IP address.
- `get_region` — Look up the region field for a specific IP address or the caller's current IP address.
- `get_region_code` — Look up the region_code field for a specific IP address or the caller's current IP address.
- `get_threat_by_ip` — Look up threat intelligence data for a specific IP address or the caller's current IP address.
- `get_time_zone_by_ip` — Look up time zone data for a specific IP address or the caller's current IP address.
- `lookup_advanced_asn` — Look up advanced autonomous system details by ASN number with the ipdata ASN endpoint.
- `lookup_basic_asn_by_ip` — Look up a specific IP address and return only the ASN object from the ipdata response.
- `lookup_current_ip` — Look up the caller's current IP address with the ipdata main API endpoint.
- `lookup_current_ip_eu` — Look up the caller's current IP address with the ipdata EU API endpoint.
- `lookup_ip` — Look up a specific IP address with the ipdata main API endpoint.
- `lookup_ip_eu` — Look up a specific IP address with the ipdata EU API endpoint.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change ipdata.co state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — ipdata.co is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=ipdata_co
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- ipdata.co homepage: https://ipdata.co
