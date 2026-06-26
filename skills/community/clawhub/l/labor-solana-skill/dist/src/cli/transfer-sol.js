import { resolveRpcUrl } from '../config.js';
import { createConnection, inferCluster } from '../connection.js';
import { keypairFromSecretRaw } from '../keypair.js';
import { lamportsToSolString, parsePositiveSolToLamports } from '../amounts.js';
import { transactionExplorerUrl } from '../explorer.js';
import { publicKeyFromBase58, sendNativeTransfer } from '../native-transfer.js';
const USAGE = 'Usage: npm run transfer -- --to <PUBKEY> --sol <AMOUNT> [--rpc URL]';
function parseTransferFlags(argv) {
    let to = null;
    let sol = null;
    let rpc = null;
    for (let i = 2; i < argv.length; i++) {
        const a = argv[i];
        if (a === '--to') {
            if (!argv[i + 1])
                throw new Error('Missing value for --to');
            to = argv[++i];
        }
        else if (a === '--sol') {
            if (!argv[i + 1])
                throw new Error('Missing value for --sol');
            sol = argv[++i];
        }
        else if (a === '--rpc') {
            if (!argv[i + 1])
                throw new Error('Missing value for --rpc');
            rpc = argv[++i];
        }
        else {
            throw new Error(`Unknown argument: ${a}`);
        }
    }
    return { to, sol, rpc };
}
export async function runTransferSolCli(argv, env) {
    let parsedFlags;
    try {
        parsedFlags = parseTransferFlags(argv);
    }
    catch (e) {
        console.error(e instanceof Error ? e.message : String(e));
        console.error(USAGE);
        return 2;
    }
    const { to, sol, rpc: rpcFlag } = parsedFlags;
    if (!to || sol == null) {
        console.error(USAGE);
        return 2;
    }
    const rpcUrl = resolveRpcUrl(env, rpcFlag);
    let recipient;
    try {
        recipient = publicKeyFromBase58(to);
    }
    catch {
        console.error('Invalid recipient address');
        return 1;
    }
    let lamports;
    let amountSolExact;
    try {
        ({ lamports, solExact: amountSolExact } = parsePositiveSolToLamports(sol));
    }
    catch (e) {
        console.error(e instanceof Error ? e.message : String(e));
        return 1;
    }
    const secret = env.SOLANA_PRIVATE_KEY;
    if (!secret) {
        console.error('Missing SOLANA_PRIVATE_KEY');
        return 1;
    }
    let signer;
    try {
        signer = keypairFromSecretRaw(secret);
    }
    catch (e) {
        console.error('Invalid SOLANA_PRIVATE_KEY:', e instanceof Error ? e.message : String(e));
        return 1;
    }
    let connection;
    try {
        connection = createConnection(rpcUrl);
    }
    catch (e) {
        console.error('Invalid RPC URL:', e instanceof Error ? e.message : String(e));
        return 1;
    }
    const cluster = await inferCluster(connection);
    try {
        const { signature, lastValidBlockHeight } = await sendNativeTransfer(connection, {
            signer,
            recipient,
            lamports,
        });
        console.log(JSON.stringify({
            ok: true,
            signature,
            cluster,
            rpcUrl,
            from: signer.publicKey.toBase58(),
            to: recipient.toBase58(),
            lamports,
            sol: amountSolExact,
            solExact: lamportsToSolString(lamports),
            explorerUrl: transactionExplorerUrl(signature, cluster),
            lastValidBlockHeight,
        }));
        return 0;
    }
    catch (e) {
        const maybeErr = e;
        if (maybeErr?.code === 'insufficient_balance') {
            console.error(JSON.stringify({
                error: 'insufficient_balance',
                ...(maybeErr.details ?? {}),
            }));
            return 1;
        }
        console.error(e instanceof Error ? e.message : String(e));
        return 1;
    }
}
