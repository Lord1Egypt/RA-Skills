#!/usr/bin/env node
import { apiRequest, printJson } from './http.js';

const buyerWallet = process.argv[2] || process.env.BUYER_WALLET;
const itemName = process.argv[3] || process.env.ITEM_NAME;
const priceInUsdc = process.argv[4] ?? process.env.PRICE_IN_USDC;
const description = process.argv[5] || process.env.DESCRIPTION || null;
const adId = process.env.AD_ID || undefined;

if (!buyerWallet || !itemName || priceInUsdc === undefined) {
  console.error(
    'Usage: node scripts/create-trade.js <buyerWallet> <itemName> <priceInUsdc> [description]',
  );
  console.error('Env: BUYER_WALLET, ITEM_NAME, PRICE_IN_USDC, optional DESCRIPTION, AD_ID');
  process.exit(1);
}

const body = {
  buyerWallet,
  itemName,
  priceInUsdc: Number(priceInUsdc),
  description,
};
if (adId) {
  body.adId = adId;
}

try {
  const out = await apiRequest('POST', '/api/trades', body);
  printJson(out);
} catch (e) {
  console.error(e.message, e.body ?? '');
  process.exit(1);
}
