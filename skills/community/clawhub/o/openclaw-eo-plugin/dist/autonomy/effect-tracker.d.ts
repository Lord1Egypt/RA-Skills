/**
 * Effect Tracker v3 - Tracks decision outcomes with scoring + persistence
 *
 * Part of the self-optimization loop:
 * Decision → Execute → Track → Score → Optimize → Evolve
 *
 * Features:
 * - JSON file persistence (survives restarts)
 * - Automatic save on each track()
 * - Load on initialization
 */
import { type ScoringDecision, type ScoringOutcome, type ScoringScore } from './effect-scorer.js';
export type { ScoringDecision, ScoringOutcome, ScoringScore } from './effect-scorer.js';
export declare class EffectTracker {
    private tracked;
    private max;
    private scoreHistory;
    private persistPath;
    private dirty;
    private saveDebounceTimer;
    constructor(persistPath?: string);
    /**
     * Load data from disk
     */
    private load;
    /**
     * Persist data to disk (debounced)
     */
    private persist;
    /**
     * Save immediately
     */
    private saveNow;
    /**
     * Track a decision and its outcome, automatically calculate score
     */
    track(decision: ScoringDecision, outcome: ScoringOutcome): ScoringScore;
    /**
     * Track with implicit feedback (no explicit outcome)
     */
    trackWithFeedback(decision: ScoringDecision, feedback: {
        userFeedback?: 'positive' | 'negative' | 'neutral';
        repeatedTask?: boolean;
        taskAbandoned?: boolean;
        quickApproval?: boolean;
        modifications?: number;
    }): ScoringScore;
    /**
     * Get score for a specific decision
     */
    getScore(id: string): ScoringScore | undefined;
    /**
     * Get recent scores
     */
    getRecentScores(limit?: number): ScoringScore[];
    /**
     * Calculate average score (last 100 decisions)
     */
    avgScore(): number;
    /**
     * Calculate success rate (scores >= 70)
     */
    successRate(): number;
    /**
     * Get aggregated statistics
     */
    stats(): {
        total: number;
        avgScore: number;
        successRate: number;
        grade: 'A' | 'B' | 'C' | 'D' | 'F';
        trend: 'improving' | 'stable' | 'declining';
        percentile: number;
        scoreStats: {
            min: number;
            max: number;
            stdDev: number;
        };
    };
    /**
     * Get scores by grade
     */
    getScoresByGrade(): Record<string, ScoringScore[]>;
    /**
     * Prune oldest 10% of tracked items
     */
    private prune;
    /**
     * Reset all tracked data
     */
    reset(): void;
    /**
     * Force save now (for testing)
     */
    forceSave(): void;
    /**
     * Export all scores as JSON (for debugging/analysis)
     */
    exportScores(): string;
}
export declare const effectTracker: EffectTracker;
//# sourceMappingURL=effect-tracker.d.ts.map