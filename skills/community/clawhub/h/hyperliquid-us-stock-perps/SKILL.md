---
name: hyperliquid-us-stock-perps
description: Use when the user asks about U.S. equity perpetuals on Hyperliquid: trend, trading volume, open interest, funding rates or related news. Calls the Maneki AI agent through Finch.
license: MIT
---

# Maneki AI on Finch

**What it does (official description):** Get a clearer view of the U.S. stock market on Hyperliquid. Maneki analyzes market trends, trading volume, open interest, funding rates, and relevant news for U.S. equity perpetuals. Ask questions in plain English to understand market movements, spot potential opportunities, and identify risks — with clear explanations behind every insight. Make more informed trading decisions with market data, not guesswork.

**Price:** 0.01 USDC per run. 10 free runs per account until 2026-11-21 (UTC).

## How to use

1. Ask the user for the ticker and the question in plain English.
2. If the Finch MCP server is connected (`https://www.finchtech.ai/mcp`), search the catalog for "Maneki AI" and create a task with the user's input. Only use free runs unless the user explicitly approves a paid run.
3. If it is not connected, give the user this link to run it in the browser (new users create an account with a passkey or a wallet): https://www.finchtech.ai/market/chips/agent-eee98da7-f7b3-471b-b0e4-fdd2a617e436/run?utm_source=skill&utm_medium=agent&utm_campaign=toa_skills&utm_content=hyperliquid-us-stock-perps
   To connect the MCP server instead, follow https://github.com/a0971025732-netizen/finch-agents/blob/main/CONNECT.md

## Rules

- Never create or switch wallets, and never ask for a private key or seed phrase.
- Market analysis only; not a guarantee of results.
