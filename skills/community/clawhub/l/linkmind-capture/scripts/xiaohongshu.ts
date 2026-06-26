/**
 * Xiaohongshu (RedNote) content handler
 * Usage: npx tsx xiaohongshu.ts "<xiaohongshu-url>"
 * Output: JSON to stdout
 *
 * Uses Chrome DevTools Protocol (CDP) for browser-based content extraction.
 * Connects to the user's system Chrome — no Chromium download required.
 */

import { fileURLToPath } from "node:url";
import type { XiaohongshuContent, HandlerError, ErrorCode } from "./types.js";
import { withRetry, isRetryableError } from "./retry.js";
import { loadConfig, parseConfigArg } from "./config.js";
import { launchWithPage, type CDPBrowser, type CDPPage } from "./chrome-cdp.js";

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const DESKTOP_UA =
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) " +
  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36";

const NAVIGATION_TIMEOUT = 30_000;
const CONTENT_WAIT_TIMEOUT = 15_000;

// ---------------------------------------------------------------------------
// URL parsing
// ---------------------------------------------------------------------------

export function extractNoteId(url: string): string {
  let u: URL;
  try {
    u = new URL(url);
  } catch {
    throw new Error(`无效的 URL: ${url}`);
  }

  const host = u.hostname;
  const path = u.pathname;

  if (host.includes("xiaohongshu.com")) {
    const m = path.match(/\/(?:explore|discovery\/item)\/([a-f0-9]+)/);
    if (m) return m[1];
    const m2 = path.match(/\/user\/profile\/[^/]+\/([a-f0-9]+)/);
    if (m2) return m2[1];
  }

  if (host.includes("xhslink.com")) {
    const segments = path.split("/").filter(Boolean);
    const last = segments[segments.length - 1];
    if (last && /^[A-Za-z0-9]+$/.test(last) && last.length > 1) return last;
  }

  throw new Error(`无法从 URL 中解析小红书笔记 ID: ${url}`);
}

// ---------------------------------------------------------------------------
// Short link resolution
// ---------------------------------------------------------------------------

async function resolveShortUrl(url: string): Promise<string> {
  let u: URL;
  try {
    u = new URL(url);
  } catch {
    return url;
  }

  if (!u.hostname.includes("xhslink.com")) return url;

  return withRetry(
    async () => {
      let current = url;
      for (let i = 0; i < 5; i++) {
        const resp = await fetch(current, {
          headers: { "User-Agent": DESKTOP_UA },
          redirect: "manual",
        });
        const location = resp.headers.get("location");
        if (!location) break;
        current = location.startsWith("http")
          ? location
          : new URL(location, current).href;
        if (current.includes("xiaohongshu.com")) return current;
      }
      return current;
    },
    { shouldRetry: isRetryableError },
  );
}

// ---------------------------------------------------------------------------
// Stealth script injected before every navigation
// ---------------------------------------------------------------------------

const STEALTH_SCRIPT = `
  Object.defineProperty(navigator, "webdriver", { get: function() { return undefined; } });
  Object.defineProperty(navigator, "plugins", { get: function() { return [1, 2, 3, 4, 5]; } });
  Object.defineProperty(navigator, "languages", { get: function() { return ["zh-CN", "zh", "en"]; } });
  window.chrome = { runtime: {} };
`;

// ---------------------------------------------------------------------------
// Content extraction — __INITIAL_STATE__
// ---------------------------------------------------------------------------

interface RawNoteData {
  title: string;
  desc: string;
  imageList: Array<{ urlDefault: string; url?: string; infoList?: Array<{ url: string }> }>;
  video?: { consumer?: { originVideoKey?: string }; media?: { stream?: { h264?: Array<{ masterUrl?: string }> } } };
  tagList: Array<{ name: string }>;
  user: { nickname: string; avatar?: string };
  time: number;
  interactInfo: {
    likedCount: string;
    collectedCount: string;
    commentCount: string;
  };
  type: string;
}

