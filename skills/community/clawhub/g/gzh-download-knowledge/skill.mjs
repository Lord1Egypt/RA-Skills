#!/usr/bin/env node
/**
 * gzh-download-knowledge — 公众号文章下载归档（自己的公众号历史文章 → 本地 Markdown）
 *
 * 编排器分工：
 * - 确定性浏览器操作（URL 构造、导航、page.eval + DOM 提取、去重、写文件）→ 直接代码，
 *   全部走 Extension Relay HTTP API（:3459），不使用 CDP。
 *
 * 关键决策注释：
 * 1. 全程串行单 tab：微信系（mp.weixin.qq.com）无授权请求对访问频率有严格限制，并发开多 tab 会触发访问限制；
 *    每条间隔 ≥2.5s，翻页/开 tab 后 sleep 6s 等加载。
 * 2. 只做自己的公众号：后台「发表记录」是官方全量历史列表（按发布日期倒序），账号由登录态决定，
 *    无需传 account；offset 直接映射到发表记录分页参数 begin（增量归档）。
 * 3. 去重用稳定短码（mp.weixin.qq.com/s/XXX 无参数、跨次稳定）。
 * 4. page.eval 的 JS 一律不用可选链 / 内嵌反引号模板串 / ${}——relay JSON 转义会报错，用普通 if 写法。
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync } from 'node:fs';
import { join, resolve, dirname } from 'node:path';
import { tmpdir } from 'node:os';
import { fileURLToPath } from 'node:url';
const SKILL_HOME = dirname(fileURLToPath(import.meta.url));
const RUNS_DIR = join(SKILL_HOME, 'runs');

const RELAY_URL = 'http://127.0.0.1:3459';
const TMP = join(tmpdir(), 'gzh-download-knowledge-' + process.pid);

// ---------- 时序常量（微信系访问节奏） ----------
const SLEEP_OPEN_MS = 6000;    // 开 tab / 翻页后等页面加载（微信页面慢）
const SLEEP_ITEM_MS = 2500;    // 条与条之间间隔，控制访问节奏
const PAGE_SIZE = 10;          // 发表记录每页 10 条
const MAX_PAGES = 10;          // 翻页封顶
const RETRY_ATTEMPTS = 3;      // 扩展瞬时断开重试次数
const RETRY_SLEEP_MS = 3000;

// ---------- Extension Relay HTTP API ----------
async function relayCall(op, params = {}, timeout = 30000) {
  const res = await fetch(`${RELAY_URL}/api/call`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ op, params, timeout }),
  });
  const data = await res.json();
  if (data.error) throw new Error(data.error);
  return data.result;
}

async function callWithRetry(op, params = {}, timeout = 30000, attempts = RETRY_ATTEMPTS) {
  // 微信系页面跳转时扩展会瞬时断开（几秒后自动重连）——sleep 后重试吸收
  let lastErr;
  for (let i = 0; i < attempts; i++) {
    try {
      return await relayCall(op, params, timeout);
    } catch (e) {
      lastErr = e;
      await sleep(RETRY_SLEEP_MS);
    }
  }
  throw lastErr;
}

async function ensureRelay() {
  // 微信系页面跳转会触发扩展瞬时断开（几秒后自动重连）——启动检查也要重试吸收
  let lastErr;
  for (let i = 0; i < RETRY_ATTEMPTS; i++) {
    try {
      const status = await (await fetch(`${RELAY_URL}/api/status`)).json();
      if (!status.extensionConnected) throw new Error('extension not connected');
      return;
    } catch (e) {
      lastErr = e;
      await sleep(RETRY_SLEEP_MS);
    }
  }
  throw new Error(
    `浏览器中继服务不可用（${RELAY_URL}）。请先确认环境：1) 浏览器中继扩展已安装并启用；2) 中继服务已启动。` +
    `可用 \`curl -s ${RELAY_URL}/api/status\` 检查，或让 agent 检查浏览器中继环境。原错误：${lastErr && lastErr.message}`
  );
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

function pageEval(tabId, code) {
  return callWithRetry('page.eval', { tabId, code });
}

// ---------- 页面提取 JS ----------
// 后台首页：取 location.href 中的 token（未登录时无 token）
const EXTRACT_LOGIN = `(()=>{const href=location.href;const m=href.match(/[?&]token=(\\d+)/);return JSON.stringify({href:href,token:m?m[1]:''});})()`;

// 发表记录页：正文文本中的「全部 N」= 历史文章总数（翻页终止判断用）
const EXTRACT_OWN_TOTAL = `(()=>{const m=document.body.innerText.match(/全部\\s*(\\d+)/);return JSON.stringify({total:m?parseInt(m[1],10):0});})()`;

// 发表记录列表：以 .publish_hover_content 为遍历单位（日期组容器）。
// 文章标题 a 的 href 即稳定短码 mp.weixin.qq.com/s/XXX；"已删除"条目是 tempkey 签名式
// （mp.weixin.qq.com/s?__biz=...），不匹配 a[href^="https://mp.weixin.qq.com/s/"]，天然跳过。
const EXTRACT_OWN_LIST = `(()=>{const arts=[];const groups=document.querySelectorAll('.publish_hover_content');groups.forEach(phc=>{const tEl=phc.querySelector('.weui-desktop-mass__time');const date=tEl?tEl.innerText.trim():'';const items=phc.querySelectorAll('.weui-desktop-mass-appmsg');items.forEach(item=>{const a=item.querySelector('a[href^="https://mp.weixin.qq.com/s/"]');if(!a)return;const sp=a.querySelector('span');const title=sp?sp.innerText.trim():'';arts.push({title:title,date:date,shortUrl:a.href});});});return JSON.stringify({count:arts.length,arts:arts});})()`;

// 正文提取：#activity-name 标题 / #js_content 正文 / #js_name 公众号名
const EXTRACT_CONTENT = `(()=>{const t=document.querySelector('#activity-name');const c=document.querySelector('#js_content');const n=document.querySelector('#js_name');const og=document.querySelector('meta[property="og:url"]');const body=document.body?document.body.innerText:'';return JSON.stringify({title:t?t.innerText.trim():'',content:c?c.innerText.trim():'',author:n?n.innerText.trim():'',ogUrl:og?og.content:'',url:location.href,deleted:(body.indexOf('已被发布者删除')>=0||body.indexOf('内容已被发布者删除')>=0)});})()`;

// ---------- 通用工具 ----------
function q(s) {
  return '"' + String(s).replace(/\\/g, '\\\\').replace(/"/g, '\\"') + '"';
}
function sanitizeTitle(s) {
  const t = String(s).replace(/[\u0000-\u001f\\/:*?"<>|]/g, '_').trim();
  return t || 'untitled';
}
function shortCodeOf(url) {
  const m = String(url).match(/mp\.weixin\.qq\.com\/s\/([A-Za-z0-9_-]+)/);
  return m ? m[1] : '';
}
function normalizeTitle(s) {
  return String(s).replace(/\s+/g, '');
}

// 从既有产物扫描去重 key：
// own 用稳定短码（frontmatter url: 行），sogou 用标题（frontmatter title: 行，去空白）。
// articles/*.md 缺失（如 csv 模式）时，从上次 index.json 的 articles 补 key，保证跨次/跨格式去重。
function loadExistingKeys(exportDir) {
  const seenUrl = new Set();
  const seenTitle = new Set();
  const articlesDir = join(exportDir, 'articles');
  let fileCount = 0;
  if (existsSync(articlesDir)) {
    for (const f of readdirSync(articlesDir)) {
      if (!f.endsWith('.md')) continue;
      fileCount++;
      let txt;
      try { txt = readFileSync(join(articlesDir, f), 'utf-8'); } catch { continue; }
      const m = txt.match(/^url:\s*"?(https:\/\/mp\.weixin\.qq\.com\/s\/[A-Za-z0-9_-]+)/m);
      if (m) seenUrl.add(m[1]);
      const t = txt.match(/^title:\s*"?(.+?)"?\s*$/m);
      if (t) seenTitle.add(normalizeTitle(t[1]));
    }
  }
  const idxFile = join(exportDir, 'index.json');
  if (existsSync(idxFile)) {
    try {
      const idx = JSON.parse(readFileSync(idxFile, 'utf-8'));
      for (const a of (idx.articles || [])) {
        const code = shortCodeOf(a.url || '');
        if (code) seenUrl.add(code);
        if (a.title) seenTitle.add(normalizeTitle(a.title));
      }
    } catch { /* 旧 index 损坏不影响本次 */ }
  }
  return { seenUrl, seenTitle, fileCount };
}

