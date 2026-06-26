# Passive Savings Crypto

[![Built for Claude](https://img.shields.io/badge/Built%20for-Claude-8A2BE2?logo=anthropic&logoColor=white)](https://claude.ai)
[![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-Compatible-00C2FF)](https://openclaw.ai)
[![ClawBot Ready](https://img.shields.io/badge/ClawBot-Ready-00C2FF)](https://openclaw.ai)
[![Powered by Aave](https://img.shields.io/badge/Powered%20by-Aave-B6509E?logo=aave&logoColor=white)](https://aave.com)
[![Linea](https://img.shields.io/badge/Network-Linea-121212?logo=linea&logoColor=white)](https://linea.build)
[![Base](https://img.shields.io/badge/Network-Base-0052FF?logo=base&logoColor=white)](https://base.org)

> Turn idle USDC into yield — automatically. For AI agents and crypto wallets alike.

**For agent developers:** This is a Claude skill and OpenClaw/ClawBot-compatible tool that gives your autonomous agent a yield-bearing wallet. Idle USDC earns Aave yield automatically in the background — no extra agent instructions needed. When your agent is ready to spend or transfer, funds move like regular USDC. Perfect for AI agent DeFi workflows where capital shouldn't sit dead between tasks.

**For crypto users:** Passive income on USDC with zero manual claiming. Deposit once, watch your balance grow on Base and Linea via Aave yield. DeFi savings that work like a bank account — but onchain.

---

A Claude skill for AI agents to manage sUSDC (Spendable Yield Tokens) on the Linea blockchain — converting idle USDC into yield-bearing tokens so users save while they spend.

## Install as a Claude Code Skill

The fastest way — install directly from ClawHub:

```bash
npx clawhub@latest install passive-savings-crypto
```

Restart Claude Code and the skill loads automatically. Ask Claude things like "check my sUSDC balance" or "deposit 100 USDC" — it will know what to do.

**To install from source instead:**

```bash
git clone https://github.com/locker-labs/passive-savings-crypto
cd passive-savings-crypto
npm install
npm run install-skill
```

`npm run install-skill` copies `SKILL.md` to `~/.claude/skills/passive-savings-crypto/SKILL.md` — the directory Claude Code scans for user-installed skills. You only need to run it once, or again after pulling updates.

---

## Overview

sUSDC is a rebasing token backed 1:1 by USDC. Holding sUSDC earns yield automatically; the balance grows over time without any manual claiming. This skill provides three operations:

- **Mint** — deposit USDC and receive sUSDC
- **Balance** — check sUSDC balance (and its underlying USDC value)
- **Transfer** — send sUSDC to another address (underlying USDC moves with it)

## Prerequisites

- Node.js v18+
- A wallet funded with USDC on Linea mainnet
- A Linea RPC endpoint (e.g. `https://rpc.linea.build`)

## Installation

```bash
npm install
```

## Configuration

Set the following environment variables before running any script:

| Variable | Description |
|---|---|
| `AGENT_PRIVATE_KEY` | Hex private key of the wallet executing transactions |
| `RPC_URL` | Linea RPC endpoint |

```bash
export AGENT_PRIVATE_KEY=0x...
export RPC_URL=https://rpc.linea.build
```

## Usage

### Mint sUSDC

Deposit USDC and receive sUSDC. On first use, this approves the Locker Router for unlimited USDC spending (one-time transaction).

```bash
node scripts/mintSYT.js <amount>

# Example: deposit 10.5 USDC
node scripts/mintSYT.js 10.5
```

### Check Balance

Query the sUSDC balance of an address. Defaults to the agent's own wallet if no address is provided.

```bash
node scripts/getSYTBalance.js [address]

# Check agent's own balance
node scripts/getSYTBalance.js

# Check another address
node scripts/getSYTBalance.js 0x7c334f35BF2B4a9e55f60CF3287c885598cF9A02
```

### Transfer sUSDC

Send sUSDC to a recipient. The script verifies sufficient balance before executing.

```bash
node scripts/transferSYT.js <recipient> <amount>

# Example: send 20 sUSDC
node scripts/transferSYT.js 0x7c334f35BF2B4a9e55f60CF3287c885598cF9A02 20
```

## Contract Addresses (Linea Mainnet)

| Contract | Address |
|---|---|
| USDC | `0x176211869cA2b568f2A7D4EE941E073a821EE1ff` |
| sUSDC (SYT) | `0x060c1cBE54a34deCE77f27ca9955427c0e295Fd4` |
| Locker Router | `0xa289AE6ed8336CaB82626c3ff8e5Af334Eb7E0DE` |

## Notes

**Rebase awareness** — sUSDC is a rebasing token. The raw balance returned by the contract increases over time as yield accrues. Always use `getSYTBalance.js` for the current balance rather than caching a previous value.

**Infinite approval** — `mintSYT.js` requests unlimited USDC approval on first use to avoid repeated approval transactions. This is a common pattern for DeFi protocols.

## Publishing to ClawHub

Install the ClawHub CLI and authenticate once:

```bash
npm install -g clawhub
clawhub login
```

Bump the version in `package.json`, then publish:

```bash
npm run release       # publish to ClawHub
npm run release:dry   # preview without uploading
```
