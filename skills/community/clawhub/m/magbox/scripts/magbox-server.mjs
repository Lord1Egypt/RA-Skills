#!/usr/bin/env node
// MagBox 0.2.0: current files in two owner-controlled directories.
// Host/Origin checks reduce browser abuse. They are not authentication.
import http from 'node:http';
import { promises as fs, constants } from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { randomBytes } from 'node:crypto';
import { pipeline } from 'node:stream/promises';
import { pathToFileURL } from 'node:url';

const MiB = 1024 * 1024;
const MAX_NAME_BYTES = 200;
const MAX_PARTS = 8;
const HEADER_LIMIT = 8192;
const SAFE_INLINE = new Map([
  ['jpg', 'image/jpeg'], ['jpeg', 'image/jpeg'], ['png', 'image/png'],
  ['gif', 'image/gif'], ['webp', 'image/webp'], ['mp3', 'audio/mpeg'],
  ['mp4', 'video/mp4'], ['mov', 'video/quicktime'], ['txt', 'text/plain; charset=utf-8'],
  ['md', 'text/plain; charset=utf-8'], ['json', 'text/plain; charset=utf-8'],
]);

class HttpError extends Error {
  constructor(status, message, headers = {}) {
    super(message);
    this.status = status;
    this.headers = headers;
  }
}

function integer(value, fallback, min, max, label) {
  const text = String(value ?? fallback);
  const number = Number(text);
  if (!/^\d+$/.test(text) || !Number.isSafeInteger(number) || number < min || number > max) {
    throw new Error(`${label} must be an integer from ${min} to ${max}`);
  }
  return number;
}

function hostName(value) {
  const text = value.trim().toLowerCase();
  const url = new URL(`http://${text}`);
  if (!text || url.username || url.password || url.port || url.pathname !== '/' || url.search || url.hash || url.host !== text) {
    throw new Error('Host entries must be plain hostnames or addresses, without ports');
  }
  return url.hostname;
}

// Read only documented application settings, never the entire environment.
export function configFromEnv(env = {
  MAGBOX_BIND: process.env.MAGBOX_BIND,
  MAGBOX_PORT: process.env.MAGBOX_PORT,
  MAGBOX_HOSTS: process.env.MAGBOX_HOSTS,
  MAGBOX_TO_AGENT: process.env.MAGBOX_TO_AGENT,
  MAGBOX_FROM_AGENT: process.env.MAGBOX_FROM_AGENT,
  MAGBOX_MAX_BYTES: process.env.MAGBOX_MAX_BYTES,
  MAGBOX_MAX_UPLOADS: process.env.MAGBOX_MAX_UPLOADS,
  MAGBOX_UPLOAD_TIMEOUT_MS: process.env.MAGBOX_UPLOAD_TIMEOUT_MS,
}) {
  const bind = env.MAGBOX_BIND || '127.0.0.1';
  // A specific private address is the simplest LAN opt-in. Wildcard binding
  // needs explicit hosts so an arbitrary DNS name cannot reach the application.
  const extraHosts = (env.MAGBOX_HOSTS || '').split(',').filter(Boolean).map(hostName);
  if (['0.0.0.0', '::'].includes(bind) && !extraHosts.length) {
    throw new Error('Wildcard binding needs MAGBOX_HOSTS with the addresses/names clients will use');
  }
  const bindHost = bind.includes(':') && !bind.startsWith('[') ? `[${bind}]` : bind;
  const allowedHosts = new Set(['localhost', '127.0.0.1', '[::1]', ...extraHosts]);
  if (!['0.0.0.0', '::'].includes(bind)) allowedHosts.add(hostName(bindHost));
  return {
    bind,
    port: integer(env.MAGBOX_PORT, 9900, 0, 65535, 'MAGBOX_PORT'),
    toDir: path.resolve(env.MAGBOX_TO_AGENT || path.join(os.homedir(), 'Inbox')),
    fromDir: path.resolve(env.MAGBOX_FROM_AGENT || path.join(os.homedir(), 'Outbox')),
    maxBytes: integer(env.MAGBOX_MAX_BYTES, 16 * MiB, 1, 256 * MiB, 'MAGBOX_MAX_BYTES'),
    maxUploads: integer(env.MAGBOX_MAX_UPLOADS, 2, 1, 8, 'MAGBOX_MAX_UPLOADS'),
    uploadTimeout: integer(env.MAGBOX_UPLOAD_TIMEOUT_MS, 30000, 50, 300000, 'MAGBOX_UPLOAD_TIMEOUT_MS'),
    allowedHosts,
    advertisedHost: extraHosts[0] || bindHost,
  };
}

