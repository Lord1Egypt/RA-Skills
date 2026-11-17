---
name: mass-intelligence
description: Retrieve dated market research through Mass REST or MCP integrations with explicit x402 payment controls.
---

# Mass Intelligence skill

Use this skill when a user asks for curated market signals, macro context, capital activity, narrative changes, or observed airdrop research from an authorized Mass integration.

## Rules

- Start with the catalog or tool description so the user can understand the resource, price, timestamp, and limitations.
- Treat every paid request as requiring explicit authorization. Ask for a maximum spend and never infer recurring or unlimited permission.
- On a `402 Payment Required` response, verify the exact network, asset, amount, recipient, resource, and expiry before a local signer retries.
- Never expose or request private keys, recovery phrases, API keys, payment proofs, or private report URLs in chat, logs, tool arguments, or repository files.
- Keep wallet signing client-side. MCP tools return research; they do not receive signing secrets.
- State the observed timestamp and research caveats. Do not frame output as execution instructions or a guarantee.
- For private, user-specific reports, use the authorized API authentication channel; never pass an API key as an MCP tool argument.

## Suggested workflow

1. Discover the relevant capability in the catalog or MCP tool list.
2. Summarize the expected cost and ask the user to approve a bounded amount.
3. Execute only after policy validation and approval.
4. Return the dated research, evidence, counter-evidence, and uncertainty.
5. Record only non-sensitive local audit data such as the approved cap and outcome.
