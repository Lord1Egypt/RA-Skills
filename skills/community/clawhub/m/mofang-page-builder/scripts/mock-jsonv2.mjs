#!/usr/bin/env node
/**
 * jsonv2 本地服务：
 * - mock（默认）：spaces/feed + forms/feed + fielddef + 记录列表/增删改（本地 mock-data + 内存）
 * - proxy：将 /magicflu/service/json/spaces/feed、/magicflu/service/s/json... 和 /magicflu/service/s/jsonv2/... 转发到真实魔方（服务端鉴权）
 *
 * 用法：
 *   node scripts/mock-jsonv2.mjs --port 3847 --dir ./mock-data
 *   node scripts/mock-jsonv2.mjs --mode proxy --port 3847 --baseUrl http://host:9999 --username u --password p
 *   BASE_URL=... MOFANG_USERNAME=... MOFANG_PASSWORD=... node scripts/mock-jsonv2.mjs --mode proxy --port 3847
 *
 * 环境变量（proxy）：BASE_URL、MOFANG_USERNAME、MOFANG_PASSWORD、COOKIE、FETCH_TIMEOUT_MS
 */

import { createServer } from 'http';
import { readFileSync, existsSync, readdirSync, statSync } from 'fs';
import { join, resolve } from 'path';
import {
  normalizeBaseUrl,
  fetchWithTimeout,
  mergeCookieHeader,
  obtainSessionCookieFromCredentials,
} from './lib/magicflu-session.mjs';

const stores = new Map();

function parseArgs() {
  const a = process.argv.slice(2);
  let port = 3847;
  let dir = './mock-data';
  let mode = process.env.MOCK_JSONV2_MODE || 'mock';
  let baseUrl = process.env.BASE_URL || null;
  let cookie = process.env.COOKIE || null;
  let username = process.env.MOFANG_USERNAME || process.env.MAGICFLU_USERNAME || null;
  let password = process.env.MOFANG_PASSWORD || process.env.MAGICFLU_PASSWORD || null;

  for (let i = 0; i < a.length; i++) {
    if (a[i] === '--port' && a[i + 1]) port = parseInt(a[++i], 10);
    else if (a[i] === '--dir' && a[i + 1]) dir = a[++i];
    else if (a[i] === '--mode' && a[i + 1]) mode = String(a[++i]).toLowerCase();
    else if (a[i] === '--baseUrl' && a[i + 1]) baseUrl = a[++i];
    else if (a[i] === '--cookie' && a[i + 1]) cookie = a[++i];
    else if (a[i] === '--username' && a[i + 1]) username = a[++i];
    else if (a[i] === '--password' && a[i + 1]) password = a[++i];
  }

  if (mode !== 'mock' && mode !== 'proxy') {
    console.error('错误：--mode 仅支持 mock 或 proxy');
    process.exit(1);
  }

  return {
    port,
    dir: resolve(process.cwd(), dir),
    mode,
    baseUrl,
    cookie,
    username,
    password,
  };
}

function loadStore(baseDir, formId) {
  const seedPath = join(baseDir, formId, 'records.seed.json');
  let seed = [];
  if (existsSync(seedPath)) {
    try {
      seed = JSON.parse(readFileSync(seedPath, 'utf8'));
      if (!Array.isArray(seed)) seed = [];
    } catch {
      seed = [];
    }
  }
  const records = seed.map((r) => ({ ...r }));
  let maxId = records.reduce((m, r) => {
    const n = parseInt(String(r.id ?? 0), 10);
    return Number.isFinite(n) ? Math.max(m, n) : m;
  }, 0);
  stores.set(formId, { records, nextId: maxId + 1 });
}

function ensureStore(baseDir, formId) {
  if (stores.has(formId)) return true;
  if (!existsSync(join(baseDir, formId, 'fielddef.json'))) return false;
  loadStore(baseDir, formId);
  return true;
}

function cors(res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS,PATCH');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
}

function sendJson(res, code, obj) {
  cors(res);
  res.writeHead(code, { 'Content-Type': 'application/json; charset=utf-8' });
  res.end(JSON.stringify(obj));
}

function sendText(res, code, text) {
  cors(res);
  res.writeHead(code, { 'Content-Type': 'text/plain; charset=utf-8' });
  res.end(text);
}

