---
name: maverick-stripe-mcp
description: Search, read, and manage Stripe account data through Stripe's hosted MCP server. Thin pass-through to Stripe's official MCP; the live tool catalog is whatever that server advertises. Use when the user asks about Stripe payments, customers, products, prices, invoices, subscriptions, refunds, balances, or documentation.
homepage: https://docs.stripe.com/mcp
metadata:
  openclaw:
    emoji: "💳"
    requires:
      bins:
        - mcporter
      env:
        - MAVERICK_STRIPE_MCP_ACCESS_TOKEN
    primaryEnv: MAVERICK_STRIPE_MCP_ACCESS_TOKEN
    install:
      - id: node
        kind: node
        package: mcporter
        bins:
          - mcporter
        label: Install mcporter (node)
---

# Stripe

## How to use this skill

This skill is a thin pass-through to Stripe's hosted MCP server at `https://mcp.stripe.com`. The live server is the source of truth for what tools exist, what they're called, what arguments they take, and any per-server instructions the server publishes.

**Step 1 — Discover the live tool catalog and any server-published usage instructions.** Always run this first; do not rely on tool names from memory:

```sh
mcporter --config {baseDir}/mcporter.json list maverick-stripe-mcp --schema
```

The output includes the server's `Instructions:` field, if published, and a JSON Schema for every tool's parameters. Treat this as the authoritative reference for the rest of the session.

**Step 2 — Call any tool from the catalog** using the form `maverick-stripe-mcp.<tool>`:

```sh
mcporter --config {baseDir}/mcporter.json call maverick-stripe-mcp.<tool> <arg>=<value> ...
```

Add `--output json` for structured output and transport-error envelopes:

```sh
mcporter --config {baseDir}/mcporter.json call --output json maverick-stripe-mcp.<tool> ...
```

## Safety

Stripe tools can affect real customers, billing objects, subscriptions, refunds, account settings, and money movement. Confirm explicit user intent before any write-capable call, use restricted credentials where possible, and inspect current object state before changing it.

## Authentication

This skill expects `MAVERICK_STRIPE_MCP_ACCESS_TOKEN` to be set in the agent runtime environment. mcporter sends it as `Authorization: Bearer <value>` on every request.

If calls fail with auth errors, the token is invalid or revoked - re-issue and re-set `MAVERICK_STRIPE_MCP_ACCESS_TOKEN`. There is no automatic refresh; bearer tokens are static.

For agentic software, Stripe documents bearer authentication with a Stripe API key and recommends restricted API keys for least privilege. Store the credential in the runtime secret store or environment; do not embed it in code.

## References

- Stripe MCP overview and bearer authentication notes: <https://docs.stripe.com/mcp>
- Stripe restricted API keys: <https://docs.stripe.com/keys/restricted-api-keys>
- mcporter config reference: <https://github.com/openclaw/mcporter/blob/main/docs/config.md>
