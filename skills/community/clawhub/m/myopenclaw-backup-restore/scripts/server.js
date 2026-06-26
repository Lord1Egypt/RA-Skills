#!/usr/bin/env node
/**
 * MyOpenClaw Backup Restore Server �?lightweight HTTP server for backup management
 * Part of MyClaw.ai (https://myclaw.ai) open skills ecosystem
 *
 * SECURITY MODEL (enforced in code, not just docs):
 *   - Token is REQUIRED to start (process.exit if missing)
 *   - POST /backup and POST /restore are LOCALHOST-ONLY (127.0.0.1 / ::1)
 *   - Remote clients can only: list, download, upload
 *   - /health is unauthenticated and returns no sensitive info
 *
 * Usage: node server.js --token <secret> [--port 7373] [--backup-dir <dir>]
 */

'use strict';
const http = require('http');
const fs   = require('fs');
const path = require('path');
const os   = require('os');
const { execSync } = require('child_process');

// ── Config ────────────────────────────────────────────────────────────────────
const argv = process.argv.slice(2);
const arg  = (flag, def) => { const i = argv.indexOf(flag); return i !== -1 && argv[i+1] ? argv[i+1] : def; };

const PORT       = parseInt(arg('--port', process.env.BACKUP_PORT || '7373'));
const defaultBackupDir = path.join(os.homedir(), 'openclaw-backups');
const BACKUP_DIR = arg('--backup-dir', process.env.BACKUP_DIR || defaultBackupDir);
const TOKEN      = arg('--token', process.env.BACKUP_TOKEN || '');
const SKILL_DIR  = path.resolve(__dirname, '..');
const BACKUP_JS  = path.join(SKILL_DIR, 'scripts', 'backup-restore.js');

// ── SECURITY GATE 1: Token required ──────────────────────────────────────────
if (!TOKEN) {
  console.error('\n�? --token is required. This server handles credentials and API keys.');
  console.error('    Example: node server.js --token mySecretToken123\n');
  process.exit(1);
}

// ── SECURITY GATE 2: Localhost-only check ────────────────────────────────────
function isLocalhost(req) {
  const ip = req.socket.remoteAddress || '';
  return ip === '127.0.0.1' || ip === '::1' || ip === '::ffff:127.0.0.1';
}

// ── Ensure backup dir exists ──────────────────────────────────────────────────
fs.mkdirSync(BACKUP_DIR, { recursive: true });

// ── Helpers ───────────────────────────────────────────────────────────────────
const SECURE_HEADERS = {
  'X-Content-Type-Options': 'nosniff',
  'X-Frame-Options': 'DENY',
  'Cache-Control': 'no-store',
};

function json(res, status, data) {
  res.writeHead(status, { 'Content-Type': 'application/json', ...SECURE_HEADERS });
  res.end(JSON.stringify(data, null, 2));
}

function fmt(bytes) {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / 1048576).toFixed(1) + ' MB';
}

function listBackups() {
  return fs.readdirSync(BACKUP_DIR)
    .filter(f => (f.startsWith('openclaw-backup_') || f.startsWith('pre-restore_')) &&
                 (f.endsWith('.tar.gz') || f.endsWith('.zip')))
    .map(f => {
      try {
        const stat = fs.statSync(path.join(BACKUP_DIR, f));
        return {
          filename: f,
          size: stat.size,
          sizeHuman: fmt(stat.size),
          createdAt: stat.mtime.toISOString(),
          downloadUrl: `/download/${encodeURIComponent(f)}?token=${TOKEN}`,
        };
      } catch { return null; }
    })
    .filter(Boolean)
    .sort((a, b) => b.createdAt.localeCompare(a.createdAt));
}

function checkAuth(req) {
  const q = new URL('http://x' + req.url).searchParams.get('token');
  const h = (req.headers['authorization'] || '').replace('Bearer ', '').trim();
  return q === TOKEN || h === TOKEN;
}

