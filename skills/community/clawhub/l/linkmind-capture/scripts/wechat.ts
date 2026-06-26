/**
 * WeChat Official Account article handler
 * Usage: npx tsx wechat.ts "<url>"
 * Output: JSON to stdout
 */

import { fileURLToPath } from "node:url";
import type { WechatContent, HandlerError, ErrorCode } from "./types.js";
import { withRetry, isRetryableError } from "./retry.js";
import { loadConfig, parseConfigArg } from "./config.js";
import { launchWithPage } from "./chrome-cdp.js";

const DESKTOP_UA =
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) " +
  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36";

// ---------------------------------------------------------------------------
// URL validation
// ---------------------------------------------------------------------------

export function extractArticleUrl(url: string): string {
  let u: URL;
  try {
    u = new URL(url);
  } catch {
    throw new Error(`无效的 URL: ${url}`);
  }

  if (!u.hostname.includes("mp.weixin.qq.com")) {
    throw new Error(`不是微信公众号链接: ${url}`);
  }

  // 必须是文章路径：/s/<id> 或 /s?... 查询参数形式
  const isShort = /^\/s\/[A-Za-z0-9_-]+/.test(u.pathname);
  const isLong = u.pathname === "/s" && u.searchParams.has("__biz");
  if (!isShort && !isLong) {
    throw new Error(`不是微信文章链接（路径格式不匹配）: ${url}`);
  }

  return url;
}

// ---------------------------------------------------------------------------
// HTML variable extraction
// ---------------------------------------------------------------------------

export function extractHtmlVar(html: string, varName: string): string | null {
  // 匹配 var <name> = "value"; 或 var <name> = 'value';
  // 使用 \b 确保精确匹配变量名（不匹配前缀）
  const re = new RegExp(
    `var\\s+${varName}\\s*=\\s*(?:"([^"]*)"|'([^']*)')`,
    "s",
  );
  const m = html.match(re);
  if (!m) return null;
  return m[1] !== undefined ? m[1] : m[2] ?? null;
}

// ---------------------------------------------------------------------------
// HTML content cleaning
// ---------------------------------------------------------------------------

export function stripWechatHtml(html: string): string {
  return html
    .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, "")
    .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, "")
    .replace(/<br\s*\/?>/gi, "\n")
    // Block-level close tags → paragraph break (must run before generic tag strip)
    .replace(/<\/(p|div|section|article|h[1-6]|blockquote|ul|ol|tr|td|th)>/gi, "\n\n")
    // List items get a bullet prefix
    .replace(/<li[^>]*>/gi, "\n- ")
    .replace(/<\/li>/gi, "")
    .replace(/<[^>]+>/g, "")
    .replace(/&#x([0-9a-fA-F]+);/gi, (_, hex) =>
      String.fromCodePoint(parseInt(hex, 16)),
    )
    .replace(/&nbsp;/g, " ")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&amp;/g, "&")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

const WECHAT_UI_DOMAINS = ["res.wx.qq.com"];

/**
 * Convert WeChat article HTML to Markdown with inline images.
 * Unlike stripWechatHtml (which discards images), this preserves each <img>
 * as a `![](url)` at its original position in the text flow, so the resulting
 * Markdown faithfully reflects the author's image placement.
 */
export function convertWechatHtmlToMd(html: string): string {
  // Replace <img> tags with Markdown image placeholders before stripping HTML
  const withImages = html.replace(/<img\s[^>]*>/gi, (tag) => {
    const dataSrc = tag.match(/data-src="([^"]+)"/)?.[1];
    const src = tag.match(/\bsrc="([^"]+)"/)?.[1];
    let url: string | null = null;
    if (dataSrc && dataSrc.startsWith("http")) url = dataSrc;
    else if (src && src.startsWith("http")) url = src;
    if (!url || WECHAT_UI_DOMAINS.some((d) => url!.includes(d))) return "";
    return `\n\n![](${url})\n\n`;
  });

  return withImages
    .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, "")
    .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, "")
    .replace(/<br\s*\/?>/gi, "\n")
    // Block-level close tags → paragraph break (must run before generic tag strip)
    .replace(/<\/(p|div|section|article|h[1-6]|blockquote|ul|ol|tr|td|th)>/gi, "\n\n")
    // List items get a bullet prefix
    .replace(/<li[^>]*>/gi, "\n- ")
    .replace(/<\/li>/gi, "")
    .replace(/<[^>]+>/g, "")
    .replace(/&#x([0-9a-fA-F]+);/gi, (_, hex) =>
      String.fromCodePoint(parseInt(hex, 16)),
    )
    .replace(/&nbsp;/g, " ")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&amp;/g, "&")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

