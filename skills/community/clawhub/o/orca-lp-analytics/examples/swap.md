# Example: SOL to USDC Swap via SDK

Swap tokens using the Whirlpools SDK directly — no external API dependency. Useful when you need to rebalance tokens before opening an LP position.

> **Playbook**: [Swap (single-pool)](../SKILL.md#swap-single-pool) — quote, broadcast, and slippage pattern live in SKILL.md.

## Prerequisites

```bash
export SOLANA_RPC_URL="https://api.mainnet-beta.solana.com"
export KEYPAIR_PATH="/path/to/your/keypair.json"
```

## Full Example

```typescript
import { Connection, Keypair, PublicKey } from "@solana/web3.js";
import { Wallet } from "@coral-xyz/anchor";
import {
  WhirlpoolContext,
  buildWhirlpoolClient,
  ORCA_WHIRLPOOL_PROGRAM_ID,
  swapQuoteByInputToken,
  PriceMath,
} from "@orca-so/whirlpools-sdk";
import { Percentage, DecimalUtil } from "@orca-so/common-sdk";
import BN from "bn.js";
import * as fs from "fs";

const RPC_URL = process.env.SOLANA_RPC_URL || "https://api.mainnet-beta.solana.com";
const KEYPAIR_PATH = process.env.KEYPAIR_PATH ?? (() => {
  throw new Error("KEYPAIR_PATH environment variable is required.");
})();
const CONFIRM = process.argv.includes("--confirm");

// SOL/USDC 0.04% Whirlpool (highest TVL)
const SOL_USDC_POOL = new PublicKey("Czfq3xZZDmsdGdUyrNLtRhGc47cXcZtLG4crryfu44zE");
const SOL_MINT = new PublicKey("So11111111111111111111111111111111111111112");

const SWAP_SOL = 0.025; // Amount of SOL to swap to USDC
const SLIPPAGE = Percentage.fromFraction(1, 100); // 1%

async function main() {
  const connection = new Connection(RPC_URL, "confirmed");
  const secretKey = JSON.parse(fs.readFileSync(KEYPAIR_PATH, "utf-8"));
  const keypair = Keypair.fromSecretKey(Uint8Array.from(secretKey));
  const wallet = new Wallet(keypair);

  console.log(`Wallet: ${wallet.publicKey.toBase58()}`);

  // 1. Initialize SDK
  const ctx = WhirlpoolContext.from(connection, wallet);
  const client = buildWhirlpoolClient(ctx);

  // 2. Load pool
  const whirlpool = await client.getPool(SOL_USDC_POOL);
  const whirlpoolData = whirlpool.getData();

  const currentPrice = PriceMath.sqrtPriceX64ToPrice(
    whirlpoolData.sqrtPrice, 9, 6
  );
  console.log(`SOL/USDC price: $${currentPrice.toFixed(4)}`);

  // 3. Get swap quote
  const amountIn = new BN(SWAP_SOL * 1e9); // SOL in lamports

  const quote = await swapQuoteByInputToken(
    whirlpool,
    SOL_MINT,
    amountIn,
    SLIPPAGE,
    ORCA_WHIRLPOOL_PROGRAM_ID,
    ctx.fetcher,
  );

  const estIn = DecimalUtil.fromBN(quote.estimatedAmountIn, 9);
  const estOut = DecimalUtil.fromBN(quote.estimatedAmountOut, 6);
  const rate = estOut.toNumber() / estIn.toNumber();

  console.log(`\n=== Swap Quote ===`);
  console.log(`Input:  ${estIn.toFixed(6)} SOL`);
  console.log(`Output: ${estOut.toFixed(6)} USDC`);
  console.log(`Rate:   1 SOL = ${rate.toFixed(2)} USDC`);

  // 4. Execute swap (gated)
  if (!CONFIRM) {
    console.log(`\nDry-run only. Re-run with --confirm to broadcast this swap.`);
    return;
  }
  console.log(`\nExecuting swap...`);
  const tx = await whirlpool.swap(quote);
  const sig = await tx.buildAndExecute();

  console.log(`Swap confirmed: https://solscan.io/tx/${sig}`);

  // 5. Check new balance — use getParsedTokenAccountsByOwner (plain variant with
  // jsonParsed encoding throws StructError under @solana/web3.js 1.95+)
  const usdcMint = new PublicKey("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v");
  const usdcAta = await connection.getParsedTokenAccountsByOwner(wallet.publicKey, { mint: usdcMint });
  if (usdcAta.value.length > 0) {
    const bal = usdcAta.value[0].account.data.parsed.info.tokenAmount.uiAmountString;
    console.log(`USDC balance: ${bal}`);
  }
}

main().catch((err) => {
  console.error("Error:", err.message || err);
  process.exit(1);
});
```

## How It Works

1. **Load the pool** via `client.getPool()` — same as for LP operations.
2. **Quote the swap** with `swapQuoteByInputToken()` — the SDK fetches tick arrays, computes the route, and returns a `SwapQuote` with estimated amounts and slippage thresholds.
3. **Execute** with `whirlpool.swap(quote)` — the SDK builds the Anchor instruction, handles wSOL wrapping/unwrapping automatically, and sends the transaction.

No external API needed. The SDK does everything on-chain.

## Output

```
Wallet: 69Hbc2QzECnJgrrcp4kTeTuwScVw8QXjXiJXhjpa1X4v
SOL/USDC price: $86.07

=== Swap Quote ===
Input:  0.025000 SOL
Output: 2.147239 USDC
Rate:   1 SOL = 85.89 USDC

Executing swap...
Swap confirmed: https://solscan.io/tx/4xKm...

USDC balance: 2.150718
```

## Notes

- The SDK handles wSOL wrapping/unwrapping automatically for native SOL swaps.
- Slippage is enforced on-chain via `otherAmountThreshold` in the swap instruction.
- The same `swapQuoteByInputToken` + `whirlpool.swap()` pattern works for any token pair that has a Whirlpool.
- For exact-output swaps, use `swapQuoteByOutputToken()` instead.
