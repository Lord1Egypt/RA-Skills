/**
 * Rule Types and Storage - Hybrid Architecture
 *
 * Rules are stored as JSON (portable) and executed by local Hooks (enforced)
 */
export type RuleType = 'suggestion' | 'mandatory';
export type RuleTrigger = 'tool_call' | 'message' | 'action';
export type RuleAction = 'warn' | 'block' | 'suggest' | 'require_confirmation';
export interface Rule {
    id: string;
    name: string;
    type: RuleType;
    trigger: RuleTrigger;
    triggerPattern: string;
    action: RuleAction;
    condition?: string;
    description: string;
    examples?: string[];
    createdAt: string;
    updatedAt: string;
    source: 'evolution' | 'manual' | 'imported' | 'builtin';
    enabled: boolean;
}
export interface RulesPackage {
    version: string;
    exportedAt: string;
    exportedBy: string;
    rules: Rule[];
    metadata: {
        totalRules: number;
        mandatoryCount: number;
        suggestionCount: number;
    };
}
export interface RulesConfig {
    rulesDir: string;
    rulesFile: string;
    metadataFile: string;
    autoReload: boolean;
}
export declare const DEFAULT_RULES_PATH = "./.eo-rules/rules.json";
export declare const DEFAULT_METADATA_PATH = "./.eo-rules/metadata.json";
export declare const BUILTIN_HARD_RULES: Rule[];
export declare class RuleStorage {
    private rules;
    private config;
    constructor(config?: Partial<RulesConfig>);
    /**
     * Load rules from disk
     */
    load(): void;
    /**
     * Save rules to disk
     */
    save(): void;
    /**
     * Get all rules
     */
    getRules(): Rule[];
    /**
     * Get rules by type
     */
    getRulesByType(type: RuleType): Rule[];
    /**
     * Get mandatory rules (for Hook enforcement)
     */
    getMandatoryRules(): Rule[];
    /**
     * Get suggestion rules (for SOUL injection)
     */
    getSuggestionRules(): Rule[];
    /**
     * Add a rule
     */
    addRule(rule: Omit<Rule, 'id' | 'createdAt' | 'updatedAt'>): Rule;
    /**
     * Update a rule
     */
    updateRule(id: string, updates: Partial<Rule>): Rule | null;
    /**
     * Delete a rule
     */
    deleteRule(id: string): boolean;
    /**
     * Check if a trigger matches a rule
     */
    matchRule(trigger: string): Rule | null;
    /**
     * Get metadata
     */
    getMetadata(): {
        totalRules: number;
        mandatoryCount: number;
        suggestionCount: number;
    };
    /**
     * Export rules as package (for migration)
     */
    exportRules(exportedBy: string): RulesPackage;
    /**
     * Import rules from package
     */
    importRules(pkg: RulesPackage, strategy?: 'merge' | 'replace'): void;
    /**
     * Get rule count
     */
    count(): {
        total: number;
        mandatory: number;
        suggestion: number;
    };
}
export declare function getRuleStorage(config?: Partial<RulesConfig>): RuleStorage;
export declare function resetRuleStorage(): void;
//# sourceMappingURL=rule-types.d.ts.map