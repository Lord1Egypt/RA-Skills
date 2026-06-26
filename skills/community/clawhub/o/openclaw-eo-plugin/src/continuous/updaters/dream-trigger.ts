/**
 * Dream Trigger
 * Triggers Dream analysis based on accumulated errors or thresholds
 */

import { DreamEngine, type DreamTrigger as DreamTriggerType } from '../../dream/dream-engine.js'
import { logger } from '../../utils/logger.js'

export interface DreamTriggerResult {
  triggered: boolean
  reason?: string
  reportId?: string
  durationMs?: number
  error?: string
}

export interface DreamThresholdConfig {
  errorCount: number
  sessionCount: number
  timeWindowMs: number
}

export class DreamTrigger {
  private engine: DreamEngine
  private errorCount: number
  private sessionCount: number
  private lastTriggerTime: number = 0
  private triggerHistory: Array<{ timestamp: number; type: string; success: boolean }> = []

  constructor(engine: DreamEngine, initialErrorCount: number = 0) {
    this.engine = engine
    this.errorCount = initialErrorCount
    this.sessionCount = 0
  }

  /**
   * Trigger Dream analysis
   */
  async trigger(trigger: DreamTriggerType): Promise<DreamTriggerResult> {
    const startTime = Date.now()

    try {
      logger.info(`Triggering dream: ${trigger.type}`)

      const result = await this.engine.executeDream(trigger)

      if (result.success) {
        this.lastTriggerTime = Date.now()
        this.triggerHistory.push({
          timestamp: Date.now(),
          type: trigger.type,
          success: true,
        })

        return {
          triggered: true,
          reason: trigger.type,
          reportId: result.report?.id,
          durationMs: result.durationMs,
        }
      } else {
        this.triggerHistory.push({
          timestamp: Date.now(),
          type: trigger.type,
          success: false,
        })

        return {
          triggered: false,
          reason: trigger.type,
          error: result.error,
        }
      }
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error)
      console.error(`[DreamTrigger] Trigger failed: ${errorMsg}`)

      return {
        triggered: false,
        reason: trigger.type,
        error: errorMsg,
        durationMs: Date.now() - startTime,
      }
    }
  }

  /**
   * Check if Dream should be triggered based on thresholds
   */
  shouldTrigger(config: DreamThresholdConfig): boolean {
    const now = Date.now()

    // Check if we're within the time window
    const withinTimeWindow = now - this.lastTriggerTime < config.timeWindowMs
    if (withinTimeWindow && this.lastTriggerTime > 0) {
      return false
    }

    // Check error threshold
    if (this.errorCount >= config.errorCount) {
      return true
    }

    // Check session count threshold
    if (this.sessionCount >= config.sessionCount) {
      return true
    }

    return false
  }

  /**
   * Increment error counter
   */
  incrementError(): void {
    this.errorCount++
    logger.debug(`Error count: ${this.errorCount}`)
  }

  /**
   * Increment session counter
   */
  incrementSession(): void {
    this.sessionCount++
  }

  /**
   * Reset counters
   */
  resetCounters(): void {
    this.errorCount = 0
    this.sessionCount = 0
  }

  /**
   * Set error count directly
   */
  setErrorCount(count: number): void {
    this.errorCount = count
  }

  /**
   * Get current error count
   */
  getErrorCount(): number {
    return this.errorCount
  }

  /**
   * Get Dream status
   */
  getStatus(): {
    errorCount: number
    sessionCount: number
    lastTrigger: number | null
    triggerHistoryLength: number
    pendingReports: number
  } {
    return {
      errorCount: this.errorCount,
      sessionCount: this.sessionCount,
      lastTrigger: this.lastTriggerTime || null,
      triggerHistoryLength: this.triggerHistory.length,
      pendingReports: this.engine.getPendingPatches().length,
    }
  }

  /**
   * Get recent trigger history
   */
  getRecentTriggers(count: number = 5): Array<{ timestamp: number; type: string; success: boolean }> {
    return this.triggerHistory.slice(-count)
  }

  /**
   * Check if Dream is available
   */
  isAvailable(): boolean {
    return true // In plugin context, Dream is always available
  }

  /**
   * Get dream reports
   */
  getReports(): { date: string; summary: string }[] {
    return this.engine.listReports()
  }

  /**
   * Get pending patches from Dream
   */
  getPendingPatches() {
    return this.engine.getPendingPatches()
  }
}
