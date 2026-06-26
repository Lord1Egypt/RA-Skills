/**
 * Dream Trigger
 * Triggers Dream analysis based on accumulated errors or thresholds
 */
import { DreamEngine, type DreamTrigger as DreamTriggerType } from '../../dream/dream-engine.js';
export interface DreamTriggerResult {
    triggered: boolean;
    reason?: string;
    reportId?: string;
    durationMs?: number;
    error?: string;
}
export interface DreamThresholdConfig {
    errorCount: number;
    sessionCount: number;
    timeWindowMs: number;
}
export declare class DreamTrigger {
    private engine;
    private errorCount;
    private sessionCount;
    private lastTriggerTime;
    private triggerHistory;
    constructor(engine: DreamEngine, initialErrorCount?: number);
    /**
     * Trigger Dream analysis
     */
    trigger(trigger: DreamTriggerType): Promise<DreamTriggerResult>;
    /**
     * Check if Dream should be triggered based on thresholds
     */
    shouldTrigger(config: DreamThresholdConfig): boolean;
    /**
     * Increment error counter
     */
    incrementError(): void;
    /**
     * Increment session counter
     */
    incrementSession(): void;
    /**
     * Reset counters
     */
    resetCounters(): void;
    /**
     * Set error count directly
     */
    setErrorCount(count: number): void;
    /**
     * Get current error count
     */
    getErrorCount(): number;
    /**
     * Get Dream status
     */
    getStatus(): {
        errorCount: number;
        sessionCount: number;
        lastTrigger: number | null;
        triggerHistoryLength: number;
        pendingReports: number;
    };
    /**
     * Get recent trigger history
     */
    getRecentTriggers(count?: number): Array<{
        timestamp: number;
        type: string;
        success: boolean;
    }>;
    /**
     * Check if Dream is available
     */
    isAvailable(): boolean;
    /**
     * Get dream reports
     */
    getReports(): {
        date: string;
        summary: string;
    }[];
    /**
     * Get pending patches from Dream
     */
    getPendingPatches(): import("../../dream/dream-engine.js").EvolutionOperation[];
}
//# sourceMappingURL=dream-trigger.d.ts.map