// ── Multipart parser (no deps, robust boundary handling) ─────────────────────
function parseMultipart(req, maxSize = 500 * 1024 * 1024) {
  return new Promise((resolve, reject) => {
    const ct = req.headers['content-type'] || '';
    const bm = ct.match(/boundary=(?:"([^"]+)"|([^\s;]+))/);
    if (!bm) return reject(new Error('No multipart boundary'));
    const boundary = bm[1] || bm[2];

    const chunks = [];
    let totalSize = 0;

    req.on('data', chunk => {
      totalSize += chunk.length;
      if (totalSize > maxSize) {
        req.destroy();
        return reject(new Error(`Upload exceeds max size (${fmt(maxSize)})`));
      }
      chunks.push(chunk);
    });

    req.on('error', reject);

    req.on('end', () => {
      try {
        const body = Buffer.concat(chunks);
        const boundaryBuf = Buffer.from('--' + boundary);

        // Find first boundary
        let start = body.indexOf(boundaryBuf);
        if (start === -1) return reject(new Error('Boundary not found in body'));
        start += boundaryBuf.length + 2; // skip \r\n after boundary

        // Find header end
        const headerEnd = body.indexOf('\r\n\r\n', start);
        if (headerEnd === -1) return reject(new Error('Malformed multipart: no header end'));

        const headerStr = body.slice(start, headerEnd).toString('utf8');
        const fnm = headerStr.match(/filename="([^"]+)"/);
        if (!fnm) return reject(new Error('No filename in multipart'));

        const filename = path.basename(fnm[1]); // sanitize
        const dataStart = headerEnd + 4;

        // Find end boundary
        const endBoundary = Buffer.from('\r\n--' + boundary);
        let dataEnd = body.indexOf(endBoundary, dataStart);
        if (dataEnd === -1) dataEnd = body.length; // fallback

        resolve({ filename, data: body.slice(dataStart, dataEnd) });
      } catch (e) {
        reject(e);
      }
    });
  });
}

// ── Web UI ────────────────────────────────────────────────────────────────────
function serveUI(req, res) {
  const uiPath = path.join(SKILL_DIR, 'scripts', 'ui.html');
  let html = fs.existsSync(uiPath) ? fs.readFileSync(uiPath, 'utf8') : '<h1>UI not found</h1>';
  const backups = listBackups();
  const rows = backups.map(b =>
    `<tr><td><span class="tag">${b.filename.endsWith('.zip') ? 'zip' : 'tar.gz'}</span> ${b.filename}</td>` +
    `<td>${b.sizeHuman}</td>` +
    `<td>${new Date(b.createdAt).toLocaleString()}</td>` +
    `<td class="actions"><a class="btn btn-gray" href="${b.downloadUrl}" download>�?Download</a>` +
    `<button class="btn btn-success restore-btn" data-file="${b.filename}">👁 Dry Run</button>` +
    `<button class="btn btn-danger restore-btn" data-file="${b.filename}" data-confirm="1">♻️ Restore</button></td></tr>`
  ).join('');
  html = html
    .replace('{{TOKEN}}', TOKEN)
    .replace('{{BACKUP_COUNT}}', String(backups.length))
    .replace('{{BACKUP_ROWS}}', backups.length ? rows : '<tr><td colspan="4" class="empty">No backups yet.</td></tr>');
  res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', ...SECURE_HEADERS });
  res.end(html);
}

