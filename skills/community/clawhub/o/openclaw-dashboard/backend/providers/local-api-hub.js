'use strict';
/**
 * Local API Hub Provider
 *
 * Exposes two capabilities:
 *   1. GET  /ops/local-api-hub          — health + metadata (for Health panel)
 *   2. ANY  /local-api-hub/*            — transparent proxy to hub at port 3456
 *
 * Hub base URL: http://127.0.0.1:3456  (overridable via LOCAL_API_HUB_PORT/HOST env)
 */
const http = require('http');
const cfg  = require('../lib/config');
const { jsonReply, errorReply } = require('../lib/http-helpers');

const HUB_URL = cfg.LOCAL_API_HUB_URL; // e.g. http://127.0.0.1:3456

// ── Internal helpers ──────────────────────────────────────────────────────────

/** Fire a GET to hub and return parsed JSON. Rejects on network error or non-2xx. */
function hubGet(path, timeoutMs = 3000) {
  return new Promise((resolve, reject) => {
    const url = `${HUB_URL}${path}`;
    const req = http.get(url, { timeout: timeoutMs }, (res) => {
      const chunks = [];
      res.on('data', c => chunks.push(c));
      res.on('end', () => {
        try { resolve({ status: res.statusCode, body: JSON.parse(Buffer.concat(chunks).toString()) }); }
        catch (e) { reject(new Error(`Hub JSON parse error: ${e.message}`)); }
      });
    });
    req.on('timeout', () => { req.destroy(); reject(new Error('Hub request timed out')); });
    req.on('error', reject);
  });
}

/** Proxy any method + body to the hub. */
function hubProxy(req, res) {
  // Strip /local-api-hub prefix, pass the rest directly
  const upstreamPath = req.url.replace(/^\/local-api-hub/, '') || '/';

  const options = {
    hostname: cfg.LOCAL_API_HUB_HOST,
    port:     cfg.LOCAL_API_HUB_PORT,
    path:     upstreamPath,
    method:   req.method,
    headers:  {
      'content-type': req.headers['content-type'] || 'application/json',
      'user-agent':   'openclaw-dashboard-proxy/2.0',
    },
    timeout: 10000,
  };

  const proxy = http.request(options, (upRes) => {
    res.writeHead(upRes.statusCode, {
      'content-type': upRes.headers['content-type'] || 'application/json',
      'access-control-allow-origin': '*',
    });
    upRes.pipe(res);
  });

  proxy.on('timeout', () => {
    proxy.destroy();
    errorReply(res, 504, 'Local API Hub proxy timed out');
  });

  proxy.on('error', (err) => {
    // Hub likely not running
    if (err.code === 'ECONNREFUSED') {
      errorReply(res, 503, `Local API Hub not reachable at ${HUB_URL}`);
    } else {
      errorReply(res, 502, `Local API Hub proxy error: ${err.message}`);
    }
  });

  // Pipe request body for POST/PUT/PATCH
  req.pipe(proxy);
}

/** Proxy an exact root-level dashboard alias to the corresponding hub path. */
function hubAliasProxy(upstreamPath) {
  return (req, res) => {
    const originalUrl = req.url;
    const queryIndex = originalUrl.indexOf('?');
    const query = queryIndex >= 0 ? originalUrl.slice(queryIndex) : '';
    req.url = `${upstreamPath}${query}`;
    return hubProxy(req, res);
  };
}

// ── Route handlers ────────────────────────────────────────────────────────────

/** GET /ops/local-api-hub — health check + metadata for Health panel */
async function handleHubStatus(_req, res) {
  const started = Date.now();
  try {
    const { status, body } = await hubGet('/health');
    const latencyMs = Date.now() - started;

    // Also fetch routes for the metadata card
    let routes = null;
    try { ({ body: { routes } } = await hubGet('/routes', 2000)); } catch { /* non-fatal */ }

    jsonReply(res, 200, {
      ok: true,
      reachable: status >= 200 && status < 300,
      status,
      latencyMs,
      hubUrl: HUB_URL,
      service: body?.service || 'local-api-hub',
      module:  body?.module  || null,
      modules: body?.modules || [],
      port:    body?.port    || cfg.LOCAL_API_HUB_PORT,
      routes:  routes        || null,
    });
  } catch (err) {
    const latencyMs = Date.now() - started;
    jsonReply(res, 200, {
      ok: false,
      reachable: false,
      latencyMs,
      hubUrl: HUB_URL,
      error: err.code === 'ECONNREFUSED'
        ? `Not running (port ${cfg.LOCAL_API_HUB_PORT})`
        : err.message,
    });
  }
}

