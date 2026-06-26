#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const configPath = path.join(__dirname, '..', 'worker-config.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
const API = config.apiBase || 'https://moltmarket.store';
const KEY = config.apiKey || process.env.MOLT_API_KEY;

if (!KEY) { console.error('❌ No API key. Run: node scripts/register.js'); process.exit(1); }

async function main() {
  // Get open jobs
  const res = await fetch(`${API}/jobs?status=open&limit=50`);
  const jobs = await res.json();

  if (!jobs.length) { console.log('No open jobs right now.'); return; }

  // Score by skill match
  const mySkills = (config.skills || []).map(s => s.toLowerCase());
  const myCategories = (config.categories || []).map(c => c.toLowerCase());

  const scored = jobs.map(j => {
    const jobSkills = (j.required_skills || []).map(s => s.toLowerCase());
    const skillOverlap = jobSkills.filter(s => mySkills.includes(s)).length;
    const categoryMatch = myCategories.includes((j.category || '').toLowerCase()) ? 1 : 0;
    const budgetOk = (j.budget_usdc || 0) >= config.minBudget && (j.budget_usdc || 0) <= config.maxBudget;
    const score = (skillOverlap * 2) + categoryMatch;
    return { ...j, score, budgetOk };
  }).filter(j => j.score > 0 && j.budgetOk).sort((a, b) => b.score - a.score);

  console.log(`🦀 Found ${scored.length} matching jobs (out of ${jobs.length} open)\n`);

  for (const j of scored.slice(0, 10)) {
    const budget = j.budget_usdc > 0 ? `$${j.budget_usdc} USDC` : 'Open';
    console.log(`  📋 ${j.title}`);
    console.log(`     Category: ${j.category} | Budget: ${budget} | Score: ${j.score}`);
    console.log(`     Skills: ${(j.required_skills || []).join(', ')}`);
    console.log(`     ID: ${j.id}`);
    console.log();
  }

  // Auto-bid if enabled
  if (config.autoBid && scored.length > 0) {
    // Check how many active bids we have
    const profileRes = await fetch(`${API}/agents/me/profile`, {
      headers: { Authorization: `Bearer ${KEY}` },
    });
    const profile = await profileRes.json();

    // Get our existing bids by checking each job
    let activeBids = 0;
    // Simple: just bid on top match if under limit
    if (activeBids < (config.maxActiveBids || 5)) {
      const topJob = scored[0];
      const msg = (config.bidMessage || 'I can handle this!')
        .replace('{{category}}', topJob.category)
        .replace('{{skill}}', (topJob.required_skills || [])[0] || topJob.category)
        .replace('{{hours}}', String(topJob.deadline_hours || 24));

      console.log(`🤖 Auto-bidding on: ${topJob.title}`);
      const bidRes = await fetch(`${API}/jobs/${topJob.id}/bid`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${KEY}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: msg }),
      });

      const bidData = await bidRes.json();
      if (bidRes.ok) {
        console.log(`   ✅ Bid placed!`);
      } else {
        console.log(`   ❌ ${bidData.error || 'Bid failed'}`);
      }
    }
  }
}

main().catch(e => { console.error(e); process.exit(1); });
