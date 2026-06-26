/**
 * Rule Enforcer - Hybrid Architecture
 *
 * Executes rules at Hook level (cannot be bypassed)
 * - Mandatory rules: Hook enforcement (hard)
 * - Suggestion rules: SOUL injection (soft)
 */
import { type Rule, type RulesPackage } from './rule-types.js';
export interface EnforcementResult {
    allowed: boolean;
    rule?: Rule;
    reason?: string;
    suggestion?: string;
}
export interface EnforcerConfig {
    rulesPath: string;
    enableBuiltinRules: boolean;
    allowRuleDisable: boolean;
}
/**
 * Rule Enforcer - Checks if an action violates mandatory rules
 */
export declare class RuleEnforcer {
    private storage;
    private config;
    constructor(config?: Partial<EnforcerConfig>);
    /**
     * Check if a tool call or action should be allowed
     */
    check(toolCall: string, context?: Record<string, any>): EnforcementResult;
    /**
     * Get all active rules
     */
    getActiveRules(): Rule[];
    /**
     * Get mandatory rules count
     */
    getMandatoryCount(): number;
    /**
     * Get suggestion rules for SOUL injection
     */
    getSuggestionForSoul(): Rule[];
    /**
     * Export rules for migration
     */
    exportRules(agentId: string): RulesPackage;
    /**
     * Import rules from package
     */
    importRules(pkg: RulesPackage, strategy?: 'merge' | 'replace'): void;
    /**
     * Get rules stats
     */
    getStats(): {
        total: number;
        mandatory: number;
        suggestion: number;
    };
}
export declare function getRuleEnforcer(): RuleEnforcer;
/**
 * Generate SOUL.md section for suggestion rules
 */
export declare function generateSuggestionSection(): string;
/**
 * Check if a tool call should be blocked (for Hook use)
 */
export declare function shouldBlockToolCall(toolCall: string, context?: Record<string, any>): {
    blocked: boolean;
    reason?: string;
    suggestion?: string;
};
//# sourceMappingURL=rule-enforcer-hybrid.d.ts.map