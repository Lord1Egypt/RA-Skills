// ============================================================================
// EO Daemon Mode - Phase 4.1: Continuous Operation Architecture
//
// Implements background continuous operation, health monitoring,
// and automatic recovery.
// ============================================================================
// ============================================================================
// Types
// ============================================================================
import { logger } from '../utils/logger.js';
// ============================================================================
// Health Monitor
// ============================================================================
class HealthMonitor {
    config;
    metrics;
    startTime;
    events = [];
    maxEvents = 100;
    constructor(config) {
        this.config = config;
        this.startTime = Date.now();
        this.metrics = {
            uptime: 0,
            memoryUsage: 0,
            cpuUsage: 0,
            activeTasks: 0,
            completedTasks: 0,
            failedTasks: 0,
            lastHeartbeat: Date.now(),
            errorCount: 0,
            warnings: [],
        };
    }
    /**
     * Perform a health check.
     */
    check() {
        const now = Date.now();
        // Update basic metrics
        this.metrics.uptime = now - this.startTime;
        this.metrics.lastHeartbeat = now;
        // Get memory usage
        if (global.gc) {
            global.gc();
        }
        const memUsage = process.memoryUsage();
        this.metrics.memoryUsage = Math.round(memUsage.heapUsed / 1024 / 1024);
        // Check for issues
        this.metrics.warnings = [];
        if (this.metrics.memoryUsage > this.config.maxMemoryMB) {
            this.metrics.warnings.push(`Memory usage high: ${this.metrics.memoryUsage}MB`);
        }
        if (this.metrics.errorCount > 10) {
            this.metrics.warnings.push(`High error count: ${this.metrics.errorCount}`);
        }
        return { ...this.metrics };
    }
    /**
     * Record task completion.
     */
    recordCompletion(success) {
        if (success) {
            this.metrics.completedTasks++;
        }
        else {
            this.metrics.failedTasks++;
        }
    }
    /**
     * Increment active tasks.
     */
    incrementActive() {
        return ++this.metrics.activeTasks;
    }
    /**
     * Decrement active tasks.
     */
    decrementActive() {
        return Math.max(0, --this.metrics.activeTasks);
    }
    /**
     * Record an error.
     */
    recordError(error) {
        this.metrics.errorCount++;
        this.logEvent('error', error);
    }
    /**
     * Record a warning.
     */
    recordWarning(message) {
        this.metrics.warnings.push(message);
        this.logEvent('warning', message);
    }
    /**
     * Log an event.
     */
    logEvent(type, message, details) {
        this.events.push({
            type,
            timestamp: Date.now(),
            message,
            details,
        });
        // Trim old events
        if (this.events.length > this.maxEvents) {
            this.events = this.events.slice(-this.maxEvents);
        }
    }
    /**
     * Get recent events.
     */
    getRecentEvents(count = 20) {
        return this.events.slice(-count);
    }
    /**
     * Get metrics summary.
     */
    getMetrics() {
        return { ...this.metrics };
    }
    /**
     * Check if health is acceptable.
     */
    isHealthy() {
        return this.metrics.warnings.length === 0 &&
            this.metrics.memoryUsage < this.config.maxMemoryMB &&
            this.metrics.errorCount < 5;
    }
}
// ============================================================================
// Task Scheduler
// ============================================================================
class TaskScheduler {
    tasks = new Map();
    intervalId;
    config;
    constructor(config) {
        this.config = config;
    }
    /**
     * Add a scheduled task.
     */
    add(task) {
        const nextRun = this.calculateNextRun(task.schedule);
        this.tasks.set(task.id, { ...task, nextRun });
    }
    /**
     * Remove a scheduled task.
     */
    remove(taskId) {
        return this.tasks.delete(taskId);
    }
    /**
     * Enable/disable a task.
     */
    setEnabled(taskId, enabled) {
        const task = this.tasks.get(taskId);
        if (!task)
            return false;
        task.enabled = enabled;
        return true;
    }
    /**
     * Start the scheduler.
     */
    start() {
        if (this.intervalId)
            return;
        // Check every minute
        this.intervalId = setInterval(() => this.tick(), 60000);
    }
    /**
     * Stop the scheduler.
     */
    stop() {
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = undefined;
        }
    }
    /**
     * Execute a tick - check and run due tasks.
     */
    async tick() {
        const now = Date.now();
        for (const task of this.tasks.values()) {
            if (!task.enabled || !task.nextRun)
                continue;
            if (now >= task.nextRun) {
                try {
                    await task.handler();
                    task.lastRun = now;
                }
                catch (e) {
                    console.error(`Scheduled task ${task.name} failed:`, e);
                }
                // Calculate next run
                task.nextRun = this.calculateNextRun(task.schedule);
            }
        }
    }
    /**
     * Calculate next run time from cron-like expression.
     * Simplified: supports "daily", "hourly", "every:X:minutes"
     */
    calculateNextRun(schedule) {
        const now = Date.now();
        if (schedule === 'daily') {
            // Next midnight
            const tomorrow = new Date();
            tomorrow.setDate(tomorrow.getDate() + 1);
            tomorrow.setHours(0, 0, 0, 0);
            return tomorrow.getTime();
        }
        if (schedule === 'hourly') {
            // Next hour
            const next = new Date();
            next.setHours(next.getHours() + 1, 0, 0, 0);
            return next.getTime();
        }
        if (schedule.startsWith('every:')) {
            const minutes = parseInt(schedule.split(':')[1]);
            return now + minutes * 60 * 1000;
        }
        // Default: every 5 minutes
        return now + 5 * 60 * 1000;
    }
    /**
     * Get all scheduled tasks.
     */
    getTasks() {
        return Array.from(this.tasks.values());
    }
}
// ============================================================================
// Auto-Recovery Manager
// ============================================================================
class AutoRecoveryManager {
    config;
    restartCount = 0;
    lastRestartTime;
    errorHistory = [];
    constructor(config) {
        this.config = config;
    }
    /**
     * Record an error for recovery tracking.
     */
    recordError(error) {
        this.errorHistory.push({ time: Date.now(), error });
        // Keep only recent errors
        if (this.errorHistory.length > 20) {
            this.errorHistory = this.errorHistory.slice(-20);
        }
    }
    /**
     * Check if auto-recovery should be attempted.
     */
    shouldAutoRestart() {
        if (!this.config.autoRestartOnError)
            return false;
        if (this.restartCount >= this.config.maxRestarts)
            return false;
        // Check if we restarted recently
        if (this.lastRestartTime && Date.now() - this.lastRestartTime < 60000) {
            // Restarted within last minute - don't restart again
            return false;
        }
        return true;
    }
    /**
     * Attempt auto-recovery.
     */
    async attemptRecovery(recoveryAction) {
        if (!this.shouldAutoRestart())
            return false;
        this.restartCount++;
        this.lastRestartTime = Date.now();
        logger.warn(`Attempting recovery #${this.restartCount}`);
        try {
            await new Promise(resolve => setTimeout(resolve, this.config.restartDelayMs));
            await recoveryAction();
            return true;
        }
        catch (e) {
            console.error('[AutoRecovery] Recovery failed:', e);
            return false;
        }
    }
    /**
     * Reset restart counter (when system is stable).
     */
    reset() {
        this.restartCount = 0;
        this.errorHistory = [];
    }
    /**
     * Get recovery status.
     */
    getStatus() {
        return {
            restartCount: this.restartCount,
            lastRestartTime: this.lastRestartTime,
            recentErrors: this.errorHistory.slice(-5).map(e => e.error),
        };
    }
}
// ============================================================================
// Daemon (Main Class)
// ============================================================================
export class EODaemon {
    config;
    status;
    healthMonitor;
    scheduler;
    recoveryManager;
    alertConfig;
    heartbeatInterval;
    constructor(config) {
        this.config = {
            healthCheckIntervalMs: 30000,
            maxMemoryMB: 512,
            maxCpuPercent: 80,
            autoRestartOnError: true,
            maxRestarts: 3,
            restartDelayMs: 5000,
            enableMetrics: true,
            gracefulShutdownTimeoutMs: 10000,
            ...config,
        };
        this.status = 'stopped';
        this.healthMonitor = new HealthMonitor(this.config);
        this.scheduler = new TaskScheduler(this.config);
        this.recoveryManager = new AutoRecoveryManager(this.config);
    }
    // ============================================================================
    // Lifecycle
    // ============================================================================
    /**
     * Start the daemon.
     */
    async start() {
        if (this.status === 'running')
            return;
        this.status = 'starting';
        this.healthMonitor.logEvent('start', 'EO Daemon starting');
        try {
            // Start health monitor
            this.startHealthChecks();
            // Start task scheduler
            this.scheduler.start();
            this.status = 'running';
            this.healthMonitor.logEvent('start', 'EO Daemon started successfully');
            logger.info('EODaemon started successfully');
        }
        catch (error) {
            this.status = 'error';
            const errorMsg = error instanceof Error ? error.message : String(error);
            this.healthMonitor.recordError(errorMsg);
            this.healthMonitor.logEvent('error', 'Failed to start: ' + errorMsg);
            throw error;
        }
    }
    /**
     * Stop the daemon gracefully.
     */
    async stop() {
        if (this.status === 'stopped')
            return;
        this.status = 'stopping';
        this.healthMonitor.logEvent('stop', 'EO Daemon shutting down');
        // Clear intervals
        if (this.heartbeatInterval) {
            clearInterval(this.heartbeatInterval);
        }
        // Stop scheduler
        this.scheduler.stop();
        // Wait for active tasks
        const metrics = this.healthMonitor.getMetrics();
        if (metrics.activeTasks > 0) {
            logger.info(`Waiting for ${metrics.activeTasks} active tasks to complete...`);
            await new Promise(resolve => setTimeout(resolve, 5000));
        }
        this.status = 'stopped';
        this.healthMonitor.logEvent('stop', 'EO Daemon stopped');
        logger.info('EODaemon stopped');
    }
    /**
     * Restart the daemon.
     */
    async restart() {
        logger.info('EODaemon restarting...');
        await this.stop();
        await this.start();
    }
    // ============================================================================
    // Health Monitoring
    // ============================================================================
    /**
     * Start periodic health checks.
     */
    startHealthChecks() {
        this.heartbeatInterval = setInterval(() => {
            this.performHealthCheck();
        }, this.config.healthCheckIntervalMs);
    }
    /**
     * Perform a single health check.
     */
    performHealthCheck() {
        const health = this.healthMonitor.check();
        this.healthMonitor.logEvent('health_check', `Health check: memory=${health.memoryUsage}MB, errors=${health.errorCount}`);
        // Check if recovery is needed
        if (!this.healthMonitor.isHealthy()) {
            this.handleUnhealthy(health);
        }
    }
    /**
     * Handle unhealthy state.
     */
    async handleUnhealthy(health) {
        const reasons = health.warnings.join('; ');
        this.healthMonitor.recordWarning(`Unhealthy: ${reasons}`);
        this.healthMonitor.logEvent('warning', `Unhealthy state detected: ${reasons}`);
        if (this.recoveryManager.shouldAutoRestart()) {
            await this.recoveryManager.attemptRecovery(async () => {
                // Attempt garbage collection
                if (global.gc) {
                    global.gc();
                }
                // Restart daemon components
                logger.warn('Attempting self-recovery...');
            });
        }
    }
    /**
     * Get current health status.
     */
    getHealth() {
        return this.healthMonitor.check();
    }
    /**
     * Get daemon status.
     */
    getStatus() {
        return this.status;
    }
    // ============================================================================
    // Task Scheduling
    // ============================================================================
    /**
     * Schedule a recurring task.
     */
    schedule(task) {
        this.scheduler.add(task);
    }
    /**
     * Unschedule a task.
     */
    unschedule(taskId) {
        return this.scheduler.remove(taskId);
    }
    /**
     * Get scheduled tasks.
     */
    getScheduledTasks() {
        return this.scheduler.getTasks();
    }
    // ============================================================================
    // Event & Alert Handling
    // ============================================================================
    /**
     * Configure alerts.
     */
    configureAlerts(config) {
        this.alertConfig = config;
    }
    /**
     * Send an alert.
     */
    async sendAlert(severity, message) {
        if (!this.alertConfig)
            return;
        const severityOrder = { info: 0, warning: 1, error: 2, critical: 3 };
        if (severityOrder[severity] < severityOrder[this.alertConfig.minSeverity])
            return;
        logger.error(`EODaemon Alert: ${severity}: ${message}`);
        if (this.alertConfig.enableWebhook && this.alertConfig.webhookUrl) {
            try {
                await fetch(this.alertConfig.webhookUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ severity, message, timestamp: Date.now() }),
                });
            }
            catch (e) {
                console.error('[EODaemon] Failed to send webhook alert:', e);
            }
        }
    }
    // ============================================================================
    // Metrics
    // ============================================================================
    /**
     * Get daemon metrics.
     */
    getMetrics() {
        return {
            status: this.status,
            health: this.healthMonitor.getMetrics(),
            recovery: this.recoveryManager.getStatus(),
            scheduledTasks: this.scheduler.getTasks().length,
            uptime: this.healthMonitor.getMetrics().uptime,
        };
    }
    /**
     * Get recent events.
     */
    getRecentEvents(count = 20) {
        return this.healthMonitor.getRecentEvents(count);
    }
}
// ============================================================================
// Global Instance
// ============================================================================
export const eoDaemon = new EODaemon();
export default EODaemon;
//# sourceMappingURL=daemon.js.map