/**
 * Xiaoyuzhou (小宇宙) podcast handler
 * Usage: npx tsx xiaoyuzhou.ts "<url>" --config skills/linkmind/config.json
 * Output: JSON to stdout
 */

import { fileURLToPath } from "node:url";
import type { XiaoyuzhouContent, HandlerError, ErrorCode } from "./types.js";
import { withRetry, isRetryableError } from "./retry.js"; // used in later tasks
import { loadConfig, parseConfigArg } from "./config.js"; // used in later tasks

const MOBILE_UA =
  "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) " +
  "AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148";

// ---------------------------------------------------------------------------
// URL parsing
// ---------------------------------------------------------------------------

export interface ParsedEpisodeUrl {
  episodeId: string;
  timestampSeconds: number | null;
}

/**
 * Parse a full xiaoyuzhoufm.com episode URL.
 * Handles: https://www.xiaoyuzhoufm.com/episode/{id}#ts={seconds}?s=...
 */
export function parseEpisodeUrl(url: string): ParsedEpisodeUrl {
  if (!url.includes("xiaoyuzhoufm.com")) {
    throw new Error(`不是小宇宙链接: ${url}`);
  }

  // Extract episode ID from path /episode/{id}
  const idMatch = url.match(/\/episode\/([\w]+)/i);
  if (!idMatch) {
    throw new Error(`无法从 URL 中提取 episode ID: ${url}`);
  }
  const episodeId = idMatch[1];

  // Extract timestamp from fragment #ts={seconds}
  // URL may look like: /episode/{id}#ts=1023?s=... (fragment before query)
  const tsMatch = url.match(/#ts=(\d+)/);
  const timestampSeconds = tsMatch ? parseInt(tsMatch[1], 10) : null;

  return { episodeId, timestampSeconds };
}

/**
 * Resolve a short link (xyzfm.link/s/xxx) by following HTTP redirect.
 * Returns the final URL (xiaoyuzhoufm.com/episode/...) with fragment preserved.
 *
 * Uses redirect: "manual" to capture the raw Location header, which includes
 * the URL fragment (#ts=...). fetch redirect:"follow" strips fragments from resp.url.
 */
export async function resolveShortLink(url: string): Promise<string> {
  const resp = await fetch(url, {
    method: "HEAD",
    redirect: "manual",
    headers: { "User-Agent": MOBILE_UA },
  });
  // Capture Location header to preserve the URL fragment (#ts=...)
  const location = resp.headers.get("location");
  return location ?? resp.url;
}

// ---------------------------------------------------------------------------
// Web page scraping (no auth needed)
// ---------------------------------------------------------------------------

const WEB_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36";
const APP_UA = "Xiaoyuzhou/2.105.1 (build:3386; iOS 26.4.0)";
const API_BASE = "https://api.xiaoyuzhoufm.com";

interface XyzPageEpisode {
  eid: string;
  title: string;
  pubDate: string;
  description: string;
  shownotes: string;
  duration: number;
  enclosure: { url: string };
  transcriptMediaId?: string | null;
  podcast: {
    title: string;
    author: string;
    image: { picUrl: string };
  };
}

/**
 * Fetch episode metadata by scraping the web page __NEXT_DATA__ JSON.
 * No authentication required.
 */
async function fetchEpisodePage(episodeId: string): Promise<XyzPageEpisode> {
  const url = `https://www.xiaoyuzhoufm.com/episode/${episodeId}`;
  const resp = await withRetry(
    () => fetch(url, { headers: { "User-Agent": WEB_UA } }),
    { shouldRetry: isRetryableError },
  );
  if (!resp.ok) {
    throw Object.assign(
      new Error(`小宇宙页面请求失败: HTTP ${resp.status}`),
      { httpStatus: resp.status },
    );
  }
  const html = await resp.text();
  const m = html.match(/<script id="__NEXT_DATA__"[^>]*>([\s\S]*?)<\/script>/);
  if (!m) {
    throw new Error("无法从页面提取 __NEXT_DATA__，页面结构可能已变更");
  }
  const data = JSON.parse(m[1]) as {
    props: { pageProps: { episode: XyzPageEpisode } };
  };
  const ep = data?.props?.pageProps?.episode;
  if (!ep?.eid) {
    throw new Error("__NEXT_DATA__ 中未找到 episode 数据");
  }
  return ep;
}

/**
 * Fetch transcript URL from Xiaoyuzhou API.
 * Requires x-jike-access-token. Returns null if not configured or not available.
 */
async function fetchTranscriptUrl(
  eid: string,
  mediaId: string,
  token: string,
): Promise<string | null> {
  try {
    const resp = await fetch(`${API_BASE}/v1/episode-transcript/get`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "User-Agent": APP_UA,
        "x-jike-access-token": token,
      },
      body: JSON.stringify({ eid, mediaId }),
    });
    if (!resp.ok) return null;
    const json = await resp.json() as { data?: { transcriptUrl?: string } };
    return json?.data?.transcriptUrl ?? null;
  } catch (e) {
    process.stderr.write(`[linkmind] 字幕 URL 获取失败（不影响主流程）: ${(e as Error).message}\n`);
    return null;
  }
}

