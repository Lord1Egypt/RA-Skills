#!/usr/bin/env node
/**
 * OpenClaw Token Monitor - Pro with SQLite Persistence
 * 数据永久存储，历史回溯，费用统计
 */
const http = require('http');
const fs = require('fs');
const path = require('path');
const { execFile } = require('child_process');
const initSqlJs = require('/tmp/node_modules/sql.js');

const PORT = 3000;
var POLL_INTERVAL = 3000; // 可通过 API 修改
const HTML_FILE = __dirname + '/token-monitor.html';
const DB_FILE = __dirname + '/../data/token_history.db';

let db = null;
let latestSnap = null;
let lastSnap = null;
let lastTs = null;
let clients = [];
let sqlJsReady = null;

// ─── DB Init ─────────────────────────────────────────────────────────────
async function initDB() {
  const SQL = await initSqlJs();
  // Load existing or create new
  try {
    if (fs.existsSync(DB_FILE)) {
      const buf = fs.readFileSync(DB_FILE);
      db = new SQL.Database(buf);
      console.log('DB loaded:', DB_FILE, '(' + buf.length + ' bytes)');
    } else {
      db = new SQL.Database();
      console.log('New DB created');
    }
  } catch(e) {
    db = new SQL.Database();
    console.log('DB error, created new:', e.message);
  }

  db.run(`
    CREATE TABLE IF NOT EXISTS snapshots (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      ts INTEGER NOT NULL,
      date TEXT NOT NULL,
      hour INTEGER NOT NULL,
      session_key TEXT NOT NULL,
      model TEXT,
      kind TEXT,
      input_tokens INTEGER DEFAULT 0,
      output_tokens INTEGER DEFAULT 0,
      total_tokens INTEGER DEFAULT 0,
      context_tokens INTEGER DEFAULT 0,
      age_ms INTEGER DEFAULT 0
    );
    CREATE TABLE IF NOT EXISTS daily_summary (
      date TEXT PRIMARY KEY,
      input_tokens INTEGER DEFAULT 0,
      output_tokens INTEGER DEFAULT 0,
      total_tokens INTEGER DEFAULT 0,
      context_tokens INTEGER DEFAULT 0,
      cost_cny REAL DEFAULT 0,
      session_count INTEGER DEFAULT 0,
      peak_rate_in REAL DEFAULT 0,
      peak_rate_out REAL DEFAULT 0
    );
    CREATE TABLE IF NOT EXISTS rate_history (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      ts INTEGER NOT NULL,
      date TEXT NOT NULL,
      rate_in REAL DEFAULT 0,
      rate_out REAL DEFAULT 0,
      rate_total REAL DEFAULT 0,
      rate_cny REAL DEFAULT 0,
      input_tokens INTEGER DEFAULT 0,
      output_tokens INTEGER DEFAULT 0,
      total_tokens INTEGER DEFAULT 0
    );
  `);

  saveDB();
  console.log('DB tables ready');
}

// Save DB to disk every 30s
setInterval(() => { if (db) saveDB(); }, 15000);

function saveDB() {
  if (!db) return;
  try {
    const data = db.export();
    const buf = Buffer.from(data);
    fs.writeFileSync(DB_FILE, buf);
  } catch(e) {}
}

// ─── Polling ──────────────────────────────────────────────────────────────
function pollSessions() {
  return new Promise((resolve) => {
    execFile('openclaw', ['sessions', '--active', '60', '--json'], { timeout: 10000 }, (err, stdout) => {
      if (err) { resolve({ error: err.message }); return; }
      try {
        const d = JSON.parse(stdout);
        const snap = buildSnap(d);
        latestSnap = snap;
        resolve(snap);
      } catch(e) { resolve({ error: e.message }); }
    });
  });
}

