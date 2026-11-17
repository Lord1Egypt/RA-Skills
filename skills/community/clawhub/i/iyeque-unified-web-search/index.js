const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const ALLOW_NETWORK = args.includes('--allow-network');
const ALLOW_LOCAL = args.includes('--allow-local');
const params = {};
for (let i = 0; i < args.length; i++) {
  if (!args[i].startsWith('--')) continue;
  params[args[i].slice(2)] = args[i + 1] && !args[i + 1].startsWith('--') ? args[++i] : true;
}

const MAX_QUERY = 500;
const MAX_RESULTS = 50;
const ALLOWED_SOURCES = new Set(['tavily', 'web-search-plus', 'browser', 'local']);

function validateQuery(value) {
  if (typeof value !== 'string' || !value.trim()) throw new Error('Query is required');
  const query = value.trim();
  if (query.length > MAX_QUERY) throw new Error(`Query too long (max ${MAX_QUERY} characters)`);
  return query;
}

function parseSources(value) {
  if (value === undefined) return ['tavily'];
  let sources;
  try { sources = JSON.parse(value); } catch { throw new Error('sources must be a JSON array'); }
  if (!Array.isArray(sources) || sources.length === 0 || sources.some(s => !ALLOWED_SOURCES.has(s))) {
    throw new Error(`sources must contain only: ${[...ALLOWED_SOURCES].join(', ')}`);
  }
  return [...new Set(sources)];
}

function resultLimit(value) {
  const n = Number(value ?? 5);
  if (!Number.isInteger(n) || n < 1 || n > MAX_RESULTS) throw new Error(`max_results must be an integer from 1 to ${MAX_RESULTS}`);
  return n;
}

async function tavilySearch(query, limit) {
  if (!ALLOW_NETWORK) return { items: [], warning: 'Network search disabled; pass --allow-network after confirming the query may be sent to Tavily' };
  if (/\b(password|passwd|secret|token|api[_ -]?key|private key|credential)\b/i.test(query)) return { items: [], warning: 'Network search blocked for a potentially sensitive query' };
  if (!process.env.TAVILY_API_KEY) return { items: [], warning: 'TAVILY_API_KEY is not set' };
  const response = await fetch('https://api.tavily.com/search', {
    method: 'POST', headers: {'content-type': 'application/json'},
    body: JSON.stringify({ api_key: process.env.TAVILY_API_KEY, query, max_results: limit, search_depth: 'basic', include_answer: false }),
    signal: AbortSignal.timeout(20_000)
  });
  if (!response.ok) throw new Error(`Tavily HTTP ${response.status}`);
  const data = await response.json();
  return { items: (data.results || []).slice(0, limit).map(item => ({ source: 'tavily', title: item.title || '', url: item.url || '', score: Number(item.score) || 0, content: item.content || '' })) };
}

function workspaceRoot() { return fs.realpathSync(process.cwd()); }
function localSearch(query, limit) {
  const root = workspaceRoot();
  const dirs = ['memory', 'skills'].map(name => path.join(root, name));
  const out = [];
  const needle = query.toLowerCase();
  function walk(dir, depth = 0) {
    if (depth > 4 || out.length >= limit) return;
    let entries; try { entries = fs.readdirSync(dir, {withFileTypes: true}); } catch { return; }
    for (const entry of entries) {
      if (out.length >= limit || entry.name === 'node_modules' || entry.name.startsWith('.')) continue;
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) { walk(full, depth + 1); continue; }
      if (!entry.isFile()) continue;
      try {
        const stat = fs.statSync(full); if (stat.size > 1_000_000) continue;
        const text = fs.readFileSync(full, 'utf8'); const index = text.toLowerCase().indexOf(needle);
        if (index >= 0 || entry.name.toLowerCase().includes(needle)) {
          const start = index >= 0 ? Math.max(0, index - 80) : 0;
          out.push({source: 'local', title: path.relative(root, full), url: '', score: index >= 0 ? 0.5 : 0.25, snippet: text.slice(start, start + 240).replace(/\s+/g, ' ').trim()});
        }
      } catch { /* skip binary/unreadable files */ }
    }
  }
  for (const dir of dirs) if (fs.existsSync(dir)) walk(dir);
  return out;
}

async function main() {
  try {
    const query = validateQuery(params.query);
    const sources = parseSources(params.sources);
    const limit = resultLimit(params.max_results);
    const results = [];
    const warnings = [];
    if (sources.includes('tavily')) {
      try { const r = await tavilySearch(query, limit); results.push(...r.items); if (r.warning) warnings.push(r.warning); }
      catch (e) { warnings.push(`tavily unavailable: ${e.message}`); }
    }
    if (sources.includes('local')) {
      if (ALLOW_LOCAL) results.push(...localSearch(query, limit));
      else warnings.push('Local search disabled; pass --allow-local after confirming workspace content may be read');
    }
    for (const source of sources.filter(s => s === 'web-search-plus' || s === 'browser')) warnings.push(`${source} is not configured in this standalone bundle`);
    results.sort((a, b) => (b.score || 0) - (a.score || 0));
    const output = results.slice(0, limit);
    if (warnings.length) console.error(JSON.stringify({warnings}));
    process.stdout.write(JSON.stringify(output, null, 2) + '\n');
  } catch (e) { console.error(`Invalid request: ${e.message}`); process.exitCode = 1; }
}
main();
