/**
 * Self Optimizer v2 - Optimizes based on scored outcomes
 *
 * Part of the self-optimization loop:
 * Decision → Execute → Track → Score → Optimize → Evolve
 *
 * Uses EffectScore data to make intelligent optimization decisions
 */
import type { OptimizationResult, Strategy } from './types.js';
export declare class SelfOptimizer {
    private lastOpt;
    private cooldown;
    private currentStrategy;
    private optimizationHistory;
    /**
     * Main optimization entry point
     * Call this after collecting sufficient effect scores
     */
    optimize(): Promise<OptimizationResult>;
    /**
     * Optimize specific parameters based on stats
     */
    private optimizeParams;
    /**
     * Apply a specific strategy
     */
    private applyStrategy;
    /**
     * Calculate score improvement from last optimization
     */
    private calculateImprovement;
    /**
     * Get current strategy
     */
    getCurrentStrategy(): Strategy;
    /**
     * Get optimization history
     */
    getHistory(): typeof this.optimizationHistory;
    /**
     * Force optimization (bypass cooldown)
     */
    forceOptimize(): Promise<OptimizationResult>;
    /**
     * Get optimization recommendations as formatted string
     */
    getRecommendations(): Promise<string>;
}
export declare const selfOptimizer: SelfOptimizer;
//# sourceMappingURL=optimizer.d.ts.map