---
name: architecture
description: HyperCore vs HyperEVM — what lives where, how they interact, the complete system model. Essential reading before building anything on Hyperliquid. Use when planning architecture, understanding state, or deciding where logic belongs.
---

# Hyperliquid Architecture

## What You Probably Got Wrong

**"Hyperliquid is an EVM chain."** HyperEVM is ONE component of Hyperliquid. The other component — HyperCore — is a custom exchange engine that runs alongside the EVM. They share finality but are distinct execution environments.

**"Everything is a contract."** HyperCore has no contracts. Its logic (orderbook matching, liquidations, funding rate calculation) is built into the L1 protocol. You can't deploy to HyperCore — you integrate with it via API.

**"The EVM and exchange are on separate chains."** They share the same validator set and consensus round. An EVM transaction and a HyperCore order placed in the same block are final at the same time. This atomic finality is what makes Hyperliquid unique.

---

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    HyperBFT Consensus                       │
│  (All validators agree on HyperCore + HyperEVM state)       │
│                                                             │
│  ┌──────────────────────┐   ┌──────────────────────────┐   │
│  │      HyperCore       │   │         HyperEVM         │   │
│  │                      │   │                          │   │
│  │  • Perp orderbook    │   │  • EVM contracts         │   │
│  │  • Spot orderbook    │◄──┤  • ERC-20 tokens         │   │
│  │  • Positions         │   │  • DeFi protocols        │   │
│  │  • Funding rates     │   │  • Chain ID 999          │   │
│  │  • HLP vault         │   │  • HYPE gas token        │   │
│  │  • HIP-1/2/3 tokens  │   │                          │   │
│  │  • Cross-margin      │   │                          │   │
│  └──────────────────────┘   └──────────────────────────┘   │
│                                                             │
│  Access:                     Access:                        │
│  POST /info                  Standard EVM RPC               │
│  POST /exchange              https://rpc.hyperliquid.xyz/   │
│  WSS /ws                     evm                            │
└─────────────────────────────────────────────────────────────┘
```

---

## HyperCore

HyperCore is the native exchange engine. It is NOT EVM — it's a purpose-built exchange running at L1 consensus speed.

### What Lives in HyperCore

**Perpetual Futures:**
- All open perp positions (long/short, size, entry price, margin)
- Funding rates and payments (every 8 hours, can be instantaneous)
- Cross-margin pool (USDC collateral shared across all perp positions)
- Isolated margin positions
- Liquidation engine

**Spot Orderbook:**
- HIP-1 native spot tokens
- Full CLOB (central limit orderbook) for each spot pair
- HIP-2 hyperliquidity — protocol-level AMM for spot tokens

**Vaults:**
- HLP (Hyperliquid Liquidity Provider) — the main protocol vault
- User-created vaults
- Vault deposits and withdrawals

**Token Standards:**
- HIP-1: native spot token definition
- HIP-2: automated hyperliquidity seeding
- HIP-3: permissioned spot DEX (builder-controlled listing)

**User Accounts:**
- Balances (USDC, HYPE, HIP-1 tokens)
- Positions
- Open orders

### How to Read HyperCore State

All via `POST /info` to `https://api.hyperliquid.xyz/info`:

```json
// Get perp market metadata
{ "type": "meta" }

// Get spot market metadata
{ "type": "spotMeta" }

// Get user state (all positions, balances)
{ "type": "clearinghouseState", "user": "0x..." }

// Get open orders
{ "type": "openOrders", "user": "0x..." }

// Get orderbook
{ "type": "l2Book", "coin": "ETH" }

// Get all perp markets ticker data
{ "type": "allMids" }
```

### How to Write to HyperCore

All via `POST /exchange` to `https://api.hyperliquid.xyz/exchange`:

```json
{
  "action": { "type": "order", ... },
  "nonce": 1234567890123,
  "signature": { "r": "0x...", "s": "0x...", "v": 27 }
}
```

Every write requires an EIP-712 signature. No unsigned writes.

---

## HyperEVM

HyperEVM is a standard EVM environment running alongside HyperCore.

### What Lives in HyperEVM

- Smart contracts (Solidity, Vyper)
- ERC-20 tokens, ERC-721 NFTs
- HyperSwap V2 (deployed AMM DEX)
- Any contract you deploy
- HYPE as native currency (Chain ID 999)

### Key Differences from Ethereum Mainnet

| Feature | Ethereum Mainnet | HyperEVM |
|---------|-----------------|----------|
| Chain ID | 1 | 999 (mainnet) / 998 (testnet) |
| Native currency | ETH | HYPE |
| Block time | ~12s | ~1-2s |
| Priority fees | → validators | Burned |
| Blob transactions | Yes (Cancun) | No (Cancun opcodes, no blobs) |
| MEV | Significant | Minimal |
| Testnet | Sepolia (11155111) | 998 |

