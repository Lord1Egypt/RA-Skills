---
name: why-hyperliquid
description: Why build on Hyperliquid. HyperBFT consensus, native orderbook, speed, AI agent angle, honest tradeoffs. Use when someone asks "should I build on Hyperliquid?", "why not Ethereum?", or when an agent needs to understand what makes Hyperliquid unique.
---

# Why Hyperliquid

## What You Probably Got Wrong

**"Hyperliquid is just a fast Ethereum L2."** No. Hyperliquid is a purpose-built L1 with HyperBFT consensus and a native orderbook. HyperEVM is ONE component — it's an EVM environment that runs alongside HyperCore (the native exchange engine). They share finality. They are NOT the same thing.

**"MEV sandwich attacks happen here too."** They don't. HyperCore processes orders through HyperBFT consensus — there's no public mempool, no reordering by validators. Orders arrive, match, settle. No frontrunning. No sandwich. This is structurally different from any EVM chain.

**"The native token is ETH."** It's HYPE. HYPE is the gas token on HyperEVM, the staking token for HyperBFT validators, and the governance token. ETH has no role on Hyperliquid.

**"I'll just use standard Ethereum tooling."** HyperEVM works with standard EVM tools (wagmi, viem, Foundry). But HyperCore does NOT. HyperCore has its own API (`/info`, `/exchange`), its own token standards (HIP-1, HIP-2, HIP-3), and its own signing scheme (EIP-712 typed data over the exchange).

---

## The Architecture in One Sentence

Hyperliquid is a purpose-built L1 where HyperCore (native orderbook, perps, spot) and HyperEVM (Solidity contracts) share atomic finality via HyperBFT consensus.

---

## HyperBFT Consensus

HyperBFT is a BFT (Byzantine Fault Tolerant) consensus algorithm optimized for throughput and finality. Key properties:

- **Sub-second finality:** Transactions are final in ~1 block, not probabilistically safe after 6+ blocks like PoW chains
- **No public mempool:** Orders and transactions don't sit in a visible pool where bots can frontrun them
- **~100,000 orders/sec throughput:** Native orderbook capacity that no EVM chain can match
- **Validator set:** Permissioned set of validators staking HYPE; slashing for equivocation
- **Not PoW, not standard PoS:** HyperBFT is a custom algorithm, not Ethereum's Gasper or Tendermint

**What this means for builders:**
- Finality is fast and hard. No need to wait multiple block confirmations.
- MEV extraction (sandwich attacks, frontrunning) is structurally prevented on HyperCore.
- Order execution is deterministic and fair. First-come, first-served at the protocol level.

---

## HyperCore — The Native Exchange

HyperCore is the core of Hyperliquid. It's not an EVM contract. It's built into the L1 itself.

**What lives in HyperCore:**
- Perpetual futures: all perp positions, funding rates, liquidations, cross-margin
- Spot orderbook: native spot trading for HIP-1 tokens
- Vault system: protocol-native vaults (like HLP — the Hyperliquid Liquidity Provider vault)
- HIP-1/HIP-2 token standards: native token issuance and automated market-making
- Clearing: margining, settlement, liquidations

**You interact with HyperCore via:**
- `POST /info` — read-only queries (no auth)
- `POST /exchange` — signed actions (orders, cancels, transfers)
- WebSocket at `wss://api.hyperliquid.xyz/ws` — real-time streams

HyperCore is what makes Hyperliquid unique. No other chain has a native perp DEX running at L1 consensus speed with no MEV.

---

## HyperEVM — The EVM Layer

HyperEVM is a standard EVM environment running alongside HyperCore. It:

- Supports all standard EVM tooling (Foundry, Hardhat, wagmi, viem, ethers.js)
- Has Chain ID 999 (mainnet), 998 (testnet)
- Uses HYPE as the native gas token (not ETH)
- Supports Cancun-era opcodes (no blobs — Hyperliquid doesn't need data availability blobs)
- Burns priority fees (not paid to validators)
- Block time: ~1-2 seconds
- Has a system precompile at `0x2222222222222222222222222222222222222222` — send HYPE here to bridge from HyperCore to HyperEVM

**HyperEVM and HyperCore share finality.** A HyperEVM transaction and a HyperCore order that execute in the same block are final together — no cross-chain bridge risk between them.

---

## Why Build on Hyperliquid

### For Trading/DeFi Applications

- **Native orderbook:** No DEX approximation. Real limit orders, real price discovery, native CLOB.
- **No MEV:** Your users' trades execute at the price they expect. No sandwich attacks.
- **Speed:** Sub-second order acknowledgment. HyperCore doesn't have 12-second block times.
- **Capital efficiency:** Cross-margin across perps. Unified collateral. No fragmented liquidity across pools.

### For AI Agents

- **Programmatic trading:** The `/exchange` API is designed for algorithmic trading. Order placement is deterministic.
- **No gas surprises:** HyperCore order placement doesn't require gas — only EVM transactions do. Agents can place thousands of orders cheaply.
- **Real-time data:** WebSocket subscriptions give sub-second price, order, and fill data.
- **Agent wallet pattern:** Main wallet approves an agent subaccount key with spending limits. Agents never touch the main key.

### For Token Launches

- **HIP-1 tokens:** Native spot tokens with built-in orderbook integration
- **HIP-2 hyperliquidity:** Protocol-level automated market-making — no need to bootstrap a Uniswap pool
- **Bonding curve:** x*y=k until graduation threshold, then full orderbook listing — predictable launch mechanics

---

## Honest Tradeoffs

| What Hyperliquid Does Well | What It Doesn't |
|---------------------------|-----------------|
| High-speed, high-volume trading | Ecosystem as deep as Ethereum/Arbitrum |
| Native orderbook with no MEV | Not EVM-only — HyperCore has its own API surface |
| Built-in token launch rails | Developer tooling still maturing vs Ethereum |
| Sub-second finality | Less composability surface (smaller protocol ecosystem) |
| Low gas costs on HyperEVM | HyperCore API learning curve |
| AI-agent-friendly trading API | Smaller DeFi liquidity than Arbitrum |

**When NOT to choose Hyperliquid:**
- You need deep DeFi liquidity composability (Aave, Curve, Balancer) → Arbitrum
- You need the largest EVM developer ecosystem → Ethereum mainnet
- You're building a simple token with no trading ambitions → Base or Ethereum
- You need ZK proofs or privacy → zkSync or Scroll

**When TO choose Hyperliquid:**
- Trading application, perp protocol, or high-frequency anything
- Token launch with built-in market-making
- AI agent that needs programmatic market access
- Any application where MEV-free execution matters

---

## Current Network Stats (Early 2026)

- **HyperCore throughput:** ~100,000 orders/sec (measured)
- **HyperEVM block time:** ~1-2 seconds
- **Finality:** Sub-second (HyperBFT)
- **HyperEVM Chain ID:** 999 (mainnet), 998 (testnet)
- **Native gas token:** HYPE
- **HYPE price:** Volatile — verify on CoinGecko or Hyperliquid's own UI

---

## Resources

- **Official docs:** https://hyperliquid.gitbook.io/hyperliquid-docs/
- **Python SDK:** https://github.com/hyperliquid-dex/hyperliquid-python-sdk
- **TypeScript SDK:** https://github.com/nktkas/hyperliquid
- **HyperEVM Explorer:** https://explorer.hyperliquid.xyz
- **API endpoints:**
  - Mainnet: https://api.hyperliquid.xyz
  - Testnet: https://api.hyperliquid-testnet.xyz
