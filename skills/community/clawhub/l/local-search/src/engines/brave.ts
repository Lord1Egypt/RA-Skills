/**
 * Brave Search engine backend.
 *
 * Endpoint: https://search.brave.com/search?q=<query>&source=web
 *
 * No API key required. Brave has its own independent index (not Bing-powered
 * like DDG), which means:
 *   - Better handling of compound words and brand names
 *   - Better Chinese query understanding than Bing
 *   - Higher result quality on the first call
 *
 * BUT: Brave enforces aggressive rate limiting (~1 request per few seconds).
 * After the first call, subsequent calls within a short window return 429.
 * The auto-fallback chain handles this — if Brave 429s, we fall through to
 * DDG → Bing.
 *
 * Parser: Brave uses SvelteKit with server-side rendering. Results are in
 * <a href="https://..."> tags within snippet containers. We extract all
 * external links with meaningful text, then filter out Brave's own chrome.
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

export const braveEngine: SearchEngine = {
  id: "brave",
  display: "Brave Search",
  async search(query, opts) {
    const { num, recency_days, timeoutMs, userAgent, locale, fetchImpl } = opts;

    const url = new URL("https://search.brave.com/search");
    url.searchParams.set("q", query);
    url.searchParams.set("source", "web");
    // Brave locale: accepts country= and language= params.
    const localeNorm = locale.trim();
    const country = localeNorm.split("-")[1]?.toLowerCase() || "us";
    const lang = localeNorm.split("-")[0] || "en";
    url.searchParams.set("country", country);
    url.searchParams.set("language", lang);
    // Brave freshness filter: "pd" (past day), "pw" (past week),
    // "pm" (past month), "py" (past year).
    if (recency_days && recency_days > 0) {
      if (recency_days <= 1) url.searchParams.set("tf", "pd");
      else if (recency_days <= 7) url.searchParams.set("tf", "pw");
      else if (recency_days <= 30) url.searchParams.set("tf", "pm");
      else url.searchParams.set("tf", "py");
    }

    let html = "";
    let lastError: Error | null = null;
    // Brave rate-limits aggressively (429 after ~1 req per few seconds).
    // We do NOT retry on 429 — the rate limit window is ~5-10s, so retrying
    // after 2s just wastes time and delays the fallback to DDG/Bing. Better
    // to fail fast and let the auto chain move on.
    try {
      const headers = defaultHeaders(userAgent);
      headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8";
      headers["Accept-Language"] = `${localeNorm},${lang};q=0.9,en;q=0.5`;
      headers["Sec-GPC"] = "1";
      headers["DNT"] = "1";
      headers["Upgrade-Insecure-Requests"] = "1";
      html = await fetchHtml(url.toString(), {
        fetchImpl,
        headers,
        timeoutMs,
      });
      // Check for 429 body (Brave sometimes returns 200 with a short page).
      if (html.length < 50000 && /rate.?limit|too many requests|429/i.test(html)) {
        throw new SearchEngineError("brave", "Rate limited (429). Try again in a few seconds.");
      }
    } catch (err) {
      throw new SearchEngineError("brave", `Request failed: ${(err as Error).message}`, err);
    }

    if (!html || html.length < 5000) {
      throw new SearchEngineError("brave", "Empty or near-empty response body");
    }

    let results: SearchFunctionResultItem[];
    try {
      const cheerio = await loadCheerio();
      const $ = cheerio.load(html);
      const items: SearchFunctionResultItem[] = [];
      const seenUrls = new Set<string>();

      // Brave's result structure (SvelteKit SSR):
      //   <a href="https://..." class="result-header ...">
      //   <span class="snippet-title">...</span>
      //   <div class="snippet-description">...</div>
      //
      // But class names vary. The stable signal is: external <a> tags with
      // meaningful text that aren't Brave's own chrome. We scan all <a> tags
      // with http(s) href, extract text + nearby snippet.

      $("a[href]").each((i, el) => {
        if (items.length >= num) return;
        const $a = $(el);
        const href = $a.attr("href") || "";
        if (!href) return;
        if (!/^https?:\/\//i.test(href)) return;
        // Skip Brave's own domains and tracking redirects.
        if (/brave\.com|search\.brave|cdn\.search\.brave|imgs\.search\.brave/i.test(href)) return;
        // Skip obvious navigation / footer links.
        const text = cleanText($a.text());
        if (!text || text.length < 8 || text.length > 250) return;
        // Skip if it looks like a button label or nav item.
        if (/^(search|home|about|login|sign|menu|next|previous|more)$/i.test(text)) return;

        // Dedupe by URL.
        if (seenUrls.has(href)) return;
        seenUrls.add(href);

        // Try to find a snippet near this link.
        // Brave wraps results in containers; walk up to find snippet text.
        const $parent = $a.closest("div, article, section");
        let snippet = "";
        if ($parent.length) {
          // Look for snippet-description, snippet-content, or just longest <p>.
          const $snippet = $parent.find(".snippet-description, .snippet-content, [class*='snippet']").first();
          if ($snippet.length) {
            snippet = cleanText($snippet.text());
          } else {
            // Fallback: any <p> in the parent.
            const $p = $parent.find("p").first();
            if ($p.length) snippet = cleanText($p.text());
          }
        }

        const item = makeItem({
          url: href,
          name: text,
          snippet: snippet || "(no snippet)",
          rank: items.length + 1,
          source_engine: "brave",
        });
        item.score = scoreItem(item, query);
        if (isLikelyIrrelevant(item, query)) return;
        // Additional filter: skip if the URL is clearly a search/aggregator page.
        if (/google\.com\/search|bing\.com\/search|duckduckgo\.com\//i.test(href)) return;
        items.push(item);
      });

      results = items;
    } catch (err) {
      throw new SearchEngineError("brave", `Parse failed: ${(err as Error).message}`, err);
    }

    if (results.length === 0) {
      throw new SearchEngineError(
        "brave",
        "No results parsed (page may be rate-limited or require JS rendering)"
      );
    }
    return results;
  },
};