async function readBodyJson(req) {
  const chunks = [];
  for await (const c of req) chunks.push(c);
  const raw = Buffer.concat(chunks).toString('utf8');
  if (!raw) return {};
  try {
    return JSON.parse(raw);
  } catch {
    return {};
  }
}

async function readRawBody(req) {
  const chunks = [];
  for await (const c of req) chunks.push(c);
  return Buffer.concat(chunks);
}

function isMagicfluServiceProxyPath(pathname) {
  return (
    pathname === '/magicflu/service/json/spaces/feed' ||
    pathname === '/magicflu/service/s/jsonv2' ||
    pathname.startsWith('/magicflu/service/s/jsonv2/') ||
    pathname === '/magicflu/service/s/json' ||
    pathname.startsWith('/magicflu/service/s/json/')
  );
}

/**
 * @param {import('http').IncomingMessage} req
 * @param {import('http').ServerResponse} res
 * @param {string} baseUrl
 * @param {{ cookie: string | null, token: string | null }} session
 */
async function proxyJsonv2(req, res, baseUrl, session) {
  const u = new URL(req.url || '/', `http://${req.headers.host || 'localhost'}`);
  const targetUrl = `${normalizeBaseUrl(baseUrl)}${u.pathname}${u.search}`;

  const headers = {};
  const ct = req.headers['content-type'];
  if (ct) headers['Content-Type'] = ct;
  const acc = req.headers['accept'];
  if (acc) headers['Accept'] = acc;

  if (session.cookie) headers['Cookie'] = session.cookie;
  if (session.token) headers['Authorization'] = `Bearer ${session.token}`;

  const init = { method: req.method, headers };
  if (req.method !== 'GET' && req.method !== 'HEAD') {
    init.body = await readRawBody(req);
  }

  const upstream = await fetchWithTimeout(targetUrl, init);
  const buf = Buffer.from(await upstream.arrayBuffer());

  cors(res);
  const uct = upstream.headers.get('content-type');
  if (uct) res.setHeader('Content-Type', uct);

  res.writeHead(upstream.status);
  res.end(buf);
}

function discoverFormIds(baseDir) {
  const ids = new Set();
  const man = join(baseDir, 'manifest.json');
  if (existsSync(man)) {
    try {
      const m = JSON.parse(readFileSync(man, 'utf8'));
      for (const f of m.forms || []) {
        if (f.formId) ids.add(f.formId);
      }
    } catch {
      /* ignore */
    }
  }
  if (!ids.size && existsSync(baseDir)) {
    for (const n of readdirSync(baseDir)) {
      try {
        if (statSync(join(baseDir, n)).isDirectory() && existsSync(join(baseDir, n, 'fielddef.json'))) {
          ids.add(n);
        }
      } catch {
        /* ignore */
      }
    }
  }
  return [...ids];
}

function readManifest(baseDir) {
  const man = join(baseDir, 'manifest.json');
  if (!existsSync(man)) return {};
  try {
    return JSON.parse(readFileSync(man, 'utf8'));
  } catch {
    return {};
  }
}

function readManifestForms(baseDir) {
  const forms = new Map();
  const m = readManifest(baseDir);
  for (const f of m.forms || []) {
    const formId = f.formId || f.id;
    if (formId) forms.set(formId, { ...f, formId });
  }
  for (const formId of discoverFormIds(baseDir)) {
    if (!forms.has(formId)) forms.set(formId, { formId });
  }
  return [...forms.values()];
}

function matchesLabelBq(label, bq) {
  const match = String(bq || '').match(/^\(label,(eq|like_and),(.+)\)$/);
  if (!match) return true;
  const op = match[1];
  const needle = match[2];
  return op === 'eq' ? label === needle : label.includes(needle);
}

function buildSpacesFeed(baseDir, bq) {
  const m = readManifest(baseDir);
  const spaceId = m.spaceId || '00000000-0000-0000-0000-000000000001';
  const label = m.spaceLabel || m.label || spaceId;
  const items = matchesLabelBq(label, bq)
    ? [
        {
          id: spaceId,
          label,
          desc: m.spaceDesc || '',
          defaulte: 0,
        },
      ]
    : [];
  return { items, totalCount: items.length };
}

