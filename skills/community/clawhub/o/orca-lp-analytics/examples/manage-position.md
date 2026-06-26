# Manage an Existing LP Position

Increase liquidity, decrease liquidity, and close a position on Orca Whirlpools.

> **Playbooks**: [Increase Liquidity](../SKILL.md#increase-liquidity), [Decrease Liquidity](../SKILL.md#decrease-liquidity), [Close Position](../SKILL.md#close-position), [Fetch Positions](../SKILL.md#fetch-positions). Compute-unit sizing and refresh requirements live in SKILL.md.

## Increase Liquidity

Add more tokens to an existing position without changing the tick range.

```typescript
import { Connection, Keypair, PublicKey } from "@solana/web3.js";
import { Wallet } from "@coral-xyz/anchor";
import {
  WhirlpoolContext,
  buildWhirlpoolClient,
  ORCA_WHIRLPOOL_PROGRAM_ID,
  PDAUtil,
  increaseLiquidityQuoteByInputTokenUsingPriceDeviation,
  PriceMath,
  TokenExtensionUtil,
} from "@orca-so/whirlpools-sdk";
import { Percentage, DecimalUtil } from "@orca-so/common-sdk";
import { Decimal } from "decimal.js";
import * as fs from "fs";

const RPC_URL = process.env.SOLANA_RPC_URL || "https://api.mainnet-beta.solana.com";
const KEYPAIR_PATH = process.env.KEYPAIR_PATH ?? (() => {
  throw new Error("KEYPAIR_PATH environment variable is required.");
})();
const CONFIRM = process.argv.includes("--confirm");

// Replace with your position mint from open-position output
const POSITION_MINT = new PublicKey("YOUR_POSITION_MINT_HERE");
const ADDITIONAL_AMOUNT = 0.5; // Amount of token A to add (adjust units to match pool)

async function increaseLiquidity() {
  const connection = new Connection(RPC_URL, "confirmed");
  const secretKey = JSON.parse(fs.readFileSync(KEYPAIR_PATH, "utf-8"));
  const keypair = Keypair.fromSecretKey(Uint8Array.from(secretKey));
  const wallet = new Wallet(keypair);

  const ctx = WhirlpoolContext.from(connection, wallet);
  const client = buildWhirlpoolClient(ctx);

  // 1. Fetch position via PDA and its parent pool
  const positionPda = PDAUtil.getPosition(ORCA_WHIRLPOOL_PROGRAM_ID, POSITION_MINT);
  const position = await client.getPosition(positionPda.publicKey);
  const positionData = position.getData();
  const whirlpool = await client.getPool(positionData.whirlpool);
  await whirlpool.refreshData();  // bypass fetcher cache before quoting
  const whirlpoolData = whirlpool.getData();

  const tokenAInfo = whirlpool.getTokenAInfo();
  const tokenBInfo = whirlpool.getTokenBInfo();
  const tokenADecimals = tokenAInfo.decimals;
  const tokenBDecimals = tokenBInfo.decimals;
  const symbolA = `mint ${whirlpoolData.tokenMintA.toBase58().slice(0, 6)}`;
  const symbolB = `mint ${whirlpoolData.tokenMintB.toBase58().slice(0, 6)}`;

  const currentPrice = PriceMath.sqrtPriceX64ToPrice(
    whirlpoolData.sqrtPrice, tokenADecimals, tokenBDecimals
  );
  console.log(`Current price: ${currentPrice.toFixed(6)}`);

  // 2. Check if position is in range
  const inRange = whirlpoolData.tickCurrentIndex >= positionData.tickLowerIndex &&
                  whirlpoolData.tickCurrentIndex < positionData.tickUpperIndex;
  console.log(`Position in range: ${inRange}`);

  if (!inRange) {
    console.log("Position is out of range. Consider rebalancing instead.");
    return;
  }

  // 3. Build increase liquidity quote (tokenExtensionCtx required in SDK v0.20+)
  const tokenExtCtx = await TokenExtensionUtil.buildTokenExtensionContextForPool(
    ctx.fetcher, whirlpoolData.tokenMintA, whirlpoolData.tokenMintB,
  );

  const depositAmount = new Decimal(ADDITIONAL_AMOUNT);
  // Use PriceDeviation (NOT PriceSlippage) — position.increaseLiquidity expects
  // ByTokenAmountsParams which needs minSqrtPrice/maxSqrtPrice bounds around the
  // current pool price, correctly returned only by the deviation variant.
  const quote = increaseLiquidityQuoteByInputTokenUsingPriceDeviation(
    whirlpoolData.tokenMintA,
    depositAmount,
    positionData.tickLowerIndex,
    positionData.tickUpperIndex,
    Percentage.fromFraction(1, 100),
    whirlpool,
    tokenExtCtx,
  );

  const estA = DecimalUtil.fromBN(quote.tokenEstA, tokenADecimals);
  const estB = DecimalUtil.fromBN(quote.tokenEstB, tokenBDecimals);
  console.log(`\nAdding: ~${estA.toFixed(6)} ${symbolA} + ~${estB.toFixed(6)} ${symbolB}`);

  // 4. Execute (gated)
  if (!CONFIRM) {
    console.log(`\nDry-run only. Re-run with --confirm to broadcast increaseLiquidity.`);
    return;
  }
  const tx = await position.increaseLiquidity(quote);
  const txId = await tx.buildAndExecute();
  console.log(`Liquidity increased: https://solscan.io/tx/${txId}`);
}