function sameFile(a, b) { return a.dev === b.dev && a.ino === b.ino; }

async function prepareRoot(directory) {
  await fs.mkdir(directory, { recursive: true, mode: 0o700 });
  const stat = await fs.lstat(directory);
  if (!stat.isDirectory() || stat.isSymbolicLink()) throw new Error('Storage roots must be real directories');
  const real = await fs.realpath(directory);
  return { directory: real, stat: await fs.lstat(real), pending: new Set() };
}

async function checkRoot(root) {
  const stat = await fs.lstat(root.directory);
  if (!stat.isDirectory() || stat.isSymbolicLink() || !sameFile(stat, root.stat) || await fs.realpath(root.directory) !== root.directory) {
    throw new HttpError(409, 'Storage directory changed; restart after checking its configuration');
  }
}

function childPath(root, name) {
  if (!name || name === '.' || name === '..' || name.includes('/') || name.includes('\\') || /[\u0000-\u001f\u007f]/.test(name)) {
    throw new HttpError(400, 'Invalid filename');
  }
  const target = path.resolve(root.directory, name);
  if (path.dirname(target) !== root.directory) throw new HttpError(403, 'File is outside the storage directory');
  return target;
}

async function openRegular(root, name) {
  await checkRoot(root);
  const target = childPath(root, name);
  if (root.pending.has(name)) throw new HttpError(409, 'Upload is still being saved');
  const before = await fs.lstat(target);
  if (!before.isFile() || before.isSymbolicLink()) throw new HttpError(403, 'Only regular files are served');
  let handle;
  try {
    // Nonblocking avoids hanging if a FIFO replaces a file during opening.
    handle = await fs.open(target, constants.O_RDONLY | constants.O_NOFOLLOW | constants.O_NONBLOCK);
    const stat = await handle.stat();
    const after = await fs.lstat(target);
    await checkRoot(root);
    if (!stat.isFile() || after.isSymbolicLink() || !sameFile(before, stat) || !sameFile(stat, after)) {
      throw new HttpError(409, 'File changed while opening');
    }
    return { handle, stat };
  } catch (error) {
    await handle?.close().catch(() => {});
    throw error;
  }
}

async function listDirectory(root) {
  await checkRoot(root);
  const entries = await fs.readdir(root.directory, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    if (!entry.isFile() || entry.name.startsWith('.magbox-') || root.pending.has(entry.name)) continue;
    let opened;
    try {
      opened = await openRegular(root, entry.name);
      files.push({ name: entry.name, size: opened.stat.size, modified: opened.stat.mtime.toISOString() });
    } catch (error) {
      if (!['ENOENT', 'ELOOP', 'EACCES'].includes(error.code) && ![400, 403, 409].includes(error.status)) throw error;
    } finally {
      await opened?.handle.close().catch(() => {});
    }
  }
  await checkRoot(root);
  files.sort((a, b) => b.modified.localeCompare(a.modified) || a.name.localeCompare(b.name));
  return { files, count: files.length, totalBytes: files.reduce((sum, file) => sum + file.size, 0) };
}

function parseRange(value, size) {
  if (!value) return null;
  const match = /^bytes=(\d*)-(\d*)$/.test(value) ? value.match(/^bytes=(\d*)-(\d*)$/) : null;
  const invalid = () => new HttpError(416, 'Unsupported or unsatisfiable byte range', { 'Content-Range': `bytes */${size}` });
  if (!match || (!match[1] && !match[2]) || size === 0) throw invalid();
  const first = match[1] ? Number(match[1]) : null;
  const last = match[2] ? Number(match[2]) : null;
  if ((first !== null && !Number.isSafeInteger(first)) || (last !== null && !Number.isSafeInteger(last))) throw invalid();
  if (first === null) {
    if (last === 0) throw invalid();
    return { start: Math.max(0, size - last), end: size - 1 };
  }
  if (first >= size || (last !== null && last < first)) throw invalid();
  return { start: first, end: last === null ? size - 1 : Math.min(last, size - 1) };
}