// ── Router ────────────────────────────────────────────────────────────────────
const server = http.createServer(async (req, res) => {
  const urlPath = new URL('http://x' + req.url).pathname;

  // /health �?no auth, minimal info only
  if (req.method === 'GET' && urlPath === '/health') {
    return json(res, 200, { status: 'ok', service: 'openclaw-backup', version: '3.0' });
  }

  // All other routes require auth
  if (!checkAuth(req)) {
    return json(res, 401, { error: 'Unauthorized. Pass ?token=xxx or Authorization: Bearer xxx' });
  }

  // GET / �?Web UI
  if (req.method === 'GET' && urlPath === '/') return serveUI(req, res);

  // GET /backups �?list
  if (req.method === 'GET' && urlPath === '/backups') {
    return json(res, 200, { backups: listBackups() });
  }

  // POST /backup �?LOCALHOST ONLY (shell execution)
  if (req.method === 'POST' && urlPath === '/backup') {
    if (!isLocalhost(req)) {
      return json(res, 403, { error: 'POST /backup is localhost-only.', hint: 'Run backup locally on this machine.' });
    }
    try {
      const out = execSync(
        `node "${BACKUP_JS}" backup --output-dir "${BACKUP_DIR}"`,
        { encoding: 'utf8', timeout: 120000 }
      );
      const latest = listBackups()[0];
      return json(res, 200, {
        message: 'Backup created',
        filename: latest?.filename,
        size: latest?.sizeHuman,
        downloadUrl: latest?.downloadUrl,
        output: out.replace(/\x1b\[[0-9;]*m/g, ''),
      });
    } catch (e) { return json(res, 500, { error: e.message }); }
  }

  // GET /download/:filename
  if (req.method === 'GET' && urlPath.startsWith('/download/')) {
    const filename = path.basename(decodeURIComponent(urlPath.slice('/download/'.length)));
    const filePath = path.join(BACKUP_DIR, filename);
    if (!fs.existsSync(filePath) || !(filename.endsWith('.tar.gz') || filename.endsWith('.zip'))) {
      return json(res, 404, { error: 'File not found' });
    }
    const stat = fs.statSync(filePath);
    const contentType = filename.endsWith('.zip') ? 'application/zip' : 'application/gzip';
    res.writeHead(200, {
      'Content-Type': contentType,
      'Content-Disposition': `attachment; filename="${filename}"`,
      'Content-Length': stat.size,
    });
    fs.createReadStream(filePath).pipe(res);
    return;
  }

  // POST /upload �?allowed from remote (upload only, no execution)
  if (req.method === 'POST' && urlPath === '/upload') {
    try {
      const file = await parseMultipart(req);
      if (!file.filename.endsWith('.tar.gz') && !file.filename.endsWith('.zip')) {
        return json(res, 400, { error: 'Only .tar.gz or .zip files accepted' });
      }
      const dest = path.join(BACKUP_DIR, path.basename(file.filename));
      fs.writeFileSync(dest, file.data);
      harden(dest, 0o600);
      return json(res, 200, { message: 'Upload successful', filename: file.filename, size: fmt(file.data.length) });
    } catch (e) {
      return json(res, 400, { error: e.message });
    }
  }

  // POST /restore/:filename �?LOCALHOST ONLY (shell execution)
  if (req.method === 'POST' && urlPath.startsWith('/restore/')) {
    if (!isLocalhost(req)) {
      return json(res, 403, {
        error: 'POST /restore is localhost-only.',
        hint: 'Download the backup file and run: node backup-restore.js restore <archive> --dry-run',
      });
    }
    const filename = path.basename(decodeURIComponent(urlPath.slice('/restore/'.length)));
    const filePath = path.join(BACKUP_DIR, filename);
    const params   = new URL('http://x' + req.url).searchParams;
    const isDryRun = params.get('dry_run') === '1';
    const confirmed = params.get('confirm') === '1';
    if (!fs.existsSync(filePath)) return json(res, 404, { error: 'File not found: ' + filename });
    if (!isDryRun && !confirmed) {
      return json(res, 400, { error: 'Add ?confirm=1 to apply restore. Run ?dry_run=1 first to preview.' });
    }
    try {
      const cmd = isDryRun
        ? `node "${BACKUP_JS}" restore "${filePath}" --dry-run`
        : `echo yes | node "${BACKUP_JS}" restore "${filePath}"`;
      const out = execSync(cmd, { encoding: 'utf8', timeout: 180000 });
      return json(res, 200, {
        message: isDryRun ? 'Dry run complete' : 'Restore complete',
        dryRun: isDryRun,
        output: out.replace(/\x1b\[[0-9;]*m/g, ''),
      });
    } catch (e) {
      return json(res, 500, {
        error: e.message,
        output: (e.stdout || '').replace(/\x1b\[[0-9;]*m/g, ''),
      });
    }
  }

  json(res, 404, { error: 'Not found' });
});

/** Set restrictive permissions (non-Windows only) */
function harden(filePath, mode) {
  if (process.platform === 'win32') return;
  try { fs.chmodSync(filePath, mode); } catch {}
}

server.listen(PORT, '0.0.0.0', () => {
  console.log(`\n🦞 MyOpenClaw Backup Restore Server v3.0`);
  console.log(`   Token protected | Localhost-only for /backup and /restore`);
  console.log(`   http://localhost:${PORT}/?token=${TOKEN}`);
  console.log(`   ⚠️  Do not expose this port to the internet without TLS.\n`);
});
server.on('error', err => { console.error('Server error:', err.message); process.exit(1); });
