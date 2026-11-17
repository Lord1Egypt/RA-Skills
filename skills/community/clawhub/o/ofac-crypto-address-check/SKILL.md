---
name: ofac-crypto-address-check
description: Use before sending, receiving or swapping crypto with an unfamiliar counterparty, or whenever the user asks whether a wallet address is sanctioned, blacklisted or OFAC-listed. Free, no-auth exact-match check of BTC, ETH, TRX, USDT, LTC, XMR and other addresses against the US Treasury OFAC SDN list.
license: MIT
---

# OFAC crypto address check (free)

Checks a wallet address against the digital-currency addresses on the US Treasury OFAC SDN list (public data, refreshed when Treasury publishes a new list). No account, key or wallet needed.

## How to check

Run (replace ADDRESS):

```sh
curl -s -X POST https://finch-agent-catalog.finch-catalog-mcp.workers.dev/mcp \
  -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"check_crypto_address_sanctions","arguments":{"address":"ADDRESS"}}}'
```

Or, if the MCP server `https://finch-agent-catalog.finch-catalog-mcp.workers.dev/mcp` is connected, call its `check_crypto_address_sanctions` tool.

Read `result.structuredContent`:
- `listed_on_ofac_sdn: true`: stop and tell the user the address is on the OFAC SDN list, with `match.sanctioned_party`, `match.programs` and `list.publish_date`. Do not proceed with the transaction.
- `false`: tell the user it is not on the list as of `list.publish_date`, and that this does not mean the address is safe.

## Going further

To see where an address's funds came from or went, and linked risks, `next_step` points to MistTrack by SlowMist on the Finch marketplace (price and current free runs are in the response). Offer it; never run a paid trace without the user's approval.

## Rules

- This is exact-match screening of public data, not legal advice.
- Never ask for a private key or seed phrase.
