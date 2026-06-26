/**
 * 定时巡检调度器 v3.0
 *
 * 支持定时执行健康检查、磁盘监控等操作
 * 自动评估告警规则并触发通知
 * 生成巡检报告
 */

import { join } from 'path'
import { existsSync, mkdirSync, writeFileSync, readFileSync } from 'fs'
import { getAuditLogger } from './audit-logger.js'
import { getAlertManager, type AlertLevel } from './alert-manager.js'

// ============================================================
// 类型定义
// ============================================================

/** 巡检任务 */
export interface PatrolJob {
  id: string
  name: string
  /** 检查类型 */
  checks: PatrolCheck[]
  /** cron 表达式 或 秒间隔 */
  schedule: string
  /** 适用的服务器 (空=本地+所有远程) */
  servers?: string[]
  /** 适用的标签 */
  tags?: string[]
  /** 是否启用 */
  enabled: boolean
  /** 上次执行时间 */
  lastRun?: string
  /** 下次执行时间 */
  nextRun?: string
}

/** 巡检检查项 */
export interface PatrolCheck {
  type: 'health' | 'disk' | 'memory' | 'load' | 'cpu' | 'service' | 'network' | 'process'
  /** 检查参数 */
  params?: Record<string, any>
  /** 是否评估告警 */
  alertEnabled?: boolean
}

/** 巡检结果 */
export interface PatrolResult {
  jobId: string
  jobName: string
  server: string
  timestamp: string
  checks: {
    type: string
    status: 'ok' | 'warning' | 'critical' | 'error'
    value?: number
    message: string
    detail?: string
  }[]
  alertsFired: number
  duration: number
}

/** 巡检报告 */
export interface PatrolReport {
  id: string
  timestamp: string
  totalServers: number
  totalChecks: number
  totalAlerts: number
  results: PatrolResult[]
  summary: {
    healthy: number
    warning: number
    critical: number
    error: number
  }
}

// ============================================================
// 默认巡检任务
// ============================================================

export const DEFAULT_PATROL_JOBS: PatrolJob[] = [
  {
    id: 'basic-health',
    name: '基础健康巡检',
    checks: [
      { type: 'health', alertEnabled: true },
      { type: 'disk', alertEnabled: true },
      { type: 'memory', alertEnabled: true },
      { type: 'load', alertEnabled: true },
    ],
    schedule: 'every 5m',
    enabled: true,
  },
  {
    id: 'service-check',
    name: '服务状态巡检',
    checks: [
      { type: 'service', params: { services: ['nginx', 'docker', 'sshd'] }, alertEnabled: true },
      { type: 'process', params: { processes: ['nginx', 'docker', 'sshd'] }, alertEnabled: true },
    ],
    schedule: 'every 1m',
    enabled: false, // 默认关闭，需要配置具体服务
  },
]

// ============================================================
// 巡检调度器
// ============================================================

export class PatrolScheduler {
  private configDir: string
  private reportDir: string
  private jobsFile: string
  private jobs: PatrolJob[]
  private timers: Map<string, ReturnType<typeof setInterval>> = new Map()
  private isRunning = false

  /** 巡检执行回调 — 由外部注入实际执行逻辑 */
  private executor: PatrolExecutor | null = null

  constructor() {
    this.configDir = join(process.env.HOME || '~', '.config/ops-maintenance')
    this.reportDir = join(this.configDir, 'reports')
    this.jobsFile = join(this.configDir, 'patrol-jobs.json')

    if (!existsSync(this.reportDir)) {
      mkdirSync(this.reportDir, { recursive: true })
    }

    this.jobs = this.loadJobs()
  }

  /** 设置巡检执行器 */
  setExecutor(executor: PatrolExecutor): void {
    this.executor = executor
  }

  // ----------------------------------------------------------
  // 任务管理
  // ----------------------------------------------------------

  /** 获取所有任务 */
  getJobs(): PatrolJob[] {
    return [...this.jobs]
  }

  /** 添加/更新任务 */
  upsertJob(job: PatrolJob): void {
    const idx = this.jobs.findIndex(j => j.id === job.id)
    if (idx >= 0) {
      this.jobs[idx] = job
      // 如果调度器在运行，更新定时器
      if (this.isRunning && job.enabled) {
        this.stopJobTimer(job.id)
        this.startJobTimer(job)
      }
    } else {
      this.jobs.push(job)
      if (this.isRunning && job.enabled) {
        this.startJobTimer(job)
      }
    }
    this.saveJobs()
  }

  /** 删除任务 */
  removeJob(jobId: string): boolean {
    const idx = this.jobs.findIndex(j => j.id === jobId)
    if (idx >= 0) {
      this.stopJobTimer(jobId)
      this.jobs.splice(idx, 1)
      this.saveJobs()
      return true
    }
    return false
  }

