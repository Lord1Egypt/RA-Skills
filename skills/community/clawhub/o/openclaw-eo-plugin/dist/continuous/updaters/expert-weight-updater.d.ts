/**
 * Expert Weight Updater
 * Adjusts expert weights based on performance feedback
 */
import { SelfLearningOrchestrator } from '../../self-learning/orchestrator.js';
import type { AnalyzedSession } from '../analyzers/session-analyzer.js';
export interface WeightAdjustment {
    expertId: string;
    previousWeight: number;
    newWeight: number;
    delta: number;
    reason: string;
}
export interface WeightUpdateResult {
    success: boolean;
    adjustments: WeightAdjustment[];
    totalAdjusted: number;
}
export declare class ExpertWeightUpdater {
    private orchestrator;
    private adjustmentLog;
    constructor(orchestrator: SelfLearningOrchestrator);
    /**
     * Update weights based on session analysis
     */
    update(session: AnalyzedSession): Promise<WeightUpdateResult>;
    /**
     * Manually adjust weight for an expert
     */
    manualAdjust(expertId: string, delta: number, reason: string): Promise<WeightAdjustment | null>;
    /**
     * Get weight report
     */
    getWeightReport(): {
        roles: Array<{
            role: string;
            base: number;
            dynamic: number;
            delta: number;
        }>;
        recentAdjustments: WeightAdjustment[];
    };
    /**
     * Get all expert weights
     */
    getAllWeights(): Array<{
        expertId: string;
        role: string;
        weight: number;
    }>;
    /**
     * Get top performing experts
     */
    getTopExperts(count?: number): Array<{
        expertId: string;
        role: string;
        weight: number;
    }>;
    /**
     * Get underperforming experts
     */
    getUnderperformingExperts(threshold?: number): Array<{
        expertId: string;
        role: string;
        weight: number;
    }>;
    /**
     * Reset weights to base values
     */
    resetWeights(): void;
    /**
     * Get adjustment history
     */
    getAdjustmentHistory(count?: number): WeightAdjustment[];
    /**
     * Get adjustment statistics
     */
    getStats(): {
        totalAdjustments: number;
        positiveAdjustments: number;
        negativeAdjustments: number;
        avgPositiveDelta: number;
        avgNegativeDelta: number;
    };
}
//# sourceMappingURL=expert-weight-updater.d.ts.map