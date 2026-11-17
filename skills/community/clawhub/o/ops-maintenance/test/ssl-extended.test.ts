/**
 * SSLMonitor 单元测试（扩展）
 */

import { SSLMonitor } from '../skills/ops-maintenance/src/utils/ssl-monitor'

describe('SSLMonitor 扩展测试', () => {
  it('应该正确加载域名配置', () => {
    const domains = SSLMonitor.loadDomainsFromConfig('/nonexistent/path.json')
    expect(Array.isArray(domains)).toBe(true)
    expect(domains.length).toBe(0)
  })

  it('checkDomain 应该返回正确结构', async () => {
    const monitor = new SSLMonitor()
    const result = await monitor.checkDomain('localhost', 443)
    expect(result).toBeDefined()
    if (result.status === 'error') {
      expect(typeof result.error).toBe('string')
    } else if (result.cert) {
      expect(typeof result.cert.subject).toBe('string')
    }
  })

  it('formatReport 应该返回字符串', () => {
    const monitor = new SSLMonitor()
    const report = {
      domains: [],
      results: [],
      summary: { total: 0, valid: 0, expiring: 0, expired: 0, errors: 0 },
      generatedAt: new Date().toISOString(),
    }
    const formatted = monitor.formatReport(report as any)
    expect(typeof formatted).toBe('string')
  })
})
