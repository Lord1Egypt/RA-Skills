/**
 * 智能日志分析器 v3.0
 *
 * 支持：
 * - 日志趋势统计（错误量时间线）
 * - 多日志文件关联分析
 * - 异常模式自动识别
 * - 日志分类和聚合
 */

import { exec } from 'child_process'
import { promisify } from 'util'
import { readFileSync, existsSync } from 'fs'
import { join } from 'path'

const execAsync = promisify(exec)

// ============================================================
// 类型定义
// ============================================================

export type LogLevel = 'error' | 'warn' | 'info' | 'debug' | 'critical'

export interface LogEntry {
  timestamp?: string
  level: LogLevel
  message: string
  source?: string
  raw: string
}

export interface LogTrend {
  timeBucket: string
  count: number
  errors: number
  warnings: number
  infos: number
}

export interface LogPattern {
  pattern: string
  count: number
  level: LogLevel
  firstSeen?: string
  lastSeen?: string
  examples: string[]
}

export interface LogAnomaly {
  type: 'spike' | 'new_pattern' | 'correlation' | 'timeout_cluster' | 'error_burst'
  severity: 'info' | 'warning' | 'critical'
  description: string
  details: Record<string, any>
}

export interface LogAnalysisResult {
  source: string
  totalLines: number
  timeRange: { start?: string; end?: string }
  levelCounts: Record<LogLevel, number>
  trends: LogTrend[]
  topPatterns: LogPattern[]
  anomalies: LogAnomaly[]
  correlations: { sources: string[]; pattern: string; strength: number }[]
}

// ============================================================
// 智能日志分析器
// ============================================================

export class SmartLogAnalyzer {
  private timeout: number

  constructor(timeout: number = 15000) {
    this.timeout = timeout
  }

  // ----------------------------------------------------------
  // 日志收集
  // ----------------------------------------------------------

  /**
   * 搜索日志文件
   */
  async searchLogs(
    paths: string[],
    pattern: string = 'error',
    lines: number = 200
  ): Promise<LogEntry[]> {
    const entries: LogEntry[] = []

    for (const logPath of paths) {
      try {
        const cmd = `grep -i "${pattern}" "${logPath}" 2>/dev/null | tail -${lines}`
        const { stdout } = await execAsync(cmd, { timeout: this.timeout })

        for (const line of stdout.trim().split('\n').filter(l => l.trim())) {
          entries.push(this.parseLine(line, logPath))
        }
      } catch {
        // 文件不存在或无匹配
      }
    }

    return entries
  }

  /**
   * 读取 journalctl 日志 (Linux)
   */
  async searchJournalctl(
    unit?: string,
    pattern: string = 'error',
    since: string = '1 hour ago',
    lines: number = 200
  ): Promise<LogEntry[]> {
    try {
      const unitArg = unit ? `-u ${unit}` : ''
      const cmd = `journalctl ${unitArg} --since "${since}" --no-pager -o short-iso 2>/dev/null | grep -i "${pattern}" | tail -${lines}`
      const { stdout } = await execAsync(cmd, { timeout: this.timeout })

      return stdout.trim().split('\n')
        .filter(l => l.trim() && !l.startsWith('--'))
        .map(line => this.parseLine(line, 'journalctl'))
    } catch {
      return []
    }
  }

  /**
   * 自动发现常见日志路径
   */
  discoverLogPaths(): string[] {
    const commonPaths = [
      '/var/log/syslog',
      '/var/log/system.log',
      '/var/log/nginx/access.log',
      '/var/log/nginx/error.log',
      '/var/log/apache2/access.log',
      '/var/log/apache2/error.log',
      '/var/log/postgresql/postgresql.log',
      '/var/log/redis/redis.log',
      '/var/log/docker.log',
      '/var/log/homer.log',
    ]

    // macOS 特有路径
    if (process.platform === 'darwin') {
      commonPaths.push(
        '/var/log/system.log',
        `${process.env.HOME}/Library/Logs/*.log`
      )
    }

    return commonPaths.filter(p => {
      try {
        // 简单通配符展开
        if (p.includes('*')) return true
        return existsSync(p)
      } catch {
        return false
      }
    })
  }

