# Open Concentrated Liquidity Position on SOL/USDC

Open a position on the SOL/USDC Whirlpool with a +/-5% range around the current price.

> **Playbooks**: [Open Position](../SKILL.md#open-position) for the main flow, [Open from Single Token](../SKILL.md#open-from-single-token) if starting with only one token. `tokenMax` vs `tokenEst` details live in SKILL.md.

## Full Example

```typescript
import { Connection, Keypair, PublicKey } from "@solana/web3.js";
import { Wallet } from "@coral-xyz/anchor";
import {
  WhirlpoolContext,
  buildWhirlpoolClient,
  PriceMath,
  increaseLiquidityQuoteByInputTokenUsingPriceDeviation,
  TokenExtensionUtil,
} from "@orca-so/whirlpools-sdk";
import { Percentage, DecimalUtil } from "@orca-so/common-sdk";
import { Decimal } from "decimal.js";
import * as fs from "fs";

// --- Configuration ---
const RPC_URL = process.env.SOLANA_RPC_URL || "https://api.mainnet-beta.solana.com";
const KEYPAIR_PATH = process.env.KEYPAIR_PATH ?? (() => {
  throw new Error("KEYPAIR_PATH environment variable is required.");
})();
const CONFIRM = process.argv.includes("--confirm");

// SOL/USDC 0.04% Whirlpool address (tick spacing = 4)
const SOL_USDC_POOL = new PublicKey("Czfq3xZZDmsdGdUyrNLtRhGc47cXcZtLG4crryfu44zE");

// Amount of SOL to deposit
const DEPOSIT_SOL = 1.0;

// Range: +/- 5% around current price
const RANGE_PERCENT = 5;

// Slippage tolerance
const SLIPPAGE = Percentage.fromFraction(1, 100); // 1%

async function main() {
  // 1. Initialize connection and wallet
  const connection = new Connection(RPC_URL, "confirmed");
  const secretKey = JSON.parse(fs.readFileSync(KEYPAIR_PATH, "utf-8"));
  const keypair = Keypair.fromSecretKey(Uint8Array.from(secretKey));
  const wallet = new Wallet(keypair);
  console.log(`Wallet: ${wallet.publicKey.toBase58()}`);

  // 2. Initialize Whirlpool client
  const ctx = WhirlpoolContext.from(connection, wallet);
  const client = buildWhirlpoolClient(ctx);

  // 3. Load pool data — refreshData bypasses fetcher cache.
  // CRITICAL: stale cached sqrtPrice causes PriceSlippageOutOfBounds at tx time.
  const whirlpool = await client.getPool(SOL_USDC_POOL);
  await whirlpool.refreshData();
  const whirlpoolData = whirlpool.getData();

  const tokenADecimals = 9;  // SOL
  const tokenBDecimals = 6;  // USDC
  const tickSpacing = whirlpoolData.tickSpacing;

  // 4. Get current price
  const currentPrice = PriceMath.sqrtPriceX64ToPrice(
    whirlpoolData.sqrtPrice,
    tokenADecimals,
    tokenBDecimals,
  );
  const currentPriceNum = currentPrice.toNumber();
  console.log(`Current SOL/USDC price: $${currentPriceNum.toFixed(4)}`);

  // 5. Calculate tick range (+/- 5%) using SDK price-to-tick conversion
  const priceLower = new Decimal(currentPriceNum * (1 - RANGE_PERCENT / 100));
  const priceUpper = new Decimal(currentPriceNum * (1 + RANGE_PERCENT / 100));

  const rawTickLower = PriceMath.priceToTickIndex(priceLower, tokenADecimals, tokenBDecimals);
  const rawTickUpper = PriceMath.priceToTickIndex(priceUpper, tokenADecimals, tokenBDecimals);

  // Align to tick spacing (round down for lower, round up for upper)
  const tickLower = Math.floor(rawTickLower / tickSpacing) * tickSpacing;
  const tickUpper = Math.ceil(rawTickUpper / tickSpacing) * tickSpacing;

  const actualPriceLower = PriceMath.tickIndexToPrice(tickLower, tokenADecimals, tokenBDecimals);
  const actualPriceUpper = PriceMath.tickIndexToPrice(tickUpper, tokenADecimals, tokenBDecimals);

  console.log(`\nTick range: [${tickLower}, ${tickUpper}]`);
  console.log(`Price range: $${actualPriceLower.toFixed(4)} - $${actualPriceUpper.toFixed(4)}`);

  // 6. Check SOL balance
  const solBalance = await connection.getBalance(wallet.publicKey);
  const solBalanceDecimal = solBalance / 1e9;
  console.log(`\nSOL balance: ${solBalanceDecimal.toFixed(4)} SOL`);

  if (solBalanceDecimal < DEPOSIT_SOL + 0.05) {
    throw new Error(
      `Insufficient SOL. Need ${DEPOSIT_SOL} SOL for deposit + ~0.05 SOL for fees/rent. ` +
      `Available: ${solBalanceDecimal.toFixed(4)} SOL`
    );
  }

  // 7. Get deposit quote using price-DEVIATION variant
  //
  // IMPORTANT: use UsingPriceDeviation (NOT UsingPriceSlippage) because
  // openPositionWithMetadata's ByTokenAmountsParams requires both tokenMaxA/B
  // AND minSqrtPrice/maxSqrtPrice. Only the deviation variant returns these
  // sqrt bounds CORRECTLY computed around the current pool price.
  //
  // Using the slippage variant and faking in sqrt bounds from the position
  // range (tickLower/tickUpper) causes PriceSlippageOutOfBounds (error 0x17b5)
  // when the pool moves between quote and tx submission — the loose sqrt
  // bounds pass, but tokenMaxA/B was computed for a different price, and the
  // on-chain amount check rejects.
  const tokenExtCtx = await TokenExtensionUtil.buildTokenExtensionContextForPool(
    ctx.fetcher, whirlpoolData.tokenMintA, whirlpoolData.tokenMintB,
  );

  const depositAmount = new Decimal(DEPOSIT_SOL);
  const quote = increaseLiquidityQuoteByInputTokenUsingPriceDeviation(
    whirlpoolData.tokenMintA,  // input token mint (SOL)
    depositAmount,
    tickLower,
    tickUpper,
    SLIPPAGE,  // price deviation tolerance (±1% of current price)
    whirlpool,
    tokenExtCtx,
  );

  const estimatedSOL = DecimalUtil.fromBN(quote.tokenEstA, tokenADecimals);
  const estimatedUSDC = DecimalUtil.fromBN(quote.tokenEstB, tokenBDecimals);
  const maxSOL = DecimalUtil.fromBN(quote.tokenMaxA, tokenADecimals);
  const maxUSDC = DecimalUtil.fromBN(quote.tokenMaxB, tokenBDecimals);

  console.log(`\n=== Open Position Summary ===`);
  console.log(`Pool: SOL/USDC (0.04%)`);
  console.log(`Range: $${actualPriceLower.toFixed(4)} - $${actualPriceUpper.toFixed(4)} (+/-${RANGE_PERCENT}%)`);
  console.log(`Deposit: ~${estimatedSOL.toFixed(4)} SOL + ~${estimatedUSDC.toFixed(4)} USDC`);
  console.log(`Max (with slippage): ${maxSOL.toFixed(4)} SOL + ${maxUSDC.toFixed(4)} USDC`);
  console.log(`Price deviation tolerance: 1%`);

  // 8. Open position with metadata and initial liquidity
  // The quote already contains correctly-matched minSqrtPrice/maxSqrtPrice
  const { positionMint, tx } = await whirlpool.openPositionWithMetadata(
    tickLower,
    tickUpper,
    quote,
  );

  if (!CONFIRM) {
    console.log(`\nDry-run only. Re-run with --confirm to broadcast openPositionWithMetadata.`);
    console.log(`Would mint position: ${positionMint.toBase58()}`);
    return;
  }
  console.log(`\nSending transaction...`);
  const txId = await tx.buildAndExecute();

  console.log(`\nPosition opened successfully!`);
  console.log(`Position mint (NFT): ${positionMint.toBase58()}`);
  console.log(`Transaction: https://solscan.io/tx/${txId}`);
  console.log(`\nSave the position mint address to manage this position later.`);
}