export function extractContentImages(html: string): string[] {
  const results: string[] = [];
  const imgRe = /<img\s[^>]*>/gi;
  let m: RegExpExecArray | null;
  while ((m = imgRe.exec(html)) !== null) {
    const tag = m[0];
    const dataSrc = tag.match(/data-src="([^"]+)"/)?.[1];
    const src = tag.match(/\bsrc="([^"]+)"/)?.[1];
    let url: string | null = null;
    if (dataSrc && dataSrc.startsWith("http")) {
      url = dataSrc;
    } else if (src && src.startsWith("http")) {
      url = src;
    }
    if (url && !WECHAT_UI_DOMAINS.some((d) => url!.includes(d))) {
      results.push(url);
    }
  }
  return results;
}

export function formatUnixTimestamp(ts: string): string {
  const today = new Date().toISOString().slice(0, 10);
  const n = parseInt(ts, 10);
  if (!n || isNaN(n)) return today;
  const d = new Date(n * 1000);
  if (isNaN(d.getTime())) return today;
  return d.toISOString().slice(0, 10);
}

// ---------------------------------------------------------------------------
// Helper functions for parseWechatHtml
// ---------------------------------------------------------------------------

/**
 * Extract the inner HTML of #js_content by tracking div nesting depth.
 * A lazy regex like ([\s\S]*?)<\/div> would stop at the FIRST </div>,
 * silently truncating any article body that contains nested divs.
 */
function extractJsContent(html: string): string {
  const openRe = /<div[^>]+id="js_content"[^>]*>/i;
  const openMatch = html.match(openRe);
  if (!openMatch || openMatch.index === undefined) return "";

  const contentStart = openMatch.index + openMatch[0].length;
  let depth = 1;
  let i = contentStart;

  while (i < html.length && depth > 0) {
    if (html[i] !== "<") { i++; continue; }
    if (/^<\/div>/i.test(html.slice(i, i + 6))) {
      depth--;
      if (depth === 0) return html.slice(contentStart, i);
      i += 6;
    } else if (/^<div[\s>/]/i.test(html.slice(i, i + 5))) {
      depth++;
      i++;
    } else {
      i++;
    }
  }

  // Ran out of HTML without finding the closing tag — return what we have
  return html.slice(contentStart);
}

function makeTitle(text: string): string {
  const firstLine = text.split("\n")[0];
  if (firstLine.length <= 30) return firstLine;
  return firstLine.slice(0, 30) + "…";
}

function extractOgMeta(html: string, property: string): string | null {
  const m = html.match(
    new RegExp(`<meta[^>]+property="${property}"[^>]+content="([^"]*)"`, "i"),
  );
  return m ? m[1] : null;
}

function extractVideoUrl(html: string): string | null {
  const m = html.match(/<video[^>]*>[\s\S]*?<source[^>]+src="([^"]+)"/i)
    ?? html.match(/<video[^>]+src="([^"]+)"/i);
  return m ? m[1] : null;
}

export function parseWechatHtml(html: string, originalUrl: string): WechatContent {
  const title = extractHtmlVar(html, "msg_title") ?? extractOgMeta(html, "og:title") ?? "";
  const nickname = extractHtmlVar(html, "nickname") ?? "";
  const ct = extractHtmlVar(html, "ct") ?? "0";
  const coverVar = extractHtmlVar(html, "cover") ?? "";
  const coverImage = coverVar || extractOgMeta(html, "og:image") || null;
  const digest = extractHtmlVar(html, "desc") ?? extractOgMeta(html, "og:description") ?? "";

  // Extract #js_content using depth-tracking (not lazy regex — see extractJsContent)
  const contentHtml = extractJsContent(html);
  const text = stripWechatHtml(contentHtml);
  const richContent = convertWechatHtmlToMd(contentHtml);
  const images = extractContentImages(contentHtml);
  const videoUrl = extractVideoUrl(contentHtml);

  return {
    platform: "wechat",
    title: title || makeTitle(text),
    author: nickname || "未知",
    accountName: nickname || "未知",
    date: formatUnixTimestamp(ct),
    digest,
    coverImage: coverImage || null,
    text,
    richContent,
    images,
    videoUrl,
    readCount: null,
    likeCount: null,
    inLookCount: null,
    originalUrl,
    fetchedAt: new Date().toISOString(),
  };
}

