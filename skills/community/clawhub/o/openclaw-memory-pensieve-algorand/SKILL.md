---
name: openclaw-memory-pensieve-algorand-v3
description: Long-term episodic memory for OpenClaw with append-only hash-chained local layers, daily dream-cycle consolidation, AES-GCM encrypted Algorand anchoring, and post-anchor recoverability validation. Single MCP server — no scripts, no extra venvs.
---

# OpenClaw Memory Pensieve v3.0.0

## MCP server

All functionality is in one file: `server.py`.

Register it in Claude Code settings:

```json
{
  "mcpServers": {
    "pensieve": {
      "command": "python3",
      "args": ["/path/to/server.py"],
      "env": {
        "OPENCLAW_WORKSPACE": "/path/to/workspace",
        "ALGORAND_WALLET_ADDRESS": "<address>",
        "ALGORAND_WALLET_MNEMONIC": "<25-word mnemonic>",
        "ALGORAND_NOTE_KEY_HEX": "<64 hex chars = 32 bytes>",
        "ALGORAND_ALGOD_URL": "https://mainnet-api.algonode.cloud",
        "ALGORAND_INDEXER_URL": "https://mainnet-idx.algonode.cloud"
      }
    }
  }
}
```

Install dependencies (one-time):

```bash
pip install mcp algosdk cryptography
```

## Tools

| Tool | Purpose |
|------|---------|
| `pensieve_capture` | Append an event to the hash-chained ledger (deduplicates by content) |
| `pensieve_dream_cycle` | Promote 24 h recurring patterns into semantic / procedural / self_model |
| `pensieve_anchor` | Encrypt + anchor today's memory to Algorand (idempotent, auto-chunks) |
| `pensieve_validate` | Run v2.1 hardening: chain integrity, decrypt, parity, chunk hashes |
| `pensieve_recover` | Reconstruct memory from blockchain for a given date |
| `pensieve_status` | Layer counts, chain tip, last anchor date, today's cost estimate |

## Daily workflow

1. Capture events throughout the day with `pensieve_capture`.
2. At end-of-day, run `pensieve_dream_cycle` to consolidate patterns.
3. Run `pensieve_anchor` to encrypt and commit to Algorand.
4. Run `pensieve_validate` — only trust recovery claims when `ok=true`.

## Mandatory operational rules

- All `*.jsonl` files are append-only. Never rewrite or delete lines.
- Secrets stay in env vars (or `.secrets/`). Never print them in chat.
- Anchor encrypted payloads only — never plaintext memory.
- Treat `pensieve_validate` failures as blocking for disaster-recovery claims.

## Security

Sensitive values are read from environment variables at runtime:

- `ALGORAND_WALLET_MNEMONIC` — never logged, never written to disk by the server.
- `ALGORAND_NOTE_KEY_HEX` — 64 hex chars (32-byte AES key).

Fallback to `.secrets/algorand-wallet-nox.json` and `.secrets/algorand-note-key.bin`
is supported for local development only. Prefer env vars in all deployments.

Use a **dedicated low-balance anchoring wallet**. Fund it with enough ALGO for
your expected daily TX volume (see cost model in `server.py` module docstring).
Never reuse the main OpenClaw operations wallet for anchoring.

## Recovery

```python
# Recover and inspect
pensieve_recover(date="2026-03-14")

# Recover and write files to memory/recovered/
pensieve_recover(date="2026-03-14", restore=True)
```

## Architecture reference

See `references/architecture.md` for memory layer model and integrity guarantees.
See `references/hardening-v21.md` for the v2.1 pass/fail contract.
