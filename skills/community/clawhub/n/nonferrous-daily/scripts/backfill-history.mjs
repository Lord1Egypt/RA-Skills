import { readFileSync, writeFileSync, existsSync, readdirSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = join(__dirname, '..');
const SIGNAL_HISTORY_PATH = join(PROJECT_ROOT, 'memory', 'signal-history.jsonl');
const MEMORY_DIR = join(PROJECT_ROOT, 'memory');

const METALS = [
  { code: 'Cu', key: 'copper', unit: 'USD/lb', yahoo: 'HG=F', westmetallField: 'LME_Cu_stock', westmetallUnit: 'USD/t' },
  { code: 'Zn', key: 'zinc', unit: 'USD/t', yahoo: 'ZNC=F', westmetallField: 'LME_Zn_stock', westmetallUnit: 'USD/t' },
  { code: 'Ni', key: 'nickel', unit: 'USD/t', yahoo: null, westmetallField: 'LME_Ni_stock', westmetallUnit: 'USD/t' },
  { code: 'Co', key: 'cobalt', unit: 'USD/t', yahoo: null, westmetallField: null },
  { code: 'Bi', key: 'bismuth', unit: 'USD/t', yahoo: null, westmetallField: null },
  { code: 'Mg', key: 'magnesium', unit: 'USD/t', yahoo: null, westmetallField: null },
];

const METAL_CODE_SET = new Set(METALS.map(m => m.code));

function usdToCnyPerTon(usd, unit, fxRate) {
  if (usd == null || fxRate == null) return null;
  const usdPerTon = unit === 'USD/lb' ? usd * 2204.62 : usd;
  return usdPerTon * fxRate;
}

function parseWestmetallDate(str) {
  // e.g. 24. April 2026
  const m = str.match(/^(\d{1,2})\.\s+([A-Za-z]+)\s+(\d{4})$/);
  if (!m) return null;
  const months = {
    January: 1, February: 2, March: 3, April: 4, May: 5, June: 6,
    July: 7, August: 8, September: 9, October: 10, November: 11, December: 12,
  };
  const d = Number(m[1]);
  const mo = months[m[2]];
  const y = Number(m[3]);
  if (!mo) return null;
  return `${y}-${String(mo).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
}

function parseNum(s) {
  if (s == null) return null;
  const cleaned = String(s).replace(/[,$\s]/g, '');
  const n = Number(cleaned);
  return Number.isFinite(n) ? n : null;
}

function loadJsonl(filePath) {
  if (!existsSync(filePath)) return [];
  return readFileSync(filePath, 'utf-8')
    .split('\n')
    .map(x => x.trim())
    .filter(Boolean)
    .map(line => {
      try { return JSON.parse(line); } catch { return null; }
    })
    .filter(Boolean);
}

async function fetchYahooChart(symbol, range = '6mo') {
  const url = `https://query1.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(symbol)}?interval=1d&range=${range}`;
  const res = await fetch(url, {
    headers: { 'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json' },
    signal: AbortSignal.timeout(15000),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const data = await res.json();
  const result = data?.chart?.result?.[0];
  const ts = result?.timestamp || [];
  const close = result?.indicators?.quote?.[0]?.close || [];
  const out = [];
  for (let i = 0; i < ts.length; i++) {
    if (close[i] == null) continue;
    const date = new Date(ts[i] * 1000).toISOString().slice(0, 10);
    out.push({ date, close: Number(close[i]) });
  }
  return out;
}

async function fetchWestmetallHistory(field) {
  const url = `https://www.westmetall.com/en/markdaten.php?action=table&field=${encodeURIComponent(field)}`;
  const res = await fetch(url, {
    headers: { 'User-Agent': 'Mozilla/5.0', 'Accept': 'text/html' },
    signal: AbortSignal.timeout(20000),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const html = await res.text();
  const rows = [...html.matchAll(/<tr[^>]*>\s*<td[^>]*>([^<]+)<\/td>\s*<td[^>]*>([^<]+)<\/td>\s*<td[^>]*>([^<]+)<\/td>/g)];
  return rows.map(m => {
    const date = parseWestmetallDate(m[1].trim());
    const lmeInv = parseNum(m[2]);
    const usd = parseNum(m[3]);
    if (!date || usd == null) return null;
    return { date, usd, lmeInv };
  }).filter(Boolean);
}

function indexFxByDate(rows) {
  const m = new Map();
  for (const r of rows) m.set(r.date, r.close);
  return m;
}

function nearestFx(date, fxMap) {
  if (fxMap.has(date)) return fxMap.get(date);
  const keys = [...fxMap.keys()].sort();
  let prev = null;
  for (const k of keys) {
    if (k > date) break;
    prev = k;
  }
  return prev ? fxMap.get(prev) : null;
}

function parseLocalMarkdownHistory() {
  if (!existsSync(MEMORY_DIR)) return [];
  const mdFiles = readdirSync(MEMORY_DIR).filter(n => /^\d{4}-\d{2}-\d{2}\.md$/.test(n));
  const out = [];
  for (const f of mdFiles) {
    const date = f.replace('.md', '');
    const text = readFileSync(join(MEMORY_DIR, f), 'utf-8');
    const lines = text.split(/\r?\n/);
    for (const line of lines) {
      // 解析诸如 Cu=311600t 或 Co 415000 这类简易线索，保守处理
      const pairs = [
        { code: 'Cu', re: /(?:Cu|铜)[^\d]{0,8}(\d{4,7})/i },
        { code: 'Zn', re: /(?:Zn|锌)[^\d]{0,8}(\d{4,7})/i },
        { code: 'Ni', re: /(?:Ni|镍)[^\d]{0,8}(\d{4,7})/i },
        { code: 'Co', re: /(?:Co|钴)[^\d]{0,8}(\d{4,7})/i },
        { code: 'Bi', re: /(?:Bi|铋)[^\d]{0,8}(\d{4,7})/i },
        { code: 'Mg', re: /(?:Mg|镁)[^\d]{0,8}(\d{4,6})/i },
      ];
      for (const p of pairs) {
        const m = line.match(p.re);
        if (!m) continue;
        const cny = Number(m[1]);
        if (!Number.isFinite(cny)) continue;
        out.push({ date, metal: p.code, cny, source: 'local-memory-md' });
      }
    }
  }
  return out;
}

async function fetchCurrentSnapshot() {
  try {
    const scriptPath = join(__dirname, 'fetch-all-data.mjs');
    const cp = await import('child_process');
    const { promisify } = await import('util');
    const execFileAsync = promisify(cp.execFile);
    const { stdout } = await execFileAsync(process.execPath, [scriptPath], { timeout: 90000, maxBuffer: 8 * 1024 * 1024 });
    const d = JSON.parse(stdout);
    const rows = [];
    for (const m of METALS) {
      const item = d?.prices?.[m.key] || {};
      if (item.cny == null && item.usd == null) continue;
      rows.push({
        date: d.date,
        metal: m.code,
        cny: item.cny ?? null,
        usd: item.usd ?? null,
        lmeInv: null,
        cnyChange: item.cnyChange ?? null,
        alertLevel: 0,
        trendTag: '震荡',
        keyEvidence: '回填快照：fetch-all-data',
        source: 'fetch-all-data',
      });
    }
    return rows;
  } catch {
    return [];
  }
}

function dedupeAndSort(records) {
  const map = new Map();
  for (const r of records) {
    if (!r?.date || !r?.metal || !METAL_CODE_SET.has(r.metal)) continue;
    const k = `${r.date}|${r.metal}`;
    const prev = map.get(k);
    if (!prev) map.set(k, r);
    else {
      const prevScore = (prev.cny != null ? 2 : 0) + (prev.usd != null ? 1 : 0);
      const currScore = (r.cny != null ? 2 : 0) + (r.usd != null ? 1 : 0);
      if (currScore >= prevScore) map.set(k, { ...prev, ...r });
    }
  }
  return [...map.values()].sort((a, b) => a.date === b.date ? a.metal.localeCompare(b.metal) : a.date.localeCompare(b.date));
}

async function main() {
  const existing = loadJsonl(SIGNAL_HISTORY_PATH).filter(r => METAL_CODE_SET.has(r.metal));
  const localMd = parseLocalMarkdownHistory();

  let fxMap = new Map();
  try {
    const fxRows = await fetchYahooChart('USDCNY=X', '6mo');
    fxMap = indexFxByDate(fxRows);
  } catch {}

  const fetched = [];

  // Source A: Yahoo chart
  for (const m of METALS.filter(x => x.yahoo)) {
    try {
      const rows = await fetchYahooChart(m.yahoo, '6mo');
      for (const r of rows) {
        const fx = nearestFx(r.date, fxMap);
        fetched.push({
          date: r.date,
          metal: m.code,
          usd: r.close,
          cny: usdToCnyPerTon(r.close, m.unit, fx),
          lmeInv: null,
          cnyChange: null,
          alertLevel: 0,
          trendTag: '震荡',
          keyEvidence: `backfill: Yahoo ${m.yahoo}`,
          source: `yahoo:${m.yahoo}`,
        });
      }
    } catch {}
  }

  // Source A/B supplement: Westmetall history (Cu/Zn/Ni)
  for (const m of METALS.filter(x => x.westmetallField)) {
    try {
      const rows = await fetchWestmetallHistory(m.westmetallField);
      for (const r of rows) {
        const fx = nearestFx(r.date, fxMap);
        fetched.push({
          date: r.date,
          metal: m.code,
          usd: r.usd,
          cny: usdToCnyPerTon(r.usd, m.westmetallUnit || m.unit, fx),
          lmeInv: r.lmeInv ?? null,
          cnyChange: null,
          alertLevel: 0,
          trendTag: '震荡',
          keyEvidence: `backfill: Westmetall ${m.westmetallField}`,
          source: `westmetall:${m.westmetallField}`,
        });
      }
    } catch {}
  }

  // Source B: local structured history + markdown notes
  const currentSnapshot = await fetchCurrentSnapshot();

  const merged = dedupeAndSort([...existing, ...localMd, ...fetched, ...currentSnapshot]);
  const beforeKeys = new Set(existing.map(r => `${r.date}|${r.metal}`));
  const added = merged.filter(r => !beforeKeys.has(`${r.date}|${r.metal}`));

  writeFileSync(SIGNAL_HISTORY_PATH, merged.map(r => JSON.stringify(r)).join('\n') + '\n', 'utf-8');

  const stats = {};
  for (const m of METALS) {
    const allCount = merged.filter(r => r.metal === m.code).length;
    const addCount = added.filter(r => r.metal === m.code).length;
    stats[m.code] = { total: allCount, added: addCount };
  }

  console.log(JSON.stringify({
    ok: true,
    output: SIGNAL_HISTORY_PATH,
    added: added.length,
    total: merged.length,
    stats,
  }, null, 2));
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
