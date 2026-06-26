---
name: concepts
description: Essential mental models for building on Hyperliquid. HyperCore vs HyperEVM, asset IDs, nonce mechanics, margin types, incentive design. Use when designing a system or when you need to understand how Hyperliquid actually works.
---

# Hyperliquid Concepts

## What You Probably Got Wrong

**"Nothing is automatic on EVM."** This is still true on HyperEVM. Smart contracts don't run themselves. Every HyperEVM function needs a caller. But HyperCore is different — it HAS automatic processes: funding rate settlements, liquidations, order matching. The protocol runs these autonomously.

**"Nonces increment by 1."** On HyperCore, NO. HyperCore nonces are a rolling-set scheme — not sequential. Read the nonce section carefully before building any trading system.

**"HYPE is like ETH."** On HyperEVM, mostly yes. But HYPE is also the staking/governance token for the whole L1, not just gas. The total HYPE supply matters for protocol economics in ways ETH's doesn't.

---

## HyperCore vs HyperEVM: The Mental Model

Think of Hyperliquid as two machines sharing the same clock:

**HyperCore** = The Exchange Machine
- Native perp/spot orderbook running at protocol speed
- Manages positions, margins, liquidations, funding
- You interact via HTTP API (POST /info, POST /exchange)
- No contracts. No gas. Built into consensus.
- Think: a centralized exchange's matching engine, but consensus-secured

**HyperEVM** = The Smart Contract Machine
- Standard EVM: Solidity, OpenZeppelin, viem, Foundry
- Custom logic, composability, token contracts
- You interact via EVM RPC (eth_call, eth_sendTransaction)
- Needs gas (in HYPE). Has contracts.
- Think: a fast, cheap Ethereum L2

**The shared clock** = HyperBFT
- Both machines settle in the same consensus round
- Atomic finality across both layers
- Bridge between them is trustless (same validators)

---

## Nothing Is Automatic (HyperEVM)

Same rule as Ethereum. Smart contracts are state machines. Between caller interactions, they do nothing.

```
For every HyperEVM function:
  Who calls it? → Someone must pay HYPE gas
  Why would they? → What's their incentive?
  Is the incentive sufficient? → Does it cover gas + profit?
```

**HyperCore is different.** These ACTUALLY happen automatically:
- **Funding rate settlement:** Every 8 hours (and can be more frequent), funding payments happen automatically via the protocol
- **Liquidations:** When health factor drops below threshold, bots compete to liquidate (they earn a bonus)
- **Order matching:** Whenever a matching bid/ask exists, the protocol matches them

**Design implication:** If you need automatic behavior on HyperEVM, you still need an incentivized caller. If you want automatic trading behavior, it belongs in HyperCore (via a bot using the API), not in a contract.

---

## Asset IDs

Understanding asset IDs is the #1 source of confusion for HyperCore API users.

**Perp assets:**
- ID = index in `meta.universe` array
- ETH perp is typically index 1 (BTC is 0), but verify dynamically
- **NEVER hardcode asset indices.** They can change when new assets are added.

**Spot assets:**
- ID = 10000 + spot token index
- First HIP-1 token = spot index 0 → asset ID 10000
- Verify via `{"type": "spotMeta"}`

**HIP-3 builder DEX assets:**
- ID = 100000 + (perp_dex_index × 10000) + token_index
- Rarely needed unless building a HIP-3 exchange

```python
# CORRECT: Always fetch asset IDs dynamically
def get_asset_id(info, symbol, is_perp=True):
    if is_perp:
        meta = info.meta()
        for i, asset in enumerate(meta['universe']):
            if asset['name'] == symbol:
                return i
        raise ValueError(f"Perp asset {symbol} not found")
    else:
        spot_meta = info.spot_meta()
        for i, token in enumerate(spot_meta['tokens']):
            if token['name'] == symbol:
                return 10000 + i
        raise ValueError(f"Spot asset {symbol} not found")
```

---

## Nonces on HyperCore

**This is critically different from Ethereum.** Read carefully.

### HyperCore Nonce Rules

- Each signer has a **rolling window** of the 20 highest nonces seen
- Any new nonce must be **strictly greater** than the lowest nonce in the window
- Once the window is full (20 entries), new entries evict the lowest

