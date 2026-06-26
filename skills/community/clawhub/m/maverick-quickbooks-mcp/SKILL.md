---
name: maverick-quickbooks-mcp
description: Use QuickBooks integration context for customers, invoices, payments, expenses, vendors, and financial reports. Use after Maverick connects QuickBooks and provisions runtime OAuth credentials; this skill has no provider-owned MCP manifest registered in this repository yet.
metadata:
  openclaw:
    emoji: "🧾"
    requires:
      bins:
        - mcporter
        - jq
        - flock
        - shasum
      env:
        - MAVERICK_QUICKBOOKS_MCP_REFRESH_TOKEN
        - MAVERICK_QUICKBOOKS_MCP_CLIENT_ID
        - MAVERICK_QUICKBOOKS_MCP_ACCESS_TOKEN
    primaryEnv: MAVERICK_QUICKBOOKS_MCP_REFRESH_TOKEN
    install:
      - id: node
        kind: node
        package: mcporter
        bins:
          - mcporter
        label: Install mcporter (node)
---

# QuickBooks

## Quick start

This skill has the shared `mcporter` wrapper scripts, but no skill-local `mcporter.json` is registered for QuickBooks yet. Do not call `bash {baseDir}/scripts/invoke.sh` until a provider MCP manifest is added. In current runtime, inspect the available QuickBooks tools first, then use the smallest read path that can identify the customer, invoice, payment, expense, vendor, or report target.

When a QuickBooks MCP manifest is added, follow the same wrapper rule as Linear: invoke through `bash {baseDir}/scripts/invoke.sh`, never call `mcporter` directly, and discover tool schemas before choosing tool names.

## Safety

Write operations that create, update, delete, send, void, or sync customers, invoices, payments, expenses, vendors, and accounting records can affect financial books. Confirm clear user intent before invoking write tools, and read current object state before any money-moving or accounting-affecting change.

## Authentication

Tokens are provisioned and rotated automatically. If available runtime tools return HTTP 401 that doesn't recover within a few seconds, the OAuth grant has been revoked — re-authorize the integration to refresh credentials.

## Data flow

No provider-owned QuickBooks MCP endpoint is registered in this repository yet. Runtime tool calls, if present in the active OpenClaw environment, use Maverick-provisioned OAuth credentials and expose QuickBooks customer, invoice, payment, expense, vendor, and report data to the active tool provider. Use this skill for QuickBooks-related work only; do not pass unrelated sensitive content through these tools.

## Dependencies

- **`mcporter`** ([github.com/steipete/mcporter](https://github.com/steipete/mcporter)) — MCP CLI used by the shared wrapper once a QuickBooks MCP manifest exists. Auto-installed via `npm install -g --ignore-scripts mcporter` if missing on PATH (see `install` spec in frontmatter). The install spec uses unpinned `mcporter` (npm `latest`); operators with strict supply-chain controls should override the install to pin a specific version (e.g. `mcporter@<version>`).
- **`jq`** ([stedolan.github.io/jq](https://stedolan.github.io/jq/)) — JSON processor used by the vault initializer. System dependency; install via your OS package manager (`apt install jq`, `brew install jq`, etc.).
- **`flock`** (part of [util-linux](https://github.com/util-linux/util-linux)) — file locking used to serialize concurrent vault writes. Available by default on Linux; on macOS install via `brew install flock`.
- **`shasum`** (Perl, ships with [`Digest::SHA`](https://metacpan.org/pod/Digest::SHA)) — computes the SHA-256 hashes used to derive the mcporter vault key and the provisioned-token marker. Preinstalled on macOS and on Debian/Ubuntu (incl. the deployed `cloudflare/sandbox` Ubuntu 22.04 image); on minimal Linux images install `perl-Digest-SHA`. The script invokes `shasum -a 256` rather than GNU `sha256sum` so it runs on stock macOS without `coreutils`.
