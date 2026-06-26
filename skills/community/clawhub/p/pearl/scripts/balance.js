#!/usr/bin/env node
import { loadConfig, PEARL_HOST } from './io.js';

const config = loadConfig();

const res = await fetch(`${PEARL_HOST}/api/wallet`, { headers: { Authorization: `Bearer ${config.read_token}` } });
const { data, error } = await res.json();
if (error) { console.error(error); process.exit(1); }

const fmt = n => '$' + (n / 100_000_000).toFixed(8).replace(/0+$/, '').replace(/\.$/, '');

console.log(`Balance: ${fmt(data.balance)}`);
console.log(`Per-charge limit: ${data.per_charge_limit ? fmt(data.per_charge_limit) : 'none'}`);
console.log(`Daily limit: ${data.daily_limit ? fmt(data.daily_limit) : 'none'}`);
console.log(`Frozen: ${data.frozen ? 'yes' : 'no'}`);
