/**
 * Cron Manager - Manages OpenClaw cron jobs
 *
 * Provides programmatic cron job management for EO scheduling
 */
export interface CronJob {
    id: string;
    name: string;
    description?: string;
    enabled: boolean;
    createdAtMs: number;
    updatedAtMs: number;
    schedule: {
        kind: 'cron' | 'interval';
        expr?: string;
        tz?: string;
        everyMs?: number;
    };
    sessionTarget: 'isolated' | 'current' | 'background';
    wakeMode: 'now' | 'keepAwake';
    payload: {
        kind: 'agentTurn' | 'script';
        message?: string;
        script?: string;
        timeoutSeconds?: number;
    };
    delivery?: {
        mode: 'announce' | 'silent' | 'webhook';
        channel?: string;
        webhookUrl?: string;
    };
    state?: {
        lastRunAtMs?: number;
        lastRunStatus?: 'success' | 'error' | 'timeout';
        lastStatus?: 'success' | 'error' | 'timeout';
        lastDurationMs?: number;
        lastDeliveryStatus?: string;
        consecutiveErrors?: number;
        lastError?: string;
    };
}
export interface CronManagerStats {
    totalJobs: number;
    enabledJobs: number;
    disabledJobs: number;
    jobsByStatus: Record<string, number>;
}
/**
 * CronManager class for managing OpenClaw cron jobs
 */
export declare class CronManager {
    private jobsPath;
    constructor(jobsPath?: string);
    /**
     * Load all cron jobs from the config file
     */
    loadJobs(): Promise<CronJob[]>;
    /**
     * Save jobs back to the config file
     */
    saveJobs(jobs: CronJob[]): Promise<void>;
    /**
     * Get a specific job by ID
     */
    getJob(id: string): Promise<CronJob | undefined>;
    /**
     * Create a new cron job
     */
    createJob(job: Omit<CronJob, 'id' | 'createdAtMs' | 'updatedAtMs'>): Promise<CronJob>;
    /**
     * Update an existing job
     */
    updateJob(id: string, updates: Partial<CronJob>): Promise<CronJob | undefined>;
    /**
     * Delete a job by ID
     */
    deleteJob(id: string): Promise<boolean>;
    /**
     * Enable a job
     */
    enableJob(id: string): Promise<boolean>;
    /**
     * Disable a job
     */
    disableJob(id: string): Promise<boolean>;
    /**
     * Get statistics about all jobs
     */
    getStats(): Promise<CronManagerStats>;
    /**
     * List all jobs with optional filter
     */
    listJobs(filter?: {
        enabled?: boolean;
        nameContains?: string;
    }): Promise<CronJob[]>;
    /**
     * Validate a cron expression
     */
    validateCronExpr(expr: string): boolean;
    /**
     * Generate a unique job ID
     */
    private generateId;
}
export declare const cronManager: CronManager;
//# sourceMappingURL=cron-manager.d.ts.map