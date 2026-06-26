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

import * as fs from 'fs'
import * as path from 'path'
import { EffectScoreCalculator, ScoreAggregator, AutoScorer, type ScoringDecision, type ScoringOutcome, type ScoringScore } from './effect-scorer.js'
import { trackerLogger } from '../utils/logger.js'

// Re-export for external use
export type { ScoringDecision, ScoringOutcome, ScoringScore } from './effect-scorer.js'

interface Tracked {
  decision: ScoringDecision
  outcome?: ScoringOutcome
  score?: ScoringScore
  at: number
}

interface PersistedData {
  version: string
  tracked: [string, Tracked][]
  scoreHistory: ScoringScore[]
  savedAt: string
}

export class EffectTracker {
  private tracked: Map<string, Tracked> = new Map()
  private max = 1000
  private scoreHistory: ScoringScore[] = []
  private persistPath: string = './.eo-effect/tracker.json'
  private dirty = false
  private saveDebounceTimer: NodeJS.Timeout | null = null

  constructor(persistPath?: string) {
    if (persistPath) {
      this.persistPath = persistPath
    }
    this.load()
  }

  /**
   * Load data from disk
   */
  private load(): void {
    try {
      if (fs.existsSync(this.persistPath)) {
        const data = JSON.parse(fs.readFileSync(this.persistPath, 'utf-8')) as PersistedData
        if (data.tracked) {
          this.tracked = new Map(data.tracked)
        }
        if (data.scoreHistory) {
          this.scoreHistory = data.scoreHistory
        }
        trackerLogger.info(`Loaded ${this.tracked.size} decisions from disk`);
      }
    } catch (e) {
      console.warn('[EffectTracker] Failed to load from disk:', e)
    }
  }

  /**
   * Persist data to disk (debounced)
   */
  private persist(): void {
    this.dirty = true
    
    // Debounce saves (max once per second)
    if (this.saveDebounceTimer) {
      clearTimeout(this.saveDebounceTimer)
    }
    
    this.saveDebounceTimer = setTimeout(() => {
      this.saveNow()
    }, 1000)
  }

  /**
   * Save immediately
   */
  private saveNow(): void {
    if (!this.dirty) return
    this.dirty = false
    
    try {
      const dir = path.dirname(this.persistPath)
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true })
      }
      
      const data: PersistedData = {
        version: '3.0',
        tracked: Array.from(this.tracked.entries()),
        scoreHistory: this.scoreHistory.slice(-this.max), // Keep last max
        savedAt: new Date().toISOString(),
      }
      
      fs.writeFileSync(this.persistPath, JSON.stringify(data, null, 2))
      console.debug(`[EffectTracker] Saved ${this.tracked.size} decisions to disk`)
    } catch (e) {
      console.error('[EffectTracker] Failed to persist:', e)
    }
  }

  /**
   * Track a decision and its outcome, automatically calculate score
   */
  track(decision: ScoringDecision, outcome: ScoringOutcome): ScoringScore {
    const score = EffectScoreCalculator.calculate(decision, outcome)
    this.tracked.set(decision.id, { decision, outcome, score, at: Date.now() })
    this.scoreHistory.push(score)
    if (this.tracked.size > this.max) this.prune()
    if (this.scoreHistory.length > this.max) {
      this.scoreHistory = this.scoreHistory.slice(-this.max)
    }
    this.persist()
    return score
  }

  /**
   * Track with implicit feedback (no explicit outcome)
   */
  trackWithFeedback(decision: ScoringDecision, feedback: {
    userFeedback?: 'positive' | 'negative' | 'neutral'
    repeatedTask?: boolean
    taskAbandoned?: boolean
    quickApproval?: boolean
    modifications?: number
  }): ScoringScore {
    const implicitOutcome = AutoScorer.fromImplicitFeedback(decision, feedback)
    return this.track(decision, implicitOutcome)
  }

  /**
   * Get score for a specific decision
   */
  getScore(id: string): ScoringScore | undefined {
    return this.tracked.get(id)?.score
  }

  /**
   * Get recent scores
   */
  getRecentScores(limit = 50): ScoringScore[] {
    return this.scoreHistory.slice(-limit)
  }

  /**
   * Calculate average score (last 100 decisions)
   */
  avgScore(): number {
    const scores = this.getRecentScores(100)
    if (!scores.length) return 0
    return scores.reduce((s, sc) => s + sc.score, 0) / scores.length
  }

  /**
   * Calculate success rate (scores >= 70)
   */
  successRate(): number {
    const scores = this.getRecentScores(100)
    if (!scores.length) return 0
    return scores.filter(s => s.score >= 70).length / scores.length
  }

  /**
   * Get aggregated statistics
   */
  stats(): {
    total: number
    avgScore: number
    successRate: number
    grade: 'A' | 'B' | 'C' | 'D' | 'F'
    trend: 'improving' | 'stable' | 'declining'
    percentile: number
    scoreStats: { min: number; max: number; stdDev: number }
  } {
    const scores = this.getRecentScores(100)
    const agg = ScoreAggregator.aggregate(scores)
    return {
      total: this.tracked.size,
      avgScore: agg.avgScore,
      successRate: this.successRate(),
      grade: agg.grade,
      trend: agg.trend,
      percentile: agg.percentile,
      scoreStats: agg.stats,
    }
  }

  /**
   * Get scores by grade
   */
  getScoresByGrade(): Record<string, ScoringScore[]> {
    const byGrade: Record<string, ScoringScore[]> = { A: [], B: [], C: [], D: [], F: [] }
    for (const score of this.scoreHistory) {
      byGrade[score.grade].push(score)
    }
    return byGrade
  }

  /**
   * Prune oldest 10% of tracked items
   */
  private prune(): void {
    const entries = Array.from(this.tracked.entries())
      .sort((a, b) => a[1].at - b[1].at)
    entries.slice(0, Math.floor(this.max * 0.1))
      .forEach(([id]) => this.tracked.delete(id))
  }

  /**
   * Reset all tracked data
   */
  reset(): void {
    this.tracked.clear()
    this.scoreHistory = []
    this.persist()
    trackerLogger.info('Reset all data');
  }

  /**
   * Force save now (for testing)
   */
  forceSave(): void {
    this.saveNow()
  }

  /**
   * Export all scores as JSON (for debugging/analysis)
   */
  exportScores(): string {
    return JSON.stringify({
      scores: this.scoreHistory,
      stats: this.stats(),
      byGrade: this.getScoresByGrade(),
      exportedAt: Date.now(),
    }, null, 2)
  }
}

// Singleton instance (will load from default path)
export const effectTracker = new EffectTracker()
