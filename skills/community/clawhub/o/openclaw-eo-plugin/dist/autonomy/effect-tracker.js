/**
 * Effect Tracker v3 - Tracks decision outcomes with scoring + persistence
 *
 * Part of the self-optimization loop:
 * Decision → Execute → Track → Score → Optimize → Evolve
 *
 * Features:
 * - JSON file persistence (survives restarts)
 * - Automatic save on each track()
 * - Load on initialization
 */
import * as fs from 'fs';
import * as path from 'path';
import { EffectScoreCalculator, ScoreAggregator, AutoScorer } from './effect-scorer.js';
import { trackerLogger } from '../utils/logger.js';
export class EffectTracker {
    tracked = new Map();
    max = 1000;
    scoreHistory = [];
    persistPath = './.eo-effect/tracker.json';
    dirty = false;
    saveDebounceTimer = null;
    constructor(persistPath) {
        if (persistPath) {
            this.persistPath = persistPath;
        }
        this.load();
    }
    /**
     * Load data from disk
     */
    load() {
        try {
            if (fs.existsSync(this.persistPath)) {
                const data = JSON.parse(fs.readFileSync(this.persistPath, 'utf-8'));
                if (data.tracked) {
                    this.tracked = new Map(data.tracked);
                }
                if (data.scoreHistory) {
                    this.scoreHistory = data.scoreHistory;
                }
                trackerLogger.info(`Loaded ${this.tracked.size} decisions from disk`);
            }
        }
        catch (e) {
            console.warn('[EffectTracker] Failed to load from disk:', e);
        }
    }
    /**
     * Persist data to disk (debounced)
     */
    persist() {
        this.dirty = true;
        // Debounce saves (max once per second)
        if (this.saveDebounceTimer) {
            clearTimeout(this.saveDebounceTimer);
        }
        this.saveDebounceTimer = setTimeout(() => {
            this.saveNow();
        }, 1000);
    }
    /**
     * Save immediately
     */
    saveNow() {
        if (!this.dirty)
            return;
        this.dirty = false;
        try {
            const dir = path.dirname(this.persistPath);
            if (!fs.existsSync(dir)) {
                fs.mkdirSync(dir, { recursive: true });
            }
            const data = {
                version: '3.0',
                tracked: Array.from(this.tracked.entries()),
                scoreHistory: this.scoreHistory.slice(-this.max), // Keep last max
                savedAt: new Date().toISOString(),
            };
            fs.writeFileSync(this.persistPath, JSON.stringify(data, null, 2));
            console.debug(`[EffectTracker] Saved ${this.tracked.size} decisions to disk`);
        }
        catch (e) {
            console.error('[EffectTracker] Failed to persist:', e);
        }
    }
    /**
     * Track a decision and its outcome, automatically calculate score
     */
    track(decision, outcome) {
        const score = EffectScoreCalculator.calculate(decision, outcome);
        this.tracked.set(decision.id, { decision, outcome, score, at: Date.now() });
        this.scoreHistory.push(score);
        if (this.tracked.size > this.max)
            this.prune();
        if (this.scoreHistory.length > this.max) {
            this.scoreHistory = this.scoreHistory.slice(-this.max);
        }
        this.persist();
        return score;
    }
    /**
     * Track with implicit feedback (no explicit outcome)
     */
    trackWithFeedback(decision, feedback) {
        const implicitOutcome = AutoScorer.fromImplicitFeedback(decision, feedback);
        return this.track(decision, implicitOutcome);
    }
    /**
     * Get score for a specific decision
     */
    getScore(id) {
        return this.tracked.get(id)?.score;
    }
    /**
     * Get recent scores
     */
    getRecentScores(limit = 50) {
        return this.scoreHistory.slice(-limit);
    }
    /**
     * Calculate average score (last 100 decisions)
     */
    avgScore() {
        const scores = this.getRecentScores(100);
        if (!scores.length)
            return 0;
        return scores.reduce((s, sc) => s + sc.score, 0) / scores.length;
    }
    /**
     * Calculate success rate (scores >= 70)
     */
    successRate() {
        const scores = this.getRecentScores(100);
        if (!scores.length)
            return 0;
        return scores.filter(s => s.score >= 70).length / scores.length;
    }
    /**
     * Get aggregated statistics
     */
    stats() {
        const scores = this.getRecentScores(100);
        const agg = ScoreAggregator.aggregate(scores);
        return {
            total: this.tracked.size,
            avgScore: agg.avgScore,
            successRate: this.successRate(),
            grade: agg.grade,
            trend: agg.trend,
            percentile: agg.percentile,
            scoreStats: agg.stats,
        };
    }
    /**
     * Get scores by grade
     */
    getScoresByGrade() {
        const byGrade = { A: [], B: [], C: [], D: [], F: [] };
        for (const score of this.scoreHistory) {
            byGrade[score.grade].push(score);
        }
        return byGrade;
    }
    /**
     * Prune oldest 10% of tracked items
     */
    prune() {
        const entries = Array.from(this.tracked.entries())
            .sort((a, b) => a[1].at - b[1].at);
        entries.slice(0, Math.floor(this.max * 0.1))
            .forEach(([id]) => this.tracked.delete(id));
    }
    /**
     * Reset all tracked data
     */
    reset() {
        this.tracked.clear();
        this.scoreHistory = [];
        this.persist();
        trackerLogger.info('Reset all data');
    }
    /**
     * Force save now (for testing)
     */
    forceSave() {
        this.saveNow();
    }
    /**
     * Export all scores as JSON (for debugging/analysis)
     */
    exportScores() {
        return JSON.stringify({
            scores: this.scoreHistory,
            stats: this.stats(),
            byGrade: this.getScoresByGrade(),
            exportedAt: Date.now(),
        }, null, 2);
    }
}
// Singleton instance (will load from default path)
export const effectTracker = new EffectTracker();
//# sourceMappingURL=effect-tracker.js.map