/**
 * Continuous Learning Loop Engine
 * Connects Dream, RAG, and SelfLearning into an automated cycle
 */
import type { OpenClawPluginApi } from 'openclaw/plugin-sdk';
export interface LoopConfig {
    enabled: boolean;
    sessionEndTrigger: boolean;
    periodicTrigger: boolean;
    periodicIntervalMs: number;
    dreamThreshold: number;
    maxPatternsPerCycle: number;
}
export interface LoopResult {
    success: boolean;
    sessionAnalyzed: boolean;
    patternsExtracted: number;
    ragUpdated: boolean;
    weightsAdjusted: number;
    dreamTriggered: boolean;
    durationMs: number;
    errors: string[];
}
export declare class ContinuousLoopEngine {
    private api;
    private config;
    private rag;
    private orchestrator;
    private dream;
    private scheduler;
    private sessionAnalyzer;
    private patternExtractor;
    private feedbackLoop;
    private ragUpdater;
    private weightUpdater;
    private dreamTrigger;
    private errorCount;
    constructor(api: OpenClawPluginApi, workspace: string);
    /**
     * Execute the continuous learning loop for a session end event
     */
    execute(event: {
        toolsUsed?: string[];
        messageCount?: number;
        lastMessage?: string;
        context?: Record<string, unknown>;
    }): Promise<LoopResult>;
    /**
     * Execute periodic dream cycle
     */
    executePeriodicDream(): Promise<void>;
    /**
     * Increment error counter (called when errors occur)
     */
    incrementError(): void;
    /**
     * Get engine status
     */
    getStatus(): {
        enabled: boolean;
        errorCount: number;
        schedulerActive: boolean;
        dreamAvailable: boolean;
        ragChunkCount: number;
        orchestratorStatus: {
            enabled: boolean;
            feedbackCount: number;
        };
    };
    /**
     * Update configuration
     */
    updateConfig(config: Partial<LoopConfig>): void;
    /**
     * Reset error counter
     */
    resetErrors(): void;
}
export declare function createContinuousLoop(api: OpenClawPluginApi, workspace: string): ContinuousLoopEngine;
export declare function resetContinuousLoop(): void;
//# sourceMappingURL=loop-engine.d.ts.map