  // ----------------------------------------------------------
  // 趋势分析
  // ----------------------------------------------------------

  /**
   * 分析日志趋势（按时间段统计错误量）
   */
  analyzeTrends(entries: LogEntry[], bucketMinutes: number = 15): LogTrend[] {
    const buckets = new Map<string, LogTrend>()

    for (const entry of entries) {
      if (!entry.timestamp) continue

      const time = new Date(entry.timestamp)
      if (isNaN(time.getTime())) continue

      // 按桶分时
      const bucketMs = bucketMinutes * 60 * 1000
      const bucketStart = new Date(Math.floor(time.getTime() / bucketMs) * bucketMs)
      const key = bucketStart.toISOString().replace(/\.\d+Z$/, '')

      if (!buckets.has(key)) {
        buckets.set(key, {
          timeBucket: key,
          count: 0,
          errors: 0,
          warnings: 0,
          infos: 0,
        })
      }

      const bucket = buckets.get(key)!
      bucket.count++
      if (entry.level === 'error' || entry.level === 'critical') bucket.errors++
      else if (entry.level === 'warn') bucket.warnings++
      else bucket.infos++
    }

    return Array.from(buckets.values()).sort((a, b) =>
      a.timeBucket.localeCompare(b.timeBucket)
    )
  }

  // ----------------------------------------------------------
  // 模式识别
  // ----------------------------------------------------------

  /**
   * 识别日志模式（相似日志聚合）
   */
  identifyPatterns(entries: LogEntry[], topN: number = 10): LogPattern[] {
    const patternMap = new Map<string, LogPattern>()

    for (const entry of entries) {
      // 将日志消息泛化为模式：替换数字、IP、路径、UUID等
      const pattern = this.generalizeMessage(entry.message)

      if (!patternMap.has(pattern)) {
        patternMap.set(pattern, {
          pattern,
          count: 0,
          level: entry.level,
          firstSeen: entry.timestamp,
          lastSeen: entry.timestamp,
          examples: [],
        })
      }

      const p = patternMap.get(pattern)!
      p.count++
      if (entry.timestamp) {
        if (!p.lastSeen || entry.timestamp > p.lastSeen) p.lastSeen = entry.timestamp
        if (!p.firstSeen || entry.timestamp < p.firstSeen) p.firstSeen = entry.timestamp
      }
      // 保留前3个原始示例
      if (p.examples.length < 3) {
        p.examples.push(entry.raw.substring(0, 200))
      }
    }

    return Array.from(patternMap.values())
      .sort((a, b) => b.count - a.count)
      .slice(0, topN)
  }

  /**
   * 泛化日志消息为模式
   */
  private generalizeMessage(message: string): string {
    return message
      .replace(/\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/g, '<IP>')
      .replace(/\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b/gi, '<UUID>')
      .replace(/\b\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?\b/g, '<TIMESTAMP>')
      .replace(/\b\d{10,13}\b/g, '<EPOCH>')
      .replace(/\/[\w./-]+/g, '<PATH>')
      .replace(/\b\d+\.?\d*\b/g, '<NUM>')
      .replace(/\b0x[0-9a-f]+\b/gi, '<HEX>')
      .substring(0, 200)
  }

  // ----------------------------------------------------------
  // 异常检测
  // ----------------------------------------------------------

  /**
   * 检测异常
   */
  detectAnomalies(
    entries: LogEntry[],
    trends: LogTrend[]
  ): LogAnomaly[] {
    const anomalies: LogAnomaly[] = []

    // 1. 错误突增检测
    this.detectErrorSpikes(trends, anomalies)

    // 2. 新模式检测
    this.detectNewPatterns(entries, anomalies)

    // 3. 超时聚类
    this.detectTimeoutClusters(entries, anomalies)

    // 4. 连续错误爆发
    this.detectErrorBursts(entries, anomalies)

    return anomalies.sort((a, b) => {
      const severityOrder = { critical: 0, warning: 1, info: 2 }
      return severityOrder[a.severity] - severityOrder[b.severity]
    })
  }

