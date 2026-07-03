/**
 * DuckDuckGo HTML backend.
 *
 * Endpoint: https://html.duckduckgo.com/html/?q=<query>   (GET)
 *
 * This is the "lite" non-JS page that returns parseable HTML without
 * running their SPA. No API key required. Subject to rough rate limits —
 * if you hammer it, you'll start getting empty result sets or 202s.
 *
 * Implementation note: the POST form variant of this endpoint silently
 * returns an empty "lite" page when called from datacenter IPs; the GET
 * variant is markedly more reliable and is what we use here.
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

export const duckduckgoEngine: SearchEngine = {
  id: "duckduckgo",
  display: "DuckDuckGo (HTML)",
  async search(query, opts) {
    const { num, recency_days, timeoutMs, userAgent, locale, fetchImpl } = opts;

    // Build the GET URL. DDG accepts `df=d<N>` as a date filter for
    // "past N days" — much finer-grained than Bing/Google's day/week/month
    // buckets, which is why DDG is our primary engine despite the rougher
    // rate limiting.
    //
    // DDG largely ignores locale params; `kl=<country>` selects the region
    // (e.g. "us-en" = US-English, "cn-zh" = China-Chinese) but in practice
    // DDG returns the same English-centric SERP regardless. We pass it for
    // completeness; do not rely on it for strict locale enforcement.
    const url = new URL("https://html.duckduckgo.com/html/");
    url.searchParams.set("q", query);
    const klRegion = locale.split("-")[1]?.toLowerCase() || "us";
    const klLang = locale.split("-")[0] || "en";
    url.searchParams.set("kl", `${klRegion}-${klLang}`);
    if (recency_days && recency_days > 0) {
      url.searchParams.set("df", `d${recency_days}`);
    }

    let html: string;
    try {
      html = await fetchHtml(url.toString(), {
        fetchImpl,
        headers: {
          ...defaultHeaders(userAgent),
          Referer: "https://duckduckgo.com/",
        },
        timeoutMs,
        method: "GET",
      });
    } catch (err) {
      throw new SearchEngineError("duckduckgo", `Request failed: ${(err as Error).message}`, err);
    }

    if (!html || html.length < 200) {
      throw new SearchEngineError("duckduckgo", "Empty or near-empty response body");
    }

    let results: SearchFunctionResultItem[];
    try {
      const cheerio = await loadCheerio();
      const $ = cheerio.load(html);
      const items: SearchFunctionResultItem[] = [];

      // DDG's HTML uses `.result` blocks; each contains `.result__a` (link),
      // `.result__snippet`, and `.result__title`. Older layouts use
      // `.web-result` instead — we cover both with a union selector.
      const blocks = $(
        ".result, .web-result, .results_links, .results_links_deep"
      ).toArray();

      blocks.forEach((block, i) => {
        if (items.length >= num) return;
        const $block = $(block);

        // Skip ad units. DDG marks them with `.result--ad` /
        // `.result--ad--small` classes, and the link's href always points
        // to a `duckduckgo.com/y.js` click-tracker rather than a `/l/?uddg=`
        // organic redirect. We check both signals defensively.
        const blockClass = ($block.attr("class") || "").toLowerCase();
        if (/\bresult--ad\b|\bresult--ad--/.test(blockClass)) return;

        const $link = $block.find(".result__a").first().length
          ? $block.find(".result__a").first()
          : $block.find("a.result-link").first();

        const href = $link.attr("href") || "";
        if (!href) return;

        // DDG wraps outgoing links as //duckduckgo.com/l/?uddg=<encoded>.
        // Ad click-trackers use /y.js — those should never decode to a real
        // destination and `decodeDdgRedirect` will return "" for them.
        const realUrl = decodeDdgRedirect(href);
        if (!realUrl) return;
        // Defensive: also skip anything that still points back into DDG.
        if (/duckduckgo\.com\/(?:y\.js|ad|spice)/i.test(realUrl)) return;

        const title = cleanText($link.text()) || cleanText($block.find(".result__title").text());
        if (!title) return;

        // DDG wraps the snippet in `.result__snippet`, but it sometimes
        // contains nested `<a>` links to "related searches". We extract
        // just the first text node to avoid noise.
        const $snippet = $block.find(".result__snippet").first();
        // Strip nested links' text (related-search chips) before reading.
        $snippet.find("a").remove();
        const snippet = cleanText($snippet.text());

        const rawHtml = $block.find(".result__snippet").html() || "";

        const item = makeItem({
          url: realUrl,
          name: title,
          snippet,
          rank: i + 1,
          source_engine: "duckduckgo",
          raw_html: rawHtml || undefined,
        });
        item.score = scoreItem(item, query);
        // Defensive: drop search-redirect URLs and empty-title junk.
        if (isLikelyIrrelevant(item, query)) return;
        items.push(item);
      });

      results = items;
    } catch (err) {
      throw new SearchEngineError("duckduckgo", `Parse failed: ${(err as Error).message}`, err);
    }

    if (results.length === 0) {
      // DDG will silently return a "no results" page when rate-limited; treat
      // that as a soft failure so `auto` fallback can kick in.
      throw new SearchEngineError(
        "duckduckgo",
        "No results parsed (page may be rate-limited or blocked)"
      );
    }
    return results;
  },
};

/**
 * DDG wraps outgoing URLs in a redirector: `//duckduckgo.com/l/?uddg=<encoded>&rut=...`
 * Some installs also return plain `https://...` links. Decode defensively.
 */
function decodeDdgRedirect(href: string): string {
  if (!href) return "";
  // Protocol-relative → https
  let h = href.trim();
  if (h.startsWith("//")) h = "https:" + h;

  // Plain URL already
  if (/^https?:\/\//i.test(h) && !h.includes("duckduckgo.com/l/")) {
    return h;
  }

  try {
    const u = new URL(h);
    if (u.pathname.startsWith("/l/")) {
      const target = u.searchParams.get("uddg");
      if (target) return target;
    }
    // Not a redirect — give up on this link.
    return "";
  } catch {
    return "";
  }
}
