/**
 * Context Manager
 * Central coordinator for context monitoring, summarization, and eviction
 */
import type { OpenClawPluginApi } from 'openclaw/plugin-sdk';
import type { ContextMetrics, MonitorConfig, SummarizableItem, Summary } from './types.js';
import { ContextLevel } from './types.js';
export declare class ContextManager {
    private monitor;
    private summarizer;
    private evictionEngine;
    private api;
    private currentSummary?;
    private itemHistory;
    private lastSummaryTime;
    constructor(api: OpenClawPluginApi, config?: {
        monitor?: Partial<MonitorConfig>;
    });
    /**
     * Add an item to history for potential summarization
     */
    addItem(item: SummarizableItem): void;
    /**
     * Process current context state - called periodically
     */
    process(): Promise<{
        level: ContextLevel;
        metrics: ContextMetrics;
        tookAction: boolean;
        action?: string;
    }>;
    /**
     * Emergency eviction - remove low-value items immediately
     */
    private emergencyEviction;
    /**
     * Summarize old items and create summary
     */
    private summarize;
    /**
     * Report context state to SelfLearning module
     */
    private reportToSelfLearning;
    /**
     * Get current summary if available
     */
    getSummary(): Summary | undefined;
    /**
     * Get current context level
     */
    getLevel(): ContextLevel;
    /**
     * Force a summary (for manual triggering)
     */
    forceSummarize(): Summary | undefined;
    /**
     * Get item history count
     */
    getHistoryCount(): number;
}
//# sourceMappingURL=manager.d.ts.map