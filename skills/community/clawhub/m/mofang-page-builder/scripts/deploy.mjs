#!/usr/bin/env node
/**
 * 魔方网表页面部署脚本
 *
 * 流程：创建站点 → 上传文件
 *
 * 鉴权：
 *   - 推荐：--username + --password（或 MOFANG_USERNAME + MOFANG_PASSWORD）
 *     先 POST /magicflu/jwt 取得 token 与 Cookie；**创建站点** 请求会带 Cookie + Authorization: Bearer（与 UI 一致）。
 *     **上传文件** 则 POST 到 /magicflu/html/sites/connectors/jsp/filemanager.jsp?spaceId=…，**仅 Cookie**、Referer 为 site.jsp（与浏览器里站点文件上传一致，不用 websites/upload）。
 *   - 备选：--cookie / COOKIE — 可单独或与账号密码合并（Cookie 头会与 JWT 登录结果合并）
 *
 * 用法：
 *   node scripts/deploy.mjs --spaceId xxx --label "我的站点" --shortcut mysite --files index.html \\
 *     --username u --password 'p'
 *   node scripts/deploy.mjs --spaceId xxx --label "站点" --shortcut s1 --files a.html,b.css --cookie "JSESSIONID=xxx"
 *
 * 环境变量：BASE_URL、SPACE_ID、COOKIE、MOFANG_USERNAME、MOFANG_PASSWORD（亦支持 MAGICFLU_USERNAME / MAGICFLU_PASSWORD）
 *          FETCH_TIMEOUT_MS（可选，默认 120000）：单次 HTTP 超时毫秒数，避免服务无响应时长时间卡住
 */

import { readFileSync } from 'fs';
import { resolve, basename } from 'path';
import {
  normalizeBaseUrl,
  fetchWithTimeout,
  pairsFromSetCookieResponse,
  mergeCookieHeader,
  obtainSessionCookieFromCredentials,
} from './lib/magicflu-session.mjs';

/** 打开站点页（与实际上传时的 Referer 一致），合并 Set-Cookie，利于 filemanager 上传识别会话 */
async function warmSessionViaSiteJsp(baseUrl, spaceId, websiteId, cookie, bearerToken) {
  const root = normalizeBaseUrl(baseUrl);
  const url = `${root}/magicflu/html/sites/site.jsp?spaceId=${encodeURIComponent(spaceId)}&websiteId=${encodeURIComponent(websiteId)}`;
  const headers = {
    Cookie: cookie,
    Authorization: `Bearer ${bearerToken}`,
  };
  const res = await fetchWithTimeout(url, { headers });
  const merged = mergeCookieHeader(cookie, pairsFromSetCookieResponse(res).join('; '));
  await res.text().catch(() => '');
  return merged;
}

/** multipart 中文件部分的 Content-Type，与浏览器 DevTools 中常见类型对齐 */
function mimeForUploadFilename(name) {
  const ext = String(name).toLowerCase().split('.').pop() || '';
  const map = {
    html: 'text/html',
    htm: 'text/html',
    css: 'text/css',
    js: 'application/javascript',
    mjs: 'application/javascript',
    json: 'application/json',
    png: 'image/png',
    jpg: 'image/jpeg',
    jpeg: 'image/jpeg',
    gif: 'image/gif',
    svg: 'image/svg+xml',
    woff: 'font/woff',
    woff2: 'font/woff2',
  };
  return map[ext] || 'application/octet-stream';
}

// ========== 解析参数 ==========
function parseArgs() {
  const args = process.argv.slice(2);
  const opts = {
    spaceId: process.env.SPACE_ID,
    baseUrl: process.env.BASE_URL || 'http://localhost:8080',
    label: '魔方定制页',
    shortcut: 'custom',
    desc: '',
    files: [],
    cookie: process.env.COOKIE || null,
    username: process.env.MOFANG_USERNAME || process.env.MAGICFLU_USERNAME || null,
    password: process.env.MOFANG_PASSWORD || process.env.MAGICFLU_PASSWORD || null,
  };

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--spaceId' && args[i + 1]) opts.spaceId = args[++i];
    else if (args[i] === '--baseUrl' && args[i + 1]) opts.baseUrl = args[++i];
    else if (args[i] === '--label' && args[i + 1]) opts.label = args[++i];
    else if (args[i] === '--shortcut' && args[i + 1]) opts.shortcut = args[++i];
    else if (args[i] === '--desc' && args[i + 1]) opts.desc = args[++i];
    else if (args[i] === '--files' && args[i + 1]) opts.files = args[++i].split(',').map((f) => f.trim()).filter(Boolean);
    else if (args[i] === '--cookie' && args[i + 1]) opts.cookie = args[++i];
    else if (args[i] === '--username' && args[i + 1]) opts.username = args[++i];
    else if (args[i] === '--password' && args[i + 1]) opts.password = args[++i];
  }

  return opts;
}

// ========== 创建站点 XML ==========
function buildCreateSiteXml(spaceId, label, shortcut, desc) {
  return `<entry><id></id><content><website><label>${escapeXml(label)}</label><shortcut>${escapeXml(shortcut)}</shortcut><homePage>index.html</homePage><loginPage>undefined</loginPage><encoding>UTF-8</encoding><desc>${escapeXml(desc)}</desc><defaulte>0</defaulte><classid></classid><aclLevel>0</aclLevel><publick>0</publick><spaceId>${escapeXml(spaceId)}</spaceId></website></content></entry>`;
}

function escapeXml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

