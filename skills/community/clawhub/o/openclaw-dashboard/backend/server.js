#!/usr/bin/env node
'use strict';
/**
 * OpenClaw Dashboard — Modular Backend Server
 *
 * Thin HTTP shell: auth → CORS → route dispatch → provider.
 * All business logic lives in providers/.
 *
 * Start: node backend/server.js
 * Env:   DASHBOARD_PORT (default 18791), OPENCLAW_AUTH_TOKEN, etc.
 */
const http = require('http');
const fs = require('fs');
const path = require('path');
const packageInfo = require('../package.json');

const cfg    = require('./lib/config');
const helpers = require('./lib/http-helpers');

// ── Global Error Handlers ───────────────────────────────────────────
process.on('uncaughtException', (err) => {
  console.error('[FATAL] Uncaught Exception:', err);
  console.error(err.stack);
  // Give logs time to flush before exit
  setTimeout(() => process.exit(1), 100);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('[FATAL] Unhandled Rejection at:', promise, 'reason:', reason);
  // Don't exit, but log prominently
});

// ── Simple Router ───────────────────────────────────────────────────
class Router {
  constructor() {
    this._routes = new Map(); // exact: "METHOD /path" → handler(req, res, query)
    this._dynamic = [];       // dynamic: { method, pattern, regex, keys, handler }
  }

  add(method, pattern, handler) {
    const m = String(method || 'GET').toUpperCase();
    const p = String(pattern || '/');
    if (p.includes(':')) {
      const keys = [];
      const regexSrc = '^' + p.replace(/:[^/]+/g, (seg) => {
        keys.push(seg.slice(1));
        return '([^/]+)';
      }) + '$';
      this._dynamic.push({ method: m, pattern: p, regex: new RegExp(regexSrc), keys, handler });
      return;
    }
    this._routes.set(`${m} ${p}`, handler);
  }

  resolve(method, pathname) {
    const m = String(method || 'GET').toUpperCase();
    const exact = this._routes.get(`${m} ${pathname}`);
    if (exact) return { handler: exact, params: {} };

    for (const r of this._dynamic) {
      if (r.method !== m) continue;
      const match = pathname.match(r.regex);
      if (!match) continue;
      const params = {};
      r.keys.forEach((k, idx) => { params[k] = decodeURIComponent(match[idx + 1] || ''); });
      return { handler: r.handler, params };
    }
    return null;
  }

  /** List all registered routes (for debug) */
  list() {
    const exact = [...this._routes.keys()];
    const dyn = this._dynamic.map(r => `${r.method} ${r.pattern}`);
    return [...exact, ...dyn];
  }
}

const router = new Router();

// ── Register Providers ──────────────────────────────────────────────
// Each provider exports register(router) which adds its routes.
const providers = [
  require('./providers/ground-truth'),
  require('./providers/sessions'),
  require('./providers/ledger'),
  require('./providers/cron'),
  require('./providers/spark'),
  require('./providers/copilot'),
  require('./providers/watchdog'),
  require('./providers/system'),
  require('./providers/config'),
  require('./providers/tasks'),
  require('./providers/local-api-hub'), // Local API Hub health + proxy
  require('./providers/spark-tasks'),   // Spark Agent task monitor
  require('./providers/ops-legacy'),    // proxy remaining routes to old api-server.js
];

for (const p of providers) {
  p.register(router);
}

console.log(`[server] registered ${router.list().length} routes from ${providers.length} providers`);

// ── Static files ────────────────────────────────────────────────────
const STATIC_ROOT = path.join(__dirname, '..');
const STATIC_FILES = {
  '/icon.svg':     { file: 'icon.svg',     type: 'image/svg+xml' },
  '/favicon.svg':  { file: 'favicon.svg',  type: 'image/svg+xml' },
  '/icon-180.png': { file: 'icon-180.png', type: 'image/png' },
  '/marked.min.js':  { file: 'marked.min.js',  type: 'application/javascript' },
  '/purify.min.js':  { file: 'purify.min.js',  type: 'application/javascript' },
  '/models-registry.json': { file: 'models-registry.json', type: 'application/json' },
};

const MIME_TYPES = {
  '.js':  'application/javascript',
  '.css': 'text/css',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.html': 'text/html',
};

