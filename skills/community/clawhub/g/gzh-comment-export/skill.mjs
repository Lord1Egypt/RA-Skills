#!/usr/bin/env node
/**
 * gzh-comment-export —— 公众号留言导出（只读）
 *
 * 流程：
 *   1. 打开已登录的公众号后台首页 → 从 location.href 动态提取 token
 *   2. 用 token 拼「互动管理 → 留言」管理页 URL 并打开
 *   3. 左栏 .comment-article-list 按文章分组，逐篇点击切换右栏
 *   4. 右栏提取留言（作者/内容/时间/地区），右栏若自身分页则一并翻到底
 *   5. 文章列表翻页（.weui-desktop-pagination 的「下一页」）到底
 *   6. 写 <outputDir>/comments.md（按文章分组）+ <outputDir>/index.json（统计）
 *
 * 只读边界（硬性）：
 *   全程只做两类操作——「左栏文章切换」和「分页点击」。条目内的
 *   屏蔽 / 删除 / 置顶 / 加入黑名单 / 回复 / 写留言输入框一律不碰。
 *
 * 浏览器通道：Extension Relay HTTP API（127.0.0.1:3459），无 CDP 依赖。
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { join, resolve, basename } from 'node:path';

// ── 浏览器通道 ──────────────────────────────────────────────────────
const RELAY_URL = 'http://127.0.0.1:3459';

// ── 目标页面（token 动态注入，绝不写死）─────────────────────────────
const HOME_URL = 'https://mp.weixin.qq.com/';
const COMMENT_PAGE_BASE = 'https://mp.weixin.qq.com/misc/appmsgcomment';
const COMMENT_PAGE_QUERY = 'action=list_latest_comment&begin=0&count=10&sendtype=MASSSEND&scene=1&lang=zh_CN';

// ── 时序（取自探索实测的成功记录）───────────────────────────────────
const PAGE_LOAD_WAIT_MS = 6000;        // tab.create 打开页面后的基础等待
const ARTICLE_MIN_WAIT_MS = 2500;      // 点击某篇文章后的基础等待（同时满足「每篇间隔 ≥2s」）
const ARTICLE_EXTRA_WAIT_MS = 5000;    // 右栏未就绪时的额外轮询上限
const LIST_PAGE_WAIT_MS = 3000;        // 文章列表翻页后的基础等待
const LIST_PAGE_EXTRA_WAIT_MS = 8000;  // 文章列表翻页后的额外轮询上限
const COMMENT_PAGE_WAIT_MS = 3000;     // 右栏留言分页后的等待
const POLL_INTERVAL_MS = 700;
const TOKEN_WAIT_MS = 20000;           // 等后台首页出 token 的上限（覆盖慢加载）

// ── 循环上限 / 失败容忍 ─────────────────────────────────────────────
const MAX_ARTICLE_PAGES = 50;          // 文章列表翻页上限，防「下一页」判定失灵时死循环
const MAX_COMMENT_PAGES = 50;          // 单篇留言分页上限
const MAX_CONSECUTIVE_FAILURES = 3;    // 连续失败这么多篇就停，不硬刚
const RELAY_RETRY_ATTEMPTS = 5;        // 微信系页面跳转常报 Extension disconnected，需有限重试
const RELAY_RETRY_INTERVAL_MS = 3000;

// ── 运行时引导文案（失败现场直接给可执行指引）───────────────────────
const CHANNEL_LAYER1 =
  '需要浏览器自动化通道（复用你已登录的 Chrome 才能进公众号后台），但本地 relay 未响应（' + RELAY_URL + '）。' +
  '请先安装该浏览器通道（Chrome 扩展 wc3-chrome + 本地 relay 服务，一条命令装好，见其仓库 README），' +
  '装好后运行其 doctor 自检脚本，或直接 `curl -s ' + RELAY_URL + '/api/status` 确认通道已起。装好告诉我继续。';

const CHANNEL_LAYER2 =
  '浏览器通道 relay 已就绪，但浏览器侧没连上：' +
  '① 确认 Chrome 扩展 wc3-chrome 已启用（chrome://extensions）；' +
  '② 在 Chrome 里登录 mp.weixin.qq.com 公众号后台；' +
  '③ 重跑通道 doctor 自检看 advice。都好了告诉我继续。';

const NOT_LOGGED_IN =
  '已打开公众号后台但读不到登录 token —— 通常是登录态失效。' +
  '请在 Chrome 里登录 mp.weixin.qq.com 公众号后台（确认后台首页能正常打开），然后重跑本 skill。';

// ════════════════════════════════════════════════════════════════════
// 页面内执行的 JS（抽成顶部常量，直接当字符串传给 page.eval）
// 注意：这里的 \\d / \\( 在 Node 模板字符串里会还原成页面侧的 \d / \(
// ════════════════════════════════════════════════════════════════════

/** 左栏文章列表：标题 / 发表时间 / 留言数（「N条」） */
const ARTICLE_LIST_JS = `(() => {
  const items = Array.from(document.querySelectorAll('.comment-article-list .article-list__item'));
  return JSON.stringify(items.map(it => ({
    title: it.querySelector('.article-list__item-title')?.textContent?.trim() || '',
    time: it.querySelector('.article-list__item-time')?.textContent?.trim() || '',
    count: it.querySelector('.article-list__item-total-count')?.textContent?.trim() || '',
  })));
})()`;

