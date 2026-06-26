export declare class ClosedLoopEvolver {
    enabled: boolean;
    minDecisionsForEvolution: number;
    cooldown: number;
    lastEvolution: number;
    evolutionCount: number;
    autoEnforce: boolean;
    /**
     * Main entry point: Run closed-loop evolution
     * This will:
     * 1. Analyze effect tracker data
     * 2. Generate hybrid rules (mandatory + suggestion)
     * 3. Persist rules to JSON (portable format)
     * 4. Enforce: Hook for mandatory, SOUL for suggestions
     */
    evolve(api: any): Promise<any>;
    /**
     * Force evolution (bypass cooldown) - for testing
     */
    forceEvolve(api: any): Promise<any>;
    /**
     * Check if evolution should run
     */
    shouldEvolve(): boolean;
    /**
     * Get evolution status
     */
    getStatus(): any;
    /**
     * Enable/disable auto-enforce
     */
    setAutoEnforce(enabled: boolean): void;
    /**
     * Get current mandatory rules
     */
    getCurrentRules(): any[];
    /**
     * Get evolution history
     */
    getEvolutionHistory(limit?: number): any[];
    /**
     * Export rules for migration
     */
    exportRules(agentId: string): any;
    /**
     * Import rules from package
     */
    importRules(pkg: any, strategy?: 'merge' | 'replace'): void;
    /**
     * Manually trigger rule enforcement
     */
    enforceRulesNow(rules: any[], api: any): any;
}
export declare const closedLoopEvolver: ClosedLoopEvolver;
//# sourceMappingURL=closed-loop-evolver.d.ts.map