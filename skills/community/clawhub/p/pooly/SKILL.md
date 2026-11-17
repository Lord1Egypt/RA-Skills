---
name: pooly
description: Read your Pooly group wallets — pools, USDC balances on Base, members, spending rules, agents, and spend history — through the official read-only Pooly MCP server. Can simulate a spend; never moves money.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🟢"
    homepage: https://www.pooly.org/developer
    requires:
      anyBins:
        - npx
        - node
---

# Pooly (read-only)

Pooly is a shared USDC wallet for groups. Each pool is a Safe on Base. Members spend from it under on-chain limits (for example, gift cards via Bitrefill).

This skill is **read-only**. You can look things up and simulate a spend. You cannot send, pay, approve, sign, invite, or change anything, and you must not try.

## Connect

Use the official remote MCP server. It signs the user in with OAuth on pooly.org; there is no API key to paste.

- MCP URL: `https://pooly-be.onrender.com/mcp` (Streamable HTTP)
- Scope: `pooly.read`

If your MCP client needs a config entry:

```json
{
  "mcpServers": {
    "pooly": { "url": "https://pooly-be.onrender.com/mcp" }
  }
}
```

The first tool call opens a Pooly sign-in page. The user enters their Pooly email and password there, never in chat.

## Tools

| Tool | Use it to |
| --- | --- |
| `list_pools` | List the user's pools with balance (USD) and Safe address. Start here to get a `pool_id`. |
| `get_pool` | Show one pool: balance, signatures required, spend-module limit, member count. |
| `list_members` | Show members, roles, shares, and per-member limits (no emails). |
| `get_spending_policy` | Check whether agents are enabled and the user's on-chain allowance. |
| `list_agents` | Show which AI/API agents have access and their limits. |
| `get_transactions` | Show recent spends and their status and tx hash. Gift card codes are never returned. |
| `simulate_spend` | Check whether a spend of `amount_usd` would fit the balance, fee, and allowance. Nothing is sent. |

## Rules

1. Never ask for or accept the user's password, recovery phrase, private key, or gift card codes in chat.
2. Never claim a spend happened. `simulate_spend` always returns `executed: false`.
3. When the user wants to actually spend or pay, tell them to do it themselves in the Pooly app (pooly.org) or with `npx pooly@latest spend`. They approve it with their own key. Do not run `pay`, `spend`, `approve`, `execute`, or `delegate` for them.
4. Amounts are USD-denominated USDC on Base. Show dollars, e.g. `$12.50`.
5. If a tool says the pool was not found, the user is not a member of it. Do not guess other ids.
6. If a tool says the sign-in expired, ask the user to reconnect Pooly in their MCP client.

## Examples

- "How much is in our Trip pool?" → `list_pools`, then `get_pool` for the match.
- "Can I buy a $25 gift card from Rent?" → `simulate_spend` with `amount_usd: 25`, then explain the blockers or say it looks fine and how to do it in the app.
- "Who spent from the pool this week?" → `get_transactions`.

## Read-only CLI (optional)

If MCP is unavailable, these CLI commands are read-only: `npx pooly@latest login`, `pools`, `balance <pool>`, `status`, `activity <pool>`, `rules <actor>`. The user signs in themselves.