  /** 启用/禁用任务 */
  toggleJob(jobId: string, enabled: boolean): boolean {
    const job = this.jobs.find(j => j.id === jobId)
    if (job) {
      job.enabled = enabled
      if (this.isRunning) {
        if (enabled) {
          this.startJobTimer(job)
        } else {
          this.stopJobTimer(jobId)
        }
      }
      this.saveJobs()
      return true
    }
    return false
  }

  // ----------------------------------------------------------
  // 调度管理
  // ----------------------------------------------------------

  /** 启动调度器 */
  start(): void {
    if (this.isRunning) return

    this.isRunning = true
    for (const job of this.jobs) {
      if (job.enabled) {
        this.startJobTimer(job)
      }
    }

    const audit = getAuditLogger()
    audit.logSuccess('patrol_start', 'scheduler', undefined, undefined, { jobCount: this.jobs.filter(j => j.enabled).length })
  }

  /** 停止调度器 */
  stop(): void {
    for (const [id] of this.timers) {
      this.stopJobTimer(id)
    }
    this.isRunning = false

    const audit = getAuditLogger()
    audit.logSuccess('patrol_stop', 'scheduler')
  }

  /** 检查是否在运行 */
  running(): boolean {
    return this.isRunning
  }

  /** 手动触发一个任务 */
  async runJobNow(jobId: string): Promise<PatrolResult[]> {
    const job = this.jobs.find(j => j.id === jobId)
    if (!job) throw new Error(`巡检任务不存在: ${jobId}`)

    return this.executeJob(job)
  }

  /** 手动触发所有启用的任务 */
  async runAllNow(): Promise<PatrolResult[]> {
    const results: PatrolResult[] = []
    for (const job of this.jobs.filter(j => j.enabled)) {
      const jobResults = await this.executeJob(job)
      results.push(...jobResults)
    }
    return results
  }

  // ----------------------------------------------------------
  // 内部方法
  // ----------------------------------------------------------

  private startJobTimer(job: PatrolJob): void {
    const intervalMs = this.parseSchedule(job.schedule)
    if (intervalMs <= 0) return

    // 立即执行一次
    this.executeJob(job).catch(() => {})

    // 定时执行
    const timer = setInterval(() => {
      this.executeJob(job).catch(() => {})
    }, intervalMs)

    this.timers.set(job.id, timer)
  }

  private stopJobTimer(jobId: string): void {
    const timer = this.timers.get(jobId)
    if (timer) {
      clearInterval(timer)
      this.timers.delete(jobId)
    }
  }

  /** 解析 schedule 为毫秒间隔 */
  private parseSchedule(schedule: string): number {
    // "every 5m" -> 300000
    // "every 30s" -> 30000
    // "every 1h" -> 3600000
    const match = schedule.match(/^every\s+(\d+)(s|m|h)$/)
    if (match) {
      const value = parseInt(match[1])
      const unit = match[2]
      switch (unit) {
        case 's': return value * 1000
        case 'm': return value * 60 * 1000
        case 'h': return value * 3600 * 1000
      }
    }

    // 纯数字 (秒)
    const num = parseInt(schedule)
    if (!isNaN(num) && num > 0) {
      return num * 1000
    }

    console.warn(`[PatrolScheduler] 无法解析调度: ${schedule}`)
    return 0
  }

  /** 执行单个巡检任务 */
  private async executeJob(job: PatrolJob): Promise<PatrolResult[]> {
    if (!this.executor) {
      console.warn('[PatrolScheduler] 未设置巡检执行器，跳过执行')
      return []
    }

    const alertManager = getAlertManager()
    const audit = getAuditLogger()
    const results: PatrolResult[] = []

    // 更新任务执行时间
    job.lastRun = new Date().toISOString()

    try {
      // 获取要巡检的服务器列表
      const servers = await this.executor.getServerList(job)

      for (const server of servers) {
        const startTime = Date.now()
        const result: PatrolResult = {
          jobId: job.id,
          jobName: job.name,
          server,
          timestamp: new Date().toISOString(),
          checks: [],
          alertsFired: 0,
          duration: 0,
        }

        for (const check of job.checks) {
          try {
            const checkResult = await this.executor.executeCheck(server, check)

            result.checks.push({
              type: check.type,
              status: checkResult.status,
              value: checkResult.value,
              message: checkResult.message,
              detail: checkResult.detail,
            })

            // 评估告警
            if (check.alertEnabled && checkResult.value !== undefined) {
              const alert = alertManager.evaluate(check.type, server, checkResult.value, checkResult.extra)
              if (alert) result.alertsFired++
            }
          } catch (error: any) {
            result.checks.push({
              type: check.type,
              status: 'error',
              message: error.message,
            })
          }
        }

        result.duration = Date.now() - startTime
        results.push(result)
      }

      audit.logSuccess('patrol_job', 'scheduler', undefined, undefined, {
        jobId: job.id,
        serversChecked: servers.length,
        alertsFired: results.reduce((sum, r) => sum + r.alertsFired, 0),
      })
    } catch (error: any) {
      audit.logFailure('patrol_job', 'scheduler', error.message, undefined, { jobId: job.id })
    }

    this.saveJobs()
    return results
  }

