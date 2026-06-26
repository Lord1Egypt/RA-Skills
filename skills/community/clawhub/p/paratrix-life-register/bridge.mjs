/**
 * bridge.mjs — Bridge Server + Embedded HTML
 *
 * Single-tab bridge between Node.js and browser wallet extensions.
 */

import http from 'node:http';
import { exec as execCallback } from 'node:child_process';
import { promisify } from 'node:util';

const execAsync = promisify(execCallback);

function log(emoji, msg) { console.log(`${emoji} ${msg}`); }

// ═══════════════════════════════════════════════════════════════
// Embedded HTML Bridge Page (Single-Page, Fully Automatic)
// ═══════════════════════════════════════════════════════════════

export const BRIDGE_HTML = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>Karpak Wallet Authorization</title>
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { font-family:-apple-system,system-ui,sans-serif; background:#0a0a0a; color:#e0e0e0;
         display:flex; align-items:center; justify-content:center; min-height:100vh;
         min-height:100dvh; padding:16px; }
  .card { background:#1a1a2e; border-radius:16px; padding:32px 24px; max-width:520px; width:100%;
          text-align:center; box-shadow:0 8px 32px rgba(0,0,0,.4); }
  .step { display:inline-block; background:#7c5cfc22; color:#7c5cfc; font-size:12px; font-weight:600;
          padding:4px 12px; border-radius:12px; margin-bottom:12px; letter-spacing:.5px; }
  h2 { margin-bottom:10px; font-size:22px; color:#e0e0e0; }
  .hint { margin:16px 0 8px; color:#f0c040; font-size:15px; font-weight:600; line-height:1.6; }
  .detail { margin:8px 0; color:#888; font-size:13px; line-height:1.6; }
  .address { font-family:monospace; color:#7c5cfc; font-size:12px; background:#7c5cfc11;
             padding:6px 12px; border-radius:6px; word-break:break-all; margin:10px 0; }
  .status { font-size:13px; padding:10px 16px; border-radius:8px; margin:16px 0; }
  .status.pending  { background:#2a2a1e; color:#f0c040; }
  .status.success  { background:#1e2a1e; color:#40f060; }
  .status.error    { background:#2a1e1e; color:#f04040; }
  .spinner { display:inline-block; width:18px; height:18px; border:2px solid #333;
             border-top-color:#7c5cfc; border-radius:50%; animation:spin .8s linear infinite;
             vertical-align:middle; margin-right:8px; }
  @keyframes spin { to { transform:rotate(360deg); } }
  .icon { font-size:40px; margin-bottom:8px; }
  .wallet-list { display:flex; flex-direction:column; gap:10px; width:100%; margin-top:12px; }
  .wallet-btn { display:flex; align-items:center; gap:12px; background:#252540; border:1px solid #3a3a5c;
                border-radius:10px; padding:12px 16px; cursor:pointer; transition:all .15s; width:100%;
                text-align:left; color:#e0e0e0; font-size:14px; -webkit-tap-highlight-color:transparent; }
  .wallet-btn:active { border-color:#7c5cfc; background:#2e2e50; }
  .wallet-btn .wallet-icon { width:28px; height:28px; display:flex; align-items:center;
                              justify-content:center; font-size:22px; background:#333; border-radius:6px; }
  .wallet-btn .wallet-name { font-weight:600; }
  .wallet-btn .wallet-tag { font-size:11px; color:#888; margin-left:auto; }
</style>
</head>
<body>
<div class="card">
  <div class="step" id="step"></div>
  <div class="icon" id="icon">&#x1F517;</div>
  <h2 id="title"></h2>
  <p class="hint" id="hint"></p>
  <p class="detail" id="detail"></p>
  <div class="address" id="addr" style="display:none"></div>
  <div class="status" id="status" style="display:none"></div>
  <div class="wallet-list" id="wallets" style="display:none"></div>
</div>
<script>
(async () => {
  const titleEl = document.getElementById('title');
  const hintEl  = document.getElementById('hint');
  const detailEl = document.getElementById('detail');
  const statEl  = document.getElementById('status');
  const stepEl  = document.getElementById('step');
  const iconEl  = document.getElementById('icon');
  const addrEl  = document.getElementById('addr');

  function showStep(t)   { stepEl.textContent = t; stepEl.style.display = 'inline-block'; }
  function showHint(t)   { hintEl.textContent = t; hintEl.style.display = 'block'; }
  function showDetail(t) { detailEl.textContent = t; detailEl.style.display = 'block'; }
  function showAddress(t){ addrEl.textContent = t; addrEl.style.display = 'block'; }
  function showStatus(cls, t) { statEl.style.display='block'; statEl.className='status '+cls; statEl.innerHTML=t; }

  function fail(msg) {
    showStatus('error', msg);
    titleEl.textContent = 'Operation Failed';
    iconEl.innerHTML = '&#x274C;';
    hintEl.style.display = 'none';
  }

  async function submit(payload) {
    for (let i = 0; i < 3; i++) {
      try {
        await fetch('/submit', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload) });
        return;
      } catch(e) {
        if (i < 2) await new Promise(r => setTimeout(r, 1000));
      }
    }
  }

  async function requestWithRetry(provider, method, params, retries = 3) {
    for (let i = 0; i < retries; i++) {
      try {
        return await provider.request({ method, params });
      } catch (e) {
        const msg = e.message || '';
        if ((msg.includes('selectExtension') || msg.includes('Unexpected error')) && i < retries - 1) {
          showStatus('pending', '<span class="spinner"></span> Retrying... (' + (i+1) + '/' + retries + ')');
          await new Promise(r => setTimeout(r, (i + 1) * 2000));
          continue;
        }
        throw e;
      }
    }
  }

  async function nextAction() {
    for (let i = 0; i < 5; i++) {
      try {
        const resp = await fetch('/next-action');
        const cmd = await resp.json();
        if (cmd.action === 'ping') continue;
        return cmd;
      } catch(e) {
        if (i < 4) await new Promise(r => setTimeout(r, 2000));
        else throw e;
      }
    }
  }

  // ── Step 0: Wait for wallet extensions to initialize ──
  // Extensions inject window.ethereum asynchronously; the 'ethereum#initialized'
  // event fires once they are ready.  We also wait a short grace period so that
  // multiple extensions have time to finish their setup before we start probing.
  showStatus('pending', '<span class="spinner"></span> Detecting wallet extensions...');

  function waitForEthereum(timeout = 3000) {
    return new Promise((resolve) => {
      if (window.ethereum) { resolve(window.ethereum); return; }
      const handler = () => { resolve(window.ethereum); };
      window.addEventListener('ethereum#initialized', handler, { once: true });
      setTimeout(() => {
        window.removeEventListener('ethereum#initialized', handler);
        resolve(window.ethereum || null);
      }, timeout);
    });
  }

  const _initialEthereum = await waitForEthereum();

  // Small additional delay so that *other* extensions that loaded slightly after
  // the first one also get a chance to patch window.ethereum.providers.
  if (_initialEthereum) {
    await new Promise(r => setTimeout(r, 500));
  }

  if (!window.ethereum) {
    titleEl.textContent = 'Wallet Not Found';
    showHint('Please install MetaMask or another Web3 wallet extension.');
    showStatus('error', 'No window.ethereum detected');
    iconEl.innerHTML = '&#x1F98A;';
    await submit({ error: 'NO_WALLET', message: 'No wallet extension found' });
    return;
  }

  // ── EIP-6963 Discovery (avoids multi-extension conflicts) ──
  // Modern wallets announce themselves via EIP-6963 which gives us
  // isolated provider instances — no more shared window.ethereum proxy.
  const eip6963Providers = [];
  function onAnnouncement(evt) {
    eip6963Providers.push(evt.detail);
  }

  // Wallets that do NOT support BSC — hidden from selection
  const BSC_UNSUPPORTED = new Set(['phantom']);

  function isBscCompatible(name) {
    return !BSC_UNSUPPORTED.has((name || '').toLowerCase());
  }

  const WALLET_META = [
    { flag: 'isMetaMask',       name: 'MetaMask',        icon: '&#x1F98B;' },
    { flag: 'isCoinbaseWallet', name: 'Coinbase Wallet',  icon: '&#x1F4B0;' },
    { flag: 'isTrust',          name: 'Trust Wallet',     icon: '&#x1F6E1;' },
    { flag: 'isBraveWallet',    name: 'Brave Wallet',     icon: '&#x1F981;' },
    { flag: 'isOkxWallet',      name: 'OKX Wallet',       icon: '&#x26D4;' },
    { flag: 'isBitKeep',        name: 'BitKeep',          icon: '&#x1F4DA;' },
    { flag: 'isTokenPocket',    name: 'TokenPocket',      icon: '&#x1F4CB;' },
  ];

  function walletName(p, i) { for (const m of WALLET_META) { if (p[m.flag]) return m.name; } return 'Wallet ' + (i+1); }
  function walletIcon(p)    { for (const m of WALLET_META) { if (p[m.flag]) return m.icon; } return '&#x1F517;'; }

  function walletNameFromInfo(info) {
    const name = (info.name || '').toLowerCase();
    for (const m of WALLET_META) {
      if (name.includes(m.name.toLowerCase())) return m.name;
    }
    return info.name || 'Unknown Wallet';
  }

  function walletIconFromInfo(info) {
    const name = (info.name || '').toLowerCase();
    for (const m of WALLET_META) {
      if (name.includes(m.name.toLowerCase())) return m.icon;
    }
    return '&#x1F517;';
  }

  // Listen for EIP-6963 announcements for a short window
  window.addEventListener('eip6963:announceProvider', onAnnouncement);
  window.dispatchEvent(new Event('eip6963:requestProvider'));
  await new Promise(r => setTimeout(r, 1000));
  window.removeEventListener('eip6963:announceProvider', onAnnouncement);

  // ── Provider Selection ──
  let ethereum;

  // Filter out wallets that don't support BSC
  const bscProviders = eip6963Providers.filter(d => isBscCompatible(walletNameFromInfo(d.info)));

  if (bscProviders.length >= 1) {
    // EIP-6963 path — each provider is isolated, no MetaMask routing conflicts
    if (bscProviders.length > 1) {
      titleEl.textContent = 'Select a Wallet';
      iconEl.innerHTML = '&#x1F517;';
      showHint('Multiple wallet extensions detected. Pick one to continue.');
      const listEl = document.getElementById('wallets');
      listEl.style.display = 'flex';
      const selectedDetail = await new Promise((resolve) => {
        bscProviders.forEach((detail) => {
          const p = detail.provider;
          const info = detail.info;
          const btn = document.createElement('button');
          btn.className = 'wallet-btn';
          btn.innerHTML = '<span class="wallet-icon">' + walletIconFromInfo(info) + '</span>'
            + '<span class="wallet-name">' + walletNameFromInfo(info) + '</span>'
            + '<span class="wallet-tag">EVM</span>';
          btn.onclick = () => { listEl.style.display = 'none'; resolve(detail); };
          listEl.appendChild(btn);
        });
      });
      ethereum = selectedDetail.provider;
      showDetail('Selected: ' + walletNameFromInfo(selectedDetail.info));
    } else {
      ethereum = bscProviders[0].provider;
    }
  } else {
    // Legacy path — fall back to window.ethereum.providers
    function detectProviders() {
      const base = window.ethereum;
      if (!base) return [];
      if (base.providers && Array.isArray(base.providers) && base.providers.length > 1) {
        return base.providers.filter(p => p && typeof p.request === 'function');
      }
      return [base];
    }

    const allProviders = detectProviders();
    const providers = allProviders.filter(p => isBscCompatible(walletName(p, allProviders.indexOf(p))));

    if (providers.length > 1) {
      titleEl.textContent = 'Select a Wallet';
      iconEl.innerHTML = '&#x1F517;';
      showHint('Multiple wallet extensions detected. Pick one to continue.');
      const listEl = document.getElementById('wallets');
      listEl.style.display = 'flex';
      ethereum = await new Promise((resolve) => {
        providers.forEach((p, i) => {
          const btn = document.createElement('button');
          btn.className = 'wallet-btn';
          btn.innerHTML = '<span class="wallet-icon">' + walletIcon(p) + '</span>'
            + '<span class="wallet-name">' + walletName(p, i) + '</span>'
            + '<span class="wallet-tag">EVM</span>';
          btn.onclick = () => { listEl.style.display = 'none'; resolve(p); };
          listEl.appendChild(btn);
        });
      });
      showDetail('Selected: ' + walletName(ethereum));
    } else {
      ethereum = providers[0];
    }

    // Override window.ethereum with the selected provider so that MetaMask's
    // internal routing (selectExtension) does not try to proxy through the
    // multi-provider wrapper any more.
    window.ethereum = ethereum;
  }

  // ── Step 1: Auto Connect ──
  showStep('Step 1 / 3');
  iconEl.innerHTML = '&#x1F517;';
  titleEl.textContent = 'Connecting Wallet';
  showHint('Please confirm in your wallet popup.');
  showStatus('pending', '<span class="spinner"></span> Waiting for wallet confirmation...');

  let address;
  try {
    const accounts = await requestWithRetry(ethereum, 'eth_requestAccounts', []);
    address = accounts[0];
  } catch (e) {
    fail('Wallet connection failed: ' + e.message);
    await submit({ error: 'WALLET_DENIED', message: e.message });
    return;
  }
  showAddress(address);
  showStatus('success', 'Wallet connected!');
  await submit({ address });

  // ── Main Loop: auto-process commands from Node.js ──
  while (true) {
    const cmd = await nextAction();

    if (cmd.action === 'sign') {
      showStep('Step 2 / 3 · Authentication');
      iconEl.innerHTML = '&#x270D;&#xFE0F;';
      titleEl.textContent = 'Signing Message';
      showHint('Please sign in your wallet popup.');
      showDetail('This is a SIWE login signature. No gas fees.');
      showStatus('pending', '<span class="spinner"></span> Waiting for signature...');

      try {
        const signature = await requestWithRetry(ethereum, 'personal_sign', [cmd.message, cmd.address || address]);
        showStatus('success', 'Signature obtained!');
        await submit({ signature, address: cmd.address || address });
      } catch (e) {
        fail('Signing failed: ' + e.message);
        await submit({ error: e.code === 4001 ? 'SIGNATURE_REJECTED' : 'SIGN_FAILED', message: e.message });
        return;
      }

    } else if (cmd.action === 'mint') {
      showStep('Step 3 / 3 · Mint SBT');
      iconEl.innerHTML = '&#x1F48E;';
      titleEl.textContent = 'Minting Soulbound Token';
      showHint('Please confirm the transaction in your wallet popup.');
      showDetail('This transaction only requires gas fees.');
      showStatus('pending', '<span class="spinner"></span> Waiting for confirmation...');

      try {
        const txHash = await requestWithRetry(ethereum, 'eth_sendTransaction', [{
          from: cmd.address || address, to: cmd.to, data: cmd.data, value: cmd.value || '0x0', gas: '0xF4240'
        }]);
        showStatus('success', 'Transaction submitted! Hash: ' + txHash.slice(0, 10) + '...');
        await submit({ txHash, address: cmd.address || address });
      } catch (e) {
        fail('Transaction failed: ' + e.message);
        await submit({ error: e.code === 4001 ? 'TX_REJECTED' : 'TX_FAILED', message: e.message });
        return;
      }

    } else if (cmd.action === 'done') {
      iconEl.innerHTML = '&#x2705;';
      titleEl.textContent = cmd.title || 'All Done!';
      showHint(cmd.message || 'Registration complete. You can close this page.');
      showDetail('');
      showStatus('success', 'Success');
      return;

    } else if (cmd.action === 'error') {
      fail(cmd.message || 'Unknown error');
      return;

    } else {
      fail('Unknown action: ' + cmd.action);
      await submit({ error: 'UNKNOWN_ACTION', message: cmd.action });
      return;
    }
  }
})();
</script>
</body>
</html>`;

// ═══════════════════════════════════════════════════════════════
// Bridge Server
// ═══════════════════════════════════════════════════════════════

export class BridgeServer {
  constructor(port, host = 'localhost') {
    this.server = null;
    this.port = port;
    this.host = host;
    this.base = `http://${host}:${port}`;
    this._resolveSubmit = null;
    this._actionQueue = [];
    this._actionWaiters = [];
  }

  async start() {
    return new Promise((resolve, reject) => {
      this.server = http.createServer((req, res) => this._handle(req, res));
      this.server.listen(this.port, this.host, () => {
        log('>>>', `Bridge server listening on ${this.base}`);
        resolve();
      });
      this.server.on('error', reject);
    });
  }

  _handle(req, res) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    if (req.method === 'OPTIONS') { res.writeHead(204); res.end(); return; }

    const url = new URL(req.url, this.base);

    if (url.pathname === '/' && req.method === 'GET') {
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(BRIDGE_HTML);
      return;
    }

    if (url.pathname === '/next-action' && req.method === 'GET') {
      if (this._actionQueue.length > 0) {
        const action = this._actionQueue.shift();
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(action));
      } else {
        let settled = false;
        const waiter = (action) => {
          if (settled) return;
          settled = true;
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify(action));
        };
        this._actionWaiters.push(waiter);
        req.on('close', () => {
          if (!settled) {
            settled = true;
            const idx = this._actionWaiters.indexOf(waiter);
            if (idx !== -1) this._actionWaiters.splice(idx, 1);
          }
        });
        setTimeout(() => {
          if (!settled) {
            settled = true;
            const idx = this._actionWaiters.indexOf(waiter);
            if (idx !== -1) this._actionWaiters.splice(idx, 1);
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ action: 'ping' }));
          }
        }, 30000);
      }
      return;
    }

    if (url.pathname === '/submit' && req.method === 'POST') {
      const chunks = [];
      req.on('data', (c) => chunks.push(c));
      req.on('end', () => {
        try {
          const payload = JSON.parse(Buffer.concat(chunks).toString());
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end('{"ok":true}');
          if (this._resolveSubmit) {
            const resolve = this._resolveSubmit;
            this._resolveSubmit = null;
            resolve(payload);
          }
        } catch (e) {
          res.writeHead(400);
          res.end('{"error":"invalid json"}');
        }
      });
      return;
    }

    if (url.pathname === '/favicon.ico') {
      res.writeHead(204);
      res.end();
      return;
    }

    if (url.pathname === '/health') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end('{"status":"ok"}');
      return;
    }

    res.writeHead(404);
    res.end('Not Found');
  }

  pushAction(action, params = {}) {
    const item = { action, ...params };
    if (this._actionWaiters.length > 0) {
      const waiter = this._actionWaiters.shift();
      waiter(item);
    } else {
      this._actionQueue.push(item);
    }
  }

  async waitForSubmit(timeoutMs = 120000) {
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        this._resolveSubmit = null;
        reject(new Error(`Timeout: no response within ${timeoutMs / 1000}s`));
      }, timeoutMs);

      this._resolveSubmit = (payload) => {
        clearTimeout(timer);
        this._resolveSubmit = null;
        resolve(payload);
      };
    });
  }

  openFlow() {
    const url = `${this.base}/`;
    log('>>>', `Opening browser: ${url}`);

    const cmd = process.platform === 'darwin'
      ? `open "${url}"`
      : process.platform === 'win32'
        ? `start "" "${url}"`
        : `xdg-open "${url}" 2>/dev/null || sensible-browser "${url}" 2>/dev/null`;

    execAsync(cmd, { timeout: 5000 }).catch(e => log('!', `Browser open failed: ${e.message}`));
  }

  async close() {
    if (this.server) {
      return new Promise((resolve) => {
        this.server.close(() => { log('>>>', 'Bridge server closed'); resolve(); });
      });
    }
  }
}