function buildExtractScript(noteId: string): string {
  return `(() => {
    var state = window.__INITIAL_STATE__;
    if (!state) return null;

    var noteMap =
      (state.note && state.note.noteDetailMap) ||
      (state.note && state.note.noteMap) ||
      null;
    if (!noteMap) return null;

    var entry = noteMap["${noteId}"];
    var note = (entry && entry.note) ? entry.note : entry;
    if (!note || (!note.title && !note.desc)) return null;

    function unwrap(v) {
      if (v && typeof v === 'object' && '_rawValue' in v) return v._rawValue;
      if (v && typeof v === 'object' && '_value' in v) return v._value;
      return v;
    }
    function str(v) { var u = unwrap(v); return (u == null) ? "" : String(u); }
    function num(v) { var u = unwrap(v); return (typeof u === 'number') ? u : 0; }
    function arr(v) { var u = unwrap(v); return Array.isArray(u) ? u : []; }

    var seen = new WeakSet();
    function safeClone(obj, depth) {
      if (depth > 6 || obj == null) return obj;
      if (typeof obj !== 'object') return obj;
      if (seen.has(obj)) return null;
      seen.add(obj);
      if (Array.isArray(obj)) return obj.map(function(v) { return safeClone(v, depth + 1); });
      var out = {};
      Object.keys(obj).forEach(function(k) {
        if (k.indexOf('__') === 0 || k === 'dep' || k === 'effect' || k === 'computed') return;
        try { out[k] = safeClone(obj[k], depth + 1); } catch(e) {}
      });
      return out;
    }

    return safeClone({
      title: str(note.title),
      desc: str(note.desc),
      imageList: arr(note.imageList),
      video: note.video || null,
      tagList: arr(note.tagList),
      user: {
        nickname: str(note.user && (note.user.nickname || note.user.name)),
        avatar: str(note.user && (note.user.avatar || note.user.images)),
      },
      time: num(note.time),
      interactInfo: {
        likedCount: str(note.interactInfo && note.interactInfo.likedCount),
        collectedCount: str(note.interactInfo && note.interactInfo.collectedCount),
        commentCount: str(note.interactInfo && note.interactInfo.commentCount),
      },
      type: str(note.type),
    }, 0);
  })()`;
}

// ---------------------------------------------------------------------------
// Content extraction — DOM fallback
// ---------------------------------------------------------------------------

const DOM_EXTRACT_SCRIPT = `(() => {
  function qs(sel) {
    var el = document.querySelector(sel);
    return (el && el.textContent) ? el.textContent.trim() : "";
  }

  var title =
    qs("#detail-title") ||
    qs(".note-top .title") ||
    qs("[class*='title']") ||
    "";

  var desc =
    qs("#detail-desc") ||
    qs(".note-text") ||
    qs("[class*='desc']") ||
    "";

  var imgElements = document.querySelectorAll(
    ".swiper-slide img, .note-image img, [class*='carousel'] img, #noteContainer img"
  );
  var imageList = Array.from(imgElements)
    .map(function(img) {
      var src = img.src || img.getAttribute("data-src") || "";
      return { urlDefault: src };
    })
    .filter(function(i) { return i.urlDefault && i.urlDefault.indexOf("avatar") === -1; });

  var videoEl = document.querySelector("video source, video");
  var videoSrc = videoEl
    ? (videoEl.src || videoEl.getAttribute("src") || "")
    : "";

  var authorEl =
    document.querySelector(".author-container .username") ||
    document.querySelector("[class*='author'] [class*='name']") ||
    document.querySelector(".user-info .name");
  var authorName = (authorEl && authorEl.textContent) ? authorEl.textContent.trim() : "";

  var tags = [];
  document
    .querySelectorAll('a[href*="search_result"], a[href*="tag"]')
    .forEach(function(a) {
      var text = (a.textContent || "").trim().replace(/^#/, "");
      if (text) tags.push({ name: text });
    });

  function parseCount(sel) {
    var text = qs(sel);
    return text.replace(/[^\\d]/g, "") || "0";
  }

  return {
    title: title,
    desc: desc,
    imageList: imageList,
    video: videoSrc
      ? { consumer: { originVideoKey: videoSrc } }
      : undefined,
    tagList: tags,
    user: { nickname: authorName },
    time: 0,
    interactInfo: {
      likedCount: parseCount(".like-wrapper .count, [class*='like'] [class*='count']"),
      collectedCount: parseCount(".collect-wrapper .count, [class*='collect'] [class*='count']"),
      commentCount: parseCount(".chat-wrapper .count, [class*='comment'] [class*='count']"),
    },
    type: videoSrc ? "video" : "normal",
  };
})()`;

// ---------------------------------------------------------------------------
// Cookie helpers
// ---------------------------------------------------------------------------

function parseCookieString(
  cookieStr: string,
  domain: string,
): Array<{ name: string; value: string; domain: string; path: string }> {
  return cookieStr
    .split(";")
    .map((pair) => pair.trim())
    .filter(Boolean)
    .map((pair) => {
      const eqIdx = pair.indexOf("=");
      if (eqIdx === -1) return null;
      return {
        name: pair.slice(0, eqIdx).trim(),
        value: pair.slice(eqIdx + 1).trim(),
        domain,
        path: "/",
      };
    })
    .filter(Boolean) as Array<{
    name: string;
    value: string;
    domain: string;
    path: string;
  }>;
}