function disposition(name, inline) {
  const encoded = encodeURIComponent(name).replace(/['()*]/g, c => `%${c.charCodeAt(0).toString(16).toUpperCase()}`);
  return `${inline ? 'inline' : 'attachment'}; filename*=UTF-8''${encoded}`;
}

async function serveFile(req, res, root, encodedName) {
  let name;
  try { name = decodeURIComponent(encodedName); } catch { throw new HttpError(400, 'Invalid percent encoding'); }
  const { handle, stat } = await openRegular(root, name);
  try {
    const ext = name.split('.').pop().toLowerCase();
    const type = SAFE_INLINE.get(ext);
    // Uploaded SVG/HTML and all unknown formats download as opaque attachments.
    // Sandbox also prevents active documents from inheriting the app origin.
    const headers = {
      'Content-Type': type || 'application/octet-stream',
      'Content-Disposition': disposition(name, Boolean(type)),
      'Content-Security-Policy': "sandbox; default-src 'none'; base-uri 'none'",
      'Accept-Ranges': 'bytes',
    };
    // HTTP Range applies to GET. HEAD reports metadata for the full resource.
    const range = req.method === 'GET' ? parseRange(req.headers.range, stat.size) : null;
    headers['Content-Length'] = range ? range.end - range.start + 1 : stat.size;
    if (range) headers['Content-Range'] = `bytes ${range.start}-${range.end}/${stat.size}`;
    res.writeHead(range ? 206 : 200, headers);
    if (req.method === 'HEAD' || stat.size === 0) { res.end(); return; }
    await pipeline(handle.createReadStream({ autoClose: false, start: range?.start ?? 0, end: range?.end ?? stat.size - 1 }), res);
  } finally {
    await handle.close().catch(() => {});
  }
}

// Parse MIME parameters, including quoted boundaries and escaped quoted names.
function mimeParameters(text) {
  const separator = text.indexOf(';');
  const kind = (separator < 0 ? text : text.slice(0, separator)).trim().toLowerCase();
  const params = new Map();
  let tail = separator < 0 ? '' : text.slice(separator);
  while (tail.length) {
    const match = tail.match(/^;\s*([\w-]+)\s*=\s*(?:"((?:[^"\\\r\n]|\\[\x20-\x7e])*)"|([^;\s]+))\s*/);
    if (!match) throw new HttpError(400, 'Malformed MIME parameters');
    const key = match[1].toLowerCase();
    if (params.has(key)) throw new HttpError(400, 'Duplicate MIME parameter');
    params.set(key, match[2] === undefined ? match[3] : match[2].replace(/\\([\x20-\x7e])/g, '$1'));
    tail = tail.slice(match[0].length);
  }
  return { kind, params };
}

function uploadBoundary(contentType) {
  const { kind, params } = mimeParameters(contentType || '');
  const boundary = params.get('boundary');
  if (kind !== 'multipart/form-data' || !boundary || !/^[0-9A-Za-z'()+_,\-./:=? ]{1,70}$/.test(boundary) || boundary.endsWith(' ')) {
    throw new HttpError(400, 'Expected multipart/form-data with a valid boundary');
  }
  return boundary;
}

function parseMultipart(body, boundary) {
  const opening = Buffer.from(`--${boundary}\r\n`);
  const marker = Buffer.from(`\r\n--${boundary}`);
  if (!body.subarray(0, opening.length).equals(opening)) throw new HttpError(400, 'Invalid multipart opening');
  const parts = [];
  let position = opening.length;
  while (position < body.length) {
    if (parts.length >= MAX_PARTS) throw new HttpError(413, 'Too many files in one request');
    const headerEnd = body.indexOf('\r\n\r\n', position);
    if (headerEnd < 0 || headerEnd - position > HEADER_LIMIT) throw new HttpError(400, 'Invalid multipart headers');
    const headers = new Map();
    for (const line of body.subarray(position, headerEnd).toString('utf8').split('\r\n')) {
      const match = line.match(/^([A-Za-z0-9-]+):[ \t]*(.*)$/);
      if (!match || headers.has(match[1].toLowerCase())) throw new HttpError(400, 'Invalid multipart header');
      headers.set(match[1].toLowerCase(), match[2]);
    }
    const { kind, params } = mimeParameters(headers.get('content-disposition') || '');
    if (kind !== 'form-data' || params.get('name') !== 'file' || !params.has('filename') || headers.has('content-transfer-encoding')) {
      throw new HttpError(400, 'Only file fields are accepted');
    }
    const dataStart = headerEnd + 4;
    let next = dataStart;
    let closing = false;
    while (true) {
      next = body.indexOf(marker, next);
      if (next < 0) throw new HttpError(400, 'Missing multipart terminator');
      const suffix = next + marker.length;
      if (body.subarray(suffix, suffix + 2).equals(Buffer.from('\r\n'))) break;
      if (body.subarray(suffix, suffix + 2).equals(Buffer.from('--')) &&
          (suffix + 2 === body.length || (suffix + 4 === body.length && body.subarray(suffix + 2).equals(Buffer.from('\r\n'))))) {
        closing = true;
        break;
      }
      // Boundary-like bytes embedded in binary payloads remain untouched.
      next += marker.length;
    }
    parts.push({ name: params.get('filename'), data: body.subarray(dataStart, next) });
    if (closing) return parts;
    position = next + marker.length + 2;
  }
  throw new HttpError(400, 'Incomplete multipart body');
}

function readBody(req, maximum, timeout) {
  const length = req.headers['content-length'];
  if (length && (!/^\d+$/.test(length) || Number(length) > maximum)) throw new HttpError(413, 'Upload exceeds byte limit');
  return new Promise((resolve, reject) => {
    let size = 0;
    let chunks = [];
    const finish = (error, body) => {
      clearTimeout(timer);
      req.off('data', onData); req.off('end', onEnd); req.off('aborted', onAbort); req.off('error', onError);
      chunks = [];
      if (error) { req.pause(); reject(error); } else resolve(body);
    };
    const onData = chunk => {
      size += chunk.length;
      if (size > maximum) finish(new HttpError(413, 'Upload exceeds byte limit'));
      else chunks.push(chunk);
    };
    const onEnd = () => finish(null, Buffer.concat(chunks, size));
    const onAbort = () => finish(new HttpError(400, 'Upload interrupted'));
    const onError = () => finish(new HttpError(400, 'Upload stream failed'));
    const timer = setTimeout(() => finish(new HttpError(408, 'Upload timed out')), timeout);
    req.on('data', onData); req.once('end', onEnd); req.once('aborted', onAbort); req.once('error', onError);
  });
}

function checkRequest(req, config, port) {
  const authority = req.headers.host;
  let host;
  try {
    host = new URL(`http://${authority}`);
    if (host.host !== authority.toLowerCase() || host.username || host.password || host.pathname !== '/' || host.search || host.hash || Number(host.port || 80) !== port) throw new Error();
  } catch { throw new HttpError(403, 'Host is not allowed'); }
  if (!config.allowedHosts.has(host.hostname)) throw new HttpError(403, 'Host is not allowed');
  if (req.method === 'POST') {
    const origin = req.headers.origin;
    if ((origin !== undefined && origin !== host.origin) ||
        (req.headers['sec-fetch-site'] !== undefined && req.headers['sec-fetch-site'] !== 'same-origin')) {
      throw new HttpError(403, 'Cross-origin uploads are not allowed');
    }
    // Non-browser clients can omit Origin. Every reachable client still has
    // unauthenticated read/write access; this is browser defense only.
  }
}

function sendJson(res, status, body, headers = {}) {
  const data = JSON.stringify(body);
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8', 'Content-Length': Buffer.byteLength(data), ...headers });
  res.end(data);
}

function reportError(res, error) {
  if (res.destroyed) return;
  if (res.headersSent) { res.destroy(); return; }
  const status = error.status || ({ ENOENT: 404, ELOOP: 403, EACCES: 403, EPERM: 403, ENOSPC: 507, EDQUOT: 507 }[error.code]) || 500;
  const message = error.status ? error.message : ({ 404: 'File not found', 403: 'File access denied', 507: 'Storage is full' }[status] || 'Storage or server error');
  sendJson(res, status, { error: message }, { Connection: 'close', ...error.headers });
}

// Rendering and storage helpers follow below; the server remains one file.
const CSS = `
*{box-sizing:border-box}body{margin:0;padding:28px;font-family:-apple-system,BlinkMacSystemFont,sans-serif;background:#0d0d0d;color:#e5e5e0}
body.to{background:#fafafa;color:#1a1a1a}main{max-width:1100px;margin:auto}.to main{max-width:520px;padding-top:12px}
h1{font-size:.8rem;letter-spacing:.08em;text-transform:uppercase;color:#c8a84b;margin:0 0 22px}.to h1{color:#888}
nav{display:flex;gap:10px;margin-bottom:28px}nav a,button{font:inherit;font-size:.75rem;color:inherit;background:transparent;border:1px solid #555;border-radius:4px;padding:6px 10px;text-decoration:none;cursor:pointer}
nav a[aria-current]{border-color:#c8a84b}button:disabled{opacity:.5;cursor:wait}.header{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:14px}
.summary,.meta{font-size:.75rem;color:#999}.to .summary,.to .meta{color:#666}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px}
.card{background:#111;border:1px solid #333;border-radius:6px;padding:12px;min-width:0}.thumb,.placeholder{width:100%;height:90px;object-fit:cover;border-radius:3px;margin-bottom:8px;background:#080808}.placeholder{display:flex;align-items:center;justify-content:center;color:#c8a84b;font-size:.7rem}
.name{font-size:.8rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin:8px 0}.download{display:inline-block;font-size:.75rem;color:#c8a84b;margin-top:8px}
.zone{border:2px dashed #ccc;border-radius:12px;padding:45px 20px;text-align:center;background:#fff}.zone.dragover{border-color:#1a1a1a;background:#eee}.zone p{color:#666}
input{max-width:100%}progress{width:100%;margin-top:14px;accent-color:#1a1a1a}.status{font-size:.8rem;margin-top:14px;white-space:pre-wrap;overflow-wrap:anywhere}.error{color:#d33}
details{margin-top:36px}summary{cursor:pointer;font-size:.8rem;color:#666}.sent-item{display:flex;justify-content:space-between;gap:12px;padding:8px 0;border-bottom:1px solid #ddd}.sent-item .name{max-width:60%;margin:0}.empty{font-size:.85rem;color:#999}
`;

const SHARED_BROWSER = `
const byId = id => document.getElementById(id);
function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}
function size(bytes) {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / 1048576).toFixed(1) + ' MB';
}
function modified(iso) { return new Date(iso).toLocaleString(); }
async function listing(endpoint) {
  const response = await fetch(endpoint, { cache: 'no-store' });
  if (!response.ok) throw new Error('Could not load files.');
  return response.json();
}
function summary(data) { return data.count + ' current file' + (data.count === 1 ? '' : 's') + ' · ' + size(data.totalBytes); }
`;

function renderShell(title, bodyClass, content, script, nonce) {
  const from = bodyClass !== 'to';
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>${title}</title><style nonce="${nonce}">${CSS}</style></head><body class="${bodyClass}"><main><h1>${title}</h1>
<nav aria-label="Directions"><a href="/"${from ? ' aria-current="page"' : ''}>From Agent</a><a href="/to"${from ? '' : ' aria-current="page"'}>To Agent</a></nav>
${content}</main><script nonce="${nonce}">${SHARED_BROWSER}${script}</script></body></html>`;
}

function renderFrom(nonce) {
  return renderShell('Drop from Agent', 'from', `
<div class="header"><span id="count" class="summary" aria-live="polite">Loading…</span><button id="refresh" type="button">Refresh</button></div>
<div class="grid" id="grid"></div>`, `
async function load() {
  try {
    const data = await listing('/api/from');
    byId('count').textContent = summary(data);
    const grid = byId('grid'); grid.replaceChildren();
    if (!data.files.length) grid.append(element('p', 'empty', 'Nothing here yet.'));
    for (const file of data.files) {
      const card = element('article', 'card');
      const ext = file.name.split('.').pop().toLowerCase();
      const url = '/dl/from/' + encodeURIComponent(file.name);
      if (['jpg','jpeg','png','gif','webp'].includes(ext)) {
        const img = element('img', 'thumb'); img.src = url; img.alt = ''; img.loading = 'lazy';
        img.addEventListener('error', () => { img.hidden = true; }); card.append(img);
      } else card.append(element('div', 'placeholder', ext.toUpperCase() || 'FILE'));
      const name = element('div', 'name', file.name); name.title = file.name;
      const link = element('a', 'download', 'Download'); link.href = url; link.download = file.name;
      card.append(name, element('div', 'meta', size(file.size) + ' · Modified ' + modified(file.modified)), link);
      grid.append(card);
    }
  } catch (error) {
    byId('count').textContent = 'Files unavailable';
    byId('grid').replaceChildren(element('p', 'error', error.message));
  }
}
byId('refresh').addEventListener('click', load);
load();`, nonce);
}

function renderTo(nonce, maximum) {
  return renderShell('Drop to Agent', 'to', `
<div class="zone" id="zone"><p>Drag files here or choose them below.</p><label for="picker">Choose files</label> <input type="file" id="picker" multiple></div>
<p class="summary">Upload limit: ${(maximum / MiB).toFixed(2)} MiB per request.</p>
<progress id="bar" value="0" max="100" hidden aria-label="Upload progress"></progress>
<div class="status" id="status" role="status" aria-live="polite"></div>
<details><summary id="tray-label">Current inbox files</summary><div class="header"><span id="inbox-count" class="summary"></span><button id="refresh" type="button">Refresh</button></div><div id="sent"></div></details>`, `
async function loadSent() {
  try {
    const data = await listing('/api/to/list');
    byId('tray-label').textContent = 'Current inbox files (' + data.count + ')';
    byId('inbox-count').textContent = summary(data);
    const tray = byId('sent'); tray.replaceChildren();
    if (!data.files.length) tray.append(element('p', 'empty', 'Nothing here yet.'));
    for (const file of data.files) {
      const row = element('div', 'sent-item'); const name = element('span', 'name', file.name); name.title = file.name;
      row.append(name, element('span', 'meta', size(file.size) + ' · Modified ' + modified(file.modified))); tray.append(row);
    }
  } catch (error) { byId('sent').replaceChildren(element('p', 'error', error.message)); }
}
function sendFile(file) {
  return new Promise((resolve, reject) => {
    const form = new FormData(); form.append('file', file);
    const xhr = new XMLHttpRequest(); xhr.open('POST', '/api/to'); xhr.timeout = 60000;
    xhr.upload.onprogress = event => { if (event.lengthComputable) byId('bar').value = event.loaded / event.total * 100; };
    xhr.onload = () => {
      let data; try { data = JSON.parse(xhr.responseText); } catch { reject(new Error('Invalid server response')); return; }
      if (xhr.status === 200) resolve(data.saved);
      else reject(new Error(data.error || 'Upload failed'));
    };
    xhr.onerror = () => reject(new Error('Upload failed'));
    xhr.ontimeout = () => reject(new Error('Upload timed out'));
    xhr.onabort = () => reject(new Error('Upload cancelled'));
    xhr.send(form);
  });
}
let uploading = false;
async function upload(files) {
  if (uploading) return;
  uploading = true; byId('picker').disabled = true;
  const results = []; let failed = false;
  try {
    for (const file of files) {
      byId('status').className = 'status'; byId('status').textContent = 'Uploading ' + file.name + '…';
      byId('bar').hidden = false; byId('bar').value = 0;
      try { const saved = await sendFile(file); results.push(...saved.map(item => item.name + ' delivered.')); }
      catch (error) { failed = true; results.push(file.name + ': ' + error.message); }
    }
  } finally {
    uploading = false; byId('picker').disabled = false; byId('picker').value = ''; byId('bar').hidden = true;
    byId('status').className = failed ? 'status error' : 'status'; byId('status').textContent = results.join('\\n');
    await loadSent();
  }
}
const zone = byId('zone');
zone.addEventListener('dragover', event => { event.preventDefault(); zone.classList.add('dragover'); });
zone.addEventListener('dragleave', () => zone.classList.remove('dragover'));
zone.addEventListener('drop', event => { event.preventDefault(); zone.classList.remove('dragover'); upload([...event.dataTransfer.files]); });
byId('picker').addEventListener('change', event => upload([...event.target.files]));
byId('refresh').addEventListener('click', loadSent);
loadSent();`, nonce);
}

function sanitizeName(original) {
  const name = path.basename(original).replace(/[^a-zA-Z0-9._-]/g, '_');
  if (!name || name === '.' || name === '..' || name.startsWith('.magbox-') || Buffer.byteLength(name) > MAX_NAME_BYTES) {
    throw new HttpError(400, 'Filename is empty, reserved, or longer than 200 bytes after sanitizing');
  }
  return name;
}

async function removeCreated(root, record) {
  await checkRoot(root);
  const current = await fs.lstat(record.target).catch(error => {
    if (error.code === 'ENOENT') return null;
    throw error;
  });
  // Do not delete a file replaced by the directory owner after this upload.
  if (current && sameFile(current, record.stat)) await fs.unlink(record.target);
}

async function createVersion(root, name) {
  const extension = path.extname(name);
  const stem = name.slice(0, name.length - extension.length);
  for (let version = 1; version <= 10000; version++) {
    const candidate = version === 1 ? name : `${stem}-v${version}${extension}`;
    await checkRoot(root);
    const target = childPath(root, candidate);
    let handle;
    try {
      // Exclusive creation rejects existing files AND symlinks atomically.
      handle = await fs.open(target, 'wx', 0o600);
    } catch (error) {
      if (error.code === 'EEXIST') continue;
      throw error;
    }
    root.pending.add(candidate);
    try {
      const stat = await handle.stat();
      const record = { name: candidate, target, stat, handle };
      await checkRoot(root);
      return record;
    } catch (error) {
      await handle.close().catch(() => {});
      // A changed root is not safe to address for cleanup.
      root.pending.delete(candidate);
      throw error;
    }
  }
  throw new HttpError(409, 'Too many existing versions of this filename');
}

async function storeParts(root, parts, interrupted) {
  // Validate every filename before writing any part of a multi-file request.
  const named = parts.map(part => ({ ...part, name: sanitizeName(part.name) }));
  const created = [];
  try {
    for (const part of named) {
      if (interrupted()) throw new HttpError(400, 'Upload interrupted');
      const record = await createVersion(root, part.name);
      created.push(record);
      try {
        await record.handle.writeFile(part.data);
        await record.handle.sync();
      } finally {
        await record.handle.close();
      }
      await checkRoot(root);
      const current = await fs.lstat(record.target);
      if (current.isSymbolicLink() || !sameFile(current, record.stat)) throw new HttpError(409, 'Upload file changed while saving');
      record.size = part.data.length;
    }
    if (interrupted()) throw new HttpError(400, 'Upload interrupted');
    return created.map(({ name, size }) => ({ name, size }));
  } catch (error) {
    for (const record of created) {
      await record.handle.close().catch(() => {});
      await removeCreated(root, record).catch(() => {
        process.stderr.write('MagBox: could not clean an incomplete upload; inspect the inbox locally.\n');
      });
    }
    throw error;
  } finally {
    for (const record of created) root.pending.delete(record.name);
  }
}

export async function createMagBox(config = configFromEnv()) {
  if (constants.O_NOFOLLOW === undefined || constants.O_NONBLOCK === undefined) throw new Error('This build supports macOS and Linux');
  const to = await prepareRoot(config.toDir);
  const from = await prepareRoot(config.fromDir);
  const relative = path.relative(to.directory, from.directory);
  const reverse = path.relative(from.directory, to.directory);
  const nested = value => value === '' || (!value.startsWith(`..${path.sep}`) && value !== '..' && !path.isAbsolute(value));
  if (nested(relative) || nested(reverse)) throw new Error('Inbox and outbox must be separate, non-nested directories');
  let activeUploads = 0;
  const server = http.createServer({ maxHeaderSize: 16384 }, (req, res) => {
    // These listeners prevent transport failures from becoming uncaught errors.
    req.on('error', () => {});
    res.on('error', () => {});
    res.setHeader('Cache-Control', 'no-store');
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('Referrer-Policy', 'no-referrer');
    res.setHeader('X-Frame-Options', 'DENY');
    const run = async () => {
      checkRequest(req, config, server.address().port);
      if (!req.url?.startsWith('/') || req.url.startsWith('//')) throw new HttpError(400, 'Invalid request target');
      const route = req.url.split('?')[0];
      if (req.method === 'GET' && ['/', '/from', '/to'].includes(route)) {
        const nonce = randomBytes(18).toString('base64');
        const html = route === '/to' ? renderTo(nonce, config.maxBytes) : renderFrom(nonce);
        res.writeHead(200, {
          'Content-Type': 'text/html; charset=utf-8',
          'Content-Security-Policy': `default-src 'none'; script-src 'nonce-${nonce}'; style-src 'nonce-${nonce}'; img-src 'self'; connect-src 'self'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'`,
        });
        res.end(html); return;
      }
      if (req.method === 'GET' && route === '/api/from') { sendJson(res, 200, await listDirectory(from)); return; }
      if (req.method === 'GET' && route === '/api/to/list') { sendJson(res, 200, await listDirectory(to)); return; }
      if (['GET', 'HEAD'].includes(req.method)) {
        for (const [prefix, root] of [['/dl/from/', from], ['/dl/to/', to]]) {
          if (route.startsWith(prefix)) { await serveFile(req, res, root, route.slice(prefix.length)); return; }
        }
      }
      if (req.method === 'POST' && route === '/api/to') {
        if (activeUploads >= config.maxUploads) throw new HttpError(429, 'Too many simultaneous uploads', { 'Retry-After': '2' });
        const boundary = uploadBoundary(req.headers['content-type']);
        activeUploads++;
        try {
          const body = await readBody(req, config.maxBytes, config.uploadTimeout);
          const parts = parseMultipart(body, boundary);
          const saved = await storeParts(to, parts, () => req.aborted || res.destroyed);
          sendJson(res, 200, { saved });
        } finally { activeUploads--; }
        return;
      }
      throw new HttpError(404, 'Route not found');
    };
    run().catch(error => reportError(res, error));
  });
  server.headersTimeout = 10000;
  server.requestTimeout = Math.max(10000, config.uploadTimeout + 1000);
  server.keepAliveTimeout = 5000;
  server.maxConnections = 128;
  server.on('clientError', (_error, socket) => {
    if (socket.writable) socket.end('HTTP/1.1 400 Bad Request\r\nConnection: close\r\nContent-Length: 0\r\n\r\n');
    else socket.destroy();
  });
  return server;
}

async function main() {
  const config = configFromEnv();
  const server = await createMagBox(config);
  await new Promise((resolve, reject) => {
    server.once('error', reject);
    server.listen(config.port, config.bind, resolve);
  });
  const port = server.address().port;
  const base = `http://${config.advertisedHost}:${port}`;
  process.stdout.write(`MagBox 0.2.0\nFrom Agent: ${base}/\nTo Agent:   ${base}/to\nInbox: ${config.toDir}\nOutbox: ${config.fromDir}\nNo authentication: anyone reaching this port can access served files.\n`);
  server.on('error', error => { process.stderr.write(`MagBox server error: ${error.code || 'unknown'}\n`); });
  const stop = () => { server.close(); server.closeIdleConnections(); };
  process.once('SIGINT', stop);
  process.once('SIGTERM', stop);
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  main().catch(error => { process.stderr.write(`MagBox: ${error.message}\n`); process.exitCode = 1; });
}
