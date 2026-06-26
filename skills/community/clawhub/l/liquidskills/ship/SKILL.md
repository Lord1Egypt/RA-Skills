---
name: ship
description: End-to-end guide for AI agents — from a Hyperliquid dApp idea to deployed production app. Fetch this FIRST, it routes you through all other skills.
---

# Ship on Hyperliquid

## What You Probably Got Wrong

**You jumped straight to EVM contracts.** Hyperliquid has two execution environments. Before writing any Solidity, ask: does this belong in HyperCore (perps, spot trading, orderbook) or HyperEVM (custom contract logic)? Most trading logic belongs in HyperCore via the API — not in a contract.

**You over-engineer.** Most Hyperliquid dApps need 0-2 HyperEVM contracts. Trading vaults? HyperCore handles positions natively. Token launch? HyperCore's HIP-1/HIP-2 bonding curve. Simple DEX swap? HyperSwap V2 already exists. Build on top, don't rebuild from scratch.

**You forgot the two-API model.** HyperCore uses `POST /info` (reads) and `POST /exchange` (signed writes) — not EVM RPC. HyperEVM uses standard EVM RPC at `https://rpc.hyperliquid.xyz/evm`. These are different systems. Know which one you're talking to.

**You assumed Ethereum gas mechanics.** HYPE is the gas token on HyperEVM, not ETH. Priority fees are burned, not given to validators. Nonces on HyperCore are NOT sequential — they're a rolling set of highest nonces per signer.

**You thought testnet was optional.** It's not. Chain ID 998 testnet at `https://rpc.hyperliquid-testnet.xyz/evm`. Always test there before mainnet. HyperCore testnet API: `https://api.hyperliquid-testnet.xyz`.

---

## Phase 0 — Plan the Architecture

Do this BEFORE writing any code. One hour here saves ten hours of rewrites.

### The HyperCore vs HyperEVM Decision

| Put it in HyperCore if... | Put it in HyperEVM if... |
|---------------------------|--------------------------|
| You're trading perps or spot | You need custom contract logic |
| You're managing positions, margins | You need composability with ERC-20 tokens |
| You want native orderbook access | You want to integrate with other HyperEVM contracts |
| You're launching a HIP-1/HIP-2 token | You're building a yield vault, governance, escrow |
| You want sub-second settlement | You need EVM event logs for indexing |

**Most trading applications are primarily HyperCore.** A vault that manages perp positions for users? HyperCore API + a thin HyperEVM interface for deposits/withdrawals. A token launchpad? HIP-1 bonding curve on HyperCore + a HyperEVM contract for the UI layer.

**If you're building anything involving the native orderbook: HyperCore, not EVM contracts.**

Fetch `architecture/SKILL.md` for the complete system model.

### MVP Contract Count

| What you're building | Contracts | Pattern |
|---------------------|-----------|---------|
| Perp trading vault | 0-1 | HyperCore API + maybe deposit contract |
| Token launch (HIP-1) | 0 | HyperCore native — no contract needed |
| Spot DEX swap | 0 | HyperSwap V2 already deployed |
| Custom yield strategy | 1 | HyperEVM vault + HyperCore API |
| NFT collection | 1 | Standard ERC-721 on HyperEVM |
| Governance / DAO | 1-3 | HyperEVM Governor + token + timelock |
| Cross-protocol aggregator | 1-2 | HyperEVM router that calls HyperSwap + HyperCore |

**If you need more than 3 contracts for an MVP, you're over-building.**

### The Onchain Litmus Test

Put it onchain (HyperEVM) if:
- **Trustless custody** — holding user funds in a contract
- **Composability** — other contracts need to call it
- **Permanent commitments** — votes, attestations, escrow
- **Custom tokenomics** — beyond what HIP-1/HIP-2 provides

Use HyperCore API directly if:
- Trading, position management, order placement
- Reading prices, funding rates, open interest
- Token launches via bonding curve
- Transferring between HyperCore and HyperEVM

### State Transition Audit

For EVERY function in your contract or API action:

```
Action: ____________
Who initiates it? ____________
Why would they? ____________
What if nobody does? ____________
Does it need HYPE for gas? ____________
Is there a signing requirement? ____________
```

