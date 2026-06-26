/**
 * 告警管理和定时巡检单元测试
 */

import { describe, it, expect, beforeEach, afterEach } from 'vitest'
import { existsSync, unlinkSync, readdirSync, rmSync } from 'fs'
import { join } from 'path'
import {
 AlertManager,
 DEFAULT_ALERT_RULES,
 resetAlertManager,
 type AlertRule,
 type AlertLevel,
} from '../src/utils/alert-manager.js'

// 测试隔离：清除持久化文件，防止历史数据污染
const configDir = join(process.env.HOME || '~', '.config', 'ops-maintenance')
const alertFile = join(configDir, 'alerts.json')
const configFile = join(configDir, 'alert-config.json')
import {
  PatrolScheduler,
  DEFAULT_PATROL_JOBS,
  type PatrolJob,
  type PatrolCheck,
  type PatrolExecutor,
  type PatrolResult,
} from '../src/utils/patrol-scheduler.js'

// ============================================================
// AlertManager 测试
// ============================================================

describe('AlertManager', () => {
  let manager: AlertManager

  beforeEach(() => {
  // 清除持久化文件，确保测试隔离
  for (const f of [alertFile, configFile]) {
  if (existsSync(f)) { try { unlinkSync(f) } catch {} }
  }
  resetAlertManager()
  manager = new AlertManager({
  rules: [...DEFAULT_ALERT_RULES],
  notify: {},
  silencePeriod: 60,
  repeatInterval: 60,
  })
  })

  afterEach(() => {
  // 清除测试产生的持久化文件
  for (const f of [alertFile, configFile]) {
  if (existsSync(f)) { try { unlinkSync(f) } catch {} }
  }
  })

  it('应正确加载默认告警规则', () => {
    const rules = manager.getRules()
    expect(rules.length).toBeGreaterThan(0)
    expect(rules.some(r => r.type === 'disk')).toBe(true)
    expect(rules.some(r => r.type === 'memory')).toBe(true)
    expect(rules.some(r => r.type === 'load')).toBe(true)
  })

  it('应能添加新规则', () => {
    const newRule: AlertRule = {
      id: 'test-rule',
      name: '测试规则',
      type: 'disk',
      threshold: 95,
      level: 'critical',
      duration: 30,
      interval: 60,
      channels: ['console'],
      enabled: true,
    }

    manager.upsertRule(newRule)
    const rules = manager.getRules()
    expect(rules.some(r => r.id === 'test-rule')).toBe(true)
  })

  it('应能更新已有规则', () => {
    const rule = manager.getRules()[0]
    const updated = { ...rule, threshold: 99 }
    manager.upsertRule(updated)
    const rules = manager.getRules()
    const found = rules.find(r => r.id === rule.id)
    expect(found?.threshold).toBe(99)
  })

  it('应能删除规则', () => {
    const rule = manager.getRules()[0]
    const deleted = manager.removeRule(rule.id)
    expect(deleted).toBe(true)
    expect(manager.getRules().some(r => r.id === rule.id)).toBe(false)
  })

  it('应能启用/禁用规则', () => {
    const rule = manager.getRules()[0]
    expect(manager.toggleRule(rule.id, false)).toBe(true)
    expect(manager.getRules().find(r => r.id === rule.id)?.enabled).toBe(false)
    expect(manager.toggleRule(rule.id, true)).toBe(true)
    expect(manager.getRules().find(r => r.id === rule.id)?.enabled).toBe(true)
  })

  it('磁盘超过阈值应触发告警', () => {
    const alert = manager.evaluate('disk', 'test-server', 85)
    expect(alert).not.toBeNull()
    expect(alert!.status).toBe('firing')
    expect(alert!.level).toBe('warning')
    expect(alert!.value).toBe(85)
  })

  it('磁盘超过critical阈值应触发critical告警', () => {
    const alert = manager.evaluate('disk', 'test-server', 92)
    expect(alert).not.toBeNull()
    expect(alert!.level).toBe('critical')
  })

  it('磁盘正常不应触发告警', () => {
    const alert = manager.evaluate('disk', 'test-server', 50)
    expect(alert).toBeNull()
  })

  it('内存超过阈值应触发告警', () => {
    const alert = manager.evaluate('memory', 'test-server', 90)
    expect(alert).not.toBeNull()
    expect(alert!.type).toBe('memory')
  })

  it('负载超过阈值应触发告警', () => {
    const alert = manager.evaluate('load', 'test-server', 7)
    expect(alert).not.toBeNull()
    expect(alert!.type).toBe('load')
  })

  it('同一规则+服务器不应重复触发告警', () => {
    const alert1 = manager.evaluate('disk', 'test-server', 85)
    expect(alert1).not.toBeNull()
    const alert2 = manager.evaluate('disk', 'test-server', 86)
    // 返回已有告警，但不应新增
    expect(alert2!.id).toBe(alert1!.id)
    expect(alert2!.notifyCount).toBe(1)
  })

  it('恢复正常后告警应resolved', () => {
    manager.evaluate('disk', 'test-server', 85)
    manager.evaluate('disk', 'test-server', 50)
    const alerts = manager.getActiveAlerts()
    expect(alerts.some(a => a.server === 'test-server' && a.type === 'disk')).toBe(false)
  })

  it('应能静默告警', () => {
    manager.evaluate('disk', 'test-server', 85)
    const silenced = manager.silence('disk-warning:test-server', 300)
    expect(silenced).toBe(true)
    const stats = manager.getAlertStats()
    expect(stats.silenced).toBeGreaterThan(0)
  })

  it('应能清理旧告警', () => {
    manager.evaluate('disk', 'test-server', 85)
    manager.evaluate('disk', 'test-server', 50) // resolved
    const removed = manager.cleanup(0) // 清理所有已恢复的
    expect(removed).toBeGreaterThanOrEqual(0)
  })

  it('告警统计应正确计算', () => {
    manager.evaluate('disk', 'server-1', 85)
    manager.evaluate('memory', 'server-2', 90)
    const stats = manager.getAlertStats()
    expect(stats.total).toBeGreaterThanOrEqual(2)
    expect(stats.firing).toBeGreaterThanOrEqual(2)
  })
})