**Why this design?**
- Allows parallel order submission (multiple nonces in flight simultaneously)
- Allows out-of-order arrival (nonce 5 can arrive after nonce 7)
- Prevents stuck nonces (you don't need sequential inclusion)

### Practical Nonce Management

```python
# ✅ CORRECT: Use millisecond timestamps
import time
nonce = int(time.time() * 1000)  # Always increasing, works for concurrent requests

# ✅ CORRECT: Use the official SDK (handles nonces internally)
from hyperliquid.exchange import Exchange
exchange = Exchange(wallet, api_url)  # SDK manages nonces

# ❌ WRONG: Don't try to track sequential nonces manually
nonce = last_nonce + 1  # Fails with concurrent requests

# ❌ WRONG: Don't reuse old nonces
nonce = 1234  # Will fail if this is in the current window
```

**Nonce conflict = order rejection.** Use millisecond timestamps or let the SDK handle it.

### Nonce Window and Concurrency

If you need to submit 5 orders in rapid succession:
```python
import time

# Stagger by 1ms each to guarantee unique nonces
orders = []
for i in range(5):
    nonce = int(time.time() * 1000) + i
    orders.append(build_order(nonce=nonce, ...))

# Submit in parallel or sequence
```

---

## Margin Types on HyperCore

HyperCore has two margin modes for perp positions:

### Cross Margin (Default)
- All positions share a single USDC margin pool
- If one position loses, the shared pool covers it
- More capital-efficient (don't need margin per position)
- Risk: a big loss in one position can liquidate ALL positions

### Isolated Margin
- Each position has its own dedicated margin
- Losses in one position don't affect others
- Less capital-efficient (need to allocate margin per position)
- Risk: limited to the allocated margin for that position

```python
# Switch a position to isolated margin
result = exchange.update_isolated_margin(
    coin="ETH",
    is_buy=True,
    ntli=100.0  # Isolated margin amount in USDC
)
```

---

## Liquidations on HyperCore

Understanding liquidations is critical for designing systems around HyperCore:

**How liquidations work:**
1. Position health = (account equity / maintenance margin requirement)
2. When health < 1: the position is eligible for liquidation
3. Anyone (typically bots) can call liquidate
4. Liquidator receives a bonus (% of position value)
5. Remaining assets go back to the liquidated user

**Health factor calculation:**
```
Account Value = USDC Balance + Unrealized PnL
Maintenance Margin = Sum of (position_size × price × maintenance_rate)

Health = Account Value / Maintenance Margin
```

**Liquidation trigger:** Health < 1 (or specified threshold per market).

**For vault builders:** Your vault can become a liquidation bot — earn fees by monitoring positions and liquidating unhealthy ones.

---

## Funding Rates

Perpetual futures use funding rates to keep perp prices in line with spot:

- **Positive funding:** Longs pay shorts (perp price > spot → shorts pay longs)
- **Negative funding:** Shorts pay longs (perp price < spot → longs pay shorts)
- **Settlement:** Funding accrues continuously but settles periodically (every 8 hours standard)
- **Rate:** Calculated based on the spread between perp mark price and index price

```python
# Get current funding rates
ctx = requests.post('https://api.hyperliquid.xyz/info',
                    json={'type': 'metaAndAssetCtxs'}).json()

for i, (asset, ctx) in enumerate(zip(ctx[0]['universe'], ctx[1])):
    if ctx.get('funding'):
        print(f"{asset['name']}: funding={ctx['funding']} premium={ctx.get('premium', 'N/A')}")
```

---

## Price Types in HyperCore

HyperCore uses several price concepts:

- **Mark price:** Used for margin calculations. Derived from median of oracle prices.
- **Oracle price:** External price feed, used for funding rate calculation.
- **Mid price:** (Best bid + Best ask) / 2 from the CLOB.
- **Last trade price:** Price of the most recent fill.

**For calculations involving margin and health:** Use mark price.
**For placing limit orders:** Use mid price as reference.
**For spot price:** Use the CLOB mid price.

---

## Decimals: A Gotcha Summary

| Asset | HyperCore API | HyperEVM |
|-------|--------------|---------|
| HYPE | Float string (e.g., "1.5") | 18 decimals (1.5 HYPE = 1.5e18 wei) |
| USDC | Float string (e.g., "100.0") | 6 decimals (100 USDC = 100e6) |
| Perp size | Float string | N/A |
| Perp notional | USDC float | N/A |
| HIP-1 tokens | Per token config | N/A unless bridged |

**USDC has 6 decimals on HyperEVM.** This is the #1 decimal bug. Don't assume 18.

---

## The EIP-712 Signing Mental Model

Every HyperCore exchange action requires an EIP-712 signature:

```
1. Build action payload (specific to the action type)
2. Construct EIP-712 message:
   - Domain: { name: "Exchange", version: "1", chainId: 1337 }
   - Struct: the action data
3. Hash: keccak256(abi.encodePacked("\x19\x01", domainSeparator, structHash))
4. Sign: ECDSA sign with private key
5. Extract: r, s, v components
6. Submit: POST /exchange with { action, nonce, signature: {r, s, v} }
```

**chainId in EIP-712 is always 1337 for HyperCore** — not 999 (HyperEVM mainnet) or 998 (testnet). This is a deliberate design choice that makes HyperCore signing portable.

Use the SDK — it handles all this correctly.
