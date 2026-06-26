/**
 * Expert Weight Updater
 * Adjusts expert weights based on performance feedback
 */
export class ExpertWeightUpdater {
    orchestrator;
    adjustmentLog = [];
    constructor(orchestrator) {
        this.orchestrator = orchestrator;
    }
    /**
     * Update weights based on session analysis
     */
    async update(session) {
        const result = {
            success: false,
            adjustments: [],
            totalAdjusted: 0,
        };
        try {
            // Determine success/failure
            const hasErrors = session.errorIndicators.some(e => e.severity === 'high');
            const hasSuccesses = session.successIndicators.length > 0;
            const success = !hasErrors || hasSuccesses;
            // Update weights for each expert used
            for (const [expertId] of session.expertUsage) {
                const previousWeight = this.orchestrator.getExpertWeight(expertId);
                // Record feedback
                this.orchestrator.recordFeedback({
                    taskId: session.sessionId,
                    taskType: session.workflowType,
                    success,
                    durationMs: 0,
                    expertId,
                    rating: success ? 5 : 3,
                });
                const newWeight = this.orchestrator.getExpertWeight(expertId);
                if (previousWeight !== newWeight) {
                    const adjustment = {
                        expertId,
                        previousWeight,
                        newWeight,
                        delta: newWeight - previousWeight,
                        reason: success ? 'Positive feedback' : 'Negative feedback',
                    };
                    this.adjustmentLog.push(adjustment);
                    result.adjustments.push(adjustment);
                }
            }
            result.totalAdjusted = result.adjustments.length;
            result.success = true;
        }
        catch (error) {
            console.error('[ExpertWeightUpdater] Update failed:', error);
        }
        return result;
    }
    /**
     * Manually adjust weight for an expert
     */
    async manualAdjust(expertId, delta, reason) {
        const previousWeight = this.orchestrator.getExpertWeight(expertId);
        const newWeight = Math.max(0.1, Math.min(1.5, previousWeight + delta));
        // Record as feedback with manual adjustment
        this.orchestrator.recordFeedback({
            taskId: 'manual-adjustment',
            taskType: 'manual',
            success: delta > 0,
            durationMs: 0,
            expertId,
            rating: delta > 0 ? 5 : 2,
            comments: reason,
        });
        const updatedWeight = this.orchestrator.getExpertWeight(expertId);
        const adjustment = {
            expertId,
            previousWeight,
            newWeight: updatedWeight,
            delta: updatedWeight - previousWeight,
            reason,
        };
        this.adjustmentLog.push(adjustment);
        return adjustment;
    }
    /**
     * Get weight report
     */
    getWeightReport() {
        const report = this.orchestrator.getWeightReport();
        return {
            roles: report.roles,
            recentAdjustments: this.adjustmentLog.slice(-5),
        };
    }
    /**
     * Get all expert weights
     */
    getAllWeights() {
        const weights = this.orchestrator.getAllWeights();
        return weights.map(w => ({
            expertId: w.expertId,
            role: w.role,
            weight: w.dynamicWeight,
        }));
    }
    /**
     * Get top performing experts
     */
    getTopExperts(count = 3) {
        return this.getAllWeights()
            .sort((a, b) => b.weight - a.weight)
            .slice(0, count);
    }
    /**
     * Get underperforming experts
     */
    getUnderperformingExperts(threshold = 0.8) {
        const weights = this.orchestrator.getAllWeights();
        const baseWeight = 1.0;
        return weights
            .filter(w => w.dynamicWeight < baseWeight * threshold)
            .map(w => ({
            expertId: w.expertId,
            role: w.role,
            weight: w.dynamicWeight,
        }));
    }
    /**
     * Reset weights to base values
     */
    resetWeights() {
        // In a real implementation, this would reset dynamic weights to base
        this.adjustmentLog = [];
    }
    /**
     * Get adjustment history
     */
    getAdjustmentHistory(count = 20) {
        return this.adjustmentLog.slice(-count);
    }
    /**
     * Get adjustment statistics
     */
    getStats() {
        const positive = this.adjustmentLog.filter(a => a.delta > 0);
        const negative = this.adjustmentLog.filter(a => a.delta < 0);
        return {
            totalAdjustments: this.adjustmentLog.length,
            positiveAdjustments: positive.length,
            negativeAdjustments: negative.length,
            avgPositiveDelta: positive.length > 0 ? positive.reduce((sum, a) => sum + a.delta, 0) / positive.length : 0,
            avgNegativeDelta: negative.length > 0 ? negative.reduce((sum, a) => sum + a.delta, 0) / negative.length : 0,
        };
    }
}
//# sourceMappingURL=expert-weight-updater.js.map