#!/usr/bin/env node
/**
 * 拉取 fielddef（或从 JSON 导入）并写入 mock-data 目录，供 mock-jsonv2 使用。
 *
 * 鉴权（任选其一，按优先级）：
 *   1) --username + --password，或环境变量 MOFANG_USERNAME + MOFANG_PASSWORD
 *      → POST /magicflu/jwt，复用公共会话逻辑拿到 Bearer + Cookie 后调 fielddef
 *   2) --cookie 或 COOKIE → 浏览器会话 Cookie
 *   3) --import-json → 不访问网络
 *
 * 注意：Windows 下环境变量 USERNAME 常为系统登录名，本脚本不读取 USERNAME，请用 MOFANG_USERNAME 或命令行传参。
 *
 * 用法：
 *   node scripts/fetch-form-spec.mjs --baseUrl http://host:9999 --spaceId <UUID> --formId <UUID> --out ./mock-data --username aitools --password 'xxx'
 *   node scripts/fetch-form-spec.mjs --baseUrl http://host:9999 --spaceLabel "空间名称" --formLabel "表单名称" --out ./mock-data --cookie "JSESSIONID=..."
 *   BASE_URL=http://host:9999 MOFANG_USERNAME=u MOFANG_PASSWORD=p node scripts/fetch-form-spec.mjs --spaceId ... --formId ... --out ./mock-data
 *   node scripts/fetch-form-spec.mjs --baseUrl https://host --spaceId <UUID> --formId <UUID> --out ./mock-data --cookie "JSESSIONID=..."
 *   node scripts/fetch-form-spec.mjs --spaceId <UUID> --formId <UUID> --out ./mock-data --import-json ./fielddef-export.json
 *
 * 环境变量：BASE_URL、SPACE_ID、SPACE_LABEL、FORM_LABEL、COOKIE、MOFANG_USERNAME、MOFANG_PASSWORD、FETCH_TIMEOUT_MS
 */

import { mkdirSync, writeFileSync, readFileSync } from 'fs';
import { resolve, join } from 'path';
import {
  normalizeBaseUrl,
  fetchWithTimeout,
  mergeCookieHeader,
  obtainSessionCookieFromCredentials,
} from './lib/magicflu-session.mjs';

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = {
    baseUrl: process.env.BASE_URL || 'http://localhost:8080',
    spaceId: process.env.SPACE_ID || null,
    spaceLabel: process.env.SPACE_LABEL || null,
    formIds: [],
    formLabels: process.env.FORM_LABEL ? process.env.FORM_LABEL.split(',').map((s) => s.trim()).filter(Boolean) : [],
    out: './mock-data',
    cookie: process.env.COOKIE || null,
    username: process.env.MOFANG_USERNAME || process.env.MAGICFLU_USERNAME || null,
    password: process.env.MOFANG_PASSWORD || process.env.MAGICFLU_PASSWORD || null,
    importJson: null,
  };
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === '--baseUrl' && args[i + 1]) opts.baseUrl = args[++i];
    else if (a === '--spaceId' && args[i + 1]) opts.spaceId = args[++i];
    else if (a === '--spaceLabel' && args[i + 1]) opts.spaceLabel = args[++i];
    else if (a === '--formId' && args[i + 1]) {
      const v = args[++i];
      v.split(',').forEach((id) => {
        const t = id.trim();
        if (t) opts.formIds.push(t);
      });
    } else if (a === '--formLabel' && args[i + 1]) {
      const v = args[++i];
      v.split(',').forEach((label) => {
        const t = label.trim();
        if (t) opts.formLabels.push(t);
      });
    } else if (a === '--out' && args[i + 1]) opts.out = args[++i];
    else if (a === '--cookie' && args[i + 1]) opts.cookie = args[++i];
    else if (a === '--username' && args[i + 1]) opts.username = args[++i];
    else if (a === '--password' && args[i + 1]) opts.password = args[++i];
    else if (a === '--import-json' && args[i + 1]) opts.importJson = args[++i];
  }
  return opts;
}

