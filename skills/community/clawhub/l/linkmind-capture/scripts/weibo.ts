/**
 * Weibo content handler
 * Usage: npx tsx weibo.ts "<weibo-url>"
 * Output: JSON to stdout
 */

import { fileURLToPath } from "node:url";
import type { WeiboContent, HandlerError, ErrorCode } from "./types.js";
import { withRetry, isRetryableError } from "./retry.js";
import { loadConfig, parseConfigArg } from "./config.js";

// ---------------------------------------------------------------------------
// URL parsing
// ---------------------------------------------------------------------------

const BASE62_ALPHABET =
  "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";

export function base62ToMid(base62: string): string {
  const groups: string[] = [];
  for (let i = base62.length; i > 0; i -= 4) {
    const start = Math.max(0, i - 4);
    const group = base62.slice(start, i);
    let num = 0;
    for (const ch of group) {
      num = num * 62 + BASE62_ALPHABET.indexOf(ch);
    }
    groups.unshift(start === 0 ? String(num) : String(num).padStart(7, "0"));
  }
  return groups.join("");
}

export function extractWeiboId(url: string): string {
  let u: URL;
  try {
    u = new URL(url);
  } catch {
    throw new Error(`无效的 URL: ${url}`);
  }

  const host = u.hostname;
  const path = u.pathname;

  // m.weibo.cn/detail/{mid} or m.weibo.cn/status/{mid}
  if (host.includes("m.weibo.cn")) {
    const m = path.match(/\/(?:detail|status)\/(\d+)/);
    if (m) return m[1];
  }

  // weibo.com/{uid}/{base62}
  if (host.includes("weibo.com")) {
    const m = path.match(/\/(\d+)\/([A-Za-z0-9]+)/);
    if (m) return /^\d+$/.test(m[2]) ? m[2] : base62ToMid(m[2]);
  }

  // query param ?id=xxx
  const idParam = u.searchParams.get("id");
  if (idParam && /^\d+$/.test(idParam)) return idParam;

  throw new Error(`无法从 URL 中解析微博 ID: ${url}`);
}

// ---------------------------------------------------------------------------
// HTML cleanup
// ---------------------------------------------------------------------------

export function stripHtml(html: string): string {
  return html
    .replace(/<br\s*\/?>/gi, "\n")
    .replace(/<span class="url-icon">.*?<\/span>/gi, "")
    .replace(/<a[^>]*>#([^<]+)#<\/a>/gi, "#$1#")
    .replace(/<a[^>]*>@([^<]+)<\/a>/gi, "@$1")
    .replace(/<img[^>]*alt="([^"]*)"[^>]*>/gi, "$1")
    .replace(/<[^>]+>/g, "")
    .replace(/&#x([0-9a-fA-F]+);/gi, (_, hex) =>
      String.fromCodePoint(parseInt(hex, 16)),
    )
    .replace(/&nbsp;/g, " ")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&amp;/g, "&")
    .trim();
}

// ---------------------------------------------------------------------------
// Date parsing — Weibo format: "Sun Mar 22 14:30:00 +0800 2026"
// ---------------------------------------------------------------------------

function parseWeiboDate(dateStr: string): string {
  const d = new Date(dateStr);
  if (isNaN(d.getTime())) return dateStr;
  return d.toISOString().slice(0, 10);
}

// ---------------------------------------------------------------------------
// Short link resolution
// ---------------------------------------------------------------------------

const MOBILE_UA =
  "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) " +
  "AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148";

async function resolveShortUrl(url: string): Promise<string> {
  let u: URL;
  try {
    u = new URL(url);
  } catch {
    return url;
  }
  if (u.hostname === "t.cn") {
    const resp = await fetch(url, {
      headers: { "User-Agent": MOBILE_UA },
      redirect: "manual",
    });
    const location = resp.headers.get("location");
    if (location) return location;
  }
  return url;
}

// ---------------------------------------------------------------------------
// Visitor cookie acquisition
// ---------------------------------------------------------------------------

async function acquireVisitorCookies(): Promise<string> {
  return withRetry(
    async () => {
      const genResp = await fetch(
        "https://passport.weibo.com/visitor/genvisitor",
        {
          method: "POST",
          headers: {
            "User-Agent": MOBILE_UA,
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: "cb=gen_callback&fp=%7B%7D",
        },
      );
      const genText = await genResp.text();
      const tidMatch = genText.match(/"tid":"([^"]+)"/);
      if (!tidMatch) throw new Error("无法获取微博访客 tid");
      const tid = tidMatch[1];

      const incarnateResp = await fetch(
        `https://passport.weibo.com/visitor/visitor?a=incarnate&t=${encodeURIComponent(tid)}&w=3&c=100&gc=&cb=cross_domain&from=weibo&_rand=${Math.random()}`,
        { headers: { "User-Agent": MOBILE_UA } },
      );
      const incarnateText = await incarnateResp.text();
      const subMatch = incarnateText.match(/"sub":"([^"]+)"/);
      const subpMatch = incarnateText.match(/"subp":"([^"]+)"/);
      if (!subMatch || !subpMatch) {
        throw new Error("无法获取微博访客 cookie");
      }

      return `SUB=${subMatch[1]}; SUBP=${subpMatch[1]}`;
    },
    { shouldRetry: isRetryableError },
  );
}

// ---------------------------------------------------------------------------
// API fetch
// ---------------------------------------------------------------------------

