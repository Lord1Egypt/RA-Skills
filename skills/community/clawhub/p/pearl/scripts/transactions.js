#!/usr/bin/env node
import { loadConfig, PEARL_HOST } from './io.js';

const config = loadConfig();

const limitArg = process.argv.indexOf('--limit');
const limit = limitArg !== -1 ? process.argv[limitArg + 1] : '10';

const res = await fetch(`${PEARL_HOST}/api/transactions?limit=${limit}`, { headers: { Authorization: `Bearer ${config.read_token}` } });
const { data, error } = await res.json();
if (error) { console.error(error); process.exit(1); }

if (data.length === 0) { console.log('No transactions yet.'); process.exit(0); }

const fmt = n => '$' + (n / 100_000_000).toFixed(8).replace(/0+$/, '').replace(/\.$/, '');

for (const tx of data) {
  console.log(`${tx.created_at}  -${fmt(tx.amount)}  ${tx.description}`);
}
