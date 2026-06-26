#!/usr/bin/env node
import { apiRequest, printJson } from './http.js';

const tradeId = process.argv[2] || process.env.TRADE_ID;
const txSignature = process.argv[3] || process.env.TX_SIGNATURE;
if (!tradeId || !txSignature) {
  console.error('Usage: node scripts/submit-deposit-sig.js <tradeId> <txSignature>');
  process.exit(1);
}

try {
  const out = await apiRequest('POST', `/api/trades/${encodeURIComponent(tradeId)}/deposit-signature`, {
    txSignature,
  });
  printJson(out);
} catch (e) {
  console.error(e.message, e.body ?? '');
  process.exit(1);
}
