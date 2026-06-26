/**
 * Wallet Manager
 * 
 * Usage:
 *   npx tsx scripts/wallet.ts sol
 *   npx tsx scripts/wallet.ts tokens
 *   npx tsx scripts/wallet.ts created
 *   npx tsx scripts/wallet.ts deposit
 *   npx tsx scripts/wallet.ts show
 *   npx tsx scripts/wallet.ts mintto
 */

import { LAMPORTS_PER_SOL, PublicKey, TokenAmount } from '@solana/web3.js'
import { TOKEN_PROGRAM_ID, AccountLayout} from "@solana/spl-token"
import { deriveUserTokenAccount } from "@moria/moria-sdk"
import { loadConfig } from './config.js'
import { fileURLToPath } from 'url'
import QRCode from 'qrcode'
import { getMyTokens, getMyMinttoTokens, Token } from "./lib/index.js"
import { printPrettyTable } from "./util/table.js"
import { Decimal } from "decimal.js"

async function main() {
    const [, , command, ...args] = process.argv;

    const config = loadConfig();
    if (config == null) {
        console.error('请参阅 [BOOTSTRAP.md](BOOTSTRAP.md) 重新初始化。');
        process.exit(1);
    }

    switch (command) {
        case 'show':{
            console.log("当前钱包地址：" + config.wallet.publicKey.toBase58());
            break;
        }
        case 'deposit':{
            const base64 = await QRCode.toDataURL(config.wallet.publicKey.toBase58());

            console.log(`以下是**充值二维码**图片：

                ![qr](${base64})
            `);
            break;
        }

        case 'sol': {
            const lamports = await config.connection.getBalance(config.wallet.publicKey);
            printPrettyTable(['sol', 'lamports'], [[(lamports / LAMPORTS_PER_SOL).toString(), lamports.toString()]]);
            break;
        }
        case 'tokens': {
            const tokenAccounts = await config.connection.getParsedTokenAccountsByOwner(config.wallet.publicKey, {
                programId: TOKEN_PROGRAM_ID
            }).then(res => res.value || []);

            const tokens = tokenAccounts.map((account) => {
                const { mint, tokenAmount } = account.account.data.parsed.info;

                return [
                    mint,
                    (tokenAmount as TokenAmount).uiAmountString,
                    (tokenAmount as TokenAmount).amount,
                ];
                
            }) || [];

            printPrettyTable(['mint', 'balance', 'lamports'], tokens);
            break;
        }
        case 'mintto': {
            const tokens = await getMyMinttoTokens(config.privy_device_id);
            if (tokens == null) {
                printPrettyTable(['balance', 'mint', 'name', 'symbol', 'status', 'process', 'create_timestamp'],[]);
                break;
            }

            var arr = [];

            for (let i = 0; i<tokens.length;i++) {
                const token = tokens[i];

                const ata = deriveUserTokenAccount(new PublicKey(token.mint), config.wallet.publicKey);
                const info = await config.connection.getAccountInfo(ata)
                if (!info) {
                    continue
                }

                const data = AccountLayout.decode(info.data);
                const balance = new Decimal(data.amount.toString()).div(new Decimal(10).pow(9));
                if (balance.toString() == '0') {
                    continue
                }

                const migration_quote_threshold = new Decimal(token.migration_quote_threshold);
                const migration_threshold = new Decimal(token.migration_threshold);

                const value = migration_quote_threshold
                    .mul(new Decimal(100))
                    .div(migration_threshold)

                arr.push([
                    balance.toString(),
                    token.mint, 
                    token.name, 
                    token.symbol, 
                    token.status == 0 ? 'minting' : token.status == 1 ? 'wait migrated' : token.status == 2 ? 'dammv2' : 'end', 
                    (value.isInteger() ? value.toFixed(0) : value.toFixed(2)) + '%',
                    new Date(token.create_timestamp * 1000).toISOString().replace('T', ' ').slice(0, 19) + '(UTC)',
                ]);
            }

            printPrettyTable(
                ['balance','mint', 'name', 'symbol', 'status', 'process', 'create_timestamp'],
                arr,
            );
            break;
        }
        case 'created': {
            const tokens = await getMyTokens(config.privy_device_id);
            if (tokens == null) {
                printPrettyTable(['mint', 'name', 'symbol', 'status', 'process', 'create_timestamp'],[]);
                break;
            }

            printPrettyTable(['mint', 'name', 'symbol', 'status', 'process', 'create_timestamp'], await Promise.all(tokens.map(async (token: Token) => {
                const migration_quote_threshold = new Decimal(token.migration_quote_threshold);
                const migration_threshold = new Decimal(token.migration_threshold);

                const value = migration_quote_threshold
                    .mul(new Decimal(100))
                    .div(migration_threshold)
                return [
                    token.mint,
                    token.name,
                    token.symbol,
                    token.status == 0 ? 'minting' : token.status == 1 ? 'wait migrated' : token.status == 2 ? 'dammv2' : 'end',
                    (value.isInteger() ? value.toFixed(0) : value.toFixed(2)) + '%',
                    new Date(token.create_timestamp * 1000).toISOString().replace('T', ' ').slice(0, 19) + '(UTC)',
                ]

            })));

            break;
        }

        default:
            console.log(`
Wallet Manager

Commands:
  show                                    查询我的钱包
  deposit                                 查看充值二维码
  sol                                     查询账户余额
  tokens                                  查询账户下所有代币
  created                                 获取我创建的代币
  mintto                                  获取我铸造的代币

Examples:
  npx tsx scripts/wallet.ts show
  npx tsx scripts/wallet.ts deposit
  npx tsx scripts/wallet.ts sol
  npx tsx scripts/wallet.ts tokens
  npx tsx scripts/wallet.ts created
  npx tsx scripts/wallet.ts mintto
`);

    }
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
    main().catch(console.error);
}