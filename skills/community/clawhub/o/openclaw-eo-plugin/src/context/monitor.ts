/**
 * Context Monitor
 * Real-time monitoring of context usage with threshold alerts
 */

import type { OpenClawPluginApi } from 'openclaw/plugin-sdk'
import type { ContextMetrics, ContextThresholds, MonitorConfig } from './types.js'
import { DEFAULT_THRESHOLDS, ContextLevel } from './types.js'

export class ContextMonitor {
  private api: OpenClawPluginApi
  private thresholds: ContextThresholds
  private lastCheckTime = 0
  private lastReportTime = 0
  private checkIntervalMs: number
  private reportIntervalMs: number
  private tokenLimit: number

  constructor(api: OpenClawPluginApi, config?: Partial<MonitorConfig>) {
    this.api = api
    this.thresholds = { ...DEFAULT_THRESHOLDS, ...config?.thresholds }
    this.checkIntervalMs = config?.checkIntervalMs ?? 60000  // 1 minute minimum
    this.reportIntervalMs = config?.reportIntervalMs ?? 300000 // 5 minutes
    this.tokenLimit = 100000 // Approximate token limit (adjust based on model)
  }

  /**
   * Check if enough time has passed since last check
   */
  canCheck(): boolean {
    return Date.now() - this.lastCheckTime >= this.checkIntervalMs
  }

  /**
   * Get current context metrics
   * Note: This is an approximation based on available APIs
   */
  async getMetrics(): Promise<ContextMetrics> {
    // Try to get actual metrics from API if available
    let tokenCount = 0
    let messageCount = 0

    try {
      // Access session info if available
      const sessionInfo = (this.api as any).session?.info?.()
      if (sessionInfo) {
        tokenCount = sessionInfo.tokenCount ?? 0
        messageCount = sessionInfo.messageCount ?? 0
      }
    } catch {
      // Fallback estimation
    }

    // If we can't get real metrics, estimate based on message count
    if (tokenCount === 0) {
      tokenCount = messageCount * 150 // Rough estimate: 150 tokens per message
    }

    const usagePercent = Math.min(100, (tokenCount / this.tokenLimit) * 100)

    return {
      tokenCount,
      tokenLimit: this.tokenLimit,
      usagePercent,
      messageCount,
      timestamp: Date.now(),
    }
  }

  /**
   * Determine context level based on usage
   */
  getLevel(usagePercent: number): ContextLevel {
    if (usagePercent >= this.thresholds.critical) return ContextLevel.CRITICAL
    if (usagePercent >= this.thresholds.compress) return ContextLevel.COMPRESS
    if (usagePercent >= this.thresholds.warning) return ContextLevel.WARNING
    return ContextLevel.NORMAL
  }

  /**
   * Check context and return current state
   */
  async check(): Promise<{ metrics: ContextMetrics; level: ContextLevel; shouldReport: boolean }> {
    if (!this.canCheck()) {
      return {
        metrics: { tokenCount: 0, tokenLimit: 0, usagePercent: 0, messageCount: 0, timestamp: Date.now() },
        level: ContextLevel.NORMAL,
        shouldReport: false,
      }
    }

    this.lastCheckTime = Date.now()
    const metrics = await this.getMetrics()
    const level = this.getLevel(metrics.usagePercent)
    const shouldReport = Date.now() - this.lastReportTime >= this.reportIntervalMs

    if (shouldReport) {
      this.lastReportTime = Date.now()
    }

    // Log warning states
    if (level !== ContextLevel.NORMAL) {
      this.api.logger.warn(`[ContextMonitor] Context level: ${level} (${metrics.usagePercent.toFixed(1)}%)`)
    }

    return { metrics, level, shouldReport }
  }

  /**
   * Get thresholds
   */
  getThresholds(): ContextThresholds {
    return { ...this.thresholds }
  }

  /**
   * Update thresholds dynamically
   */
  updateThresholds(thresholds: Partial<ContextThresholds>): void {
    this.thresholds = { ...this.thresholds, ...thresholds }
    this.api.logger.info(`[ContextMonitor] Thresholds updated: ${JSON.stringify(this.thresholds)}`)
  }
}