function buildSnap(d) {
  const sessions = d.sessions || [];
  const now = Date.now();
  const ts = Math.floor(now);
  const date = new Date(now).toISOString().slice(0, 10);
  const hour = new Date(now).getHours();

  const totals = sessions.reduce((a, s) => ({
    inputTokens: a.inputTokens + (s.inputTokens||0),
    outputTokens: a.outputTokens + (s.outputTokens||0),
    totalTokens: a.totalTokens + (s.inputTokens||0) + (s.outputTokens||0),
    contextTokens: a.contextTokens + (s.contextTokens||0),
  }), { inputTokens:0, outputTokens:0, totalTokens:0, contextTokens:0 });

  // Rate
  var rateIn = 0, rateOut = 0, rateTotal = 0, rateCny = 0;
  if (lastSnap && lastTs) {
    var dt = (now - lastTs) / 1000;
    if (dt > 0) {
      var din = totals.inputTokens - lastSnap.totals.inputTokens;
      var dout = totals.outputTokens - lastSnap.totals.outputTokens;
      var dcny = calcCny(totals.inputTokens, totals.outputTokens) - calcCny(lastSnap.totals.inputTokens, lastSnap.totals.outputTokens);
      rateIn = Math.max(0, din / dt);
      rateOut = Math.max(0, dout / dt);
      rateTotal = rateIn + rateOut;
      rateCny = Math.max(0, dcny * 60 / dt);
    }
  }

  const sessionData = sessions.map(s => ({
    key: s.key||'',
    shortKey: (s.key||'').length > 12 ? '\u2026'+(s.key||'').slice(-12) : (s.key||''),
    model: s.model||'-',
    kind: s.kind||'-',
    inputTokens: s.inputTokens||0,
    outputTokens: s.outputTokens||0,
    totalTokens: s.totalTokens||0,
    contextTokens: s.contextTokens||0,
    inputPct: s.totalTokens>0 ? Math.round(s.inputTokens/s.totalTokens*100) : 0,
    ageMs: s.ageMs||0,
    ageStr: fmtAge(s.ageMs||0),
    updatedAt: s.updatedAt||0,
    timeStr: s.updatedAt ? new Date(s.updatedAt).toLocaleTimeString('zh-CN',{hour12:false}) : '-',
  }));

  // Per-model cost aggregation
  const modelMap = {};
  sessions.forEach(s => {
    const m = s.model || 'unknown';
    if (!modelMap[m]) modelMap[m] = { inp: 0, out: 0, total: 0 };
    modelMap[m].inp += s.inputTokens || 0;
    modelMap[m].out += s.outputTokens || 0;
    modelMap[m].total += s.totalTokens || 0;
  });
  const models = Object.entries(modelMap).map(([name, v]) => ({
    name, inputTokens: v.inp, outputTokens: v.out, totalTokens: v.total,
    cny: calcCnyByModel(v.inp, v.out, name),
    pricing: getPricing(name),
  }));
  const snap = {
    ts, date, hour,
    timeStr: new Date(now).toLocaleTimeString('zh-CN',{hour12:false}),
    totals, sessionCount: sessions.length, sessionData, models,
    rateIn, rateOut, rateTotal, rateCny,
    error: null,
  };

  // Save to DB
  saveSnapshot(snap, sessions);
  saveRate(snap);

  lastSnap = { ts: now, totals: { inputTokens: totals.inputTokens, outputTokens: totals.outputTokens } };
  lastTs = now;
  latestSnap = snap;

  return snap;
}

function saveSnapshot(snap, sessions) {
  if (!db) return;
  try {
    const stmt = db.prepare(`INSERT OR REPLACE INTO snapshots (ts, date, hour, session_key, model, kind, input_tokens, output_tokens, total_tokens, context_tokens, age_ms) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`);
    for (const s of sessions) {
      stmt.run([snap.ts, snap.date, snap.hour, s.key||'', s.model||'-', s.kind||'-', s.inputTokens||0, s.outputTokens||0, s.totalTokens||0, s.contextTokens||0, s.ageMs||0]);
    }
    stmt.free();
    updateDailySummary(snap);
  } catch(e) {}
}

function updateDailySummary(snap) {
  if (!db) return;
  try {
    const t = snap.totals;
    const cny = calcCny(t.inputTokens, t.outputTokens);
    const existing = queryDailySummary(snap.date);
    if (existing) {
      db.run(`UPDATE daily_summary SET
        input_tokens = MAX(input_tokens, ?),
        output_tokens = MAX(output_tokens, ?),
        total_tokens = MAX(total_tokens, ?),
        context_tokens = MAX(context_tokens, ?),
        cost_cny = MAX(cost_cny, ?),
        session_count = MAX(session_count, ?),
        peak_rate_in = MAX(peak_rate_in, ?),
        peak_rate_out = MAX(peak_rate_out, ?)
        WHERE date = ?`,
        [t.inputTokens, t.outputTokens, t.totalTokens, t.contextTokens, cny, snap.sessionCount, snap.rateIn, snap.rateOut, snap.date]);
    } else {
      db.run(`INSERT INTO daily_summary (date, input_tokens, output_tokens, total_tokens, context_tokens, cost_cny, session_count, peak_rate_in, peak_rate_out) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`,
        [snap.date, t.inputTokens, t.outputTokens, t.totalTokens, t.contextTokens, cny, snap.sessionCount, snap.rateIn, snap.rateOut]);
    }
  } catch(e) {}
}

