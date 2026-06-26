---
name: cross-forge-trade
description: Performs token buy/sell on Cross Forge. Use when a user wants to buy or sell a specific token, or needs a swap through the Cross Forge Router.
---

# Cross Forge Token Trading Skill

This skill provides methods to buy or sell tokens through the Cross Forge DEX Router contract.

## Configuration

### Mainnet

| Item | Value |
|------|-------|
| Chain ID | 612055 |
| RPC URL | https://mainnet.crosstoken.io:22001 |
| Router Address | 0x7aF414e4d373bb332f47769c8d28A446A0C1a1E8 |
| Wrapped Native (WCROSS) | 0xDdF8AaA3927b8Fd5684dc2edcc7287EcB0A2122d |
| Trade Token (MOLTZ) | 0xdb99a97d607c5c5831263707E7b746312406ba7E |

## Required ABI

### Router ABI (Trading)

```json
[
  {
    "name": "swapExactNativeForTokens",
    "type": "function",
    "stateMutability": "payable",
    "inputs": [
      { "name": "amountOutMin", "type": "uint256" },
      { "name": "path", "type": "address[]" },
      { "name": "to", "type": "address" },
      { "name": "deadline", "type": "uint256" }
    ],
    "outputs": [{ "name": "amounts", "type": "uint256[]" }]
  },
  {
    "name": "swapExactTokensForNative",
    "type": "function",
    "stateMutability": "nonpayable",
    "inputs": [
      { "name": "amountIn", "type": "uint256" },
      { "name": "amountOutMin", "type": "uint256" },
      { "name": "path", "type": "address[]" },
      { "name": "to", "type": "address" },
      { "name": "deadline", "type": "uint256" }
    ],
    "outputs": [{ "name": "amounts", "type": "uint256[]" }]
  },
  {
    "name": "getAmountOutWithFees",
    "type": "function",
    "stateMutability": "view",
    "inputs": [
      { "name": "amountIn", "type": "uint256" },
      { "name": "path", "type": "address[]" }
    ],
    "outputs": [
      { "name": "amountOut", "type": "uint256" },
      { "name": "creatorFee", "type": "uint256" },
      { "name": "protocolFee", "type": "uint256" }
    ]
  }
]
```

### ERC20 ABI (for approve)

```json
[
  {
    "name": "approve",
    "type": "function",
    "stateMutability": "nonpayable",
    "inputs": [
      { "name": "spender", "type": "address" },
      { "name": "amount", "type": "uint256" }
    ],
    "outputs": [{ "name": "", "type": "bool" }]
  },
  {
    "name": "allowance",
    "type": "function",
    "stateMutability": "view",
    "inputs": [
      { "name": "owner", "type": "address" },
      { "name": "spender", "type": "address" }
    ],
    "outputs": [{ "name": "", "type": "uint256" }]
  },
  {
    "name": "balanceOf",
    "type": "function",
    "stateMutability": "view",
    "inputs": [{ "name": "account", "type": "address" }],
    "outputs": [{ "name": "", "type": "uint256" }]
  }
]
```

## Trading Flow

### 1. Buy (CROSS -> Token)

Buy tokens using CROSS.

```
┌──────────────────────────────────────────────────────────────────┐
│ 1. Call getAmountOutWithFees to check expected output amount     │
│ 2. Call swapExactNativeForTokens (include CROSS amount in value) │
└──────────────────────────────────────────────────────────────────┘
```

**Parameter setup:**

```javascript
// Buy example: Purchase tokens with 10 CROSS
const amountIn = "10000000000000000000"; // 10 CROSS (18 decimals)
const tokenAddress = "0xdb99a97d607c5c5831263707E7b746312406ba7E"; // MOLTZ token
const wcross = "0xDdF8AaA3927b8Fd5684dc2edcc7287EcB0A2122d";

// 1. Get quote
const path = [wcross, tokenAddress];
const [amountOut, creatorFee, protocolFee] = await getAmountOutWithFees(amountIn, path);

// 2. Apply slippage (e.g. 1%)
const amountOutMin = amountOut * 99n / 100n;

// 3. Execute buy
const deadline = Math.floor(Date.now() / 1000) + 300; // 5 minutes from now
await swapExactNativeForTokens(
  amountOutMin,
  path,
  recipientAddress,
  deadline,
  { value: amountIn }
);
```

### 2. Sell (Token -> CROSS)

Sell tokens to receive CROSS.

**Important: Approve is required before selling**