/**
 * Fetch complete episode data for Xiaoyuzhou platform.
 * Scrapes web page for metadata, optionally fetches transcript URL.
 */
export async function fetchEpisodeData(
  episodeId: string,
  timestampSeconds: number | null,
  token: string | undefined,
): Promise<XiaoyuzhouContent> {
  const ep = await fetchEpisodePage(episodeId);

  const date = ep.pubDate
    ? new Date(ep.pubDate).toISOString().slice(0, 10)
    : new Date().toISOString().slice(0, 10);

  // Fetch transcript URL if token is configured and mediaId is available
  let subtitleUrl: string | null = null;
  if (token && ep.transcriptMediaId) {
    subtitleUrl = await fetchTranscriptUrl(ep.eid, ep.transcriptMediaId, token);
  }

  return {
    platform: "xiaoyuzhou",
    episodeId: ep.eid,
    title: ep.title ?? "",
    podcast: ep.podcast?.title ?? "",
    author: ep.podcast?.author ?? ep.podcast?.title ?? "",
    date,
    description: ep.description ?? "",
    text: ep.description ?? "",
    images: ep.podcast?.image?.picUrl ? [ep.podcast.image.picUrl] : [],
    videoUrl: null,
    audioUrl: ep.enclosure?.url ?? "",
    durationSeconds: ep.duration ?? 0,
    timestampSeconds,
    subtitleUrl,
    originalUrl: `https://www.xiaoyuzhoufm.com/episode/${episodeId}`,
    fetchedAt: new Date().toISOString(),
  } as XiaoyuzhouContent;
}

// ---------------------------------------------------------------------------
// Subtitle utilities
// ---------------------------------------------------------------------------

export interface SubtitleEntry {
  startSeconds: number;
  endSeconds: number;
  text: string;
}

/**
 * Parse SRT subtitle content into structured entries.
 * Handles both SRT (HH:MM:SS,mmm --> HH:MM:SS,mmm) and
 * WebVTT (HH:MM:SS.mmm --> HH:MM:SS.mmm) timestamp formats.
 */
export function parseSubtitleEntries(content: string): SubtitleEntry[] {
  if (!content.trim()) return [];

  const entries: SubtitleEntry[] = [];
  const blocks = content.trim().split(/\n\n+/);

  for (const block of blocks) {
    const lines = block.trim().split("\n").map((l) => l.trim()).filter(Boolean);
    if (lines.length < 2) continue;

    const tsLine = lines.find((l) => l.includes("-->"));
    if (!tsLine) continue;

    const tsMatch = tsLine.match(
      /(\d{1,2}):(\d{2}):(\d{2})[,.](\d+)\s*-->\s*(\d{1,2}):(\d{2}):(\d{2})[,.](\d+)/,
    );
    if (!tsMatch) continue;

    const toSeconds = (h: string, m: string, s: string) =>
      parseInt(h, 10) * 3600 + parseInt(m, 10) * 60 + parseInt(s, 10);

    const startSeconds = toSeconds(tsMatch[1], tsMatch[2], tsMatch[3]);
    const endSeconds = toSeconds(tsMatch[5], tsMatch[6], tsMatch[7]);

    const textLines = lines.filter(
      (l) => l !== tsLine && !/^\d+$/.test(l) && !l.startsWith("WEBVTT"),
    );
    const text = textLines.join(" ").trim();

    if (text) entries.push({ startSeconds, endSeconds, text });
  }

  return entries;
}

