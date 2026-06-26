#!/usr/bin/env node
import { apiRequest, printJson } from './http.js';

const tradeId = process.argv[2] || process.env.TRADE_ID;
if (!tradeId) {
  console.error('Usage: node scripts/settle.js <tradeId>');
  process.exit(1);
}

try {
  const out = await apiRequest('POST', `/api/trades/${encodeURIComponent(tradeId)}/settle`);
  printJson(out);
} catch (e) {
  console.error(e.message, e.body ?? '');
  process.exit(1);
}
