'use strict';

const https = require('https');
const http = require('http');
const { loadConfig } = require('./config');

function getServerUrl() {
  const cfg = loadConfig();
  const raw = cfg?.server?.url || process.env.PLANIT_SERVER_URL || 'http://8.216.37.65:3721';
  if (!raw) return null;
  const trimmed = String(raw).trim();
  if (trimmed.endsWith('/api')) return trimmed.slice(0, -4);
  if (trimmed.endsWith('/api/')) return trimmed.slice(0, -5);
  return trimmed;
}

async function postJson(path, body) {
  const base = getServerUrl();
  if (!base) throw new Error('PLANIT_SERVER_URL not set');

  const url = new URL(path, base);
  const payload = JSON.stringify(body || {});
  const secret = process.env.PLANIT_SECRET || '';

  return new Promise((resolve, reject) => {
    const lib = url.protocol === 'https:' ? https : http;
    const req = lib.request({
      hostname: url.hostname,
      port: url.port || (url.protocol === 'https:' ? 443 : 80),
      path: url.pathname + url.search,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload),
        ...(secret ? { 'Authorization': `Bearer ${secret}` } : {}),
      },
      timeout: 10000,
    }, (res) => {
      const chunks = [];
      res.on('data', (c) => chunks.push(c));
      res.on('end', () => {
        const raw = Buffer.concat(chunks).toString('utf8');
        let json = null;
        try { json = JSON.parse(raw); } catch { /* ignore */ }
        if (res.statusCode >= 400) {
          return reject(new Error(json?.error || json?.message || `HTTP ${res.statusCode}`));
        }
        resolve(json);
      });
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('timeout')); });
    req.write(payload);
    req.end();
  });
}

async function plan(message, skillConfig) {
  return postJson('/plan', { ...message, skillConfig: skillConfig || null });
}

async function telemetry(event) {
  try {
    return await postJson('/telemetry', event);
  } catch {
    return null;
  }
}

async function contribute(payload) {
  return postJson('/contributions', payload);
}

module.exports = { getServerUrl, postJson, plan, telemetry, contribute };
