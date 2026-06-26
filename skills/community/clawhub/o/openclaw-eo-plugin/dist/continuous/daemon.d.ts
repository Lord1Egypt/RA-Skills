export type DaemonStatus = 'starting' | 'running' | 'paused' | 'stopping' | 'stopped' | 'error';
export interface HealthMetrics {
    uptime: number;
    memoryUsage: number;
    cpuUsage: number;
    activeTasks: number;
    completedTasks: number;
    failedTasks: number;
    lastHeartbeat: number;
    errorCount: number;
    warnings: string[];
}
export interface DaemonConfig {
    healthCheckIntervalMs: number;
    maxMemoryMB: number;
    maxCpuPercent: number;
    autoRestartOnError: boolean;
    maxRestarts: number;
    restartDelayMs: number;
    enableMetrics: boolean;
    gracefulShutdownTimeoutMs: number;
}
export interface DaemonEvent {
    type: 'start' | 'stop' | 'error' | 'warning' | 'restart' | 'health_check';
    timestamp: number;
    message: string;
    details?: any;
}
export interface ScheduledTask {
    id: string;
    name: string;
    schedule: string;
    handler: () => Promise<void>;
    lastRun?: number;
    nextRun?: number;
    enabled: boolean;
}
export interface AlertConfig {
    enableEmail: boolean;
    enableWebhook: boolean;
    webhookUrl?: string;
    emailRecipients?: string[];
    minSeverity: 'info' | 'warning' | 'error' | 'critical';
}
declare class AutoRecoveryManager {
    private config;
    private restartCount;
    private lastRestartTime?;
    private errorHistory;
    constructor(config: DaemonConfig);
    /**
     * Record an error for recovery tracking.
     */
    recordError(error: string): void;
    /**
     * Check if auto-recovery should be attempted.
     */
    shouldAutoRestart(): boolean;
    /**
     * Attempt auto-recovery.
     */
    attemptRecovery(recoveryAction: () => Promise<void>): Promise<boolean>;
    /**
     * Reset restart counter (when system is stable).
     */
    reset(): void;
    /**
     * Get recovery status.
     */
    getStatus(): {
        restartCount: number;
        lastRestartTime?: number;
        recentErrors: string[];
    };
}
export declare class EODaemon {
    private config;
    private status;
    private healthMonitor;
    private scheduler;
    private recoveryManager;
    private alertConfig?;
    private heartbeatInterval?;
    constructor(config?: Partial<DaemonConfig>);
    /**
     * Start the daemon.
     */
    start(): Promise<void>;
    /**
     * Stop the daemon gracefully.
     */
    stop(): Promise<void>;
    /**
     * Restart the daemon.
     */
    restart(): Promise<void>;
    /**
     * Start periodic health checks.
     */
    private startHealthChecks;
    /**
     * Perform a single health check.
     */
    private performHealthCheck;
    /**
     * Handle unhealthy state.
     */
    private handleUnhealthy;
    /**
     * Get current health status.
     */
    getHealth(): HealthMetrics;
    /**
     * Get daemon status.
     */
    getStatus(): DaemonStatus;
    /**
     * Schedule a recurring task.
     */
    schedule(task: Omit<ScheduledTask, 'nextRun'>): void;
    /**
     * Unschedule a task.
     */
    unschedule(taskId: string): boolean;
    /**
     * Get scheduled tasks.
     */
    getScheduledTasks(): ScheduledTask[];
    /**
     * Configure alerts.
     */
    configureAlerts(config: AlertConfig): void;
    /**
     * Send an alert.
     */
    private sendAlert;
    /**
     * Get daemon metrics.
     */
    getMetrics(): {
        status: DaemonStatus;
        health: HealthMetrics;
        recovery: ReturnType<AutoRecoveryManager['getStatus']>;
        scheduledTasks: number;
        uptime: number;
    };
    /**
     * Get recent events.
     */
    getRecentEvents(count?: number): DaemonEvent[];
}
export declare const eoDaemon: EODaemon;
export default EODaemon;
//# sourceMappingURL=daemon.d.ts.map