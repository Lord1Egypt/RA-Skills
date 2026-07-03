/**
 * Google HTML backend.
 *
 * Endpoint: https://www.google.com/search?q=<query>&num=<num>
 *
 * No API key required, BUT Google is the most aggressive at blocking scrapers.
 * Expect intermittent 429s and consent-page redirects (especially from EU
 * IPs). This engine is therefore positioned as the LAST fallback in the
 * `auto` chain.
 *
 * The parser targets stable-ish class names from the 2023–2024 SERP layout:
 *   - `.g` containers (organic results)
 *   - `h3` inside `.g` for the title
 *   - parent `<a>` of the `h3` for the URL
 *   - `.VwiC3b` / `[style*="-webkit-line-clamp"]` for the snippet
 *
 * If Google ships a layout change, this file is the most likely to break.
 */
import type {
  SearchEngine,
  SearchFunctionResultItem,
} from "../types.js";
import { SearchEngineError } from "../types.js";
import {
  cleanText,
  defaultHeaders,
  fetchHtml,
  loadCheerio,
  makeItem,
  scoreItem,
} from "./_shared.js";

export const googleEngine: SearchEngine = {
  id: "google",
  display: "Google (HTML)",
  async search(query, opts) {
    const { num, recency_days, timeoutMs, userAgent, locale, fetchImpl } = opts;

    const url = new URL("https://www.google.com/search");
    url.searchParams.set("q", query);
    url.searchParams.set("num", String(Math.max(num, 10)));
    // Google locale: `hl` = UI language, `gl` = geo. Both default from
    // the requested BCP-47 locale.
    const localeNorm = locale.trim();
    const lang = localeNorm.split("-")[0] || "en";
    const country = localeNorm.split("-")[1]?.toUpperCase() || "US";
    url.searchParams.set("hl", localeNorm);
    url.searchParams.set("gl", country.toLowerCase());
    // Google date filter: `qdr:d` (past day), `qdr:w` (past week),
    // `qdr:m` (past month), `qdr:y` (past year). There is no native
    // "past N days" — we approximate.
    if (recency_days && recency_days > 0) {
      let qdr = "w";
      if (recency_days <= 1) qdr = "d";
      else if (recency_days <= 30) qdr = "m";
      else qdr = "y";
      url.searchParams.set("tbs", `qdr:${qdr}`);
    }

    let html: string;
    try {
      html = await fetchHtml(url.toString(), {
        fetchImpl,
        headers: {
          ...defaultHeaders(userAgent),
          // Picking an Accept-Language that matches the requested locale
          // reduces the chance of being bounced to a consent.google.com
          // page (especially for EU locales).
          "Accept-Language": `${localeNorm},${lang};q=0.9,en;q=0.5`,
        },
        timeoutMs,
      });
    } catch (err) {
      throw new SearchEngineError("google", `Request failed: ${(err as Error).message}`, err);
    }

    if (!html || html.length < 200) {
      throw new SearchEngineError("google", "Empty or near-empty response body");
    }

    // Cheap consent-redirect detector.
    if (/consent\.google\.com|Sorry\/Captcha|unusual traffic/i.test(html)) {
      throw new SearchEngineError(
        "google",
        "Google returned a consent / captcha page (likely blocked). Try another engine."
      );
    }

    let results: SearchFunctionResultItem[];
    try {
      const cheerio = await loadCheerio();
      const $ = cheerio.load(html);
      const items: SearchFunctionResultItem[] = [];

      // Modern Google SERP: each organic result is a `<div class="g">` whose
      // first `<a>` carries the href and whose `<h3>` carries the title.
      // We skip entries whose href is `/url?...` (Google's redirect) — those
      // are usually "People also ask" / inline modules, not real results.
      $('div.g, div.Gx5Zad').each((i, el) => {
        if (items.length >= num) return;
        const $el = $(el);

        const $h3 = $el.find("h3").first();
        if (!$h3.length) return;
        const title = cleanText($h3.text());
        if (!title) return;

        // Walk up to find the anchor that actually has an href.
        const $link = $h3.parent('a[href]').first();
        const href = $link.attr("href");
        if (!href || !/^https?:\/\//i.test(href)) return;
        // Skip Google's own internal links (calendar, maps deep links, etc.)
        if (/google\.com\/(?:maps|calendar|search|url\?)/i.test(href)) return;

        // Snippet: Google has rotated class names several times; we try a
        // list of candidates and take the first non-empty match.
        const snippet = cleanText(
          $el.find(".VwiC3b").text() ||
            $el.find('[style*="-webkit-line-clamp"]').text() ||
            $el.find(".IsZvec").text() ||
            $el.find(".s3v9rd").text()
        );

        const rawHtml = $el.find(".VwiC3b").html() || "";

        const item = makeItem({
          url: href,
          name: title,
          snippet,
          rank: i + 1,
          source_engine: "google",
          raw_html: rawHtml || undefined,
        });
        item.score = scoreItem(item, query);
        items.push(item);
      });

      results = items;
    } catch (err) {
      throw new SearchEngineError("google", `Parse failed: ${(err as Error).message}`, err);
    }

    if (results.length === 0) {
      throw new SearchEngineError(
        "google",
        "No results parsed (page layout may have changed or results were blocked)"
      );
    }
    return results;
  },
};
