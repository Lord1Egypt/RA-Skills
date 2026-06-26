/**
 * FilteredExecutor — Phase 2+3 of RTK Exec Compression
 * ====================================================
 *
 * Wraps any async exec function with filter-chain support.
 * Applies the FilterRegistry on every run; exec errors propagate.
 * Phase 3 adds: config flag (outputTransform) + oversized output logging.
 */

import { FilterRegistry } from "./filter-registry.ts";

/**
 * Configuration for FilteredExecutor behavior.
 */
export interface ExecutorConfig {
  /**
   * When false, bypasses all filtering and returns raw output unchanged.
   * @default true
   */
  outputTransform?: boolean;

  /**
   * Log a message when raw output exceeds this many characters.
   * 0 = disabled (no logging).
   * @default 0
   */
  oversizedOutputLog?: number;
}

const DEFAULT_CONFIG: Required<ExecutorConfig> = {
  outputTransform: true,
  oversizedOutputLog: 0,
};

/**
 * Wraps an exec function with registry-based output filtering.
 *
 * Usage:
 *   const executor = new FilteredExecutor(myExecFn, registry);
 *   const filtered = await executor.run("git diff HEAD~5");
 *
 *   // With config:
 *   const executor = new FilteredExecutor(myExecFn, registry, {
 *     outputTransform: false,       // bypass filters
 *     oversizedOutputLog: 10000,  // log when output > 10KB
 *   });
 *
 * Filter errors are fail-safe: raw output is returned instead.
 * Exec errors (rejects) are NOT swallowed — they propagate.
 */
export class FilteredExecutor {
  private execFn: (cmd: string) => Promise<string>;
  private registry: FilterRegistry;
  private onError?: (err: Error, cmd: string, raw: string) => string;
  private config: Required<ExecutorConfig>;

  constructor(
    execFn: (cmd: string) => Promise<string>,
    registry: FilterRegistry,
    config?: ExecutorConfig,
    onError?: (err: Error, cmd: string, raw: string) => string
  ) {
    this.execFn = execFn;
    this.registry = registry;
    this.config = { ...DEFAULT_CONFIG, ...config };
    this.onError = onError;
  }

  /**
   * Execute a command and filter its output through the registry.
   *
   * @param command - The command string to execute
   * @returns Filtered output; on filter error returns raw; on exec error throws
   */
  async run(command: string): Promise<string> {
    const raw = await this.execFn(command);

    // Phase 3: oversized output logging
    if (
      this.config.oversizedOutputLog > 0 &&
      raw.length > this.config.oversizedOutputLog
    ) {
      console.error(
        `[exec-truncate] oversized output: ${raw.length} chars for "${command}" — truncated`
      );
    }

    // Phase 3: outputTransform flag — bypass all filtering
    if (this.config.outputTransform === false) {
      return raw;
    }

    try {
      return this.registry.compose(command, raw);
    } catch (err) {
      if (this.onError) return this.onError(err as Error, command, raw);
      console.error("[filtered-executor] filter compose error:", err);
      return raw;
    }
  }
}
