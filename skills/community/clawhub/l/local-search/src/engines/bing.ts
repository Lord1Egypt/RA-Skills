/**
 * Bing HTML backend.
 *
 * Endpoint: https://www.bing.com/search?q=<query>&count=<num>
 *
 * No API key required. Bing's HTML is relatively stable and easy to parse.
 * Add `&ensearch=1&setmkt=en-US&setlang=en-US` to force the en-US locale,
 * otherwise Bing may serve a localized variant based on the caller's IP
 * (which still parses, but titles/snippets may be non-English).
 *
 * Bing wraps outgoing URLs in a tracking redirector (`/ck/a?...&u=a1<base64>`).
 * We decode that base64 payload to recover the real destination URL.
 */
import type {
  SearchEngine,
  SearchFunctionResultItem,
} from "../types.js";
import { SearchEngineError } from "../types.js";
import {
  DEFAULT_USER_AGENT,
  cleanText,
  defaultHeaders,
  fetchHtml,
  isLikelyIrrelevant,
  loadCheerio,
  makeItem,
  scoreItem,
} from "./_shared.js";

export const bingEngine: SearchEngine = {
  id: "bing",
  display: "Bing (HTML)",
  async search(query, opts) {
    const { num, recency_days, timeoutMs, userAgent, locale, fetchImpl } = opts;

    const url = new URL("https://www.bing.com/search");
    url.searchParams.set("q", query);
    url.searchParams.set("count", String(Math.max(num, 10)));
    // Locale forcing strategy:
    //
    //   - `cc=<country>` + `mkt=<locale>` + `setlang=<locale>` are the
    //     standard Bing locale params. They work fine on their own.
    //   - `ensearch=1` is a special flag that *forces the English SERP*
    //     regardless of geo-IP. This is essential for English queries from
    //     non-US IPs (otherwise Bing localizes to the IP's country).
    //     BUT it is POISON for non-English queries — Bing's English SERP
    //     misinterprets CJK / Cyrillic / etc. queries and returns totally
    //     irrelevant results (e.g., "巴黎奥运会" returns Microsoft Teams
    //     error pages).
    //   - Therefore: only set `ensearch=1` when the locale is English.
    //     For other locales, rely on `cc` + `mkt` + `setlang` alone.
    const localeNorm = locale.trim();
    const country = localeNorm.split("-")[1]?.toUpperCase() || "US";
    const isEnglishLocale = localeNorm.toLowerCase().startsWith("en-");
    url.searchParams.set("cc", country);
    url.searchParams.set("mkt", localeNorm);
    url.searchParams.set("setlang", localeNorm);
    if (isEnglishLocale) {
      url.searchParams.set("ensearch", "1");
    }
    url.searchParams.set("form", "QBLH");
    // Bing freshness filter: "d1" = past day, "w1" = past week, "m1" = past month.
    // Bing's URL API does not accept arbitrary N days; we fall back to
    // `w1`/`m1` buckets otherwise.
    if (recency_days && recency_days > 0) {
      if (recency_days <= 1) url.searchParams.set("freshness", "d1");
      else if (recency_days <= 7) url.searchParams.set("freshness", "w1");
      else url.searchParams.set("freshness", "m1");
    }

    let html: string;
    try {
      // Force Accept-Language to match the requested locale. This header
      // is the second-most-important locale signal after `cc`/`mkt` —
      // without it, Bing may still serve a localized page to match the
      // geo of the requester's IP.
      const headers = defaultHeaders(userAgent);
      headers["Accept-Language"] = `${localeNorm},${localeNorm.split("-")[0]};q=0.9,en;q=0.5`;
      // SearXNG-derived header set: DNT + Sec-GPC + Cache-Control make
      // the request look more like a privacy-conscious browser, which
      // seems to reduce Bing's bot heuristic score.
      headers["DNT"] = "1";
      headers["Sec-GPC"] = "1";
      headers["Cache-Control"] = "max-age=0";

      // deedy5's locale cookie trick: set _EDGE_CD and _EDGE_S to lock
      // the locale at the cookie layer. This is more reliable than URL
      // params alone — Bing reads these cookies before processing the
      // query string, so they override geo-IP localization.
      const lang = localeNorm.split("-")[0] || "en";
      const countryLower = country.toLowerCase();
      const edgeCookies = `_EDGE_CD=m=${lang}-${countryLower}&u=${lang}-${countryLower}; _EDGE_S=mkt=${localeNorm}&ui=${localeNorm}`;
      headers["Cookie"] = edgeCookies;

      html = await fetchHtml(url.toString(), {
        fetchImpl,
        headers,
        timeoutMs,
      });
    } catch (err) {
      throw new SearchEngineError("bing", `Request failed: ${(err as Error).message}`, err);
    }

    if (!html || html.length < 200) {
      throw new SearchEngineError("bing", "Empty or near-empty response body");
    }

    let results: SearchFunctionResultItem[];
    try {
      const cheerio = await loadCheerio();
      const $ = cheerio.load(html);
      const items: SearchFunctionResultItem[] = [];

      // Bing's main organic results live in `<li class="b_algo">`.
      $("li.b_algo").each((i, el) => {
        if (items.length >= num) return;
        const $el = $(el);

        const $link = $el.find("h2 a").first();
        const rawHref = $link.attr("href") || "";
        if (!rawHref) return;

        // Bing wraps outbound URLs in /ck/a?...&u=a1<base64>. Decode it.
        const realUrl = decodeBingRedirect(rawHref);
        if (!realUrl) return;

        const title = cleanText($link.text());
        if (!title) return;

        // Snippet: Bing keeps it under `.b_caption p` (sometimes `.b_lineclamp*`).
        // Do NOT use `.b_factrow` — that's the URL breadcrumb, not a snippet
        // (e.g., "en.wikipedia.org › wiki › Machine"), and including it was
        // polluting the `snippet` field with URL paths.
        //
        // SearXNG finding: Bing injects a decorative `<span class="algoSlug_icon">`
        // (usually a `›`-style bullet) into the snippet `<p>`. Strip it before
        // reading text, or it shows up as a leading glyph in the snippet.
        const $snippetEl = $el.find(".b_caption p").first().length
          ? $el.find(".b_caption p").first()
          : $el.find(".b_lineclamp4, .b_lineclamp3, .b_lineclamp2").first();
        $snippetEl.find("span.algoSlug_icon").remove();
        const snippet = cleanText($snippetEl.text());
        const rawHtml = $snippetEl.html() || "";

        const item = makeItem({
          url: realUrl,
          name: title,
          snippet,
          rank: i + 1,
          source_engine: "bing",
          raw_html: rawHtml || undefined,
        });

        // Bing sometimes embeds a publish date in `.news_dt`. Strict pattern:
        // accept only strings that look like a date or relative time, and
        // reject anything containing URL characters (those are breadcrumbs
        // leaking in from `.b_attribution cite`).
        const dateText = cleanText($el.find(".news_dt").first().text());
        if (
          dateText &&
          !/[\/<>]/.test(dateText) &&
          !dateText.includes("http") &&
          /\d{4}|hour|day|minute|second|ago|年|月|日/i.test(dateText)
        ) {
          item.date = dateText;
        }

        item.score = scoreItem(item, query);
        // Defensive: drop obvious garbage (search-redirect URLs, empty titles).
        if (isLikelyIrrelevant(item, query)) return;
        items.push(item);
      });

      results = items;
    } catch (err) {
      throw new SearchEngineError("bing", `Parse failed: ${(err as Error).message}`, err);
    }

    if (results.length === 0) {
      throw new SearchEngineError("bing", "No results parsed (page may be blocked or rate-limited)");
    }
    return results;
  },
};

