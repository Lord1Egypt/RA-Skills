/**
 * Search orchestrator.
 *
 * `search()` is the single entry point used by both the CLI and the SDK.
 * It normalizes options, dispatches to one or more engine backends, and
 * implements the `auto` fallback chain with **quality gating** — meaning
 * it doesn't just take the first engine that returns *any* results, it
 * takes the first engine that returns *good* results (measured by how
 * many results mention a query token in their title/url/snippet).
 */
import {
  AllEnginesFailedError,
  type SearchEngineId,
  type SearchFunctionResultItem,
  type SearchOptions,
} from "./types.js";
import {
  DEFAULT_USER_AGENT,
  ENGINE_IDS,
  detectLocale,
  filterNewsHomepages,
  mergeAndRankResults,
  rewriteQuery,
  resultSetQuality,
} from "./engines/_shared.js";
import {
  AUTO_ENGINE_ORDER,
  AUTO_QUALITY_THRESHOLD,
  ENGINES,
} from "./engines/index.js";

/**
 * Per-engine trust weight, used by `mergeAndRankResults` when the auto
 * chain falls through to cross-engine merging. Higher = more trusted.
 * Empirical: Brave has the best per-result quality when it works;
 * DDG handles long-tail technical queries well; Bing is stable but
 * weak on CJK/compound words; Google is best when reachable.
 */
const ENGINE_WEIGHTS: Record<SearchEngineId, number> = {
  brave: 1.3,
  duckduckgo: 1.2,
  bing: 1.0,
  google: 1.1,
};

export interface SearchSuccess<T extends "single" | "auto" = "single" | "auto"> {
  success: true;
  results: SearchFunctionResultItem[];
  /** Which engine produced these results. Equal to the requested id for `single`. */
  engine: SearchEngineId;
  /** How many engines were tried (1 for explicit, possibly >1 for `auto`). */
  enginesTried: T extends "auto" ? SearchEngineId[] : [SearchEngineId];
  /** How long the call took in ms. */
  elapsedMs: number;
  /** The locale actually used for this call (explicit override or auto-detected). */
  locale: string;
  /** 0-100 heuristic relevance score for the returned result set. */
  quality: number;
  /** Non-fatal warnings (e.g., "no engine cleared the quality gate"). */
  warnings: string[];
}

export interface SearchFailure {
  success: false;
  error: string;
  /** Only populated under `engine: "auto"` — list of all engine errors. */
  errors?: Array<{ engine: SearchEngineId; error: unknown }>;
  elapsedMs: number;
}

export type SearchOutcome = SearchSuccess<"single"> | SearchSuccess<"auto"> | SearchFailure;

/** Normalize the user-supplied options into a fully-resolved shape. */
function resolveOptions(opts: SearchOptions = {}) {
  const num = Math.max(1, Math.min(opts.num ?? 10, 50));
  const recency_days = Math.max(0, Math.min(opts.recency_days ?? 0, 365));
  const timeoutMs = Math.max(500, Math.min(opts.timeoutMs ?? 8000, 60_000));
  const userAgent = opts.userAgent?.trim() || DEFAULT_USER_AGENT;
  const localeExplicit = opts.locale?.trim() || null;
  const fetchImpl = opts.fetchImpl ?? globalThis.fetch;
  if (typeof fetchImpl !== "function") {
    throw new Error(
      "No global `fetch` available. Pass `fetchImpl` explicitly (Node 18+ ships one by default)."
    );
  }
  const engineRaw = (opts.engine ?? "auto").toLowerCase();
  if (engineRaw !== "auto" && !ENGINE_IDS.includes(engineRaw as SearchEngineId)) {
    throw new Error(
      `Unknown engine "${opts.engine}". Valid: auto, ${ENGINE_IDS.join(", ")}`
    );
  }
  return {
    num,
    recency_days,
    timeoutMs,
    userAgent,
    localeExplicit,
    fetchImpl,
    engine: engineRaw as SearchEngineId | "auto",
  };
}

