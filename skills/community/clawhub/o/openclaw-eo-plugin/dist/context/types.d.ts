/**
 * Context Module Types
 * Type definitions for proactive context management
 */
export interface ContextMetrics {
    /** Current token count (approximate) */
    tokenCount: number;
    /** Token limit threshold */
    tokenLimit: number;
    /** Usage percentage 0-100 */
    usagePercent: number;
    /** Message count in current session */
    messageCount: number;
    /** Timestamp of last check */
    timestamp: number;
}
export interface ContextThresholds {
    warning: number;
    compress: number;
    critical: number;
}
export declare const DEFAULT_THRESHOLDS: ContextThresholds;
export declare enum ContextLevel {
    NORMAL = "normal",
    WARNING = "warning",
    COMPRESS = "compress",
    CRITICAL = "critical"
}
export interface SummarizableItem {
    id: string;
    type: 'message' | 'tool_call' | 'result' | 'system';
    content: string;
    timestamp: number;
    importance: number;
    keyInfo?: string[];
}
export interface Summary {
    id: string;
    originalCount: number;
    condensedCount: number;
    keyPoints: string[];
    preservedDecisions: string[];
    userPreferences: Record<string, string>;
    currentTaskState: string;
    timestamp: number;
}
export interface EvictionCandidate {
    item: SummarizableItem;
    score: number;
    reason: string;
}
export interface EvictionPolicy {
    name: string;
    minImportance: number;
    maxAge: number;
    preserveRecent: number;
}
export declare const DEFAULT_EVICTION_POLICY: EvictionPolicy;
export interface ContextState {
    metrics: ContextMetrics;
    level: ContextLevel;
    recentSummary?: Summary;
    pendingItems: SummarizableItem[];
    lastReportTime: number;
}
export interface MonitorConfig {
    thresholds: ContextThresholds;
    checkIntervalMs: number;
    reportIntervalMs: number;
}
//# sourceMappingURL=types.d.ts.map