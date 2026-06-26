/**
 * Swap Manager
 * 
 * Usage:
 *   npx tsx scripts/swap.ts mintto <mint> <copies>
 *   npx tsx scripts/swap.ts refund <mint>
 */

import { PublicKey, sendAndConfirmTransaction, ConfirmOptions } from '@solana/web3.js'
import { ClawlabClient, derivePool, MintToParams, RefundParams } from "@moria/moria-sdk"
import { NATIVE_MINT, TOKEN_PROGRAM_ID } from "@solana/spl-token"
import { CpAmm, Swap2Params, deriveCustomizablePoolAddress, SwapMode } from "@meteora-ag/cp-amm-sdk"

import { loadConfig } from './config.js'
import { fileURLToPath } from 'url'
import { printPrettyTable } from "./util/table.js"
import { BN } from 'bn.js'

const wait_time = 1000 * 60 * 60 * 24;

async function main() {
    const [, , command, mint, copies, ...args] = process.argv;

    const config = loadConfig();
    if (config == null) {
        console.error('请参阅 [BOOTSTRAP.md](BOOTSTRAP.md) 重新初始化。');
        process.exit(1);
    }

    switch (command) {
        case 'mintto': {
            if (mint == undefined || copies == undefined) {
                console.error('Usage: npx tsx scripts/swap.ts mintto <mint> <copies>');
                break;
            }

            const clawlabClient = new ClawlabClient(config.connection);

            const baseMint = new PublicKey(mint);

            const poolAddress = derivePool(
                baseMint,
                NATIVE_MINT,
            );

            const poolState = await clawlabClient.state.getPoolConfig(poolAddress);

            if (poolState.liquidityAdded != 0) {
                console.error(`铸造失败：代币已添加流动性。`);
                break;
            }
            if ((Date.now() - poolState.createdAt.toNumber() * 1000) > wait_time) {
                console.error(`铸造失败：创建时间大于24小时的代币无法铸造。`);
                break;
            }

            const mintToTx = await clawlabClient.pool.MintToTx({
                payer: config.wallet.publicKey,
                baseMint: baseMint,
                copies: new BN(copies),
            } as MintToParams);

            const sig = await sendAndConfirmTransaction(config.connection, mintToTx, [
                config.wallet,
            ]);

            console.log(`✅ mintto token success`);
            printPrettyTable(['Signature'], [[sig]]);
            break;
        }
        case 'refund': {
            if (mint == undefined) {
                console.error('Usage: npx tsx scripts/swap.ts refund <mint>');
                break;
            }

            const clawlabClient = new ClawlabClient(config.connection);

            const baseMint = new PublicKey(mint);

            const poolAddress = derivePool(
                baseMint,
                NATIVE_MINT,
            );

            const poolState = await clawlabClient.state.getPoolConfig(poolAddress);

            if (poolState.liquidityAdded != 0) {
                console.error(`退款失败：代币已添加流动性。`);
                break;
            }
            
            if ((Date.now() - poolState.createdAt.toNumber() * 1000) < wait_time) {
                console.error(`退款失败：创建时间小于24小时的代币无法退款。`);
                break;
            }

            const refundTx = await clawlabClient.pool.RefundTx({
                payer: config.wallet.publicKey,
                baseMint: baseMint,
            } as RefundParams);

            const sig = await sendAndConfirmTransaction(config.connection, refundTx, [
                config.wallet,
            ]);

            console.log(`✅ refund token success`);
            printPrettyTable(['Signature'], [[sig]]);
            break;
        }

        default:
            console.log(`
Swap Manager

Commands:
  mintto <mint> <copies>                                铸造代币
  refund <mint>                                         退款代币

Examples:
  npx tsx scripts/swap.ts mintto Hxxxxxxe 2
  npx tsx scripts/swap.ts refund Hxxxxxxe
`);

    }
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
    main().catch(console.error);
}