/** 点击左栏第 index 篇文章（读操作：只切换右栏） */
function clickArticleJs(index) {
  return `(() => {
  const items = document.querySelectorAll('.comment-article-list .article-list__item');
  if (!items[${index}]) return JSON.stringify({ ok: false, reason: 'no item ${index}' });
  items[${index}].click();
  return JSON.stringify({ ok: true });
})()`;
}

/** 右栏就绪状态：当前选中项下标 + 表头「全部留言(N条)」 */
const PANEL_STATE_JS = `(() => {
  const items = Array.from(document.querySelectorAll('.comment-article-list .article-list__item'));
  const cur = items.findIndex(it => it.classList.contains('article-list__item-current'));
  const wrp = document.querySelector('.comment-list-wrp');
  const m = wrp ? wrp.innerText.match(/全部留言\\((\\d+)条\\)/) : null;
  return JSON.stringify({ current: cur, headerCount: m ? Number(m[1]) : null });
})()`;

/**
 * 右栏留言提取。
 * 陷阱①：.comment-list 内有一个隐藏的 reply-dialog 克隆节点，带相同的
 *        data-commentid，不过滤会把同一条留言数成两条（表头 1 条却提到 2 条）。
 *        故必须排除 .reply-dialog 且只取可见节点。
 * 陷阱②：屏蔽占位是 .comment-text_shield，需排除。
 * 陷阱③：微信表情 img 无 alt/title、src 是 blank.gif，textContent 会丢，用 [表情] 占位。
 */
const COMMENTS_JS = `(() => {
  const items = Array.from(document.querySelectorAll('.comment-list .comment-list__item[data-commentid]'))
    .filter(it => !it.closest('.reply-dialog') && it.offsetParent !== null);
  const comments = items.map(it => {
    const nick = it.querySelector('.comment-nickname')?.textContent?.trim() || '';
    const textEl = it.querySelector('.comment-text:not(.comment-text_shield)');
    let content = '';
    if (textEl) {
      content = Array.from(textEl.childNodes).map(n => {
        if (n.nodeType === 3) return n.textContent;
        if (n.nodeName === 'IMG') return n.getAttribute('alt') || n.getAttribute('title') || '[表情]';
        return n.textContent || '';
      }).join('').trim();
    }
    const tEl = it.querySelector('.comment-list__item-time');
    const raw = tEl ? tEl.textContent.trim() : '';
    const m = raw.match(/^(\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2})\\s*(.*)$/);
    return {
      author: nick,
      content,
      time: m ? m[1] : raw,
      region: m ? m[2].trim() : '',
      commentid: it.getAttribute('data-commentid') || '',
    };
  });
  const wrp = document.querySelector('.comment-list-wrp');
  const hdr = wrp ? wrp.innerText.match(/全部留言\\((\\d+)条\\)/) : null;
  return JSON.stringify({ headerCount: hdr ? Number(hdr[1]) : null, comments });
})()`;

