// ============================================================================
// EO Self-Learning Orchestrator - Plugin Integration Wrapper
// 
// Simplified Self-Learning for OpenClaw plugin context.
// ============================================================================
import { selfLearningLogger as logger } from '../utils/logger.js';
export * from './types.js';
/**
 * Simplified Self-Learning Orchestrator for plugin context
 */
export class SelfLearningOrchestrator {
    config;
    workspace;
    feedback = [];
    patterns = [];
    weights = new Map();
    events = [];
    constructor(workspace, config) {
        this.workspace = workspace;
        this.config = {
            enabled: true,
            autoCollect: true,
            patternMining: true,
            weightAdjustment: true,
            ...config,
        };
        this.initializeWeights();
    }
    initializeWeights() {
        const expertRoles = [
            { expertId: 'plan-001', role: 'planner' },
            { expertId: 'arch-001', role: 'architect' },
            { expertId: 'fe-001', role: 'frontend' },
            { expertId: 'be-001', role: 'backend' },
            { expertId: 'qa-001', role: 'qa' },
            { expertId: 'sec-001', role: 'security' },
            { expertId: 'devops-001', role: 'devops' },
            { expertId: 'rev-001', role: 'reviewer' },
        ];
        for (const { expertId, role } of expertRoles) {
            this.weights.set(expertId, {
                expertId,
                role,
                baseWeight: 1.0,
                dynamicWeight: 1.0,
            });
        }
    }
    // ==========================================================================
    // Feedback Collection
    // ==========================================================================
    /**
     * Record feedback for a task
     */
    recordFeedback(feedback) {
        if (!this.config.enabled || !this.config.autoCollect) {
            return '';
        }
        const feedbackId = `fb-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
        this.feedback.push({
            ...feedback,
            taskId: feedbackId,
        });
        // Update weights based on feedback
        if (this.config.weightAdjustment && feedback.expertId) {
            this.adjustWeight(feedback.expertId, feedback.success);
        }
        this.logEvent('feedback_received', { feedbackId, taskId: feedback.taskId });
        return feedbackId;
    }
    /**
     * Adjust expert weight based on feedback
     */
    adjustWeight(expertId, success) {
        const weight = this.weights.get(expertId);
        if (!weight)
            return;
        const delta = success ? 0.05 : -0.05;
        weight.dynamicWeight = Math.max(0.1, Math.min(1.5, weight.dynamicWeight + delta));
        this.weights.set(expertId, weight);
        this.logEvent('weight_adjusted', { expertId, newWeight: weight.dynamicWeight });
    }
    // ==========================================================================
    // Pattern Mining
    // ==========================================================================
    /**
     * Mine patterns from feedback
     */
    minePatterns() {
        if (!this.config.enabled || !this.config.patternMining) {
            return [];
        }
        const newPatterns = [];
        // Analyze feedback for patterns
        const successCount = this.feedback.filter(f => f.success).length;
        const totalCount = this.feedback.length;
        const successRate = totalCount > 0 ? successCount / totalCount : 0;
        if (successRate > 0.8) {
            newPatterns.push({
                name: 'High Success Rate',
                description: `System maintains ${(successRate * 100).toFixed(0)}% success rate`,
                frequency: successCount,
                evidence: [`${successCount}/${totalCount} tasks succeeded`],
                severity: 'low',
            });
        }
        // Detect task type patterns
        const taskTypeCounts = new Map();
        for (const fb of this.feedback) {
            const count = taskTypeCounts.get(fb.taskType) || 0;
            taskTypeCounts.set(fb.taskType, count + 1);
        }
        for (const [taskType, count] of taskTypeCounts) {
            if (count >= 3) {
                newPatterns.push({
                    name: `${taskType} Task Pattern`,
                    description: `${taskType} tasks appear ${count} times in feedback`,
                    frequency: count,
                    evidence: [`${count} feedback entries for ${taskType}`],
                    severity: 'low',
                });
            }
        }
        this.patterns.push(...newPatterns);
        this.logEvent('patterns_mined', { count: newPatterns.length });
        return newPatterns;
    }
    // ==========================================================================
    // Batch Learning
    // ==========================================================================
    /**
     * Run batch learning cycle
     */
    async runBatchLearning() {
        if (!this.config.enabled) {
            return { patternsMined: 0, weightsAdjusted: 0, feedbackProcessed: 0 };
        }
        logger.info('Running batch learning...');
        // Mine patterns
        const newPatterns = this.minePatterns();
        // Count weight adjustments
        let weightsAdjusted = 0;
        for (const weight of this.weights.values()) {
            if (weight.baseWeight !== weight.dynamicWeight) {
                weightsAdjusted++;
            }
        }
        const result = {
            patternsMined: newPatterns.length,
            weightsAdjusted,
            feedbackProcessed: this.feedback.length,
        };
        this.logEvent('batch_learn_completed', result);
        return result;
    }
    // ==========================================================================
    // Expert Weight Queries
    // ==========================================================================
    /**
     * Get effective weight for an expert
     */
    getExpertWeight(expertId, taskType) {
        const weight = this.weights.get(expertId);
        if (!weight)
            return 1.0;
        return weight.dynamicWeight;
    }
    /**
     * Get all expert weights
     */
    getAllWeights() {
        return Array.from(this.weights.values());
    }
    /**
     * Get weight report
     */
    getWeightReport() {
        const roleMap = new Map();
        for (const weight of this.weights.values()) {
            const existing = roleMap.get(weight.role);
            if (existing) {
                existing.base = (existing.base + weight.baseWeight) / 2;
                existing.dynamic = (existing.dynamic + weight.dynamicWeight) / 2;
            }
            else {
                roleMap.set(weight.role, {
                    base: weight.baseWeight,
                    dynamic: weight.dynamicWeight,
                });
            }
        }
        return {
            roles: Array.from(roleMap.entries()).map(([role, values]) => ({
                role,
                base: values.base,
                dynamic: values.dynamic,
                delta: values.dynamic - values.base,
            })),
        };
    }
    // ==========================================================================
    // Statistics
    // ==========================================================================
    /**
     * Get system status
     */
    getStatus() {
        return {
            enabled: this.config.enabled,
            feedbackCount: this.feedback.length,
            patternCount: this.patterns.length,
            pendingAdjustments: this.patterns.filter(p => p.severity === 'high').length,
        };
    }
    /**
     * Get learning summary
     */
    getSummary() {
        const successCount = this.feedback.filter(f => f.success).length;
        const totalDuration = this.feedback.reduce((sum, f) => sum + f.durationMs, 0);
        const severityCounts = { low: 0, medium: 0, high: 0 };
        for (const p of this.patterns) {
            severityCounts[p.severity]++;
        }
        let totalDelta = 0;
        let adjustedCount = 0;
        for (const w of this.weights.values()) {
            if (w.baseWeight !== w.dynamicWeight) {
                totalDelta += Math.abs(w.dynamicWeight - w.baseWeight);
                adjustedCount++;
            }
        }
        return {
            feedbackStats: {
                total: this.feedback.length,
                successRate: this.feedback.length > 0 ? successCount / this.feedback.length : 0,
                avgDurationMs: this.feedback.length > 0 ? totalDuration / this.feedback.length : 0,
            },
            patternStats: {
                total: this.patterns.length,
                bySeverity: severityCounts,
            },
            weightStats: {
                adjusted: adjustedCount,
                avgDelta: adjustedCount > 0 ? totalDelta / adjustedCount : 0,
            },
        };
    }
    // ==========================================================================
    // Logging
    // ==========================================================================
    logEvent(type, data) {
        const event = {
            id: `evt-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
            type: type,
            timestamp: Date.now(),
            data,
            metadata: { automatic: true },
        };
        this.events.push(event);
        logger.debug(`Event: ${type}`, data);
    }
    /**
     * Get recent events
     */
    getRecentEvents(count = 10) {
        return this.events.slice(-count);
    }
}
// ============================================================================
// Factory
// ============================================================================
let defaultOrchestrator = null;
export function getSelfLearningOrchestrator(workspace) {
    if (!defaultOrchestrator) {
        defaultOrchestrator = new SelfLearningOrchestrator(workspace);
    }
    return defaultOrchestrator;
}
export function resetSelfLearningOrchestrator() {
    defaultOrchestrator = null;
}
//# sourceMappingURL=orchestrator.js.map