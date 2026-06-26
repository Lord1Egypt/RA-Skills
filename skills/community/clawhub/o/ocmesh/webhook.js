/**
 * webhook.js
 * Push notifications to your OpenClaw agent (or any HTTP endpoint)
 * when events arrive on the mesh — no polling required.
 *
 * Events fired:
 *   peer.discovered   → new peer found
 *   peer.handshaked   → peer completed handshake
 *   message.received  → incoming DM
 *   group.message     → incoming group message
 *   receipt.delivered → peer delivered your message
 *   receipt.read      → peer read your message
 */

const http = require('http');
const https = require('https');
const crypto = require('crypto');

let config = null;

function start(cfg) {
  config = cfg;
  if (cfg.webhook?.enabled && cfg.webhook?.url) {
    console.log(`[webhook] Push enabled → ${cfg.webhook.url}`);
  }
}

async function fire(eventType, payload) {
  if (!config?.webhook?.enabled || !config?.webhook?.url) return;

  const body = JSON.stringify({
    event: eventType,
    ts: Date.now(),
    payload,
  });

  const url = new URL(config.webhook.url);
  const isHttps = url.protocol === 'https:';
  const lib = isHttps ? https : http;

  const headers = {
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(body),
    'X-Ocmesh-Event': eventType,
  };

  // HMAC signature if secret is set
  if (config.webhook.secret) {
    const sig = crypto
      .createHmac('sha256', config.webhook.secret)
      .update(body)
      .digest('hex');
    headers['X-Ocmesh-Signature'] = `sha256=${sig}`;
  }

  const options = {
    hostname: url.hostname,
    port: url.port || (isHttps ? 443 : 80),
    path: url.pathname + url.search,
    method: 'POST',
    headers,
    timeout: 5000,
  };

  return new Promise((resolve) => {
    const req = lib.request(options, (res) => {
      res.resume();
      resolve(res.statusCode);
    });

    req.on('error', (err) => {
      console.error(`[webhook] Delivery failed (${eventType}):`, err.message);
      resolve(null);
    });

    req.on('timeout', () => {
      req.destroy();
      console.error(`[webhook] Timeout (${eventType})`);
      resolve(null);
    });

    req.write(body);
    req.end();
  });
}

module.exports = { start, fire };
