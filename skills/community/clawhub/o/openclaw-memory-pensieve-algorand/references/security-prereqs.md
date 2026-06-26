# Security & prerequisites

## Dependencies

Install once, system-wide or in a virtualenv:

```bash
pip install mcp algosdk cryptography
```

## Secrets configuration

Secrets are read from **environment variables** (recommended) or from a
local fallback file (local development only).

### Recommended: environment variables

Set these in your MCP server config (e.g. Claude Code `settings.json`):

| Variable | Description |
|---|---|
| `ALGORAND_WALLET_ADDRESS` | Algorand account address |
| `ALGORAND_WALLET_MNEMONIC` | 25-word mnemonic — never log or print |
| `ALGORAND_NOTE_KEY_HEX` | 64 hex chars = 32-byte AES-GCM encryption key |
| `ALGORAND_ALGOD_URL` | Algod endpoint (default: `https://mainnet-api.algonode.cloud`) |
| `ALGORAND_ALGOD_TOKEN` | Algod token (leave empty for public nodes) |
| `ALGORAND_INDEXER_URL` | Indexer endpoint (default: `https://mainnet-idx.algonode.cloud`) |
| `ALGORAND_INDEXER_TOKEN` | Indexer token (leave empty for public nodes) |

### Fallback: local secret files

Only for local development. The server will use these if the env vars above
are absent:

- `<workspace>/.secrets/algorand-wallet-nox.json` — JSON with `address` and `mnemonic`
- `<workspace>/.secrets/algorand-note-key.bin` — raw 32-byte binary key

Set restrictive permissions on the `.secrets/` directory:

```bash
chmod 700 <workspace>/.secrets
chmod 600 <workspace>/.secrets/*
```

Never commit `.secrets/` to version control.

## Safety constraints

- Never print secret material (mnemonic, raw keys) in logs or chat.
- Never include `.secrets/*` in git or any distributable artifact.
- The server validates that the mnemonic matches the address before sending any transaction.
- Treat recovery claims as valid only after `pensieve_validate` returns `ok=true`.

## Wallet guidance

Use a **dedicated low-balance anchoring wallet** — never reuse your main
operations wallet. Fund it with enough ALGO for your expected daily TX volume
(see cost model in `server.py` module docstring). Top up as needed.

## Deployment checklist

1. Install dependencies: `pip install mcp algosdk cryptography`
2. Set environment variables in your MCP server config.
3. Register `server.py` as an MCP server in Claude Code.
4. Run `pensieve_status()` to confirm the server starts and workspace is reachable.
5. Run a test capture + anchor + validate cycle before relying on it for real data.