increaseLiquidity().catch(console.error);
```

## Decrease Liquidity

Partially withdraw tokens from a position.

```typescript
import { Connection, Keypair, PublicKey } from "@solana/web3.js";
import { Wallet } from "@coral-xyz/anchor";
import BN from "bn.js";
import {
  WhirlpoolContext,
  buildWhirlpoolClient,
  ORCA_WHIRLPOOL_PROGRAM_ID,
  PDAUtil,
  decreaseLiquidityQuoteByLiquidityWithParams,
  TokenExtensionUtil,
} from "@orca-so/whirlpools-sdk";
import { Percentage, DecimalUtil } from "@orca-so/common-sdk";
import * as fs from "fs";

const RPC_URL = process.env.SOLANA_RPC_URL || "https://api.mainnet-beta.solana.com";
const KEYPAIR_PATH = process.env.KEYPAIR_PATH ?? (() => {
  throw new Error("KEYPAIR_PATH environment variable is required.");
})();
const CONFIRM = process.argv.includes("--confirm");

const POSITION_MINT = new PublicKey("YOUR_POSITION_MINT_HERE");
const WITHDRAW_PERCENT = 50; // Withdraw 50% of liquidity

async function decreaseLiquidity() {
  const connection = new Connection(RPC_URL, "confirmed");
  const secretKey = JSON.parse(fs.readFileSync(KEYPAIR_PATH, "utf-8"));
  const keypair = Keypair.fromSecretKey(Uint8Array.from(secretKey));
  const wallet = new Wallet(keypair);

  const ctx = WhirlpoolContext.from(connection, wallet);
  const client = buildWhirlpoolClient(ctx);

  const positionPda = PDAUtil.getPosition(ORCA_WHIRLPOOL_PROGRAM_ID, POSITION_MINT);
  const position = await client.getPosition(positionPda.publicKey);
  const positionData = position.getData();
  const whirlpool = await client.getPool(positionData.whirlpool);
  const whirlpoolData = whirlpool.getData();

  const tokenADecimals = whirlpool.getTokenAInfo().decimals;
  const tokenBDecimals = whirlpool.getTokenBInfo().decimals;

  // Calculate liquidity to remove
  const totalLiquidity = positionData.liquidity;
  const liquidityToRemove = totalLiquidity.mul(new BN(WITHDRAW_PERCENT)).div(new BN(100));

  console.log(`Total liquidity: ${totalLiquidity.toString()}`);
  console.log(`Removing ${WITHDRAW_PERCENT}%: ${liquidityToRemove.toString()}`);

  // Build decrease quote (tokenExtensionCtx required in SDK v0.20+)
  const tokenExtCtx = await TokenExtensionUtil.buildTokenExtensionContextForPool(
    ctx.fetcher, whirlpoolData.tokenMintA, whirlpoolData.tokenMintB,
  );

  const quote = decreaseLiquidityQuoteByLiquidityWithParams({
    liquidity: liquidityToRemove,
    tickLowerIndex: positionData.tickLowerIndex,
    tickUpperIndex: positionData.tickUpperIndex,
    slippageTolerance: Percentage.fromFraction(1, 100),
    sqrtPrice: whirlpoolData.sqrtPrice,
    tickCurrentIndex: whirlpoolData.tickCurrentIndex,
    tokenExtensionCtx: tokenExtCtx,
  });

  const estA = DecimalUtil.fromBN(quote.tokenEstA, tokenADecimals);
  const estB = DecimalUtil.fromBN(quote.tokenEstB, tokenBDecimals);
  console.log(`\nWithdrawing: ~${estA.toFixed(6)} token A + ~${estB.toFixed(6)} token B`);

  if (!CONFIRM) {
    console.log(`\nDry-run only. Re-run with --confirm to broadcast decreaseLiquidity.`);
    return;
  }
  const tx = await position.decreaseLiquidity(quote);
  const txId = await tx.buildAndExecute();
  console.log(`Liquidity decreased: https://solscan.io/tx/${txId}`);
}

decreaseLiquidity().catch(console.error);
```

## Close Position

Fully exit: collect fees, withdraw all liquidity, burn the NFT, reclaim rent.

```typescript
import { Connection, Keypair, PublicKey } from "@solana/web3.js";
import { Wallet } from "@coral-xyz/anchor";
import {
  WhirlpoolContext,
  buildWhirlpoolClient,
  ORCA_WHIRLPOOL_PROGRAM_ID,
  PDAUtil,
  decreaseLiquidityQuoteByLiquidityWithParams,
  TokenExtensionUtil,
} from "@orca-so/whirlpools-sdk";
import { Percentage, DecimalUtil } from "@orca-so/common-sdk";
import * as fs from "fs";

