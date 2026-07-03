/**
 * Shared helpers used by every engine backend.
 *
 * Only Node's built-in `fetch` (Node 18+) and a couple of small utilities.
 * `cheerio` is loaded lazily so that environments without it still get a
 * clean import graph for the SDK types.
 */
import type { SearchFunctionResultItem, SearchEngineId } from "../types.js";

let cheerioPromise: Promise<typeof import("cheerio")> | null = null;

/** Lazy-load cheerio (keeps `import` cheap for callers who only need types). */
export async function loadCheerio(): Promise<typeof import("cheerio")> {
  if (!cheerioPromise) {
    cheerioPromise = import("cheerio").catch((err) => {
      throw new Error(
        "Required dependency 'cheerio' is not installed. Run `npm install cheerio` (or `bun add cheerio`)."
      );
    });
  }
  return cheerioPromise;
}

/** Default User-Agent — looks like a normal browser to most engines. */
export const DEFAULT_USER_AGENT =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " +
  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36";

/** Standard browser-ish headers, override-able per call. */
export function defaultHeaders(userAgent: string): Record<string, string> {
  return {
    "User-Agent": userAgent,
    "Accept":
      "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
  };
}

/** Tiny fetch-with-timeout wrapper. Aborts via `AbortController`. */
export async function fetchHtml(
  url: string,
  opts: {
    fetchImpl: typeof fetch;
    headers: Record<string, string>;
    timeoutMs: number;
    method?: "GET" | "POST";
    body?: string;
  }
): Promise<string> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), opts.timeoutMs);
  try {
    const res = await opts.fetchImpl(url, {
      method: opts.method ?? "GET",
      headers: opts.headers,
      body: opts.body,
      signal: controller.signal,
      redirect: "follow",
    });
    if (!res.ok) {
      throw new Error(`HTTP ${res.status} ${res.statusText} — ${url}`);
    }
    // `res.text()` will decode based on Content-Type charset; good enough for
    // the major search engines which all return utf-8.
    return await res.text();
  } finally {
    clearTimeout(timer);
  }
}

/** Extract the host (registrable domain) from a URL string, defensively. */
export function hostOf(url: string): string {
  try {
    return new URL(url).hostname;
  } catch {
    // Fallback: crude host extraction. Useful when engines return URLs that
    // are not strictly valid (rare, but happens with DDG redirects).
    const m = url.match(/^https?:\/\/([^/]+)/i);
    return m ? m[1] : "";
  }
}

/** Build a Google S2-style favicon URL for a host. */
export function faviconForHost(host: string): string {
  if (!host) return "";
  return `https://www.google.com/s2/favicons?sz=64&domain=${encodeURIComponent(host)}`;
}

/** Strip HTML tags + collapse whitespace from a cheerio selection / string. */
export function cleanText(input: string | undefined | null): string {
  if (!input) return "";
  return input
    .replace(/\s+/g, " ")
    .replace(/<[^>]*>/g, "")
    .trim();
}

/** Build a `SearchFunctionResultItem` with all the cross-engine defaults filled in. */
export function makeItem(
  partial: Pick<
    SearchFunctionResultItem,
    "url" | "name" | "snippet" | "rank" | "source_engine"
  > & { raw_html?: string; date?: string }
): SearchFunctionResultItem {
  const host = hostOf(partial.url);
  return {
    url: partial.url,
    name: partial.name,
    snippet: partial.snippet,
    host_name: host,
    rank: partial.rank,
    date: partial.date ?? "N/A",
    favicon: faviconForHost(host),
    source_engine: partial.source_engine,
    raw_html: partial.raw_html,
  };
}

/** Convenience: assign a heuristic 0–100 score based on title/snippet length & rank. */
export function scoreItem(item: SearchFunctionResultItem, query: string): number {
  let score = 50;
  if (item.name && item.name.length > 10) score += 10;
  if (item.snippet && item.snippet.length > 50) score += 15;
  if (item.snippet && item.snippet.length > 150) score += 5;
  // Higher rank (== lower position) → small penalty.
  score -= Math.min(20, Math.max(0, item.rank - 1) * 2);
  // Bonus if the query appears in the title or snippet.
  const q = query.trim().toLowerCase();
  if (q) {
    const name = item.name.toLowerCase();
    const snip = item.snippet.toLowerCase();
    const terms = q.split(/\s+/).filter((t) => t.length > 1);
    let hits = 0;
    for (const t of terms) {
      if (name.includes(t) || snip.includes(t)) hits++;
    }
    score += Math.min(20, hits * 5);
  }
  return Math.max(0, Math.min(100, score));
}