### Connecting to HyperEVM

```typescript
// viem
import { defineChain } from 'viem';

export const hyperliquid = defineChain({
  id: 999,
  name: 'HyperEVM',
  nativeCurrency: { name: 'HYPE', symbol: 'HYPE', decimals: 18 },
  rpcUrls: {
    default: { http: ['https://rpc.hyperliquid.xyz/evm'] },
  },
  blockExplorers: {
    default: { name: 'HyperEVM Explorer', url: 'https://explorer.hyperliquid.xyz' },
  },
});

export const hyperliquidTestnet = defineChain({
  id: 998,
  name: 'HyperEVM Testnet',
  nativeCurrency: { name: 'HYPE', symbol: 'HYPE', decimals: 18 },
  rpcUrls: {
    default: { http: ['https://rpc.hyperliquid-testnet.xyz/evm'] },
  },
  blockExplorers: {
    default: { name: 'HyperEVM Testnet Explorer', url: 'https://explorer-testnet.hyperliquid.xyz' },
  },
});
```

---

## The Bridge: 0x2222...2222

The system address `0x2222222222222222222222222222222222222222` is the HyperCore ↔ HyperEVM bridge.

**Moving HYPE from HyperCore to HyperEVM:**
- Method 1: On HyperEVM, send a transaction to `0x2222...2222` with HYPE value. This is counterintuitive — you're sending FROM HyperEVM TO the bridge address, and HYPE appears on HyperEVM.
- Wait, actually: sending HYPE to `0x2222...2222` on HyperEVM **withdraws** it TO HyperCore.

Let me clarify the bridge mechanics:

**HyperEVM → HyperCore (withdraw from EVM):**
- Send HYPE to `0x2222222222222222222222222222222222222222` on HyperEVM
- HYPE appears in your HyperCore spot balance

**HyperCore → HyperEVM (deposit to EVM):**
- Use the `/exchange` API with action type `"spotSend"` or use the `"evmUserModify"` action
- HYPE appears as HYPE token on HyperEVM

**In practice:**
- The Hyperliquid app UI handles bridging for users
- For programmatic bridging, use the SDK
- HYPE decimals: 18 on HyperEVM, float representation in HyperCore API

---

## HyperCore State Reading from HyperEVM

HyperEVM contracts can read HyperCore state via a system precompile at address `0x0000000000000000000000000000000000000800` (verify current address in official docs — may change).

This enables HyperEVM contracts to:
- Read open positions
- Read orderbook state
- Trigger HyperCore actions based on onchain conditions

This is advanced functionality — most builders use the REST API instead of the precompile.

---

## State Sync and Finality

Both HyperCore and HyperEVM reach finality in the same HyperBFT round. This means:

- A HyperCore order and a HyperEVM transaction in the same block are BOTH final at the same time
- There's no "cross-chain" risk between HyperCore and HyperEVM — they share consensus
- Bridge operations (via 0x2222...2222) have the same finality guarantee

**No waiting for "safe" confirmations.** 1 block = final. Plan your UX accordingly.

---

## Decision Framework: Where Does Logic Go?

```
Does it involve trading, positions, or native token markets?
├─ YES → HyperCore API (/exchange)
│        Use SDK, EIP-712 signing
│
└─ NO  → Does it need custom contract logic?
         ├─ YES → HyperEVM (Solidity contract)
         │         Chain ID 999, HYPE gas
         │
         └─ NO  → Is it a read query?
                   ├─ HyperCore state → POST /info
                   └─ EVM state → standard eth_call via RPC
```

---

## Asset IDs

Understanding asset IDs is critical for HyperCore API calls:

- **Perp asset IDs:** 0-indexed position in `meta.universe` array (e.g., ETH-perp might be asset 1)
- **Spot asset IDs:** 10000 + spot index (e.g., if PURR is spot index 0, its asset ID is 10000)
- **HIP-3 builder assets:** 100000 + (perp_dex_index * 10000) + index

Always fetch current asset IDs via `POST /info` with `{ "type": "meta" }` — never hardcode them.

```python
# Get current asset IDs
import requests

meta = requests.post('https://api.hyperliquid.xyz/info',
                     json={'type': 'meta'}).json()

# Perp assets
for i, asset in enumerate(meta['universe']):
    print(f"Perp {i}: {asset['name']}")

# Spot assets
spot_meta = requests.post('https://api.hyperliquid.xyz/info',
                           json={'type': 'spotMeta'}).json()
for i, token in enumerate(spot_meta['tokens']):
    print(f"Spot {i} (ID: {10000+i}): {token['name']}")
```