function saveRate(snap) {
  if (!db) return;
  try {
    db.run(`INSERT INTO rate_history (ts, date, rate_in, rate_out, rate_total, rate_cny, input_tokens, output_tokens, total_tokens) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`,
      [snap.ts, snap.date, snap.rateIn, snap.rateOut, snap.rateTotal, snap.rateCny, snap.totals.inputTokens, snap.totals.outputTokens, snap.totals.totalTokens]);
  } catch(e) {}
}

// ─── Helpers ──────────────────────────────────────────────────────────────
function fmtAge(ms) {
  if (!ms) return '-';
  if (ms < 60000) return Math.round(ms/1000)+'s';
  if (ms < 3600000) return Math.round(ms/60000)+'m';
  return (ms/3600000).toFixed(1)+'h';
}

function fmtNum(n) {
  if (n >= 1e9) return (n/1e9).toFixed(2)+'B';
  if (n >= 1e6) return (n/1e6).toFixed(2)+'M';
  if (n >= 1e3) return (n/1e3).toFixed(1)+'K';
  return String(n);
}

// Multi-model pricing table (yuan per million tokens, CNY)
// Key format: model name substring match
const MODEL_PRICING = {
  'MiniMax-M2.7-highspeed': { inp: 6.0,  out: 24.0,  unit: '¥/M' },
  'MiniMax-M2.7':           { inp: 2.1,  out: 8.4,   unit: '¥/M' },
  'MiniMax-M2':            { inp: 1.0,  out: 4.0,   unit: '¥/M' },
  'gpt-4o':                { inp: 18.0, out: 72.0,  unit: '¥/M' },
  'gpt-4-turbo':           { inp: 36.0, out: 108.0, unit: '¥/M' },
  'gpt-4':                 { inp: 90.0, out: 270.0, unit: '¥/M' },
  'gpt-4o-mini':           { inp: 2.5,  out: 10.0,  unit: '¥/M' },
  'gpt-35-turbo':          { inp: 1.8,  out: 7.2,   unit: '¥/M' },
  'claude-3-5-sonnet':     { inp: 10.8, out: 54.0,  unit: '¥/M' },
  'claude-3-opus':         { inp: 108.0,out: 540.0, unit: '¥/M' },
  'claude-3-haiku':        { inp: 1.2,  out: 5.0,   unit: '¥/M' },
  'deepseek-chat':         { inp: 1.0,  out: 2.0,   unit: '¥/M' },
  'deepseek-coder':        { inp: 1.0,  out: 2.0,   unit: '¥/M' },
  'qwen3':                 { inp: 0.8,  out: 3.2,   unit: '¥/M' },
  'qwen2':                 { inp: 1.2,  out: 4.8,   unit: '¥/M' },
  'qwen-plus':             { inp: 4.0,  out: 12.0,  unit: '¥/M' },
  'qwen-max':              { inp: 20.0, out: 60.0,  unit: '¥/M' },
  'default':               { inp: 2.1,  out: 8.4,   unit: '¥/M' },
};

function getPricing(modelName) {
  if (!modelName) return MODEL_PRICING['default'];
  for (const key of Object.keys(MODEL_PRICING)) {
    if (key !== 'default' && modelName.includes(key)) return MODEL_PRICING[key];
  }
  return MODEL_PRICING['default'];
}

// Calculate total cost for input/output tokens using appropriate model pricing
function calcCnyByModel(inp, out, modelName) {
  const p = getPricing(modelName);
  return inp * p.inp / 1e6 + out * p.out / 1e6;
}

// Legacy single-model calc (MiniMax-M2.7)
function calcCny(inp, out) {
  return calcCnyByModel(inp, out, 'MiniMax-M2.7');
}

// Return pricing info for UI display
function getPricingInfo() {
  return MODEL_PRICING;
}

