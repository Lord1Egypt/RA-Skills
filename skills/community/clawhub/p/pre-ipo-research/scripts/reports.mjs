import { readFile } from "node:fs/promises";
import { readPublic } from "./http.mjs";

function decode(value) {
  const entities = { amp: "&", lt: "<", gt: ">", quot: '"', apos: "'", nbsp: " ", ndash: "–", mdash: "—", hellip: "…", times: "×", rarr: "→" };
  return value.replace(/&(#x[\da-f]+|#\d+|[a-z]+);/gi, (match, key) => {
    if (key.startsWith("#")) {
      const code = key[1].toLowerCase() === "x" ? parseInt(key.slice(2), 16) : Number(key.slice(1));
      return code > 0 && code <= 0x10ffff ? String.fromCodePoint(code) : match;
    }
    return entities[key] ?? match;
  });
}

function plain(html) {
  return decode(html.replace(/<[^>]*>/g, "")).replace(/[ \t\r]+/g, " ").replace(/ *\n */g, "\n").replace(/\n{3,}/g, "\n\n").trim();
}

function hrefAttribute(attributes) {
  const match = attributes.match(/\bhref\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>]+))/i);
  return match ? decode(match[1] ?? match[2] ?? match[3]) : null;
}

export function allowedReportUrl(href, base) {
  const url = new URL(href, base + "/");
  if (url.origin !== new URL(base).origin || url.username || url.password || url.search || url.hash ||
      !/^\/reports\/[a-z0-9-]+-investment-research\.html$/.test(url.pathname)) {
    throw new Error("Report link is not an approved same-site static report.");
  }
  return url.href;
}

export function parseReport(html, reportUrl) {
  const safe = html.replace(/<!--[\s\S]*?-->/g, "").replace(/<(script|style|noscript)\b[^>]*>[\s\S]*?<\/\1\s*>/gi, "");
  const title = plain(safe.match(/<title\b[^>]*>([\s\S]*?)<\/title>/i)?.[1] ?? "");
  const body = safe.match(/<body\b[^>]*>([\s\S]*?)<\/body>/i)?.[1] ?? safe;
  const sources = [];
  const seen = new Set();
  const linked = body.replace(/<a\b([^>]*)>([\s\S]*?)<\/a>/gi, (_, attributes, inner) => {
    const href = hrefAttribute(attributes);
    const label = plain(inner);
    if (!href) return label;
    let url;
    try { url = new URL(href, reportUrl); } catch { return label; }
    if (!["http:", "https:"].includes(url.protocol) || url.username || url.password) return label;
    if (!href.startsWith("#") && !seen.has(url.href)) {
      seen.add(url.href);
      const kind = url.hostname === "research.contrary.com" ? "contrary"
        : url.hostname === "sacra.com" ? "sacra"
        : url.origin === new URL(reportUrl).origin ? "observer" : "external";
      sources.push({ url: url.href, label, kind });
    }
    return label + " (" + url.href + ")";
  });
  const contentText = plain(linked
    .replace(/<br\b[^>]*>/gi, "\n")
    .replace(/<\/(?:p|div|section|article|h[1-6]|li|tr|header|footer|ul|ol|table)>/gi, "\n\n")
    .replace(/<\/(?:td|th)>/gi, " | "));
  if (!title || contentText.length < 80 || !/报告截至|静态版本/.test(contentText)) {
    throw new Error("Page is not a recognized published research report.");
  }
  return {
    title,
    asOf: contentText.match(/报告截至[：:]\s*(\d{4}-\d{2}-\d{2})/)?.[1] ?? null,
    version: contentText.match(/静态版本[：:]\s*(v[\d.]+)/i)?.[1] ?? null,
    contentText,
    sources,
  };
}

export async function reportIndex() {
  return JSON.parse(await readFile(new URL("../data/report-index.json", import.meta.url), "utf8"));
}

export async function loadReport(platform, assetId, detail, base, options) {
  const index = platform === "jarsy" ? await reportIndex() : null;
  const registered = index?.reports[assetId.trim().toUpperCase()];
  const href = detail.reportHref ?? registered?.href;
  const identity = { platform, assetId };
  if (!href) return { ...identity, status: "unavailable", reportUrl: null, message: "暂无已登记研报；未猜测链接。" };
  let reportUrl;
  try {
    reportUrl = allowedReportUrl(href, base);
    const html = await readPublic(reportUrl, { ...options, html: true });
    return { ...identity, status: "success", reportUrl, ...parseReport(html, reportUrl) };
  } catch (error) {
    return { ...identity, status: "error", reportUrl: reportUrl ?? null, error: error.message };
  }
}
