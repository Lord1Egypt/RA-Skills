---
name: gas
description: HYPE gas costs on HyperEVM, actual transaction costs, fee mechanics, and when gas applies vs doesn't. Use when estimating costs, setting fee parameters, or explaining HyperEVM gas to users.
---

# Gas & Costs on HyperEVM

## What You Probably Got Wrong

**"Gas is paid in ETH."** No. HYPE is the native gas token on HyperEVM. Every HyperEVM transaction costs HYPE, not ETH.

**"Priority fees go to validators."** No. Priority fees on HyperEVM are burned. Validators do not receive priority fees. This is different from Ethereum.

**"Every Hyperliquid action costs gas."** HyperCore actions (placing orders, canceling orders, HyperCore transfers) do NOT cost EVM gas. Only HyperEVM transactions cost HYPE gas. Know which layer you're on.

**"Blobs are available for cheap data."** No blobs on HyperEVM — Hyperliquid doesn't need data availability blobs. The Cancun hardfork is implemented but without blob support. Don't use `blobhash()` or blob-related opcodes.

---

## Fee Mechanics

HyperEVM uses EIP-1559:

```
transaction fee = (baseFee + priorityFee) * gasUsed
```

- **baseFee**: set by protocol, burned
- **priorityFee (tip)**: also burned on HyperEVM (NOT paid to validators)
- **maxFeePerGas**: maximum you'll pay per unit of gas
- **maxPriorityFeePerGas**: tip above base fee — burned, but still required to signal urgency

**Both components are burned. Validators earn HYPE through staking rewards, not gas fees.**

---

## What Things Actually Cost

> Costs in HYPE. HYPE price is volatile — verify current price on CoinGecko or Hyperliquid's UI.
> Gas usage is similar to Ethereum for equivalent operations — the difference is the fee token.

| Action | Gas Used (approx) | Cost at 1 gwei baseFee |
|--------|-------------------|------------------------|
| HYPE transfer | 21,000 | ~0.000021 HYPE |
| ERC-20 transfer | ~65,000 | ~0.000065 HYPE |
| ERC-20 approve | ~46,000 | ~0.000046 HYPE |
| HyperSwap V2 swap | ~130,000 | ~0.000130 HYPE |
| ERC-20 deploy | ~1,200,000 | ~0.0012 HYPE |
| Simple contract deploy | ~500,000 | ~0.0005 HYPE |
| Complex DeFi contract | ~3,000,000 | ~0.003 HYPE |

**Gas costs are very low in absolute terms** because base fees on HyperEVM are low.

---

## HyperCore — No Gas Required

HyperCore actions do NOT cost EVM gas:

- Placing orders (perp or spot)
- Canceling orders
- Modifying orders
- HyperCore-to-HyperCore transfers (between HyperCore accounts)

HyperCore has its own fee structure (trading fees: maker 0.02%, taker 0.05% default, reduced for high volume), but these are NOT gas — they're trading fees charged in the quote asset.

**Only HyperEVM contract interactions cost HYPE gas.**

---

## Getting HYPE for Gas

Users need HYPE on HyperEVM to pay gas. Two ways to get it:

**1. Bridge from HyperCore to HyperEVM:**
Send HYPE to `0x2222222222222222222222222222222222222222` on HyperEVM, OR use the `/exchange` API action `"type": "spotSend"` to move HYPE from HyperCore to HyperEVM.

**2. Buy on HyperSwap V2:**
If already on HyperEVM with other tokens, swap for HYPE on HyperSwap V2 (see `addresses/SKILL.md` for router address).

**Testnet:** Get testnet HYPE from the Hyperliquid testnet faucet at https://app.hyperliquid-testnet.xyz/

---

## Practical Fee Settings

```typescript
// viem: setting gas for HyperEVM transactions
const tx = await walletClient.sendTransaction({
  to: contractAddress,
  data: calldata,
  maxFeePerGas: parseGwei('2'),          // 2 gwei max (safe headroom)
  maxPriorityFeePerGas: parseGwei('0.1'), // 0.1 gwei tip (burned anyway)
});

// Or let viem estimate automatically
const gasPrice = await publicClient.getGasPrice();
```

```python
# Python: setting gas for HyperEVM via web3.py
tx = contract.functions.myFunction(arg1, arg2).build_transaction({
    'from': account.address,
    'maxFeePerGas': web3.to_wei('2', 'gwei'),
    'maxPriorityFeePerGas': web3.to_wei('0.1', 'gwei'),
    'nonce': web3.eth.get_transaction_count(account.address),
})
```

**Recommended settings for current conditions:**
- `maxFeePerGas`: 2-5 gwei (generous headroom)
- `maxPriorityFeePerGas`: 0.1-0.5 gwei (tip is burned but still needed)

---

## Checking Gas Programmatically

```bash
# Foundry cast commands for HyperEVM
cast gas-price --rpc-url https://rpc.hyperliquid.xyz/evm
cast base-fee --rpc-url https://rpc.hyperliquid.xyz/evm

# Testnet
cast gas-price --rpc-url https://rpc.hyperliquid-testnet.xyz/evm
cast base-fee --rpc-url https://rpc.hyperliquid-testnet.xyz/evm
```

```typescript
// viem: get current gas price
import { createPublicClient, http } from 'viem';
import { hyperliquid } from './chains'; // your chain definition

const client = createPublicClient({
  chain: hyperliquid,
  transport: http('https://rpc.hyperliquid.xyz/evm'),
});

const feeData = await client.estimateFeesPerGas();
console.log('Base fee:', feeData.maxFeePerGas);
```

---

## HYPE Decimal Gotcha

**HYPE has 18 decimals on HyperEVM** (same as ETH on Ethereum). But in HyperCore API responses, HYPE amounts are expressed with different precision — check the context.

When bridging:
- HyperEVM: HYPE is 18-decimal (standard wei)
- HyperCore: HYPE balances are often expressed in float notation (e.g., `"1.5"` = 1.5 HYPE)

```solidity
// HyperEVM: 1 HYPE = 1e18 wei
uint256 oneHype = 1e18;

// Never assume 1e8 (that's a HyperCore internal representation)
// Always verify with the actual chain
```

---

## Gas Estimation for Contracts

```typescript
// Estimate gas before sending
const gasEstimate = await publicClient.estimateGas({
  account: myAddress,
  to: contractAddress,
  data: encodeFunctionData({ abi, functionName: 'myFunction', args: [arg1] }),
});

// Add 20% buffer
const gasLimit = gasEstimate * 120n / 100n;
```

Always estimate before sending. HyperEVM contracts can have variable gas costs based on state.

---

## HyperCore Trading Fees (Not Gas)

For reference — these are NOT gas, they're exchange trading fees:

| Tier | Maker Fee | Taker Fee | Minimum 14-day volume |
|------|-----------|-----------|----------------------|
| Default | 0.02% | 0.05% | — |
| Tier 1 | 0.014% | 0.042% | $5M |
| Tier 2 | 0.01% | 0.035% | $25M |
| Tier 3 | 0.004% | 0.028% | $100M |
| VIP | 0% | 0.020% | $500M+ |

Builder fees (HIP-3): up to 0.1% additional, set by the builder.

These fees are charged in the quote asset of each market (USDC for perps, quote token for spot).
