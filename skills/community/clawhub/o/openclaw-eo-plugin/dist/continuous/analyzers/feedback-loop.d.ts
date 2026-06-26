/**
 * Feedback Loop
 * Processes feedback from sessions and feeds it back into the learning system
 */
import type { AnalyzedSession } from './session-analyzer.js';
export interface FeedbackLoopConfig {
    enabled: boolean;
    successThreshold: number;
    errorThreshold: number;
    autoAdjustWeights: boolean;
}
export interface FeedbackEntry {
    id: string;
    timestamp: number;
    sessionId: string;
    success: boolean;
    errorCount: number;
    patternCount: number;
    weightAdjustment?: number;
}
export declare class FeedbackLoop {
    private config;
    private feedbackHistory;
    constructor(config?: Partial<FeedbackLoopConfig>);
    /**
     * Process session and generate feedback
     */
    process(session: AnalyzedSession): Promise<FeedbackEntry>;
    /**
     * Process multiple sessions
     */
    processBatch(sessions: AnalyzedSession[]): Promise<FeedbackEntry[]>;
    /**
     * Get success rate
     */
    getSuccessRate(): number;
    /**
     * Get recent feedback entries
     */
    getRecentFeedback(count?: number): FeedbackEntry[];
    /**
     * Get feedback statistics
     */
    getStats(): {
        totalFeedback: number;
        successRate: number;
        avgErrorCount: number;
        recentTrend: 'improving' | 'stable' | 'declining';
    };
    /**
     * Check if intervention is needed
     */
    needsIntervention(): boolean;
    /**
     * Get intervention suggestions
     */
    getInterventionSuggestions(): string[];
    /**
     * Reset feedback history
     */
    reset(): void;
    /**
     * Update configuration
     */
    updateConfig(config: Partial<FeedbackLoopConfig>): void;
}
//# sourceMappingURL=feedback-loop.d.ts.map