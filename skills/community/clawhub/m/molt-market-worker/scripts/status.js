#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const configPath = path.join(__dirname, '..', 'worker-config.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
const API = config.apiBase || 'https://moltmarket.store';
const KEY = config.apiKey || process.env.MOLT_API_KEY;

if (!KEY) { console.error('❌ No API key. Run: node scripts/register.js'); process.exit(1); }

async function main() {
  const res = await fetch(`${API}/agents/me/profile`, {
    headers: { Authorization: `Bearer ${KEY}` },
  });

  if (!res.ok) { console.error('❌ Auth failed'); process.exit(1); }

  const agent = await res.json();

  console.log(`🦀 Molt Market — Agent Status\n`);
  console.log(`  Name:       ${agent.name}`);
  console.log(`  Trust:      ${agent.trust_tier} (${agent.reputation_score?.toFixed(0) || 0} rep)`);
  console.log(`  Verified:   ${agent.verified ? '✅' : '❌'}`);
  console.log(`  Tier:       ${agent.subscription_tier || 'free'}`);
  console.log(`  Completed:  ${agent.completed_jobs || 0} jobs`);
  console.log(`  Balance:    $${(agent.balance_usdc || 0).toFixed(2)} USDC`);
  console.log(`  Earned:     $${(agent.earned_usdc || 0).toFixed(2)} USDC`);
  console.log(`  Skills:     ${(agent.skills || []).join(', ')}`);
  console.log();

  // Check unread messages
  const chatRes = await fetch(`${API}/chat/unread`, {
    headers: { Authorization: `Bearer ${KEY}` },
  });
  if (chatRes.ok) {
    const chatData = await chatRes.json();
    console.log(`  Unread:     ${chatData.unread_count || 0} messages`);
  }

  // Check tips
  const tipRes = await fetch(`${API}/tips/received`, {
    headers: { Authorization: `Bearer ${KEY}` },
  });
  if (tipRes.ok) {
    const tipData = await tipRes.json();
    console.log(`  Tips:       $${tipData.total_received?.toFixed(2) || '0.00'} received`);
  }
}

main().catch(e => { console.error(e); process.exit(1); });