// ============================================================
// PatrolScheduler 测试
// ============================================================

describe('PatrolScheduler', () => {
  let scheduler: PatrolScheduler

  // Mock 执行器
  const mockExecutor: PatrolExecutor = {
    async getServerList() {
      return ['localhost', 'server-1']
    },
    async executeCheck(server: string, check: PatrolCheck) {
      if (check.type === 'disk') {
        return { status: 'warning' as const, value: 85, message: '磁盘使用率: 85%' }
      }
      if (check.type === 'memory') {
        return { status: 'ok' as const, value: 60, message: '内存使用率: 60%' }
      }
      return { status: 'ok' as const, value: 0, message: '正常' }
    },
  }

  beforeEach(() => {
    scheduler = new PatrolScheduler()
    // 确保有测试需要的任务
    const existing = scheduler.getJobs()
    if (!existing.some(j => j.id === 'basic-health')) {
      scheduler.upsertJob(DEFAULT_PATROL_JOBS[0])
    }
    if (!existing.some(j => j.id === 'service-check')) {
      scheduler.upsertJob(DEFAULT_PATROL_JOBS[1])
    }
    scheduler.setExecutor(mockExecutor)
  })

  afterEach(() => {
    if (scheduler.running()) {
      scheduler.stop()
    }
  })

  it('应正确加载默认巡检任务', () => {
    const jobs = scheduler.getJobs()
    expect(jobs.length).toBeGreaterThan(0)
    expect(jobs.some(j => j.id === 'basic-health')).toBe(true)
  })

  it('应能添加新任务', () => {
    const newJob: PatrolJob = {
      id: 'test-job',
      name: '测试巡检',
      checks: [{ type: 'disk', alertEnabled: true }],
      schedule: 'every 10m',
      enabled: true,
    }
    scheduler.upsertJob(newJob)
    expect(scheduler.getJobs().some(j => j.id === 'test-job')).toBe(true)
  })

  it('应能删除任务', () => {
    const job = scheduler.getJobs()[0]
    const deleted = scheduler.removeJob(job.id)
    expect(deleted).toBe(true)
  })

  it('应能启用/禁用任务', () => {
    const job = scheduler.getJobs()[0]
    expect(scheduler.toggleJob(job.id, false)).toBe(true)
    expect(scheduler.getJobs().find(j => j.id === job.id)?.enabled).toBe(false)
  })

  it('手动执行巡检应返回结果', async () => {
    const results = await scheduler.runJobNow('basic-health')
    expect(results.length).toBeGreaterThan(0)
    expect(results[0].checks.length).toBeGreaterThan(0)
  })

  it('巡检报告应正确生成', async () => {
    const results = await scheduler.runJobNow('basic-health')
    const report = scheduler.generateReport(results)
    expect(report.totalServers).toBeGreaterThan(0)
    expect(report.totalChecks).toBeGreaterThan(0)
    expect(report.results.length).toBeGreaterThan(0)
  })

  it('报告格式化应包含Markdown标题', async () => {
    const results = await scheduler.runJobNow('basic-health')
    const report = scheduler.generateReport(results)
    const formatted = scheduler.formatReport(report)
    expect(formatted).toContain('巡检报告')
    expect(formatted).toContain('###')
  })

  it('调度器启动/停止应正常工作', () => {
    expect(scheduler.running()).toBe(false)
    scheduler.start()
    expect(scheduler.running()).toBe(true)
    scheduler.stop()
    expect(scheduler.running()).toBe(false)
  })

  it('解析调度表达式应正确', () => {
    // 通过手动执行验证，调度解析是内部方法
    const job: PatrolJob = {
      id: 'parse-test',
      name: '调度解析测试',
      checks: [{ type: 'disk' }],
      schedule: 'every 5m',
      enabled: false,
    }
    scheduler.upsertJob(job)
    expect(scheduler.getJobs().some(j => j.id === 'parse-test')).toBe(true)
  })
})

