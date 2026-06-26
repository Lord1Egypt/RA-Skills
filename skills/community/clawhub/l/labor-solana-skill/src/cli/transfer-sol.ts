import { resolveRpcUrl } from '../config.js';
import { createConnection, inferCluster } from '../connection.js';
import { keypairFromSecretRaw } from '../keypair.js';
import { lamportsToSolString, parsePositiveSolToLamports } from '../amounts.js';
import { transactionExplorerUrl } from '../explorer.js';
import { publicKeyFromBase58, sendNativeTransfer } from '../native-transfer.js';
import type { Keypair, PublicKey } from '@solana/web3.js';

const USAGE = 'Usage: npm run transfer -- --to <PUBKEY> --sol <AMOUNT> [--rpc URL]';

function parseTransferFlags(argv: string[]): { to: string | null; sol: string | null; rpc: string | null } {
  let to: string | null = null;
  let sol: string | null = null;
  let rpc: string | null = null;

  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--to') {
      if (!argv[i + 1]) throw new Error('Missing value for --to');
      to = argv[++i];
    } else if (a === '--sol') {
      if (!argv[i + 1]) throw new Error('Missing value for --sol');
      sol = argv[++i];
    } else if (a === '--rpc') {
      if (!argv[i + 1]) throw new Error('Missing value for --rpc');
      rpc = argv[++i];
    } else {
      throw new Error(`Unknown argument: ${a}`);
    }
  }

  return { to, sol, rpc };
}

type InsufficientBalanceError = Error & {
  code: 'insufficient_balance';
  details: Record<string, unknown>;
};

export async function runTransferSolCli(argv: string[], env: NodeJS.ProcessEnv): Promise<number> {
  let parsedFlags: { to: string | null; sol: string | null; rpc: string | null };
  try {
    parsedFlags = parseTransferFlags(argv);
  } catch (e) {
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
  let recipient: PublicKey;
  try {
    recipient = publicKeyFromBase58(to);
  } catch {
    console.error('Invalid recipient address');
    return 1;
  }

  let lamports: number;
  let amountSolExact: string;
  try {
    ({ lamports, solExact: amountSolExact } = parsePositiveSolToLamports(sol));
  } catch (e) {
    console.error(e instanceof Error ? e.message : String(e));
    return 1;
  }

  const secret = env.SOLANA_PRIVATE_KEY;
  if (!secret) {
    console.error('Missing SOLANA_PRIVATE_KEY');
    return 1;
  }

  let signer: Keypair;
  try {
    signer = keypairFromSecretRaw(secret);
  } catch (e) {
    console.error('Invalid SOLANA_PRIVATE_KEY:', e instanceof Error ? e.message : String(e));
    return 1;
  }

  let connection;
  try {
    connection = createConnection(rpcUrl);
  } catch (e) {
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

    console.log(
      JSON.stringify({
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
      }),
    );
    return 0;
  } catch (e) {
    const maybeErr = e as Partial<InsufficientBalanceError>;
    if (maybeErr?.code === 'insufficient_balance') {
      console.error(
        JSON.stringify({
          error: 'insufficient_balance',
          ...(maybeErr.details ?? {}),
        }),
      );
      return 1;
    }
    console.error(e instanceof Error ? e.message : String(e));
    return 1;
  }
}
