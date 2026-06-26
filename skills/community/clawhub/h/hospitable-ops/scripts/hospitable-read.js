#!/usr/bin/env node
const https = require('https');

const token = process.env.HOSPITABLE_TOKEN;
const base = process.env.HOSPITABLE_BASE_URL || 'https://public.api.hospitable.com/v2/';

function usage() {
  console.error(`Usage:
  hospitable-read.js properties [--per-page N]
  hospitable-read.js reservations --property <uuid> [--per-page N]
  hospitable-read.js calendar --property <uuid> --start YYYY-MM-DD --end YYYY-MM-DD
`);
  process.exit(2);
}
if (!token) {
  console.error(JSON.stringify({ error: 'HOSPITABLE_TOKEN is required' }, null, 2));
  process.exit(2);
}
const args = process.argv.slice(2);
if (!args.length) usage();
function getArg(flag, required = false) {
  const i = args.indexOf(flag);
  if (i === -1) return required ? usage() : null;
  const v = args[i + 1];
  if (!v || v.startsWith('--')) usage();
  return v;
}
function requestJson(path) {
  return new Promise((resolve, reject) => {
    const url = new URL(path, base);
    const req = https.request(url, { method: 'GET', headers: { Authorization: `Bearer ${token}`, Accept: 'application/json' } }, (res) => {
      let body = '';
      res.on('data', c => body += c);
      res.on('end', () => {
        let parsed = null;
        try { parsed = JSON.parse(body); } catch (_) {}
        resolve({ statusCode: res.statusCode, headers: res.headers, body: parsed ?? body });
      });
    });
    req.on('error', reject);
    req.end();
  });
}
(async () => {
  const cmd = args[0];
  const perPage = getArg('--per-page') || '5';
  let result;
  if (cmd === 'properties') {
    result = await requestJson(`properties?per_page=${encodeURIComponent(perPage)}`);
  } else if (cmd === 'reservations') {
    const property = getArg('--property', true);
    result = await requestJson(`reservations?properties[]=${encodeURIComponent(property)}&per_page=${encodeURIComponent(perPage)}`);
  } else if (cmd === 'calendar') {
    const property = getArg('--property', true);
    const start = getArg('--start', true);
    const end = getArg('--end', true);
    result = await requestJson(`properties/${encodeURIComponent(property)}/calendar?start_date=${encodeURIComponent(start)}&end_date=${encodeURIComponent(end)}`);
  } else usage();
  console.log(JSON.stringify(result, null, 2));
})();