/**
 * Heuristic language detection from a query string.
 * Returns a BCP-47 locale tag.
 *
 * Uses Unicode block ranges to detect the dominant script:
 * - CJK Unified Ideographs → "zh-CN" (covers Chinese; JP/KR queries usually
 *   also contain kana/hangul which we check first)
 * - Hiragana / Katakana → "ja-JP"
 * - Hangul → "ko-KR"
 * - Cyrillic → "ru-RU"
 * - Arabic → "ar-SA"
 * - Thai → "th-TH"
 * - Hebrew → "he-IL"
 * - Greek → "el-GR"
 * - Default (Latin / mixed / empty) → "en-US"
 *
 * This is intentionally simple — we only need to pick a reasonable locale
 * for the search engine, not do real NLP. If the user explicitly passes
 * `locale` in SearchOptions, that always wins (see `resolveOptions`).
 */
export function detectLocale(query: string): string {
  if (!query) return "en-US";
  // Tally characters per script.
  const counts = { cjk: 0, hira: 0, kata: 0, hangul: 0, cyrillic: 0, arabic: 0, thai: 0, hebrew: 0, greek: 0, latin: 0 };
  for (const ch of query) {
    const cp = ch.codePointAt(0)!;
    if (cp >= 0x3040 && cp <= 0x309f) counts.hira++;
    else if (cp >= 0x30a0 && cp <= 0x30ff) counts.kata++;
    else if (cp >= 0xac00 && cp <= 0xd7af) counts.hangul++;
    else if (cp >= 0x4e00 && cp <= 0x9fff) counts.cjk++;
    else if (cp >= 0x0400 && cp <= 0x04ff) counts.cyrillic++;
    else if (cp >= 0x0600 && cp <= 0x06ff) counts.arabic++;
    else if (cp >= 0x0e00 && cp <= 0x0e7f) counts.thai++;
    else if (cp >= 0x0590 && cp <= 0x05ff) counts.hebrew++;
    else if (cp >= 0x0370 && cp <= 0x03ff) counts.greek++;
    else if (cp >= 0x0041 && cp <= 0x024f) counts.latin++;
  }
  // Japanese and Korean have unique scripts (kana, hangul) that Chinese
  // doesn't. They usually appear alongside CJK ideographs (because both
  // languages use kanji/hanja to varying degrees), so we check them FIRST
  // — even a single kana/hangul character means it's Japanese/Korean,
  // regardless of how many CJK ideographs there are.
  if (counts.hira > 0 || counts.kata > 0) return "ja-JP";
  if (counts.hangul > 0) return "ko-KR";
  // No kana/hangul → CJK ideographs mean Chinese (or rarer CJK-using
  // languages; we default to zh-CN as that's by far the most common).
  //
  // IMPORTANT: even a SINGLE CJK ideograph means the query has Chinese
  // intent — don't let Latin tokens (like "iPhone 15 Pro 价格" which has
  // 2 Latin words + 2 CJK chars) fool us into picking en-US. The CJK
  // chars are the disambiguator.
  if (counts.cjk > 0) return "zh-CN";
  if (counts.cyrillic > 0) return "ru-RU";
  if (counts.arabic > 0) return "ar-SA";
  if (counts.thai > 0) return "th-TH";
  if (counts.hebrew > 0) return "he-IL";
  if (counts.greek > 0) return "el-GR";
  return "en-US";
}

/**
 * Returns true if a result item is obviously irrelevant and should be dropped:
 * - URL points back into a search engine's own domain (search redirect, "did
 *   you mean" page, etc.)
 * - Title is empty / pure whitespace / identical to the query (suggests a
 *   "search suggestion" entry, not a real result)
 *
 * This is a defensive filter; engines should already not return such items,
 * but layouts drift and this catches the worst offenders.
 */
