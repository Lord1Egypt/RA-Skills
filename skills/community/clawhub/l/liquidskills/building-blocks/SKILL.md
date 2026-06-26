---
name: building-blocks
description: DeFi legos on Hyperliquid — HyperSwap V2, bonding curves, HyperCore perps/spot as composable primitives. How to build on top of existing protocols instead of reinventing them.
---

# Building Blocks on Hyperliquid

## What You Probably Got Wrong

**"I need to deploy my own DEX."** HyperSwap V2 is already deployed on HyperEVM. It's Uniswap V2 compatible. Use it for swaps, liquidity, and price discovery on HyperEVM assets.

**"I need to write an orderbook contract."** HyperCore's native CLOB processes 100k orders/sec. You can't deploy a better orderbook in Solidity. Build on HyperCore's native orderbook via the API.

**"Token launches need a lot of setup."** HIP-1 + HIP-2 handles the whole thing at the protocol level. Bonding curve, initial liquidity, graduation to full orderbook — built in.

---

## HyperSwap V2 (Main DEX on HyperEVM)

HyperSwap V2 is the primary AMM DEX on HyperEVM. It's Uniswap V2 compatible — same interface, same mechanics, different chain.

See `addresses/SKILL.md` for deployed contract addresses.

### How HyperSwap V2 Works

- Constant product AMM: `x * y = k`
- Liquidity providers deposit token pairs into pools
- Swap fees go to LPs (standard 0.3%)
- Each pair is a separate pool contract deployed by the factory

### Swapping via HyperSwap Router

```solidity
import "@uniswap/v2-periphery/contracts/interfaces/IUniswapV2Router02.sol";

interface IHyperSwapV2Router02 is IUniswapV2Router02 {}

// Address from addresses/SKILL.md
IHyperSwapV2Router02 router = IHyperSwapV2Router02(HYPERSWAP_V2_ROUTER);

// Approve first
IERC20(tokenIn).approve(address(router), amountIn);

// Swap exact tokens for tokens
address[] memory path = new address[](2);
path[0] = tokenIn;
path[1] = tokenOut;

uint256[] memory amounts = router.swapExactTokensForTokens(
    amountIn,
    amountOutMin,   // ALWAYS set a minimum — never 0
    path,
    recipient,
    block.timestamp + 300
);
```

```typescript
// TypeScript: swap on HyperSwap V2
import { parseAbi, parseEther, parseUnits } from 'viem';

const hyperSwapRouterAbi = parseAbi([
  'function swapExactTokensForTokens(uint256 amountIn, uint256 amountOutMin, address[] calldata path, address to, uint256 deadline) returns (uint256[] memory amounts)',
  'function getAmountsOut(uint256 amountIn, address[] calldata path) view returns (uint256[] memory amounts)',
]);

// Get expected output
const amounts = await publicClient.readContract({
  address: HYPERSWAP_V2_ROUTER,
  abi: hyperSwapRouterAbi,
  functionName: 'getAmountsOut',
  args: [parseEther('1'), [WETH_ADDRESS, USDC_ADDRESS]],
});

const expectedOut = amounts[1];
const amountOutMin = expectedOut * 99n / 100n; // 1% slippage

// Approve and swap
await walletClient.writeContract({
  address: HYPERSWAP_V2_ROUTER,
  abi: hyperSwapRouterAbi,
  functionName: 'swapExactTokensForTokens',
  args: [parseEther('1'), amountOutMin, [WETH_ADDRESS, USDC_ADDRESS], recipientAddress, BigInt(Date.now() / 1000) + 300n],
});
```

### Adding Liquidity

```solidity
// Add liquidity to a HyperSwap V2 pair
IERC20(tokenA).approve(address(router), amountADesired);
IERC20(tokenB).approve(address(router), amountBDesired);

(uint amountA, uint amountB, uint liquidity) = router.addLiquidity(
    tokenA,
    tokenB,
    amountADesired,
    amountBDesired,
    amountAMin,     // Minimum A accepted (slippage protection)
    amountBMin,     // Minimum B accepted (slippage protection)
    recipient,
    deadline
);
```

---

## HyperCore Native Orderbook (Perps + Spot)

HyperCore's CLOB is the highest-leverage building block. You compose with it via the API, not via contracts.

### Perp Markets as Legos

**Reading perp state:**
```python
import requests

# All perp markets + metadata
meta = requests.post('https://api.hyperliquid.xyz/info',
                     json={'type': 'meta'}).json()

# All current mid prices
mids = requests.post('https://api.hyperliquid.xyz/info',
                     json={'type': 'allMids'}).json()

# Specific user's positions
state = requests.post('https://api.hyperliquid.xyz/info', json={
    'type': 'clearinghouseState',
    'user': '0xYourAddress'
}).json()

# Open interest and funding
ctx = requests.post('https://api.hyperliquid.xyz/info', json={
    'type': 'metaAndAssetCtxs'
}).json()
```

