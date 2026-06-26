#!/usr/bin/env node
/**
 * query.js — Smart Money Data Query Tool
 *
 * Usage:
 *   node query.js addr   <address>
 *   node query.js top    <domain> [n] [--label LABEL]
 *   node query.js filter [--label L] [--domain D] [--sort F] [--limit N]
 */
'use strict';

const sm = require('./smartmoney');

const DOMAIN_LABELS = {
  POL: 'Politics', GEO: 'Geopolitics', FIN: 'Finance',
  CRY: 'Crypto', SPT: 'Sports', TEC: 'Tech/AI',
  CUL: 'Entertainment', GEN: 'Generalist',
};
const LABEL_DESC = {
  HUMAN: 'Human Trader', SIGNAL: 'Signal', MM: 'Market Maker',
  BOT: 'Bot', COPYBOT: 'Copy Bot', NOISE: 'Noise',
};

function pct(v)  { return ((v || 0) * 100).toFixed(1) + '%'; }
function roi(v)  { const s = ((v || 0) * 100).toFixed(1); return (v >= 0 ? '+' : '') + s + '%'; }
function pnl(v)  { const r = Math.round(v || 0); return (r >= 0 ? '+$' : '-$') + Math.abs(r).toLocaleString(); }
function usd(v)  { return '$' + Math.round(v || 0).toLocaleString(); }

// ── addr ──────────────────────────────────────────────────────
async function cmdAddr(args, classified) {
  const input = (args[0] || '').toLowerCase();
  if (!input) { console.error('Usage: node query.js addr <address>'); process.exit(1); }

  const key = Object.keys(classified).find(a => a.toLowerCase() === input);
  if (!key) {
    console.log(`Address not found: ${args[0]}`);
    console.log('Hint: This address may not be in the smart money list (below classification threshold)');
    return;
  }
  const v = classified[key];
  const domains = (v.domains || ['GEN']).map(d => `${d}(${DOMAIN_LABELS[d] || d})`).join(' + ');
  console.log('\n' + '═'.repeat(62));
  console.log(`  ${key}`);
  console.log('═'.repeat(62));
  console.log(`  Type       ${v.label} (${LABEL_DESC[v.label] || v.label})`);
  console.log(`  Domains    ${domains}`);
  console.log(`  Total Vol  ${usd(v.total_volume)}`);
  console.log(`  Win Rate   ${pct(v.win_rate)}`);
  console.log(`  Avg ROI    ${roi(v.avg_roi)}`);
  console.log(`  Realized PnL ${pnl(v.realized_pnl)}`);
  console.log(`  Daily Freq ${(v.daily_30d || 0).toFixed(1)} times/day (last 30d)`);
  console.log(`  Markets    ${v.market_count || '-'} markets`);
  console.log('═'.repeat(62) + '\n');
}

// ── top ───────────────────────────────────────────────────────
async function cmdTop(args, classified) {
  const domain = (args[0] || '').toUpperCase();
  if (!domain || !DOMAIN_LABELS[domain]) {
    console.error(`Usage: node query.js top <domain> [n] [--label LABEL]`);
    console.error(`  Available domains: ${Object.keys(DOMAIN_LABELS).join(' / ')}`);
    process.exit(1);
  }

  let n = 10, labelFilter = null;
  for (let i = 1; i < args.length; i++) {
    if (args[i] === '--label' && args[i + 1]) labelFilter = args[++i].toUpperCase();
    else if (!isNaN(Number(args[i])))          n = Number(args[i]);
  }

  const rows = Object.entries(classified)
    .filter(([, v]) => (v.domains || ['GEN']).includes(domain))
    .filter(([, v]) => !labelFilter || v.label === labelFilter)
    .sort((a, b) => (b[1].avg_roi || 0) - (a[1].avg_roi || 0))
    .slice(0, n);

  const labelStr = labelFilter ? `[${labelFilter}] ` : '';
  console.log(`\n  Top ${n} ${labelStr}${domain}(${DOMAIN_LABELS[domain]}) · by ROI\n`);
  console.log('  ' + '─'.repeat(88));
  console.log(
    '  # '.padEnd(5) + 'Address'.padEnd(46) + 'Type'.padEnd(9) +
    'Domain'.padEnd(14) + 'ROI'.padStart(9) + 'Win%'.padStart(8) + 'Realized PnL'.padStart(14)
  );
  console.log('  ' + '─'.repeat(88));
  rows.forEach(([addr, v], i) => {
    const tags = (v.domains || ['GEN']).join('+');
    console.log(
      `  ${String(i + 1).padStart(2)}. `.padEnd(5) +
      addr.padEnd(46) +
      v.label.padEnd(9) +
      tags.padEnd(14) +
      roi(v.avg_roi).padStart(9) +
      pct(v.win_rate).padStart(8) +
      pnl(v.realized_pnl).padStart(14)
    );
  });
  console.log('  ' + '─'.repeat(88));
  console.log(`\n  ${rows.length} entries\n`);
}

