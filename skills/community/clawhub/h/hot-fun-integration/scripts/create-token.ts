#!/usr/bin/env node
/**
 * Hot.fun - create token: full flow (API → sign → send).
 *
 * 1. Call hot.fun API to get a base58-encoded Solana transaction
 * 2. Sign the transaction with the wallet private key
 * 3. Send the signed transaction to Solana RPC
 *
 * Usage:
 *   npx hotfun create-token <name> <symbol> <image_url> [options]
 *
 * Options:
 *   --description <desc>        Token description
 *   --x-royalty-party <user>    X (Twitter) username for royalty party
 *
 * Env: PRIVATE_KEY (Solana wallet private key, base58 or JSON array)
 * Optional env: SOLANA_RPC_URL
 */

import {
  Connection,
  Keypair,
  VersionedTransaction,
} from '@solana/web3.js';
import bs58 from 'bs58';
import nacl from 'tweetnacl';

const API_URL = 'https://gate.game.com/v3/hotfun/agent/create_pool_with_config';

function loadKeypair(privateKey: string): Keypair {
  try {
    if (privateKey.startsWith('[')) {
      const arr = JSON.parse(privateKey);
      return Keypair.fromSecretKey(new Uint8Array(arr));
    }
    return Keypair.fromSecretKey(bs58.decode(privateKey));
  } catch {
    throw new Error('Invalid PRIVATE_KEY format. Use base58 string or JSON array of bytes.');
  }
}

function parseArgs(argv: string[]) {
  const positional: string[] = [];
  const options: Record<string, string> = {};
  let i = 0;
  while (i < argv.length) {
    if (argv[i] === '--description' && i + 1 < argv.length) {
      options.description = argv[++i];
    } else if (argv[i] === '--x-royalty-party' && i + 1 < argv.length) {
      options.xRoyaltyParty = argv[++i];
    } else if (!argv[i].startsWith('--')) {
      positional.push(argv[i]);
    }
    i++;
  }
  return { positional, options };
}

async function main() {
  const { positional, options } = parseArgs(process.argv.slice(2));
  const name = positional[0];
  const symbol = positional[1];
  const imageUrl = positional[2];

  if (!name || !symbol || !imageUrl) {
    console.error('Usage: npx hotfun create-token <name> <symbol> <image_url> [options]');
    console.error('Options:');
    console.error('  --description <desc>        Token description');
    console.error('  --x-royalty-party <user>    X (Twitter) username for royalty party');
    console.error('');
    console.error('Example: npx hotfun create-token MyToken MTK "https://example.com/image.png" --description "A cool token" --x-royalty-party "myTwitter"');
    process.exit(1);
  }

  const privateKey = process.env.PRIVATE_KEY;
  if (!privateKey) {
    console.error('Set PRIVATE_KEY (Solana wallet private key, base58 or JSON array)');
    process.exit(1);
  }

  const keypair = loadKeypair(privateKey);
  const payer = keypair.publicKey.toBase58();
  const rpcUrl = process.env.SOLANA_RPC_URL || 'https://api.mainnet-beta.solana.com';
  const connection = new Connection(rpcUrl, 'confirmed');

  // ── Generate agent_ts and agent_sign ──────────────────────────────────
  const agentTs = Math.floor(Date.now() / 1000).toString();
  const agentTsBytes = new TextEncoder().encode(agentTs);
  const signature = nacl.sign.detached(agentTsBytes, keypair.secretKey);
  const agentSign = bs58.encode(signature);

  // ── Step 1: Call API to get transaction ────────────────────────────────
  console.error(`Creating token "${name}" (${symbol}) ...`);
  console.error(`  payer: ${payer}`);
  console.error(`  image_url: ${imageUrl}`);
  if (options.description) console.error(`  description: ${options.description}`);
  if (options.xRoyaltyParty) console.error(`  x_royalty_party: ${options.xRoyaltyParty}`);

  const formData = new FormData();
  formData.append('payer', payer);
  formData.append('name', name);
  formData.append('symbol', symbol);
  formData.append('image_url', imageUrl);
  formData.append('agent_ts', agentTs);
  formData.append('agent_sign', agentSign);
  if (options.description) formData.append('description', options.description);
  if (options.xRoyaltyParty) formData.append('x_royalty_party', options.xRoyaltyParty);

  const res = await fetch(API_URL, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`API request failed: ${res.status} ${res.statusText}\n${text}`);
  }

  const json = await res.json() as {
    data: {
      transaction: string;
      signature: string;
      dbc_config: string;
      dbc_pool: string;
      base_mint: string;
      name: string;
      symbol: string;
      uri: string;
      royalty_party: string;
    };
    common: Record<string, unknown>;
  };

  const { transaction: txBase58, dbc_config, dbc_pool, base_mint, uri } = json.data;

  if (!txBase58) {
    throw new Error('API returned empty transaction. Response: ' + JSON.stringify(json));
  }

  console.error(`  base_mint: ${base_mint}`);
  console.error(`  dbc_config: ${dbc_config}`);
  console.error(`  dbc_pool: ${dbc_pool}`);
  console.error(`  uri: ${uri}`);

  // ── Step 2: Deserialize and sign transaction ──────────────────────────
  const txBytes = bs58.decode(txBase58);
  const tx = VersionedTransaction.deserialize(txBytes);
  tx.sign([keypair]);

  // ── Step 3: Send to Solana RPC ────────────────────────────────────────
  console.error('Sending transaction ...');
  const txHash = await connection.sendRawTransaction(tx.serialize(), {
    skipPreflight: false,
    maxRetries: 3,
  });

  console.error('Confirming ...');
  const confirmation = await connection.confirmTransaction(txHash, 'confirmed');

  if (confirmation.value.err) {
    throw new Error(`Transaction failed: ${JSON.stringify(confirmation.value.err)}`);
  }

  // ── Output ────────────────────────────────────────────────────────────
  const out = {
    txHash,
    wallet: payer,
    baseMint: base_mint,
    dbcConfig: dbc_config,
    dbcPool: dbc_pool,
    name,
    symbol,
    imageUrl,
    uri,
  };
  console.log(JSON.stringify(out, null, 2));
}

main().catch((e) => {
  console.error(e.message || e);
  process.exit(1);
});