const RPC_URL = process.env.SOLANA_RPC_URL || "https://api.mainnet-beta.solana.com";
const KEYPAIR_PATH = process.env.KEYPAIR_PATH ?? (() => {
  throw new Error("KEYPAIR_PATH environment variable is required.");
})();
const CONFIRM = process.argv.includes("--confirm");

const POSITION_MINT = new PublicKey("YOUR_POSITION_MINT_HERE");

async function closePosition() {
  const connection = new Connection(RPC_URL, "confirmed");
  const secretKey = JSON.parse(fs.readFileSync(KEYPAIR_PATH, "utf-8"));
  const keypair = Keypair.fromSecretKey(Uint8Array.from(secretKey));
  const wallet = new Wallet(keypair);

  const ctx = WhirlpoolContext.from(connection, wallet);
  const client = buildWhirlpoolClient(ctx);

  const positionPda = PDAUtil.getPosition(ORCA_WHIRLPOOL_PROGRAM_ID, POSITION_MINT);
  const position = await client.getPosition(positionPda.publicKey);
  const positionData = position.getData();
  const whirlpool = await client.getPool(positionData.whirlpool);
  const whirlpoolData = whirlpool.getData();

  const tokenADecimals = whirlpool.getTokenAInfo().decimals;
  const tokenBDecimals = whirlpool.getTokenBInfo().decimals;

  console.log(`Closing position: ${POSITION_MINT.toBase58()}`);
  console.log(`Liquidity: ${positionData.liquidity.toString()}`);

  if (!CONFIRM) {
    console.log(`\nDry-run only. Re-run with --confirm to broadcast collect → drain → close.`);
    return;
  }

  // 1. Collect fees (pass true to sync fee accounting first)
  const feesTx = await position.collectFees(true);
  await feesTx.buildAndExecute();
  console.log("Fees collected.");

  // 2. Collect rewards (returns TransactionBuilder[])
  const rewardTxs = await position.collectRewards(undefined, true);
  for (const rtx of rewardTxs) {
    await rtx.buildAndExecute();
  }
  if (rewardTxs.length > 0) console.log("Rewards collected.");

  // 3. Withdraw all liquidity
  if (!positionData.liquidity.isZero()) {
    const tokenExtCtx = await TokenExtensionUtil.buildTokenExtensionContextForPool(
      ctx.fetcher, whirlpoolData.tokenMintA, whirlpoolData.tokenMintB,
    );

    const withdrawQuote = decreaseLiquidityQuoteByLiquidityWithParams({
      liquidity: positionData.liquidity,
      tickLowerIndex: positionData.tickLowerIndex,
      tickUpperIndex: positionData.tickUpperIndex,
      slippageTolerance: Percentage.fromFraction(1, 100),
      sqrtPrice: whirlpoolData.sqrtPrice,
      tickCurrentIndex: whirlpoolData.tickCurrentIndex,
      tokenExtensionCtx: tokenExtCtx,
    });

    const estA = DecimalUtil.fromBN(withdrawQuote.tokenEstA, tokenADecimals);
    const estB = DecimalUtil.fromBN(withdrawQuote.tokenEstB, tokenBDecimals);
    console.log(`Withdrawing: ~${estA.toFixed(6)} token A + ~${estB.toFixed(6)} token B`);

    const withdrawTx = await position.decreaseLiquidity(withdrawQuote);
    await withdrawTx.buildAndExecute();
  }

  // 4. Close position (burns NFT, reclaims rent)
  const closeTxs = await whirlpool.closePosition(
    positionPda.publicKey,
    Percentage.fromFraction(1, 100),
  );
  for (const ctxn of closeTxs) {
    await ctxn.buildAndExecute();
  }

  console.log(`\nPosition closed! NFT burned, ~0.003 SOL rent reclaimed.`);
}

closePosition().catch(console.error);
```

## Output

```
=== Increase Liquidity ===
Current price: 83.180000
Position in range: true
Adding: ~0.500000 mint So1111 + ~41.590000 mint EPjFWd
Liquidity increased: https://solscan.io/tx/3xKm...

=== Decrease Liquidity (50%) ===
Total liquidity: 4829173
Removing 50%: 2414586
Withdrawing: ~0.750000 token A + ~62.380000 token B
Liquidity decreased: https://solscan.io/tx/5yNp...

=== Close Position ===
Closing position: 7hYz...9pLm
Fees collected.
Withdrawing: ~1.500000 token A + ~124.770000 token B
Position closed! NFT burned, ~0.003 SOL rent reclaimed.
```

## Notes

- Increase liquidity requires both tokens in the correct ratio (determined by tick range and current price).
- Decrease liquidity returns tokens based on the current price -- if the position is out of range, you get only one token.
- Close position is a multi-step process: collect fees -> collect rewards -> withdraw liquidity -> close account.
- Always collect fees before closing -- uncollected fees are lost when the position is burned.
- Position PDA must be derived from the mint: `PDAUtil.getPosition(ORCA_WHIRLPOOL_PROGRAM_ID, positionMint)`.
- Close position lives on `whirlpool.closePosition()`, not on the position object.
