#!/usr/bin/env node
// Inject PageController + helpers into a browser page via CDP HTTP protocol
// Usage: node inject-cdp.mjs <target_id> [cdp_host]
import { readFileSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';
const __dirname = dirname(fileURLToPath(import.meta.url));
const targetId = process.argv[2];
const cdpHost = process.argv[3] || 'http://127.0.0.1:18800';

if (!targetId) { console.error('Usage: node inject-cdp.mjs <target_id>'); process.exit(1); }

const pcJs = readFileSync(join(__dirname, 'page-controller-global.js'), 'utf8');
const injectJs = readFileSync(join(__dirname, 'inject.js'), 'utf8');

// Use fetch-based CDP (no ws needed)
// We need to use the /json/protocol to send commands... but CDP requires WebSocket.
// Alternative: use Deno-style or node built-in WebSocket (Node 22+)

const listResp = await fetch(`${cdpHost}/json`);
const pages = await listResp.json();
const target = pages.find(p => p.id === targetId);
if (!target) { console.error('Target not found'); process.exit(1); }

const ws = new globalThis.WebSocket(target.webSocketDebuggerUrl);

ws.addEventListener('open', () => {
  ws.send(JSON.stringify({
    id: 1,
    method: 'Runtime.evaluate',
    params: {
      expression: pcJs + ';\n' + injectJs,
      awaitPromise: false,
      returnByValue: true
    }
  }));
});

ws.addEventListener('message', (ev) => {
  const msg = JSON.parse(typeof ev.data === 'string' ? ev.data : ev.data.toString());
  if (msg.id === 1) {
    if (msg.result?.result?.value) {
      console.log('✅', msg.result.result.value);
    } else if (msg.result?.exceptionDetails) {
      console.error('❌', JSON.stringify(msg.result.exceptionDetails, null, 2));
    } else {
      console.log(JSON.stringify(msg.result, null, 2));
    }
    ws.close();
  }
});

ws.addEventListener('error', (e) => { console.error('WS error:', e.message); process.exit(1); });
