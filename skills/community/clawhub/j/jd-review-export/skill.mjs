#!/usr/bin/env node
/**
 * jd-review-export — 京东商品评价导出
 *
 * 流程（全部通过 Extension Relay HTTP API 操作真实 Chrome，不使用 CDP）：
 *   开任务分组 → 打开商品页 → 探针（登录态 + 页面结构）→ 评价区滚入视口
 *   → 点「全部评价」触发浮层 → 在浮层虚拟列表里边滚边提取（去重累积）→ 导出 → 渲染 Markdown 表格
 *
 * 分工：除「页面状态判别」在拿不准时交给 LLM 子会话外，其余全部为确定性代码。
 * 用法：node skill.mjs <input.json>
 */

import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { spawn } from 'node:child_process';

// ---------------------------------------------------------------------------
// 常量
// ---------------------------------------------------------------------------
const RELAY_URL = 'http://127.0.0.1:3459';
const TMP = join(tmpdir(), 'jd-review-export-' + process.pid);
const WC3_CODE = join(import.meta.dirname, 'wc3-code.mjs');

const DEFAULT_COUNT = 50;          // 入参 count 缺省值
const MIN_REQUIRED = 5;            // 验收底线：至少 5 条
const PROBE_TIMEOUT_MS = 15000;    // 商品页渲染慢（实测约 9s），轮询等到评价区出现
const OVERLAY_TIMEOUT_MS = 15000;  // 点「全部评价」后等浮层出现
const POLL_INTERVAL_MS = 1500;     // 轮询间隔
const SCROLL_INTO_VIEW_MS = 2000;  // 评价区滚入视口后的稳定等待
// 滚动间隔设 2.2s：实测更快的连续滚动会触发页面访问限制，商品页直接返回 403
const SCROLL_INTERVAL_MS = 2200;
const MAX_ROUNDS = 40;             // 安全上限，避免虚拟列表永不"到底"时无限滚动

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// ---------------------------------------------------------------------------
// Extension Relay（HTTP API，端口 3459）
// ---------------------------------------------------------------------------
async function relayCall(op, params = {}, timeout = 30000) {
  const body = { op, params, timeout };
  if (process.env.WC3_OPERATION_LOG) body.logFile = process.env.WC3_OPERATION_LOG;
  const res = await fetch(`${RELAY_URL}/api/call`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  const data = await res.json();
  if (data.error) throw new Error(data.error);
  return data.result;
}

async function ensureRelay() {
  try {
    const status = await (await fetch(`${RELAY_URL}/api/status`)).json();
    if (!status.extensionConnected) throw new Error('浏览器扩展未连接');
  } catch (e) {
    throw new Error(
      `无法连接 Extension Relay（${RELAY_URL}）：${e.message}。` +
        '请确认 Chrome 已打开、浏览器扩展已启用、relay 服务已启动。'
    );
  }
}

/** page.eval 可能返回字符串（JSON.stringify 的结果）或已解析对象，统一处理 */
function parseEval(raw) {
  if (raw == null) return null;
  if (typeof raw === 'object') return raw;
  try {
    return JSON.parse(raw);
  } catch {
    return raw;
  }
}

// ---------------------------------------------------------------------------
// 页面 JS（直接作为字符串传给 page.eval；一律用同步 IIFE——page.eval 不 await Promise）
// ---------------------------------------------------------------------------

// 登录态 + 页面结构探针
const PROBE_JS = `JSON.stringify({
  url: location.href,
  title: document.title,
  pin: (document.cookie.match(/(?:^|;\\s*)(pin|unick|pt_pin)=([^;]*)/) || [])[0] || null,
  hasCommentRoot: !!document.querySelector("#comment-root"),
  hasAllBtn: !!document.querySelector("#comment-root .all-btn"),
  bodyLen: document.body.innerText.length,
  head: document.body.innerText.slice(0, 300)
})`;

// 把评价区滚入视口
const SCROLL_INTO_VIEW_JS = `(function(){
  var el = document.querySelector("#comment-root");
  if (!el) return JSON.stringify({ ok: false, err: "no comment-root" });
  el.scrollIntoView({ block: "center" });
  var r = el.getBoundingClientRect();
  return JSON.stringify({ ok: true, top: Math.round(r.top), height: Math.round(r.height) });
})()`;

// 触发「全部评价」浮层。
// 为什么用完整事件序列 + 直接调 React onClick：只做 el.click() 或单个 dispatchEvent(MouseEvent) 不生效，
// React 的 onClick 挂在 __reactProps 上且按钮有 pointer 事件前置逻辑。
const CLICK_ALL_BTN_JS = `(function(){
  var btn = document.querySelector("#comment-root .all-btn");
  if (!btn) return JSON.stringify({ ok: false, err: "no all-btn" });
  var r = btn.getBoundingClientRect();
  var x = r.left + r.width / 2, y = r.top + r.height / 2;
  var opts = { bubbles: true, cancelable: true, composed: true, clientX: x, clientY: y, view: window, button: 0, buttons: 1 };
  ["pointerdown", "mousedown", "pointerup", "mouseup", "click"].forEach(function (t) {
    var E = t.indexOf("pointer") === 0 ? PointerEvent : MouseEvent;
    btn.dispatchEvent(new E(t, opts));
  });
  var k = Object.keys(btn).find(function (key) { return key.indexOf("__reactProps") === 0; });
  if (k && btn[k] && typeof btn[k].onClick === "function") {
    try {
      btn[k].onClick.call(btn, { preventDefault: function () {}, stopPropagation: function () {}, currentTarget: btn, target: btn });
    } catch (e) {}
  }
  return JSON.stringify({ ok: true, x: Math.round(x), y: Math.round(y), text: (btn.innerText || "").trim() });
})()`;

// 确认浮层与滚动容器出现（哈希 class 后缀随版本变，必须前缀匹配）
const CONFIRM_OVERLAY_JS = `(function(){
  var r = document.querySelector("#rateList");
  var c = document.querySelector('[id="rateList"] [class*="_rateListContainer_"]')
        || document.querySelector('[class*="_rateListContainer_"]');
  return JSON.stringify({
    hasRateList: !!r,
    rateListDisplay: r ? getComputedStyle(r).display : null,
    hasContainer: !!c,
    containerClass: c ? c.className : null,
    containerScrollH: c ? c.scrollHeight : null,
    containerClientH: c ? c.clientHeight : null
  });
})()`;

// 单轮：提取当前渲染的条目 → 去重累积到 window.__jd → 滚到底。
// 为什么必须边滚边收集：浮层是虚拟列表，DOM 只渲染视口附近 3-6 条，历史条目会被回收，
// 滚到底再一次性提取会大量丢数据。
// 注意：必须是同步 IIFE，不能 async/await（page.eval 不 await Promise，会返回 {} 但副作用已发生）。
const SCROLL_COLLECT_JS = `(function(){
  window.__jd = window.__jd || { seen: {}, items: [], lastH: 0, rounds: 0 };
  var S = window.__jd;
  var c = document.querySelector('[id="rateList"] [class*="_rateListContainer_"]');
  if (!c) return JSON.stringify({ err: 'no container', total: S.items.length, url: location.href });
  var items = Array.prototype.slice.call(c.querySelectorAll('[class*="_listItem_"]'));
  var added = 0;
  for (var i = 0; i < items.length; i++) {
    var it = items[i];
    var g = function (s) { var e = it.querySelector(s); return e ? e.innerText.trim() : ''; };
    var nick = g('.jdc-pc-rate-card-nick');
    var tag = g('.jd-content-pc-tag');
    var date = g('.date');
    var sku = g('.info');
    var desc = g('.jdc-pc-rate-card-main-desc');
    var reply = g('.jdc-pc-rate-card-reply span');
    var infos = Array.prototype.slice.call(it.querySelectorAll('.jdc-pc-rate-card-info'));
    var last = infos[infos.length - 1];
    var m = (last ? last.innerText : '').match(/(\\d+)\\s*有用/);
    var useful = m ? m[1] : '';
    if (!nick && !desc) continue;
    var key = nick + '|' + date + '|' + desc.slice(0, 20);
    if (S.seen[key]) continue;
    S.seen[key] = 1;
    S.items.push({ nick: nick, tag: tag, date: date, sku: sku, desc: desc, reply: reply, useful: useful });
    added++;
  }
  var prevH = S.lastH;
  c.scrollTop = c.scrollHeight;
  S.lastH = c.scrollHeight;
  S.rounds++;
  return JSON.stringify({ round: S.rounds, rendered: items.length, added: added, total: S.items.length, prevH: prevH, newH: c.scrollHeight, scrollTop: c.scrollTop });
})()`;

// 一次性导出浏览器内存里累积的全部条目（不经 shell 变量中转大 JSON）
const EXPORT_JS = `JSON.stringify({ total: window.__jd.items.length, items: window.__jd.items })`;

// ---------------------------------------------------------------------------
// 页面状态判别
// ---------------------------------------------------------------------------

/** 已知特征串直接短路，无需消耗 token 调子会话 */
function quickClassify(probe) {
  const url = (probe && probe.url) || '';
  if (/passport\.jd\.com|plogin\.m\.jd\.com|passport\.jd\.hk|login\.jd\.com/.test(url)) return 'need_login';
  if (/reason=403|privatedomain|cfe\.m\.jd\.com|pf\.jd\.com/.test(url)) return 'rate_limited';
  if (probe && probe.hasCommentRoot && probe.hasAllBtn) return 'ok';
  if (!probe || !probe.pin) return 'need_login';
  return 'unknown';
}

const CLASS_HINT = {
  need_login: '当前未登录京东。请在你的 Chrome 中登录京东后重试。',
  rate_limited: '页面返回访问限制（403）。请等待约 10 分钟后再重试。',
  invalid_url: '商品链接无效或商品不存在，请确认链接形如 https://item.jd.com/{sku}.html。',
  other: '页面状态无法确认，请稍后重试。',
};

function normalizeCategory(v) {
  const s = String(v == null ? '' : v).toLowerCase().trim();
  if (!s) return 'other';
  if (/(need_login|login|登录|未登录|passport)/.test(s)) return 'need_login';
  if (/(rate_limited|rate.?limit|restricted|403)/.test(s)) return 'rate_limited';
  if (/(invalid_url|invalid|不存在|无效|404)/.test(s)) return 'invalid_url';
  if (/(^|[^a-z])ok([^a-z]|$)/.test(s) || /正常/.test(s)) return 'ok';
  return 'other';
}

// LLM 子会话返回值不可靠：递归解析 + 归一化，解析不出就返回 null（绝不编造结论）
function extractJson(raw) {
  if (raw == null) return null;
  if (typeof raw === 'object') {
    if (typeof raw.result === 'string') {
      const inner = extractJson(raw.result);
      if (inner != null) return inner;
    }
    return raw;
  }
  if (typeof raw !== 'string') return null;
  const s = raw.trim();
  try {
    return JSON.parse(s);
  } catch {}
  const fence = s.match(/```(?:json)?\s*([\s\S]*?)```/i);
  if (fence) {
    try {
      return JSON.parse(fence[1].trim());
    } catch {}
  }
  const first = s.match(/[{[][\s\S]*[}\]]/);
  if (first) {
    try {
      return JSON.parse(first[0]);
    } catch {}
  }
  return null;
}

/**
 * 页面状态语义判别（唯一需要"理解"的步骤）。
 * 只在 quickClassify 无法断定（'unknown'）或浮层拿不到时调用。
 */
async function llmClassify(probe, anomaly) {
  mkdirSync(TMP, { recursive: true });
  const prompt = `你是网页状态判别助手。下面是一个京东商品页的探针结果（JSON），请判断当前页面处于哪种状态，并给出一句给最终用户看的中文提示。

探针结果：
\`\`\`json
${JSON.stringify(probe, null, 2)}
\`\`\`
${anomaly ? '采集过程中的异常：' + anomaly : ''}

分类枚举（只能选一个）：
- ok：页面正常，评价区存在
- need_login：未登录或被登录墙拦截（跳转 passport / cookie 无 pin）
- rate_limited：页面返回访问限制（403 / 站点限流页）
- invalid_url：商品不存在或链接无效
- other：其它情况（如商品确实没有评价、页面结构变化）

只输出一个 JSON 对象，不要任何解释文字：
{"category":"<枚举>","hint":"<一句中文提示，给最终用户看>"}`;

  const outFile = join(TMP, 'classify-' + Date.now() + '.json');
  try {
    const raw = await callClaude(prompt, outFile, { timeout: 180 });
    const obj = extractJson(raw);
    if (!obj || typeof obj !== 'object') return null;
    const category = normalizeCategory(obj.category || obj.status || obj.result);
    const hint = String(obj.hint || obj.message || obj.summary || '').trim();
    return { category, hint: hint || CLASS_HINT[category] || CLASS_HINT.other };
  } catch (e) {
    process.stderr.write('LLM 状态判别失败: ' + e.message + '\n');
    return null; // 不编造结论，交由调用方按 other 如实上报
  }
}

// ---------------------------------------------------------------------------
// LLM 子会话封装（照抄参考实现，不自己 spawn Code CLI 以外的逻辑）
// ---------------------------------------------------------------------------
function callClaude(prompt, outputFile, opts = {}) {
  return new Promise((resolve, reject) => {
    const args = ['--prompt', prompt, '--output', outputFile];
    if (opts.timeout) args.push('--timeout', String(opts.timeout));
    if (opts.schema) args.push('--schema', opts.schema);
    if (opts.resume) args.push('--resume', opts.resume);
    const child = spawn('node', [WC3_CODE, ...args], { stdio: ['ignore', 'ignore', 'pipe'] });
    let stderr = '';
    child.stderr.on('data', (d) => {
      stderr += d;
    });
    child.on('close', (code) => {
      if (code !== 0) return reject(new Error(`wc3-code exit ${code}: ${stderr.slice(0, 500)}`));
      try {
        resolve(JSON.parse(readFileSync(outputFile, 'utf-8')));
      } catch {
        resolve(readFileSync(outputFile, 'utf-8'));
      }
    });
    child.on('error', reject);
  });
}

// ---------------------------------------------------------------------------
// Markdown 渲染
// ---------------------------------------------------------------------------
function esc(v) {
  return String(v == null ? '' : v)
    .replace(/\r?\n/g, '<br>')
    .replace(/\|/g, '\\|')
    .trim();
}

function renderMarkdown({ productUrl, sku, title, count, items, partial, reason }) {
  const lines = [];
  if (partial) lines.push('<!-- partial -->');
  lines.push('# 京东商品评价导出');
  lines.push('');
  lines.push('- 商品链接：' + productUrl);
  lines.push('- SKU：' + (sku || '未知'));
  lines.push('- 商品标题：' + (title || '（未获取）'));
  lines.push('- 采集条数：' + items.length + '（上限 ' + count + '）');
  if (partial) lines.push('- 说明：' + reason);
  lines.push('');
  lines.push('| 序号 | 用户名 | 购买标签 | 日期 | SKU | 正文 | 商家回复 | 有用数 |');
  lines.push('|---|---|---|---|---|---|---|---|');
  items.forEach((r, i) => {
    lines.push(
      '| ' + (i + 1) + ' | ' + esc(r.nick) + ' | ' + esc(r.tag) + ' | ' + esc(r.date) + ' | ' +
        esc(r.sku) + ' | ' + esc(r.desc) + ' | ' + esc(r.reply) + ' | ' + esc(r.useful) + ' |'
    );
  });
  lines.push('');
  return lines.join('\n');
}

function renderFailure(productUrl, sku, reason, hint) {
  const lines = ['<!-- partial -->', '# 京东商品评价导出', ''];
  lines.push('- 商品链接：' + productUrl);
  lines.push('- SKU：' + (sku || '未知'));
  lines.push('- 采集条数：0');
  lines.push('- 说明：' + reason);
  if (hint) lines.push('- 处理建议：' + hint);
  lines.push('');
  return lines.join('\n');
}

// ---------------------------------------------------------------------------
// 主流程
// ---------------------------------------------------------------------------
async function main() {
  const inputPath = process.argv[2];
  if (!inputPath) throw new Error('用法: node skill.mjs <input.json>');
  const input = JSON.parse(readFileSync(inputPath, 'utf-8'));

  const productUrl = String(input.productUrl || input.product_url || '').trim();
  const rawCount = Number(input.count);
  const count = Number.isFinite(rawCount) && rawCount > 0 ? Math.floor(rawCount) : DEFAULT_COUNT;
  const outputDir = input.output_dir || input.outputDir || '/tmp/jd-review-export-output';
  const outputFiles = input.output_files || {};
  const resultFile = join(outputDir, outputFiles.result || 'res.json');
  const dataFile = join(outputDir, outputFiles.data || 'data.md');
  const reviewsFile = join(outputDir, 'reviews.md');

  mkdirSync(outputDir, { recursive: true });
  mkdirSync(TMP, { recursive: true });

  let parsedUrl = null;
  try {
    parsedUrl = new URL(productUrl);
  } catch {
    parsedUrl = null;
  }
  const sku = parsedUrl ? (parsedUrl.pathname.match(/(\d{5,})/) || [])[1] || null : null;
  const hostOk = parsedUrl && /(^|\.)jd\.com$/i.test(parsedUrl.hostname);

  let title = '';
  let groupId = null;

  function writeOutputs(status, summary, markdown, extra = {}) {
    const result = {
      status,
      task: '导出京东商品评价为本地 Markdown 表格',
      product_url: productUrl,
      sku: sku || null,
      requested: count,
      total: extra.total != null ? extra.total : 0,
      stop_reason: extra.stopReason || null,
      data_file: 'reviews.md',
      summary,
      ...(extra.error ? { error: extra.error } : {}),
      ...(extra.hint ? { hint: extra.hint } : {}),
      ...(extra.skipped ? { skipped_incomplete: extra.skipped } : {}),
      timestamp: new Date().toISOString(),
    };
    writeFileSync(resultFile, JSON.stringify(result, null, 2));
    writeFileSync(dataFile, markdown);
    writeFileSync(reviewsFile, markdown);
    console.log(JSON.stringify({ status, summary, output_dir: outputDir }));
  }

  try {
    if (!parsedUrl || !hostOk || !sku) {
      const reason = '商品链接无效：' + (productUrl || '(空)');
      writeOutputs('failed', reason, renderFailure(productUrl, sku, reason, CLASS_HINT.invalid_url), {
        error: 'invalid_url',
        hint: CLASS_HINT.invalid_url,
      });
      return;
    }

    await ensureRelay();
    groupId = (await relayCall('group.create', { name: 'jd-review-export' })).groupId;

    const tab = await relayCall('tab.create', { url: productUrl, active: true, groupId });
    const tabId = tab.id;

    // 1) 等商品页渲染出评价区。为什么轮询而不是固定 sleep：京东渲染耗时随网络波动，
    //    固定 9s 在慢网下会拿不到 #comment-root。
    let probe = null;
    {
      const deadline = Date.now() + PROBE_TIMEOUT_MS;
      while (Date.now() < deadline) {
        probe = parseEval(await relayCall('page.eval', { tabId, groupId, code: PROBE_JS })) || {};
        if (probe.hasCommentRoot || /passport\.jd\.com|reason=403/.test(probe.url || '')) break;
        await sleep(POLL_INTERVAL_MS);
      }
    }
    title = (probe && probe.title) || '';

    // 2) 登录态 / 页面状态 / 无效链接判定（已知特征串代码短路；拿不准才交 LLM 子会话）
    let cls = quickClassify(probe);
    if (cls === 'unknown') {
      const judged = await llmClassify(probe, null);
      cls = judged ? judged.category : 'other';
      if (judged && judged.hint) process.stderr.write('状态判别: ' + cls + ' / ' + judged.hint + '\n');
    }
    if (cls !== 'ok') {
      const reason = '未能进入评价浮层（状态：' + cls + '）';
      const hint = CLASS_HINT[cls] || CLASS_HINT.other;
      writeOutputs('failed', reason + '。' + hint, renderFailure(productUrl, sku, reason, hint), {
        error: cls,
        hint,
      });
      return;
    }

    // 3) 评价区滚入视口 → 触发「全部评价」浮层
    await relayCall('page.eval', { tabId, groupId, code: SCROLL_INTO_VIEW_JS });
    await sleep(SCROLL_INTO_VIEW_MS);
    const clicked = parseEval(await relayCall('page.eval', { tabId, groupId, code: CLICK_ALL_BTN_JS })) || {};
    if (!clicked.ok) {
      const reason = '未找到「全部评价」按钮（' + (clicked.err || 'unknown') + '）';
      const hint = '页面结构可能已变化，或商品评价区未加载，请稍后重试。';
      writeOutputs('failed', reason, renderFailure(productUrl, sku, reason, hint), { error: 'no_all_btn', hint });
      return;
    }
    process.stderr.write('已点击「全部评价」: ' + JSON.stringify(clicked) + '\n');

    // 4) 等浮层与滚动容器出现
    let overlay = null;
    {
      const deadline = Date.now() + OVERLAY_TIMEOUT_MS;
      while (Date.now() < deadline) {
        overlay = parseEval(await relayCall('page.eval', { tabId, groupId, code: CONFIRM_OVERLAY_JS })) || {};
        if (overlay.hasRateList && overlay.hasContainer) break;
        await sleep(POLL_INTERVAL_MS);
      }
    }

    if (!overlay || !overlay.hasContainer) {
      // 拿不准是登录墙、访问限制还是商品无评价 → 交子会话判别
      const judged = await llmClassify(probe, '点击「全部评价」后未找到 #rateList 滚动容器');
      const cls2 = judged ? judged.category : 'other';
      const hint = (judged && judged.hint) || CLASS_HINT[cls2] || CLASS_HINT.other;
      const reason = '未能打开评价列表浮层（状态：' + cls2 + '）';
      writeOutputs('failed', reason + '。' + hint, renderFailure(productUrl, sku, reason, hint), {
        error: cls2,
        hint,
      });
      return;
    }

    // 5) 边滚边收集（虚拟列表：历史条目会被回收，必须每轮提取去重）
    let stopReason = 'bottom';
    let collectErr = null;
    let total = 0;
    for (let round = 0; round < MAX_ROUNDS; round++) {
      const stat = parseEval(await relayCall('page.eval', { tabId, groupId, code: SCROLL_COLLECT_JS })) || {};
      if (stat.err) {
        collectErr = stat.err;
        stopReason = 'no_container';
        break;
      }
      total = stat.total || 0;
      process.stderr.write(
        `round ${stat.round}: rendered=${stat.rendered} added=${stat.added} total=${stat.total} h=${stat.prevH}->${stat.newH}\n`
      );
      if (total >= count) {
        stopReason = 'count_reached';
        break;
      }
      if (stat.added === 0 && stat.newH === stat.prevH) {
        stopReason = 'bottom';
        break;
      }
      if (round === MAX_ROUNDS - 1) stopReason = 'max_rounds';
      await sleep(SCROLL_INTERVAL_MS);
    }

    // 6) 一次性导出累积数据
    const exported = parseEval(await relayCall('page.eval', { tabId, groupId, code: EXPORT_JS })) || {};
    const all = Array.isArray(exported.items) ? exported.items : [];

    // 只保留 用户名/日期/SKU/正文 四项齐全的条目（Accept 要求这四项非空）
    const complete = all.filter((r) => r && r.nick && r.date && r.sku && r.desc);
    const skipped = all.length - complete.length;
    const items = complete.slice(0, count);

    if (items.length === 0) {
      const reason =
        '未采集到任何评价' +
        (collectErr ? '（滚动容器丢失：' + collectErr + '）' : '') +
        (stopReason === 'no_container' ? '，可能页面受限或未登录' : '');
      const hint = stopReason === 'no_container' ? CLASS_HINT.rate_limited : CLASS_HINT.other;
      writeOutputs('failed', reason, renderFailure(productUrl, sku, reason, hint), {
        error: stopReason === 'no_container' ? 'rate_limited' : 'no_reviews',
        hint,
        stopReason,
        skipped,
      });
      return;
    }

    const requiredMin = Math.min(MIN_REQUIRED, count);
    const partial = items.length < requiredMin;
    let reason = '';
    if (partial) {
      if (stopReason === 'bottom') reason = '商品评价总量不足，已到底，仅采集到 ' + items.length + ' 条';
      else if (stopReason === 'max_rounds') reason = '达到最大滚动轮次上限，仅采集到 ' + items.length + ' 条';
      else if (stopReason === 'no_container') reason = '滚动中断，仅采集到 ' + items.length + ' 条';
      else reason = '仅采集到 ' + items.length + ' 条';
    }

    const markdown = renderMarkdown({ productUrl, sku, title, count, items, partial, reason });
    const status = partial ? 'partial' : 'success';
    const summary =
      `已从京东商品页「全部评价」浮层采集 ${items.length} 条评价（上限 ${count}，停止原因 ${stopReason}）` +
      (skipped ? `，跳过字段不全 ${skipped} 条` : '') +
      (partial ? '；未达验收底线，已标注 partial：' + reason : '');
    writeOutputs(status, summary, markdown, { total: items.length, stopReason, skipped });
  } catch (e) {
    const reason = '执行失败：' + (e && e.message ? e.message : String(e));
    writeOutputs('failed', reason, renderFailure(productUrl, sku, reason, CLASS_HINT.other), {
      error: 'exception',
    });
  } finally {
    if (groupId) {
      try {
        await relayCall('group.close', { groupId });
      } catch (e) {
        process.stderr.write('关闭任务分组失败: ' + e.message + '\n');
      }
    }
  }
}

main().catch((e) => {
  // 兜底：任何未捕获异常都不能让进程带栈崩溃
  try {
    console.log(JSON.stringify({ status: 'failed', summary: String((e && e.message) || e), output_dir: process.cwd() }));
  } catch {}
  process.exit(0);
});