function serveStatic(req, res, pathname) {
  // Known static files
  const entry = STATIC_FILES[pathname];
  if (entry) {
    const filePath = path.join(STATIC_ROOT, entry.file);
    try {
      const content = fs.readFileSync(filePath);
      res.writeHead(200, { 'Content-Type': entry.type, 'Cache-Control': 'public, max-age=86400' });
      res.end(content);
      return true;
    } catch { return false; }
  }

  // Serve frontend/ directory (CSS, JS modules)
  if (pathname.startsWith('/frontend/')) {
    const relPath = pathname.slice(1); // strip leading /
    const filePath = path.join(STATIC_ROOT, relPath);
    // Security: no traversal
    if (relPath.includes('..')) return false;
    const ext = path.extname(filePath);
    const mime = MIME_TYPES[ext];
    if (!mime) return false;
    try {
      const content = fs.readFileSync(filePath);
      res.writeHead(200, { 'Content-Type': mime, 'Cache-Control': 'public, max-age=300' });
      res.end(content);
      return true;
    } catch { return false; }
  }

  return false;
}

// ── Main HTML ───────────────────────────────────────────────────────
function serveDashboard(req, res) {
  // Serve modular frontend (fallback to old monolith if frontend/index.html missing)
  const newPath = path.join(STATIC_ROOT, 'frontend', 'index.html');
  const oldPath = path.join(STATIC_ROOT, 'agent-dashboard.html');
  const filePath = fs.existsSync(newPath) ? newPath : oldPath;
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(content);
  } catch (e) {
    helpers.errorReply(res, 500, 'Dashboard HTML not found');
  }
}

function parseRequestUrl(req) {
  try {
    return new URL(req?.url || '/', 'http://dashboard.invalid');
  } catch {
    return null;
  }
}

// ── Health (no auth) ────────────────────────────────────────────────
router.add('GET', '/health', (_req, res) => {
  helpers.jsonReply(res, 200, {
    status: 'ok',
    uptime: process.uptime(),
    version: packageInfo.version,
    providers: providers.length,
    routes: router.list().length,
    capabilities: {
      copilot: copilot.isConfigured(),
      configEndpoint: cfg.ENABLE_CONFIG_ENDPOINT,
      mutatingOps: false,
      operatorActions: false,
    },
    links: {
      controlUi: cfg.CONTROL_UI_URL || null,
    },
  });
});

// ── Login (cookie-based auth) ───────────────────────────────────────
router.add('POST', '/login', async (req, res) => {
  try {
    const body = await helpers.readJsonBody(req);
    if (body.token === cfg.AUTH_TOKEN) {
      res.writeHead(200, {
        'Content-Type': 'application/json',
        'Set-Cookie': helpers.authCookie(604800),
      });
      res.end(JSON.stringify({ ok: true }));
    } else {
      helpers.errorReply(res, 401, 'Invalid token');
    }
  } catch {
    helpers.errorReply(res, 400, 'Bad request');
  }
});

router.add('GET', '/logout', (_req, res) => {
  res.writeHead(302, {
    'Set-Cookie': helpers.authCookie(0),
    'Location': '/',
  });
  res.end();
});

