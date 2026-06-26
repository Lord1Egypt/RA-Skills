# Preflight Checks

Verify all of the following before proceeding. Block and inform the user if any check fails.

## 1. viem installed

```bash
node -e "require('viem')" 2>/dev/null && echo OK || echo MISSING
```

If missing, install it:

```bash
npm install viem
```

## 2. EVM wallet

An EVM wallet capable of signing and sending transactions on BNB Chain (chain ID `56`) must be available. The method of signing (private key, hardware wallet, browser wallet, MPC, etc.) is determined by the caller — this skill mainly helps you construct the transaction data.

## 3. BNB mainnet RPC access

Ask for an RPC URL for BNB Chain mainnet (chain ID `56`). A public fallback is `https://bsc-dataseed.binance.org/`. 

Verify connectivity:

```typescript
import { createPublicClient, http } from "viem";
import { bsc } from "viem/chains";

const client = createPublicClient({ chain: bsc, transport: http(RPC_URL) });
const block = await client.getBlockNumber();
console.log("Latest block:", block);
```

## 4. Sufficient BNB balance

The wallet needs BNB for:
- Gas fees (launching costs ~0.002–0.010 BNB in gas).
- Any initial buy amount (`quoteAmt`) the user wants to spend.

Check balance:

```typescript
const balance = await client.getBalance({ address: walletAddress });
// balance is in wei; 1 BNB = 1e18 wei
```

Warn if balance is below 0.01 BNB (exclusive of launch buy amount).
