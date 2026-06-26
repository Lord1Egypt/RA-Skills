#!/usr/bin/env node
// HTTP request utility - replaces curl for cross-platform compatibility
// Usage: node http-request.js <method> <url> [payload_file|-d <payload_json>]
const http = require('http');
const https = require('https');

const method = process.argv[2];
const url = new URL(process.argv[3]);
// Handle both: node http-request.js POST url -d '{"json"}'  OR  node http-request.js POST url < file
const payloadArg = process.argv[4];
let payload = null;

if (payloadArg === '-d' && process.argv[5]) {
  // Read from file path passed after -d
  const fs = require('fs');
  try {
    payload = fs.readFileSync(process.argv[5], 'utf8');
  } catch(e) {
    // Fall back to argv[5] as inline JSON
    payload = process.argv[5];
  }
} else if (payloadArg && payloadArg !== '-d') {
  const fs = require('fs');
  try {
    payload = fs.readFileSync(payloadArg, 'utf8');
  } catch(e) {
    payload = payloadArg;
  }
}

const options = {
  hostname: url.hostname,
  path: url.pathname + url.search,
  method: method,
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + process.env.DOUBAO_API_KEY,
  }
};

if (payload) {
  options.headers['Content-Length'] = Buffer.byteLength(payload);
}

const transport = url.protocol === 'https:' ? https : http;

const req = transport.request(options, function(res) {
  let body = '';
  res.on('data', function(chunk) { body += chunk; });
  res.on('end', function() {
    process.stdout.write(body + '\n' + res.statusCode);
  });
});

req.on('error', function(e) {
  console.error('HTTP_ERROR:' + e.message);
  process.exit(1);
});

req.setTimeout(60000, function() {
  console.error('TIMEOUT');
  req.destroy();
  process.exit(1);
});

if (payload) {
  req.write(payload);
}
req.end();