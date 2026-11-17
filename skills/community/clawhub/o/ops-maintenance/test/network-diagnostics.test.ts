/**
 * NetworkDiagnostics 单元测试
 */

import { NetworkDiagnostics } from '../skills/ops-maintenance/src/utils/network-diagnostics'

describe('NetworkDiagnostics', () => {
  let diagnostics: NetworkDiagnostics

  beforeEach(() => {
    diagnostics = new NetworkDiagnostics()
  })

  it('应该正确初始化', () => {
    expect(diagnostics).toBeDefined()
  })

  it('ping 方法应该返回结果对象', async () => {
    const result = await diagnostics.ping('localhost', 2)
    expect(result).toBeDefined()
    expect(typeof result.host).toBe('string')
    expect(result.alive).toBeDefined()
  })

  it('dns 方法应该返回结果对象', async () => {
    const result = await diagnostics.dns('localhost')
    expect(result).toBeDefined()
    expect(typeof result.host).toBe('string')
    expect(Array.isArray(result.addresses)).toBe(true)
  })

  it('portCheck 方法应该返回结果对象', async () => {
    const result = await diagnostics.checkPort('localhost', 22)
    expect(result).toBeDefined()
    expect(typeof result.host).toBe('string')
    expect(typeof result.port).toBe('number')
  })

  it('应该能检测常用端口', async () => {
    const result = await diagnostics.checkPort('localhost', 0)
    expect(result).toBeDefined()
  })
})
