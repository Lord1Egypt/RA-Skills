/**
 * Parse YAML rule blocks from MEMORY.md and return rules with weight >= 1.0.
 * Reads at most once per 15 seconds (cached).
 */
export declare function getPinnedRules(): string[];
/**
 * Build an XML block of pinned rules for context injection.
 * Returns empty string if no rules are pinned.
 */
export declare function buildPinnedRulesXml(): string;
/**
 * Register the weighter module. No longer writes to openclaw.json —
 * pinned rules are injected via the before_agent_start hook instead.
 */
export declare function registerWeighter(_api: any): void;
