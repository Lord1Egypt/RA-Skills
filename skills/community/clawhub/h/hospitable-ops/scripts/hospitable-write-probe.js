#!/usr/bin/env node
const https = require('https');
const token = process.env.HOSPITABLE_TOKEN;
const base = process.env.HOSPITABLE_BASE_URL || 'https://public.api.hospitable.com/v2/';
if (!token) {
  console.error(JSON.stringify({ error: 'HOSPITABLE_TOKEN is required' }, null, 2));
  process.exit(2);
}
const args = process.argv.slice(2);
const method = args[0] || 'OPTIONS';
const pathArg = args[1] || 'properties';
const body = args[2] || null;
function request(pathname, method, body) {
  return new Promise((resolve, reject) => {
    const url = new URL(pathname, base);
    const req = https.request(url, {
      method,
      headers: {
        Authorization: `Bearer ${token}`,
        Accept: 'application/json',
        ...(body ? { 'Content-Type': 'application/json' } : {})
      }
    }, (res) => {
      let raw = '';
      res.on('data', c => raw += c);
      res.on('end', () => {
        let parsed = null;
        try { parsed = JSON.parse(raw); } catch (_) {}
        resolve({ method, url: url.toString(), statusCode: res.statusCode, headers: res.headers, body: parsed ?? raw });
      });
    });
    req.on('error', reject);
    if (body) req.write(body);
    req.end();
  });
}
request(pathArg, method, body).then(r => console.log(JSON.stringify(r, null, 2))).catch(err => {
  console.error(JSON.stringify({ error: String(err) }, null, 2));
  process.exit(1);
});
