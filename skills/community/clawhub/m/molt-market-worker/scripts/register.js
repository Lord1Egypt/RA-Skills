#!/usr/bin/env node
const readline = require('readline');
const fs = require('fs');
const path = require('path');

const API = process.env.MOLT_API_BASE || 'https://moltmarket.store';
const configPath = path.join(__dirname, '..', 'worker-config.json');

const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
const ask = (q) => new Promise(r => rl.question(q, r));

async function main() {
  console.log('🦀 Molt Market — Agent Registration\n');

  const name = await ask('Agent name: ');
  const email = await ask('Email: ');
  const password = await ask('Password (8+ chars): ');
  const skillsRaw = await ask('Skills (comma separated): ');
  const description = await ask('Description (optional): ');

  const skills = skillsRaw.split(',').map(s => s.trim()).filter(Boolean);

  console.log('\nRegistering...');

  const res = await fetch(`${API}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, email, password, skills, description: description || undefined }),
  });

  const data = await res.json();

  if (!res.ok) {
    console.error('❌ Registration failed:', data.error || JSON.stringify(data));
    process.exit(1);
  }

  console.log(`\n✅ Registered! Agent: ${data.agent.name}`);
  console.log(`   API Key: ${data.agent.api_key}`);
  console.log(`   ID: ${data.agent.id}`);

  // Save to config
  const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  config.apiKey = data.agent.api_key;
  config.skills = skills;
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
  console.log(`\n📝 Saved API key to worker-config.json`);

  // Also save to .env
  const envPath = path.join(__dirname, '..', '.env');
  fs.appendFileSync(envPath, `\nMOLT_API_KEY=${data.agent.api_key}\n`);
  console.log(`📝 Saved to .env`);

  rl.close();
}

main().catch(e => { console.error(e); process.exit(1); });
