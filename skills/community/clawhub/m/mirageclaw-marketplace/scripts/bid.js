#!/usr/bin/env node
// SECURITY MANIFEST:
//   Environment variables accessed: MARKETPLACE_API_KEY
//   External endpoints called: {BASE}/upload/image, {BASE}/upload/video, {BASE}/jobs/:jobId/bids
//   Local files read: --preview path (must be under /tmp/)
//   Local files written: none

'use strict';

require('./lib/env').loadEnv();

const fs   = require('fs');
const path = require('path');
const os   = require('os');
const { spawnSync } = require('child_process');

const { CONFIG_PATH } = require('./lib/constants');
const BASE_URL = 'https://api.mirageclaw.io';

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i += 2) {
    if (i + 1 >= argv.length) break; // bounds check: skip if no value
    args[argv[i].replace('--', '')] = argv[i + 1];
  }
  return args;
}

const args = parseArgs(process.argv);

if (!args['job-id'] || !args.preview || !args.price || !args.introduction) {
  console.error('[Bid] Usage: bid.js --job-id <id> --preview <path> --price <n> --introduction <text> [--protection <low|medium|high>] [--preview-type <image|video>]');
  process.exit(1);
}

const protection = args.protection || 'medium';

// Path traversal defense
const previewPath = path.resolve(args.preview);
if (!previewPath.startsWith('/tmp/')) {
  console.error('[Bid] ERROR: Preview path must be under /tmp/');
  process.exit(1);
}
if (!fs.existsSync(previewPath)) {
  console.error(`[Bid] ERROR: Preview file not found: ${previewPath}`);
  process.exit(1);
}

let config;
try {
  config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
} catch (err) {
  console.error('[Bid] ERROR: Failed to read config:', err.message);
  process.exit(1);
}

if (!config.agentId) {
  console.error('[Bid] ERROR: agentId not found. Run register.js first.');
  process.exit(1);
}

// ─── Validate API Key ────────────────────────────────────────────────────
const apiKey = process.env.MARKETPLACE_API_KEY;
if (!apiKey) {
  console.error('[Bid] ERROR: MARKETPLACE_API_KEY not set.');
  process.exit(1);
}

// Mime type from extension
const ext      = path.extname(previewPath).toLowerCase();
const { MIME_MAP, isVideo } = require('./lib/constants');
const mimeType = MIME_MAP[ext] || 'image/png';

// ── Determine preview type (auto-detect or CLI override) ──────────────────
const previewType = args['preview-type'] || (isVideo(ext) ? 'video' : 'image');

// ── Helper: run curl and return { status, body } ──────────────────────────
function curlRequest(curlArgs) {
  // Use -s (silent) + -w to capture HTTP status without -v (which leaks auth headers)
  const result = spawnSync('curl', ['-s', '-w', '\n%{http_code}', ...curlArgs], {
    encoding: 'utf-8',
    maxBuffer: 50 * 1024 * 1024
  });
  if (result.error) {
    return { error: result.error.message, status: 0, body: '' };
  }
  const lines = (result.stdout || '').trimEnd().split('\n');
  const status = parseInt(lines.pop(), 10) || 0;
  const body = lines.join('\n');
  return { status, body, error: null };
}

// ── Step 1: Upload ─────────────────────────────────────────────────────────
const uploadUrl = previewType === 'video'
  ? `${BASE_URL}/upload/video?protection=${protection}`
  : `${BASE_URL}/upload/image?purpose=bid_preview&protection=${protection}`;

console.log(`[Bid] Uploading preview (${mimeType}, type=${previewType}, protection=${protection})...`);

const upload = curlRequest([
  '-X', 'POST',
  uploadUrl,
  '-H', `Authorization: Bearer ${apiKey}`,
  '-F', `file=@${previewPath};type=${mimeType}`
]);

if (upload.error) {
  console.error('[Bid] ERROR: curl failed:', upload.error);
  process.exit(1);
}

if (upload.status >= 400 || !upload.body) {
  console.error(`[Bid] ERROR: Upload failed (HTTP ${upload.status})`);
  console.error('[Bid] Response:', upload.body);
  process.exit(1);
}

let previewUrl, originalPath;
try {
  const uploadRes = JSON.parse(upload.body.trim());
  previewUrl = uploadRes.url;
  originalPath = uploadRes.originalPath || null;  // original path for watermark-protected download
  if (!previewUrl) throw new Error('No URL in response');
  console.log(`[Bid] 📤 Uploaded: ${previewUrl}`);
  if (originalPath) console.log(`[Bid] 🔒 Original path: ${originalPath}`);
} catch (err) {
  console.error('[Bid] ERROR: Failed to parse upload response:', upload.body);
  process.exit(1);
}

// ── Step 2: Submit bid ─────────────────────────────────────────────────────
const bidPayload = JSON.stringify({
  agentId: config.agentId,
  introduction: args.introduction,
  preview: previewUrl,
  originalPath: originalPath,  // required for original file download after acceptance
  price: Number(args.price),
  previewType: previewType
});

const bid = curlRequest([
  '-X', 'POST',
  `${BASE_URL}/jobs/${args['job-id']}/bids`,
  '-H', 'Content-Type: application/json',
  '-H', `Authorization: Bearer ${apiKey}`,
  '-d', bidPayload
]);

if (bid.status === 409) { console.log(`[Bid] SKIP — Already bid on Job #${args['job-id']}`); process.exit(0); }
if (bid.status === 400) { console.log(`[Bid] SKIP — Job #${args['job-id']} no longer open`); process.exit(0); }

if (bid.error || bid.status >= 400) {
  console.error(`[Bid] ERROR: Bid failed (HTTP ${bid.status}):`, bid.body);
  process.exit(1);
}

console.log(`[Bid] ✅ Bid submitted — Job #${args['job-id']} @ ${args.price}`);
