/**
 * Memory Auto-Trigger System
 *
 * Provides deterministic (LLM-independent) memory triggers based on rules.
 * These triggers fire automatically without requiring LLM judgment.
 *
 * Triggers are categorized as:
 * - Event-based: session_start, session_end, task_complete, error, etc.
 * - Keyword-based: user explicitly says "记住", "record", etc.
 * - Threshold-based: context usage > 70%, repeated failures, etc.
 */
import type { OpenClawPluginApi } from 'openclaw/plugin-sdk';
export interface AutoTriggerConfig {
    enabled: boolean;
    triggers: TriggerRule[];
    explicitKeywords: string[];
    thresholds: ThresholdRule[];
}
export interface TriggerRule {
    id: string;
    name: string;
    event: TriggerEvent;
    action: TriggerAction;
    enabled: boolean;
    priority: 'high' | 'low';
    metadata?: Record<string, unknown>;
}
export type TriggerEvent = 'session_start' | 'session_end' | 'task_complete' | 'task_failed' | 'error' | 'gateway_restart' | 'explicit_keyword' | 'context_threshold' | 'pattern_detected';
export interface TriggerAction {
    type: 'archive_session' | 'record_decision' | 'record_lesson' | 'sync_memory' | 'notify' | 'custom';
    params?: Record<string, unknown>;
}
export interface ThresholdRule {
    id: string;
    name: string;
    metric: ThresholdMetric;
    operator: 'gt' | 'lt' | 'eq';
    value: number;
    action: TriggerAction;
    enabled: boolean;
}
export type ThresholdMetric = 'context_usage_percent' | 'error_rate' | 'response_time_ms' | 'task_queue_depth' | 'session_count';
export declare class MemoryAutoTrigger {
    private config;
    private api;
    private workspaceRoot;
    private memoryPath;
    constructor(api: OpenClawPluginApi, workspaceRoot: string, config?: Partial<AutoTriggerConfig>);
    /**
     * Check if message contains explicit memory keywords
     */
    hasExplicitKeyword(message: string): boolean;
    /**
     * Extract explicit memory content from message
     */
    extractExplicitContent(message: string): string | null;
    /**
     * Check if event matches any trigger conditions
     */
    matchTrigger(event: TriggerEvent, metadata?: Record<string, unknown>): TriggerRule | null;
    /**
     * Check threshold conditions
     */
    checkThresholds(metrics: Record<ThresholdMetric, number>): ThresholdRule[];
    /**
     * Execute trigger action
     */
    executeAction(action: TriggerAction, context: Record<string, unknown>): Promise<void>;
    /**
     * Archive current session (called on session_end)
     */
    private archiveCurrentSession;
    /**
     * Record a decision to MEMORY.md
     */
    private recordDecision;
    /**
     * Record a lesson (from task failure or error)
     */
    private recordLesson;
    /**
     * Sync current state to memory
     */
    private syncToMemory;
    /**
     * Process an incoming event - main entry point
     */
    processEvent(event: TriggerEvent, metadata?: Record<string, unknown>): Promise<void>;
    /**
     * Get current config
     */
    getConfig(): AutoTriggerConfig;
    /**
     * Update config
     */
    updateConfig(updates: Partial<AutoTriggerConfig>): void;
    /**
     * Add a custom trigger
     */
    addTrigger(rule: TriggerRule): void;
}
export declare function createMemoryAutoTrigger(api: OpenClawPluginApi, workspaceRoot: string, config?: Partial<AutoTriggerConfig>): MemoryAutoTrigger;
export declare function getMemoryAutoTrigger(): MemoryAutoTrigger | null;
//# sourceMappingURL=auto-trigger.d.ts.map