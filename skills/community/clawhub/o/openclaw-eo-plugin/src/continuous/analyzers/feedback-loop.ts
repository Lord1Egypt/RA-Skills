/**
 * Feedback Loop
 * Processes feedback from sessions and feeds it back into the learning system
 */

import type { AnalyzedSession } from './session-analyzer.js'
import type { ExtractedPattern } from './pattern-extractor.js'

export interface FeedbackLoopConfig {
  enabled: boolean
  successThreshold: number
  errorThreshold: number
  autoAdjustWeights: boolean
}

export interface FeedbackEntry {
  id: string
  timestamp: number
  sessionId: string
  success: boolean
  errorCount: number
  patternCount: number
  weightAdjustment?: number
}

export class FeedbackLoop {
  private config: FeedbackLoopConfig
  private feedbackHistory: FeedbackEntry[] = []

  constructor(config?: Partial<FeedbackLoopConfig>) {
    this.config = {
      enabled: true,
      successThreshold: 0.7,
      errorThreshold: 3,
      autoAdjustWeights: true,
      ...config,
    }
  }

  /**
   * Process session and generate feedback
   */
  async process(session: AnalyzedSession): Promise<FeedbackEntry> {
    const hasErrors = session.errorIndicators.length > 0
    const hasSuccesses = session.successIndicators.length > 0
    const success = !hasErrors || hasSuccesses

    const entry: FeedbackEntry = {
      id: `fb-${Date.now()}`,
      timestamp: Date.now(),
      sessionId: session.sessionId,
      success,
      errorCount: session.errorIndicators.reduce((sum, e) => sum + e.count, 0),
      patternCount: session.keyTopics.length,
    }

    this.feedbackHistory.push(entry)
    return entry
  }

  /**
   * Process multiple sessions
   */
  async processBatch(sessions: AnalyzedSession[]): Promise<FeedbackEntry[]> {
    const entries: FeedbackEntry[] = []
    for (const session of sessions) {
      const entry = await this.process(session)
      entries.push(entry)
    }
    return entries
  }

  /**
   * Get success rate
   */
  getSuccessRate(): number {
    if (this.feedbackHistory.length === 0) return 0
    const successCount = this.feedbackHistory.filter(f => f.success).length
    return successCount / this.feedbackHistory.length
  }

  /**
   * Get recent feedback entries
   */
  getRecentFeedback(count: number = 10): FeedbackEntry[] {
    return this.feedbackHistory.slice(-count)
  }

  /**
   * Get feedback statistics
   */
  getStats(): {
    totalFeedback: number
    successRate: number
    avgErrorCount: number
    recentTrend: 'improving' | 'stable' | 'declining'
  } {
    const totalFeedback = this.feedbackHistory.length

    if (totalFeedback === 0) {
      return {
        totalFeedback: 0,
        successRate: 0,
        avgErrorCount: 0,
        recentTrend: 'stable',
      }
    }

    const successCount = this.feedbackHistory.filter(f => f.success).length
    const totalErrors = this.feedbackHistory.reduce((sum, f) => sum + f.errorCount, 0)

    // Calculate trend based on last 5 entries
    const recentEntries = this.feedbackHistory.slice(-5)
    const recentSuccessCount = recentEntries.filter(f => f.success).length
    const recentSuccessRate = recentSuccessCount / recentEntries.length

    let trend: 'improving' | 'stable' | 'declining'
    if (recentSuccessRate > this.config.successThreshold * 1.1) {
      trend = 'improving'
    } else if (recentSuccessRate < this.config.successThreshold * 0.9) {
      trend = 'declining'
    } else {
      trend = 'stable'
    }

    return {
      totalFeedback,
      successRate: successCount / totalFeedback,
      avgErrorCount: totalErrors / totalFeedback,
      recentTrend: trend,
    }
  }

  /**
   * Check if intervention is needed
   */
  needsIntervention(): boolean {
    const stats = this.getStats()
    return (
      stats.successRate < this.config.successThreshold ||
      stats.avgErrorCount > this.config.errorThreshold
    )
  }

  /**
   * Get intervention suggestions
   */
  getInterventionSuggestions(): string[] {
    const suggestions: string[] = []
    const stats = this.getStats()

    if (stats.successRate < this.config.successThreshold) {
      suggestions.push(`Success rate (${(stats.successRate * 100).toFixed(0)}%) is below threshold`)
    }

    if (stats.avgErrorCount > this.config.errorThreshold) {
      suggestions.push(`Error count (${stats.avgErrorCount.toFixed(1)}) exceeds threshold`)
    }

    if (stats.recentTrend === 'declining') {
      suggestions.push('Performance trend is declining, consider triggering Dream analysis')
    }

    return suggestions
  }

  /**
   * Reset feedback history
   */
  reset(): void {
    this.feedbackHistory = []
  }

  /**
   * Update configuration
   */
  updateConfig(config: Partial<FeedbackLoopConfig>): void {
    this.config = { ...this.config, ...config }
  }
}