function authHeaders(auth) {
  const headers = {};
  if (auth.bearerToken) {
    headers['Authorization'] = `Bearer ${auth.bearerToken}`;
  }
  if (auth.cookie) {
    headers['Cookie'] = auth.cookie;
  }
  return headers;
}

async function fetchJson(baseUrl, path, auth, label) {
  const url = `${normalizeBaseUrl(baseUrl)}${path}`;
  const res = await fetchWithTimeout(url, { headers: authHeaders(auth) });
  if (!res.ok) {
    const errBody = await res.text();
    throw new Error(`${label} HTTP ${res.status}: ${errBody.slice(0, 500)}`);
  }
  const raw = await res.text();
  try {
    return JSON.parse(raw);
  } catch {
    throw new Error(`${label} 响应非 JSON: ${raw.slice(0, 300)}`);
  }
}

function withQuery(path, params) {
  const url = new URL(path, 'http://local');
  for (const [k, v] of Object.entries(params)) {
    if (v !== undefined && v !== null) url.searchParams.set(k, String(v));
  }
  return `${url.pathname}${url.search}`;
}

async function fetchFielddef(baseUrl, spaceId, formId, auth) {
  const path = withQuery(`/magicflu/service/s/jsonv2/${encodeURIComponent(spaceId)}/forms/${encodeURIComponent(formId)}`, {
    selector: 'fielddef',
    lng: 'en',
  });
  return fetchJson(baseUrl, path, auth, 'fielddef');
}

async function querySpaces(baseUrl, spaceLabel, auth, op) {
  const path = withQuery('/magicflu/service/json/spaces/feed', {
    start: 0,
    limit: 10,
    bq: `(label,${op},${spaceLabel})`,
  });
  const data = await fetchJson(baseUrl, path, auth, 'spaces/feed');
  return Array.isArray(data.items) ? data.items : [];
}

async function resolveSpaceId(baseUrl, spaceLabel, auth) {
  for (const op of ['eq', 'like_and']) {
    const rows = await querySpaces(baseUrl, spaceLabel, auth, op);
    if (rows.length) {
      if (rows.length > 1) {
        console.warn(`空间名称匹配到 ${rows.length} 个候选，默认使用第一个：${rows[0].label} (${rows[0].id})`);
      }
      return { spaceId: rows[0].id, spaceLabel: rows[0].label || spaceLabel };
    }
  }
  throw new Error(`未找到空间: ${spaceLabel}`);
}

async function queryForms(baseUrl, spaceId, formLabel, auth, op) {
  const path = withQuery(`/magicflu/service/s/json/${encodeURIComponent(spaceId)}/forms/feed`, {
    start: 0,
    limit: 10,
    bq: `(label,${op},${formLabel})`,
  });
  const data = await fetchJson(baseUrl, path, auth, 'forms/feed');
  return Array.isArray(data.feed?.entry) ? data.feed.entry : [];
}

async function resolveFormId(baseUrl, spaceId, formLabel, auth) {
  for (const op of ['eq', 'like_and']) {
    const rows = await queryForms(baseUrl, spaceId, formLabel, auth, op);
    if (rows.length) {
      const first = rows[0];
      const label = first.content?.form?.label || formLabel;
      if (rows.length > 1) {
        console.warn(`表单名称匹配到 ${rows.length} 个候选，默认使用第一个：${label} (${first.id})`);
      }
      return { formId: first.id, formLabel: label };
    }
  }
  throw new Error(`未找到表单: ${formLabel}`);
}

function formLabelFromFielddef(data) {
  return data?.label || data?.form?.label || '';
}