/**
 * Bing wraps outbound URLs in a tracking redirector:
 *   https://www.bing.com/ck/a?!&&p=...&u=a1<base64>&ntb=1
 *
 * The `u` parameter holds the real destination URL, base64-encoded with a
 * leading `a1` marker and using `_*` instead of `+/` (URL-safe variant).
 * Returns "" if the input doesn't look like a Bing redirect — in which
 * case callers should treat the raw href as the URL.
 */
function decodeBingRedirect(href: string): string {
  if (!href) return "";

  // Plain http(s) URL — already the real destination.
  if (/^https?:\/\//i.test(href) && !href.includes("bing.com/ck/a")) {
    return href;
  }

  try {
    const u = new URL(href, "https://www.bing.com/");
    if (!u.pathname.startsWith("/ck/a")) return "";
    const raw = u.searchParams.get("u");
    if (!raw) return "";

    // Strip the leading "a1" marker.
    const b64 = raw.startsWith("a1") ? raw.slice(2) : raw;
    // Bing uses URL-safe base64: replace _ with / and * with +.
    const std = b64.replace(/_/g, "/").replace(/\*/g, "+");
    // Pad to a multiple of 4.
    const padded = std + "=".repeat((4 - (std.length % 4)) % 4);
    const decoded = Buffer.from(padded, "base64").toString("utf8");
    if (/^https?:\/\//i.test(decoded)) return decoded;
    return "";
  } catch {
    return "";
  }
}

// Re-export for engine registry; not used here but kept for parity.
export const _defaultUserAgent = DEFAULT_USER_AGENT;
