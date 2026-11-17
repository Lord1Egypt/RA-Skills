'use strict';
/**
 * Config Provider — read-only view of openclaw.json + workspace files.
 *
 * /ops/config  — returns { capabilities, files: [{label, category, size, modified, content}] }
 * /files       — workspace file browser (read) + optional PUT
 * /skills      — list installed skills
 */
const fs   = require('fs');
const path = require('path');
const cfg  = require('../lib/config');
const { jsonReply, errorReply } = require('../lib/http-helpers');

// ── Capability flags (read from env / config) ────────────────────────
function getCapabilities() {
  return {
    readOnly:                         true,
    mutatingOpsEnabled:              false,
    mutatingOpsLoopbackOnly:         true,
    attachmentFilePathCopyEnabled:   false,
  };
}

// ── Redact secrets ───────────────────────────────────────────────────
function isSensitiveKey(key) {
  const normalized = String(key).toLowerCase().replace(/[^a-z0-9]/g, '');
  if (normalized === 'auth') return true;
  return [
    'apikey',
    'token',
    'secret',
    'password',
    'webhook',
    'authorization',
    'credential',
    'privatekey',
  ].some(fragment => normalized.includes(fragment));
}

function redactSecrets(obj) {
  if (!obj || typeof obj !== 'object') return;
  for (const key of Object.keys(obj)) {
    if (isSensitiveKey(key)) {
      obj[key] = '[REDACTED]';
    } else if (typeof obj[key] === 'object') {
      redactSecrets(obj[key]);
    }
  }
}

// ── Build files list in the format the frontend expects ──────────────
// Each entry: { label, category, size, modified, content }
function buildConfigFiles() {
  const home = cfg.HOME;
  const ws   = cfg.WORKSPACE;
  const dotOc = cfg.DOT_OPENCLAW;
  const files = [];

  // Core config files
  const coreFiles = [
    { filePath: path.join(dotOc, 'openclaw.json'), label: 'openclaw.json',        category: 'core'  },
    { filePath: path.join(dotOc, 'exec-approvals.json'), label: 'exec-approvals.json', category: 'core' },
  ];

  // Workspace personality files
  try {
    const wsFiles = fs.readdirSync(ws)
      .filter(f => /^(SOUL|AGENTS|USER|IDENTITY|HEARTBEAT|MEMORY|TOOLS).*\.md$/i.test(f))
      .sort();
    wsFiles.forEach(f => coreFiles.push({ filePath: path.join(ws, f), label: f, category: 'personality' }));
  } catch {}

  for (const { filePath, label, category } of coreFiles) {
    try {
      const stat    = fs.statSync(filePath);
      let   content = fs.readFileSync(filePath, 'utf8');

      // Redact JSON files
      if (label.endsWith('.json')) {
        try {
          const parsed = JSON.parse(content);
          redactSecrets(parsed);
          content = JSON.stringify(parsed, null, 2);
        } catch {}
      }

      files.push({
        label,
        category,
        size:     stat.size,
        modified: stat.mtime.toISOString(),
        content,
      });
    } catch {}
  }

  return files;
}

// ── Main config endpoint ─────────────────────────────────────────────
function handleConfig(_req, res) {
  if (!cfg.ENABLE_CONFIG_ENDPOINT) {
    return errorReply(res, 403, 'Config endpoint disabled');
  }

  const capabilities = getCapabilities();
  const files        = buildConfigFiles();

  // Also include the raw openclaw.json for callers that expect { config }
  let rawConfig = null;
  try {
    const raw = JSON.parse(fs.readFileSync(cfg.OPENCLAW_CONFIG_FILE, 'utf8'));
    redactSecrets(raw);
    rawConfig = raw;
  } catch {}

  jsonReply(res, 200, { capabilities, files, config: rawConfig });
}