export function isLikelyIrrelevant(item: SearchFunctionResultItem, query: string): boolean {
  const url = item.url.toLowerCase();
  const name = (item.name || "").trim();
  if (!name) return true;
  if (name.toLowerCase() === query.trim().toLowerCase()) return true;
  // Self-referential search-engine domains — never a real result.
  if (/bing\.com\/(?:ck\/a|a\.|search|form=)/i.test(url)) return true;
  if (/duckduckgo\.com\/(?:y\.js|ad|spice|lite)/i.test(url)) return true;
  if (/google\.com\/(?:url\?|search|maps|calendar)/i.test(url)) return true;
  if (/search\.yahoo\.com|baidu\.com\/(?:s|link)/i.test(url)) return true;
  return false;
}

/**
 * Heuristic relevance scoring for a result set against the original query.
 *
 * Returns a quality score in [0, 100] representing how on-topic the result
 * set is. The scoring is intentionally stricter than naive "any token hit"
 * — that approach gave misleadingly high scores to results that mentioned
 * *one* query word in an off-topic context (e.g., "Jetpack Compose" →
 * "WordPress Jetpack plugin" scored 90/100 because "jetpack" matched).
 *
 * Scoring rules:
 *
 * For each result, compute a per-result relevance verdict:
 *   - STRONG hit (3 pts): the query appears as a contiguous phrase in
 *     title/url/host (case-insensitive). E.g., query "Jetpack Compose"
 *     matches title "Jetpack Compose for Android developers".
 *   - PARTIAL hit (1 pt): ≥ 50% of the query's distinctive tokens appear
 *     in the combined title+url+host (not just one token). E.g., for
 *     "Rust vs Go programming", tokens {rust, programming} appearing in
 *     "Rust programming language" counts; "rust game on Steam" doesn't.
 *   - MISS (0 pts): neither of the above.
 *
 * Then: quality = round(STRONG_count × 100 / total)
 *   If no STRONG hits, fall back to round(PARTIAL_count × 40 / total).
 *   This means a result set with no phrase matches but lots of partial
 *   token hits caps at 40/100 — below the AUTO_QUALITY_THRESHOLD of 30
 *   only if partials are < 75% of results, which is the right call.
 *
 * Tokenization:
 *   - CJK: each ideograph is a token. Phrase match = first 3 CJK chars
 *     appear contiguously in title/url/host.
 *   - Latin: split on non-word, drop stopwords + tokens < 3 chars.
 */
