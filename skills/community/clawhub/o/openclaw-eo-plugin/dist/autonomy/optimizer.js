/**
 * Self Optimizer v2 - Optimizes based on scored outcomes
 *
 * Part of the self-optimization loop:
 * Decision → Execute → Track → Score → Optimize → Evolve
 *
 * Uses EffectScore data to make intelligent optimization decisions
 */
import { effectTracker } from './effect-tracker.js';
export class SelfOptimizer {
    lastOpt = 0;
    cooldown = 3600000; // 1 hour
    currentStrategy = 'balanced';
    optimizationHistory = [];
    /**
     * Main optimization entry point
     * Call this after collecting sufficient effect scores
     */
    async optimize() {
        const now = Date.now();
        // Check cooldown
        if (now - this.lastOpt < this.cooldown) {
            const remainingMs = this.cooldown - (now - this.lastOpt);
            return {
                improvedParameters: [],
                averageScoreImprovement: 0,
                recommendations: [`优化冷却中，还需 ${Math.ceil(remainingMs / 60000)} 分钟`],
            };
        }
        this.lastOpt = now;
        const stats = effectTracker.stats();
        const recommendations = [];
        const improved = [];
        // Check sample size
        if (stats.total < 10) {
            recommendations.push(`样本不足 (${stats.total}/10)，需要更多决策来优化`);
            return { improvedParameters: [], averageScoreImprovement: 0, recommendations };
        }
        // Score-based optimization rules
        if (stats.avgScore < 50) {
            recommendations.push('🚨 效果极差，建议切换到保守策略');
            improved.push('strategy:conservative');
            this.applyStrategy('conservative');
        }
        else if (stats.avgScore < 70) {
            recommendations.push('⚠️ 效果较差，建议优化参数');
            const params = this.optimizeParams(stats);
            improved.push(...params);
        }
        else if (stats.avgScore >= 85 && stats.successRate > 0.8) {
            recommendations.push('✅ 效果优秀，可尝试激进策略');
            improved.push('strategy:aggressive');
            this.applyStrategy('aggressive');
        }
        else if (stats.avgScore >= 70 && stats.avgScore < 85) {
            recommendations.push('👍 效果良好，保持当前策略');
        }
        // Success rate checks
        if (stats.successRate < 0.5) {
            recommendations.push('❌ 成功率低于50%，建议增加确认步骤');
            improved.push('confirmation_threshold:0.3');
        }
        else if (stats.successRate > 0.9) {
            recommendations.push('🎯 成功率极高，可减少确认步骤提升效率');
            improved.push('confirmation_threshold:-0.1');
        }
        // Trend analysis
        if (stats.trend === 'declining') {
            recommendations.push('📉 趋势下降，建议检查最近决策质量');
            improved.push('investigate_recent_decline');
        }
        else if (stats.trend === 'improving') {
            recommendations.push('📈 趋势向好，继续当前策略');
        }
        // Grade distribution
        const gradeDist = effectTracker.getScoresByGrade();
        const failureRate = (gradeDist['D'].length + gradeDist['F'].length) / Math.max(1, stats.total);
        if (failureRate > 0.2) {
            recommendations.push('⚠️ 失败率较高 (' + (failureRate * 100).toFixed(1) + '%)，需要深入分析');
            improved.push('deep_analysis_required');
        }
        // Calculate improvement
        const avgScoreImprovement = this.calculateImprovement();
        return {
            improvedParameters: improved,
            averageScoreImprovement: avgScoreImprovement,
            recommendations,
        };
    }
    /**
     * Optimize specific parameters based on stats
     */
    optimizeParams(stats) {
        const improvements = [];
        // Check grade distribution
        const gradeDist = effectTracker.getScoresByGrade();
        const cGradeCount = gradeDist['C'].length;
        const dGradeCount = gradeDist['D'].length + gradeDist['F'].length;
        // If many C grades, try to improve
        if (cGradeCount > stats.total * 0.3) {
            improvements.push('optimize_c_grade_decisions');
        }
        // If D/F grades, need root cause analysis
        if (dGradeCount > 0) {
            improvements.push('analyze_failure_patterns');
        }
        // Check score variance (high variance = unstable)
        if (stats.scoreStats.stdDev > 20) {
            improvements.push('stabilize_decision_quality');
        }
        return improvements;
    }
    /**
     * Apply a specific strategy
     */
    applyStrategy(strategy) {
        this.currentStrategy = strategy;
    }
    /**
     * Calculate score improvement from last optimization
     */
    calculateImprovement() {
        const history = this.optimizationHistory;
        if (history.length < 2)
            return 0;
        const recent = history.slice(-3);
        if (recent.length < 2)
            return 0;
        const first = recent[0].scoreAfter;
        const last = recent[recent.length - 1].scoreAfter;
        return last - first;
    }
    /**
     * Get current strategy
     */
    getCurrentStrategy() {
        return this.currentStrategy;
    }
    /**
     * Get optimization history
     */
    getHistory() {
        return [...this.optimizationHistory];
    }
    /**
     * Force optimization (bypass cooldown)
     */
    async forceOptimize() {
        const prevCooldown = this.cooldown;
        this.cooldown = 0;
        const result = await this.optimize();
        this.cooldown = prevCooldown;
        return result;
    }
    /**
     * Get optimization recommendations as formatted string
     */
    async getRecommendations() {
        const result = await this.optimize();
        const parts = [];
        parts.push('## 优化建议');
        parts.push('');
        parts.push('平均分: ' + (result.averageScoreImprovement > 0 ? '+' : '') + result.averageScoreImprovement.toFixed(2));
        parts.push('当前策略: ' + this.currentStrategy);
        parts.push('');
        parts.push('建议:');
        for (const rec of result.recommendations) {
            parts.push('- ' + rec);
        }
        if (result.improvedParameters.length > 0) {
            parts.push('');
            parts.push('改进参数:');
            for (const param of result.improvedParameters) {
                parts.push('- ' + param);
            }
        }
        return parts.join('\n');
    }
}
export const selfOptimizer = new SelfOptimizer();
//# sourceMappingURL=optimizer.js.map