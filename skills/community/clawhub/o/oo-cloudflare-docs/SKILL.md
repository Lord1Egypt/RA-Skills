---
name: oo-cloudflare-docs
description: "Cloudflare Docs (developers.cloudflare.com). Use this skill for ANY Cloudflare Docs request — searching and reading data. Whenever a task involves Cloudflare Docs, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Cloudflare Docs"
  author: "OOMOL"
  version: "1.0.4"
  services: ["cloudflare_docs"]
  icon: "https://static.oomol.com/logo/third-party/cloudflare_docs.svg"
---

# Cloudflare Docs

Operate **Cloudflare Docs** through your OOMOL-connected account. This skill calls the `cloudflare_docs` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Cloudflare Docs. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "cloudflare_docs" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "cloudflare_docs" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_pages_to_workers_migration_guide` — Get the guide and instructions for migrating Cloudflare Pages projects to Cloudflare Workers.
- `search_cloudflare_documentation` — Search Cloudflare documentation for Workers, Pages, R2, Images, Stream, D1, Durable Objects, KV, Workflows, Hyperdrive, Queues, AI Search, Workers AI, Vectorize, AI Gateway, Browser Run, Zero Trust, Access, Tunnel, Gateway, Browser Isolation, WARP, DDOS, Magic Transit, Magic WAN, CDN, Cache, DNS, Zaraz, Argo, Rulesets, Terraform, Account and Billing.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Cloudflare Docs state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Cloudflare Docs is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/connections/cloudflare_docs
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Cloudflare Docs homepage: https://developers.cloudflare.com
- API documentation: https://developers.cloudflare.com/agents/model-context-protocol/mcp-servers-for-cloudflare/