// ========== 步骤 1: 创建站点 ==========
async function createSite(baseUrl, spaceId, label, shortcut, desc, cookie, bearerToken) {
  const root = normalizeBaseUrl(baseUrl);
  const url = `${root}/magicflu/service/s/${spaceId}/websites`;
  const xml = buildCreateSiteXml(spaceId, label, shortcut, desc);

  const headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    Referer: `${root}/magicflu/html/form/newwebsite.jsp?spaceId=${encodeURIComponent(spaceId)}`,
  };
  if (cookie) headers['Cookie'] = cookie;
  if (bearerToken) headers['Authorization'] = `Bearer ${bearerToken}`;

  const res = await fetchWithTimeout(url, {
    method: 'POST',
    headers,
    body: xml,
  });

  const setCookieFromCreate = pairsFromSetCookieResponse(res).join('; ');

  if (res.status !== 201) {
    const text = await res.text();
    throw new Error(`创建站点失败 HTTP ${res.status}: ${text.slice(0, 200)}`);
  }

  const websiteId = (await res.text()).trim();
  if (!websiteId) throw new Error('创建站点成功但未返回 websiteId');
  return { websiteId, setCookieFromCreate };
}

// ========== 步骤 2: 上传文件（与 site.jsp 内文件管理器一致：connectors/jsp/filemanager.jsp） ==========
async function uploadFile(baseUrl, spaceId, websiteId, filePath, content, cookie, usedJwtLogin) {
  const root = normalizeBaseUrl(baseUrl);
  const qp = new URLSearchParams({ spaceId });
  const url = `${root}/magicflu/html/sites/connectors/jsp/filemanager.jsp?${qp.toString()}`;
  const filename = basename(filePath);
  const currentpath = `/magicflu/html/sites/userfiles/${websiteId}/`;

  const form = new FormData();
  form.append('mode', 'add');
  form.append('currentpath', currentpath);
  form.append('newfile', new Blob([content], { type: mimeForUploadFilename(filename) }), filename);
  form.append('upload', 'Upload');

  const refererSite = `${root}/magicflu/html/sites/site.jsp?spaceId=${encodeURIComponent(spaceId)}&websiteId=${encodeURIComponent(websiteId)}`;
  const headers = {
    'X-Requested-With': 'XMLHttpRequest',
    Referer: refererSite,
    Origin: root,
  };
  if (cookie) headers['Cookie'] = cookie;

  const res = await fetchWithTimeout(url, {
    method: 'POST',
    headers,
    body: form,
  });

  const text = await res.text();
  let json;
  const m = text.match(/\{[\s\S]*\}/);
  if (m) {
    try {
      json = JSON.parse(m[0]);
    } catch (_) {}
  }

  if (json && json.Code === 0) {
    return { success: true, filename };
  }
  const errPreview = json?.Error || text.slice(0, 200);
  const cookieHint =
    usedJwtLogin && /未登录|重新登录/.test(String(errPreview + text))
      ? ' 若仍无法上传，请从已打开站点页的浏览器复制完整 Cookie，通过 --cookie / COOKIE 与账号登录结果合并后再试。'
      : '';
  throw new Error(`上传 ${filename} 失败: ${errPreview}${cookieHint}`);
}

// ========== 主流程 ==========
async function main() {
  const opts = parseArgs();

  if (!opts.spaceId) {
    console.error('错误：请提供 --spaceId 或设置环境变量 SPACE_ID');
    process.exit(1);
  }
  if (!opts.files.length) {
    console.error('错误：请提供 --files index.html[,style.css,...]');
    process.exit(1);
  }

  let cookie = opts.cookie;
  /** 账号密码登录得到的 JWT，建站/上传需与 Cookie 一并携带（与同域 UI 一致） */
  let bearerToken = null;
  const hasUserPass = Boolean(opts.username && opts.password);

  if (hasUserPass) {
    console.log('正在使用账号密码登录并获取会话 Cookie...');
    const session = await obtainSessionCookieFromCredentials(opts.baseUrl, opts.username, opts.password);
    cookie = mergeCookieHeader(session.cookie, cookie || '');
    bearerToken = session.token;
  }

  if (!cookie) {
    console.error('错误：请提供 --cookie / COOKIE，或 --username + --password（或 MOFANG_USERNAME + MOFANG_PASSWORD）');
    process.exit(1);
  }

  const cwd = process.cwd();

  try {
    console.log('正在创建站点...');
    const created = await createSite(
      opts.baseUrl,
      opts.spaceId,
      opts.label,
      opts.shortcut,
      opts.desc,
      cookie,
      bearerToken
    );
    const websiteId = created.websiteId;
    if (created.setCookieFromCreate) {
      cookie = mergeCookieHeader(cookie, created.setCookieFromCreate);
    }
    console.log('站点已创建，websiteId:', websiteId);

    if (bearerToken) {
      console.log('正在打开站点页以同步会话...');
      try {
        cookie = await warmSessionViaSiteJsp(opts.baseUrl, opts.spaceId, websiteId, cookie, bearerToken);
      } catch (e) {
        console.warn('站点页预热跳过:', e.message);
      }
    }

    for (const f of opts.files) {
      const filePath = resolve(cwd, f);
      const content = readFileSync(filePath);
      await uploadFile(opts.baseUrl, opts.spaceId, websiteId, f, content, cookie, hasUserPass);
      console.log('已上传:', f);
    }

    const indexFile = opts.files.find((f) => f.toLowerCase().endsWith('index.html')) || opts.files[0];
    const visitPath = `/magicflu/html/sites/userfiles/${opts.spaceId}/${websiteId}/${basename(indexFile)}`;
    const visitUrl = `${normalizeBaseUrl(opts.baseUrl)}${visitPath}`;

    console.log('\n部署完成！');
    console.log('访问地址:', visitUrl);
  } catch (e) {
    const msg = e?.cause?.message ? `${e.message}（${e.cause.message}）` : e.message;
    console.error('部署失败:', msg);
    process.exit(1);
  }
}

main();