HyperCore actions require EIP-712 signatures. HyperEVM functions require gas in HYPE. Plan both.

---

## dApp Archetype Templates

### 1. Perp Trading Interface / Vault (0-1 contracts)

**Architecture:** HyperCore API handles all the trading. HyperEVM contract (optional) for user deposits/withdrawals and accounting.

**Components:**
- HyperCore API calls via Python SDK or TypeScript SDK
- `VaultDeposit.sol` (optional) — ERC-20-like interface for the vault on HyperEVM
- HYPE bridge via `0x2222...2222` for moving funds between layers

**Common mistakes:**
- Trying to place orders from a Solidity contract — orders go through HyperCore API, not EVM
- Not handling HyperCore nonces correctly (they're rolling, not sequential)
- Forgetting to bridge HYPE from HyperCore to HyperEVM for gas

**Fetch sequence:** `architecture/SKILL.md` → `api/SKILL.md` → `wallets/SKILL.md` → `security/SKILL.md`

### 2. Token Launch (HIP-1 + HIP-2) (0 contracts)

**Architecture:** Deploy a HIP-1 spot token on HyperCore. Use HIP-2 for automated hyperliquidity. No EVM contract needed unless you want custom vesting or governance.

**Components:**
- HyperCore spot token creation via the API
- HIP-2 hyperliquidity seeding
- Bonding curve: x*y=k, graduates to full orderbook at threshold

**Common mistakes:**
- Trying to use ERC-20 instead of HIP-1 for a native token (you lose native DEX integration)
- Not seeding hyperliquidity — HIP-2 requires initial liquidity provision
- Confusing HyperCore spot decimals (6 typically) with HyperEVM decimals

**Fetch sequence:** `standards/SKILL.md` → `building-blocks/SKILL.md` → `api/SKILL.md`

### 3. Yield Vault (1-2 contracts on HyperEVM)

**Architecture:** HyperEVM vault accepts HYPE/USDC deposits. Vault manager uses HyperCore API to deploy into perp strategies. Users hold vault shares (ERC-20).

**Contracts:**
- `HyperliquidVault.sol` — ERC-4626-compatible vault accepting HYPE or USDC
- Optional: `VaultStrategy.sol` — operator logic for position management

**Common mistakes:**
- Not accounting for HYPE decimal difference (8 in HyperCore, 18 in HyperEVM after bridging)
- Missing reentrancy protection on withdrawal functions
- No slippage protection on HyperCore position entry/exit

**Fetch sequence:** `standards/SKILL.md` → `building-blocks/SKILL.md` → `security/SKILL.md` → `testing/SKILL.md`

### 4. HyperSwap Integration / DEX Aggregator (0-1 contracts)

**Architecture:** Route swaps through HyperSwap V2 (already deployed). Optionally wrap in a contract for custom fee logic or multi-hop routing.

**Components:**
- HyperSwap V2 Router (deployed, see `addresses/SKILL.md`)
- Optional: `Aggregator.sol` — if you need custom routing logic

**Common mistakes:**
- Deploying your own AMM when HyperSwap V2 already has liquidity
- Not using the correct Router address (see `addresses/SKILL.md`)
- Ignoring slippage on HyperSwap swaps (use amountOutMinimum)

**Fetch sequence:** `building-blocks/SKILL.md` → `addresses/SKILL.md` → `security/SKILL.md`

### 5. AI Agent Trading Bot (0 contracts)

**Architecture:** Pure HyperCore API. Python SDK or TypeScript SDK. Agent wallet with approved subaccount keys.

**Components:**
- Python or TypeScript agent using official SDK
- API wallet pattern (agent key approved by main wallet)
- No contracts unless managing user funds

**Common mistakes:**
- Using main wallet private key in the bot (use API wallet pattern)
- Not handling rate limits (429) with exponential backoff
- Hardcoding nonces (let the SDK manage them)

**Fetch sequence:** `api/SKILL.md` → `wallets/SKILL.md` → `concepts/SKILL.md` → `tools/SKILL.md`

---

## Phase 1 — Build

**Fetch:** `standards/SKILL.md`, `building-blocks/SKILL.md`, `addresses/SKILL.md`, `security/SKILL.md`, `api/SKILL.md`

For HyperEVM contracts:
- Use OpenZeppelin base contracts — don't reinvent ERC-20, ERC-721, AccessControl
- HYPE has 18 decimals on HyperEVM (same as ETH). USDC has 6.
- Use verified addresses from `addresses/SKILL.md` — never fabricate addresses
- Emit events for every state change
- Run through the security checklist before Phase 2

For HyperCore API integration:
- Use the official SDK (Python: `hyperliquid-dex`, TypeScript: `@nktkas/hyperliquid`)
- Always sign with EIP-712 for exchange actions
- Use agent wallets for automated bots — never expose main wallet keys
- Handle nonce management carefully — see `concepts/SKILL.md`

---

## Phase 2 — Test

**Fetch:** `testing/SKILL.md`

HyperEVM testing:
```bash
# Fork HyperEVM mainnet for local testing
anvil --fork-url https://rpc.hyperliquid.xyz/evm

# Or test against actual testnet
# Chain ID: 998, RPC: https://rpc.hyperliquid-testnet.xyz/evm
```

HyperCore API testing:
- Use testnet API: `https://api.hyperliquid-testnet.xyz`
- Get testnet HYPE from the faucet
- Test all order types, cancellations, nonce edge cases

---

## Phase 3 — Build Frontend

**Fetch:** `orchestration/SKILL.md`, `frontend-ux/SKILL.md`, `tools/SKILL.md`

wagmi/viem chain config:
```typescript
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
```

Show loading states on every async operation. HyperEVM blocks are ~1s but HyperCore actions are near-instant (sub-second). Differentiate in the UI.

---

## Phase 4 — Ship to Production

**Fetch:** `wallets/SKILL.md`, `frontend-playbook/SKILL.md`, `gas/SKILL.md`

### Contract Deployment
1. Deploy to HyperEVM testnet (chain ID 998) first
2. Verify contracts on HyperEVM block explorer
3. Transfer ownership to a multisig — never leave single EOA as owner in production
4. Deploy to mainnet (chain ID 999)

### HyperCore Integration
1. Switch from testnet API to mainnet API (`api.hyperliquid.xyz`)
2. Fund the agent wallet with enough HYPE for gas
3. Test small orders first before full automation

### Pre-Ship QA
Run the QA checklist. Fetch `qa/SKILL.md` and give it to a separate reviewer agent.

---

## Anti-Patterns

**Reinventing HyperCore.** Don't write an orderbook in Solidity when HyperCore has a native one processing 100k orders/sec.

**Wrong layer.** Trading logic in EVM contracts. Settlement logic in API calls that should be onchain. Know which layer does what.

**Nonce carelessness.** HyperCore nonces are rolling-set, not sequential. Using an old nonce or collision causes rejected orders. Let the SDK manage nonces.

**Hardcoded testnet.** Deploying to testnet then forgetting to switch to mainnet for production.

**Admin key in production.** Using a single EOA as contract owner in production. Use a multisig.

---

## Quick-Start Checklist

- [ ] Decide: HyperCore API vs HyperEVM vs both?
- [ ] Plan the architecture — what layer handles what?
- [ ] Count your contracts (aim for 0-2 for MVP)
- [ ] Identify all HyperCore API calls needed
- [ ] Write contracts using OpenZeppelin base contracts
- [ ] Test on HyperEVM testnet (chain ID 998) + HyperCore testnet API
- [ ] Deploy HyperEVM contracts, verify on explorer
- [ ] Deploy frontend
- [ ] Run pre-ship QA with a separate reviewer

---

## Skill Routing Table

| Phase | What you're doing | Skills to fetch |
|-------|-------------------|-----------------|
| **Plan** | Architecture | `ship/` (this), `architecture/`, `concepts/`, `why/` |
| **Contracts** | Writing Solidity | `standards/`, `building-blocks/`, `addresses/`, `security/` |
| **API Integration** | HyperCore API | `api/`, `wallets/`, `concepts/` |
| **Test** | Testing | `testing/` |
| **Frontend** | Building UI | `orchestration/`, `frontend-ux/`, `tools/` |
| **Production** | Deploy, QA | `wallets/`, `frontend-playbook/`, `qa/`, `indexing/` |
