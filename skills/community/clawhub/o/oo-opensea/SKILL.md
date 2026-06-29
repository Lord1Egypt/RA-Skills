---
name: oo-opensea
description: "OpenSea (opensea.io). Use this skill for ANY OpenSea request — searching and reading data. Whenever a task involves OpenSea, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "OpenSea"
  author: "OOMOL"
  version: "1.0.1"
  services: ["opensea"]
  icon: "https://static.oomol.com/logo/third-party/opensea.svg"
---

# OpenSea

Operate **OpenSea** through your OOMOL-connected account. This skill calls the `opensea` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected OpenSea. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "opensea" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "opensea" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_best_nft_listing` — Get the best current OpenSea listing for a single NFT.
- `get_best_nft_offer` — Get the best current OpenSea offer for a single NFT.
- `get_collection` — Get one OpenSea collection including details, links, fees, and traits.
- `get_collection_stats` — Get comprehensive OpenSea statistics for one collection.
- `get_nft` — Get metadata, traits, ownership, and rarity for a single OpenSea NFT.
- `list_collection_nfts` — List NFTs in one OpenSea collection with optional trait filtering.
- `list_collection_offers` — List collection-level offers for an OpenSea collection.
- `list_collection_traits` — List all available traits for an OpenSea collection.
- `search` — Search OpenSea collections, tokens, NFTs, and accounts by relevance.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change OpenSea state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — OpenSea is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=opensea
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- OpenSea homepage: https://opensea.io
