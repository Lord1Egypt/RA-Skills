/**
 * Dream Scheduler - Automates Dream Module triggers via cron
 *
 * Part of the self-optimization loop:
 * Decision → Execute → Track → Score → Optimize → Evolve (Dream)
 *
 * Provides:
 * - Daily Dream trigger (00:30)
 * - Idle-based Dream trigger (30min idle)
 * - Manual trigger interface
 */
export interface DreamSchedulerConfig {
    enabled: boolean;
    dailyTime?: string;
    idleTrigger?: boolean;
    idleTimeoutMs?: number;
    feishuChatId?: string;
}
export interface DreamResult {
    success: boolean;
    jobId?: string;
    message: string;
    error?: string;
}
/**
 * Dream Scheduler class
 */
export declare class DreamScheduler {
    private config;
    private dreamJobId;
    constructor(config?: Partial<DreamSchedulerConfig>);
    /**
     * Initialize the dream scheduler
     * Creates/updates the cron job for daily Dream trigger
     */
    initialize(): Promise<DreamResult>;
    /**
     * Build the Dream Module trigger message
     */
    private buildDreamMessage;
    /**
     * Manually trigger a Dream cycle
     */
    triggerNow(feishuChatId?: string): Promise<DreamResult>;
    /**
     * Send Dream evolution report to Feishu
     */
    private sendDreamReport;
    /**
     * Get the status of the Dream scheduler
     */
    getStatus(): Promise<{
        configured: boolean;
        jobId: string | null;
        nextRun: string | null;
        lastRun: string | null;
        enabled: boolean;
    }>;
    /**
     * Calculate approximate next run time from cron expression
     * Simplified - doesn't handle all cron cases
     */
    private calculateNextRun;
    /**
     * Disable the Dream scheduler
     */
    disable(): Promise<boolean>;
    /**
     * Enable the Dream scheduler
     */
    enable(): Promise<boolean>;
    /**
     * Remove the Dream scheduler
     */
    remove(): Promise<boolean>;
    /**
     * Update configuration
     */
    updateConfig(config: Partial<DreamSchedulerConfig>): void;
    /**
     * Get current configuration
     */
    getConfig(): DreamSchedulerConfig;
}
export declare const dreamScheduler: DreamScheduler;
//# sourceMappingURL=dream-scheduler.d.ts.map