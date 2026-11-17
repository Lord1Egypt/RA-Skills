/**
 * 阈值检查器 - 简化版
 */

import type { HealthMetrics, ThresholdConfig } from '../config/schemas'
import { ServerStatus } from '../config/schemas'

export const DEFAULT_THRESHOLDS: ThresholdConfig = {
  diskWarning: 80, diskCritical: 90,
  memoryWarning: 80, memoryCritical: 90,
  swapWarning: 70, swapCritical: 90,
  loadWarningMultiplier: 1.0, loadCriticalMultiplier: 2.0
}

export const ENV_THRESHOLDS: Record<string, ThresholdConfig> = {
  production: { ...DEFAULT_THRESHOLDS, diskWarning: 75, diskCritical: 85, memoryWarning: 75, memoryCritical: 85 },
  staging: { ...DEFAULT_THRESHOLDS, diskWarning: 85, diskCritical: 95, memoryWarning: 85, memoryCritical: 95 },
  development: DEFAULT_THRESHOLDS
}

export class ThresholdChecker {
  private thresholds: ThresholdConfig
  private environment: string

  constructor(thresholds?: Partial<ThresholdConfig>, environment: string = 'production') {
    const envConfig = ENV_THRESHOLDS[environment] || DEFAULT_THRESHOLDS
    this.thresholds = { ...envConfig, ...thresholds }
    this.environment = environment
  }

  check(serverName: string, metrics: HealthMetrics): { overallStatus: string; checks: any[] } {
    const checks: any[] = []

    const diskPercent = metrics.disk.usagePercent
    checks.push(this.checkThreshold('disk', diskPercent, this.thresholds.diskCritical, this.thresholds.diskWarning, `磁盘 ${diskPercent}%`))

    const memPercent = Math.round((metrics.memory.used / metrics.memory.total) * 100)
    checks.push(this.checkThreshold('memory', memPercent, this.thresholds.memoryCritical, this.thresholds.memoryWarning, `内存 ${memPercent}%`))

    if (metrics.memory.swapTotal > 0) {
      const swapPercent = Math.round((metrics.memory.swapUsed / metrics.memory.swapTotal) * 100)
      checks.push(this.checkThreshold('swap', swapPercent, this.thresholds.swapCritical, this.thresholds.swapWarning, `Swap ${swapPercent}%`))
    }

    const hasCritical = checks.some(c => c.status === 'critical')
    const hasWarning = checks.some(c => c.status === 'warning')
    const overallStatus = hasCritical ? ServerStatus.WARNING : hasWarning ? ServerStatus.WARNING : ServerStatus.HEALTHY

    return { overallStatus, checks }
  }

  private checkThreshold(metric: string, value: number, critical: number, warning: number, message: string) {
    if (value >= critical) return { metric, value, threshold: critical, status: 'critical', message: `🔴 ${message}` }
    if (value >= warning) return { metric, value, threshold: warning, status: 'warning', message: `🟡 ${message}` }
    return { metric, value, threshold: warning, status: 'ok', message: `✅ ${message}` }
  }

  getThresholds(): ThresholdConfig { return { ...this.thresholds } }
  setThresholds(thresholds: Partial<ThresholdConfig>): void { this.thresholds = { ...this.thresholds, ...thresholds } }
  setEnvironment(env: string): void {
    const envConfig = ENV_THRESHOLDS[env]
    if (envConfig) { this.thresholds = { ...envConfig }; this.environment = env }
  }
}