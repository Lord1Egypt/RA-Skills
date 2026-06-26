#!/usr/bin/env node
/**
 * lock-me-in: Browser Login Proxy
 * 
 * Starts a headless Chromium browser, exposes it via a web UI,
 * and creates a temporary public tunnel (cloudflared) so the user
 * can interact with the browser remotely to log in.
 * 
 * Sessions (cookies/localStorage) are persisted to disk and can be
 * reloaded for future automated browsing.
 * 
 * Usage: node browser-login.mjs <url> [session-name] [--port N] [--timeout M]
 * 
 * Environment:
 *   LOCK_ME_IN_SESSIONS_DIR - Override sessions directory (default: /data/home/.browser-sessions)
 *   LOCK_ME_IN_CHROME_PATH  - Override Chrome/Chromium path (auto-detected from Playwright)
 *   LOCK_ME_IN_PORT         - Override proxy port (default: 18850)
 *   OPENCLAW_PROXY_URL      - HTTP proxy for browser traffic (optional)
 */

import { createRequire } from 'module';
const require = createRequire(import.meta.url);

const { chromium } = require('/app/node_modules/playwright-core');

// Stealth: inject anti-detection scripts after page creation
const STEALTH_SCRIPTS = [
  // Hide webdriver flag
  `Object.defineProperty(navigator, 'webdriver', { get: () => false })`,
  `delete navigator.__proto__.webdriver`,
  // Realistic plugins array
  `Object.defineProperty(navigator, 'plugins', { get: () => {
    const plugins = [
      { name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer', description: 'Portable Document Format' },
      { name: 'Chrome PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai', description: '' },
      { name: 'Native Client', filename: 'internal-nacl-plugin', description: '' },
    ];
    plugins.length = 3;
    plugins.item = i => plugins[i];
    plugins.namedItem = n => plugins.find(p => p.name === n);
    plugins.refresh = () => {};
    return plugins;
  }})`,
  // Languages
  `Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en', 'de'] })`,
  // Full Chrome runtime object
  `window.chrome = { runtime: { connect: () => {}, sendMessage: () => {}, id: undefined }, loadTimes: () => ({ commitLoadTime: Date.now()/1000, connectionInfo: 'h2', finishDocumentLoadTime: Date.now()/1000, finishLoadTime: Date.now()/1000, firstPaintAfterLoadTime: 0, firstPaintTime: Date.now()/1000, navigationType: 'Other', npnNegotiatedProtocol: 'h2', requestTime: Date.now()/1000 - 0.3, startLoadTime: Date.now()/1000 - 0.3, wasAlternateProtocolAvailable: false, wasFetchedViaSpdy: true, wasNpnNegotiated: true }), csi: () => ({ pageT: Date.now(), startE: Date.now() - 300, onloadT: Date.now() }), app: { isInstalled: false, getDetails: () => null, getIsInstalled: () => false, installState: () => 'disabled' } }`,
  // Permissions
  `const originalQuery = window.navigator.permissions.query.bind(window.navigator.permissions); window.navigator.permissions.query = (parameters) => (parameters.name === 'notifications' ? Promise.resolve({ state: Notification.permission }) : originalQuery(parameters))`,
  // WebGL vendor/renderer (look like real GPU)
  `const getParameter = WebGLRenderingContext.prototype.getParameter; WebGLRenderingContext.prototype.getParameter = function(param) { if (param === 37445) return 'Google Inc. (NVIDIA)'; if (param === 37446) return 'ANGLE (NVIDIA, NVIDIA GeForce GTX 1650 Direct3D11 vs_5_0 ps_5_0, D3D11)'; return getParameter.call(this, param); }`,
  // Connection API
  `Object.defineProperty(navigator, 'connection', { get: () => ({ effectiveType: '4g', rtt: 50, downlink: 10, saveData: false }) })`,
  // Hardware concurrency
  `Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 8 })`,
  // Device memory
  `Object.defineProperty(navigator, 'deviceMemory', { get: () => 8 })`,
  // Platform
  `Object.defineProperty(navigator, 'platform', { get: () => 'Win32' })`,
];
console.log('🥷 Stealth evasions loaded');
import http from 'http';
import { spawn } from 'child_process';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// --- Config ---
const SESSIONS_DIR = process.env.LOCK_ME_IN_SESSIONS_DIR || '/data/home/.browser-sessions';
const CLOUDFLARED = process.env.LOCK_ME_IN_CLOUDFLARED || findBinary('cloudflared');
const DEFAULT_PORT = parseInt(process.env.LOCK_ME_IN_PORT || '18850');
const DEFAULT_TIMEOUT = 15 * 60 * 1000; // 15 min auto-close

