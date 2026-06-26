/**
 * Dream Trigger
 * Triggers Dream analysis based on accumulated errors or thresholds
 */
import { logger } from '../../utils/logger.js';
export class DreamTrigger {
    engine;
    errorCount;
    sessionCount;
    lastTriggerTime = 0;
    triggerHistory = [];
    constructor(engine, initialErrorCount = 0) {
        this.engine = engine;
        this.errorCount = initialErrorCount;
        this.sessionCount = 0;
    }
    /**
     * Trigger Dream analysis
     */
    async trigger(trigger) {
        const startTime = Date.now();
        try {
            logger.info(`Triggering dream: ${trigger.type}`);
            const result = await this.engine.executeDream(trigger);
            if (result.success) {
                this.lastTriggerTime = Date.now();
                this.triggerHistory.push({
                    timestamp: Date.now(),
                    type: trigger.type,
                    success: true,
                });
                return {
                    triggered: true,
                    reason: trigger.type,
                    reportId: result.report?.id,
                    durationMs: result.durationMs,
                };
            }
            else {
                this.triggerHistory.push({
                    timestamp: Date.now(),
                    type: trigger.type,
                    success: false,
                });
                return {
                    triggered: false,
                    reason: trigger.type,
                    error: result.error,
                };
            }
        }
        catch (error) {
            const errorMsg = error instanceof Error ? error.message : String(error);
            console.error(`[DreamTrigger] Trigger failed: ${errorMsg}`);
            return {
                triggered: false,
                reason: trigger.type,
                error: errorMsg,
                durationMs: Date.now() - startTime,
            };
        }
    }
    /**
     * Check if Dream should be triggered based on thresholds
     */
    shouldTrigger(config) {
        const now = Date.now();
        // Check if we're within the time window
        const withinTimeWindow = now - this.lastTriggerTime < config.timeWindowMs;
        if (withinTimeWindow && this.lastTriggerTime > 0) {
            return false;
        }
        // Check error threshold
        if (this.errorCount >= config.errorCount) {
            return true;
        }
        // Check session count threshold
        if (this.sessionCount >= config.sessionCount) {
            return true;
        }
        return false;
    }
    /**
     * Increment error counter
     */
    incrementError() {
        this.errorCount++;
        logger.debug(`Error count: ${this.errorCount}`);
    }
    /**
     * Increment session counter
     */
    incrementSession() {
        this.sessionCount++;
    }
    /**
     * Reset counters
     */
    resetCounters() {
        this.errorCount = 0;
        this.sessionCount = 0;
    }
    /**
     * Set error count directly
     */
    setErrorCount(count) {
        this.errorCount = count;
    }
    /**
     * Get current error count
     */
    getErrorCount() {
        return this.errorCount;
    }
    /**
     * Get Dream status
     */
    getStatus() {
        return {
            errorCount: this.errorCount,
            sessionCount: this.sessionCount,
            lastTrigger: this.lastTriggerTime || null,
            triggerHistoryLength: this.triggerHistory.length,
            pendingReports: this.engine.getPendingPatches().length,
        };
    }
    /**
     * Get recent trigger history
     */
    getRecentTriggers(count = 5) {
        return this.triggerHistory.slice(-count);
    }
    /**
     * Check if Dream is available
     */
    isAvailable() {
        return true; // In plugin context, Dream is always available
    }
    /**
     * Get dream reports
     */
    getReports() {
        return this.engine.listReports();
    }
    /**
     * Get pending patches from Dream
     */
    getPendingPatches() {
        return this.engine.getPendingPatches();
    }
}
//# sourceMappingURL=dream-trigger.js.map