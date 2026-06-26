#!/usr/bin/env node
import { apiRequest, printJson } from './http.js';

const tradeId = process.argv[2] || process.env.TRADE_ID;
if (!tradeId) {
  console.error('Usage: node scripts/accept-deposit.js <tradeId>');
  process.exit(1);
}

try {
  const out = await apiRequest('POST', `/api/trades/${encodeURIComponent(tradeId)}/accept`);
  printJson(out);
} catch (e) {
  console.error(e.message, e.body ?? '');
  process.exit(1);
}
