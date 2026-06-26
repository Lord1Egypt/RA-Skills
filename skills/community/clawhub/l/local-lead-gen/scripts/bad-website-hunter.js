#!/usr/bin/env node
/**
 * Bad Website Hunter — Local Lead Gen Pipeline
 * Scans businesses by niche + city, scores websites, emails pitches to bad ones.
 *
 * Usage:
 *   node bad-website-hunter.js --niche "restaurants" --city "Austin TX" --limit 20
 *   node bad-website-hunter.js --niche "auto repair" --city "Corsicana TX" --dry-run
 *
 * Environment:
 *   BRAVE_API_KEY   — Brave Search API key (required)
 *   RESEND_API_KEY  — Resend email API key (required for sending)
 *   DEEPCRAWL_KEY   — DeepCrawl API key (optional, improves contact extraction)
 *
 * Config: Edit config.json in the same directory for templates, thresholds, etc.
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// Load config
const configPath = path.join(__dirname, 'config.json');
const config = fs.existsSync(configPath) ? JSON.parse(fs.readFileSync(configPath, 'utf8')) : {};

const BRAVE_KEY = process.env.BRAVE_API_KEY;
const RESEND_KEY = process.env.RESEND_API_KEY;
const DEEPCRAWL_KEY = process.env.DEEPCRAWL_KEY;

const SCORE_THRESHOLD = config.scoreThreshold || 40;
const FROM_EMAIL = config.fromEmail || 'hello@yourdomain.com';
const FROM_NAME = config.fromName || 'Your Name';
const DRY_RUN = process.argv.includes('--dry-run');

function parseArgs() {
  const args = {};
  for (let i = 2; i < process.argv.length; i++) {
    if (process.argv[i] === '--niche') args.niche = process.argv[++i];
    if (process.argv[i] === '--city') args.city = process.argv[++i];
    if (process.argv[i] === '--limit') args.limit = parseInt(process.argv[++i]) || 20;
  }
  return args;
}

function httpGet(url, headers = {}) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    https.get({ hostname: u.hostname, path: u.pathname + u.search, headers: { 'User-Agent': 'Mozilla/5.0', ...headers } }, res => {
      let d = ''; res.on('data', c => d += c);
      res.on('end', () => resolve({ status: res.statusCode, data: d, headers: res.headers }));
    }).on('error', reject);
  });
}

function httpPost(url, body, headers = {}) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const data = JSON.stringify(body);
    const req = https.request({
      hostname: u.hostname, path: u.pathname, method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': data.length, ...headers }
    }, res => {
      let d = ''; res.on('data', c => d += c);
      res.on('end', () => resolve({ status: res.statusCode, data: d }));
    });
    req.on('error', reject);
    req.write(data); req.end();
  });
}

// Step 1: Search businesses via Brave
async function searchBusinesses(niche, city, limit) {
  const query = encodeURIComponent(`${niche} ${city}`);
  const url = `https://api.search.brave.com/res/v1/web/search?q=${query}&count=${Math.min(limit, 20)}`;
  const res = await httpGet(url, { 'X-Subscription-Token': BRAVE_KEY, 'Accept': 'application/json' });
  const json = JSON.parse(res.data);
  return (json.web?.results || []).map(r => ({
    name: r.title, url: r.url, description: r.description
  }));
}

// Step 2: Score a website
async function scoreWebsite(url) {
  const score = { ssl: 0, mobile: 0, speed: 0, design: 0, content: 0, total: 0, issues: [] };
  try {
    const start = Date.now();
    const res = await httpGet(url);
    const elapsed = Date.now() - start;
    const html = res.data;

    // SSL
    if (url.startsWith('https://')) { score.ssl = 20; }
    else { score.issues.push('No SSL/HTTPS'); }

    // Speed
    if (elapsed < 3000) score.speed = 20;
    else if (elapsed < 6000) { score.speed = 10; score.issues.push('Slow load time'); }
    else { score.issues.push('Very slow load time (>' + (elapsed/1000).toFixed(1) + 's)'); }

    // Mobile
    if (html.includes('viewport')) { score.mobile = 20; }
    else { score.issues.push('Not mobile-friendly'); }

    // Design
    if (html.includes('tailwind') || html.includes('bootstrap') || html.includes('flexbox') || html.includes('grid')) {
      score.design = 20;
    } else if (html.includes('<table') && html.includes('bgcolor')) {
      score.issues.push('Outdated table-based layout');
    } else {
      score.design = 10;
    }

    // Content
    const brokenImg = (html.match(/<img[^>]+src=""/g) || []).length;
    const hasCopyright = html.match(/©\s*20[0-2][0-3]/); // old copyright
    if (brokenImg === 0 && !hasCopyright) { score.content = 20; }
    else {
      if (brokenImg > 0) score.issues.push(brokenImg + ' broken images');
      if (hasCopyright) score.issues.push('Outdated copyright year');
      score.content = 10;
    }

    score.total = score.ssl + score.mobile + score.speed + score.design + score.content;
  } catch (e) {
    score.issues.push('Site unreachable: ' + e.message);
    score.total = 0;
  }
  return score;
}

// Step 3: Extract email from website
async function extractEmail(url) {
  try {
    // Try DeepCrawl first if available
    if (DEEPCRAWL_KEY) {
      const dcUrl = `https://api.deepcrawl.dev/read?url=${encodeURIComponent(url)}`;
      const res = await httpGet(dcUrl, { 'Authorization': 'Bearer ' + DEEPCRAWL_KEY });
      const emailMatch = res.data.match(/[\w.+-]+@[\w-]+\.[\w.]+/g);
      if (emailMatch) return emailMatch[0];
      // Try /contact page
      const contactUrl = url.replace(/\/$/, '') + '/contact';
      const res2 = await httpGet(`https://api.deepcrawl.dev/read?url=${encodeURIComponent(contactUrl)}`,
        { 'Authorization': 'Bearer ' + DEEPCRAWL_KEY });
      const emailMatch2 = res2.data.match(/[\w.+-]+@[\w-]+\.[\w.]+/g);
      if (emailMatch2) return emailMatch2[0];
    }

    // Fallback: direct scrape
    const res = await httpGet(url);
    const emailMatch = res.data.match(/[\w.+-]+@[\w-]+\.[\w.]+/g);
    if (emailMatch) {
      // Filter out common false positives
      const filtered = emailMatch.filter(e => !e.includes('example.com') && !e.includes('wixpress') && !e.includes('sentry'));
      if (filtered.length) return filtered[0];
    }
  } catch (e) { /* skip */ }
  return null;
}