// ---------------------------------------------------------------------------
// URL helpers
// ---------------------------------------------------------------------------

function isSecurityBlocked(url: string): boolean {
  try {
    const pathname = new URL(url).pathname;
    return pathname.includes("/404") || pathname.includes("/login") || pathname.includes("/captcha");
  } catch {
    return false;
  }
}

const NOTE_URL_RE = /\/(?:explore|discovery\/item)\/([a-f0-9]+)/;

function isNotePage(url: string): boolean {
  return NOTE_URL_RE.test(url);
}

// ---------------------------------------------------------------------------
// Content fetch (CDP)
// ---------------------------------------------------------------------------

async function sleep(ms: number): Promise<void> {
  await new Promise((r) => setTimeout(r, ms));
}

async function fetchXiaohongshuData(
  noteId: string,
  originalUrl: string,
  configCookie?: string,
): Promise<RawNoteData> {
  const noteUrl = `https://www.xiaohongshu.com/explore/${noteId}`;

  const browser = await withRetry(
    () => launchWithPage({ headless: false }),
    { maxAttempts: 2, baseDelayMs: 2000 },
  );

  try {
    const { page } = browser;

    await page.addScriptOnNewDocument(STEALTH_SCRIPT);

    if (configCookie) {
      const parsed = parseCookieString(configCookie, ".xiaohongshu.com");
      if (parsed.length) await page.setCookies(parsed);
    }

    // Warm up: visit explore page first to establish session
    await page.navigate("https://www.xiaohongshu.com/explore", {
      timeout: NAVIGATION_TIMEOUT,
    });
    await sleep(2000);
    await page.mouseMove(300 + Math.random() * 200, 300 + Math.random() * 200);
    await sleep(800 + Math.random() * 400);
    await page.mouseMove(500 + Math.random() * 200, 250 + Math.random() * 150);
    await sleep(1000 + Math.random() * 500);

    // Navigate to the actual note
    await page.navigate(originalUrl, { timeout: NAVIGATION_TIMEOUT });
    await sleep(3000);

    let currentUrl = await page.url();

    if (isSecurityBlocked(currentUrl) || !isNotePage(currentUrl)) {
      await sleep(1000 + Math.random() * 1000);
      await page.navigate(noteUrl, { timeout: NAVIGATION_TIMEOUT });
      await sleep(3000);
      currentUrl = await page.url();
    }

    const notePageMatch = currentUrl.match(NOTE_URL_RE);
    if (!notePageMatch) {
      throw new Error(
        "被安全验证拦截，无法访问笔记页面。请在 .env 中配置 LINKMIND_XHS_COOKIE（参考 .env.example）",
      );
    }
    const actualNoteId = notePageMatch[1];

    await page.waitForSelector(
      "#noteContainer, .note-container, .note-detail",
      CONTENT_WAIT_TIMEOUT,
    );
    await sleep(2000);

    let data = await page.evaluate<RawNoteData | null>(
      buildExtractScript(actualNoteId),
    );

    if (!data || (!data.title && !data.desc)) {
      data = await page.evaluate<RawNoteData>(DOM_EXTRACT_SCRIPT);
    }

    if (!data || (!data.title && !data.desc)) {
      throw new Error(
        "无法提取笔记内容，可能被反爬拦截或页面结构已变更",
      );
    }

    return data;
  } finally {
    await browser.close();
  }
}

// ---------------------------------------------------------------------------
// Content assembly
// ---------------------------------------------------------------------------

function extractImageUrls(imageList: RawNoteData["imageList"]): string[] {
  return imageList
    .map((img) => {
      if (img.infoList?.length) {
        const last = img.infoList[img.infoList.length - 1];
        if (last.url) return last.url;
      }
      return img.url ?? img.urlDefault;
    })
    .filter(Boolean)
    .map((url) => (url.startsWith("//") ? `https:${url}` : url));
}

function extractVideoUrl(video: RawNoteData["video"]): string | null {
  if (!video) return null;
  const streams = video.media?.stream?.h264;
  if (streams?.length) {
    const best = streams[0];
    if (best.masterUrl) return best.masterUrl;
  }
  const key = video.consumer?.originVideoKey;
  if (key) {
    return key.startsWith("http")
      ? key
      : `https://sns-video-bd.xhscdn.com/${key}`;
  }
  return null;
}

