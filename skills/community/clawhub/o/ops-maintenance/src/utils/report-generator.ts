/**
 * 运维报告生成器 v3.0
 *
 * 自动汇总各模块数据，生成结构化运维报告
 */

import { getHealthChecker, formatHealthReport } from './health-checker.js'
import { getSecurityAuditor } from './security-auditor.js'
import { getSmartLogAnalyzer } from './smart-log-analyzer.js'
import { getConfigChangeTracker } from './config-change-tracker.js'

// ============================================================
// 类型定义
// ============================================================

export type ReportFormat = 'markdown' | 'json' | 'text'

export interface ReportOptions {
  format: ReportFormat
  includeHealth: boolean
  includeSecurity: boolean
  includeLogs: boolean
  includeConfig: boolean
  logHours: number
  logPattern: string
  title?: string
}

export interface ReportSection {
  title: string
  emoji: string
  status: 'ok' | 'warning' | 'critical' | 'skip'
  content: string
}

export interface OpsReport {
  title: string
  generatedAt: string
  hostname: string
  sections: ReportSection[]
  summary: {
    totalChecks: number
    ok: number
    warnings: number
    critical: number
  }
}

// ============================================================
// 报告生成器
// ============================================================

export class ReportGenerator {
  private hostname: string

  constructor() {
    this.hostname = require('os').hostname()
  }

  /**
   * 生成完整运维报告
   */
  async generate(options: Partial<ReportOptions> = {}): Promise<OpsReport> {
    const opts: ReportOptions = {
      format: 'markdown',
      includeHealth: true,
      includeSecurity: true,
      includeLogs: true,
      includeConfig: true,
      logHours: 1,
      logPattern: 'error|warn|critical|fail',
      title: '运维巡检报告',
      ...options,
    }

    const sections: ReportSection[] = []
    const summary = { totalChecks: 0, ok: 0, warnings: 0, critical: 0 }

    // 1. 健康检查
    if (opts.includeHealth) {
      try {
        const checker = getHealthChecker()
        const report = await checker.runAllChecks()
        const formatted = formatHealthReport(report)
        
        const status = report.overall === 'healthy' ? 'ok' as const : 
                       report.overall === 'degraded' ? 'warning' as const : 'critical' as const
        
        sections.push({
          title: '健康检查',
          emoji: '🏥',
          status,
          content: formatted,
        })
        
        summary.totalChecks += report.checks.length
        summary.ok += report.checks.filter(c => c.status === 'healthy').length
        summary.warnings += report.checks.filter(c => c.status === 'degraded').length
        summary.critical += report.checks.filter(c => c.status === 'unhealthy').length
      } catch (error: any) {
        sections.push({
          title: '健康检查',
          emoji: '🏥',
          status: 'warning',
          content: `❌ 健康检查失败: ${error.message}`,
        })
      }
    }

    // 2. 安全审计
    if (opts.includeSecurity) {
      try {
        const auditor = getSecurityAuditor()
        const findings = await auditor.runAllChecks()
        const report = auditor.formatFindings(findings)
        
        const criticalFindings = findings.filter(f => f.severity === 'high')
        const status = criticalFindings.length > 0 ? 'critical' as const : 
                       findings.length > 0 ? 'warning' as const : 'ok' as const
        
        sections.push({
          title: '安全审计',
          emoji: '🔒',
          status,
          content: report,
        })
        
        summary.totalChecks += 1
        if (status === 'ok') summary.ok++
        else if (status === 'warning') summary.warnings++
        else summary.critical++
      } catch (error: any) {
        sections.push({
          title: '安全审计',
          emoji: '🔒',
          status: 'warning',
          content: `❌ 安全审计失败: ${error.message}`,
        })
      }
    }

    // 3. 日志分析
    if (opts.includeLogs) {
      try {
        const analyzer = getSmartLogAnalyzer()
        const logPaths = analyzer.discoverLogPaths()
        const result = await analyzer.analyze(logPaths, opts.logPattern, opts.logHours)
        const formatted = analyzer.formatAnalysisResult(result)
        
        const status = result.anomalies.some(a => a.severity === 'critical') ? 'critical' as const :
                       result.anomalies.length > 0 ? 'warning' as const : 'ok' as const
        
        sections.push({
          title: '日志分析',
          emoji: '📊',
          status,
          content: formatted,
        })
        
        summary.totalChecks += 1
        if (status === 'ok') summary.ok++
        else if (status === 'warning') summary.warnings++
        else summary.critical++
      } catch (error: any) {
        sections.push({
          title: '日志分析',
          emoji: '📊',
          status: 'warning',
          content: `❌ 日志分析失败: ${error.message}`,
        })
      }
    }

    // 4. 配置变更
    if (opts.includeConfig) {
      try {
        const tracker = getConfigChangeTracker()
        const result = await tracker.checkChanges()
        const formatted = tracker.formatCheckResult(result)
        
        const status = result.changed > 0 ? 'warning' as const : 'ok' as const
        
        sections.push({
          title: '配置变更',
          emoji: '📝',
          status,
          content: formatted,
        })
        
        summary.totalChecks += 1
        if (status === 'ok') summary.ok++
        else summary.warnings++
      } catch (error: any) {
        sections.push({
          title: '配置变更',
          emoji: '📝',
          status: 'warning',
          content: `❌ 配置变更检查失败: ${error.message}`,
        })
      }
    }

    return {
      title: opts.title || '运维巡检报告',
      generatedAt: new Date().toISOString(),
      hostname: this.hostname,
      sections,
      summary,
    }
  }

