export * from './types.js';
export interface LearningConfig {
    enabled: boolean;
    autoCollect: boolean;
    patternMining: boolean;
    weightAdjustment: boolean;
}
export interface FeedbackData {
    taskId: string;
    taskType: string;
    success: boolean;
    durationMs: number;
    expertId?: string;
    rating?: number;
    comments?: string;
}
export interface PatternData {
    name: string;
    description: string;
    frequency: number;
    evidence: string[];
    severity: 'low' | 'medium' | 'high';
}
export interface ExpertWeight {
    expertId: string;
    role: string;
    baseWeight: number;
    dynamicWeight: number;
    taskType?: string;
}
/**
 * Simplified Self-Learning Orchestrator for plugin context
 */
export declare class SelfLearningOrchestrator {
    private config;
    private workspace;
    private feedback;
    private patterns;
    private weights;
    private events;
    constructor(workspace: string, config?: Partial<LearningConfig>);
    private initializeWeights;
    /**
     * Record feedback for a task
     */
    recordFeedback(feedback: FeedbackData): string;
    /**
     * Adjust expert weight based on feedback
     */
    private adjustWeight;
    /**
     * Mine patterns from feedback
     */
    minePatterns(): PatternData[];
    /**
     * Run batch learning cycle
     */
    runBatchLearning(): Promise<{
        patternsMined: number;
        weightsAdjusted: number;
        feedbackProcessed: number;
    }>;
    /**
     * Get effective weight for an expert
     */
    getExpertWeight(expertId: string, taskType?: string): number;
    /**
     * Get all expert weights
     */
    getAllWeights(): ExpertWeight[];
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
    };
    /**
     * Get system status
     */
    getStatus(): {
        enabled: boolean;
        feedbackCount: number;
        patternCount: number;
        pendingAdjustments: number;
    };
    /**
     * Get learning summary
     */
    getSummary(): {
        feedbackStats: {
            total: number;
            successRate: number;
            avgDurationMs: number;
        };
        patternStats: {
            total: number;
            bySeverity: Record<string, number>;
        };
        weightStats: {
            adjusted: number;
            avgDelta: number;
        };
    };
    private logEvent;
    /**
     * Get recent events
     */
    getRecentEvents(count?: number): LearningEvent[];
}
export interface LearningEvent {
    id: string;
    type: 'feedback_received' | 'weight_adjusted' | 'patterns_mined' | 'batch_learn_completed' | string;
    timestamp: number;
    data: Record<string, unknown>;
    metadata?: Record<string, unknown>;
}
export declare function getSelfLearningOrchestrator(workspace: string): SelfLearningOrchestrator;
export declare function resetSelfLearningOrchestrator(): void;
//# sourceMappingURL=orchestrator.d.ts.map