// ── Register ──────────────────────────────────────────────────────────────────

function register(router) {
  // Health / metadata — used by Dashboard Health panel
  router.add('GET', '/ops/local-api-hub', handleHubStatus);

  // Transparent proxy — all methods, dynamic path
  // Matches /local-api-hub, /local-api-hub/, /local-api-hub/content/write, etc.
  // Read-only proxy paths (GET only — dashboard is read-only)
  // Write paths (content/write, content/upsert, channel/:id/write|upsert) removed.
  const READ_PROXY_PATHS = [
    // Core
    '/local-api-hub/health',
    '/local-api-hub/targets',
    '/local-api-hub/schemas',
    '/local-api-hub/routes',
    '/local-api-hub/channels',
    '/local-api-hub/content/preview',
    // Spark
    '/local-api-hub/models/spark',
    '/local-api-hub/models/spark/health',
    '/local-api-hub/models/spark/status',
    '/local-api-hub/models/spark/metrics',
    // Model Routing
    '/local-api-hub/models/routing',
    '/local-api-hub/models/routing/active',
    '/local-api-hub/models/routing/history',
    '/local-api-hub/models/usage',
    // Ops
    '/local-api-hub/health/system',
    '/local-api-hub/ops/sessions',
    '/local-api-hub/ops/cron',
    // Dashboard
    '/local-api-hub/dashboard/summary',
    '/local-api-hub/dashboard/activity',
    '/local-api-hub/dashboard/metrics',
    '/local-api-hub/dashboard/alerts',
    '/local-api-hub/dashboard/usage/models/today',
    '/local-api-hub/dashboard/usage/models/history',
    '/local-api-hub/dashboard/usage/cron/summary',
    '/local-api-hub/dashboard/usage/cron/daily',
    // Memory
    '/local-api-hub/memory/stats',
    '/local-api-hub/memory/today',
    '/local-api-hub/memory/recent',
    // Ledger
    '/local-api-hub/ledger/summary',
    '/local-api-hub/ledger/today',
    '/local-api-hub/ledger/daily',
    '/local-api-hub/ledger/models',
    // Notify (read-only)
    '/local-api-hub/notify/queue',
  ];
  for (const p of READ_PROXY_PATHS) {
    router.add('GET', p, hubProxy);
  }

  // Dynamic routes
  // Channel routes (read-only)
  router.add('GET', '/local-api-hub/channel/:channelId/route',       hubProxy);
  router.add('GET', '/local-api-hub/channel/:channelId/route/:lane', hubProxy);
  // Ops detail routes
  router.add('GET', '/local-api-hub/ops/sessions/:key', hubProxy);
  router.add('GET', '/local-api-hub/ops/cron/:id', hubProxy);
  // Memory detail routes
  router.add('GET', '/local-api-hub/memory/:date', hubProxy);

  // Root-level dashboard usage aliases so frontend can call dashboard backend directly.
  router.add('GET', '/dashboard/usage/models/today', hubAliasProxy('/local-api-hub/dashboard/usage/models/today'));
  router.add('GET', '/dashboard/usage/models/history', hubAliasProxy('/local-api-hub/dashboard/usage/models/history'));
  router.add('GET', '/dashboard/usage/source/history', hubAliasProxy('/local-api-hub/dashboard/usage/source/history'));
  router.add('GET', '/dashboard/usage/cron/summary', hubAliasProxy('/local-api-hub/dashboard/usage/cron/summary'));
  router.add('GET', '/dashboard/usage/cron/trend', hubAliasProxy('/local-api-hub/dashboard/usage/cron/trend'));
  router.add('GET', '/dashboard/usage/cron/daily', hubAliasProxy('/local-api-hub/dashboard/usage/cron/daily'));
}

module.exports = { register };