// ---------------------------------------------------------------------------
// Validity check
// ---------------------------------------------------------------------------

function isExtractionValid(content: WechatContent): boolean {
  return content.title.length > 0 && content.text.length > 0;
}

// ---------------------------------------------------------------------------
// Stats API (optional, requires cookie)
// ---------------------------------------------------------------------------

interface WechatStats {
  readCount: number | null;
  likeCount: number | null;
  inLookCount: number | null;
}

async function fetchStats(
  pageHtml: string,
  pageUrl: string,
  cookie: string,
): Promise<WechatStats> {
  const empty: WechatStats = { readCount: null, likeCount: null, inLookCount: null };
  try {
    const appmsgtoken = extractHtmlVar(pageHtml, "appmsgtoken");
    if (!appmsgtoken) return empty;

    const u = new URL(pageUrl);
    const biz = u.searchParams.get("__biz");
    const mid = u.searchParams.get("mid");
    const sn = u.searchParams.get("sn");
    const idx = u.searchParams.get("idx") ?? "1";

    if (!biz || !mid || !sn) {
      // Short-form URL: lacks mid/sn in URL; skip stats
      return empty;
    }

    const statsUrl = `https://mp.weixin.qq.com/mp/getappmsgext?__biz=${biz}&mid=${mid}&sn=${sn}&idx=${idx}&appmsgtoken=${encodeURIComponent(appmsgtoken)}&f=json`;

    const resp = await fetch(statsUrl, {
      headers: {
        "User-Agent": DESKTOP_UA,
        Referer: pageUrl,
        Cookie: cookie,
      },
    });

    if (!resp.ok) return empty;
    const json = await resp.json() as Record<string, any>;
    const stat = json?.appmsgstat;
    if (!stat) return empty;

    return {
      readCount: typeof stat.read_num === "number" ? stat.read_num : null,
      likeCount: typeof stat.like_num === "number" ? stat.like_num : null,
      inLookCount: typeof stat.old_like_num === "number" ? stat.old_like_num : null,
    };
  } catch {
    return empty;
  }
}

// ---------------------------------------------------------------------------
// HTTP fetch path
// ---------------------------------------------------------------------------

async function fetchViaHttp(url: string, cookie?: string): Promise<WechatContent | null> {
  const headers: Record<string, string> = {
    "User-Agent": DESKTOP_UA,
    Accept: "text/html,application/xhtml+xml",
    "Accept-Language": "zh-CN,zh;q=0.9",
  };
  if (cookie) headers["Cookie"] = cookie;

  let resp: Response;
  try {
    resp = await withRetry(
      () =>
        fetch(url, { headers, redirect: "follow" }),
      { shouldRetry: isRetryableError },
    );
  } catch {
    return null;
  }

  if (resp.status === 403 || resp.status === 401) return null;
  if (!resp.ok) return null;

  const html = await resp.text();
  const content = parseWechatHtml(html, url);

  if (!isExtractionValid(content)) return null;

  // Try to fetch stats if cookie present
  if (cookie) {
    const stats = await fetchStats(html, url, cookie);
    content.readCount = stats.readCount;
    content.likeCount = stats.likeCount;
    content.inLookCount = stats.inLookCount;
  }

  return content;
}

// ---------------------------------------------------------------------------
// CDP DOM extraction script
// ---------------------------------------------------------------------------

const WECHAT_CDP_EXTRACT = `(() => {
  function getVar(name) {
    try { return String(eval(name) ?? ''); } catch { return ''; }
  }
  function qs(sel) {
    var el = document.querySelector(sel);
    return el ? el.textContent.trim() : '';
  }
  var contentEl = document.querySelector('#js_content');
  var descHtml = contentEl ? contentEl.innerHTML : '';
  var imgs = Array.from(document.querySelectorAll('#js_content img'))
    .map(function(img) {
      return img.getAttribute('data-src') || img.getAttribute('src') || '';
    })
    .filter(function(s) { return s && s.startsWith('http'); });
  return {
    msg_title: getVar('msg_title') || qs('#activity-name') || qs('.rich_media_title'),
    nickname: getVar('nickname') || qs('#js_name') || qs('.profile_nickname'),
    ct: getVar('ct') || '',
    cover: getVar('cover') || '',
    desc: getVar('desc') || '',
    descHtml: descHtml,
    images: imgs,
  };
})()`;

// ---------------------------------------------------------------------------
// CDP fetch path
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
    .filter(Boolean) as Array<{ name: string; value: string; domain: string; path: string }>;
}