// ─── DB Query APIs ────────────────────────────────────────────────────────
function queryDailySummary(date) {
  if (!db) return null;
  try {
    const row = db.exec(`SELECT * FROM daily_summary WHERE date = '${date}'`);
    if (row.length && row[0].values.length) {
      const cols = row[0].columns;
      const vals = row[0].values[0];
      const obj = {}; cols.forEach((c,i) => obj[c] = vals[i]);
      return obj;
    }
  } catch(e) {}
  return null;
}

function queryHistory(days, dateFilter) {
  if (!db) return [];
  try {
    const limit = Math.min(days * 24 * 60, 5000);
    let sql = "SELECT ts, date, rate_in, rate_out, rate_total, rate_cny, input_tokens, output_tokens, total_tokens FROM rate_history";
    if (dateFilter) sql += " WHERE date = '" + dateFilter + "'";
    sql += " ORDER BY ts DESC LIMIT " + limit;
    const rows = db.exec(sql);
    if (!rows.length) return [];
    const cols = rows[0].columns;
    return rows[0].values.map(v => {
      const o = {}; cols.forEach((c,i) => o[c] = v[i]); return o;
    }).reverse();
  } catch(e) { return []; }
}

function querySessionsByDate(date) {
  if (!db) return [];
  try {
    const rows = db.exec(`SELECT session_key, model, kind, input_tokens, output_tokens, total_tokens, context_tokens, MAX(age_ms) as age_ms, COUNT(*) as snap_count FROM snapshots WHERE date = '${date}' GROUP BY session_key ORDER BY total_tokens DESC`);
    if (!rows.length) return [];
    const cols = rows[0].columns;
    return rows[0].values.map(v => {
      const o = {}; cols.forEach((c,i) => o[c] = v[i]); return o;
    });
  } catch(e) { return []; }
}

function queryMonthlySummary() {
  if (!db) return null;
  try {
    const now = new Date();
    const ym = now.toISOString().slice(0, 7); // YYYY-MM
    const rows = db.exec(`SELECT SUM(input_tokens) as input_tokens, SUM(output_tokens) as output_tokens, SUM(total_tokens) as total_tokens, SUM(cost_cny) as cost_cny, COUNT(DISTINCT date) as days FROM daily_summary WHERE date LIKE '${ym}%'`);
    if (!rows.length || !rows[0].values.length) return null;
    const cols = rows[0].columns;
    const vals = rows[0].values[0];
    const obj = {}; cols.forEach((c,i) => obj[c] = vals[i]);
    return obj;
  } catch(e) { return null; }
}

