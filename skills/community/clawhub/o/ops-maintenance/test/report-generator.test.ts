/**
 * ReportGenerator 单元测试
 */

import { getReportGenerator, type ReportFormat } from '../skills/ops-maintenance/src/utils/report-generator'

describe('ReportGenerator', () => {
  let generator: ReturnType<typeof getReportGenerator>

  beforeEach(() => {
    generator = getReportGenerator()
  })

  it('应该正确初始化', () => {
    expect(generator).toBeDefined()
  })

  it('应该生成 Markdown 格式报告', async () => {
    const report = await generator.generate({ format: 'markdown' })
    expect(report).toBeDefined()
    expect(report.title).toBe('运维巡检报告')
    expect(report.sections).toBeDefined()
    expect(Array.isArray(report.sections)).toBe(true)
    expect(report.generatedAt).toBeTruthy()
    expect(report.hostname).toBeTruthy()
  })

  it('应该生成 JSON 格式报告', async () => {
    const report = await generator.generate({ format: 'json' })
    expect(report).toBeDefined()
    expect(report.summary).toBeDefined()
    expect(typeof report.summary.totalChecks).toBe('number')
  })

  it('应该生成纯文本格式报告', async () => {
    const report = await generator.generate({ format: 'text' })
    expect(report).toBeDefined()
  })

  it('应该能够跳过某些模块', async () => {
    const report = await generator.generate({
      includeHealth: false,
      includeSecurity: false,
      includeLogs: false,
      includeConfig: false,
    })
    expect(report).toBeDefined()
    expect(report.sections.length).toBe(0)
  })

  it('应该能够自定义报告标题', async () => {
    const report = await generator.generate({ title: '自定义报告标题' })
    expect(report.title).toBe('自定义报告标题')
  })

  it('format 方法应该正确格式化 Markdown', () => {
    const formatted = generator.format({
      title: '测试报告',
      generatedAt: '2024-01-01T00:00:00.000Z',
      hostname: 'test-host',
      sections: [],
      summary: { totalChecks: 0, ok: 0, warnings: 0, critical: 0 },
    } as any, 'markdown')
    expect(formatted).toContain('测试报告')
  })

  it('format 方法应该正确格式化 JSON', () => {
    const formatted = generator.format({
      title: '测试报告',
      generatedAt: '2024-01-01T00:00:00.000Z',
      hostname: 'test-host',
      sections: [],
      summary: { totalChecks: 0, ok: 0, warnings: 0, critical: 0 },
    } as any, 'json')
    expect(formatted).toContain('测试报告')
  })

  it('format 方法应该正确格式化 Text', () => {
    const formatted = generator.format({
      title: '测试报告',
      generatedAt: '2024-01-01T00:00:00.000Z',
      hostname: 'test-host',
      sections: [],
      summary: { totalChecks: 0, ok: 0, warnings: 0, critical: 0 },
    } as any, 'text')
    expect(formatted).toContain('测试报告')
  })
})
