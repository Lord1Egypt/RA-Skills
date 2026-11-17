/**
 * AuditLogger 单元测试
 */

import { existsSync, unlinkSync } from 'fs'
import { join } from 'path'
import { AuditLogger, type AuditLogEntry } from '../skills/ops-maintenance/src/utils/audit-logger'

const logDir = join(process.env.HOME || '~', '.config/ops-maintenance/logs')
const logFile = join(logDir, 'audit.log')

describe('AuditLogger', () => {
  let logger: AuditLogger
  const originalLogDir = logDir

  beforeEach(() => {
    // 确保日志目录存在
    const fs = require('fs')
    if (!fs.existsSync(logDir)) {
      fs.mkdirSync(logDir, { recursive: true })
    }
    // 清理旧的审计日志
    if (existsSync(logFile)) {
      unlinkSync(logFile)
    }
    logger = new AuditLogger()
  })

  afterEach(() => {
    // 清理审计日志
    if (existsSync(logFile)) {
      unlinkSync(logFile)
    }
  })

  it('应该正确初始化', () => {
    expect(logger).toBeDefined()
  })

  it('应该记录成功操作', () => {
    logger.log({
      timestamp: new Date().toISOString(),
      operation: 'test_op',
      server: 'test-server',
      status: 'success',
      duration: 100,
    })

    const logs = logger.query({ limit: 10 })
    expect(logs).toHaveLength(1)
    expect(logs[0].operation).toBe('test_op')
    expect(logs[0].status).toBe('success')
  })

  it('应该记录失败操作', () => {
    logger.logFailure('test_fail', 'server1', 'connection refused', 'ssh connect')

    const logs = logger.query({ limit: 10 })
    expect(logs.length).toBeGreaterThan(0)
    expect(logs.find(l => l.operation === 'test_fail')).toBeTruthy()
  })

  it('应该返回统计信息', () => {
    logger.logSuccess('op1', 'server1', 'cmd1', 50)
    logger.logSuccess('op2', 'server1', 'cmd2', 80)
    logger.logFailure('op3', 'server2', 'timeout', 'ssh connect')

    const stats = logger.getStats()
    expect(stats.total).toBe(3)
    expect(stats.success).toBe(2)
    expect(stats.failure).toBe(1)
    expect(stats.partial).toBe(0)
  })
})