function usage() {
  return (
    '用法: --spaceId <UUID>|--spaceLabel <名称> --formId <UUID>|--formLabel <名称> [--formId/--formLabel ...] ' +
    '--out ./mock-data [--baseUrl URL] [--username u --password p | --cookie ... | --import-json file]'
  );
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function ensureDir(p) {
  mkdirSync(p, { recursive: true });
}

async function main() {
  const opts = parseArgs();
  if (opts.importJson && (!opts.spaceId || opts.formIds.length !== 1)) {
    console.error('使用 --import-json 时请指定 --spaceId，并且只指定一个 --formId');
    process.exit(1);
  }
  if (!opts.importJson && (!opts.spaceId && !opts.spaceLabel)) {
    console.error(usage());
    process.exit(1);
  }
  if (!opts.importJson && !opts.formIds.length && !opts.formLabels.length) {
    console.error(usage());
    process.exit(1);
  }

  const out = resolve(process.cwd(), opts.out);
  ensureDir(out);

  let auth = { bearerToken: null, cookie: null };
  if (!opts.importJson) {
    const hasUserPass = Boolean(opts.username && opts.password);
    if (hasUserPass) {
      const session = await obtainSessionCookieFromCredentials(opts.baseUrl, opts.username, opts.password);
      auth.bearerToken = session.token;
      auth.cookie = mergeCookieHeader(session.cookie, opts.cookie || '');
    } else if (opts.cookie) {
      auth.cookie = opts.cookie;
    } else {
      console.error(
        '拉取 fielddef 需要鉴权，请选择其一：\n' +
          '  --username / --password（或 MOFANG_USERNAME + MOFANG_PASSWORD，推荐）\n' +
          '  --cookie 或环境变量 COOKIE（浏览器已登录会话）\n' +
          '  --import-json（离线，不访问网络）'
      );
      process.exit(1);
    }

    if (!opts.spaceId && opts.spaceLabel) {
      const resolved = await resolveSpaceId(opts.baseUrl, opts.spaceLabel, auth);
      opts.spaceId = resolved.spaceId;
      opts.spaceLabel = resolved.spaceLabel;
      console.log(`已解析空间: ${opts.spaceLabel} (${opts.spaceId})`);
    }

    for (const formLabel of opts.formLabels) {
      const resolved = await resolveFormId(opts.baseUrl, opts.spaceId, formLabel, auth);
      opts.formIds.push(resolved.formId);
      console.log(`已解析表单: ${resolved.formLabel} (${resolved.formId})`);
    }
    opts.formIds = unique(opts.formIds);
  }

  const manifest = {
    spaceId: opts.spaceId,
    ...(opts.spaceLabel ? { spaceLabel: opts.spaceLabel } : {}),
    generatedAt: new Date().toISOString(),
    forms: [],
  };

  for (const formId of opts.formIds) {
    let data;
    if (opts.importJson) {
      const raw = readFileSync(resolve(process.cwd(), opts.importJson), 'utf8');
      data = JSON.parse(raw);
    } else {
      data = await fetchFielddef(opts.baseUrl, opts.spaceId, formId, auth);
    }
    const dir = join(out, formId);
    ensureDir(dir);
    writeFileSync(join(dir, 'fielddef.json'), JSON.stringify(data, null, 2), 'utf8');
    writeFileSync(join(dir, 'records.seed.json'), JSON.stringify([], null, 2), 'utf8');
    manifest.forms.push({ formId, label: formLabelFromFielddef(data) });
  }

  writeFileSync(join(out, 'manifest.json'), JSON.stringify(manifest, null, 2), 'utf8');
  writeFileSync(
    join(out, 'typesnippets.md'),
    '# Type snippets\n\n可根据 fielddef 手工补充类型片段。\n',
    'utf8'
  );
  writeFileSync(join(out, 'api-outline.md'), '# API outline\n\n', 'utf8');

  console.log('已写入', out);
  console.log('下一步: node scripts/mock-jsonv2.mjs --port 3847 --dir', opts.out);
}

main().catch((e) => {
  const msg = e?.cause?.message ? `${e.message}（${e.cause.message}）` : e.message;
  console.error(msg || e);
  process.exit(1);
});
