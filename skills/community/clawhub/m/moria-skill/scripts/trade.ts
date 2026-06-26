/**
 * Trade Manager
 * 
 * Usage:
 *   npx tsx scripts/trade.ts buy <mint> <uiAmount>
 *   npx tsx scripts/trade.ts sell <mint> <uiAmount>
 */

import { PublicKey, sendAndConfirmTransaction, ConfirmOptions } from '@solana/web3.js'
import { ClawlabClient, derivePool } from "@moria/moria-sdk"
import { NATIVE_MINT, TOKEN_PROGRAM_ID } from "@solana/spl-token"
import { CpAmm, Swap2Params, deriveCustomizablePoolAddress, SwapMode } from "@meteora-ag/cp-amm-sdk"

import { loadConfig } from './config.js'
import { fileURLToPath } from 'url'
import { printPrettyTable } from "./util/table.js"
import { BN } from 'bn.js'
import { Decimal } from "decimal.js"

const slippage = 1000; // 10%

async function main() {
    const [, , command, mint, uiAmount, ...args] = process.argv;

    const config = loadConfig();
    if (config == null) {
        console.error('请参阅 [BOOTSTRAP.md](BOOTSTRAP.md) 重新初始化。');
        process.exit(1);
    }

    switch (command) {
        case 'buy': {
            if (mint == undefined || uiAmount == undefined) {
                console.error('Usage: npx tsx scripts/trade.ts buy <mint> <uiAmount>');
                break;
            }

            const amountIn = new Decimal(uiAmount).mul(1e+9);

            const clawlabClient = new ClawlabClient(config.connection);

            const baseMint = new PublicKey(mint);

            const poolAddress = derivePool(
                baseMint,
                NATIVE_MINT,
            );

            const poolState = await clawlabClient.state.getPoolConfig(poolAddress);

            if (poolState.liquidityAdded != 1) {
                console.error(`买入失败：代币未添加流动性。`);
                break;
            }

            const cpamm = new CpAmm(config.connection);

            const quoteMint = NATIVE_MINT

            const dammv2_pool = deriveCustomizablePoolAddress(baseMint, quoteMint);

            const dammv2_poolState = await cpamm.fetchPoolState(dammv2_pool);

            const slot = await config.connection.getSlot()

            const blockTime = await config.connection.getBlockTime(slot)

            const currentPoint = new BN(blockTime ?? 0)

            const quote = cpamm.getQuote2({
                inputTokenMint: quoteMint,
                slippage: slippage,
                currentPoint,
                poolState: dammv2_poolState,
                tokenADecimal: 9,
                tokenBDecimal: 9,
                hasReferral: false,
                swapMode: SwapMode.ExactIn,
                amountIn: new BN(amountIn.toString()),
            });

            const minimumAmountOut = quote.minimumAmountOut ?? new BN(0)

            const swap2Params: Swap2Params = {
                payer: config.wallet.publicKey,
                pool: dammv2_pool,
                inputTokenMint: quoteMint,
                outputTokenMint: baseMint,
                tokenAMint: dammv2_poolState.tokenAMint,
                tokenBMint: dammv2_poolState.tokenBMint,
                tokenAVault: dammv2_poolState.tokenAVault,
                tokenBVault: dammv2_poolState.tokenBVault,
                tokenAProgram: TOKEN_PROGRAM_ID,
                tokenBProgram: TOKEN_PROGRAM_ID,
                referralTokenAccount: null,
                poolState: dammv2_poolState,
                swapMode: SwapMode.ExactIn,
                amountIn: new BN(amountIn.toString()),
                minimumAmountOut: minimumAmountOut,
            };
            const swapIx = await cpamm.swap2(swap2Params);

            const sig = await sendAndConfirmTransaction(
                config.connection,
                swapIx,
                [config.wallet],
                { commitment: 'finalized' } as ConfirmOptions,
            );

            console.log(`✅ buy success`);
            printPrettyTable(['Signature'], [[sig]]);
            break;
        }
        case 'sell': {
            if (mint == undefined || uiAmount == undefined) {
                console.error('Usage: npx tsx scripts/trade.ts sell <mint> <uiAmount>');
                break;
            }

            const clawlabClient = new ClawlabClient(config.connection);

            const baseMint = new PublicKey(mint);

            const poolAddress = derivePool(
                baseMint,
                NATIVE_MINT,
            );

            const poolState = await clawlabClient.state.getPoolConfig(poolAddress);

            if (poolState.liquidityAdded != 1) {
                console.error(`卖出失败：代币未添加流动性。`);
                break;
            }

            const amountIn = new Decimal(uiAmount).mul(1e+9);

            const cpamm = new CpAmm(config.connection);

            const quoteMint = NATIVE_MINT

            const dammv2_pool = deriveCustomizablePoolAddress(baseMint, quoteMint);

            const dammv2_poolState = await cpamm.fetchPoolState(dammv2_pool);

            const slot = await config.connection.getSlot()
            const blockTime = await config.connection.getBlockTime(slot)

            const currentPoint = new BN(blockTime ?? 0)

            const quote = cpamm.getQuote2({
                inputTokenMint: baseMint,
                slippage: slippage, // 10%
                currentPoint,
                poolState: dammv2_poolState,
                tokenADecimal: 9,
                tokenBDecimal: 9,
                hasReferral: false,
                swapMode: SwapMode.ExactIn,
                amountIn: new BN(amountIn.toString()),
            });

            const minimumAmountOut = quote.minimumAmountOut ?? new BN(0)

            const swap2Params: Swap2Params = {
                payer: config.wallet.publicKey,
                pool: dammv2_pool,
                inputTokenMint: baseMint,
                outputTokenMint: quoteMint,
                tokenAMint: dammv2_poolState.tokenAMint,
                tokenBMint: dammv2_poolState.tokenBMint,
                tokenAVault: dammv2_poolState.tokenAVault,
                tokenBVault: dammv2_poolState.tokenBVault,
                tokenAProgram: TOKEN_PROGRAM_ID,
                tokenBProgram: TOKEN_PROGRAM_ID,
                referralTokenAccount: null,
                poolState: dammv2_poolState,
                swapMode: SwapMode.ExactIn,
                amountIn: new BN(amountIn.toString()),
                minimumAmountOut: minimumAmountOut,
            };

            const swapIx = await cpamm.swap2(swap2Params);

            const sig = await sendAndConfirmTransaction(
                config.connection,
                swapIx,
                [config.wallet],
                { commitment: 'finalized' } as ConfirmOptions,
            );

            console.log(`✅ sell success`);
            printPrettyTable(['Signature'], [[sig]]);
            break;
        }

        default:
            console.log(`
Trade Manager

Commands:
  buy <mint> <uiAmount>                               买入代币
  sell <mint> <uiAmount>                              卖出代币

Examples:
  npx tsx scripts/trade.ts buy Hxxxxxxe 0.02
  npx tsx scripts/trade.ts sell Hxxxxxxe 1000
`);

    }
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
    main().catch(console.error);
}