/**
 * 文章列表分页信息。
 * 左栏文章列表有独立分页（实测「1 / 2 下一页 跳转」，每页 10 篇）。
 * 用 inCommentPanel 把右栏留言分页排除掉——热门文章的右栏也会有分页，
 * 不区分就会点错按钮，导致文章列表永远停在第一页。
 */
const PAGINATION_JS = `(() => {
  const inCommentPanel = e => !!(e.closest('.comment-list-wrp') || e.closest('.comment-list'));
  const pgs = Array.from(document.querySelectorAll('.weui-desktop-pagination')).filter(p => !inCommentPanel(p));
  const txt = pgs.length ? pgs[0].innerText.replace(/\\n/g, ' ') : '';
  const m = txt.match(/(\\d+)\\s*\\/\\s*(\\d+)/);
  return JSON.stringify({ text: txt, current: m ? Number(m[1]) : null, total: m ? Number(m[2]) : null });
})()`;

/** 文章列表的「下一页」——限定在右栏留言面板之外 */
const NEXT_ARTICLE_JS = `(() => {
  const inCommentPanel = e => !!(e.closest('.comment-list-wrp') || e.closest('.comment-list'));
  const cands = Array.from(document.querySelectorAll('a,button'))
    .filter(e => e.textContent.trim() === '下一页' && !inCommentPanel(e));
  if (cands.length === 0) return JSON.stringify({ clicked: false, reason: 'no next' });
  const next = cands.find(e => !(e.classList.contains('weui-desktop-btn_disabled') || e.hasAttribute('disabled') || e.offsetParent === null));
  if (!next) return JSON.stringify({ clicked: false, reason: 'disabled' });
  next.click();
  return JSON.stringify({ clicked: true });
})()`;

/** 右栏留言列表自身的「下一页」——限定在右栏面板之内；没有就返回 false，绝不越界点左栏分页 */
const NEXT_COMMENT_JS = `(() => {
  const inCommentPanel = e => !!(e.closest('.comment-list-wrp') || e.closest('.comment-list'));
  const cands = Array.from(document.querySelectorAll('a,button'))
    .filter(e => e.textContent.trim() === '下一页' && inCommentPanel(e));
  if (cands.length === 0) return JSON.stringify({ clicked: false, reason: 'no next' });
  const next = cands.find(e => !(e.classList.contains('weui-desktop-btn_disabled') || e.hasAttribute('disabled') || e.offsetParent === null));
  if (!next) return JSON.stringify({ clicked: false, reason: 'disabled' });
  next.click();
  return JSON.stringify({ clicked: true });
})()`;

/**
 * 账号昵称——可选元信息，取不到就留空，不臆造。
 * 注意后台首页的类名是站点自身的拼写错误 `.acount_box-nickname`（少个 c），
 * 不是 account；后面的 weui 选择器只作跨版本兜底。
 */
const ACCOUNT_JS = `(() => {
  const el = document.querySelector('.acount_box-nickname')
    || document.querySelector('.weui-desktop-account__nickname')
    || document.querySelector('.weui-desktop-account__info-nickname');
  return JSON.stringify({ account: el ? el.textContent.trim() : '' });
})()`;

// ════════════════════════════════════════════════════════════════════
// 基础设施
// ════════════════════════════════════════════════════════════════════

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

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

function isTransientRelayError(err) {
  return /Extension disconnected|extensionConnected|not connected|fetch failed|ECONNREFUSED|socket hang up|network/i
    .test(String(err?.message || err));
}