// ── HTTP Server ─────────────────────────────────────────────────────
const server = http.createServer((req, res) => {
  const requestUrl = parseRequestUrl(req);
  if (!requestUrl) return helpers.errorReply(res, 400, 'Bad request');
  const pathname = requestUrl.pathname.replace(/\/+$/, '') || '/';
  const query = Object.fromEntries(requestUrl.searchParams.entries());
  const method = req.method.toUpperCase();

  // CORS preflight
  helpers.setCors(res, req);
  if (method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  // Health: no auth
  if (pathname === '/health' && method === 'GET') {
    const match = router.resolve('GET', '/health');
    if (match?.handler) return match.handler(req, res, query);
    return helpers.errorReply(res, 404, 'Health handler not found');
  }

  // Static files: no auth
  if (serveStatic(req, res, pathname)) return;

  // Login: no auth
  if (pathname === '/login' && method === 'GET') {
    const loginHtml = `<!doctype html>
<html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>OpenClaw Dashboard Login</title>
<style>
  :root{color-scheme:dark}
  body{margin:0;min-height:100vh;display:grid;place-items:center;background:#0e1015;color:#d4d4d8;font-family:Inter,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif}
  .card{width:min(420px,92vw);background:#161920;border:1px solid #1e2028;border-radius:14px;padding:28px;box-shadow:0 12px 32px rgba(0,0,0,.35)}
  h1{margin:0 0 6px;font-size:1.2rem;color:#f4f4f5;letter-spacing:-.02em} p{margin:0 0 18px;color:#838387;font-size:.88rem}
  input{width:100%;padding:11px 12px;border-radius:10px;border:1px solid #2e3040;background:#0e1015;color:#f4f4f5;box-sizing:border-box;outline:none}
  input:focus{border-color:#ff5c5c;box-shadow:0 0 0 3px rgba(255,92,92,.15)}
  button{margin-top:10px;width:100%;padding:11px 12px;border:0;border-radius:10px;background:#ff5c5c;color:#fff;font-weight:650;cursor:pointer}
  button:hover{background:#ff7070}
  .err{margin-top:10px;color:#ef4444;font-size:.82rem;display:none}
</style></head><body>
  <div class="card">
    <h1>🦞 OpenClaw Dashboard</h1>
    <p>Sign in once, then cookie-only access.</p>
    <input id="token" type="password" placeholder="Paste OPENCLAW_AUTH_TOKEN" autocomplete="off" />
    <button id="go">Sign in</button>
    <div id="err" class="err">Invalid token</div>
  </div>
<script>
  const btn=document.getElementById('go'); const inp=document.getElementById('token'); const err=document.getElementById('err');
  async function login(){
    err.style.display='none';
    const r=await fetch('/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({token:inp.value})});
    if(!r.ok){err.style.display='block';return;}
    location.href='/';
  }
  btn.onclick=login; inp.addEventListener('keydown',e=>{if(e.key==='Enter')login();});
</script></body></html>`;
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    return res.end(loginHtml);
  }
  if (pathname === '/login' && method === 'POST') {
    const match = router.resolve('POST', '/login');
    if (match?.handler) return match.handler(req, res, query);
  }
  if (pathname === '/logout') {
    const match = router.resolve('GET', '/logout');
    if (match?.handler) return match.handler(req, res, query);
  }

  // Auth check
  if (!helpers.authenticate(req)) {
    // Cookie-only UX: unauth root goes to login page.
    if (pathname === '/' && method === 'GET') {
      res.writeHead(302, { Location: '/login' });
      return res.end();
    }
    return helpers.errorReply(res, 401, 'Unauthorized');
  }

  // Dashboard HTML
  if (pathname === '/' && method === 'GET') {
    return serveDashboard(req, res);
  }

  // Route to provider
  try {
    const match = router.resolve(method, pathname);
    if (match?.handler) {
      req.params = match.params || {};
      return match.handler(req, res, query);
    }

    return helpers.errorReply(res, 404, `Route not found: ${method} ${pathname}`);
  } catch (e) {
    console.error('Unhandled error:', e);
    helpers.errorReply(res, 500, 'Internal server error');
  }
});

server.on('error', (e) => {
  console.error('Server error:', e);
  process.exit(1);
});

if (!cfg.AUTH_TOKEN) {
  console.error('[server] Refusing to start without OPENCLAW_AUTH_TOKEN.');
  process.exit(1);
}

server.listen(cfg.PORT, cfg.HOST, () => {
  console.log(`[server] Dashboard ${packageInfo.version} listening on ${cfg.HOST}:${cfg.PORT}`);
  console.log(`[server] Routes: ${router.list().length} | Providers: ${providers.length}`);
});

const { WebSocketServer } = require('ws');
const wss = new WebSocketServer({ noServer: true, maxPayload: 64 * 1024 });

const copilot = require('./providers/copilot');

wss.on('connection', (ws, req) => {
  const requestUrl = parseRequestUrl(req);
  if (requestUrl?.pathname === '/api/copilot/ws') {
    copilot.handleWsConnection(ws, req);
  } else {
    ws.close(1008, 'Invalid request');
  }
});

server.on('upgrade', (request, socket, head) => {
  const requestUrl = parseRequestUrl(request);
  if (!requestUrl) {
    socket.write('HTTP/1.1 400 Bad Request\r\nConnection: close\r\n\r\n');
    socket.destroy();
    return;
  }
  if (requestUrl.pathname === '/api/copilot/ws') {
    if (!helpers.authenticate(request)) {
      socket.write('HTTP/1.1 401 Unauthorized\r\nConnection: close\r\n\r\n');
      socket.destroy();
      return;
    }
    if (!copilot.isConfigured()) {
      socket.write('HTTP/1.1 503 Service Unavailable\r\nConnection: close\r\n\r\n');
      socket.destroy();
      return;
    }
    wss.handleUpgrade(request, socket, head, (ws) => {
      wss.emit('connection', ws, request);
    });
  } else {
    socket.destroy();
  }
});
