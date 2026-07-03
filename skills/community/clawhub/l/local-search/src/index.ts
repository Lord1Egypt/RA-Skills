/**
 * Public SDK entry point.
 *
 * Import from this module:
 *   import { search, searchOrThrow } from "local-search";
 *
 * Runtime dependencies: only `cheerio` (installed via the package's own
 * `dependencies`) and Node's built-in `fetch`.
 */
export type {
  SearchFunctionResultItem,
  SearchEngineId,
  SearchEngine,
  SearchOptions,
} from "./types.js";
export { SearchEngineError, AllEnginesFailedError } from "./types.js";

export { search, searchOrThrow } from "./search.js";
export type { SearchOutcome, SearchSuccess, SearchFailure } from "./search.js";

export { ENGINES, AUTO_ENGINE_ORDER } from "./engines/index.js";
export { ENGINE_IDS, DEFAULT_USER_AGENT } from "./engines/_shared.js";

// Semver-style version. Keep in sync with package.json.
export const VERSION = "1.6.2";
