/**
 * Pool Manager
 * 
 * Usage:
 *   npx tsx scripts/pool.ts create <image_path> <name> <symbol> [description] [twitter] [telegram]
 *   npx tsx scripts/pool.ts mintto
 *   npx tsx scripts/pool.ts dammv2
 */

import { unlink } from "fs/promises";
import { Keypair, sendAndConfirmTransaction, ConfirmOptions } from '@solana/web3.js'
import { ClawlabClient, CreateParams } from "@moria/moria-sdk"

import { loadConfig } from './config.js'
import { fileURLToPath } from 'url'
import { getMintToTokens, getDammV2Tokens, Token } from "./lib/index.js"
import { printPrettyTable } from "./util/table.js"
import { uploadJson, uploadImage } from "./util/ipfs.js"
import { Decimal } from "decimal.js"

function validateSymbol(symbol: string): boolean {
    // 匹配所有汉字
    const chineseChars = symbol.match(/[\u4e00-\u9fa5]/g) || [];
    const chineseCount = chineseChars.length;

    // 总长度（字符数）
    const totalLength = symbol.length;

    // 校验规则
    if (totalLength > 10) return false;
    if (chineseCount > 3) return false;

    return true;
}

async function main() {
    const [, , command, image_path, name, symbol, description, twitter, telegram, ...args] = process.argv;
    const config = loadConfig();
    if (config == null) {
        console.error('请参阅 [BOOTSTRAP.md](BOOTSTRAP.md) 重新初始化。');
        process.exit(1);
    }

    switch (command) {
        case 'create': {
            if (image_path == '' || name == '' || symbol == '') {
                console.error('Usage: npx tsx scripts/pool.ts create <image_path> <name> <symbol> [description] [twitter] [telegram]');
                break;
            }

            if (!validateSymbol(symbol)) {
                console.error('symbol 最长10个字符或3个汉字');
                break;
            }

            let image_uri = '';

            if (image_path.indexOf("/home/node") == 0) {
                try {
                    image_uri = (await uploadImage(image_path)).gatewayUrl;
                    await unlink(image_path);
                } catch (e) {
                    console.error(e);
                    break;
                }
            } else {
                image_uri = image_path
            }

            let metadata = {
                name: name,
                symbol: symbol,
                image: image_uri,
                description: description ?? '',
                website: '',
                twitter: twitter ?? '',
                telegram: telegram ?? '',
            };

            let metadata_url = '';

            try {
                metadata_url = (await uploadJson(name, JSON.stringify(metadata))).gatewayUrl;
            } catch (e) {
                console.error(e);
                break;
            }

            const baseMint = Keypair.generate();

            const clawlabClient = new ClawlabClient(config.connection);

            const createTx = await clawlabClient.pool.CreateTx({
                payer: config.wallet.publicKey,
                baseMint: baseMint.publicKey,
                name: name,
                symbol: symbol,
                uri: metadata_url,
            } as CreateParams);

            const sig = await sendAndConfirmTransaction(
                config.connection,
                createTx,
                [config.wallet, baseMint,],
                { commitment: 'finalized' } as ConfirmOptions,
            );
            console.log(`✅ create success`);
            printPrettyTable(['mint', 'Signature', 'url'], [[baseMint.publicKey.toBase58(), sig, `https://solscan.io/token/${baseMint.publicKey.toBase58()}`]]);
            break;
        }
        case 'mintto': {
            const tokens = await getMintToTokens(config.privy_device_id);
            if (tokens == null) {
                printPrettyTable(['mint', 'name', 'symbol', 'process', 'create_timestamp'], []);
                break;
            }

            printPrettyTable(['mint', 'name', 'symbol', 'process', 'create_timestamp'], await Promise.all(tokens.map(async (token: Token) => {
                const migration_quote_threshold = new Decimal(token.migration_quote_threshold);
                const migration_threshold = new Decimal(token.migration_threshold);

                const value = migration_quote_threshold
                    .mul(new Decimal(100))
                    .div(migration_threshold)

                return [
                    token.mint,
                    token.name,
                    token.symbol,
                    (value.isInteger() ? value.toFixed(0) : value.toFixed(2)) + '%',
                    new Date(token.create_timestamp * 1000).toISOString().replace('T', ' ').slice(0, 19) + '(UTC)',
                ]

            })));

            break;
        }
        case 'dammv2': {
            const tokens = await getDammV2Tokens(config.privy_device_id);
            if (tokens == null) {
                printPrettyTable(['mint', 'name', 'symbol', 'create_timestamp'], []);
                break;
            }

            printPrettyTable(['mint', 'name', 'symbol', 'create_timestamp'], await Promise.all(tokens.map(async (token: Token) => {
                return [
                    token.mint,
                    token.name,
                    token.symbol,
                    new Date(token.create_timestamp * 1000).toISOString().replace('T', ' ').slice(0, 19) + '(UTC)'
                ]
            })));

            break;
        }

        default:
            console.log(`
Pool Manager

Commands:
  create <image_path> <name> <symbol> [description] [twitter] [telegram]      创建代币
  mintto                                                                      获取正在mintto的代币
  dammv2                                                                      获取进入dammv2的代币

Examples:
  npx tsx scripts/pool.ts create /xxx/xxx.png test test
  npx tsx scripts/pool.ts mintto
  npx tsx scripts/pool.ts dammv2
`);

    }
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
    main().catch(console.error);
}