/** 等扩展重连（微信系页面跳转时扩展会瞬时断开，几秒后自愈） */
async function waitForExtension(maxMs) {
  const deadline = Date.now() + maxMs;
  while (Date.now() < deadline) {
    try {
      const st = await (await fetch(`${RELAY_URL}/api/status`)).json();
      if (st && st.extensionConnected) return true;
    } catch { /* relay 未起，继续等 */ }
    await sleep(500);
  }
  return false;
}

/** 所有浏览器 op 的统一入口：瞬时错误有限重试 */
async function call(op, params = {}, timeout = 30000) {
  let lastErr;
  for (let attempt = 1; attempt <= RELAY_RETRY_ATTEMPTS; attempt++) {
    try {
      return await relayCall(op, params, timeout);
    } catch (err) {
      lastErr = err;
      if (!isTransientRelayError(err) || attempt === RELAY_RETRY_ATTEMPTS) throw err;
      process.stderr.write(`[warn] relay op ${op} 失败（${err.message}），重试 ${attempt}/${RELAY_RETRY_ATTEMPTS}\n`);
      await sleep(RELAY_RETRY_INTERVAL_MS);
      await waitForExtension(RELAY_RETRY_INTERVAL_MS);
    }
  }
  throw lastErr;
}

/** 启动自检：区分「没装 / 没启动」与「装了没配置」两层引导 */
async function ensureRelay() {
  let status = null;
  try {
    status = await (await fetch(`${RELAY_URL}/api/status`)).json();
  } catch {
    throw new Error(CHANNEL_LAYER1);
  }
  if (!status || !status.extensionConnected) {
    const ok = await waitForExtension(8000);
    if (!ok) throw new Error(CHANNEL_LAYER2);
  }
}

function evalJson(tabId, code, groupId) {
  return call('page.eval', { tabId, code, groupId }).then((r) => JSON.parse(r));
}

// ════════════════════════════════════════════════════════════════════
// 页面读取
// ════════════════════════════════════════════════════════════════════

async function readArticleList(tabId, groupId) {
  try {
    const raw = await call('page.eval', { tabId, code: ARTICLE_LIST_JS, groupId });
    const arr = JSON.parse(raw);
    return Array.isArray(arr) ? arr : [];
  } catch {
    return [];
  }
}

async function readPagination(tabId, groupId) {
  try {
    return await evalJson(tabId, PAGINATION_JS, groupId);
  } catch {
    return { text: '', current: null, total: null };
  }
}

async function readPanelState(tabId, groupId) {
  try {
    return await evalJson(tabId, PANEL_STATE_JS, groupId);
  } catch {
    return { current: -1, headerCount: null };
  }
}

/** 「1条」→ 1；解析不出来返回 null（不猜） */
function parseCount(text) {
  const m = String(text || '').match(/(\d+)/);
  return m ? Number(m[1]) : null;
}

/** 等左栏文章列表渲染出来 */
async function waitForArticleList(tabId, groupId, timeoutMs) {
  const deadline = Date.now() + timeoutMs;
  let list = await readArticleList(tabId, groupId);
  while (list.length === 0 && Date.now() < deadline) {
    await sleep(POLL_INTERVAL_MS);
    list = await readArticleList(tabId, groupId);
  }
  return list;
}

/**
 * 点完某篇文章后等右栏刷新。
 * 用表头「全部留言(N条)」与左栏该篇的「N条」交叉校验——实测 0 条与 1 条
 * 的文章表头都存在（0 条时 headerCount=0），所以这个信号对两种情形都可靠。
 */
async function waitForArticleLoaded(tabId, groupId, index, expectedCount) {
  await sleep(ARTICLE_MIN_WAIT_MS);
  const deadline = Date.now() + ARTICLE_EXTRA_WAIT_MS;
  let st = await readPanelState(tabId, groupId);
  while (Date.now() < deadline) {
    if (expectedCount !== null && st.headerCount === expectedCount) return st;
    if (expectedCount === null && st.current === index) return st;
    await sleep(POLL_INTERVAL_MS);
    st = await readPanelState(tabId, groupId);
  }
  return st;
}