function buildFormsFeed(baseDir, bq) {
  const rows = readManifestForms(baseDir)
    .map((f) => {
      const meta = readFielddefMeta(baseDir, f.formId);
      const label = f.label || meta.label || f.formId;
      return {
        id: f.formId,
        content: {
          form: {
            label,
            name: f.name || meta.name || '',
            desc: f.desc || meta.desc || '',
          },
        },
      };
    })
    .filter((row) => matchesLabelBq(row.content.form.label || '', bq));

  return rows;
}

function readFielddefMeta(baseDir, formId) {
  try {
    const data = JSON.parse(readFileSync(join(baseDir, formId, 'fielddef.json'), 'utf8'));
    const form = data.form && typeof data.form === 'object' ? data.form : data;
    return {
      label: form.label || data.label || '',
      name: form.name || data.name || '',
      desc: form.desc || data.desc || '',
    };
  } catch {
    return { label: '', name: '', desc: '' };
  }
}

async function main() {
  const opts = parseArgs();

  /** @type {{ cookie: string | null, token: string | null } | null} */
  let session = null;

  if (opts.mode === 'proxy') {
    const base = opts.baseUrl || process.env.BASE_URL;
    if (!base) {
      console.error('错误：proxy 模式需要 --baseUrl 或环境变量 BASE_URL');
      process.exit(1);
    }
    opts.baseUrl = base;

    const hasUserPass = Boolean(opts.username && opts.password);
    if (hasUserPass) {
      console.log('proxy：正在使用账号密码登录并获取会话...');
      const s = await obtainSessionCookieFromCredentials(opts.baseUrl, opts.username, opts.password);
      session = {
        cookie: mergeCookieHeader(s.cookie, opts.cookie || ''),
        token: s.token,
      };
    } else if (opts.cookie) {
      session = { cookie: opts.cookie, token: null };
    } else {
      console.error(
        '错误：proxy 需要鉴权：--username + --password（或 MOFANG_USERNAME + MOFANG_PASSWORD），或 --cookie / COOKIE',
      );
      process.exit(1);
    }
  } else {
    if (!existsSync(opts.dir)) {
      console.error('错误：mock 模式需要有效的 mock-data 目录：', opts.dir);
      process.exit(1);
    }
    for (const fid of discoverFormIds(opts.dir)) {
      loadStore(opts.dir, fid);
    }
  }

  createServer(async (req, res) => {
    if (req.method === 'OPTIONS') {
      cors(res);
      res.writeHead(204);
      res.end();
      return;
    }

    const url = new URL(req.url || '/', `http://${req.headers.host || 'localhost'}`);
    const path = url.pathname.replace(/\/$/, '') || '/';

    if (opts.mode === 'proxy' && isMagicfluServiceProxyPath(path)) {
      try {
        await proxyJsonv2(req, res, opts.baseUrl, session);
      } catch (e) {
        const msg = e?.message || String(e);
        sendText(res, 502, `mock-jsonv2 proxy: ${msg}`);
      }
      return;
    }

    if (opts.mode !== 'mock') {
      sendText(res, 404, `mock-jsonv2: no route ${req.method} ${path}`);
      return;
    }

    if (path === '/magicflu/service/json/spaces/feed' && req.method === 'GET') {
      sendJson(res, 200, buildSpacesFeed(opts.dir, url.searchParams.get('bq')));
      return;
    }

    const mForms = path.match(/^\/magicflu\/service\/s\/json\/([^/]+)\/forms\/feed$/);
    if (mForms && req.method === 'GET') {
      const entryAll = buildFormsFeed(opts.dir, url.searchParams.get('bq'));
      const start = parseInt(url.searchParams.get('start') || '0', 10) || 0;
      const rawLimit = parseInt(url.searchParams.get('limit') || '20', 10);
      const limit = Number.isFinite(rawLimit) ? rawLimit : 20;
      const entry = limit < 0 ? entryAll.slice(start) : entryAll.slice(start, start + limit);
      sendJson(res, 200, { feed: { entry, totalCount: entryAll.length } });
      return;
    }

    const mField = path.match(/^\/magicflu\/service\/s\/jsonv2\/([^/]+)\/forms\/([^/]+)$/);
    if (mField && req.method === 'GET' && url.searchParams.get('selector') === 'fielddef') {
      const formId = mField[2];
      if (!ensureStore(opts.dir, formId)) {
        sendJson(res, 404, { error: 'unknown form', formId });
        return;
      }
      try {
        const data = JSON.parse(readFileSync(join(opts.dir, formId, 'fielddef.json'), 'utf8'));
        sendJson(res, 200, data);
      } catch (e) {
        sendJson(res, 500, { error: String(e.message) });
      }
      return;
    }

    const mList = path.match(/^\/magicflu\/service\/s\/jsonv2\/([^/]+)\/forms\/([^/]+)\/records\/entry$/);
    if (mList && req.method === 'GET') {
      const formId = mList[2];
      if (!ensureStore(opts.dir, formId)) {
        sendJson(res, 404, { error: 'unknown form', formId });
        return;
      }
      const start = parseInt(url.searchParams.get('start') || '0', 10) || 0;
      const rawLimit = parseInt(url.searchParams.get('limit') || '20', 10);
      const limit = Number.isFinite(rawLimit) ? rawLimit : 20;
      const store = stores.get(formId);
      const entry = limit < 0 ? store.records.slice(start) : store.records.slice(start, start + limit);
      sendJson(res, 200, { entry, totalCount: store.records.length });
      return;
    }

    const mCreate = path.match(/^\/magicflu\/service\/s\/jsonv2\/([^/]+)\/forms\/([^/]+)\/records$/);
    if (mCreate && req.method === 'POST') {
      const formId = mCreate[2];
      if (!ensureStore(opts.dir, formId)) {
        sendJson(res, 404, { error: 'unknown form', formId });
        return;
      }
      const body = await readBodyJson(req);
      const payload = body.data && typeof body.data === 'object' ? body.data : body;
      const store = stores.get(formId);
      const id = store.nextId++;
      const row = { ...payload, id };
      store.records.push(row);
      sendJson(res, 201, row);
      return;
    }

    const mEntryId = path.match(/^\/magicflu\/service\/s\/jsonv2\/([^/]+)\/forms\/([^/]+)\/records\/entry\/([^/]+)$/);
    if (mEntryId && req.method === 'PUT') {
      const formId = mEntryId[2];
      const rid = mEntryId[3];
      if (!ensureStore(opts.dir, formId)) {
        sendJson(res, 404, { error: 'unknown form', formId });
        return;
      }
      const body = await readBodyJson(req);
      const payload = body.data && typeof body.data === 'object' ? body.data : body;
      const store = stores.get(formId);
      const idx = store.records.findIndex((r) => String(r.id) === String(rid));
      if (idx < 0) {
        sendJson(res, 404, { error: 'record not found' });
        return;
      }
      store.records[idx] = { ...store.records[idx], ...payload, id: store.records[idx].id };
      sendJson(res, 200, store.records[idx]);
      return;
    }

    if (mEntryId && req.method === 'DELETE') {
      const formId = mEntryId[2];
      const rid = mEntryId[3];
      if (!ensureStore(opts.dir, formId)) {
        sendJson(res, 404, { error: 'unknown form', formId });
        return;
      }
      const store = stores.get(formId);
      const before = store.records.length;
      store.records = store.records.filter((r) => String(r.id) !== String(rid));
      if (store.records.length === before) {
        sendJson(res, 404, { error: 'record not found' });
        return;
      }
      sendJson(res, 200, { ok: true });
      return;
    }

    sendText(res, 404, `mock-jsonv2: no route ${req.method} ${path}`);
  }).listen(opts.port, () => {
    console.log(`jsonv2 ${opts.mode} listening http://127.0.0.1:${opts.port}`);
    if (opts.mode === 'mock') {
      console.log(`data dir: ${opts.dir}`);
    } else {
      console.log(`upstream: ${normalizeBaseUrl(opts.baseUrl)}`);
      console.warn('proxy 模式会读写真实魔方数据，POST/PUT/DELETE 将影响线上记录。');
    }
  });
}

main().catch((e) => {
  console.error(e.message || e);
  process.exit(1);
});
