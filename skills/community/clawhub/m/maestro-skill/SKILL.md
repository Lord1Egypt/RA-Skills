---
name: maestro-api
description: Query Maestro APIs over HTTP using the SIWX + JWT + x402 credit purchase flow. Resolve the exact endpoint from docs.gomaestro.org before requesting or paying.
---

# Maestro API

Use this skill when the user wants a direct HTTP call to a Maestro endpoint. The intended path is short: resolve the exact operation page, send the real request, satisfy the live SIWX challenge, and only buy credits if the server still returns `402`.

## Fast Path

1. Resolve the exact operation page in `docs.gomaestro.org`.
2. Read the page's `.md` form and use its `OpenAPI` block as the source of truth.
3. Build the request URL from `servers:` plus the operation path.
4. Send the real request with no auth or payment headers.
5. If the response is `200`, return the data.
6. If the response is `402` with `extensions.sign-in-with-x`, sign the SIWX challenge and retry the exact same request with `sign-in-with-x`.
7. If that retry returns `200`, return the data.
8. If that retry returns `402` plus `Authorization: Bearer <jwt>`, buy credits from the latest `accepts[]` entry and retry the exact same request with `Authorization` and `X-PAYMENT`.
9. Reuse the JWT for follow-up queries until it expires or Maestro asks for more credits.

## Resolve Endpoint From Docs

Use docs only to find the exact operation page. Do not browse broadly once you have it.

- Start with `https://docs.gomaestro.org/llms.txt` only if the operation page is not already obvious.
- Prefer operation pages over quick-start pages.
- Read the `.md` page and extract:
  - operation line -> path
  - `servers:` -> base URL for the chosen network
  - parameters and body schema -> request shape
- Combine `server.url + path`.
- Do not derive the REST host from the SIWX `domain` or `URI`.
- Useful Bitcoin routing shortcuts:
  - confirmed chain data -> Blockchain Indexer API
  - mempool-aware or pending data -> Mempool Monitoring API
  - mempool.space-style routes -> Esplora API
  - wallet balances or wallet activity -> Wallet API

## Minimal Prerequisites

Ask only for what is required to sign and pay:

- `PRIVATE_KEY`, or a runtime CDP wallet signer
- enough `USDC` and native gas on one network from the live `402` response
- no API key

## Request Rules

- Keep method, path, query parameters, and body unchanged across the unauthenticated request, the SIWX retry, and the paid retry.
- Always use the latest `402` response for `supported_chains`, `accepts[]`, `asset`, `pay_to`, and price limits.
- Confirm before the first paid mainnet request.
- If a paid retry still fails, report:
  - docs page used
  - selected network
  - selected amount
  - signer address
  - minimal next action

## Read Only When Needed

Read [SIWX + x402 Reference](references/siwx-x402.md) only when you need the exact signing or header details:

- `sign-in-with-x` payload format
- `X-PAYMENT` payload format
- EIP-4361 SIWX message template
- ERC-3009 EIP-712 domain and message fields
- response header meanings
- failure cases and common pitfalls