  /**
   * 格式化报告为 Markdown
   */
  formatMarkdown(report: OpsReport): string {
    const lines: string[] = []
    
    // 标题
    lines.push(`# ${report.title}`)
    lines.push('')
    lines.push(`> 生成时间: ${report.generatedAt} | 主机: ${report.hostname}`)
    lines.push('')
    
    // 摘要
    const summaryEmoji = report.summary.critical > 0 ? '🔴' : 
                         report.summary.warnings > 0 ? '⚠️' : '✅'
    lines.push(`## ${summaryEmoji} 总体状态`)
    lines.push('')
    lines.push(`| 指标 | 数值 |`)
    lines.push(`|------|------|`)
    lines.push(`| 检查项 | ${report.summary.totalChecks} |`)
    lines.push(`| ✅ 正常 | ${report.summary.ok} |`)
    lines.push(`| ⚠️ 警告 | ${report.summary.warnings} |`)
    lines.push(`| 🔴 严重 | ${report.summary.critical} |`)
    lines.push('')
    
    // 各模块详情
    for (const section of report.sections) {
      const statusEmoji = { ok: '✅', warning: '⚠️', critical: '🔴', skip: '⏭️' }[section.status]
      lines.push(`## ${section.emoji} ${section.title} ${statusEmoji}`)
      lines.push('')
      lines.push(section.content)
      lines.push('')
    }
    
    return lines.join('\n')
  }

  /**
   * 格式化报告为纯文本
   */
  formatText(report: OpsReport): string {
    const lines: string[] = []
    
    lines.push(`=== ${report.title} ===`)
    lines.push(`生成时间: ${report.generatedAt} | 主机: ${report.hostname}`)
    lines.push('')
    lines.push(`总体: ${report.summary.ok}正常 ${report.summary.warnings}警告 ${report.summary.critical}严重`)
    lines.push('')
    
    for (const section of report.sections) {
      const statusText = { ok: '[OK]', warning: '[WARN]', critical: '[CRIT]', skip: '[SKIP]' }[section.status]
      lines.push(`--- ${section.title} ${statusText} ---`)
      lines.push(section.content.replace(/[#*`]/g, ''))
      lines.push('')
    }
    
    return lines.join('\n')
  }

  /**
   * 格式化为 JSON
   */
  formatJSON(report: OpsReport): string {
    return JSON.stringify(report, null, 2)
  }

  /**
   * 按指定格式输出
   */
  format(report: OpsReport, format: ReportFormat = 'markdown'): string {
    switch (format) {
      case 'markdown': return this.formatMarkdown(report)
      case 'text': return this.formatText(report)
      case 'json': return this.formatJSON(report)
    }
  }
}

// ============================================================
// 全局单例
// ============================================================

let globalReportGenerator: ReportGenerator | null = null

export function getReportGenerator(): ReportGenerator {
  if (!globalReportGenerator) {
    globalReportGenerator = new ReportGenerator()
  }
  return globalReportGenerator
}