// ── Workspace file browser ───────────────────────────────────────────
function isAllowedPath(p) {
  if (!p || typeof p !== 'string') return false;
  const normalized = path.normalize(p);
  if (normalized.includes('..')) return false;
  if (path.isAbsolute(normalized)) return false;
  const parts = normalized.split(path.sep);
  // Root *.md files
  if (parts.length === 1 && normalized.endsWith('.md')) return true;
  // memory/*.md
  if (parts.length === 2 && parts[0] === 'memory' && parts[1].endsWith('.md')) return true;
  // channels/*.md
  if (parts.length === 2 && parts[0] === 'channels' && parts[1].endsWith('.md')) return true;
  // refs/**/*.md (new layered structure: ground-truth/systems/playbooks/archive)
  if (parts.length >= 2 && parts[0] === 'refs' && parts[parts.length - 1].endsWith('.md')) return true;
  return false;
}

function handleFiles(_req, res, query) {
  const filePath = query.path || '';
  const isList   = query.list === 'true';
  const ws       = cfg.WORKSPACE;

  // Directory listing mode
  if (isList && filePath) {
    const cleanDir = filePath.replace(/^\/|\/$/g, '').split('/')[0];
    const allowedDirs = ['memory', 'channels', 'refs'];
    if (!allowedDirs.includes(cleanDir)) return errorReply(res, 403, 'Directory not allowed');
    const dirPath = path.join(ws, cleanDir);
    try {
      const files = fs.readdirSync(dirPath).filter(f => f.endsWith('.md')).map(f => `${cleanDir}/${f}`);
      return jsonReply(res, 200, { files });
    } catch { return jsonReply(res, 200, { files: [] }); }
  }

  if (!filePath) {
    // List workspace .md files
    const files = [];
    try {
      for (const f of fs.readdirSync(ws)) {
        if (f.endsWith('.md')) files.push(f);
      }
      for (const dir of ['memory', 'channels', 'refs']) {
        const d = path.join(ws, dir);
        try {
          for (const f of fs.readdirSync(d)) {
            if (f.endsWith('.md')) files.push(`${dir}/${f}`);
          }
        } catch {}
      }
    } catch {}
    return jsonReply(res, 200, { files });
  }

  if (!isAllowedPath(filePath)) {
    return errorReply(res, 403, 'Path not allowed');
  }
  const fullPath = path.join(ws, filePath);
  try {
    const content = fs.readFileSync(fullPath, 'utf8');
    jsonReply(res, 200, { path: filePath, content });
  } catch {
    errorReply(res, 404, 'File not found');
  }
}

function handleSkills(_req, res) {
  try {
    const skills = fs.readdirSync(cfg.SKILLS_DIR)
      .filter(d => {
        try { return fs.statSync(path.join(cfg.SKILLS_DIR, d)).isDirectory(); }
        catch { return false; }
      })
      .map(name => {
        const metaPath = path.join(cfg.SKILLS_DIR, name, '_meta.json');
        let meta = {};
        try { meta = JSON.parse(fs.readFileSync(metaPath, 'utf8')); } catch {}
        return { name, ...meta };
      });
    jsonReply(res, 200, { count: skills.length, skills });
  } catch {
    jsonReply(res, 200, { count: 0, skills: [] });
  }
}

function register(router) {
  router.add('GET', '/api/config',  (req, res) => handleConfig(req, res));
  router.add('GET', '/api/files',   (req, res, q) => handleFiles(req, res, q));
  router.add('GET', '/api/skills',  (req, res) => handleSkills(req, res));

  // Legacy compat (frontend still calls these)
  router.add('GET', '/ops/config',  (req, res) => handleConfig(req, res));
  router.add('GET', '/files',       (req, res, q) => handleFiles(req, res, q));
  // PUT /files removed — dashboard is read-only; file edits go via CLI/Discord.
  router.add('GET', '/skills',      (req, res) => handleSkills(req, res));
  router.add('GET', '/notes',       (_req, res) => jsonReply(res, 200, []));
}

module.exports = { register, _test: { isSensitiveKey, redactSecrets } };