export function resultSetQuality(
  results: SearchFunctionResultItem[],
  query: string
): number {
  if (results.length === 0) return 0;
  const q = query.trim();
  if (!q) return 0;

  const isCJK = /[\u3040-\u30ff\u4e00-\u9fff\uac00-\ud7af]/.test(q);
  const qLower = q.toLowerCase();

  // Build the distinctive-token list for PARTIAL-hit scoring.
  let tokens: string[];
  if (isCJK) {
    tokens = [...q].filter(c =>
      /[\u3040-\u30ff\u4e00-\u9fff\uac00-\ud7af]/.test(c)
    );
    tokens = [...new Set(tokens)];
  } else {
    const stop = new Set([
      "the", "a", "an", "is", "are", "of", "to", "in", "on", "for",
      "and", "or", "how", "what", "when", "where", "why", "with",
      "from", "by", "at", "be", "this", "that", "these", "those",
      "vs", "versus", "latest", "new", "best", "top",
    ]);
    tokens = qLower
      .split(/[^a-z0-9]+/i)
      .filter(t => t.length >= 3 && !stop.has(t));
    tokens = [...new Set(tokens)];
  }

  if (tokens.length === 0) {
    // No scorable tokens (e.g., query was all stopwords). Be optimistic.
    return 75;
  }

  // For phrase matching: take the longest 1-3 token run from the query.
  // For "Jetpack Compose" → phrase = "jetpack compose".
  // For "Rust vs Go programming" → phrase = "rust" (vs/Go filtered out)
  //   → in that case, fall back to "rust programming" as a multi-token
  //   partial-match requirement.
  const phrase = isCJK
    ? tokens.slice(0, 3).join("")
    : qLower.replace(/\s+/g, " ").trim();

  let strongHits = 0;
  let partialHits = 0;

  for (const r of results) {
    const titleUrlHost = `${r.name} ${r.url} ${r.host_name}`.toLowerCase();
    const titleUrlHostSnippet = `${titleUrlHost} ${r.snippet}`.toLowerCase();

    // STRONG: phrase appears contiguously.
    // For CJK, phrase is a char run; for Latin, it's the original query
    // lowercased (so multi-word phrases like "jetpack compose" match).
    let phraseHit = false;
    if (isCJK) {
      phraseHit = titleUrlHost.includes(phrase);
    } else {
      // For Latin queries, try the full query string first (most strict),
      // then fall back to the longest contiguous token run.
      if (titleUrlHost.includes(qLower)) {
        phraseHit = true;
      } else {
        // Find longest contiguous alphabetic run in the query.
        const runs = qLower.match(/[a-z][a-z0-9]+(?:\s+[a-z][a-z0-9]+)*/g) || [];
        const longestRun = runs.sort((a, b) => b.length - a.length)[0];
        if (longestRun && longestRun.length >= 4 && titleUrlHost.includes(longestRun)) {
          phraseHit = true;
        }
      }
    }
    // VERSION-SENSITIVE QUERIES: if the query contains a version number
    // (like "TypeScript 5.6" or "Python 3.12"), the version number MUST
    // appear in title/url/host for a STRONG hit. Otherwise we'd score
    // typescriptlang.org homepage as a strong match for "TypeScript 5.6"
    // just because "typescript" matches.
    const versionInQuery = qLower.match(/\b\d+(?:\.\d+)+\b/);
    if (phraseHit && versionInQuery) {
      if (!titleUrlHost.includes(versionInQuery[0]) &&
          !titleUrlHost.includes(versionInQuery[0].replace(/\./g, "-"))) {
        phraseHit = false;  // demote to partial
      }
    }
    // SPECIAL CASE: "X vs Y" comparison queries. The original query has
    // "vs"/"versus" in it, so we check if both X and Y appear in the
    // title/url/host (engines often reorder them as "Y vs X"). This is
    // a STRONG signal because comparison pages almost always mention both.
    if (!phraseHit && /\bvs\.?\b/i.test(q)) {
      // Strip "vs/versus" and any rewriter-added "programming/comparison"
      // to get the raw X Y tokens.
      const cleaned = qLower
        .replace(/\b(vs\.?|versus|programming|comparison|language|languages)\b/g, " ")
        .replace(/\s+/g, " ")
        .trim();
      const parts = cleaned.split(" ").filter(t => t.length >= 2);
      if (parts.length >= 2) {
        // Need at least 2 of the original X/Y tokens to both appear.
        // Use the first and last non-stopword token as X and Y.
        const x = parts[0];
        const y = parts[parts.length - 1];
        if (titleUrlHost.includes(x) && titleUrlHost.includes(y)) {
          phraseHit = true;
        }
        // Also accept common aliases (golang for go, rust-lang for rust, etc.)
        const aliases: Record<string, string[]> = {
          go: ["golang", "go-lang"],
          rust: ["rust-lang"],
          csharp: ["c#", "c sharp"],
          cpp: ["c++"],
        };
        const xAlts = aliases[x] || [];
        const yAlts = aliases[y] || [];
        const xHit = titleUrlHost.includes(x) || xAlts.some(a => titleUrlHost.includes(a));
        const yHit = titleUrlHost.includes(y) || yAlts.some(a => titleUrlHost.includes(a));
        if (xHit && yHit) phraseHit = true;
      }
    }
    if (phraseHit) {
      strongHits++;
      continue;
    }

    // PARTIAL: ≥ 50% of distinctive tokens appear (anywhere, including snippet).
    const hitCount = tokens.filter(t => titleUrlHostSnippet.includes(t)).length;
    if (hitCount >= Math.ceil(tokens.length * 0.5)) {
      partialHits++;
    }
  }

  // Strong hits dominate; partials are a weaker fallback.
  const strongScore = (strongHits / results.length) * 100;
  const partialScore = (partialHits / results.length) * 40;
  return Math.round(Math.max(strongScore, partialScore));
}