**Using perps in a vault strategy:**
```python
from hyperliquid.exchange import Exchange
from hyperliquid.info import Info

# Delta-neutral vault: long spot, short perp
def rebalance_vault(exchange, info, target_notional):
    # Get current ETH perp price
    mids = info.all_mids()
    eth_price = float(mids['ETH'])

    # Calculate position size
    size = target_notional / eth_price

    # Open short perp
    result = exchange.order(
        "ETH",
        is_buy=False,       # Short
        sz=size,
        limit_px=eth_price * 0.999,  # 0.1% below mid
        order_type={"limit": {"tif": "Gtc"}},
        reduce_only=False
    )
    return result
```

### Spot Markets as Legos

**HIP-1 spot tokens** are the building blocks for anything token-related on HyperCore:

```python
# Get all spot markets
spot_meta = requests.post('https://api.hyperliquid.xyz/info',
                           json={'type': 'spotMeta'}).json()

# Get spot orderbook for a token
book = requests.post('https://api.hyperliquid.xyz/info', json={
    'type': 'l2Book',
    'coin': 'PURR'  # Example HIP-1 token
}).json()

# Place spot limit order (buy PURR)
result = exchange.order(
    "PURR",
    is_buy=True,
    sz=1000,
    limit_px=0.001,
    order_type={"limit": {"tif": "Gtc"}}
)
```

---

## Bonding Curves and Token Launches

HIP-1 tokens use a bonding curve before graduating to a full orderbook:

**The RYPE pattern (x*y=k until threshold):**

```
Price discovery phase:
- New HIP-1 token launches with bonding curve
- x*y=k: buying increases price, selling decreases it
- No traditional LP needed — protocol handles liquidity

Graduation:
- When market cap hits the threshold (varies by configuration)
- Protocol removes liquidity from bonding curve
- Full CLOB (limit orderbook) activates
- Token now tradeable with all order types
```

**Building on bonding curve mechanics:**

```python
# Monitor token graduation
def watch_for_graduation(token_symbol, exchange, info):
    spot_meta = info.spot_meta()

    # Find the token
    token = next(t for t in spot_meta['tokens']
                 if t['name'] == token_symbol)

    token_index = spot_meta['tokens'].index(token)
    asset_id = 10000 + token_index

    # Check if bonding curve is still active or graduated
    # When graduated, there will be a CLOB with bid/ask spread
    book = info.l2_snapshot(token_symbol)

    if book['levels'][0] and book['levels'][1]:
        print(f"{token_symbol}: Graduated! Full orderbook active.")
    else:
        print(f"{token_symbol}: Still on bonding curve.")
```

---

## HyperCore Vault as a Building Block

The HLP (Hyperliquid Liquidity Provider) vault is a protocol-native vault. You can:
- Deposit into HLP and earn market-making fees
- Build custom vaults on top of HyperCore

**Custom vault pattern:**

```python
# Vault manager: accept user deposits, deploy into HyperCore strategies

class HyperliquidVault:
    def __init__(self, exchange, info):
        self.exchange = exchange
        self.info = info

    def deposit(self, amount_usdc, user_address):
        # Record deposit in your own accounting
        # USDC is in HyperCore balance
        pass

    def rebalance(self):
        # Use HyperCore perps/spot for strategy execution
        mids = self.info.all_mids()
        eth_price = float(mids['ETH'])

        # Example: long/short strategy
        self.exchange.order("ETH", True, 1.0, eth_price * 1.001,
                            {"limit": {"tif": "Gtc"}})
```

---

## Composability Patterns

### HyperEVM → HyperCore (Contract-Triggered Trades)

A HyperEVM contract can trigger HyperCore actions by reading from the HyperCore precompile:

```solidity
// Reading HyperCore state from HyperEVM
// System precompile (verify address in latest docs)
address constant HYPERCORE_PRECOMPILE = 0x0000000000000000000000000000000000000800;

// This enables conditional logic based on HyperCore state
// e.g., "execute this contract action only if ETH perp price > $2000"
```

### Flash Arb: HyperEVM + HyperCore

Since HyperEVM and HyperCore share finality:
1. Execute a HyperEVM swap (HyperSwap V2)
2. The price mismatch between HyperSwap and HyperCore spot is an arb opportunity
3. HyperBFT finality means both sides settle together

This is the most powerful composability pattern — using both layers atomically.

---

## What NOT to Build

- **Custom orderbook in Solidity** — HyperCore already has the best orderbook
- **Custom AMM from scratch** — HyperSwap V2 is deployed and has liquidity
- **Custom bonding curve** — HIP-2 does this at protocol level
- **MEV bots** — HyperCore's consensus eliminates frontrunning opportunities

**Build on top of primitives. Don't rebuild them.**
