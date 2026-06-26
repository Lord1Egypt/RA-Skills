#!/bin/bash
# Inject PageController into a browser page via CDP
# Usage: bash inject-via-cdp.sh <ws_url>
# Or: bash inject-via-cdp.sh <target_id> [cdp_endpoint]

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET_ID="${1}"
CDP_ENDPOINT="${2:-http://127.0.0.1:18800}"

# Use node to inject via CDP Runtime.evaluate
node -e "
const fs = require('fs');
const http = require('http');

const scriptContent = fs.readFileSync('${SCRIPT_DIR}/page-controller-global.js', 'utf8');
const injectContent = fs.readFileSync('${SCRIPT_DIR}/inject.js', 'utf8');
const combined = scriptContent + ';\n' + injectContent;

// Use CDP to evaluate
const ws = require('ws') || null;

async function injectViaCDP() {
  // Get WebSocket URL for the target
  const listUrl = '${CDP_ENDPOINT}/json';
  const resp = await fetch(listUrl);
  const pages = await resp.json();
  const target = pages.find(p => p.id === '${TARGET_ID}');
  if (!target) {
    console.error('Target not found:', '${TARGET_ID}');
    process.exit(1);
  }
  
  const WebSocket = require('ws');
  const wsUrl = target.webSocketDebuggerUrl;
  const socket = new WebSocket(wsUrl);
  
  socket.on('open', () => {
    socket.send(JSON.stringify({
      id: 1,
      method: 'Runtime.evaluate',
      params: {
        expression: combined,
        awaitPromise: false,
        returnByValue: true
      }
    }));
  });
  
  socket.on('message', (data) => {
    const msg = JSON.parse(data.toString());
    if (msg.id === 1) {
      console.log(JSON.stringify(msg.result, null, 2));
      socket.close();
    }
  });
  
  socket.on('error', (err) => {
    console.error('WS error:', err.message);
    process.exit(1);
  });
}

injectViaCDP();
"
