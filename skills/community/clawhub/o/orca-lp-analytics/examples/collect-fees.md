# Collect Fees from an Orca Whirlpool Position

Harvest accrued trading fees and reward emissions from an existing concentrated liquidity position.

> **Playbook**: [Collect Fees + Rewards](../SKILL.md#collect-fees--rewards) — `collectFees(true)` syncs + collects in one tx; `collectRewards` returns a TransactionBuilder[] to iterate.

## Full Example

```typescript
import { Connection, Keypair, PublicKey } from "@solana/web3.js";
import { Wallet } from "@coral-xyz/anchor";
import {
  WhirlpoolContext,
  buildWhirlpoolClient,
  ORCA_WHIRLPOOL_PROGRAM_ID,
  PDAUtil,
  PriceMath,
} from "@orca-so/whirlpools-sdk";
import { DecimalUtil } from "@orca-so/common-sdk";
import * as fs from "fs";

// --- Configuration ---
const RPC_URL = process.env.SOLANA_RPC_URL || "https://api.mainnet-beta.solana.com";
const KEYPAIR_PATH = process.env.KEYPAIR_PATH ?? (() => {
  throw new Error("KEYPAIR_PATH environment variable is required.");
})();
const CONFIRM = process.argv.includes("--confirm");

// Position mint address (the NFT representing the LP position)
const POSITION_MINT = new PublicKey("YOUR_POSITION_MINT_ADDRESS");

async function main() {
  // 1. Initialize
  const connection = new Connection(RPC_URL, "confirmed");
  const secretKey = JSON.parse(fs.readFileSync(KEYPAIR_PATH, "utf-8"));
  const keypair = Keypair.fromSecretKey(Uint8Array.from(secretKey));
  const wallet = new Wallet(keypair);

  const ctx = WhirlpoolContext.from(connection, wallet);
  const client = buildWhirlpoolClient(ctx);

  // 2. Load position
  const positionPda = PDAUtil.getPosition(ORCA_WHIRLPOOL_PROGRAM_ID, POSITION_MINT);
  const position = await client.getPosition(positionPda.publicKey);
  const positionData = position.getData();

  // 3. Load parent whirlpool for context
  const whirlpool = await client.getPool(positionData.whirlpool);
  const whirlpoolData = whirlpool.getData();

  const tokenADecimals = whirlpool.getTokenAInfo().decimals;
  const tokenBDecimals = whirlpool.getTokenBInfo().decimals;

  // 4. Display position status
  const currentTick = whirlpoolData.tickCurrentIndex;
  const inRange = currentTick >= positionData.tickLowerIndex &&
                  currentTick < positionData.tickUpperIndex;

  const currentPrice = PriceMath.sqrtPriceX64ToPrice(
    whirlpoolData.sqrtPrice,
    tokenADecimals,
    tokenBDecimals,
  );

  console.log(`=== Position Status ===`);
  console.log(`Position: ${POSITION_MINT.toBase58()}`);
  console.log(`Pool: ${positionData.whirlpool.toBase58()}`);
  console.log(`Current price: ${currentPrice.toFixed(6)} (B per A)`);
  console.log(`Range: tick [${positionData.tickLowerIndex}, ${positionData.tickUpperIndex}]`);
  console.log(`Status: ${inRange ? "IN RANGE (earning fees)" : "OUT OF RANGE (not earning)"}`);
  console.log(`Liquidity: ${positionData.liquidity.toString()}`);

  // 5. Collect fees (pass true to sync fee accounting first)
  // This updates the position's fee checkpoints against the pool's global fee growth
  // and then collects in a single transaction.
  console.log(`\nPending fees (on-chain, may be stale until collected):`);
  console.log(`  Token A: ${DecimalUtil.fromBN(positionData.feeOwedA, tokenADecimals).toFixed(6)}`);
  console.log(`  Token B: ${DecimalUtil.fromBN(positionData.feeOwedB, tokenBDecimals).toFixed(6)}`);

  if (!CONFIRM) {
    console.log(`\nDry-run only. Re-run with --confirm to broadcast collectFees + collectRewards.`);
    return;
  }
  console.log(`\nCollecting fees (syncing + collecting)...`);
  const collectTx = await position.collectFees(true);
  const txId = await collectTx.buildAndExecute();
  console.log(`Fees collected!`);
  console.log(`Transaction: https://solscan.io/tx/${txId}`);

  // 6. Collect reward emissions (returns TransactionBuilder[])
  console.log(`\n=== Reward Emissions ===`);

  const rewardInfos = whirlpoolData.rewardInfos;
  const activeRewards = rewardInfos.filter(
    (r: any) => r.mint && !r.mint.equals(PublicKey.default)
  );

  if (activeRewards.length > 0) {
    for (let i = 0; i < activeRewards.length; i++) {
      const positionReward = positionData.rewardInfos[i];
      console.log(`Reward ${i}: mint=${activeRewards[i].mint.toBase58().slice(0, 8)}... owed=${positionReward.amountOwed.toString()}`);
    }

    const rewardTxs = await position.collectRewards(undefined, true);
    for (const rtx of rewardTxs) {
      const sig = await rtx.buildAndExecute();
      console.log(`Rewards collected: https://solscan.io/tx/${sig}`);
    }
    if (rewardTxs.length === 0) console.log("No reward amounts owed.");
  } else {
    console.log("This pool has no active reward emissions.");
  }

  console.log(`\nDone.`);
}

main().catch(console.error);
```

## How It Works

1. **Load the position** using its NFT mint address and derive the PDA via `PDAUtil.getPosition()`.
2. **Check position status** -- whether the position is in range and currently earning fees.
3. **Collect trading fees** using `collectFees(true)`. The `true` flag syncs fee accounting first (updates checkpoints against global fee growth) and then collects in one call.
4. **Collect reward emissions** separately using `collectRewards()`. Returns `TransactionBuilder[]` — iterate and execute each. Some pools distribute additional tokens (e.g., ORCA, MNDE) as incentives.

## Important Notes

- **Fees accrue only while in range.** If the position is out of range, no new fees accumulate. Previously earned fees can still be collected.
- **Pass `true` to `collectFees()`** to sync fee accounting first. Without this, `feeOwedA`/`feeOwedB` may be outdated.
- **Fees and rewards are separate calls.** `collectFees()` handles trading fees. `collectRewards()` returns `TransactionBuilder[]` for emission rewards. Execute each.
- **Gas cost.** Each collection requires a transaction (~0.000005 SOL). For small fee amounts, it may be more efficient to batch collections or wait for fees to accumulate.
- **Collection frequency.** Each collection costs ~0.000005 SOL in transaction fees. For small positions, wait for fees to accumulate before collecting.

## Output

> **Requires**: dependencies pinned by the skill, `KEYPAIR_PATH`, `SOLANA_RPC_URL` (optional). Submits an on-chain transaction when re-run with `--confirm`.

Expected output (with keypair):
```
=== Position Status ===
Position: 7hYz...9pLm
Pool: Czfq3xZZ...44zE
Current price: 85.871234 (B per A)
Range: tick [-25608, -23596]
Status: IN RANGE (earning fees)
Liquidity: 58071605

Pending fees (on-chain, may be stale until collected):
  Token A: 0.000134
  Token B: 0.011046

Collecting fees (syncing + collecting)...
Fees collected!
Transaction: https://solscan.io/tx/2mNx...8kTp

=== Reward Emissions ===
This pool has no active reward emissions.
```
