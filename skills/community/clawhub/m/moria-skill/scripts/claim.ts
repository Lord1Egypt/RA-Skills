/**
 * Claim Manager
 * 
 * Usage:
 *   npx tsx scripts/claim.ts fee <mint>
 *   npx tsx scripts/claim.ts token <mint>
 */

import { PublicKey, sendAndConfirmTransaction, ConfirmOptions } from '@solana/web3.js'
import { ClawlabClient, derivePool, deriveUserTokenAccount, ClaimFeeParams, ClaimTokenParams } from "@moria/moria-sdk"
import { NATIVE_MINT, AccountLayout } from "@solana/spl-token"

import { loadConfig } from './config.js'
import { fileURLToPath } from 'url'
import { printPrettyTable } from "./util/table.js"
import { BN } from 'bn.js'

import { Decimal } from "decimal.js"


async function main() {
    const [, , command, mint, ...args] = process.argv;

    const config = loadConfig();
    if (config == null) {
        console.error('请参阅 [BOOTSTRAP.md](BOOTSTRAP.md) 重新初始化。');
        process.exit(1);
    }

    switch (command) {
        case 'fee': {
            if (mint == undefined) {
                console.error('Usage: npx tsx scripts/claim.ts fee <mint>');
                break;
            }

            const clawlabClient = new ClawlabClient(config.connection);

            const baseMint = new PublicKey(mint);

            const poolAddress = derivePool(
                baseMint,
                NATIVE_MINT,
            );

            const poolState = await clawlabClient.state.getPoolConfig(poolAddress);

            if (poolState.creatorFee.toString() == '0' && poolState.creator != config.wallet.publicKey) {
                console.log("没有可领取的手续费")
                break;
            }

            const claimTx = await clawlabClient.creator.ClaimFeeTx({
                payer: config.wallet.publicKey,
                baseMint: baseMint,
            } as ClaimFeeParams);

            const sig = await sendAndConfirmTransaction(
                config.connection,
                claimTx,
                [config.wallet],
                { commitment: 'finalized' } as ConfirmOptions,
            );

            const fee = new Decimal(poolState.creatorFee.toString()).div(new Decimal(10).pow(9));
            console.log(`✅ claim fee success`);
            printPrettyTable(['balance', 'Signature'], [[`${fee.toFixed(2)} SOL`, sig]]);
            break;
        }
        case 'token': {
            if (mint == undefined) {
                console.error('Usage: npx tsx scripts/claim.ts token <mint>');
                break;
            }

            const clawlabClient = new ClawlabClient(config.connection);

            
            const baseMint = new PublicKey(mint);

            const poolAddress = derivePool(
                baseMint,
                NATIVE_MINT,
            );

            const poolState = await clawlabClient.state.getPoolConfig(poolAddress);

            if (poolState.liquidityAdded == 0) {
                console.error(`领取失败：代币未增加流动性，等代币增加流动性后再进行领取。`);
                break;
            }

            const ata = deriveUserTokenAccount(baseMint, config.wallet.publicKey);

            const info = await config.connection.getAccountInfo(ata)
            if (!info) {
                console.error(`领取失败：未持有该代币。`);
                break;
            }

            const data = AccountLayout.decode(info.data);

            const balance = new Decimal(data.amount.toString()).div(new Decimal(10).pow(9));

            if (balance.toString() == '0') {
                console.error(`领取失败：未持有该代币。`);
                break;
            }

            const claimTx = await clawlabClient.user.ClaimTokenTx({
                payer: config.wallet.publicKey,
                baseMint: baseMint,
            } as ClaimTokenParams);

            const sig = await sendAndConfirmTransaction(
                config.connection,
                claimTx,
                [config.wallet],
                { commitment: 'finalized' } as ConfirmOptions,
            );

            console.log(`✅ claim token success`);
            printPrettyTable(['token(mint)','balance', 'Signature'], [[baseMint.toBase58(),`${balance.toFixed(2)}`, sig]]);

            break;
        }

        default:
            console.log(`
Claim Manager

Commands:
  fee <mint>                                  创作者领取手续费
  token <mint>                                领取代币

Examples:
  npx tsx scripts/claim.ts fee Hxxxxxxe
  npx tsx scripts/claim.ts token Hxxxxxxe
`);

    }
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
    main().catch(console.error);
}
