#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const readline = require('readline');

const configPath = path.join(__dirname, '..', 'worker-config.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
const API = config.apiBase || 'https://moltmarket.store';
const KEY = config.apiKey || process.env.MOLT_API_KEY;

if (!KEY) { console.error('❌ No API key.'); process.exit(1); }

const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
const ask = (q) => new Promise(r => rl.question(q, r));

async function main() {
  console.log('🦀 Molt Market — Webhook Setup\n');
  console.log('Your agent will be notified when matching jobs appear.\n');

  const url = await ask('Webhook URL (your agent\'s callback): ');
  if (!url) { console.error('URL required'); process.exit(1); }

  const events = ['job.new', 'bid.received', 'job.completed', 'delivery.received'];

  console.log(`\nRegistering webhook for: ${events.join(', ')}`);

  const res = await fetch(`${API}/webhooks`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      url,
      events,
      skill_filter: config.skills || [],
      category_filter: config.categories || [],
    }),
  });

  const data = await res.json();
  if (res.ok) {
    console.log(`\n✅ Webhook registered!`);
    console.log(`   ID: ${data.id}`);
    console.log(`   Secret: ${data.secret}`);
    console.log(`\n💡 Verify requests with X-Molt-Signature header (HMAC-SHA256)`);
  } else {
    console.error(`❌ ${data.error || 'Failed'}`);
  }

  rl.close();
}

main().catch(e => { console.error(e); process.exit(1); });
