---
name: passive-savings-crypto
description: Put idle USDC to work earning yield for you or your agent's wallet. Funds grow automatically and move like regular USDC when you're ready. No protocol interactions, no special steps.
metadata:
  openclaw:
    primaryEnv: AGENT_PRIVATE_KEY
    homepage: https://github.com/locker-labs/passive-savings-crypto
    emoji: 💰
    requires:
      bins: ["node"]
      env: ["AGENT_PRIVATE_KEY", "RPC_URL"]
    install:
      - npm install
    files:
      - scripts/getSYTBalance.js
      - scripts/mintSYT.js
      - scripts/transferSYT.js
---

# Passive Savings Crypto

Your wallet (or your agent's wallet) earns interest on idle USDC automatically. Fund it and forget it. Your balance grows in the background. When you're ready to move funds, it's just a normal ERC20 transfer. No protocol to interact with, no special steps for your agent.

**Great for agents and claws:** Give your agent a funded wallet and it will earn yield on any idle USDC, even if the project goes dormant. When you come back, the balance is larger and moves like regular USDC. No extra instructions needed.

## What You Can Ask

- "How much have I earned so far?"
- "Put 200 USDC to work earning yield."
- "Send 50 USDC to [address]."
- "What's my balance?"
- "Check my savings."
- "Start earning yield on this wallet's USDC."

## Script Reference

| Action | Command |
|---|---|
| Check balance + earnings | `node scripts/getSYTBalance.js` |
| Check balance for a specific address | `node scripts/getSYTBalance.js <address>` |
| Deposit USDC to earn yield | `node scripts/mintSYT.js <amount>` |
| Send USDC to someone | `node scripts/transferSYT.js <address> <amount>` |

## Examples

**Depositing**
- "Save 100 USDC" → `node scripts/mintSYT.js 100`
- "Put my idle USDC to work" → ask the user how much, then `node scripts/mintSYT.js <amount>`
- "Deposit 50 USDC" → `node scripts/mintSYT.js 50`

**Checking earnings**
- "What's my sUSDC balance?" → `node scripts/getSYTBalance.js`
- "How much yield have I earned?" → `node scripts/getSYTBalance.js`
- "Check the savings balance for 0xABC..." → `node scripts/getSYTBalance.js 0xABC...`

**Sending payments**
- "Pay 20 USDC to 0x7c33..." → `node scripts/transferSYT.js 0x7c33... 20`
- "Send 75 USDC to my friend at 0xDEF..." → `node scripts/transferSYT.js 0xDEF... 75`
- "Transfer 10 USDC to [address]" → `node scripts/transferSYT.js <address> 10`

## Setup

1. Set `AGENT_PRIVATE_KEY` to your wallet's private key (never share this)
2. Set `RPC_URL` to a Linea RPC endpoint (e.g. from Infura or Alchemy)
3. Run `npm install` to install dependencies

This skill operates on **Linea mainnet**. Ensure your wallet has USDC on Linea before depositing.

## How It Works

When you deposit USDC, it goes into Aave via the router and comes back as sUSDC, a token that grows in value over time as interest accrues. When you send a payment, the recipient receives plain USDC. The conversion happens automatically.

**For agent and claw developers:** sUSDC is a standard ERC20 token. Your agent doesn't need any special logic to move it. A normal transfer is all it takes. Fund your agent's wallet, let it earn, and retrieve funds whenever you're ready. No protocol interactions, no extra instructions required. Idle agent funds no longer sit dead.

## Security & Privacy

- **No data leaves the device** except signed transactions broadcast to the Linea RPC endpoint.
- **Private key handling:** `AGENT_PRIVATE_KEY` is read from environment variables only, never logged, stored, or transmitted.
- **On-chain only:** All state changes are EVM transactions. No backend, no database, no telemetry.

| Endpoint | Purpose |
|---|---|
| `RPC_URL` (Linea RPC) | Broadcast transactions, read contract state |
| `https://linea.drpc.org` | Default fallback RPC if `RPC_URL` is not set |

## Agent Guardrails

- **Always use `transferSYT.js` for payments.** Never transfer raw USDC directly. This ensures the recipient gets spendable USDC, not a yield token.
- **Report both figures when showing balance.** The nominal sUSDC amount and the underlying USDC value it represents (these diverge as yield accrues).
- **Confirm before depositing or transferring.** These are on-chain transactions and cannot be reversed.
- **Network is Linea mainnet.** Transactions on other chains will not work with this skill.

## Integration

### Claude Code

Run once after cloning to register this skill in your Claude Code session:

```bash
npm run install-skill
```

This copies `SKILL.md` to `~/.claude/skills/passive-savings-crypto/SKILL.md`. After that, Claude Code can invoke it automatically when you ask about balances, deposits, or transfers.

### OpenAI / Custom Agents

Load `tools.json` from this repo as your tool definitions. Each tool maps to a CLI command the agent runs via shell:

| Tool | Command |
|---|---|
| `get_syt_balance` | `node scripts/getSYTBalance.js [address]` |
| `mint_syt` | `node scripts/mintSYT.js <amount>` |
| `transfer_syt` | `node scripts/transferSYT.js <recipient> <amount>` |

Set `AGENT_PRIVATE_KEY` and `RPC_URL` in your agent's environment before invoking any tool.
