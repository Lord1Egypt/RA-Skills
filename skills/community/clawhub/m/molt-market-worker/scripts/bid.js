#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const configPath = path.join(__dirname, '..', 'worker-config.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
const API = config.apiBase || 'https://moltmarket.store';
const KEY = config.apiKey || process.env.MOLT_API_KEY;

if (!KEY) { console.error('❌ No API key.'); process.exit(1); }

const jobId = process.argv[2];
const message = process.argv[3] || config.bidMessage || 'I can handle this!';

if (!jobId) { console.error('Usage: node bid.js <jobId> [message]'); process.exit(1); }

async function main() {
  const res = await fetch(`${API}/jobs/${jobId}/bid`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  });

  const data = await res.json();
  if (res.ok) {
    console.log(`✅ Bid placed on job ${jobId}`);
    console.log(`   Bid ID: ${data.id}`);
  } else {
    console.error(`❌ ${data.error || 'Failed'}`);
  }
}

main().catch(e => { console.error(e); process.exit(1); });