// Step 4: Send cold email via Resend
async function sendEmail(to, businessName, issues, city) {
  const issueList = issues.slice(0, 3).join(', ');
  const subject = config.emailSubject?.replace('{business_name}', businessName) || `Quick question about ${businessName}'s website`;
  const body = config.emailBody?.replace('{business_name}', businessName).replace('{issues_found}', issueList).replace('{city}', city) ||
    `Hi,\n\nI was looking at ${businessName}'s website and noticed a few things that might be costing you customers: ${issueList}.\n\nI help local businesses in ${city} modernize their online presence. Would you be open to a quick chat about what an upgrade could look like?\n\nBest,\n${FROM_NAME}`;

  if (DRY_RUN) {
    console.log(`[DRY RUN] Would email ${to}: ${subject}`);
    return true;
  }

  const res = await httpPost('https://api.resend.com/emails', {
    from: `${FROM_NAME} <${FROM_EMAIL}>`,
    to: [to],
    subject,
    text: body
  }, { 'Authorization': 'Bearer ' + RESEND_KEY });

  return JSON.parse(res.data).id ? true : false;
}

// Main pipeline
async function main() {
  const args = parseArgs();
  if (!args.niche || !args.city) {
    console.log('Usage: node bad-website-hunter.js --niche "restaurants" --city "Austin TX" [--limit 20] [--dry-run]');
    process.exit(1);
  }
  if (!BRAVE_KEY) { console.error('Missing BRAVE_API_KEY'); process.exit(1); }

  console.log(`\n🔍 Scanning ${args.niche} in ${args.city} (limit: ${args.limit || 20})...\n`);

  // Search
  const businesses = await searchBusinesses(args.niche, args.city, args.limit || 20);
  console.log(`Found ${businesses.length} businesses\n`);

  const results = { scanned: 0, bad: 0, emailed: 0, leads: [] };

  for (const biz of businesses) {
    results.scanned++;
    const score = await scoreWebsite(biz.url);
    const emoji = score.total < SCORE_THRESHOLD ? '🔴' : score.total < 60 ? '🟡' : '🟢';
    console.log(`${emoji} ${score.total}/100 | ${biz.name} | ${biz.url}`);
    if (score.issues.length) console.log(`   Issues: ${score.issues.join(', ')}`);

    if (score.total < SCORE_THRESHOLD) {
      results.bad++;
      const email = await extractEmail(biz.url);
      if (email) {
        const sent = await sendEmail(email, biz.name, score.issues, args.city);
        if (sent) {
          results.emailed++;
          console.log(`   📧 ${DRY_RUN ? 'Would email' : 'Emailed'}: ${email}`);
        }
      } else {
        console.log(`   ⚠️  No email found`);
      }
      results.leads.push({ ...biz, score: score.total, issues: score.issues, email });
    }
  }

  console.log(`\n📊 Results: ${results.scanned} scanned, ${results.bad} bad sites, ${results.emailed} emailed`);
  console.log(`Leads:`, results.leads.map(l => `${l.name} (${l.score}/100) ${l.email || 'no email'}`).join('\n  '));
}

main().catch(e => { console.error('Pipeline error:', e.message); process.exit(1); });
