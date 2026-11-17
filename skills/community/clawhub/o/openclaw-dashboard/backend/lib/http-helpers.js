'use strict';
/**
 * Shared HTTP helpers: JSON replies, CORS, auth, body parsing.
 */
const cfg = require('./config');

// ── JSON reply ──────────────────────────────────────────────────────
function jsonReply(res, status, data) {
  const body = JSON.stringify(data);
  res.writeHead(status, { 'Content-Type': 'application/json' });
  res.end(body);
}

function errorReply(res, status, message) {
  jsonReply(res, status, { error: message });
}

// ── CORS ────────────────────────────────────────────────────────────
const CORS_ALLOWED_ORIGINS = Array.isArray(cfg.CORS_ALLOWED_ORIGINS)
  ? cfg.CORS_ALLOWED_ORIGINS
  : [];

function getCorsOrigin(req) {
  const origin = req.headers['origin'] || '';
  if (CORS_ALLOWED_ORIGINS.length === 0) {
    if (/^https?:\/\/(localhost|127\.0\.0\.1|0\.0\.0\.0)(:\d+)?$/.test(origin)) return origin;
    return '';
  }
  if (CORS_ALLOWED_ORIGINS.includes('*')) return '*';
  if (CORS_ALLOWED_ORIGINS.includes(origin)) return origin;
  return '';
}

function setCors(res, req) {
  const allowed = req ? getCorsOrigin(req) : '';
  if (allowed) {
    res.setHeader('Access-Control-Allow-Origin', allowed);
    if (allowed !== '*') res.setHeader('Vary', 'Origin');
  }
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
}

// ── Auth ─────────────────────────────────────────────────────────────
function parseCookies(req) {
  const raw = req.headers['cookie'] || '';
  const cookies = {};
  for (const part of raw.split(';')) {
    const value = part.trim();
    if (!value) continue;
    const separator = value.indexOf('=');
    const rawName = separator >= 0 ? value.slice(0, separator) : value;
    const rawValue = separator >= 0 ? value.slice(separator + 1) : '';
    try {
      const name = decodeURIComponent(rawName.trim());
      if (!name) continue;
      cookies[name] = decodeURIComponent(rawValue.trim());
    } catch {
      // Ignore malformed cookie fragments instead of terminating the request.
    }
  }
  return cookies;
}

function authCookie(maxAge) {
  const parts = [
    `ds=${encodeURIComponent(cfg.AUTH_TOKEN)}`,
    'Path=/',
    'HttpOnly',
    'SameSite=Strict',
    `Max-Age=${Math.max(0, Number(maxAge) || 0)}`,
  ];
  if (cfg.COOKIE_SECURE) parts.push('Secure');
  return parts.join('; ');
}

function authenticate(req) {
  if (!cfg.AUTH_TOKEN) return true; // no token = open
  const authHeader = req.headers['authorization'] || '';
  if (authHeader.startsWith('Bearer ') && authHeader.slice(7).trim() === cfg.AUTH_TOKEN) return true;
  const cookies = parseCookies(req);
  if (cookies['ds'] === cfg.AUTH_TOKEN) return true;
  return false;
}

// ── Body parsing ─────────────────────────────────────────────────────
function readBody(req, maxSize) {
  const limit = maxSize || cfg.MAX_BODY;
  return new Promise((resolve, reject) => {
    const chunks = [];
    let size = 0;
    req.on('data', (chunk) => {
      size += chunk.length;
      if (size > limit) { reject(new Error('Request body too large')); req.destroy(); return; }
      chunks.push(chunk);
    });
    req.on('end', () => resolve(Buffer.concat(chunks)));
    req.on('error', reject);
  });
}

function readJsonBody(req) {
  return readBody(req).then((buf) => {
    const text = buf.toString('utf8');
    if (!text.trim()) return {};
    try { return JSON.parse(text); }
    catch { throw new Error('Invalid JSON body'); }
  });
}

// ── Formatters ───────────────────────────────────────────────────────
function formatDuration(seconds) {
  const s = Math.max(0, Math.floor(seconds || 0));
  const d = Math.floor(s / 86400);
  const h = Math.floor((s % 86400) / 3600);
  const m = Math.floor((s % 3600) / 60);
  if (d > 0) return `${d}d ${h}h ${m}m`;
  if (h > 0) return `${h}h ${m}m`;
  return `${m}m`;
}

function bytesHuman(bytes) {
  const b = Number(bytes || 0);
  if (b < 1024) return `${b.toFixed(0)} B`;
  if (b < 1024 * 1024) return `${(b / 1024).toFixed(1)} KB`;
  if (b < 1024 * 1024 * 1024) return `${(b / (1024 * 1024)).toFixed(1)} MB`;
  return `${(b / (1024 * 1024 * 1024)).toFixed(1)} GB`;
}

// ── Sanitization ─────────────────────────────────────────────────────
function sanitizeUntrustedText(value, maxLen = cfg.MAX_UNTRUSTED_PROMPT_FIELD) {
  return String(value || '')
    .replace(/[\u0000-\u001f\u007f]/g, ' ')
    .replace(/[`$\\]/g, '_')
    .slice(0, maxLen)
    .trim();
}

function sanitizeFilename(name) {
  return String(name || '').replace(/[^a-zA-Z0-9._-]/g, '_').slice(0, 200);
}

module.exports = {
  jsonReply, errorReply,
  getCorsOrigin, setCors,
  authenticate, parseCookies, authCookie,
  readBody, readJsonBody,
  formatDuration, bytesHuman,
  sanitizeUntrustedText, sanitizeFilename,
};
