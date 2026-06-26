/**
 * Context Monitor
 * Real-time monitoring of context usage with threshold alerts
 */
import type { OpenClawPluginApi } from 'openclaw/plugin-sdk';
import type { ContextMetrics, ContextThresholds, MonitorConfig } from './types.js';
import { ContextLevel } from './types.js';
export declare class ContextMonitor {
    private api;
    private thresholds;
    private lastCheckTime;
    private lastReportTime;
    private checkIntervalMs;
    private reportIntervalMs;
    private tokenLimit;
    constructor(api: OpenClawPluginApi, config?: Partial<MonitorConfig>);
    /**
     * Check if enough time has passed since last check
     */
    canCheck(): boolean;
    /**
     * Get current context metrics
     * Note: This is an approximation based on available APIs
     */
    getMetrics(): Promise<ContextMetrics>;
    /**
     * Determine context level based on usage
     */
    getLevel(usagePercent: number): ContextLevel;
    /**
     * Check context and return current state
     */
    check(): Promise<{
        metrics: ContextMetrics;
        level: ContextLevel;
        shouldReport: boolean;
    }>;
    /**
     * Get thresholds
     */
    getThresholds(): ContextThresholds;
    /**
     * Update thresholds dynamically
     */
    updateThresholds(thresholds: Partial<ContextThresholds>): void;
}
//# sourceMappingURL=monitor.d.ts.map