function writeMdArticle(exportDir, seq, meta, content) {
  const dir = join(exportDir, 'articles');
  mkdirSync(dir, { recursive: true });
  const md = `---\ntitle: ${q(meta.title)}\nauthor: ${q(meta.author)}\nurl: ${q(meta.url)}\ndate: ${q(meta.date)}\n---\n\n${content}\n`;
  let base = `${String(seq).padStart(2, '0')}-${sanitizeTitle(meta.title.slice(0, 20))}`;
  let file = join(dir, base + '.md');
  let i = 2;
  while (existsSync(file)) { file = join(dir, `${base}-${i}.md`); i++; }
  writeFileSync(file, md, 'utf-8');
}

// 打开一篇公众号文章页并提取正文（稳定短码链接直接打开，无签名）
async function fetchArticle(openUrl) {
  const t = await callWithRetry('tab.create', { url: openUrl, active: false }, 30000, 2);
  try {
    await sleep(SLEEP_OPEN_MS);
    let res = JSON.parse(await pageEval(t.id, EXTRACT_CONTENT));
    // 页面加载慢时内容可能还没渲染：轮询补几轮，避免把"没渲染好"误判成"已删除"
    for (let i = 0; i < 3 && !res.title && !res.content && !res.deleted; i++) {
      await sleep(2000);
      res = JSON.parse(await pageEval(t.id, EXTRACT_CONTENT));
    }
    return res;
  } finally {
    try { await callWithRetry('tab.close', { tabId: t.id }); } catch { /* tab 可能已关 */ }
  }
}

