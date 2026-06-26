---
name: maverick-pandadoc-mcp
description: Use PandaDoc integration context for documents, templates, recipients, proposals, and document status. Use after Maverick connects PandaDoc and provisions runtime OAuth credentials; this skill has no provider-owned MCP manifest registered in this repository yet.
metadata:
  openclaw:
    emoji: "📄"
    requires:
      bins:
        - mcporter
        - jq
        - flock
        - shasum
      env:
        - MAVERICK_PANDADOC_MCP_REFRESH_TOKEN
        - MAVERICK_PANDADOC_MCP_CLIENT_ID
        - MAVERICK_PANDADOC_MCP_ACCESS_TOKEN
    primaryEnv: MAVERICK_PANDADOC_MCP_REFRESH_TOKEN
    install:
      - id: node
        kind: node
        package: mcporter
        bins:
          - mcporter
        label: Install mcporter (node)
---

# PandaDoc

## Quick start

This skill has the shared `mcporter` wrapper scripts, but no skill-local `mcporter.json` is registered for PandaDoc yet. Do not call `bash {baseDir}/scripts/invoke.sh` until a provider MCP manifest is added. In current runtime, inspect the available PandaDoc tools first, then use the smallest read path that can identify the document, template, recipient, proposal, or status target.

When a PandaDoc MCP manifest is added, follow the same wrapper rule as Linear: invoke through `bash {baseDir}/scripts/invoke.sh`, never call `mcporter` directly, and discover tool schemas before choosing tool names.

## Safety

Write operations that create, send, update, complete, delete, or modify documents, templates, recipients, proposals, or document status can affect customer-visible signing workflows. Confirm clear user intent before invoking write tools, and read current document/template state before making changes.

## Authentication

Tokens are provisioned and rotated automatically. If available runtime tools return HTTP 401 that doesn't recover within a few seconds, the OAuth grant has been revoked — re-authorize the integration to refresh credentials.

## Data flow

No provider-owned PandaDoc MCP endpoint is registered in this repository yet. Runtime tool calls, if present in the active OpenClaw environment, use Maverick-provisioned OAuth credentials and expose PandaDoc document, template, recipient, proposal, and status data to the active tool provider. Use this skill for PandaDoc-related work only; do not pass unrelated sensitive content through these tools.

## Dependencies

- **`mcporter`** ([github.com/steipete/mcporter](https://github.com/steipete/mcporter)) — MCP CLI used by the shared wrapper once a PandaDoc MCP manifest exists. Auto-installed via `npm install -g --ignore-scripts mcporter` if missing on PATH (see `install` spec in frontmatter). The install spec uses unpinned `mcporter` (npm `latest`); operators with strict supply-chain controls should override the install to pin a specific version (e.g. `mcporter@<version>`).
- **`jq`** ([stedolan.github.io/jq](https://stedolan.github.io/jq/)) — JSON processor used by the vault initializer. System dependency; install via your OS package manager (`apt install jq`, `brew install jq`, etc.).
- **`flock`** (part of [util-linux](https://github.com/util-linux/util-linux)) — file locking used to serialize concurrent vault writes. Available by default on Linux; on macOS install via `brew install flock`.
- **`shasum`** (Perl, ships with [`Digest::SHA`](https://metacpan.org/pod/Digest::SHA)) — computes the SHA-256 hashes used to derive the mcporter vault key and the provisioned-token marker. Preinstalled on macOS and on Debian/Ubuntu (incl. the deployed `cloudflare/sandbox` Ubuntu 22.04 image); on minimal Linux images install `perl-Digest-SHA`. The script invokes `shasum -a 256` rather than GNU `sha256sum` so it runs on stock macOS without `coreutils`.
