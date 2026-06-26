/**
 * Context Manager
 * Central coordinator for context monitoring, summarization, and eviction
 */
import { ContextLevel } from './types.js';
import { ContextMonitor } from './monitor.js';
import { ContextSummarizer } from './summarizer.js';
import { EvictionPolicyEngine } from './eviction-policy.js';
export class ContextManager {
    monitor;
    summarizer;
    evictionEngine;
    api;
    currentSummary;
    itemHistory = [];
    lastSummaryTime = 0;
    constructor(api, config) {
        this.api = api;
        this.monitor = new ContextMonitor(api, config?.monitor);
        this.summarizer = new ContextSummarizer();
        this.evictionEngine = new EvictionPolicyEngine();
    }
    /**
     * Add an item to history for potential summarization
     */
    addItem(item) {
        this.itemHistory.push(item);
        this.api.logger.debug(`[ContextManager] Added item: ${item.type} (importance: ${item.importance})`);
    }
    /**
     * Process current context state - called periodically
     */
    async process() {
        const { metrics, level, shouldReport } = await this.monitor.check();
        let tookAction = false;
        let action;
        switch (level) {
            case ContextLevel.CRITICAL:
                // Emergency eviction
                action = await this.emergencyEviction();
                tookAction = true;
                this.api.logger.warn(`[ContextManager] CRITICAL: ${action}`);
                break;
            case ContextLevel.COMPRESS:
                // Summarize old items
                if (Date.now() - this.lastSummaryTime > 60000) { // Max once per minute
                    action = await this.summarize();
                    tookAction = true;
                    this.api.logger.info(`[ContextManager] COMPRESS: ${action}`);
                }
                break;
            case ContextLevel.WARNING:
                // Log warning, maybe pre-emptively summarize
                this.api.logger.info(`[ContextManager] WARNING: Context at ${metrics.usagePercent.toFixed(1)}%`);
                break;
            default:
                // Normal - no action needed
                break;
        }
        // Report to SelfLearning if needed
        if (shouldReport) {
            this.reportToSelfLearning(metrics, level);
        }
        return { level, metrics, tookAction, action };
    }
    /**
     * Emergency eviction - remove low-value items immediately
     */
    async emergencyEviction() {
        const targetItems = this.itemHistory.filter(i => i.importance < 50);
        const count = Math.min(targetItems.length, Math.ceil(this.itemHistory.length * 0.3));
        const toEvict = this.evictionEngine.selectForEviction(this.itemHistory, 0.3);
        const evictedCount = toEvict.length;
        // Remove evicted items from history
        const evictIds = new Set(toEvict.map(i => i.id));
        this.itemHistory = this.itemHistory.filter(i => !evictIds.has(i.id));
        return `Evicted ${evictedCount} items (emergency)`;
    }
    /**
     * Summarize old items and create summary
     */
    async summarize() {
        if (this.itemHistory.length < 10) {
            return 'Not enough items to summarize';
        }
        const oldItems = this.itemHistory.slice(0, -5); // Keep last 5
        this.currentSummary = this.summarizer.summarize(oldItems);
        this.lastSummaryTime = Date.now();
        // Remove summarized items but keep recent ones
        this.itemHistory = this.itemHistory.slice(-5);
        this.api.logger.info(`[ContextManager] Summarized ${this.currentSummary.originalCount} items ` +
            `-> ${this.currentSummary.condensedCount} key points`);
        return `Summarized ${this.currentSummary.originalCount} items into ${this.currentSummary.keyPoints.length} key points`;
    }
    /**
     * Report context state to SelfLearning module
     */
    reportToSelfLearning(metrics, level) {
        // This would integrate with the SelfLearning module
        // For now, just log
        this.api.logger.debug(`[ContextManager] Report: level=${level}, usage=${metrics.usagePercent.toFixed(1)}%, ` +
            `messages=${metrics.messageCount}`);
    }
    /**
     * Get current summary if available
     */
    getSummary() {
        return this.currentSummary;
    }
    /**
     * Get current context level
     */
    getLevel() {
        return this.monitor.getLevel(100); // Would need actual metrics
    }
    /**
     * Force a summary (for manual triggering)
     */
    forceSummarize() {
        if (this.itemHistory.length >= 10) {
            const oldItems = this.itemHistory.slice(0, -5);
            this.currentSummary = this.summarizer.summarize(oldItems);
            this.lastSummaryTime = Date.now();
            this.itemHistory = this.itemHistory.slice(-5);
        }
        return this.currentSummary;
    }
    /**
     * Get item history count
     */
    getHistoryCount() {
        return this.itemHistory.length;
    }
}
//# sourceMappingURL=manager.js.map