/**
 * Per-result relevance score, used for sorting merged results across engines.
 *
 * Adapted from SearXNG's `calculate_score` formula:
 *   score = Σ (engine_weight / rank)
 *
 * Higher engine weight = more trusted engine. Lower rank = higher position
 * in that engine's result list (rank 1 is the top hit). A result that
 * appears in multiple engines accumulates score from each — that's the
 * cross-engine consensus signal.
 *
 * We also apply deedy5's `SimpleFilterRanker` heuristic as a tiebreaker:
 * results whose title contains a query token beat results whose snippet
 * contains it beat results with no token hit at all.
 */
export function resultRelevanceScore(
  item: SearchFunctionResultItem,
  query: string,
  engineWeight = 1.0
): number {
  // SearXNG base: weight / rank. Rank is 1-indexed.
  let score = engineWeight / Math.max(1, item.rank);

  // deedy5 SimpleFilterRanker tiebreaker: title-hit > snippet-hit > neither.
  const q = query.trim().toLowerCase();
  if (q) {
    const isCJK = /[\u3040-\u30ff\u4e00-\u9fff\uac00-\ud7af]/.test(q);
    const name = item.name.toLowerCase();
    const snip = item.snippet.toLowerCase();
    if (isCJK) {
      const chars = [...q].filter(c => /[\u3040-\u30ff\u4e00-\u9fff\uac00-\ud7af]/.test(c));
      const nameHit = chars.some(c => name.includes(c));
      const snipHit = chars.some(c => snip.includes(c));
      if (nameHit) score += 0.5;
      if (snipHit) score += 0.2;
    } else {
      const stop = new Set(["the", "a", "an", "is", "are", "of", "to", "in", "on", "for", "and", "or", "how"]);
      const tokens = q.split(/[^a-z0-9]+/i).filter(t => t.length >= 3 && !stop.has(t));
      const nameHit = tokens.some(t => name.includes(t));
      const snipHit = tokens.some(t => snip.includes(t));
      if (nameHit) score += 0.5;
      if (snipHit) score += 0.2;
    }
  }
  return score;
}

/**
 * Merge results from multiple engines, deduplicate by URL, and re-rank
 * using the SearXNG/deedy5 hybrid score.
 *
 * On URL collision (case-insensitive), keep the variant from the engine
 * that scored it higher OR — if scores tie — the one with the longer
 * snippet (deedy5's ResultsAggregator rule).
 *
 * Returns a new sorted array. Each item's `score` field is overwritten
 * with the merged relevance score (rounded to nearest integer in [0, 100]
 * for backwards-compat with the existing score field convention).
 */
export function mergeAndRankResults(
  perEngine: Array<{ engine: SearchEngineId; weight: number; results: SearchFunctionResultItem[] }>,
  query: string,
  limit = 10
): SearchFunctionResultItem[] {
  // Map from normalized URL → accumulated result + score
  const merged = new Map<string, { item: SearchFunctionResultItem; score: number }>();

  for (const { engine, weight, results } of perEngine) {
    for (const r of results) {
      // Normalize URL for dedup: lowercase, strip trailing slash + query
      // params that don't affect content (utm_*, fbclid, gclid, etc.).
      const key = normalizeUrlForDedup(r.url);
      const contribution = resultRelevanceScore({ ...r, source_engine: engine }, query, weight);
      const existing = merged.get(key);
      if (!existing) {
        merged.set(key, {
          item: { ...r, source_engine: engine },
          score: contribution,
        });
      } else {
        // Accumulate score across engines (SearXNG consensus signal).
        existing.score += contribution;
        // On collision, keep the variant with the longer snippet.
        if (r.snippet.length > existing.item.snippet.length) {
          existing.item = { ...r, source_engine: engine };
        }
      }
    }
  }

  // Sort by accumulated score descending.
  const sorted = [...merged.values()].sort((a, b) => b.score - a.score);

  // Re-rank 1..N and clamp score to [0, 100] for the public score field.
  return sorted.slice(0, limit).map((entry, i) => ({
    ...entry.item,
    rank: i + 1,
    score: Math.max(0, Math.min(100, Math.round(entry.score * 25))),  // scale ~4.0 max → 100
  }));
}

