---
name: standards
description: Token standards on Hyperliquid — ERC-20 on HyperEVM, HIP-1/HIP-2/HIP-3 native token standards on HyperCore. When to use each, how they work, key interfaces.
---

# Standards on Hyperliquid

## What You Probably Got Wrong

**"I'll use ERC-20 for my token."** For HyperEVM: yes. But for a native Hyperliquid token with built-in orderbook access, use HIP-1 on HyperCore. HIP-1 tokens get native spot trading without a DEX contract.

**"HIP-1 is just a wrapper."** HIP-1 is a native token standard at the protocol level. HIP-1 tokens are first-class citizens in HyperCore — they have native orderbook pairs, native transfer, native balances in HyperCore accounts.

**"I need to write a contract to create a market."** No. HIP-2 hyperliquidity is built into the protocol. Create a HIP-1 token, seed HIP-2 liquidity, and you have a market — no Solidity required.

---

## HyperEVM Standards (EVM-Compatible)

These work exactly like on Ethereum:

### ERC-20 (Fungible Tokens)
Standard fungible token on HyperEVM. Use when:
- You need composability with other HyperEVM contracts
- You want standard DeFi integrations (HyperSwap V2, lending)
- You're building a governance token or vault share token

```solidity
// Standard OpenZeppelin ERC-20 — works on HyperEVM unchanged
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract MyToken is ERC20 {
    constructor() ERC20("My Token", "MTK") {
        _mint(msg.sender, 1_000_000e18);
    }
}
```

**USDC on HyperEVM:** 6 decimals — same as on Ethereum.
**HYPE on HyperEVM:** 18 decimals (native currency).

### ERC-721 (NFTs)
Standard NFTs. Work exactly like Ethereum.

### ERC-4626 (Tokenized Vaults)
Vault standard for yield-bearing positions. Use for:
- HYPE staking vaults
- Perp trading vaults
- Any yield-generating contract

### ERC-2612 (Permit)
Gasless approvals. Works on HyperEVM.

---

## HyperCore Standards (Native, Non-EVM)

These are protocol-level standards on HyperCore. No contract deployment needed.

### HIP-1: Native Spot Tokens

HIP-1 is the standard for native spot tokens on HyperCore. A HIP-1 token is:
- First-class in HyperCore — appears in user balances, transferable, tradeable
- Has a native spot orderbook pair on HyperCore
- Uses a bonding curve (x*y=k) for initial price discovery
- Graduates to a full limit orderbook when market cap reaches the graduation threshold

**Creating a HIP-1 token:**
```python
# Via Python SDK
from hyperliquid.exchange import Exchange

exchange = Exchange(wallet, constants.MAINNET_API_URL)

# Register a spot asset (HIP-1)
result = exchange.spot_deploy_token(
    name="MY TOKEN",
    symbol="MTKN",
    total_supply=1_000_000_000,  # 1 billion
    decimals=6,
    initial_supply=500_000_000,  # 500M allocated to creator
    is_blacklist=False
)
```

**HIP-1 token properties:**
- Name: up to 20 characters
- Symbol: up to 6 characters
- Decimals: typically 6 or 8
- Supply: fixed at creation (no mint function)
- Transfer: native HyperCore transfer (no gas on HyperCore)

### HIP-2: Hyperliquidity

HIP-2 is protocol-level automated market-making for HIP-1 tokens. It's like having Uniswap built into the protocol.

**How it works:**
- Token creator seeds initial liquidity (USDC + tokens)
- HyperCore protocol manages the liquidity curve
- Uses x*y=k bonding curve mechanics
- Graduation: when market cap hits a threshold (~$10M-100M depending on configuration), moves to full CLOB

**Seeding HIP-2:**
```python
# After creating a HIP-1 token, seed hyperliquidity
result = exchange.spot_seed_liquidity(
    token="MTKN",
    usdc_amount=100_000,    # $100k USDC
    token_amount=500_000    # 500k tokens
)
```

**Key insight:** HIP-2 removes the cold-start problem. Your token has immediate liquidity from launch — no need to incentivize LPs.

### HIP-3: Builder-Controlled Spot DEX

HIP-3 lets builders deploy their own spot DEX with custom token listing controls. Unlike the main HyperCore spot market (where anyone can create a HIP-1 token), HIP-3 gives a builder exclusive authority to list tokens on their DEX.

**Use cases:**
- Curated token exchanges
- Platform-specific trading hubs
- Ecosystem DEXes

**HIP-3 asset ID formula:**
`asset_id = 100000 + (perp_dex_index * 10000) + token_index`

**Fee model:** Builders can charge up to 0.1% additional fee on HIP-3 trades, split with the protocol.

---

## Comparing Token Approaches

| Feature | ERC-20 on HyperEVM | HIP-1 on HyperCore |
|---------|-------------------|-------------------|
| Standard | ERC-20 | HIP-1 |
| Trading | Via HyperSwap V2 | Native orderbook |
| Gas for transfer | HYPE (HyperEVM tx) | None (HyperCore native) |
| DeFi composability | Full EVM ecosystem | HyperCore ecosystem |
| Liquidity bootstrap | Need to seed AMM | HIP-2 built-in |
| Token creation | Deploy contract | API call |
| Minting | Constructor/function | Fixed at creation |
| Best for | DeFi, governance, complex logic | Native trading, speculation |

**Hybrid approach (recommended for serious tokens):**
1. Launch as HIP-1 for native trading and fast price discovery
2. Bridge to HyperEVM as an ERC-20 wrapper for DeFi composability
3. Use both layers for maximum reach

---

## Token Decimals Quick Reference

| Token | HyperCore | HyperEVM |
|-------|-----------|---------|
| HYPE | float (e.g., "1.5") | 18 decimals |
| USDC | float (e.g., "100.0") | 6 decimals |
| HIP-1 tokens | per token config (usually 6) | N/A (unless wrapped) |
| ERC-20 | N/A | 18 decimals (standard) |

**CRITICAL:** USDC is 6 decimals on HyperEVM. Don't assume 18.

---

## Quick Reference: Which Standard to Use

| Scenario | Standard |
|----------|----------|
| DeFi token (vault shares, governance) | ERC-20 on HyperEVM |
| NFT collection | ERC-721 on HyperEVM |
| Token with native trading | HIP-1 on HyperCore |
| Token launch with instant liquidity | HIP-1 + HIP-2 on HyperCore |
| Curated exchange platform | HIP-3 on HyperCore |
| Yield vault | ERC-4626 on HyperEVM |
| Gasless token approvals | ERC-2612 on HyperEVM |