// ── filter ────────────────────────────────────────────────────
async function cmdFilter(args, classified) {
  let labelFilter = null, domainFilter = null, sortField = 'avg_roi', limit = 20;
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--label'  && args[i+1]) labelFilter  = args[++i].toUpperCase();
    if (args[i] === '--domain' && args[i+1]) domainFilter = args[++i].toUpperCase();
    if (args[i] === '--sort'   && args[i+1]) sortField    = args[++i];
    if (args[i] === '--limit'  && args[i+1]) limit        = Number(args[++i]);
  }

  const validSort = ['avg_roi', 'win_rate', 'realized_pnl', 'total_volume'];
  if (!validSort.includes(sortField)) {
    console.error(`--sort options: ${validSort.join(' / ')}`); process.exit(1);
  }

  const rows = Object.entries(classified)
    .filter(([, v]) => !labelFilter  || v.label === labelFilter)
    .filter(([, v]) => !domainFilter || (v.domains || ['GEN']).includes(domainFilter))
    .sort((a, b) => (b[1][sortField] || 0) - (a[1][sortField] || 0))
    .slice(0, limit);

  const filterStr = [
    labelFilter  && `label=${labelFilter}`,
    domainFilter && `domain=${domainFilter}`,
    `sort=${sortField}`,
  ].filter(Boolean).join(' ');

  console.log(`\n  Filter Results (${filterStr}) — ${rows.length} entries\n`);
  console.log('  ' + '─'.repeat(96));
  console.log(
    '  # '.padEnd(5) + 'Address'.padEnd(46) + 'Type'.padEnd(9) +
    'Domain'.padEnd(14) + 'ROI'.padStart(9) + 'Win%'.padStart(8) +
    'Realized PnL'.padStart(14) + 'Total Vol'.padStart(12)
  );
  console.log('  ' + '─'.repeat(96));
  rows.forEach(([addr, v], i) => {
    const tags = (v.domains || ['GEN']).join('+');
    console.log(
      `  ${String(i+1).padStart(2)}. `.padEnd(5) +
      addr.padEnd(46) +
      v.label.padEnd(9) +
      tags.padEnd(14) +
      roi(v.avg_roi).padStart(9) +
      pct(v.win_rate).padStart(8) +
      pnl(v.realized_pnl).padStart(14) +
      usd(v.total_volume).padStart(12)
    );
  });
  console.log('  ' + '─'.repeat(96) + '\n');
}

// ── Entry Point ──────────────────────────────────────────────────────
const [,, cmd, ...rest] = process.argv;
const CMDS = { addr: cmdAddr, top: cmdTop, filter: cmdFilter };

if (!cmd || !CMDS[cmd]) {
  console.log(`
Smart Money Query Tool

Usage:
  node query.js addr   <address>
  node query.js top    <domain> [n] [--label LABEL]
  node query.js filter [--label L] [--domain D] [--sort F] [--limit N]

Domain Codes: ${Object.entries(DOMAIN_LABELS).map(([k,v]) => `${k}(${v})`).join(' / ')}
Types:   HUMAN / SIGNAL / MM / BOT / COPYBOT / NOISE
Sort:    avg_roi (default) / win_rate / realized_pnl / total_volume
  `);
  process.exit(cmd ? 1 : 0);
}

sm.classify({ withDomains: true })
  .then(classified => CMDS[cmd](rest, classified))
  .catch(e => { console.error(e); process.exit(1); });