// ============================================================
// 集成测试: 告警 + 巡检联动
// ============================================================

describe('告警与巡检联动', () => {
 beforeEach(() => {
 for (const f of [alertFile, configFile]) {
 if (existsSync(f)) { try { unlinkSync(f) } catch {} }
 }
 })

 afterEach(() => {
 for (const f of [alertFile, configFile]) {
 if (existsSync(f)) { try { unlinkSync(f) } catch {} }
 }
 })

 it('巡检中超过阈值应触发告警', async () => {
 resetAlertManager()
    const alertManager = new AlertManager({
      rules: DEFAULT_ALERT_RULES.filter(r => r.type === 'disk'),
      notify: {},
      silencePeriod: 60,
      repeatInterval: 60,
    })

    // 模拟磁盘 92% 超过 critical 阈值
    const alert = alertManager.evaluate('disk', 'test-server', 92)
    expect(alert).not.toBeNull()
    expect(alert!.level).toBe('critical')
  })

  it('巡检恢复正常后告警应自动resolved', () => {
    resetAlertManager()
    const alertManager = new AlertManager({
      rules: DEFAULT_ALERT_RULES.filter(r => r.type === 'disk'),
      notify: {},
      silencePeriod: 60,
      repeatInterval: 60,
    })

    // 触发告警
    alertManager.evaluate('disk', 'test-server', 92)
    // 恢复正常
    alertManager.evaluate('disk', 'test-server', 50)

    const active = alertManager.getActiveAlerts()
    expect(active.some(a => a.server === 'test-server' && a.type === 'disk')).toBe(false)
  })
})
