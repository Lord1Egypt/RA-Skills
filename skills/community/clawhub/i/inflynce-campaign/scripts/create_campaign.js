#!/usr/bin/env node
/**
 * Create Inflynce Boost campaign via postBoostWeb API.
 * BOOST any link: tweets, project websites, Farcaster casts, etc.
 * Each campaign requires 0.25 USDC (prior payment on Base as proof).
 *
 * Usage:
 *   node create_campaign.js --cast-url URL --payment-hash 0x... --creator-wallet 0x... --budget 50
 */

import { keccak256 } from 'ethereum-cryptography/keccak';

const ALLOWED_GRAPHQL_HOST = 'boost.inflynce.com';

function getLinkIdentifier(urlOrHash) {
  const trimmed = String(urlOrHash || '').trim();
  if (!trimmed) return null;

  // Raw hash
  if (trimmed.startsWith('0x') && /^0x[0-9a-fA-F]{8,64}$/.test(trimmed)) {
    return trimmed;
  }
  // Farcaster/warpcast/base.app URLs - cast hash is in path
  if (trimmed.includes('farcaster.xyz') || trimmed.includes('base.app') || trimmed.includes('warpcast.com')) {
    const parts = trimmed.split('/');
    const last = parts[parts.length - 1];
    if (last?.startsWith('0x') && /^0x[0-9a-fA-F]+$/.test(last)) return last;
  }
  // Any https URL (tweet, website, etc.) - keccak256 of URL (backend requires https://)
  if (trimmed.startsWith('https://')) {
    const buf = new TextEncoder().encode(trimmed);
    const hash = keccak256(buf);
    return '0x' + Buffer.from(hash).toString('hex');
  }
  return null;
}

function parseArgs() {
  const args = process.argv.slice(2);
  const out = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].slice(2).replace(/-/g, '_');
      if (key === 'dry_run') {
        out[key] = 'true';
      } else if (args[i + 1] && !args[i + 1].startsWith('--')) {
        out[key] = args[++i];
      }
    }
  }
  return out;
}

function validateGraphqlUrl(graphqlUrl) {
  let parsed;
  try {
    parsed = new URL(graphqlUrl);
  } catch {
    throw new Error(`Invalid GRAPHQL_URL: "${graphqlUrl}" is not a valid URL.`);
  }
  if (parsed.hostname !== ALLOWED_GRAPHQL_HOST) {
    throw new Error(
      `Untrusted GRAPHQL_URL host: "${parsed.hostname}". Only "${ALLOWED_GRAPHQL_HOST}" is permitted.`
    );
  }
  if (parsed.protocol !== 'https:') {
    throw new Error(`GRAPHQL_URL must use HTTPS. Got: "${parsed.protocol}"`);
  }
}

async function createCampaign(params) {
  const dryRun = params.dry_run === 'true' || params.dry_run === '1';
  const graphqlUrl = params.graphql_url || process.env.GRAPHQL_URL;
  if (!dryRun && !graphqlUrl) throw new Error('GRAPHQL_URL required (env or --graphql-url)');

  // Security: validate GRAPHQL_URL points to the trusted Inflynce endpoint only.
  if (!dryRun) {
    validateGraphqlUrl(graphqlUrl);
  }

  const castUrl = params.cast_url;
  const castHashParam = params.cast_hash;
  const paymentHash = params.payment_hash;
  const creatorWallet = params.creator_wallet;
  const budget = params.budget || params.max_budget || '10';
  const budgetNum = parseFloat(budget);
  if (isNaN(budgetNum) || budgetNum < 5) {
    throw new Error('Minimum budget is 5 USDC');
  }
  const multiplier = parseInt(params.multiplier || '1', 10);

  if (!castUrl || !paymentHash || !creatorWallet) {
    throw new Error('Required: --cast-url, --payment-hash, --creator-wallet');
  }
  if (!/^0x[a-fA-F0-9]{64}$/.test(paymentHash.trim())) {
    throw new Error('payment-hash must be a valid tx hash (0x + 64 hex chars)');
  }

  const castHash = castHashParam || getLinkIdentifier(castUrl);
  if (!castHash) {
    throw new Error('Invalid URL: must be https (tweet, website, cast, etc.) or a raw 0x hash');
  }

  const input = {
    castUrl: castUrl.trim(),
    castHash,
    creatorWallet: creatorWallet.trim(),
    mindshareFilterDuration: 7,
    minMindshare: '0.003', // fixed
    multiplier,
    paymentHash: paymentHash.trim(),
    maxBudget: budget,
    appType: 2, // Agent (OpenClaw skill)
  };

  if (dryRun) {
    return { dryRun: true, input };
  }

  const query = `
    mutation PostBoostWeb($input: PostBoostWebInput!) {
      postBoostWeb(input: $input) {
        id
        boostStatus
        creatorWallet
      }
    }
  `;

  const res = await fetch(graphqlUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, variables: { input } }),
  });

  const json = await res.json();
  if (json.errors) {
    throw new Error(json.errors.map((e) => e.message).join('; '));
  }
  if (!json.data?.postBoostWeb) {
    throw new Error('No postBoostWeb in response');
  }
  return json.data.postBoostWeb;
}

const params = parseArgs();
createCampaign(params)
  .then((r) => console.log(JSON.stringify(r, null, 2)))
  .catch((e) => {
    console.error(e.message);
    process.exit(1);
  });