/** 提取当前文章的留言；右栏若自身分页则翻到底，按 commentid 去重累加 */
async function extractArticleComments(tabId, groupId, articleTitle) {
  const collected = [];
  const seen = new Set();
  let page = 0;

  while (page < MAX_COMMENT_PAGES) {
    const res = await evalJson(tabId, COMMENTS_JS, groupId);
    let added = 0;
    for (const c of res.comments || []) {
      const key = c.commentid || `${c.author}\u0000${c.time}\u0000${c.content}`;
      if (seen.has(key)) continue;
      seen.add(key);
      collected.push({
        author: c.author || '',
        content: c.content || '',
        time: c.time || '',
        region: c.region || '',
        article: articleTitle,
      });
      added++;
    }

    const next = await evalJson(tabId, NEXT_COMMENT_JS, groupId);
    if (!next.clicked) break;
    await sleep(COMMENT_PAGE_WAIT_MS);
    // 点了「下一页」但没有新增 → 面板没变，停下，避免空转
    if (added === 0) break;
    page++;
  }

  return collected;
}

/**
 * 翻文章列表到下一页，并等到列表真的换页。
 * 两个独立信号取「或」：分页「当前页」变化、或左栏首篇标题变化。
 * 只用其中一个都可能误判——分页文本解析失败时只能靠标题，而两页首篇
 * 标题理论上不会相同（每篇文章只出现一次），所以标题信号同样可靠。
 * 必须确认换页才继续，否则会把同一页的 10 篇重复采集一遍。
 */
async function goToNextArticlePage(tabId, groupId, prevCurrent, prevFirstTitle) {
  const next = await evalJson(tabId, NEXT_ARTICLE_JS, groupId);
  if (!next.clicked) return { advanced: false, reason: next.reason || 'no next' };

  await sleep(LIST_PAGE_WAIT_MS);
  const deadline = Date.now() + LIST_PAGE_EXTRA_WAIT_MS;
  let last = null;
  while (Date.now() < deadline) {
    const pagination = await readPagination(tabId, groupId);
    const list = await readArticleList(tabId, groupId);
    last = { pagination, list };

    const pageChanged = prevCurrent !== null && pagination.current !== null && pagination.current !== prevCurrent;
    const listChanged = list.length > 0 && prevFirstTitle !== null && list[0].title !== prevFirstTitle;
    if (pageChanged || listChanged) return { advanced: true, pagination, list };

    await sleep(POLL_INTERVAL_MS);
  }
  return { advanced: false, reason: 'page not changed', ...(last || {}) };
}

// ════════════════════════════════════════════════════════════════════
// 入参 / 输出
// ════════════════════════════════════════════════════════════════════

function readInput() {
  const arg = process.argv[2];
  if (arg && existsSync(arg)) return JSON.parse(readFileSync(arg, 'utf-8'));
  if (arg && arg.trim().startsWith('{')) return JSON.parse(arg);
  if (process.env.SKILL_INPUT_JSON) return JSON.parse(process.env.SKILL_INPUT_JSON);
  return {};
}

function nowStamp() {
  const d = new Date();
  const p = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}:${p(d.getSeconds())}`;
}

/** 表格单元格里转义竖线，避免 markdown 表格被留言内容里的 | 撑破 */
function cell(text) {
  return String(text ?? '').replace(/\|/g, '\\|').replace(/\r?\n/g, ' ');
}

function renderMarkdown({ account, exportTime, articles, totalComments, partial, partialReason }) {
  const lines = [];
  lines.push('# 公众号留言导出');
  lines.push('');
  if (account) lines.push(`> 账号：${account}`);
  lines.push(`> 导出时间：${exportTime}`);
  lines.push('> 数据来源：公众号后台「互动管理 → 留言」（只读）');
  lines.push(`> 文章总数：${articles.length}　留言总数：${totalComments}`);
  if (partial) lines.push(`> 数据完整性：部分（${partialReason || '见 index.json'}）`);
  lines.push('');
  lines.push('---');
  lines.push('');

  for (const a of articles) {
    lines.push(`## ${a.title || '（标题缺失）'}`);
    lines.push('');
    lines.push(`- 发表时间：${a.articleTime || '（页面未提供）'}`);
    lines.push(`- 留言数：${a.comments.length}`);
    if (a.error) lines.push(`- 读取状态：失败（${a.error}）`);
    lines.push('');

    if (a.comments.length === 0) {
      lines.push(a.error ? '（本篇读取失败，未取到留言）' : '（暂无留言）');
      lines.push('');
      continue;
    }

    lines.push('| 作者 | 留言内容 | 留言时间 | 地区 |');
    lines.push('| --- | --- | --- | --- |');
    for (const c of a.comments) {
      lines.push(`| ${cell(c.author)} | ${cell(c.content)} | ${cell(c.time)} | ${cell(c.region)} |`);
    }
    lines.push('');
  }

  return lines.join('\n');
}