  /** 错误突增 */
  private detectErrorSpikes(trends: LogTrend[], anomalies: LogAnomaly[]): void {
    if (trends.length < 3) return

    const errorCounts = trends.map(t => t.errors)
    const avg = errorCounts.reduce((a, b) => a + b, 0) / errorCounts.length
    const stdDev = Math.sqrt(errorCounts.reduce((a, b) => a + (b - avg) ** 2, 0) / errorCounts.length)

    for (const trend of trends) {
      if (trend.errors > avg + 2 * stdDev && trend.errors > 3) {
        anomalies.push({
          type: 'spike',
          severity: trend.errors > avg + 3 * stdDev ? 'critical' : 'warning',
          description: `${trend.timeBucket} 错误数 ${trend.errors} 异常偏高 (均值 ${avg.toFixed(1)}, 标准差 ${stdDev.toFixed(1)})`,
          details: { timeBucket: trend.timeBucket, errors: trend.errors, avg, stdDev },
        })
      }
    }
  }

  /** 新模式检测 */
  private detectNewPatterns(entries: LogEntry[], anomalies: LogAnomaly[]): void {
    const now = new Date()
    const oneHourAgo = new Date(now.getTime() - 3600000)
    const recent = entries.filter(e => {
      if (!e.timestamp) return false
      return new Date(e.timestamp) >= oneHourAgo
    })

    const recentPatterns = new Set(recent.map(e => this.generalizeMessage(e.message)))
    const olderPatterns = new Set(
      entries.filter(e => {
        if (!e.timestamp) return true
        return new Date(e.timestamp) < oneHourAgo
      }).map(e => this.generalizeMessage(e.message))
    )

    const newPatterns = [...recentPatterns].filter(p => !olderPatterns.has(p))

    for (const pattern of newPatterns.slice(0, 5)) {
      const matchingRecent = recent.filter(e => this.generalizeMessage(e.message) === pattern)
      const errorCount = matchingRecent.filter(e => e.level === 'error' || e.level === 'critical').length

      if (errorCount > 2) {
        anomalies.push({
          type: 'new_pattern',
          severity: errorCount > 5 ? 'critical' : 'warning',
          description: `检测到新的错误模式: ${pattern.substring(0, 100)}`,
          details: { pattern, count: matchingRecent.length, errorCount },
        })
      }
    }
  }

  /** 超时聚类 */
  private detectTimeoutClusters(entries: LogEntry[], anomalies: LogAnomaly[]): void {
    const timeoutEntries = entries.filter(e =>
      e.message.toLowerCase().includes('timeout') ||
      e.message.toLowerCase().includes('timed out') ||
      e.message.toLowerCase().includes('connection refused')
    )

    if (timeoutEntries.length >= 3) {
      // 检查是否集中在短时间内
      const timestamps = timeoutEntries
        .filter(e => e.timestamp)
        .map(e => new Date(e.timestamp!).getTime())
        .sort()

      for (let i = 2; i < timestamps.length; i++) {
        if (timestamps[i] - timestamps[i - 2] < 60000) { // 1分钟内3个超时
          anomalies.push({
            type: 'timeout_cluster',
            severity: 'critical',
            description: `短时间内多个超时: ${timeoutEntries.length} 个超时/连接拒绝`,
            details: { count: timeoutEntries.length, examples: timeoutEntries.slice(0, 3).map(e => e.message.substring(0, 100)) },
          })
          break
        }
      }
    }
  }

  /** 连续错误爆发 */
  private detectErrorBursts(entries: LogEntry[], anomalies: LogAnomaly[]): void {
    let consecutive = 0
    let maxConsecutive = 0
    let burstStart = 0

    for (let i = 0; i < entries.length; i++) {
      if (entries[i].level === 'error' || entries[i].level === 'critical') {
        if (consecutive === 0) burstStart = i
        consecutive++
        maxConsecutive = Math.max(maxConsecutive, consecutive)
      } else {
        consecutive = 0
      }
    }

    if (maxConsecutive >= 5) {
      anomalies.push({
        type: 'error_burst',
        severity: maxConsecutive >= 10 ? 'critical' : 'warning',
        description: `检测到连续 ${maxConsecutive} 条错误日志`,
        details: { maxConsecutive, startEntry: entries[burstStart]?.raw?.substring(0, 100) },
      })
    }
  }