/**
 * Run a search. Throws only on programming errors (bad options, no fetch).
 * Network / parse failures are surfaced via the returned `SearchOutcome`.
 */
export async function search(
  query: string,
  opts: SearchOptions = {}
): Promise<SearchOutcome> {
  const resolved = resolveOptions(opts);
  const startedAt = Date.now();

  if (!query || !query.trim()) {
    return {
      success: false,
      error: "Query is empty.",
      elapsedMs: Date.now() - startedAt,
    };
  }

  // Query rewriting: add disambiguation context for queries that confuse
  // search engines (e.g., "Rust" alone → "Rust programming"). The
  // rewriter is conservative — see its docstring for the rules.
  const rewrittenQuery = rewriteQuery(query, { recency_days: resolved.recency_days });
  const queryWasRewritten = rewrittenQuery !== query;

  // Locale is auto-detected from the ORIGINAL query (the user's intent),
  // not the rewritten one. CJK detection works the same on both.
  const locale = resolved.localeExplicit ?? detectLocale(query);

  // The engine call uses the rewritten query. Quality scoring uses the
  // original query (so we measure against user intent, not our own rewrite).
  const callEngine = (id: SearchEngineId) =>
    ENGINES[id].search(rewrittenQuery, {
      num: resolved.num,
      recency_days: resolved.recency_days,
      timeoutMs: resolved.timeoutMs,
      userAgent: resolved.userAgent,
      locale,
      fetchImpl: resolved.fetchImpl as typeof fetch,
    });

  // Post-process engine results: drop news-site homepages if recency_days
  // is set (user wants articles, not homepages).
  const postFilter = (results: SearchFunctionResultItem[]): SearchFunctionResultItem[] => {
    if (resolved.recency_days && resolved.recency_days > 0) {
      return filterNewsHomepages(results);
    }
    return results;
  };

  // ---- Explicit single-engine mode ----
  if (resolved.engine !== "auto") {
    try {
      const rawResults = await callEngine(resolved.engine);
      const results = postFilter(rawResults);
      const quality = resultSetQuality(results, query);
      const warnings: string[] = [];
      if (queryWasRewritten) {
        warnings.push(`Query rewritten: "${query}" → "${rewrittenQuery}"`);
      }
      if (quality < AUTO_QUALITY_THRESHOLD) {
        warnings.push(
          `${resolved.engine} returned low-relevance results (quality ${quality}/100). ` +
          `Try \`--engine auto\` to let the orchestrator pick a better engine, ` +
          `or \`--engine duckduckgo\` which handles long-tail queries well.`
        );
      }
      return {
        success: true,
        results,
        engine: resolved.engine,
        enginesTried: [resolved.engine],
        elapsedMs: Date.now() - startedAt,
        locale,
        quality,
        warnings,
      };
    } catch (err) {
      return {
        success: false,
        error: (err as Error).message,
        elapsedMs: Date.now() - startedAt,
      };
    }
  }

  // ---- Auto mode with quality gating + cross-engine merging ----
  //
  // Strategy:
  //   1. Try each engine in AUTO_ENGINE_ORDER.
  //   2. For each engine that returns results, compute quality.
  //   3. If quality >= AUTO_QUALITY_THRESHOLD, accept immediately.
  //   4. Otherwise, remember this result set as "best so far" and try next.
  //   5. If no engine clears the gate BUT we have >=2 result sets, merge
  //      them with `mergeAndRankResults` (SearXNG consensus scoring) and
  //      return the merged set. Cross-engine dedup + relevance ranking
  //      often rescues a query that no single engine handled well.
  //   6. If only one engine returned anything, return its result set as
  //      best-effort with a warning.
  //   7. If every engine errored, surface as failure.
  const tried: SearchEngineId[] = [];
  const errors: Array<{ engine: SearchEngineId; error: unknown }> = [];
  // Collect every result set we got, even low-quality ones — we may merge them.
  const collected: Array<{ engine: SearchEngineId; results: SearchFunctionResultItem[]; quality: number }> = [];
  const warnings: string[] = [];

  for (const id of AUTO_ENGINE_ORDER) {
    tried.push(id);
    try {
      const rawResults = await callEngine(id);
      const results = postFilter(rawResults);
      if (results.length === 0) {
        errors.push({ engine: id, error: new Error("Engine returned 0 results (after post-filter)") });
        continue;
      }
      const quality = resultSetQuality(results, query);
      // Accept immediately if quality clears the gate.
      if (quality >= AUTO_QUALITY_THRESHOLD && collected.length === 0) {
        const acceptWarnings: string[] = [];
        if (queryWasRewritten) {
          acceptWarnings.push(`Query rewritten: "${query}" → "${rewrittenQuery}"`);
        }
        return {
          success: true,
          results,
          engine: id,
          enginesTried: tried,
          elapsedMs: Date.now() - startedAt,
          locale,
          quality,
          warnings: acceptWarnings,
        };
      }
      // Otherwise, remember and keep looking.
      collected.push({ engine: id, results, quality });
    } catch (err) {
      errors.push({ engine: id, error: err });
    }
  }

  // No engine cleared the quality gate on its own.
  if (collected.length > 0) {
    // If we have 2+ result sets, try merging them — the SearXNG consensus
    // score often surfaces results that no single engine ranked highly.
    if (collected.length >= 2) {
      const mergeInput = collected.map(c => ({
        engine: c.engine,
        weight: ENGINE_WEIGHTS[c.engine],
        results: c.results,
      }));
      const merged = mergeAndRankResults(mergeInput, query, resolved.num);
      const mergedQuality = resultSetQuality(merged, query);

      // Use the merged set if it's better than the best single-engine set.
      const bestSingle = collected.reduce((a, b) => (b.quality > a.quality ? b : a));
      if (mergedQuality >= bestSingle.quality) {
        if (queryWasRewritten) {
          warnings.push(`Query rewritten: "${query}" → "${rewrittenQuery}"`);
        }
        warnings.push(
          `Single-engine quality was low (best ${bestSingle.quality}/100 from ${bestSingle.engine}). ` +
          `Merged ${collected.length} engines (${collected.map(c => c.engine).join(" + ")}) → quality ${mergedQuality}/100.`
        );
        return {
          success: true,
          results: merged,
          engine: "auto",  // signal that this is a merged result
          enginesTried: tried,
          elapsedMs: Date.now() - startedAt,
          locale,
          quality: mergedQuality,
          warnings,
        };
      }
    }

    // Merge didn't help (or only one engine returned). Return the best single.
    const best = collected.reduce((a, b) => (b.quality > a.quality ? b : a));
    if (queryWasRewritten) {
      warnings.push(`Query rewritten: "${query}" → "${rewrittenQuery}"`);
    }
    warnings.push(
      `No engine cleared the quality gate (threshold ${AUTO_QUALITY_THRESHOLD}). ` +
      `Returning best result set from ${best.engine} (quality ${best.quality}/100). ` +
      `Tried: ${tried.join(" → ")}.`
    );
    return {
      success: true,
      results: best.results,
      engine: best.engine,
      enginesTried: tried,
      elapsedMs: Date.now() - startedAt,
      locale,
      quality: best.quality,
      warnings,
    };
  }

  // Every engine errored — surface as failure.
  const agg = new AllEnginesFailedError(errors);
  return {
    success: false,
    error: agg.message,
    errors,
    elapsedMs: Date.now() - startedAt,
  };
}

/**
 * Throw-on-failure variant. Equivalent to `search()` but throws
 * `AllEnginesFailedError` (in `auto` mode) or the underlying engine
 * error (in single mode). Handy when you'd rather use try/catch than
 * branch on `success`.
 */
export async function searchOrThrow(
  query: string,
  opts: SearchOptions = {}
): Promise<SearchFunctionResultItem[]> {
  const outcome = await search(query, opts);
  if (!outcome.success) {
    if ("errors" in outcome && outcome.errors && outcome.errors.length > 1) {
      throw new AllEnginesFailedError(outcome.errors);
    }
    throw new Error(outcome.error);
  }
  return outcome.results;
}