// ════════════════════════════════════════════════════════════════════
// 主流程
// ════════════════════════════════════════════════════════════════════

async function main() {
  const input = readInput();
  const outputDir = resolve(input.output_dir || input.outputDir || join(process.cwd(), 'gzh-comment-export'));
  const outputFiles = input.output_files || {};
  const dataFile = join(outputDir, outputFiles.data || 'comments.md');
  const indexFile = join(outputDir, outputFiles.result || 'index.json');
  mkdirSync(outputDir, { recursive: true });

  await ensureRelay();

  const { groupId } = await call('group.create', { name: 'gzh-comment-export' });
  await call('group.setStatus', { groupId, status: 'running' }).catch(() => {});

  let articles = [];
  let failures = [];
  let stopReason = 'end';
  let account = '';
  let listTotal = null;
  let pageCount = null;

  try {
    // ── 1. 打开后台首页，动态提取 token ─────────────────────────────
    const homeTab = await call('tab.create', { url: HOME_URL, active: false, groupId });
    await sleep(PAGE_LOAD_WAIT_MS);

    let href = '';
    const tokenDeadline = Date.now() + TOKEN_WAIT_MS;
    let token = null;
    while (Date.now() < tokenDeadline) {
      try {
        href = String(await call('page.eval', { tabId: homeTab.id, code: 'location.href', groupId }) || '');
      } catch { href = ''; }
      const m = href.match(/[?&]token=(\d+)/);
      if (m) { token = m[1]; break; }
      await sleep(1000);
    }
    if (!token) throw new Error(`${NOT_LOGGED_IN}（当前地址：${href || '未知'}）`);

    try {
      const acc = await evalJson(homeTab.id, ACCOUNT_JS, groupId);
      account = acc.account || '';
    } catch { account = ''; }

    // ── 2. 用 token 打开留言管理页 ─────────────────────────────────
    const listUrl = `${COMMENT_PAGE_BASE}?${COMMENT_PAGE_QUERY}&token=${token}`;
    const tab = await call('tab.create', { url: listUrl, active: false, groupId });
    await sleep(PAGE_LOAD_WAIT_MS);

    let listItems = await waitForArticleList(tab.id, groupId, 15000);
    const firstPageSize = listItems.length;
    let lastPageSize = listItems.length;
    let pageIndex = 0;
    let consecutiveFailures = 0;

    // ── 3. 逐页逐篇采集 ────────────────────────────────────────────
    while (listItems.length > 0) {
      if (pageIndex >= MAX_ARTICLE_PAGES) { stopReason = 'max-pages'; break; }

      const pg = await readPagination(tab.id, groupId);
      if (pageIndex === 0) pageCount = pg.total;
      const prevCurrent = pg.current;

      for (let i = 0; i < listItems.length; i++) {
        const item = listItems[i];
        try {
          const clicked = await evalJson(tab.id, clickArticleJs(i), groupId);
          if (!clicked.ok) throw new Error(`点击失败：${clicked.reason || 'unknown'}`);
          await waitForArticleLoaded(tab.id, groupId, i, parseCount(item.count));
          const comments = await extractArticleComments(tab.id, groupId, item.title);
          articles.push({ title: item.title, articleTime: item.time, comments, error: null });
          consecutiveFailures = 0;
        } catch (err) {
          const msg = String(err?.message || err);
          process.stderr.write(`[warn] 第 ${pageIndex + 1} 页第 ${i + 1} 篇读取失败：${item.title} — ${msg}\n`);
          failures.push({ title: item.title, page: pageIndex + 1, index: i + 1, error: msg });
          articles.push({ title: item.title, articleTime: item.time, comments: [], error: msg });
          consecutiveFailures++;
          if (consecutiveFailures >= MAX_CONSECUTIVE_FAILURES) {
            stopReason = `连续 ${MAX_CONSECUTIVE_FAILURES} 篇读取失败`;
            break;
          }
        }
      }

      if (consecutiveFailures >= MAX_CONSECUTIVE_FAILURES) break;

      // ── 4. 文章列表翻页 ─────────────────────────────────────────
      const step = await goToNextArticlePage(tab.id, groupId, prevCurrent, listItems[0]?.title || null);
      if (!step.advanced) break;

      listItems = step.list;
      lastPageSize = listItems.length;
      if (listItems.length === 0) break;
      pageIndex++;
    }

    // 用分页信息推算列表文章总数（每页篇数一致时成立），用于交叉校验是否翻到底
    if (pageCount && firstPageSize > 0) {
      listTotal = (pageCount - 1) * firstPageSize + lastPageSize;
    }
  } finally {
    await call('group.close', { groupId }).catch(() => {});
  }

  // ── 5. 汇总与落盘 ────────────────────────────────────────────────
  const totalComments = articles.reduce((n, a) => n + a.comments.length, 0);
  const exportTime = nowStamp();

  const reasons = [];
  if (failures.length > 0) {
    reasons.push(`${failures.length} 篇文章读取失败：${failures.map((f) => f.title).join('、')}`);
  }
  if (stopReason === 'max-pages') {
    reasons.push(`文章列表翻页达到上限（${MAX_ARTICLE_PAGES} 页），可能未翻到底`);
  }
  if (stopReason !== 'end' && stopReason !== 'max-pages') reasons.push(stopReason);
  if (listTotal !== null && articles.length < listTotal) {
    reasons.push(`实际读取 ${articles.length} 篇 < 列表文章总数 ${listTotal} 篇`);
  }
  const partialReason = reasons.join('；');
  const partial = reasons.length > 0;

  const okArticles = articles.filter((a) => a.title && !a.error);
  const status = okArticles.length === 0 ? 'failed' : partial ? 'partial' : 'success';

  const index = {
    account,
    exportTime,
    totalArticles: articles.length,
    totalComments,
    partial,
    partialReason,
    listArticleTotal: listTotal,
    failedArticles: failures.length,
    stopReason,
    articles: articles.map((a) => ({
      title: a.title,
      articleTime: a.articleTime,
      commentCount: a.comments.length,
    })),
  };

  writeFileSync(indexFile, JSON.stringify(index, null, 2), 'utf-8');
  writeFileSync(
    dataFile,
    renderMarkdown({ account, exportTime, articles, totalComments, partial, partialReason }),
    'utf-8',
  );

  const summary = status === 'success'
    ? `导出完成：${articles.length} 篇文章、${totalComments} 条留言 → ${basename(dataFile)} / ${basename(indexFile)}`
    : status === 'partial'
      ? `部分完成：读取 ${articles.length} 篇文章、${totalComments} 条留言（${partialReason}）→ ${basename(dataFile)} / ${basename(indexFile)}`
      : `失败：未读取到任何文章留言（${partialReason || '文章列表为空'}）`;

  console.log(JSON.stringify({ status, summary, output_dir: outputDir }));
}

main().catch((err) => {
  const msg = String(err?.message || err);
  process.stderr.write(`[error] ${msg}\n`);
  console.log(JSON.stringify({ status: 'failed', error: msg, summary: msg, output_dir: process.cwd() }));
  process.exit(0);
});