/** Normalize a URL for deduplication: lowercase host, drop tracking params. */
function normalizeUrlForDedup(url: string): string {
  try {
    const u = new URL(url);
    // Strip tracking params.
    const tracking = new Set([
      "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
      "fbclid", "gclid", "msclkid", "ref", "ref_src", "ref_url",
      "_ga", "_gl", "si", "feature", "src",
    ]);
    for (const k of [...u.searchParams.keys()]) {
      if (tracking.has(k.toLowerCase())) u.searchParams.delete(k);
    }
    // Lowercase host, strip trailing slash on path, drop hash.
    return `${u.protocol}//${u.hostname.toLowerCase()}${u.pathname.replace(/\/$/, "")}${u.search}`;
  } catch {
    return url.toLowerCase();
  }
}

/** Type guard for the engine id list. */
export const ENGINE_IDS: ReadonlyArray<SearchEngineId> = [
  "brave",
  "duckduckgo",
  "bing",
  "google",
];

/**
 * Query rewriting: improve search quality by adding disambiguation context
 * to queries that are known to confuse search engines.
 *
 * The rewriter is INTENTIONALLY CONSERVATIVE — it only fires on patterns
 * with a clear, high-confidence disambiguation benefit. Over-eager rewriting
 * (e.g., appending "programming" to any query containing "rust") damages
 * non-programming queries like "Rust prevention tips" or "Go travel guide".
 *
 * Cases handled:
 *
 * 1. Single-token programming language queries:
 *    "Rust" → "Rust programming"
 *    "Go"   → "Go programming language"
 *    "Swift" → "Swift programming"
 *    ONLY fires when the query is exactly 1 distinctive token (after
 *    dropping stopwords and short tokens). Multi-token queries are left
 *    alone — they already have context.
 *
 * 2. Comparison queries ("X vs Y"):
 *    "Rust vs Go" → "Rust vs Go programming comparison"
 *    "React vs Vue" → "React vs Vue comparison"
 *    The "vs" token is preserved (engines honor it). We add a domain
 *    qualifier only if either side is an ambiguous lang name; otherwise
 *    we just add "comparison" to bias toward compare-style pages.
 *
 * 3. News queries with recency_days:
 *    "AI news" + recency=7 → "AI news today"
 *    "最新新闻" + recency → unchanged (Chinese news queries already
 *    imply recency; the news-mode URL filter handles homepage spam).
 *
 * 4. Queries that already contain programming context:
 *    "Rust async runtime", "Go http server", "Swift generics" — left alone.
 *
 * Returns the (possibly rewritten) query. Always returns a string.
 */