async function sleep(ms: number): Promise<void> {
  await new Promise((r) => setTimeout(r, ms));
}

async function fetchViaCdp(url: string, cookie?: string): Promise<WechatContent> {
  const browser = await withRetry(
    () => launchWithPage({ headless: false }),
    { maxAttempts: 2, baseDelayMs: 2000 },
  );

  try {
    const { page } = browser;

    if (cookie) {
      const parsed = parseCookieString(cookie, ".weixin.qq.com");
      if (parsed.length) await page.setCookies(parsed);
    }

    await page.navigate(url, { timeout: 30_000 });
    await sleep(3000);

    await page.waitForSelector("#js_content, #activity-name", 15_000).catch(() => {});
    await sleep(1500);

    interface CdpExtractResult {
      msg_title: string;
      nickname: string;
      ct: string;
      cover: string;
      desc: string;
      descHtml: string;
      images: string[];
    }

    const raw = await page.evaluate<CdpExtractResult>(WECHAT_CDP_EXTRACT);

    if (!raw || (!raw.msg_title && !raw.descHtml)) {
      throw new Error("CDP 无法提取微信文章内容，可能被拦截或需要登录");
    }

    const text = stripWechatHtml(raw.descHtml);
    const richContent = convertWechatHtmlToMd(raw.descHtml);
    const title = raw.msg_title || makeTitle(text);
    const images = raw.images.filter(
      (url) => !WECHAT_UI_DOMAINS.some((d) => url.includes(d)),
    );

    return {
      platform: "wechat",
      title,
      author: raw.nickname || "未知",
      accountName: raw.nickname || "未知",
      date: formatUnixTimestamp(raw.ct),
      digest: raw.desc || "",
      coverImage: raw.cover || null,
      text,
      richContent,
      images,
      videoUrl: extractVideoUrl(raw.descHtml),
      readCount: null,
      likeCount: null,
      inLookCount: null,
      originalUrl: url,
      fetchedAt: new Date().toISOString(),
    };
  } finally {
    await browser.close();
  }
}

// ---------------------------------------------------------------------------
// Orchestrator
// ---------------------------------------------------------------------------

async function fetchWechatData(url: string, cookie?: string): Promise<WechatContent> {
  const httpResult = await fetchViaHttp(url, cookie);
  if (httpResult) return httpResult;
  return fetchViaCdp(url, cookie);
}

// ---------------------------------------------------------------------------
// Error categorization
// ---------------------------------------------------------------------------

function categorizeError(e: unknown): { code: ErrorCode; details: string } {
  const msg = e instanceof Error ? e.message : String(e);
  const lower = msg.toLowerCase();
  const status = (e as any)?.httpStatus as number | undefined;

  if (status === 404 || lower.includes("无效的 url") || lower.includes("不是微信"))
    return { code: "NOT_FOUND", details: "请检查链接是否是微信公众号文章链接" };
  if (status === 403 || status === 401 || lower.includes("登录") || lower.includes("拦截"))
    return { code: "AUTH", details: "内容需要登录，请在 .env 中配置 LINKMIND_WXMP_COOKIE（参考 .env.example）" };
  if (status === 429 || lower.includes("rate") || lower.includes("频繁"))
    return { code: "RATE_LIMIT", details: "请求过于频繁，建议稍后重试" };
  if (lower.includes("无法提取") || lower.includes("parse") || lower.includes("变更"))
    return { code: "PARSE", details: "内容解析失败，页面结构可能已变更，请提 issue" };
  if (
    lower.includes("fetch") ||
    lower.includes("network") ||
    lower.includes("timeout") ||
    lower.includes("econnr") ||
    lower.includes("chrome")
  )
    return { code: "NETWORK", details: "网络请求失败，建议检查网络连接后重试" };

  return { code: "UNKNOWN", details: "建议稍后重试" };
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main(): Promise<void> {
  const url = process.argv[2];

  if (!url) {
    const err: HandlerError = { error: "请提供微信公众号文章链接作为参数" };
    console.log(JSON.stringify(err));
    process.exit(1);
  }

  try {
    const configPath = parseConfigArg(process.argv);
    let configCookie: string | undefined;
    if (configPath) {
      try {
        const cfg = loadConfig(configPath);
        if (cfg.cookies?.wechat) configCookie = cfg.cookies.wechat;
      } catch {
        // Non-fatal; proceed without cookie
      }
    }

    const canonical = extractArticleUrl(url);
    const content = await fetchWechatData(canonical, configCookie);
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
