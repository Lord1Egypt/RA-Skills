#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const configPath = path.join(__dirname, '..', 'worker-config.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
const API = config.apiBase || 'https://moltmarket.store';
const KEY = config.apiKey || process.env.MOLT_API_KEY;

if (!KEY) { console.error('❌ No API key.'); process.exit(1); }

const jobId = process.argv[2];
const contentFile = process.argv[3];

if (!jobId) { console.error('Usage: node deliver.js <jobId> [contentFile]'); process.exit(1); }

async function main() {
  let content;
  if (contentFile && fs.existsSync(contentFile)) {
    content = fs.readFileSync(contentFile, 'utf8');
  } else if (contentFile) {
    content = contentFile; // treat as inline content
  } else {
    // Read from stdin
    const chunks = [];
    for await (const chunk of process.stdin) chunks.push(chunk);
    content = Buffer.concat(chunks).toString('utf8');
    if (!content) { console.error('Provide content via file, argument, or stdin'); process.exit(1); }
  }

  const res = await fetch(`${API}/jobs/${jobId}/deliver`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ content }),
  });

  const data = await res.json();
  if (res.ok) {
    console.log(`✅ Delivered work for job ${jobId}`);
    console.log(`   Delivery ID: ${data.id}`);
  } else {
    console.error(`❌ ${data.error || 'Failed'}`);
  }
}

main().catch(e => { console.error(e); process.exit(1); });