/**
 * Filter subtitle entries to those overlapping [startSec, endSec].
 * Pass null for both to return all entries.
 */
export function filterByTimeWindow(
  entries: SubtitleEntry[],
  startSec: number | null,
  endSec: number | null,
): SubtitleEntry[] {
  if (startSec === null && endSec === null) return entries;
  return entries.filter(
    (e) =>
      (startSec === null || e.endSeconds >= startSec) &&
      (endSec === null || e.startSeconds <= endSec),
  );
}

/**
 * Format subtitle entries as "[MM:SS] text" lines for Obsidian note.
 */
export function formatSubtitleSegment(entries: SubtitleEntry[]): string {
  return entries
    .map((e) => {
      const m = Math.floor(e.startSeconds / 60).toString().padStart(2, "0");
      const s = (e.startSeconds % 60).toString().padStart(2, "0");
      return `[${m}:${s}] ${e.text}`;
    })
    .join("\n");
}

/**
 * Download subtitle file and parse into entries.
 */
export async function downloadSubtitle(subtitleUrl: string): Promise<SubtitleEntry[]> {
  const resp = await withRetry(
    () => fetch(subtitleUrl, { headers: { "User-Agent": APP_UA } }),
    { shouldRetry: isRetryableError },
  );
  if (!resp.ok) {
    throw new Error(`字幕下载失败: HTTP ${resp.status}`);
  }
  const content = await resp.text();
  return parseSubtitleEntries(content);
}

// ---------------------------------------------------------------------------
// Error categorization
// ---------------------------------------------------------------------------

function categorizeError(e: unknown): { code: ErrorCode; details: string } {
  const msg = e instanceof Error ? e.message : String(e);
  const lower = msg.toLowerCase();
  const httpStatus = (e as any).httpStatus as number | undefined;

  if (httpStatus === 401 || httpStatus === 403)
    return { code: "AUTH", details: msg };
  if (httpStatus === 404)
    return { code: "NOT_FOUND", details: msg };
  if (
    lower.includes("timeout") ||
    lower.includes("fetch failed") ||
    lower.includes("econnreset") ||
    lower.includes("network")
  )
    return { code: "NETWORK", details: msg };
  if (lower.includes("无法解析") || lower.includes("parse"))
    return { code: "PARSE", details: msg };
  return { code: "UNKNOWN", details: msg };
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  const rawUrl = args[0];

  if (!rawUrl) {
    const err: HandlerError = {
      error: "用法: npx tsx xiaoyuzhou.ts <url> [--config <path>]",
    };
    console.log(JSON.stringify(err));
    process.exit(1);
  }

  try {
    // Load config (for x-jike-access-token)
    const configPath = parseConfigArg(process.argv);
    const token = configPath ? loadConfig(configPath).cookies?.xiaoyuzhou : undefined;

    // Resolve short link if needed
    const finalUrl = rawUrl.includes("xyzfm.link")
      ? await resolveShortLink(rawUrl)
      : rawUrl;

    // Parse episode ID and timestamp from URL
    const { episodeId, timestampSeconds } = parseEpisodeUrl(finalUrl);

    // Fetch episode metadata + optional transcript URL
    const content = await fetchEpisodeData(episodeId, timestampSeconds, token);
    console.log(JSON.stringify(content, null, 2));
  } catch (e) {
    const { code, details } = categorizeError(e);
    const err: HandlerError = {
      error: e instanceof Error ? e.message : String(e),
      code,
      details,
    };
    console.log(JSON.stringify(err, null, 2));
    process.exit(1);
  }
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  main();
}