// --- Args ---
const args = process.argv.slice(2);
const targetUrl = args.find(a => a.startsWith('http')) || 'https://example.com';
const sessionName = args.find(a => !a.startsWith('http') && !a.startsWith('--')) || 'default';
const portArg = args.find(a => a.startsWith('--port='));
const timeoutArg = args.find(a => a.startsWith('--timeout='));
const proxyPort = portArg ? parseInt(portArg.split('=')[1]) : DEFAULT_PORT;
const timeout = timeoutArg ? parseInt(timeoutArg.split('=')[1]) * 1000 : DEFAULT_TIMEOUT;

const sessionDir = path.join(SESSIONS_DIR, sessionName);
const storageFile = path.join(sessionDir, 'storage.json');
const metaFile = path.join(sessionDir, 'meta.json');

function findBinary(name) {
  const paths = [
    `/data/home/.local/bin/${name}`,
    `/usr/local/bin/${name}`,
    `/usr/bin/${name}`
  ];
  return paths.find(p => fs.existsSync(p)) || name;
}

function findChrome() {
  const override = process.env.LOCK_ME_IN_CHROME_PATH;
  if (override && fs.existsSync(override)) return override;
  
  // Auto-detect from Playwright cache
  const pwBase = '/home/node/.cache/ms-playwright';
  try {
    const dirs = fs.readdirSync(pwBase).filter(d => d.startsWith('chromium-'));
    if (dirs.length > 0) {
      const p = path.join(pwBase, dirs[0], 'chrome-linux64', 'chrome');
      if (fs.existsSync(p)) return p;
    }
  } catch {}
  
  // Fallbacks
  const fallbacks = ['/usr/bin/chromium', '/usr/bin/google-chrome', '/usr/bin/chromium-browser'];
  return fallbacks.find(p => fs.existsSync(p)) || 'chromium';
}

