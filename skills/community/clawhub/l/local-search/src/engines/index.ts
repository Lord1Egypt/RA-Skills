/**
 * Engine registry.
 *
 * Single source of truth for which engines exist + the order `auto` tries
 * them in. Adjust the order here if you want a different default priority.
 */
import type { SearchEngine, SearchEngineId } from "../types.js";
import { duckduckgoEngine } from "./duckduckgo.js";
import { bingEngine } from "./bing.js";
import { googleEngine } from "./google.js";
import { braveEngine } from "./brave.js";

export { duckduckgoEngine, bingEngine, googleEngine, braveEngine };

/** All engines, keyed by id. */
export const ENGINES: Record<SearchEngineId, SearchEngine> = {
  brave: braveEngine,
  duckduckgo: duckduckgoEngine,
  bing: bingEngine,
  google: googleEngine,
};

/**
 * Order used by `engine: "auto"`.
 *
 * v1.6.0 strategy: Brave first (highest quality on first call), then DDG
 * (good for long-tail technical), then Bing (stable fallback), then Google
 * (last resort, usually blocked on datacenter IPs).
 *
 *  1. Brave      — independent index, best for compound words / brand names /
 *                  Chinese queries. Aggressively rate-limited (~1 req per
 *                  few seconds); if it 429s we immediately fall through.
 *  2. DuckDuckGo — good for long-tail technical queries; frequently rate-
 *                  limited from datacenter IPs.
 *  3. Bing       — stable from any IP but weak on long-tail / CJK.
 *  4. Google     — best quality when reachable; usually blocked on datacenter.
 *
 * The quality-gate logic in `search()` may stop early at any engine that
 * returns a result set with quality >= AUTO_QUALITY_THRESHOLD. If no engine
 * clears the gate, results are merged via SearXNG consensus scoring.
 */
export const AUTO_ENGINE_ORDER: SearchEngineId[] = [
  "brave",
  "duckduckgo",
  "bing",
  "google",
];

/**
 * Quality threshold below which the auto chain keeps looking for a better
 * engine. 30 means "at least 30% of results mention a query token in
 * title/url/snippet" — empirical testing showed this is a good divider
 * between "useful" and "garbage" result sets.
 */
export const AUTO_QUALITY_THRESHOLD = 30;