```
┌──────────────────────────────────────────────────────────────────┐
│ 1. Check allowance                                               │
│ 2. If insufficient, call approve(routerAddress, amount)          │
│ 3. Call getAmountOutWithFees to check expected output amount     │
│ 4. Call swapExactTokensForNative                                 │
└──────────────────────────────────────────────────────────────────┘
```

**Parameter setup:**

```javascript
// Sell example: Sell 1000 tokens
const amountIn = "1000000000000000000000"; // 1000 tokens (18 decimals)
const tokenAddress = "0xdb99a97d607c5c5831263707E7b746312406ba7E"; // MOLTZ token
const wcross = "0xDdF8AaA3927b8Fd5684dc2edcc7287EcB0A2122d";
const routerAddress = "0x7aF414e4d373bb332f47769c8d28A446A0C1a1E8";

// 1. Check allowance
const currentAllowance = await allowance(walletAddress, routerAddress);

// 2. Approve if needed
if (currentAllowance < amountIn) {
  await approve(routerAddress, amountIn);
}

// 3. Get quote
const path = [tokenAddress, wcross];
const [amountOut, creatorFee, protocolFee] = await getAmountOutWithFees(amountIn, path);

// 4. Apply slippage (e.g. 1%)
const amountOutMin = amountOut * 99n / 100n;

// 5. Execute sell
const deadline = Math.floor(Date.now() / 1000) + 300; // 5 minutes from now
await swapExactTokensForNative(
  amountIn,
  amountOutMin,
  path,
  recipientAddress,
  deadline
);
```

## Cast Command Examples

Examples using the cast CLI.

### Get Quote

```bash
# Expected output amount when buying tokens with 10 CROSS
cast call 0x7aF414e4d373bb332f47769c8d28A446A0C1a1E8 \
  "getAmountOutWithFees(uint256,address[])" \
  10000000000000000000 \
  "[0xDdF8AaA3927b8Fd5684dc2edcc7287EcB0A2122d,0xdb99a97d607c5c5831263707E7b746312406ba7E]" \
  --rpc-url https://mainnet.crosstoken.io:22001
```

### Execute Buy

```bash
# Buy MOLTZ with 10 CROSS
cast send 0x7aF414e4d373bb332f47769c8d28A446A0C1a1E8 \
  "swapExactNativeForTokens(uint256,address[],address,uint256)" \
  <AMOUNT_OUT_MIN> \
  "[0xDdF8AaA3927b8Fd5684dc2edcc7287EcB0A2122d,0xdb99a97d607c5c5831263707E7b746312406ba7E]" \
  <RECIPIENT_ADDRESS> \
  <DEADLINE> \
  --value 10ether \
  --rpc-url https://mainnet.crosstoken.io:22001 \
  --private-key <PRIVATE_KEY>
```

### Approve

```bash
# Approve MOLTZ token
cast send 0xdb99a97d607c5c5831263707E7b746312406ba7E \
  "approve(address,uint256)" \
  0x7aF414e4d373bb332f47769c8d28A446A0C1a1E8 \
  <AMOUNT> \
  --rpc-url https://mainnet.crosstoken.io:22001 \
  --private-key <PRIVATE_KEY>
```

### Execute Sell

```bash
# Sell MOLTZ
cast send 0x7aF414e4d373bb332f47769c8d28A446A0C1a1E8 \
  "swapExactTokensForNative(uint256,uint256,address[],address,uint256)" \
  <AMOUNT_IN> \
  <AMOUNT_OUT_MIN> \
  "[0xdb99a97d607c5c5831263707E7b746312406ba7E,0xDdF8AaA3927b8Fd5684dc2edcc7287EcB0A2122d]" \
  <RECIPIENT_ADDRESS> \
  <DEADLINE> \
  --rpc-url https://mainnet.crosstoken.io:22001 \
  --private-key <PRIVATE_KEY>
```

## Important Notes

1. **Slippage**: Set an appropriate slippage tolerance (1-5%) to account for price fluctuations.
2. **Deadline**: Set an appropriate transaction expiry time (typically 5-30 minutes).
3. **Approve**: Token approval for the Router must be completed before selling.
4. **Gas**: Check gas fees on the CROSSFI network.
5. **Decimals**: Most tokens use 18 decimals, but verify the actual token decimals.

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `INSUFFICIENT_OUTPUT_AMOUNT` | Slippage exceeded | Lower amountOutMin or retry |
| `EXPIRED` | Deadline exceeded | Retry with a new deadline |
| `TRANSFER_FROM_FAILED` | Approve not executed | Execute approve first |
| `INSUFFICIENT_LIQUIDITY` | Insufficient liquidity | Reduce trade amount |
