/**
 * Save mandatory rules to disk
 */
export declare function saveMandatoryRules(rules: any[]): string;
/**
 * Load mandatory rules from disk
 */
export declare function loadMandatoryRules(): any[] | null;
/**
 * Append to evolution log
 */
export declare function appendEvolutionLog(entry: any): number;
/**
 * Get evolution log
 */
export declare function getEvolutionLog(limit?: number): any[];
/**
 * Clear all rules (for testing)
 */
export declare function clearAllRules(): void;
/**
 * Get rules directory path (for external use)
 */
export declare function getRulesPath(): string;
//# sourceMappingURL=rule-persistence.d.ts.map