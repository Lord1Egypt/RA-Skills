# Close Position (Anchor Fallback, Token-2022 Safe)

Full position close using raw Anchor instructions. Works for:
- Classic Token pools (SOL/USDC)
- Token-2022 pools (USDG, PYUSD, cbBTC)
- Mixed pools (USDG/USDC, one side classic + one side Token-2022)
- Positions with NFT minted on Token-2022 (`positionWithTokenExtensions`)

Use this pattern when:
- The high-level `whirlpool.closePosition()` / `position.collectFees()` helpers fail (SDK version mismatch)
- You need to close a position on a Token-2022 pool — the V1 helpers may not handle the V2 instructions

> **Playbooks**: [Close Position](../SKILL.md#close-position) (standard flow via SDK helpers) and [Raw Anchor Fallback](../SKILL.md#raw-anchor-fallback) (what this example actually uses). V1 → V2 instruction map lives in [Token-2022 Pools](../SKILL.md#token-2022-pools).

## Full Example

```typescript
import {
  Connection, Keypair, PublicKey, Transaction, ComputeBudgetProgram,
  sendAndConfirmTransaction,
} from "@solana/web3.js";
import {
  TOKEN_PROGRAM_ID, TOKEN_2022_PROGRAM_ID,
  getAssociatedTokenAddressSync,
  createAssociatedTokenAccountIdempotentInstruction,
} from "@solana/spl-token";
// Named imports for AnchorProvider/Wallet work in both CJS and ESM. Import BN
// from bn.js directly — `import { BN } from "@coral-xyz/anchor"` is unreliable
// across module systems.
import { AnchorProvider, Wallet } from "@coral-xyz/anchor";
import BN from "bn.js";
import {
  WhirlpoolContext, ORCA_WHIRLPOOL_PROGRAM_ID, PDAUtil,
} from "@orca-so/whirlpools-sdk";
import * as fs from "fs";

const RPC = process.env.SOLANA_RPC_URL || "https://api.mainnet-beta.solana.com";
const KEYPAIR_PATH = process.env.KEYPAIR_PATH ?? (() => {
  throw new Error("KEYPAIR_PATH environment variable is required.");
})();
const CONFIRM = process.argv.includes("--confirm");
const POSITION_MINT = new PublicKey("YOUR_POSITION_MINT_HERE");

// Look up which token program owns a given mint (classic vs Token-2022)
async function getMintOwner(conn: Connection, mint: PublicKey): Promise<PublicKey> {
  const info = await conn.getAccountInfo(mint);
  if (!info) throw new Error(`mint ${mint.toBase58()} not found`);
  return info.owner; // TOKEN_PROGRAM_ID or TOKEN_2022_PROGRAM_ID
}

async function main() {
  const secret = JSON.parse(fs.readFileSync(KEYPAIR_PATH, "utf-8"));
  const kp = Keypair.fromSecretKey(Uint8Array.from(secret));
  const conn = new Connection(RPC, "confirmed");
  const provider = new AnchorProvider(conn, new Wallet(kp), { commitment: "confirmed" });
  const ctx = WhirlpoolContext.withProvider(provider);
  const owner = kp.publicKey;

  // 1. Fetch position and whirlpool via raw Anchor (no client wrapper)
  // PDAUtil.getPosition works for both classic and Token-2022 positions —
  // the PDA seeds use only the mint, not the token program.
  const posPda = PDAUtil.getPosition(ORCA_WHIRLPOOL_PROGRAM_ID, POSITION_MINT).publicKey;
  const position: any = await (ctx.program.account as any).position.fetch(posPda);

  const whirlpoolKey = position.whirlpool as PublicKey;
  const whirlpool = await (ctx.program.account as any).whirlpool.fetch(whirlpoolKey);

  const tokenA = whirlpool.tokenMintA as PublicKey;
  const tokenB = whirlpool.tokenMintB as PublicKey;
  const vaultA = whirlpool.tokenVaultA as PublicKey;
  const vaultB = whirlpool.tokenVaultB as PublicKey;
  const tickSpacing: number = whirlpool.tickSpacing;

  // 2. Look up each mint's token program (classic vs Token-2022)
  const [tokenProgA, tokenProgB, positionMintOwner] = await Promise.all([
    getMintOwner(conn, tokenA),
    getMintOwner(conn, tokenB),
    getMintOwner(conn, POSITION_MINT),
  ]);

  // 3. Derive tick array PDAs from position range
  const tickArrayLower = PDAUtil.getTickArrayFromTickIndex(
    position.tickLowerIndex, tickSpacing, whirlpoolKey, ORCA_WHIRLPOOL_PROGRAM_ID,
  ).publicKey;
  const tickArrayUpper = PDAUtil.getTickArrayFromTickIndex(
    position.tickUpperIndex, tickSpacing, whirlpoolKey, ORCA_WHIRLPOOL_PROGRAM_ID,
  ).publicKey;

  // 4. ATA addresses (use correct token program per mint)
  const positionTokenAccount = getAssociatedTokenAddressSync(POSITION_MINT, owner, false, positionMintOwner);
  const ataA = getAssociatedTokenAddressSync(tokenA, owner, false, tokenProgA);
  const ataB = getAssociatedTokenAddressSync(tokenB, owner, false, tokenProgB);

  console.log("Position mint :", POSITION_MINT.toBase58());
  console.log("Position PDA  :", posPda.toBase58());
  console.log("Token A prog  :", tokenProgA.toBase58().slice(0, 8) + "...");
  console.log("Token B prog  :", tokenProgB.toBase58().slice(0, 8) + "...");
  console.log("NFT prog      :", positionMintOwner.toBase58().slice(0, 8) + "...");
  console.log("Liquidity     :", position.liquidity.toString());

  // 5. Build transaction
  const tx = new Transaction();
  tx.add(ComputeBudgetProgram.setComputeUnitLimit({ units: 600_000 }));
  tx.add(ComputeBudgetProgram.setComputeUnitPrice({ microLamports: 50_000 }));

  // Ensure destination ATAs exist (pass correct token program per mint)
  tx.add(createAssociatedTokenAccountIdempotentInstruction(owner, ataA, owner, tokenA, tokenProgA));
  tx.add(createAssociatedTokenAccountIdempotentInstruction(owner, ataB, owner, tokenB, tokenProgB));

  // Sync fees and rewards (required before collect — high-level helpers do this automatically).
  // `whirlpool` is auto-resolved from `position` via Anchor relations; don't pass it.
  tx.add(await ctx.program.methods
    .updateFeesAndRewards()
    .accounts({ position: posPda, tickArrayLower, tickArrayUpper })
    .instruction());

  // V2 collect fees (works for both classic and Token-2022 sides).
  // `whirlpool` (relations:[position]) and `memoProgram` (address-constrained)
  // are auto-resolved by Anchor — omit them.
  tx.add(await ctx.program.methods
    .collectFeesV2(null)
    .accounts({
      positionAuthority: owner,
      position: posPda,
      positionTokenAccount,
      tokenMintA: tokenA,
      tokenMintB: tokenB,
      tokenOwnerAccountA: ataA,
      tokenVaultA: vaultA,
      tokenOwnerAccountB: ataB,
      tokenVaultB: vaultB,
      tokenProgramA: tokenProgA,
      tokenProgramB: tokenProgB,
    })
    .remainingAccounts([])
    .instruction());

  // V2 decrease liquidity to 0. Same auto-resolution as above.
  tx.add(await ctx.program.methods
    .decreaseLiquidityV2(position.liquidity, new BN(0), new BN(0), null)
    .accounts({
      tokenProgramA: tokenProgA,
      tokenProgramB: tokenProgB,
      positionAuthority: owner,
      position: posPda,
      positionTokenAccount,
      tokenMintA: tokenA,
      tokenMintB: tokenB,
      tokenOwnerAccountA: ataA,
      tokenOwnerAccountB: ataB,
      tokenVaultA: vaultA,
      tokenVaultB: vaultB,
      tickArrayLower,
      tickArrayUpper,
    })
    .remainingAccounts([])
    .instruction());

  // Close position. The instruction's `tokenProgram` is hardcoded per-variant:
  //   - `closePosition` only accepts classic SPL position NFTs
  //   - `closePositionWithTokenExtensions` is the Token-2022 variant
  // Branch on the position NFT's token program.
  // `position` PDA is auto-derived from `positionMint` — omit it.
  if (positionMintOwner.equals(TOKEN_PROGRAM_ID)) {
    tx.add(await ctx.program.methods
      .closePosition()
      .accounts({
        positionAuthority: owner,
        receiver: owner,
        positionMint: POSITION_MINT,
        positionTokenAccount,
      })
      .instruction());
  } else {
    tx.add(await ctx.program.methods
      .closePositionWithTokenExtensions()
      .accounts({
        positionAuthority: owner,
        receiver: owner,
        positionMint: POSITION_MINT,
        positionTokenAccount,
      })
      .instruction());
  }

  const { blockhash } = await conn.getLatestBlockhash("confirmed");
  tx.recentBlockhash = blockhash;
  tx.feePayer = owner;

  // Simulate first
  const sim = await conn.simulateTransaction(tx);
  if (sim.value.err) {
    console.error("Simulation failed:", sim.value.err);
    sim.value.logs?.forEach(l => console.log("  " + l));
    process.exit(1);
  }
  console.log("Simulation OK.");

  // Gated send
  if (!CONFIRM) {
    console.log("\nDry-run only. Re-run with --confirm to broadcast the close.");
    return;
  }
  const sig = await sendAndConfirmTransaction(conn, tx, [kp], { commitment: "confirmed" });
  console.log("TX: https://solscan.io/tx/" + sig);
}

main().catch((e) => { console.error("Error:", e.message || e); process.exit(1); });
```

## How It Works

1. **Fetch accounts via raw Anchor** — bypasses `client.getPosition()` which requires a matching SDK version and can fail with `ctx.fetcher.getPosition is not a function`.
2. **`PDAUtil.getPosition` works for both classic and Token-2022 positions** — the PDA seeds only use the mint. What differs is the position NFT's token program (step 5).
3. **Look up every mint's token program dynamically** — the pool's token A, token B, and the position NFT can each be on classic Token or Token-2022.
4. **Use V2 instructions** — `collectFeesV2`, `decreaseLiquidityV2` support mixed token programs via explicit `tokenProgramA`/`tokenProgramB` accounts and the memo program.
5. **Pass the position NFT's actual token program** to `closePosition` — NOT `TOKEN_PROGRAM_ID` as a constant. Newer positions use Token-2022 for the NFT.
6. **Two separate instructions for fees**: `updateFeesAndRewards` then `collectFeesV2`. The high-level `position.collectFees(true)` bundles them, but the on-chain program has them as distinct instructions.
7. **Create ATAs idempotently** with the correct token program per mint — not all tokens share the same program.

## Notes

- This pattern is more verbose than the high-level helpers but is robust across SDK versions and works for every Whirlpool regardless of token program.
- For pools where both sides are classic Token, V2 instructions still work — you can use them universally. No downside.
- The compute budget is bumped to 600k units because V2 instructions with Token-2022 checks cost more CU than V1.
- Priority fee (`setComputeUnitPrice`) helps the transaction land during congestion.
