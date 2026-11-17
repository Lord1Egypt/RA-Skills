/**
 * 告警管理和定时巡检单元测试
 */

import { existsSync, unlinkSync } from 'fs'
import { join } from 'path'
import {
  AlertManager,
  DEFAULT_ALERT_RULES,
  resetAlertManager,
  type AlertRule,
} from '../skills/ops-maintenance/src/utils/alert-manager'
import {
  PatrolScheduler,
  type PatrolJob,
} from '../skills/ops-maintenance/src/utils/patrol-scheduler'

// 测试隔离：清除持久化文件
const configDir = join(process.env.HOME || '~', '.config', 'ops-maintenance')
const alertFile = join(configDir, 'alerts.json')
const configFile = join(configDir, 'alert-config.json')
const patrolFile = join(configDir, 'patrol-jobs.json')

// ============================================================
// AlertManager 测试
// ============================================================

describe('AlertManager', () => {
  let manager: AlertManager

  beforeEach(() => {
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
    resetAlertManager()
  })

  it('应该正确初始化', () => {
    expect(manager).toBeDefined()
  })

  it('应该返回默认告警规则', () => {
    const rules = manager.getRules()
    expect(rules).toHaveLength(DEFAULT_ALERT_RULES.length)
    expect(rules[0].id).toBeTruthy()
    expect(rules[0].name).toBeTruthy()
  })

  it('应该能够删除告警规则', () => {
    const firstRule = manager.getRules()[0]
    const removed = manager.removeRule(firstRule.id)
    expect(removed).toBe(true)
    expect(manager.getRules()).toHaveLength(DEFAULT_ALERT_RULES.length - 1)
  })

  it('应该能够切换规则启用状态', () => {
    const firstRule = manager.getRules()[0]
    const beforeEnabled = firstRule.enabled
    
    manager.toggleRule(firstRule.id, !beforeEnabled)
    expect(manager.getRules()[0].enabled).toBe(!beforeEnabled)
  })

  it('应该返回告警统计', () => {
    const stats = manager.getAlertStats()
    expect(stats).toBeDefined()
    expect(stats).toHaveProperty('total')
    expect(stats).toHaveProperty('firing')
    expect(stats).toHaveProperty('silenced')
  })
})

// ============================================================
// PatrolScheduler 测试
// ============================================================

describe('PatrolScheduler', () => {
  let scheduler: PatrolScheduler

  beforeEach(() => {
    // 清除持久化文件，确保测试隔离
    if (existsSync(patrolFile)) {
      try { unlinkSync(patrolFile) } catch {}
    }
    scheduler = new PatrolScheduler()
  })

  afterEach(() => {
    scheduler.stop()
    if (existsSync(patrolFile)) {
      try { unlinkSync(patrolFile) } catch {}
    }
  })

  it('应该正确初始化', () => {
    expect(scheduler).toBeDefined()
  })

  it('应该返回默认巡检任务', () => {
    const jobs = scheduler.getJobs()
    expect(jobs.length).toBeGreaterThanOrEqual(1)
  })

  it('应该能够删除巡检任务', () => {
    const jobs = scheduler.getJobs()
    if (jobs.length > 0) {
      const firstJob = jobs[0]
      const removed = scheduler.removeJob(firstJob.id)
      expect(removed).toBe(true)
    }
  })

  it('应该能够切换任务启用状态', () => {
    const jobs = scheduler.getJobs()
    if (jobs.length > 0) {
      const firstJob = jobs[0]
      const beforeEnabled = firstJob.enabled
      
      scheduler.toggleJob(firstJob.id, !beforeEnabled)
      expect(scheduler.getJobs().find(j => j.id === firstJob.id)?.enabled).toBe(!beforeEnabled)
    }
  })

  it('start/stop 不应该报错', () => {
    expect(() => scheduler.start()).not.toThrow()
    expect(() => scheduler.stop()).not.toThrow()
  })
})
