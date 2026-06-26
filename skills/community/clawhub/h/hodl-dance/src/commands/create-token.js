#!/usr/bin/env node
/**
 * Create a new token on HODL.DANCE.
 *
 * Usage:
 *   create-token --name="Token Name" --symbol=SYM --logo=./logo.png
 *
 * Options:
 *   --name          Token name (required)
 *   --symbol        Token symbol (required)
 *   --logo          Path to logo file PNG/JPG/WEBP max 5MB (required)
 *   --category      meme|ai|games|social|other (default: meme)
 *   --description   Token description (max 500 chars)
 *   --website       https://...
 *   --twitter       https://x.com/...
 *   --telegram      https://t.me/...
 *   --initial-buy   BNB amount to buy in same tx (default: 0)
 *
 * Requires: HODL_PRIVATE_KEY env variable
 */
const fs           = require('fs');
const path         = require('path');
const FormData     = require('form-data');
const fetch        = require('node-fetch');
const { ethers }   = require('ethers');
const { getWallet } = require('../lib/chain');
const { ok, err }  = require('../lib/output');

const FACTORY_ADDRESS = '0x99A1F02f56E8356e6E90A880DBb1be6EC7485737';
const FACTORY_ABI = [
  {
    inputs: [
      { name: 'name', type: 'string' },
      { name: 'symbol', type: 'string' }
    ],
    name: 'createTokenAndBondingCurve',
    outputs: [
      { name: 'token', type: 'address' },
      { name: 'bondingCurve', type: 'address' }
    ],
    stateMutability: 'payable',
    type: 'function'
  }
];
const API_BASE   = 'https://hodl.dance/api';
const DEPLOY_FEE = ethers.parseEther('0.0001');

const args  = process.argv.slice(2);
const flags = Object.fromEntries(
  args.filter(a => a.startsWith('--'))
    .map(a => { const [k, v] = a.slice(2).split('='); return [k, v ?? 'true']; })
);

const name        = flags['name'];
const symbol      = flags['symbol'];
const logoPath    = flags['logo'];
const category    = flags['category']    || 'meme';
const description = flags['description'] || '';
const website     = flags['website']     || '';
const twitter     = flags['twitter']     || '';
const telegram    = flags['telegram']    || '';
const initialBuy  = flags['initial-buy'] ? ethers.parseEther(String(flags['initial-buy'])) : 0n;

if (!name)     err('Usage: create-token --name="..." --symbol=... --logo=./logo.png', 'MISSING_ARG');
if (!symbol)   err('Usage: create-token --name="..." --symbol=... --logo=./logo.png', 'MISSING_ARG');
if (!logoPath) err('Usage: create-token --name="..." --symbol=... --logo=./logo.png', 'MISSING_ARG');

const resolvedLogo = path.resolve(logoPath);
if (!fs.existsSync(resolvedLogo)) {
  err(`Logo file not found: ${resolvedLogo}`, 'INVALID_ARG');
}

(async () => {
  const wallet  = getWallet();
  const provider = wallet.provider;

  // 1. Upload metadata + logo
  const form = new FormData();
  form.append('name',        name);
  form.append('symbol',      symbol);
  form.append('description', description);
  form.append('website',     website);
  form.append('twitter',     twitter);
  form.append('telegram',    telegram);
  form.append('creator',     wallet.address);
  form.append('category',    category);
  form.append('logo', fs.createReadStream(resolvedLogo), {
    filename: path.basename(resolvedLogo),
  });

  const uploadRes  = await fetch(`${API_BASE}/token/create`, {
    method: 'POST',
    body: form,
    headers: form.getHeaders(),
  });
  const uploadJson = await uploadRes.json();
  if (!uploadJson.success) {
    err(uploadJson.error || 'Metadata upload failed', 'ERROR');
  }

  // 2. Deploy on-chain
  const factory    = new ethers.Contract(FACTORY_ADDRESS, FACTORY_ABI, wallet);
  const value      = DEPLOY_FEE + initialBuy;
  const deployedAt = Date.now();

  const tx      = await factory.createTokenAndBondingCurve(name, symbol, { value, gasLimit: 1_000_000 });
  const receipt = await tx.wait();

  // 3. Polling API — znajdź nowy token
  let tokenAddress        = null;
  let bondingCurveAddress = null;

  for (let i = 0; i < 15; i++) {
    await new Promise(r => setTimeout(r, i === 0 ? 4000 : 2000));
    const res    = await fetch(`${API_BASE}/tokens?sort=newest&limit=50`);
    const json   = await res.json();
    const tokens = json.data?.tokens || [];
    const found  = tokens.find(t =>
      t.creator?.toLowerCase() === wallet.address.toLowerCase() &&
      new Date(t.created_at).getTime() >= deployedAt - 15000
    );
    if (found) {
      tokenAddress        = found.address;
      bondingCurveAddress = found.bonding_curve_address;
      break;
    }
  }

  ok({
    tx_hash:               receipt.hash,
    block_number:          receipt.blockNumber,
    gas_used:              receipt.gasUsed.toString(),
    token_address:         tokenAddress,
    bonding_curve_address: bondingCurveAddress,
    name,
    symbol,
    category,
    logo_ipfs:             uploadJson.data?.logo || null,
    initial_buy_bnb:       flags['initial-buy']  || '0',
  });
})().catch(e => err(e.message));