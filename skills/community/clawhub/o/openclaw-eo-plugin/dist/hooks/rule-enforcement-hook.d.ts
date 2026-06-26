/**
 * Rule Enforcement Hook - Hook-level rule checking
 *
 * This hook intercepts dangerous operations and:
 * - Warns users about potential issues
 * - Requires confirmation for risky operations
 * - Sets context flags for the agent to handle
 */
import type { OpenClawPluginApi } from 'openclaw/plugin-sdk';
export interface RuleEnforcementConfig {
    enabled: boolean;
    logViolations: boolean;
}
export declare function configureRuleEnforcement(cfg: Partial<RuleEnforcementConfig>): void;
/**
 * Create the rule enforcement hook
 */
export declare function createRuleEnforcementHook(api: OpenClawPluginApi): {
    id: string;
    name: string;
    description: string;
    handle: (event: any) => Promise<void>;
};
/**
 * Get enforcement stats
 */
export declare function getEnforcementStats(): {
    enabled: boolean;
    total: number;
    mandatory: number;
    suggestion: number;
};
//# sourceMappingURL=rule-enforcement-hook.d.ts.map