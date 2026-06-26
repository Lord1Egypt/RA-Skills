/**
 * Periodic Scheduler
 * Schedules and manages periodic tasks for the continuous learning loop
 */
export interface ScheduledTask {
    id: string;
    name: string;
    intervalMs: number;
    lastRun: number | null;
    nextRun: number;
    enabled: boolean;
    callback: () => Promise<void> | void;
}
export interface SchedulerConfig {
    enabled: boolean;
    defaultIntervalMs: number;
    maxConcurrentTasks: number;
}
export declare class PeriodicScheduler {
    private config;
    private tasks;
    private running;
    private intervalHandle;
    constructor(defaultIntervalMs?: number);
    /**
     * Schedule a periodic task
     */
    schedule(id: string, name: string, callback: () => Promise<void> | void, intervalMs?: number): ScheduledTask;
    /**
     * Unschedule a task
     */
    unschedule(id: string): boolean;
    /**
     * Enable a task
     */
    enable(id: string): boolean;
    /**
     * Disable a task
     */
    disable(id: string): boolean;
    /**
     * Start the scheduler
     */
    start(): void;
    /**
     * Stop the scheduler
     */
    stop(): void;
    /**
     * Check and run due tasks
     */
    private checkAndRunTasks;
    /**
     * Run a specific task immediately
     */
    runNow(id: string): Promise<boolean>;
    /**
     * Check if scheduler is running
     */
    isActive(): boolean;
    /**
     * Get task status
     */
    getTaskStatus(id: string): ScheduledTask | null;
    /**
     * Get all tasks
     */
    getAllTasks(): ScheduledTask[];
    /**
     * Get scheduler status
     */
    getStatus(): {
        running: boolean;
        taskCount: number;
        enabledTasks: number;
        tasks: Array<{
            id: string;
            name: string;
            enabled: boolean;
            lastRun: number | null;
            nextRun: number;
            overdue: boolean;
        }>;
    };
    /**
     * Update configuration
     */
    updateConfig(config: Partial<SchedulerConfig>): void;
    /**
     * Clear all tasks
     */
    clear(): void;
}
//# sourceMappingURL=periodic-scheduler.d.ts.map