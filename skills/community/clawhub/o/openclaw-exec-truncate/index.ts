/**
 * RTK Exec Compression — Public API
 * ==================================
 *
 * Phase 1: Domain-aware truncation (mod.ts)
 * Phase 2: Filter registry + FilteredExecutor
 * Phase 3: Config flag (outputTransform) + oversized output logging
 *
 * Usage:
 *   import { createFilteredExecutor, defaultRegistry } from './index';
 *
 *   // Simple — all defaults
 *   const executor = createFilteredExecutor(myExecFn);
 *
 *   // With config (Phase 3)
 *   const executor = createFilteredExecutor(myExecFn, {
 *     outputTransform: false,      // bypass filters
 *     oversizedOutputLog: 10000,  // log when raw output > 10KB
 *   });
 */

// ─── Phase 1 re-exports ───────────────────────────────────────────────────────

export {
  truncateWithFailSafe,
  truncateGitDiff,
  truncateGitLog,
  truncateGrepOutput,
  truncateLsOutput,
  truncateBuildOutput,
  truncateExecOutput,
} from "./mod.ts";

// ─── Phase 2+3 ────────────────────────────────────────────────────────────────

export { FilterRegistry, type ExecFilter } from "./filter-registry.ts";
export {
  FilteredExecutor,
  type ExecutorConfig,
} from "./filtered-executor.ts";

import { FilterRegistry } from "./filter-registry.ts";
import {
  FilteredExecutor,
  type ExecutorConfig,
} from "./filtered-executor.ts";
import {
  truncateGitDiff,
  truncateGitLog,
  truncateGrepOutput,
  truncateLsOutput,
  truncateBuildOutput,
} from "./mod.ts";

// ─── Pre-wired default registry ──────────────────────────────────────────────

/**
 * Pre-built registry with Phase 1 truncation functions registered.
 *
 * Registered patterns (in order):
 *   /^git diff/i      → truncateGitDiff
 *   /^git log/i       → truncateGitLog
 *   /^grep/i          → truncateGrepOutput
 *   /^rg /i           → truncateGrepOutput
 *   /^find\b/i        → truncateGrepOutput
 *   /^ls\b/i          → truncateLsOutput
 *   /^(cargo|npm|go|pip|yarn|tsc|gcc|cmake|make|ruff)/i → truncateBuildOutput
 */
export const defaultRegistry: FilterRegistry = new FilterRegistry();

defaultRegistry.register(/^git diff/i, (_cmd, output) => truncateGitDiff(output));
defaultRegistry.register(/^git log/i, (_cmd, output) => truncateGitLog(output));
defaultRegistry.register(/^grep/i, (_cmd, output) => truncateGrepOutput(output));
defaultRegistry.register(/^rg /i, (_cmd, output) => truncateGrepOutput(output));
defaultRegistry.register(/^find\b/i, (_cmd, output) => truncateGrepOutput(output));
defaultRegistry.register(/^ls\b/i, (_cmd, output) => truncateLsOutput(output));
defaultRegistry.register(
  /^(cargo|npm|go|pip|yarn|tsc|gcc|cmake|make|ruff)/i,
  (_cmd, output) => truncateBuildOutput(output)
);

// ─── Factory ─────────────────────────────────────────────────────────────────

/**
 * Create a FilteredExecutor with the default registry pre-wired.
 *
 * @param execFn - Async function: (cmd: string) => Promise<string>
 * @param config - Optional Phase 3 config:
 *   outputTransform: false → bypass all filtering, return raw
 *   oversizedOutputLog: N  → log when raw output > N chars
 * @param onError - Optional error handler for filter failures
 *
 * @example
 * // Basic usage
 * const executor = createFilteredExecutor(cmd => exec(cmd));
 *
 * // Bypass filtering entirely (Phase 3)
 * const executor = createFilteredExecutor(cmd => exec(cmd), {
 *   outputTransform: false
 * });
 *
 * // Log oversized outputs (Phase 3)
 * const executor = createFilteredExecutor(cmd => exec(cmd), {
 *   oversizedOutputLog: 5000
 * });
 */
export function createFilteredExecutor(
  execFn: (cmd: string) => Promise<string>,
  config?: ExecutorConfig,
  onError?: (err: Error, cmd: string, raw: string) => string
): FilteredExecutor {
  return new FilteredExecutor(execFn, defaultRegistry, config, onError);
}
