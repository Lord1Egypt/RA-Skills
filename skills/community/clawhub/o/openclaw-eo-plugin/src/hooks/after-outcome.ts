/**
 * After Outcome Hook - Automatic outcome collection v2
 * 
 * Part of the self-optimization loop:
 * Decision → Execute → Track → Score → Optimize → Evolve
 * 
 * This hook automatically collects outcomes after tool calls
 * and feeds them to the EffectTracker for scoring
 */

import { effectTracker, type ScoringDecision, type ScoringOutcome } from '../autonomy/index.js'
import { hookLogger } from '../utils/logger.js'

// Hook event types
export type OutcomeHookEvent = {
  type: 'tool_call'
  toolName: string
  toolParams: Record<string, unknown>
  success: boolean
  durationMs: number
  result?: unknown
  error?: string
} | {
  type: 'decision'
  decision: ScoringDecision
  outcome: ScoringOutcome
} | {
  type: 'task_complete'
  taskId: string
  success: boolean
  metrics?: {
    duration?: number
    tokens?: number
    errors?: number
  }
}

/**
 * AfterOutcomeHook - Automatically collects outcomes
 * 
 * Usage:
 * afterOutcomeHook.trigger({ type: 'tool_call', toolName: 'eo_plan', success: true, durationMs: 1234 })
 */
export class AfterOutcomeHook {
  private enabled = true
  private minScoreThreshold = 50 // Only track scores above this

  /**
   * Enable/disable the hook
   */
  setEnabled(enabled: boolean): void {
    this.enabled = enabled
  }

  /**
   * Check if hook is enabled
   */
  isEnabled(): boolean {
    return this.enabled
  }

  /**
   * Set minimum score threshold for tracking
   */
  setMinScoreThreshold(threshold: number): void {
    this.minScoreThreshold = threshold
  }

  /**
   * Trigger outcome collection
   */
  trigger(event: OutcomeHookEvent): void {
    if (!this.enabled) return

    try {
      switch (event.type) {
        case 'tool_call':
          this.handleToolCall(event)
          break
        case 'decision':
          this.handleDecision(event)
          break
        case 'task_complete':
          this.handleTaskComplete(event)
          break
      }
    } catch (e) {
      console.error(`[AfterOutcomeHook] Error handling event: ${e}`)
    }
  }

  /**
   * Handle tool call outcome
   */
  private handleToolCall(event: Extract<OutcomeHookEvent, { type: 'tool_call' }>): void {
    // Skip if no duration (likely invalid event)
    if (!event.durationMs && event.durationMs !== 0) {
      console.debug(`[AfterOutcomeHook] Skipping tool_call - no durationMs`)
      return
    }

    // Create a synthetic decision for tool calls
    const decision: ScoringDecision = {
      id: `tool_${event.toolName}_${Date.now()}`,
      type: 'binary',
      description: `Tool call: ${event.toolName}`,
      timestamp: Date.now(),
      timeoutMs: event.durationMs > 0 ? event.durationMs * 2 : 5000,
    }

    const outcome: ScoringOutcome = {
      success: event.success,
      value: event.success ? 100 : 0,
      feedback: event.error || undefined,
    }

    const score = effectTracker.track(decision, outcome)
    
    // Log if score is below threshold
    if (score.score < this.minScoreThreshold) {
      console.warn(`[AfterOutcomeHook] Low score: ${event.toolName} score=${score.score} (${score.grade})`)
    } else {
      console.debug(`[AfterOutcomeHook] Tracked: ${event.toolName} score=${score.score} success=${event.success}`)
    }
  }

  /**
   * Handle decision outcome
   */
  private handleDecision(event: Extract<OutcomeHookEvent, { type: 'decision' }>): void {
    const score = effectTracker.track(event.decision, event.outcome)
    
    if (score.score < this.minScoreThreshold) {
      console.warn(`[AfterOutcomeHook] Low score: decision ${event.decision.id} score=${score.score}`)
    }
  }

  /**
   * Handle task completion
   */
  private handleTaskComplete(event: Extract<OutcomeHookEvent, { type: 'task_complete' }>): void {
    // Aggregate task metrics
    if (event.metrics) {
      hookLogger.info(`Task ${event.taskId} completed:`, {
        success: event.success,
        duration: event.metrics.duration,
        tokens: event.metrics.tokens,
        errors: event.metrics.errors,
      })
    }
  }

  /**
   * Get recent scores summary
   */
  getRecentSummary(): string {
    const stats = effectTracker.stats()
    return `Effect Tracking Summary:
- Total tracked: ${stats.total}
- Average score: ${stats.avgScore.toFixed(1)}
- Success rate: ${(stats.successRate * 100).toFixed(1)}%
- Grade: ${stats.grade}
- Trend: ${stats.trend}`
  }
}

// Export singleton
export const afterOutcomeHook = new AfterOutcomeHook()