main().catch(console.error);
```

## How It Works

1. **Connect** to Solana RPC and load the wallet keypair.
2. **Fetch pool data** from the on-chain Whirlpool account to get the current sqrt price and tick.
3. **Calculate the tick range** by converting the desired price bounds (+/-5% of current price) to tick indices, aligned to the pool's tick spacing (4 for SOL/USDC 0.04%).
4. **Get a liquidity quote** specifying 1 SOL as the input. The SDK calculates the matching USDC amount based on the current price and tick range.
5. **Open the position** with metadata (creates an NFT representing the LP position) and deposits both tokens in a single transaction.

## Adjusting the Range

Change `RANGE_PERCENT` to adjust the strategy:

| Value | Strategy | Notes |
|-------|----------|-------|
| `2` | Tight | Highest yield, frequent rebalancing |
| `5` | Medium | Balanced approach |
| `10` | Wide | Less maintenance, lower yield |
| `100` | Near-full | Rarely goes out of range |

For a full-range position (never out of range), use:

```typescript
const MIN_TICK = -443636;
const MAX_TICK = 443636;
const tickLower = Math.ceil(MIN_TICK / tickSpacing) * tickSpacing;
const tickUpper = Math.floor(MAX_TICK / tickSpacing) * tickSpacing;
```

## Output

> **Requires**: dependencies pinned by the skill, `KEYPAIR_PATH`, `SOLANA_RPC_URL` (optional). Submits a real transaction when re-run with `--confirm`.

Expected output (with keypair):
```
Opening position on SOL/USDC (0.04% fee)
Pool: Czfq3xZZDmsdGdUyrNLtRhGc47cXcZtLG4crryfu44zE
Current price: $83.18
Tick range: -25200 to -24400 (±5% around current)
Price range: $79.02 - $87.34

Depositing:
  SOL: 1.000
  USDC: ~83.18

Transaction submitted: 4xKm...2rQp
Position opened: 7hYz...9pLm
```
