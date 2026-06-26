# Ovra Agent Payments

EU-native payment skill for AI agents. Zero-knowledge checkout — the agent never sees card data.

**Published by [Ovra Labs](https://getovra.com)** | [GitHub](https://github.com/Ovra-Labs/ovra-pay)

## Install

```bash
npx skills add Ovra-Labs/ovra-pay
```

Or manually copy `SKILL.md` into your skills directory.

## Required: Ovra API Key

This skill requires an `OVRA_API_KEY` to authenticate with the Ovra MCP server.

1. Sign up at [getovra.com](https://getovra.com)
2. Get your key from [Dashboard > Keys](https://getovra.com/dashboard/keys)
3. Sandbox keys (`sk_test_*`) are free for testing

## Setup

Connect to Ovra's MCP server at `https://api.getovra.com/api/mcp`:

```json
{
  "mcpServers": {
    "ovra": {
      "url": "https://api.getovra.com/api/mcp",
      "headers": { "Authorization": "Bearer sk_test_YOUR_KEY" }
    }
  }
}
```

## What this enables

Say "buy X" to your AI agent and it handles the entire checkout securely:

1. Declares intent (what to buy, how much, which merchant)
2. Policy engine checks spending rules
3. Issues tokenized credentials (DPAN + cryptogram via Visa Network Tokens)
4. Attaches receipt for audit trail
5. Verifies transaction matches intent

The agent never sees real card numbers (PAN/CVV). All data sent to `api.getovra.com` only.

Works with Claude Code, Cursor, Windsurf, Codex, and any MCP-compatible agent.

## Why Ovra?

Every other agent payment solution gives the agent your card number. Ovra doesn't. The agent gets `{ success: true }` and nothing else. Card data is resolved through Visa's tokenization network — even Ovra doesn't store raw PANs.

EU-native. GDPR by design. Powered by Visa Network Tokens. Built in Berlin.

## Links

- [Website](https://getovra.com)
- [Documentation](https://docs.getovra.com)
- [MCP Endpoint](https://api.getovra.com/api/mcp)
- [Dashboard](https://getovra.com/dashboard)
- [skills.sh listing](https://skills.sh/Ovra-Labs/ovra-pay)