export function rewriteQuery(
  query: string,
  opts: { recency_days?: number } = {}
): string {
  const q = query.trim();
  if (!q) return q;

  const isCJK = /[\u3040-\u30ff\u4e00-\u9fff\uac00-\ud7af]/.test(q);

  // --- 1. Single-token programming language disambiguation ---
  // ONLY for short English queries. CJK queries skip this entirely.
  if (!isCJK) {
    const ambiguousLangs = new Set([
      "rust", "go", "swift", "java", "kotlin", "ruby", "python", "perl",
      "dart", "scala", "elixir", "crystal", "julia", "lua",
    ]);
    const stop = new Set([
      "the", "a", "an", "is", "are", "of", "to", "in", "on", "for",
      "and", "or", "how", "what", "when", "where", "why", "with",
      "vs", "versus", "latest", "new", "best", "top", "today",
    ]);
    // Distinctive = length >= 3, not a stopword.
    const distinctiveTokens = q.toLowerCase()
      .split(/[^a-z0-9]+/i)
      .filter(t => t.length >= 3 && !stop.has(t));

    // Only rewrite if there's exactly 1 distinctive token AND it's an
    // ambiguous language name. This avoids damaging multi-word queries
    // like "Rust prevention" or "Go travel".
    if (distinctiveTokens.length === 1 && ambiguousLangs.has(distinctiveTokens[0])) {
      return `${q} programming`;
    }
  }

  // --- 2. Comparison queries ("X vs Y") ---
  if (/\bvs\.?\b/i.test(q) || /\bversus\b/i.test(q)) {
    const ambiguousLangs = new Set([
      "rust", "go", "swift", "java", "kotlin", "ruby", "python", "perl",
      "dart", "scala", "elixir", "crystal", "julia", "lua",
    ]);
    const tokens = q.toLowerCase().split(/[^a-z0-9]+/i).filter(Boolean);
    const hasAmbiguous = tokens.some(t => ambiguousLangs.has(t));
    if (hasAmbiguous) {
      // Both programming languages — add domain context.
      if (!/\bprogramming\b/i.test(q)) {
        return `${q} programming comparison`;
      }
    }
    // Generic comparison — add "comparison" if not present.
    if (!/\bcomparison\b/i.test(q)) {
      return `${q} comparison`;
    }
  }

  // --- 3. News queries with recency ---
  // For English queries mentioning news terms + recency, add "today" to
  // bias engines toward articles published today rather than evergreen
  // news-site homepages. The actual homepage filtering happens in the
  // `filterNewsHomepages` post-filter, not here.
  if (opts.recency_days && opts.recency_days > 0 && !isCJK) {
    if (/\b(news|latest)\b/i.test(q) && !/\btoday\b/i.test(q)) {
      return `${q} today`;
    }
  }

  // --- 4. Reddit intent ---
  // "best mechanical keyboard reddit" → user wants reddit threads.
  // NOTE: We do NOT append `site:reddit.com` because DDG/Bing HTML endpoints
  // don't reliably support the `site:` operator (they return 0 results).
  // Instead, we just ensure "reddit" stays in the query — engines naturally
  // surface reddit threads when the word is present. The quality scorer
  // also gives a bonus to reddit.com results for reddit-intent queries.
  // (No rewrite needed — just don't strip "reddit".)
  if (/\breddit\b/i.test(q)) {
    // Already contains "reddit" — engines will bias toward reddit.com.
    // Don't add anything; the word itself is the signal.
  }

  // --- 4b. "best X" queries ---
  // Bing has a known bug: queries starting with "best" get misinterpreted
  // as searches for Best Buy / the word "best" (dictionary). Strip the
  // leading "best" — the remaining "X 2024" query returns the same
  // recommendation articles without triggering Bing's bug.
  // Only strip if "best" is the FIRST word and there are 2+ other words.
  if (!isCJK && /^\s*best\s+\S/i.test(q)) {
    const stripped = q.replace(/^\s*best\s+/i, "").trim();
    // Only apply if the remaining query has at least 2 tokens (don't strip
    // "best" from "best restaurants" → "restaurants" which is too vague).
    const tokenCount = stripped.split(/\s+/).filter(t => t.length > 0).length;
    if (tokenCount >= 2) {
      return stripped;
    }
  }

  // --- 5. Chinese ambiguous brand names ---
  // "苹果" alone is ambiguous (Apple Inc vs fruit). When followed by a
  // product number ("苹果16", "苹果15"), the user almost certainly means
  // iPhone. Add "iPhone" to disambiguate.
  // "特斯拉" → "Tesla 汽车" (Tesla the car company, not the inventor).
  // Only for CJK queries; English queries don't have this ambiguity.
  if (isCJK) {
    // 苹果 + 数字 → iPhone
    if (/苹果\s*\d/i.test(q) && !/iphone|apple/i.test(q)) {
      return `${q} iPhone`;
    }
    // 特斯拉 → Tesla 汽车 (trigger on ANY mention of 特斯拉, not just
    // when "Tesla" is absent — Bing splits 特斯拉 into single chars and
    // returns dictionary entries for "特". Adding "Tesla 汽车" forces Bing
    // to treat it as a brand name.)
    if (/特斯拉/.test(q) && !/tesla/i.test(q)) {
      return `${q} Tesla 汽车`;
    }
    // 小米 + 产品 → Xiaomi (already handled by context, but add for safety)
    if (/小米/.test(q) && !/xiaomi|手机|汽车|su7|yu7/i.test(q)) {
      return `${q} Xiaomi`;
    }
    // 华为 → Huawei
    if (/华为/.test(q) && !/huawei/i.test(q)) {
      return `${q} Huawei`;
    }
    // Chinese query words that Bing misinterprets as single-char lookups.
    // "怎么注册支付宝" → Bing returns dictionary entry for "怎么".
    // Fix: if the query starts with a common Chinese question word AND
    // contains a brand/product name, the brand name is the real subject.
    // We rewrite to put the brand name first.
    const cnQuestionWords = /^(怎么|如何|哪里|哪儿|为什么|为何|是不是|是不是|请问)/;
    if (cnQuestionWords.test(q)) {
      // Extract any known brand/product term from the query.
      const brands: Record<string, string> = {
        "支付宝": "支付宝 Alipay",
        "微信": "微信 WeChat",
        "淘宝": "淘宝 Taobao",
        "京东": "京东 JD",
        "抖音": "抖音 TikTok",
        "小红书": "小红书 RED",
        "哔哩哔哩": "哔哩哔哩 B站",
        "b站": "哔哩哔哩 B站",
      };
      for (const [cn, rewritten] of Object.entries(brands)) {
        if (q.includes(cn)) {
          // Rewrite: drop the question word, lead with the brand.
          const stripped = q.replace(cnQuestionWords, "").trim();
          return `${rewritten} ${stripped}`;
        }
      }
    }
  }

  return q;
}