  // ----------------------------------------------------------
  // 多日志关联分析
  // ----------------------------------------------------------

  /**
   * 多源关联分析
   */
  correlateLogs(
    sources: { name: string; entries: LogEntry[] }[]
  ): { sources: string[]; pattern: string; strength: number }[] {
    const correlations: { sources: string[]; pattern: string; strength: number }[] = []

    if (sources.length < 2) return correlations

    // 收集每个源的错误模式
    const sourcePatterns = new Map<string, Map<string, number>>()
    for (const source of sources) {
      const patterns = new Map<string, number>()
      for (const entry of source.entries) {
        if (entry.level === 'error' || entry.level === 'critical') {
          const key = this.generalizeMessage(entry.message)
          patterns.set(key, (patterns.get(key) || 0) + 1)
        }
      }
      sourcePatterns.set(source.name, patterns)
    }

    // 查找共同模式
    const allPatternNames = new Set<string>()
    for (const patterns of sourcePatterns.values()) {
      for (const p of patterns.keys()) {
        allPatternNames.add(p)
      }
    }

    for (const pattern of allPatternNames) {
      const matchedSources: string[] = []
      let totalCount = 0

      for (const [name, patterns] of sourcePatterns) {
        const count = patterns.get(pattern) || 0
        if (count > 0) {
          matchedSources.push(name)
          totalCount += count
        }
      }

      if (matchedSources.length >= 2) {
        correlations.push({
          sources: matchedSources,
          pattern: pattern.substring(0, 100),
          strength: matchedSources.length * totalCount,
        })
      }
    }

    return correlations
      .sort((a, b) => b.strength - a.strength)
      .slice(0, 10)
  }

  // ----------------------------------------------------------
  // 综合分析
  // ----------------------------------------------------------

  /**
   * 综合分析日志
   */
  async analyze(
    logPaths: string[],
    pattern: string = 'error|warn|critical|fail',
    hours: number = 24
  ): Promise<LogAnalysisResult> {
    const allEntries: LogEntry[] = []
    const sinceArg = `${hours}h ago`

    for (const logPath of logPaths) {
      try {
        let cmd: string
        if (logPath === 'journalctl') {
          cmd = `journalctl --since "${sinceArg}" --no-pager -o short-iso 2>/dev/null | grep -iE "${pattern}" | tail -500`
        } else {
          cmd = `grep -iE "${pattern}" "${logPath}" 2>/dev/null | tail -500`
        }

        const { stdout } = await execAsync(cmd, { timeout: this.timeout })
        for (const line of stdout.trim().split('\n').filter(l => l.trim())) {
          allEntries.push(this.parseLine(line, logPath))
        }
      } catch {
        // skip
      }
    }

    // 统计
    const levelCounts: Record<LogLevel, number> = { error: 0, warn: 0, info: 0, debug: 0, critical: 0 }
    for (const entry of allEntries) {
      levelCounts[entry.level] = (levelCounts[entry.level] || 0) + 1
    }

    // 趋势
    const trends = this.analyzeTrends(allEntries, 30)

    // 模式
    const topPatterns = this.identifyPatterns(allEntries, 10)

    // 异常
    const anomalies = this.detectAnomalies(allEntries, trends)

    // 时间范围
    const timestamps = allEntries.filter(e => e.timestamp).map(e => new Date(e.timestamp!))
    const timeRange = {
      start: timestamps.length > 0 ? new Date(Math.min(...timestamps.map(Number))).toISOString() : undefined,
      end: timestamps.length > 0 ? new Date(Math.max(...timestamps.map(Number))).toISOString() : undefined,
    }

    return {
      source: logPaths.join(', '),
      totalLines: allEntries.length,
      timeRange,
      levelCounts,
      trends,
      topPatterns,
      anomalies,
      correlations: [],
    }
  }

  // ----------------------------------------------------------
  // 格式化输出
  // ----------------------------------------------------------