function extractTags(tagList: RawNoteData["tagList"], text: string): string[] {
  const tagSet = new Set<string>();
  for (const t of tagList) {
    if (t.name) tagSet.add(t.name);
  }
  const hashtagMatches = text.match(/#([^#\s]+)/g);
  if (hashtagMatches) {
    for (const m of hashtagMatches) {
      const clean = m.replace(/^#/, "").replace(/\[话题\]$/, "");
      if (clean) tagSet.add(clean);
    }
  }
  return [...tagSet];
}

function formatTimestamp(ts: number): string {
  if (!ts) return new Date().toISOString().slice(0, 10);
  const d = new Date(ts);
  if (isNaN(d.getTime())) return new Date().toISOString().slice(0, 10);
  return d.toISOString().slice(0, 10);
}

function parseStatCount(val: string): number {
  const str = String(val).trim();
  if (!str || str === "") return 0;
  if (str.endsWith("w") || str.endsWith("万")) {
    return Math.round(parseFloat(str) * 10000);
  }
  const n = parseInt(str, 10);
  return isNaN(n) ? 0 : n;
}

function makeTitle(title: string, desc: string): string {
  const raw = title || desc;
  if (!raw) return "小红书笔记";
  const firstLine = raw.split("\n")[0];
  if (firstLine.length <= 30) return firstLine;
  return firstLine.slice(0, 30) + "…";
}

export function parseXiaohongshuContent(
  data: RawNoteData,
  originalUrl: string,
): XiaohongshuContent {
  const fullText = [data.title, data.desc].filter(Boolean).join("\n\n");
  const tags = extractTags(data.tagList, fullText);

  return {
    platform: "xiaohongshu",
    title: makeTitle(data.title, data.desc),
    author: data.user.nickname || "未知",
    authorAvatar: data.user.avatar || undefined,
    date: formatTimestamp(data.time),
    text: data.desc || data.title || "",
    images: extractImageUrls(data.imageList),
    videoUrl: extractVideoUrl(data.video),
    tags,
    stats: {
      likes: parseStatCount(data.interactInfo.likedCount),
      collects: parseStatCount(data.interactInfo.collectedCount),
      comments: parseStatCount(data.interactInfo.commentCount),
    },
    originalUrl,
    fetchedAt: new Date().toISOString(),
  };
}

// ---------------------------------------------------------------------------
// Error categorization
// ---------------------------------------------------------------------------

function categorizeError(e: unknown): { code: ErrorCode; details: string } {
  const msg = e instanceof Error ? e.message : String(e);
  const lower = msg.toLowerCase();

  if (lower.includes("无法从 url") || lower.includes("无效"))
    return { code: "NOT_FOUND", details: "请检查链接是否正确" };
  if (lower.includes("登录") || lower.includes("login") || lower.includes("403") || lower.includes("安全验证"))
    return { code: "AUTH", details: "该内容可能需要登录或 cookies 已过期，请在 .env 中配置 LINKMIND_XHS_COOKIE（参考 .env.example）" };
  if (lower.includes("反爬") || lower.includes("拦截"))
    return { code: "RATE_LIMIT", details: "被反爬机制拦截，建议稍后重试或配置 cookies" };
  if (lower.includes("无法提取") || lower.includes("页面结构"))
    return { code: "PARSE", details: "内容解析失败，页面结构可能已变更" };
  if (lower.includes("未找到 chrome"))
    return { code: "NETWORK", details: "未找到系统 Chrome 浏览器，请安装 Google Chrome" };
  if (
    lower.includes("fetch") ||
    lower.includes("network") ||
    lower.includes("timeout") ||
    lower.includes("econnr") ||
    lower.includes("chrome")
  )
    return { code: "NETWORK", details: "网络请求或浏览器启动失败，建议检查网络后重试" };

  return { code: "UNKNOWN", details: "建议稍后重试" };
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main(): Promise<void> {
  const url = process.argv[2];

  if (!url) {
    const err: HandlerError = { error: "请提供小红书链接作为参数" };
    console.log(JSON.stringify(err));
    process.exit(1);
  }

  try {
    const configPath = parseConfigArg(process.argv);
    let configCookie: string | undefined;
    if (configPath) {
      try {
        const cfg = loadConfig(configPath);
        if (cfg.cookies?.xiaohongshu) configCookie = cfg.cookies.xiaohongshu;
      } catch {
        // Config read failure is non-fatal; proceed without cookies
      }
    }

    const resolved = await resolveShortUrl(url);
    const noteId = extractNoteId(resolved);
    const data = await fetchXiaohongshuData(noteId, url, configCookie);
    const content = parseXiaohongshuContent(data, url);
    console.log(JSON.stringify(content, null, 2));
  } catch (e) {
    const { code, details } = categorizeError(e);
    const err: HandlerError = {
      error: e instanceof Error ? e.message : String(e),
      code,
      url,
      details,
    };
    console.log(JSON.stringify(err, null, 2));
    process.exit(1);
  }
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  main();
}
