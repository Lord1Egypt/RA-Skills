---
name: goodwallet
description: >
  Crypto wallet for sending, swapping, trading perps, betting on Polymarket,
  earning DeFi yield, and signing across EVM, Solana, Bitcoin, Doge, and XRP.
  Use when the user asks about wallets, balances, sending tokens, swaps,
  trades, bets, vaults, or signing.
metadata:
  {
    "openclaw":
      {
        "emoji": "👛",
        "homepage": "https://goodwallet.dev",
        "source": "https://github.com/GoodDollar/mpc-wallet-api",
        "npm": "https://www.npmjs.com/package/goodwallet",
        "publisher": "GoodDollar",
        "requires":
          {
            "bins": ["node"],
          },
        "install": [
          {
            "id": "node",
            "kind": "node",
            "package": "goodwallet",
            "bins": ["goodwallet"],
            "label": "Install Goodwallet CLI (npm)"
          }
        ],
        "auth":
          {
            "method": "browser-oauth",
            "description": "Interactive browser login via `goodwallet auth`; no API key required"
          },
        "data":
          {
            "config_path": "~/.config/goodwallet/",
            "contents": "Wallet configuration, encrypted MPC key shares (ECDSA + Ed25519), and auth tokens. No full private key is ever stored — only a single MPC share."
          },
        "external_services":
          [
            {
              "domain": "sign.goodwallet.dev",
              "purpose": "MPC co-signer relay — holds the second key share and performs 2-party signing. Operated by GoodDollar.",
              "protocol": "HTTPS/WSS"
            },
            {
              "domain": "agent.goodwallet.dev",
              "purpose": "Agent API — issues signing room UUIDs and enforces transaction policy. Operated by GoodDollar.",
              "protocol": "HTTPS"
            }
          ]
      }
  }
---

# Goodwallet

Crypto wallet CLI. Run `goodwallet --help` for the latest commands, flags, chains, and usage.

## Setup

This skill assumes the `goodwallet` CLI is installed globally and available in PATH. If not, install it via npm:
Do NOT use `npx`. Always use the globally installed binary.

## Update

Before running any other command, check for updates:

1. `goodwallet update` — check for a new version.
2. If outdated, run `goodwallet update --install` before proceeding.

## Rules

- Summarize outcomes in plain language; don't dump raw CLI output unless asked.
- Never fabricate values. Only report what the CLI returns.
- **Read before write**: inspect balances/quotes/positions before proposing any state-changing action.
- **Confirm before executing** any command that moves funds or creates exposure: `send`, `swap --execute`, `trade --deposit/--withdraw/--market`, `bet --deposit/--withdraw/--market`, `earn --deposit/--withdraw`, and every `sign` command.
- Don't reveal internal wallet details unless the user asks.

## Auth

1. `goodwallet auth` — show the returned URL to the user.
2. `goodwallet auth --pair` — run immediately; polls until the browser flow completes.
3. `goodwallet auth --logout` — disconnect.

## Signing Safety

All credentials and MPC key shares are stored locally at `~/.config/goodwallet/`. No full private key ever exists — only a single MPC key share is stored on device. Signing uses 2-party MPC with a remote co-signer at `sign.goodwallet.dev` (operated by [GoodDollar](https://github.com/GoodDollar)). The agent API at `agent.goodwallet.dev` issues signing room UUIDs and enforces transaction-policy checks (token allowlists, spend limits, malicious-contract detection) before co-signing, so most harmful payloads are rejected server-side. Both services communicate over HTTPS/WSS. Still, confirm with the user before running any `sign` command so they understand what they're approving.

## Error Recovery

- Auth timeout → restart `auth` + `auth --pair`.
- Insufficient funds → suggest checking balances or reducing amount.
- No swap route → suggest different token, amount, or chain.
- Any other failure → report the error plainly, don't retry automatically.