// ─── HTTP Server ────────────────────────────────────────────────────────────
const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, 'http://localhost:'+PORT);
  const pathname = url.pathname;

  if (pathname === '/data') {
    // Current snapshot + today's history
    res.writeHead(200, {'Content-Type':'application/json','Cache-Control':'no-cache','Access-Control-Allow-Origin':'*'});
    const today = new Date().toISOString().slice(0,10);
    const hist = queryHistory(1, today);
    res.end(JSON.stringify({ snap: latestSnap, history: hist, todaySummary: queryDailySummary(today) }));
    return;
  }

  if (pathname === '/sse') {
    res.writeHead(200, {'Content-Type':'text/event-stream','Cache-Control':'no-cache','Connection':'keep-alive','Access-Control-Allow-Origin':'*'});
    clients.push(res);
    req.on('close', () => { clients = clients.filter(c => c !== res); });
    return;
  }

  
  if (pathname === '/api/pricing') {
    res.writeHead(200, {'Content-Type':'application/json','Access-Control-Allow-Origin':'*'});
    res.end(JSON.stringify({ pricing: getPricingInfo(), currency: 'CNY' }));
    return;
  }
  if (pathname === '/api/config') {
    var pollVal = url.searchParams.get('poll');
    if (pollVal) {
      POLL_INTERVAL = Math.max(200, Math.min(60000, parseInt(pollVal, 10) || 3000));
      res.writeHead(200, {'Content-Type':'application/json'});
      res.end(JSON.stringify({ poll_interval: POLL_INTERVAL, updated: true }));
      return;
    }
    res.writeHead(200, {'Content-Type':'application/json'});
    res.end(JSON.stringify({ poll_interval: POLL_INTERVAL }));
    return;
  }

  if (pathname === '/health') { res.writeHead(200); res.end('ok'); return; }

  // API: query by date
  if (pathname === '/api/daily') {
    const date = url.searchParams.get('date') || new Date().toISOString().slice(0,10);
    const summary = queryDailySummary(date);
    const sessions = querySessionsByDate(date);
    const hist = queryHistoryForDate(date);
    res.writeHead(200, {'Content-Type':'application/json','Access-Control-Allow-Origin':'*'});
    res.end(JSON.stringify({ date, summary, sessions, history: hist }));
    return;
  }

  if (pathname === '/api/monthly') {
    const m = queryMonthlySummary();
    const now = new Date();
    const ym = now.toISOString().slice(0,7);
    const daysInMonth = new Date(now.getFullYear(), now.getMonth()+1, 0).getDate();
    const today = now.getDate();
    const proj = m ? {
      input_tokens: Math.round(m.input_tokens / today * daysInMonth),
      output_tokens: Math.round(m.output_tokens / today * daysInMonth),
      total_tokens: Math.round(m.total_tokens / today * daysInMonth),
      cost_cny: m.cost_cny / today * daysInMonth,
      days_so_far: today,
      days_in_month: daysInMonth,
    } : null;
    res.writeHead(200, {'Content-Type':'application/json','Access-Control-Allow-Origin':'*'});
    res.end(JSON.stringify({ month: ym, actual: m, projected: proj }));
    return;
  }

  if (pathname === '/api/dates') {
    if (!db) { res.writeHead(200); res.end('[]'); return; }
    try {
      const rows = db.exec(`SELECT DISTINCT date FROM daily_summary ORDER BY date DESC LIMIT 90`);
      const dates = rows.length ? rows[0].values.map(v => v[0]) : [];
      res.writeHead(200, {'Content-Type':'application/json','Access-Control-Allow-Origin':'*'});
      res.end(JSON.stringify(dates));
    } catch(e) { res.writeHead(500); res.end(e.message); }
    return;
  }

  if (pathname === '/api/export') {
    if (!db) { res.writeHead(500); res.end('no db'); return; }
    try {
      const rows = db.exec(`SELECT * FROM daily_summary ORDER BY date DESC LIMIT 365`);
      const cols = rows.length ? rows[0].columns : [];
      const data = rows.length ? rows[0].values.map(v => { const o={}; cols.forEach((c,i)=>o[c]=v[i]); return o; }) : [];
      res.writeHead(200, {'Content-Type':'application/json','Access-Control-Allow-Origin':'*'});
      res.end(JSON.stringify({ daily: data, exported_at: new Date().toISOString() }));
    } catch(e) { res.writeHead(500); res.end(e.message); }
    return;
  }

  // Serve HTML
  res.writeHead(200, {'Content-Type':'text/html; charset=utf-8'});
  res.end(fs.readFileSync(HTML_FILE, 'utf8'));
});

function queryHistoryForDate(date) {
  if (!db) return [];
  try {
    const rows = db.exec(`SELECT ts, rate_in, rate_out, rate_total, rate_cny, input_tokens, output_tokens, total_tokens FROM rate_history WHERE date = '${date}' ORDER BY ts ASC`);
    if (!rows.length) return [];
    const cols = rows[0].columns;
    return rows[0].values.map(v => { const o={}; cols.forEach((c,i)=>o[c]=v[i]); return o; });
  } catch(e) { return []; }
}

// ─── Broadcast ─────────────────────────────────────────────────────────────
function broadcast() {
  if (!latestSnap || clients.length === 0) return;
  const today = new Date().toISOString().slice(0,10);
  // SSE: only send current snap, NOT history (client accumulates its own streaming buffer)
  const payload = 'data: ' + JSON.stringify({ snap: latestSnap, todaySummary: queryDailySummary(today) }) + '\n\n';
  clients.forEach(c => c.write(payload));
}

// ─── Poll Loop ─────────────────────────────────────────────────────────────
async function poll() {
  try {
    await pollSessions();
    broadcast();
  } catch(e) { console.error('poll err:', e.message); }
  setTimeout(poll, POLL_INTERVAL); // uses dynamic POLL_INTERVAL var
}

// ─── Start ─────────────────────────────────────────────────────────────────
async function main() {
  await initDB();
  poll();
  server.listen(PORT, '0.0.0.0', () => {
    console.log('OpenClaw Token Monitor: http://0.0.0.0:' + PORT);
    console.log('DB file:', DB_FILE);
  });
}

main().catch(e => console.error('Fatal:', e));
