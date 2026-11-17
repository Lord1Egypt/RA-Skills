/**
 * SSL 监控单元测试
 */

import { SSLMonitor } from '../skills/ops-maintenance/src/utils/ssl-monitor'

describe('SSLMonitor', () => {
  let monitor: SSLMonitor

  beforeEach(() => {
    monitor = new SSLMonitor()
  })

  it('应该正确初始化', () => {
    expect(monitor).toBeDefined()
  })

  it('检查 localhost SSL', async () => {
    const result = await monitor.checkDomain('localhost', 443)
    expect(result).toBeDefined()
    expect(result).toHaveProperty('domain')
    expect(result).toHaveProperty('status')
  })

  it('批量检查返回结果', async () => {
    const report = await monitor.checkDomains(['localhost'])
    expect(report).toBeDefined()
    expect(report).toHaveProperty('totalChecked')
    expect(report).toHaveProperty('timestamp')
    expect(report).toHaveProperty('results')
  })
})
