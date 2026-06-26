/**
 * Apply rules to a specific agent's SOUL.md
 */
export declare function applyRulesToAgent(agentId: string, rules: any[], dryRun?: boolean): any;
/**
 * Apply rules to ALL agent workspaces
 */
export declare function applyRulesToAllAgents(rules: any[], options?: any): any;
/**
 * Extract current mandatory rules from a SOUL.md
 */
export declare function extractRulesFromSoul(soul: string): any[];
/**
 * Generate rules from evolution analysis
 */
export declare function generateRulesFromEvolution(evolutionResult: any, stats: any): any[];
//# sourceMappingURL=rule-enforcer.d.ts.map