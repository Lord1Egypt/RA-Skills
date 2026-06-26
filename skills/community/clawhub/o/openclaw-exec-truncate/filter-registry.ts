/**
 * Filter Registry — Phase 2 of RTK Exec Compression
 * ================================================
 *
 * Pattern-based registry for composing command output filters.
 * Filters are tried in registration order; all matching patterns apply.
 * Fail-safe: any filter exception returns raw output.
 */

export type ExecFilter = (command: string, output: string) => string;

/**
 * A registry mapping RegExp patterns → filter function chains.
 *
 * Multiple patterns can match the same command — all matching filters
 * are collected and applied in registration order.
 *
 * @example
 * const registry = new FilterRegistry();
 * registry.register(/^git diff/i, truncateGitDiff);
 * registry.register(/^git log/i, truncateGitLog);
 * registry.register(/^grep/i, truncateGrepOutput, addLineNumbers);
 */
export class FilterRegistry {
  private patterns: Array<{ pattern: RegExp; filters: ExecFilter[] }> = [];

  /**
   * Register one or more filters under a command-pattern RegExp.
   * Patterns are tested in registration order; all matching patterns' filters apply.
   */
  register(pattern: RegExp, ...filters: ExecFilter[]): void {
    this.patterns.push({ pattern, filters });
  }

  /**
   * Returns all filter functions matching the given command.
   * Filters from multiple matching patterns are concatenated in registration order.
   */
  find(command: string): ExecFilter[] {
    const matches: ExecFilter[] = [];
    for (const { pattern, filters } of this.patterns) {
      if (pattern.test(command)) {
        matches.push(...filters);
      }
    }
    return matches;
  }

  /**
   * Applies all matching filters to the output, in chain order.
   * Each filter's output becomes the next filter's input.
   * Fail-safe: if any filter throws, returns raw output unchanged.
   */
  compose(command: string, output: string): string {
    const filters = this.find(command);
    if (filters.length === 0) return output;

    let result = output;
    for (const filter of filters) {
      result = filter(command, result);
    }
    return result;
  }
}
