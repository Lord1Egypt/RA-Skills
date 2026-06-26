/**
 * nostr.js
 * Manages WebSocket connections to Nostr relays.
 * Handles publishing events and subscribing to filters.
 */

const WebSocket = require('ws');
const { RELAYS } = require('./relays');

const connections = new Map(); // url → ws

function connectAll(onEvent) {
  for (const url of RELAYS) {
    connect(url, onEvent);
  }
}

function connect(url, onEvent) {
  if (connections.has(url)) return;

  const ws = new WebSocket(url);
  connections.set(url, { ws, subs: [] });

  ws.on('open', () => {
    console.log(`[nostr] Connected: ${url}`);
    // Re-subscribe after reconnect
    const entry = connections.get(url);
    if (entry && entry.subs.length > 0) {
      for (const sub of entry.subs) {
        ws.send(JSON.stringify(sub));
      }
    }
  });

  ws.on('message', (raw) => {
    try {
      const msg = JSON.parse(raw.toString());
      if (msg[0] === 'EVENT' && msg[2]) {
        onEvent(msg[2], url);
      }
    } catch (_) {}
  });

  ws.on('close', () => {
    console.log(`[nostr] Disconnected: ${url} — reconnecting in 10s`);
    connections.delete(url);
    setTimeout(() => connect(url, onEvent), 10_000);
  });

  ws.on('error', (err) => {
    console.error(`[nostr] Error on ${url}:`, err.message);
  });
}

function subscribe(filter) {
  const subId = Math.random().toString(36).slice(2, 10);
  const req = ['REQ', subId, filter];

  for (const [url, entry] of connections) {
    entry.subs.push(req);
    if (entry.ws.readyState === WebSocket.OPEN) {
      entry.ws.send(JSON.stringify(req));
    }
  }

  return subId;
}

function publish(event) {
  const msg = JSON.stringify(['EVENT', event]);
  let sent = 0;

  for (const [url, entry] of connections) {
    if (entry.ws.readyState === WebSocket.OPEN) {
      entry.ws.send(msg);
      sent++;
    }
  }

  console.log(`[nostr] Published event kind=${event.kind} to ${sent} relays`);
}

module.exports = { connectAll, subscribe, publish };