// ---------- 状态汇总 ----------
function buildMeta(meta, count) {
  const { saved, skipped, reasons } = meta;
  if (saved >= count) { meta.status = 'success'; }
  else if (saved > 0) { meta.status = 'partial'; meta.reason = reasons.join('；') || `只保存到 ${saved} 篇，未达 count=${count}`; }
  else if (skipped > 0) { meta.status = 'success'; meta.reason = `本次运行全部命中去重（${skipped} 篇已存在），未新增保存`; }
  else { meta.status = 'partial'; meta.reason = reasons.join('；') || '未保存到任何文章'; }
  meta.reason = meta.reason || '';
  return meta;
}

// ---------- own 模式（自己公众号：后台发表记录） ----------

// 获取后台会话 token（微信要求带 token 访问，无 token 会"请重新登录"）：
// 1) 用户提供带 token 的后台 URL（homeUrl 入参，从浏览器地址栏复制）
// 2) 浏览器里已打开的 mp.weixin.qq.com/cgi-bin 后台 tab（URL 带 token）
// 3) 打开不带 token 的 home 页碰运气（已登录会话偶发可带）
async function getToken(input) {
  if (input.homeUrl) {
    const t = await callWithRetry('tab.create', { url: input.homeUrl, active: false }, 30000, 2);
    try {
      await sleep(SLEEP_OPEN_MS);
      const r = JSON.parse(await pageEval(t.id, EXTRACT_LOGIN));
      return r.token || '';
    } finally {
      try { await callWithRetry('tab.close', { tabId: t.id }); } catch { }
    }
  }
  try {
    const tabs = await callWithRetry('tab.list', {}, 15000, 2);
    for (const t of tabs || []) {
      const m = String(t.url || '').match(/mp\.weixin\.qq\.com\/cgi-bin[^"']*[?&]token=(\d+)/);
      if (m) return m[1];
    }
  } catch { /* tab.list 失败继续走 3 */ }
  const t = await callWithRetry('tab.create', { url: 'https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN', active: false }, 30000, 2);
  try {
    await sleep(SLEEP_OPEN_MS);
    const r = JSON.parse(await pageEval(t.id, EXTRACT_LOGIN));
    return r.token || '';
  } finally {
    try { await callWithRetry('tab.close', { tabId: t.id }); } catch { }
  }
}

async function runOwn(input) {
  const { count, offset = 0, exportDir } = input;
  mkdirSync(join(exportDir, 'articles'), { recursive: true });
  const { seenUrl, fileCount } = loadExistingKeys(exportDir);
  const seenShort = new Set(seenUrl);
  let seq = fileCount + 1;
  let saved = 0, skipped = 0, failed = 0;
  const reasons = [];
  const articles = [];

  // 1. 拿后台会话 token（复用用户已登录浏览器，零配置）
  const token = await getToken(input);
  if (!token) {
    return {
      status: 'failed',
      reason: '未获取到公众号后台会话：请在浏览器中打开 mp.weixin.qq.com 公众号后台并保持登录（地址栏 URL 带 token），或在 input.json 里填 homeUrl=该后台 URL，然后重试。',
      saved: 0, skipped: 0, failed: 0,
      articles, reasons: ['未登录'],
    };
  }

  // 2. 逐页抓发表记录 → 逐条开短码链接提取正文（串行，控制访问节奏）
  //    offset 直接映射到发表记录分页参数 begin（列表按发布日期倒序，跳过前 offset 篇即增量归档）
  let begin = offset;
  for (let page = 0; page < MAX_PAGES; page++) {
    if (saved >= count) break;
    const listTab = await callWithRetry('tab.create', {
      url: `https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list&begin=${begin}&count=${PAGE_SIZE}&token=${token}&lang=zh_CN`,
      active: false,
    }, 30000, 2);
    try {
      await sleep(SLEEP_OPEN_MS);
      const list = JSON.parse(await pageEval(listTab.id, EXTRACT_OWN_LIST));
      const arts = (list && list.arts) || [];
      if (arts.length === 0) {
        const total = JSON.parse(await pageEval(listTab.id, EXTRACT_OWN_TOTAL));
        if (total.total === 0) reasons.push('发表记录无内容或登录态已失效');
        break;
      }
      for (const art of arts) {
        if (saved >= count) break;
        const code = shortCodeOf(art.shortUrl);
        if (!code) { failed++; articles.push({ title: art.title, url: art.shortUrl || '', status: 'failed-deleted' }); continue; }
        if (seenShort.has(code)) { skipped++; articles.push({ title: art.title, url: art.shortUrl, status: 'skipped' }); continue; }
        const res = await fetchArticle(art.shortUrl);
        await sleep(SLEEP_ITEM_MS);
        if (res.deleted || !res.title || !res.content) {
          failed++;
          articles.push({ title: art.title, url: art.shortUrl, status: 'failed-deleted' });
          continue;
        }
        const date = art.date || '';
        const meta = { title: res.title, author: res.author || '', url: art.shortUrl, date };
        writeMdArticle(exportDir, seq, meta, res.content);
        seenShort.add(code);
        seq++;
        saved++;
        articles.push({ title: res.title, author: meta.author, date, url: art.shortUrl, status: 'ok' });
      }
      if (arts.length < PAGE_SIZE) break;
      begin += PAGE_SIZE;
    } finally {
      try { await callWithRetry('tab.close', { tabId: listTab.id }); } catch { }
    }
  }

  if (saved === 0 && reasons.length === 0) reasons.push('发表记录中未提取到有效文章');
  return buildMeta({ saved, skipped, failed, articles, reasons, status: '', reason: '' }, count);
}

// ---------- 输出 ----------
function writeIndex(exportDir, input, meta) {
  const index = {
    count: input.count,
    offset: input.offset || 0,
    actual: meta.saved || 0,
    status: meta.status,
  };
  if (meta.reason) index.reason = meta.reason;
  index.articles = meta.articles.map(a => ({ title: a.title, url: a.url, status: a.status }));
  writeFileSync(join(exportDir, 'index.json'), JSON.stringify(index, null, 2), 'utf-8');
}

// ---------- 主流程 ----------
async function main() {
  mkdirSync(TMP, { recursive: true });
  let input;
  try {
    const inputFile = process.argv[2];
    if (inputFile) input = JSON.parse(readFileSync(resolve(inputFile), 'utf-8'));
    else input = JSON.parse(readFileSync(join(process.cwd(), 'input.json'), 'utf-8'));
  } catch (e) {
    console.log(JSON.stringify({ status: 'failed', error: `无法读取 input.json：${String(e.message).slice(0, 200)}` }));
    return;
  }

  const count = Number.isFinite(Number(input.count)) ? Math.max(1, Number(input.count)) : 10;
  const offset = Number.isFinite(Number(input.offset)) ? Math.max(0, Number(input.offset)) : 0;
  const exportDir = resolve(input.outputDir || '/tmp/gzh-download-knowledge-output');
  mkdirSync(exportDir, { recursive: true });

  const pipelineOutDir = resolve(input.output_dir || '/tmp/gzh-download-knowledge-output');
  const outputFiles = input.output_files || {};
  const resultFile = join(pipelineOutDir, outputFiles.result || 'res.json');
  const dataFile = join(pipelineOutDir, outputFiles.data || 'data.md');

  try {
    await ensureRelay();
    const params = { count, offset, exportDir, homeUrl: input.homeUrl || '' };
    const meta = await runOwn(params);

    // 功能输出：导出目录下 articles/*.md + index.json
    writeIndex(exportDir, params, meta);

    // 管线输出：res.json（元信息）+ data.md（本次保存清单）
    const summary = buildSummary(count, meta);
    const result = {
      status: meta.status,
      count,
      offset,
      saved: meta.saved || 0,
      skipped: meta.skipped || 0,
      failed: meta.failed || 0,
      ...(meta.reason ? { reason: meta.reason } : {}),
      summary,
      output_dir: exportDir,
    };
    writeFileSync(resultFile, JSON.stringify(result, null, 2));
    writeFileSync(dataFile, buildDataMd(count, meta));

    console.log(JSON.stringify({ status: meta.status, summary, output_dir: exportDir }));
  } catch (e) {
    console.error(e);
    console.log(JSON.stringify({ status: 'failed', error: String(e.message || e), output_dir: exportDir }));
  }
}

function buildSummary(count, meta) {
  const parts = [];
  parts.push(`保存 ${meta.saved}/${count} 篇`);
  if (meta.skipped) parts.push(`去重跳过 ${meta.skipped}`);
  if (meta.failed) parts.push(`失败 ${meta.failed}`);
  if (meta.status === 'partial' || meta.status === 'failed') parts.push(`（${meta.reason}）`);
  return parts.join('，');
}

function buildDataMd(count, meta) {
  const lines = [`# 公众号文章存档`, '',
    `- 请求 count: ${count}`,
    `- 实际保存: ${meta.saved || 0}`,
    `- 状态: ${meta.status}${meta.reason ? '（' + meta.reason + '）' : ''}`,
    ''];
  lines.push('| # | 标题 | url | 状态 |', '|---:|------|-----|------|');
  meta.articles.forEach((a, i) => {
    lines.push(`| ${i + 1} | ${String(a.title || '').replace(/\|/g, '\\|')} | ${a.url || ''} | ${a.status} |`);
  });
  lines.push('');
  return lines.join('\n');
}

main();