async function fetchWeiboData(
  mid: string,
  configCookie?: string,
): Promise<Record<string, any>> {
  const cookie = configCookie || (await acquireVisitorCookies());

  const apiHeaders: Record<string, string> = {
    "User-Agent": MOBILE_UA,
    Referer: `https://m.weibo.cn/detail/${mid}`,
    Accept: "application/json",
    "X-Requested-With": "XMLHttpRequest",
    Cookie: cookie,
  };

  const data = await withRetry(
    async () => {
      const resp = await fetch(
        `https://m.weibo.cn/statuses/show?id=${mid}`,
        { headers: apiHeaders },
      );

      if (!resp.ok) {
        const err = new Error(`API 请求失败: HTTP ${resp.status}`);
        (err as any).httpStatus = resp.status;
        throw err;
      }

      const json = await resp.json();
      if (json.ok !== 1) {
        throw new Error(`微博返回错误: ${json.msg ?? "未知"}`);
      }

      return json.data;
    },
    {
      shouldRetry(err) {
        const status = (err as any).httpStatus;
        if (status && status >= 400 && status < 500) return false;
        return isRetryableError(err);
      },
    },
  );

  if (data.isLongText) {
    try {
      const extResp = await fetch(
        `https://m.weibo.cn/statuses/extend?id=${mid}`,
        { headers: apiHeaders },
      );
      if (extResp.ok) {
        const extJson = await extResp.json();
        if (extJson.ok === 1 && extJson.data?.longTextContent) {
          data.text = extJson.data.longTextContent;
        }
      }
    } catch {
      // Fall back to truncated text
    }
  }

  return data;
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function extractVideoUrl(
  pageInfo: Record<string, any> | undefined,
): string | null {
  if (!pageInfo || pageInfo.type !== "video") return null;
  const urls = pageInfo.urls ?? {};
  return (
    urls.mp4_720p_mp4 ??
    urls.mp4_hd_mp4 ??
    urls.mp4_ld_mp4 ??
    pageInfo.media_info?.stream_url_hd ??
    pageInfo.media_info?.stream_url ??
    null
  );
}

function extractImages(pics: any[] | undefined): string[] {
  if (!Array.isArray(pics)) return [];
  return pics.map((pic) => pic.large?.url ?? pic.url).filter(Boolean);
}

function makeTitle(text: string): string {
  const firstLine = text.split("\n")[0];
  if (firstLine.length <= 30) return firstLine;
  return firstLine.slice(0, 30) + "…";
}

// ---------------------------------------------------------------------------
// Content assembly
// ---------------------------------------------------------------------------

export function parseWeiboContent(
  data: Record<string, any>,
  originalUrl: string,
): WeiboContent {
  const user = data.user ?? {};
  const cleanText = stripHtml(data.text ?? "");

  let repostOf: WeiboContent["repostOf"] = null;
  if (data.retweeted_status) {
    const rt = data.retweeted_status;
    repostOf = {
      author: rt.user?.screen_name ?? "未知",
      text: stripHtml(rt.text ?? ""),
    };
  }

  return {
    platform: "weibo",
    title: makeTitle(cleanText),
    author: user.screen_name ?? "未知",
    authorAvatar: user.profile_image_url ?? undefined,
    date: parseWeiboDate(data.created_at ?? ""),
    text: cleanText,
    images: extractImages(data.pics),
    videoUrl: extractVideoUrl(data.page_info),
    repostOf,
    stats: {
      reposts: data.reposts_count ?? 0,
      comments: data.comments_count ?? 0,
      likes: data.attitudes_count ?? 0,
    },
    originalUrl,
    fetchedAt: new Date().toISOString(),
  };
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

function categorizeError(e: unknown): { code: ErrorCode; details: string } {
  const msg = e instanceof Error ? e.message : String(e);
  const lower = msg.toLowerCase();
  const status = (e as any)?.httpStatus as number | undefined;

  if (status === 404 || lower.includes("无法从 url"))
    return { code: "NOT_FOUND", details: "请检查链接是否正确" };
  if (status === 403 || status === 401 || lower.includes("登录"))
    return { code: "AUTH", details: "该内容可能需要登录，请在 .env 中配置 LINKMIND_WEIBO_COOKIE（参考 .env.example）" };
  if (status === 429 || lower.includes("rate") || lower.includes("频繁"))
    return { code: "RATE_LIMIT", details: "请求过于频繁，建议稍后重试" };
  if (lower.includes("无法获取") || lower.includes("parse") || lower.includes("解析"))
    return { code: "PARSE", details: "内容解析失败，平台接口可能已变更" };
  if (
    lower.includes("fetch") ||
    lower.includes("network") ||
    lower.includes("timeout") ||
    lower.includes("econnr")
  )
    return { code: "NETWORK", details: "网络请求失败，建议检查网络连接后重试" };

  return { code: "UNKNOWN", details: "建议稍后重试" };
}

async function main(): Promise<void> {
  const url = process.argv[2];

  if (!url) {
    const err: HandlerError = { error: "请提供微博链接作为参数" };
    console.log(JSON.stringify(err));
    process.exit(1);
  }

  try {
    const configPath = parseConfigArg(process.argv);
    let configCookie: string | undefined;
    if (configPath) {
      try {
        const cfg = loadConfig(configPath);
        if (cfg.cookies?.weibo) configCookie = cfg.cookies.weibo;
      } catch {
        // Config read failure is non-fatal; fall back to visitor cookies
      }
    }

    const resolved = await resolveShortUrl(url);
    const mid = extractWeiboId(resolved);
    const data = await fetchWeiboData(mid, configCookie);
    const content = parseWeiboContent(data, url);
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