  // ----------------------------------------------------------
  // 巡检报告
  // ----------------------------------------------------------

  /** 生成巡检报告 */
  generateReport(results: PatrolResult[]): PatrolReport {
    const report: PatrolReport = {
      id: `report-${Date.now()}`,
      timestamp: new Date().toISOString(),
      totalServers: new Set(results.map(r => r.server)).size,
      totalChecks: results.reduce((sum, r) => sum + r.checks.length, 0),
      totalAlerts: results.reduce((sum, r) => sum + r.alertsFired, 0),
      results,
      summary: { healthy: 0, warning: 0, critical: 0, error: 0 },
    }

    for (const result of results) {
      for (const check of result.checks) {
        if (check.status === 'ok') report.summary.healthy++
        else if (check.status === 'warning') report.summary.warning++
        else if (check.status === 'critical') report.summary.critical++
        else report.summary.error++
      }
    }

    // 保存报告
    const reportFile = join(this.reportDir, `patrol-${new Date().toISOString().replace(/[:.]/g, '-')}.json`)
    writeFileSync(reportFile, JSON.stringify(report, null, 2))

    return report
  }

  /** 格式化报告为 Markdown */
  formatReport(report: PatrolReport): string {
    const lines: string[] = []
    lines.push('### 📋 巡检报告\n')
    lines.push(`**时间**: ${report.timestamp}`)
    lines.push(`**服务器**: ${report.totalServers} 台 | **检查项**: ${report.totalChecks} | **告警**: ${report.totalAlerts}\n`)

    // 摘要
    lines.push('**摘要**: ' + [
      report.summary.healthy > 0 ? `✅ 正常 ${report.summary.healthy}` : '',
      report.summary.warning > 0 ? `⚠️ 警告 ${report.summary.warning}` : '',
      report.summary.critical > 0 ? `🔴 严重 ${report.summary.critical}` : '',
      report.summary.error > 0 ? `❌ 错误 ${report.summary.error}` : '',
    ].filter(Boolean).join(' | '))

    // 各服务器详情
    for (const result of report.results) {
      lines.push(`\n#### ${result.server}`)
      for (const check of result.checks) {
        const emoji = { ok: '✅', warning: '⚠️', critical: '🔴', error: '❌' }[check.status]
        const valueStr = check.value !== undefined ? ` (${check.value})` : ''
        lines.push(`- ${emoji} ${check.type}: ${check.message}${valueStr}`)
      }
      if (result.alertsFired > 0) {
        lines.push(`  - 📢 触发 ${result.alertsFired} 条告警`)
      }
    }

    return lines.join('\n')
  }

  /** 获取最近的巡检报告列表 */
  listReports(limit: number = 10): { file: string; timestamp: string }[] {
    if (!existsSync(this.reportDir)) return []

    const files = require('fs').readdirSync(this.reportDir)
      .filter((f: string) => f.startsWith('patrol-') && f.endsWith('.json'))
      .sort()
      .reverse()
      .slice(0, limit)

    return files.map((f: string) => ({
      file: join(this.reportDir, f),
      timestamp: f.replace('patrol-', '').replace('.json', '').replace(/-/g, ':').slice(0, 19),
    }))
  }

  // ----------------------------------------------------------
  // 持久化
  // ----------------------------------------------------------

  private loadJobs(): PatrolJob[] {
    if (existsSync(this.jobsFile)) {
      try {
        const content = readFileSync(this.jobsFile, 'utf-8')
        return JSON.parse(content)
      } catch {
        return [...DEFAULT_PATROL_JOBS]
      }
    }
    return [...DEFAULT_PATROL_JOBS]
  }

  private saveJobs(): void {
    writeFileSync(this.jobsFile, JSON.stringify(this.jobs, null, 2))
  }
}

// ============================================================
// 巡检执行器接口 (由 index.ts 实现)
// ============================================================

export interface PatrolExecutor {
  /** 获取任务要巡检的服务器列表 */
  getServerList(job: PatrolJob): Promise<string[]>
  /** 执行单个检查 */
  executeCheck(
    server: string,
    check: PatrolCheck
  ): Promise<{
    status: 'ok' | 'warning' | 'critical' | 'error'
    value?: number
    message: string
    detail?: string
    extra?: Record<string, any>
  }>
}

// ============================================================
// 全局单例
// ============================================================

let globalPatrolScheduler: PatrolScheduler | null = null

export function getPatrolScheduler(): PatrolScheduler {
  if (!globalPatrolScheduler) {
    globalPatrolScheduler = new PatrolScheduler()
  }
  return globalPatrolScheduler
}