  formatAnalysisResult(result: LogAnalysisResult): string {
    const lines: string[] = []
    lines.push('### 📊 智能日志分析报告\n')

    // 概览
    lines.push('**概览**:')
    lines.push(`- 分析日志行数: ${result.totalLines}`)
    if (result.timeRange.start) {
      lines.push(`- 时间范围: ${result.timeRange.start} ~ ${result.timeRange.end}`)
    }
    lines.push(`- 🔴 严重: ${result.levelCounts.critical} | ❌ 错误: ${result.levelCounts.error} | ⚠️ 警告: ${result.levelCounts.warn} | ℹ️ 信息: ${result.levelCounts.info}`)
    lines.push('')

    // 异常
    if (result.anomalies.length > 0) {
      lines.push('**🚨 检测到的异常**:')
      for (const a of result.anomalies.slice(0, 10)) {
        const emoji = { critical: '🔴', warning: '⚠️', info: 'ℹ️' }[a.severity]
        lines.push(`- ${emoji} [${a.type}] ${a.description}`)
      }
      lines.push('')
    }

    // 趋势
    if (result.trends.length > 0) {
      lines.push('**📈 错误趋势**:')
      for (const t of result.trends.slice(-12)) {
        const bar = '█'.repeat(Math.min(t.errors, 30))
        lines.push(`- ${t.timeBucket.substring(11, 16)} ${bar} ${t.errors}`)
      }
      lines.push('')
    }

    // Top 模式
    if (result.topPatterns.length > 0) {
      lines.push('**🔍 Top 日志模式**:')
      for (const p of result.topPatterns.slice(0, 8)) {
        const levelEmoji = { error: '❌', warn: '⚠️', critical: '🔴', info: 'ℹ️', debug: '🔧' }[p.level]
        lines.push(`- ${levelEmoji} [${p.count}次] ${p.pattern.substring(0, 80)}`)
      }
      lines.push('')
    }

    // 关联
    if (result.correlations.length > 0) {
      lines.push('**🔗 多源关联**:')
      for (const c of result.correlations.slice(0, 5)) {
        lines.push(`- ${c.sources.join(' ↔ ')}: ${c.pattern.substring(0, 60)} (关联度: ${c.strength})`)
      }
    }

    if (result.totalLines === 0) {
      lines.push('未找到匹配的日志内容')
    }

    return lines.join('\n')
  }

  // ----------------------------------------------------------
  // 工具方法
  // ----------------------------------------------------------

  private parseLine(line: string, source: string): LogEntry {
    // 尝试解析常见日志格式
    let timestamp: string | undefined
    let level: LogLevel = 'info'
    let message = line

    // ISO timestamp
    const isoMatch = line.match(/^(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?)/)
    if (isoMatch) {
      timestamp = isoMatch[1]
      message = line.substring(isoMatch[0].length).trim()
    }

    // syslog timestamp
    const syslogMatch = line.match(/^(\w{3}\s+\d+\s+\d{2}:\d{2}:\d{2})/)
    if (!timestamp && syslogMatch) {
      timestamp = syslogMatch[1]
      message = line.substring(syslogMatch[0].length).trim()
    }

    // 检测日志级别
    const lowerLine = line.toLowerCase()
    if (lowerLine.includes('critical') || lowerLine.includes('fatal') || lowerLine.includes('panic')) {
      level = 'critical'
    } else if (lowerLine.includes('error') || lowerLine.includes('err:') || lowerLine.includes('exception')) {
      level = 'error'
    } else if (lowerLine.includes('warn') || lowerLine.includes('warning')) {
      level = 'warn'
    } else if (lowerLine.includes('debug') || lowerLine.includes('trace')) {
      level = 'debug'
    }

    return { timestamp, level, message, source, raw: line }
  }
}

// ============================================================
// 全局单例
// ============================================================

let globalSmartLogAnalyzer: SmartLogAnalyzer | null = null

export function getSmartLogAnalyzer(): SmartLogAnalyzer {
  if (!globalSmartLogAnalyzer) {
    globalSmartLogAnalyzer = new SmartLogAnalyzer()
  }
  return globalSmartLogAnalyzer
}
