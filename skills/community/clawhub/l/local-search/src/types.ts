/**
 * Search result item.
 *
 * The first 7 fields (url, name, snippet, host_name, rank, date, favicon)
 * form the canonical shape used across web-search skills in the ClawHub
 * registry — keeping them 1:1 means consumer code written against any
 * similarly-shaped skill works here without changes.
 *
 * The remaining fields (source_engine, raw_html, score, query_matched)
 * are extensions added by this local-search skill and are optional.
 */
export interface SearchFunctionResultItem {
  // ----- Canonical fields -----
  /** Full URL of the result page. */
  url: string;
  /** Title of the page. */
  name: string;
  /** Preview text / short description shown by the search engine. */
  snippet: string;
  /** Domain name, e.g. "en.wikipedia.org". */
  host_name: string;
  /** 1-indexed ranking within the engine's result set. */
  rank: number;
  /** Publication / update date as returned by the engine; "N/A" when unknown. */
  date: string;
  /** Best-effort favicon URL. */
  favicon: string;

  // ----- Extension fields (specific to local-search) -----
  /** Which engine actually produced this hit. */
  source_engine: SearchEngineId;
  /** Raw HTML snippet (optional, useful for re-parsing downstream). */
  raw_html?: string;
  /** Heuristic relevance score in [0, 100] (optional). */
  score?: number;
  /** Substrings of `query` that appear in title or snippet (optional). */
  query_matched?: string[];
}

/** Identifiers of supported search engine backends. */
export type SearchEngineId = "brave" | "duckduckgo" | "bing" | "google";

/** Public options accepted by `search()` / `searchWith()`. */
export interface SearchOptions {
  /** Number of results to request per engine. Default: 10. */
  num?: number;
  /**
   * Restrict to results published within the last N days.
   * Implemented per-engine (DDG `df`, Bing `freshness`, Google `tbs=qdr:d`).
   * 0 / undefined = no filter.
   */
  recency_days?: number;
  /**
   * Engine selection strategy.
   * - "auto" (default): try engines in order [duckduckgo, bing, google],
   *   return the first one that yields >=1 result; if all fail, throw an
   *   `AggregateError`-style object containing every engine's error.
   * - Specific id: only call that engine, surface its error directly.
   */
  engine?: SearchEngineId | "auto";
  /** Per-engine timeout in ms. Default: 8000. */
  timeoutMs?: number;
  /**
   * Optional custom `fetch` implementation (Node 18+ ships a global one).
   * Useful for tests or when running in a non-Node runtime.
   */
  fetchImpl?: typeof fetch;
  /**
   * Optional custom User-Agent string. Defaults to a recent Chrome UA
   * because some engines 4xx/redirect obvious bot UAs.
   */
  userAgent?: string;
  /**
   * Optional locale override for engines that support it. Default: auto-detect
   * from the query string (CJK → zh-CN, kana → ja-JP, hangul → ko-KR,
   * Cyrillic → ru-RU, etc.; Latin/default → en-US).
   *
   * Pass e.g. "zh-CN", "ja-JP", "en-GB" to override the auto-detection.
   * Bing is the most responsive to this (cc + mkt + setlang, plus `ensearch=1`
   * for English locales only). DuckDuckGo largely ignores it. Google uses
   * hl/gl.
   */
  locale?: string;
}

/** Minimal contract every engine backend must implement. */
export interface SearchEngine {
  id: SearchEngineId;
  display: string;
  /** Run a single search. MUST throw on hard failure (network / parse). */
  search(
    query: string,
    opts: Required<Pick<SearchOptions, "num" | "recency_days" | "timeoutMs" | "userAgent" | "locale">> & {
      fetchImpl: typeof fetch;
    }
  ): Promise<SearchFunctionResultItem[]>;
}

/** Normalized error with the engine id attached, so callers can tell which one failed. */
export class SearchEngineError extends Error {
  readonly engine: SearchEngineId;
  readonly cause?: unknown;
  constructor(engine: SearchEngineId, message: string, cause?: unknown) {
    super(`[${engine}] ${message}`);
    this.name = "SearchEngineError";
    this.engine = engine;
    this.cause = cause;
  }
}

/** Error thrown when `engine: "auto"` exhausts every backend. */
export class AllEnginesFailedError extends Error {
  readonly errors: Array<{ engine: SearchEngineId; error: unknown }>;
  constructor(errors: Array<{ engine: SearchEngineId; error: unknown }>) {
    super(
      `All search engines failed. Details:\n` +
        errors
          .map((e) => `  - ${e.engine}: ${errMessage(e.error)}`)
          .join("\n")
    );
    this.name = "AllEnginesFailedError";
    this.errors = errors;
  }
}

function errMessage(e: unknown): string {
  if (e instanceof Error) return e.message;
  try {
    return JSON.stringify(e);
  } catch {
    return String(e);
  }
}
