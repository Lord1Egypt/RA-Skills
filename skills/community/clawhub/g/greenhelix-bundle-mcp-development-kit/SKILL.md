---
name: greenhelix-bundle-mcp-development-kit
version: "1.3.1"
description: "Everything you need to build and publish MCP servers. Includes the MCP Server Development guide, agent commerce discovery patterns, and protocol interoperability bridge. Plus server.json and smithery.yaml templates for registry submission. 3 guides + code templates."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: bundle
includes: [mcp-server-development, agent-commerce-discovery, agent-interoperability-bridge]
price_usd: 79.0
tags: [bundle, code, mcp, server-development, starter-kit, guide, greenhelix, openclaw, ai-agent]
executable: false
install: none
credentials: [STRIPE_API_KEY, GREENHELIX_API_KEY, AGENT_SIGNING_KEY, WALLET_ADDRESS]
metadata:
  openclaw:
    requires:
      env:
        - STRIPE_API_KEY
        - GREENHELIX_API_KEY
        - AGENT_SIGNING_KEY
        - WALLET_ADDRESS
    primaryEnv: STRIPE_API_KEY
---
# MCP Development Kit: Guide + Server Templates + Registry Configs

## Included Guides
| Guide | Individual Price |
|-------|-----------------|
| MCP Server Development & Monetization Guide: Build, Publish, and Profit from the Tool Integration Standard | $49.00 |
| Agent Commerce Discovery | $0.00 |
| The Agent Interoperability Bridge: Connecting GreenHelix Agents to x402, ACP, A2A, MCP, Visa TAP, Google AP2/UCP, PayPal Agent Ready, and OpenAI ACP Ecosystems | $0.00 |

## Total Value: $49.00 | Bundle Price: $79.00
