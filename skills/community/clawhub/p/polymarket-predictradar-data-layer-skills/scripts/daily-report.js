'use strict';
const sm = require('./smartmoney');

const DOMAIN_LABELS = {
  POL: 'Politics', GEO: 'Geopolitics', FIN: 'Finance',
  CRY: 'Crypto', SPT: 'Sports', TEC: 'Tech/AI',
  CUL: 'Entertainment', GEN: 'Generalist',
};

function pct(v)    { return (v * 100).toFixed(1) + '%'; }
function usd(v)    { const r = Math.round(v || 0); return (r >= 0 ? '+$' : '-$') + Math.abs(r).toLocaleString(); }

async function main() {
  process.stderr.write('Fetching classification data...\n');
  const classified = await sm.classify({ withDomains: true });

  const date   = new Date().toISOString().slice(0, 10);
  const counts = {};
  for (const { label } of Object.values(classified)) counts[label] = (counts[label] || 0) + 1;
  const total  = Object.keys(classified).length;
  const humans = Object.entries(classified).filter(([, v]) => v.label === 'HUMAN');

  const topROI = humans.filter(([, v]) => v.market_count >= 5 && v.win_rate > 0)
    .sort((a, b) => b[1].avg_roi - a[1].avg_roi).slice(0, 10);

  const topPnL = humans.filter(([, v]) => v.market_count >= 5)
    .sort((a, b) => b[1].realized_pnl - a[1].realized_pnl).slice(0, 10);

  const topWR  = humans.filter(([, v]) => v.market_count >= 10)
    .sort((a, b) => b[1].win_rate - a[1].win_rate).slice(0, 10);

  const domainMap = {};
  for (const [addr, v] of humans) {
    for (const d of (v.domains || [])) {
      if (!domainMap[d]) domainMap[d] = [];
      domainMap[d].push([addr, v]);
    }
  }
  const domainTop = {};
  for (const [d, list] of Object.entries(domainMap)) {
    domainTop[d] = list.filter(([, v]) => v.market_count >= 5)
      .sort((a, b) => b[1].avg_roi - a[1].avg_roi).slice(0, 3);
  }

  const out = [];
  const ln  = s => out.push(s ?? '');

  ln(`📊 Polymarket Smart Money Daily Report · ${date}`);
  ln('━━━━━━━━━━━━━━━━━━━━━━');
  ln();
  ln(`📌 Network-wide Address Distribution (${total.toLocaleString()} total)`);
  for (const [label, cnt] of Object.entries(counts).sort((a, b) => b[1] - a[1])) {
    ln(`  ${label}: ${cnt} (${(cnt / total * 100).toFixed(1)}%)`);
  }

  ln();
  ln('🏆 HUMAN Top10 · by ROI');
  for (const [addr, v] of topROI) {
    const d = (v.domains || []).join('/');
    ln(`\n${topROI.indexOf(topROI.find(x => x[0] === addr)) + 1}. ROI ${pct(v.avg_roi)} · Win Rate ${pct(v.win_rate)} · PnL ${usd(v.realized_pnl)} · [${d}]`);
    ln(`▸ ${addr}`);
  }

  ln();
  ln('💰 HUMAN Top10 · by Realized PnL');
  for (let i = 0; i < topPnL.length; i++) {
    const [addr, v] = topPnL[i];
    const d = (v.domains || []).join('/');
    ln(`\n${i + 1}. PnL ${usd(v.realized_pnl)} · ROI ${pct(v.avg_roi)} · Win Rate ${pct(v.win_rate)} · [${d}]`);
    ln(`▸ ${addr}`);
  }

  ln();
  ln('🎯 HUMAN Top10 · by Win Rate (closed positions ≥ 10)');
  for (let i = 0; i < topWR.length; i++) {
    const [addr, v] = topWR[i];
    const d = (v.domains || []).join('/');
    ln(`\n${i + 1}. Win Rate ${pct(v.win_rate)} · ROI ${pct(v.avg_roi)} · PnL ${usd(v.realized_pnl)} · [${d}]`);
    ln(`▸ ${addr}`);
  }

  ln();
  ln('🌐 HUMAN Distribution by Domain');
  ln();
  const domainCounts = Object.entries(domainMap).sort((a, b) => b[1].length - a[1].length);
  for (const [d, list] of domainCounts) {
    ln(`  ${DOMAIN_LABELS[d] || d}(${d}): ${list.length} traders`);
  }

  for (const [d, list] of Object.entries(domainTop)) {
    if (!list.length) continue;
    ln();
    ln(`🔝 ${DOMAIN_LABELS[d] || d}(${d}) Top3 · by ROI`);
    for (let i = 0; i < list.length; i++) {
      const [addr, v] = list[i];
      ln(`\n${i + 1}. ROI ${pct(v.avg_roi)} · Win Rate ${pct(v.win_rate)} · PnL ${usd(v.realized_pnl)}`);
      ln(`▸ ${addr}`);
    }
  }

  ln();
  ln('📌 Data is on-chain static snapshot, not representative of real-time positions');
  ln(`⏰ Data as of: ${date}`);

  console.log(out.join('\n'));
}

main().catch(e => { console.error(e); process.exit(1); });
