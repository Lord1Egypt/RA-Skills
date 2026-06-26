#!/usr/bin/env node
/**
 * Government Permit Scraper Pipeline
 * Scrape permits → Filter → Enrich with emails → Auto-email outreach
 *
 * Usage:
 *   node permit-pipeline.js --source tabc --since 2026-03-01
 *   node permit-pipeline.js --source tabc --since 2026-03-01 --dry-run
 *
 * Environment:
 *   BRAVE_API_KEY   — Brave Search (for enrichment)
 *   RESEND_API_KEY  — Resend (for sending emails)
 *   DEEPCRAWL_KEY   — DeepCrawl API (optional, improves enrichment)
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const configPath = path.join(__dirname, 'config.json');
const config = fs.existsSync(configPath) ? JSON.parse(fs.readFileSync(configPath, 'utf8')) : {};

const BRAVE_KEY = process.env.BRAVE_API_KEY;
const RESEND_KEY = process.env.RESEND_API_KEY;
const DRY_RUN = process.argv.includes('--dry-run');

function parseArgs() {
  const args = { source: 'tabc', since: new Date(Date.now() - 30*86400000).toISOString().split('T')[0] };
  for (let i = 2; i < process.argv.length; i++) {
    if (process.argv[i] === '--source') args.source = process.argv[++i];
    if (process.argv[i] === '--since') args.since = process.argv[++i];
  }
  return args;
}

function httpGet(url, headers = {}) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    https.get({ hostname: u.hostname, path: u.pathname + u.search, headers: { 'User-Agent': 'Mozilla/5.0', ...headers } }, res => {
      let d = ''; res.on('data', c => d += c);
      res.on('end', () => resolve({ status: res.statusCode, data: d }));
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
    req.on('error', reject); req.write(data); req.end();
  });
}

// Data source scrapers
const SOURCES = {
  tabc: {
    name: 'Texas TABC Liquor Licenses',
    async scrape(since) {
      const url = 'https://www.tabc.texas.gov/public-information/new-permits-issued/';
      console.log('📡 Scraping TABC permits since', since);
      const res = await httpGet(url);
      // Parse HTML table for permits
      const permits = [];
      const rows = res.data.match(/<tr[^>]*>[\s\S]*?<\/tr>/gi) || [];
      for (const row of rows) {
        const cells = row.match(/<td[^>]*>([\s\S]*?)<\/td>/gi) || [];
        if (cells.length >= 4) {
          const clean = c => c.replace(/<[^>]+>/g, '').trim();
          permits.push({
            business: clean(cells[0]),
            permitType: clean(cells[1]),
            address: clean(cells[2]),
            city: cells[3] ? clean(cells[3]) : '',
            date: cells[4] ? clean(cells[4]) : '',
          });
        }
      }
      return permits;
    },
    filterExclude: ['distributor', 'manufacturer', 'wholesaler', 'carrier']
  },

  // Template for other sources — customize for your state
  custom: {
    name: 'Custom Permit Source',
    async scrape(since) {
      console.log('📡 Custom source — edit SOURCES.custom.scrape() with your URL and parsing logic');
      return [];
    },
    filterExclude: []
  }
};

// Filter permits
function filterPermits(permits, source) {
  const exclude = source.filterExclude || [];
  return permits.filter(p => {
    const type = (p.permitType || '').toLowerCase();
    return !exclude.some(kw => type.includes(kw));
  });
}

// Enrich with email via Brave Search
async function enrichWithEmail(business, city) {
  if (!BRAVE_KEY) return null;
  try {
    const query = encodeURIComponent(`${business} ${city} email contact`);
    const url = `https://api.search.brave.com/res/v1/web/search?q=${query}&count=3`;
    const res = await httpGet(url, { 'X-Subscription-Token': BRAVE_KEY, 'Accept': 'application/json' });
    const json = JSON.parse(res.data);
    // Look for emails in descriptions and URLs
    const text = (json.web?.results || []).map(r => r.description + ' ' + r.url).join(' ');
    const emailMatch = text.match(/[\w.+-]+@[\w-]+\.[\w.]+/g);
    if (emailMatch) {
      const filtered = emailMatch.filter(e =>
        !e.includes('example.com') && !e.includes('google.com') &&
        !e.includes('facebook.com') && !e.includes('yelp.com')
      );
      return filtered[0] || null;
    }
  } catch (e) { /* skip */ }
  return null;
}

// Send outreach email
async function sendEmail(to, businessName, city) {
  const template = config.emailTemplate || {
    subject: `Congrats on your new license, ${businessName}!`,
    body: `Hi,\n\nI noticed ${businessName} in ${city} recently received a new permit — congratulations!\n\nI work with newly licensed businesses to help them get set up with the right coverage and services from day one.\n\nWould you have 5 minutes for a quick call this week?\n\nBest,\n${config.fromName || 'Your Name'}`
  };

  if (DRY_RUN) {
    console.log(`  [DRY RUN] Would email ${to}: ${template.subject}`);
    return true;
  }

  if (!RESEND_KEY) { console.log('  ⚠️ No RESEND_API_KEY — skipping'); return false; }

  const res = await httpPost('https://api.resend.com/emails', {
    from: `${config.fromName || 'Outreach'} <${config.fromEmail || 'hello@yourdomain.com'}>`,
    to: [to],
    subject: template.subject.replace('{business_name}', businessName),
    text: template.body.replace('{business_name}', businessName).replace('{city}', city)
  }, { 'Authorization': 'Bearer ' + RESEND_KEY });

  return res.status < 300;
}

// CSV output
function saveToCSV(leads, filename) {
  const header = 'Business,Permit Type,Address,City,Email,Status,Date\n';
  const rows = leads.map(l =>
    `"${l.business}","${l.permitType}","${l.address}","${l.city}","${l.email || ''}","${l.status}","${l.date}"`
  ).join('\n');
  fs.writeFileSync(filename, header + rows);
  console.log(`\n💾 Saved ${leads.length} leads to ${filename}`);
}

// Main pipeline
async function main() {
  const args = parseArgs();
  const source = SOURCES[args.source] || SOURCES.custom;

  console.log(`\n🏛️  ${source.name} Pipeline\n`);

  // Scrape
  const raw = await source.scrape(args.since);
  console.log(`📋 Raw permits: ${raw.length}`);

  // Filter
  const filtered = filterPermits(raw, source);
  console.log(`🔍 After filtering: ${filtered.length}`);

  // Enrich & Email
  const leads = [];
  let emailed = 0;
  for (const permit of filtered) {
    const email = await enrichWithEmail(permit.business, permit.city);
    const lead = { ...permit, email, status: email ? 'enriched' : 'no-email' };

    if (email) {
      const sent = await sendEmail(email, permit.business, permit.city);
      if (sent) { lead.status = 'emailed'; emailed++; }
      console.log(`  📧 ${permit.business}: ${email} ${sent ? '✅' : '❌'}`);
    }
    leads.push(lead);
  }

  // Save
  saveToCSV(leads, `permits-${args.source}-${new Date().toISOString().split('T')[0]}.csv`);

  console.log(`\n📊 Results: ${filtered.length} permits, ${leads.filter(l=>l.email).length} enriched, ${emailed} emailed`);
}

main().catch(e => { console.error('Pipeline error:', e.message); process.exit(1); });