/**
 * News-mode URL filter: drop results that point to a news-site homepage
 * (root path) when the user asked for recent results.
 *
 * When `recency_days > 0`, the user wants *articles*, not site homepages.
 * CNN, BBC, NYT etc. frequently appear as search results pointing to
 * their root domain — these are useless for "what's new" queries.
 *
 * Heuristic: drop any result whose URL path is empty, "/", or "/index.*".
 * This catches `https://www.cnn.com/`, `https://www.bbc.com/`, etc.
 * Article URLs like `https://www.cnn.com/2026/07/01/politics/story.html`
 * have non-trivial paths and are kept.
 *
 * Also drop the well-known aggregator homepages explicitly as a safety net.
 */
export function filterNewsHomepages(
  results: SearchFunctionResultItem[]
): SearchFunctionResultItem[] {
  // Known news-site homepages to always drop in news mode.
  const newsHomepages = new Set([
    "cnn.com", "www.cnn.com", "bbc.com", "www.bbc.com", "bbc.co.uk",
    "www.bbc.co.uk", "nytimes.com", "www.nytimes.com", "reuters.com",
    "www.reuters.com", "apnews.com", "apnews.org", "aljazeera.com",
    "www.aljazeera.com", "theguardian.com", "www.theguardian.com",
    "washingtonpost.com", "www.washingtonpost.com", "foxnews.com",
    "www.foxnews.com", "nbcnews.com", "www.nbcnews.com", "cbsnews.com",
    "www.cbsnews.com", "abcnews.go.com", "usatoday.com",
    "www.usatoday.com", "bloomberg.com", "www.bloomberg.com",
    "ft.com", "www.ft.com", "wsj.com", "www.wsj.com",
    "sina.com.cn", "www.sina.com.cn", "sohu.com", "www.sohu.com",
    "163.com", "www.163.com", "qq.com", "www.qq.com", "news.qq.com",
    "ifeng.com", "www.ifeng.com", "people.com.cn",
  ]);

  return results.filter(r => {
    // Drop known homepages.
    if (newsHomepages.has(r.host_name)) {
      // But keep if the URL has a non-trivial path (article on the homepage domain).
      try {
        const u = new URL(r.url);
        if (u.pathname === "/" || u.pathname === "" || /^\/index\./i.test(u.pathname)) {
          return false;
        }
      } catch {
        return false;
      }
    }
    // Drop ANY root-domain URL (path is "/" or empty) — these are always
    // homepages, never articles.
    try {
      const u = new URL(r.url);
      if (u.pathname === "/" || u.pathname === "" || /^\/index\./i.test(u.pathname)) {
        return false;
      }
    } catch {
      // URL parse failure — keep the result, let the consumer decide.
    }
    return true;
  });
}