function buildUI(sessionName, statusMessage) {
  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>lock-me-in — ${sessionName}</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: system-ui, -apple-system, sans-serif; background: #0f172a; color: #e2e8f0; padding: 12px; max-width: 1024px; margin: 0 auto; }
    h1 { font-size: 18px; margin-bottom: 8px; color: #38bdf8; display: flex; align-items: center; gap: 8px; }
    h1 span { font-size: 24px; }
    .status { background: #1e293b; padding: 8px 12px; border-radius: 8px; margin-bottom: 10px; font-size: 13px; border-left: 3px solid #38bdf8; }
    .screen-wrap { position: relative; margin-bottom: 10px; }
    img { max-width: 100%; border-radius: 8px; border: 2px solid #334155; cursor: crosshair; display: block; }
    .controls { display: flex; gap: 6px; margin: 8px 0; flex-wrap: wrap; }
    input[type=text] { flex: 1; min-width: 180px; padding: 8px 12px; border-radius: 6px; border: 1px solid #475569; background: #1e293b; color: #e2e8f0; font-size: 14px; }
    input[type=text]:focus { outline: none; border-color: #38bdf8; }
    button { padding: 8px 14px; border-radius: 6px; border: none; background: #334155; color: #e2e8f0; cursor: pointer; font-size: 13px; font-weight: 500; transition: background 0.15s; }
    button:hover { background: #475569; }
    button.primary { background: #0ea5e9; color: white; }
    button.primary:hover { background: #38bdf8; }
    button.warn { background: #d97706; color: white; }
    button.warn:hover { background: #f59e0b; }
    button.success { background: #059669; color: white; }
    button.success:hover { background: #10b981; }
    button.danger { background: #dc2626; color: white; }
    button.danger:hover { background: #ef4444; }
    .info { font-size: 11px; color: #64748b; margin-top: 6px; }
    .click-indicator { position: absolute; width: 20px; height: 20px; border: 2px solid #38bdf8; border-radius: 50%; pointer-events: none; transform: translate(-50%, -50%); animation: ping 0.5s ease-out forwards; }
    @keyframes ping { 0% { opacity: 1; transform: translate(-50%, -50%) scale(1); } 100% { opacity: 0; transform: translate(-50%, -50%) scale(2); } }
  </style>
</head>
<body>
  <h1><span>🔐</span> lock-me-in — ${sessionName}</h1>
  <div class="status" id="status">${statusMessage}</div>
  <div class="screen-wrap" id="screenWrap">
    <img id="screen" src="/screenshot" />
  </div>
  <div class="controls">
    <input type="text" id="input" placeholder="Type here, then press Send or Enter" onkeydown="if(event.key==='Enter')doType()" autofocus />
    <button class="primary" onclick="doType()">Send</button>
    <button onclick="doAction('tab')">Tab ⇥</button>
    <button onclick="doAction('enter')">Enter ↵</button>
    <button onclick="doAction('clear')">Clear</button>
    <button onclick="doAction('backspace')">⌫</button>
    <button onclick="doAction('back')">← Back</button>
    <button onclick="doAction('scroll-down')">↓ Scroll</button>
  </div>
  <div class="controls">
    <input type="text" id="navurl" placeholder="Navigate to URL..." onkeydown="if(event.key==='Enter')doNav()" />
    <button onclick="doNav()">Go</button>
    <button class="success" onclick="doAction('save')">💾 Save</button>
    <button class="danger" onclick="if(confirm('Save session and close?'))doAction('done')">✅ Done</button>
  </div>
  <div class="info">Click screenshot to click • Type + Send to input text • Save persists cookies • Done saves & closes</div>
  <script>
    let refreshInterval = setInterval(refresh, 2500);
    function refresh() { document.getElementById('screen').src = '/screenshot?' + Date.now(); }
    
    // Touch-friendly click handler
    const screenImg = document.getElementById('screen');
    screenImg.addEventListener('click', handleClick);
    screenImg.addEventListener('touchend', function(e) {
      e.preventDefault();
      const touch = e.changedTouches[0];
      handleClick({ clientX: touch.clientX, clientY: touch.clientY, target: screenImg });
    }, { passive: false });

    async function handleClick(e) {
      const img = document.getElementById('screen');
      const rect = img.getBoundingClientRect();
      const clientX = e.clientX || 0;
      const clientY = e.clientY || 0;
      const x = Math.round((clientX - rect.left) / rect.width * img.naturalWidth);
      const y = Math.round((clientY - rect.top) / rect.height * img.naturalHeight);
      // Visual feedback
      const dot = document.createElement('div');
      dot.className = 'click-indicator';
      dot.style.left = e.clientX - document.getElementById('screenWrap').getBoundingClientRect().left + 'px';
      dot.style.top = e.clientY - document.getElementById('screenWrap').getBoundingClientRect().top + 'px';
      document.getElementById('screenWrap').appendChild(dot);
      setTimeout(() => dot.remove(), 500);
      const r = await fetch('/click?x=' + x + '&y=' + y);
      const j = await r.json();
      setStatus(j.status);
      setTimeout(refresh, 400);
    }

    async function doType() {
      const el = document.getElementById('input');
      const text = el.value;
      if (!text) return;
      const r = await fetch('/type?text=' + encodeURIComponent(text));
      const j = await r.json();
      el.value = '';
      setStatus(j.status);
      setTimeout(refresh, 400);
    }

    async function doAction(action) {
      const endpoints = { save: '/save', done: '/done', enter: '/key?key=Enter', tab: '/key?key=Tab', back: '/back', 'scroll-down': '/scroll?dir=down', clear: '/clear', backspace: '/key?key=Backspace' };
      const r = await fetch(endpoints[action] || '/');
      const j = await r.json();
      setStatus(j.status);
      if (action === 'done') { clearInterval(refreshInterval); setTimeout(() => document.body.innerHTML = '<h1 style="color:#10b981;text-align:center;margin-top:40vh">✅ Session saved & closed</h1>', 1500); }
      else setTimeout(refresh, 500);
    }

    async function doNav() {
      const el = document.getElementById('navurl');
      const url = el.value;
      if (!url) return;
      setStatus('Navigating...');
      const r = await fetch('/navigate?url=' + encodeURIComponent(url));
      const j = await r.json();
      el.value = '';
      setStatus(j.status);
      setTimeout(refresh, 1000);
    }
    
    function setStatus(msg) { document.getElementById('status').textContent = msg; }
  </script>
</body>
</html>`;
}

async function main() {
  fs.mkdirSync(sessionDir, { recursive: true });

  const chromePath = findChrome();
  console.log(`🌐 Target: ${targetUrl}`);
  console.log(`📁 Session: ${sessionName} → ${sessionDir}`);
  console.log(`🔧 Chrome: ${chromePath}`);

  // Use persistent context for realistic browser fingerprint
  const userDataDir = path.join(sessionDir, 'chrome-profile');
  fs.mkdirSync(userDataDir, { recursive: true });
  // Clean stale locks from previous runs
  for (const f of ['SingletonLock', 'SingletonCookie', 'SingletonSocket']) {
    try { fs.unlinkSync(path.join(userDataDir, f)); } catch {}
  }

  const launchOpts = {
    executablePath: chromePath,
    headless: true,
    viewport: { width: 1920, height: 1080 },
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    locale: 'en-US',
    timezoneId: 'Europe/Vienna',
    screen: { width: 1920, height: 1080 },
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-gpu',
      '--disable-blink-features=AutomationControlled',
      '--disable-features=IsolateOrigins,site-per-process',
      '--disable-infobars',
      '--lang=en-US,en',
    ]
  };

  if (fs.existsSync(storageFile)) {
    launchOpts.storageState = storageFile;
    console.log('♻️  Loaded saved session');
  }

  const proxyUrl = process.env.OPENCLAW_PROXY_URL;
  if (proxyUrl) {
    const m = proxyUrl.match(/^https?:\/\/([^:]+):([^@]+)@([^:]+):(\d+)/);
    if (m) {
      launchOpts.proxy = { server: `http://${m[3]}:${m[4]}`, username: m[1], password: m[2] };
      console.log(`🔒 Proxy: ${m[3]}:${m[4]}`);
    }
  }

  const context = await chromium.launchPersistentContext(userDataDir, launchOpts);
  let page = context.pages()[0] || await context.newPage();

  // Inject stealth scripts before any navigation
  await context.addInitScript(STEALTH_SCRIPTS.join(';\n'));

  // Handle popups (OAuth social login windows)
  context.on('page', async (newPage) => {
    console.log(`🪟 Popup opened: ${newPage.url()}`);
    page = newPage;
    await newPage.waitForLoadState('domcontentloaded').catch(() => {});
  });

  console.log('📄 Loading page...');
  await page.goto(targetUrl, { waitUntil: 'domcontentloaded', timeout: 30000 }).catch(() => {});
  await page.waitForTimeout(2000);

  // Accept common cookie banners
  for (const sel of ['button:has-text("Accept")', 'button:has-text("Akzeptieren")', 'button:has-text("Accept all")']) {
    try { const btn = page.locator(sel).first(); if (await btn.isVisible({ timeout: 500 })) await btn.click(); } catch {}
  }

  let statusMessage = `Ready — ${targetUrl}`;

  // --- HTTP Server ---
  const server = http.createServer(async (req, res) => {
    const url = new URL(req.url, `http://localhost:${proxyPort}`);
    try {
      switch (url.pathname) {
        case '/':
          res.writeHead(200, { 'Content-Type': 'text/html' });
          res.end(buildUI(sessionName, statusMessage));
          break;
        case '/screenshot':
          const img = await page.screenshot({ type: 'jpeg', quality: 65 });
          res.writeHead(200, { 'Content-Type': 'image/jpeg', 'Cache-Control': 'no-store' });
          res.end(img);
          break;
        case '/click':
          await page.mouse.click(+url.searchParams.get('x'), +url.searchParams.get('y'));
          await page.waitForTimeout(300);
          json(res, { status: `Clicked (${url.searchParams.get('x')}, ${url.searchParams.get('y')})` });
          break;
        case '/type':
          await page.keyboard.type(url.searchParams.get('text'), { delay: 30 });
          json(res, { status: `Typed "${url.searchParams.get('text')}"` });
          break;
        case '/key':
          await page.keyboard.press(url.searchParams.get('key'));
          json(res, { status: `Key: ${url.searchParams.get('key')}` });
          break;
        case '/navigate':
          await page.goto(url.searchParams.get('url'), { waitUntil: 'domcontentloaded', timeout: 15000 });
          json(res, { status: `→ ${url.searchParams.get('url')}` });
          break;
        case '/back':
          try {
            await page.goBack({ waitUntil: 'domcontentloaded', timeout: 5000 });
            json(res, { status: '← Went back' });
          } catch (e) {
            // If goBack fails, try keyboard shortcut
            await page.keyboard.down('Alt');
            await page.keyboard.press('ArrowLeft');
            await page.keyboard.up('Alt');
            json(res, { status: '← Back (keyboard fallback)' });
          }
          break;
        case '/clear':
          // Select all text in current field and delete it
          await page.keyboard.press('Control+a');
          await page.keyboard.press('Backspace');
          json(res, { status: 'Cleared field' });
          break;
        case '/scroll':
          const dir = url.searchParams.get('dir') === 'up' ? -300 : 300;
          await page.mouse.wheel(0, dir);
          json(res, { status: `Scrolled ${dir > 0 ? 'down' : 'up'}` });
          break;
        case '/eval':
          // Execute JS on the page (for clicking tricky elements, etc.)
          const script = url.searchParams.get('js');
          try {
            const result = await page.evaluate(script);
            json(res, { status: `✓ eval: ${JSON.stringify(result)}`.slice(0, 200) });
          } catch (e) {
            json(res, { status: `✗ eval error: ${e.message}`.slice(0, 200) });
          }
          break;
        case '/click-text':
          // Click element containing specific text
          const text = url.searchParams.get('text');
          try {
            await page.getByText(text, { exact: false }).first().click({ timeout: 5000 });
            json(res, { status: `Clicked: "${text}"` });
          } catch (e) {
            json(res, { status: `Could not click "${text}": ${e.message}`.slice(0, 200) });
          }
          break;
        case '/save':
          await saveSession(context, storageFile, metaFile, sessionName, page.url());
          json(res, { status: '💾 Session saved!' });
          break;
        case '/done':
          await saveSession(context, storageFile, metaFile, sessionName, page.url());
          json(res, { status: '✅ Saved & closing...' });
          setTimeout(async () => { await context.close(); server.close(); process.exit(0); }, 1500);
          break;
        default:
          res.writeHead(404);
          res.end('Not found');
      }
    } catch (e) {
      json(res, { status: `Error: ${e.message}` }, 500);
    }
  });

  function json(res, data, code = 200) {
    res.writeHead(code, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(data));
  }

  server.listen(proxyPort, '0.0.0.0', () => {
    console.log(`🖥️  Server on port ${proxyPort}`);
  });

  // --- Cloudflared Tunnel ---
  console.log('🚇 Starting tunnel...');
  const tunnel = spawn(CLOUDFLARED, ['tunnel', '--url', `http://localhost:${proxyPort}`], { stdio: ['ignore', 'pipe', 'pipe'] });
  
  let tunnelUrl = null;
  const onData = (data) => {
    const m = data.toString().match(/(https:\/\/[a-z0-9-]+\.trycloudflare\.com)/);
    if (m && !tunnelUrl) {
      tunnelUrl = m[1];
      console.log(`\n🔗 LOGIN URL: ${tunnelUrl}\n`);
    }
  };
  tunnel.stdout.on('data', onData);
  tunnel.stderr.on('data', onData);

  // Auto-close after timeout
  if (timeout > 0) {
    setTimeout(async () => {
      console.log('⏰ Timeout — saving and closing...');
      await saveSession(context, storageFile, metaFile, sessionName, page.url());
      await context.close();
      tunnel.kill();
      server.close();
      process.exit(0);
    }, timeout);
  }

  // Graceful shutdown
  async function cleanup() {
    try { await saveSession(context, storageFile, metaFile, sessionName, page.url()); } catch {}
    try { await context.close(); } catch {}
    try { tunnel.kill(); } catch {}
    try { server.close(); } catch {}
    process.exit(0);
  }
  process.on('SIGINT', cleanup);
  process.on('SIGTERM', cleanup);
}

async function saveSession(context, storageFile, metaFile, sessionName, currentUrl) {
  const state = await context.storageState();
  fs.writeFileSync(storageFile, JSON.stringify(state, null, 2));
  fs.writeFileSync(metaFile, JSON.stringify({
    session: sessionName,
    lastUrl: currentUrl,
    savedAt: new Date().toISOString(),
    cookieCount: state.cookies?.length || 0
  }, null, 2));
  console.log(`💾 Saved: ${state.cookies?.length || 0} cookies`);
}

main().catch(e => { console.error('Fatal:', e.message); process.exit(1); });
