/**
 * 审计日志工具
 * 
 * 记录所有运维操作，用于审计和问题排查
 */

import { join } from 'path'
import { existsSync, mkdirSync, appendFileSync, readFileSync } from 'fs'

export interface AuditLogEntry {
  timestamp: string
  operation: string
  server: string
  user?: string
  command?: string
  status: 'success' | 'failure' | 'partial'
  duration?: number
  error?: string
  metadata?: Record<string, any>
}

/**
 * 审计日志管理器
 */
export class AuditLogger {
  private logDir: string
  private logFile: string

  constructor(logDir?: string) {
    this.logDir = logDir || join(process.env.HOME || '~', '.config/ops-maintenance/logs')
    this.logFile = join(this.logDir, 'audit.log')
    
    // 确保日志目录存在
    if (!existsSync(this.logDir)) {
      mkdirSync(this.logDir, { recursive: true })
    }
  }

  /**
   * 记录操作
   */
  log(entry: AuditLogEntry): void {
    const logLine = JSON.stringify(entry) + '\n'
    appendFileSync(this.logFile, logLine)
  }

  /**
   * 记录成功操作
   */
  logSuccess(
    operation: string,
    server: string,
    command?: string,
    duration?: number,
    metadata?: Record<string, any>
  ): void {
    this.log({
      timestamp: new Date().toISOString(),
      operation,
      server,
      command,
      status: 'success',
      duration,
      metadata
    })
  }

  /**
   * 记录失败操作
   */
  logFailure(
    operation: string,
    server: string,
    error: string,
    command?: string,
    metadata?: Record<string, any>
  ): void {
    this.log({
      timestamp: new Date().toISOString(),
      operation,
      server,
      command,
      status: 'failure',
      error,
      metadata
    })
  }

  /**
   * 记录部分成功操作
   */
  logPartial(
    operation: string,
    server: string,
    error: string,
    command?: string,
    duration?: number,
    metadata?: Record<string, any>
  ): void {
    this.log({
      timestamp: new Date().toISOString(),
      operation,
      server,
      command,
      status: 'partial',
      duration,
      error,
      metadata
    })
  }

  /**
   * 查询日志
   */
  queryLogs(
    filter?: {
      operation?: string
      server?: string
      status?: string
      startTime?: Date
      endTime?: Date
    }
  ): AuditLogEntry[] {
    if (!existsSync(this.logFile)) {
      return []
    }

    const content = readFileSync(this.logFile, 'utf-8')
    const lines = content.trim().split('\n')
    const logs: AuditLogEntry[] = []

    for (const line of lines) {
      try {
        const entry = JSON.parse(line) as AuditLogEntry
        
        // 应用过滤条件
        if (filter) {
          if (filter.operation && entry.operation !== filter.operation) continue
          if (filter.server && entry.server !== filter.server) continue
          if (filter.status && entry.status !== filter.status) continue
          
          if (filter.startTime || filter.endTime) {
            const entryTime = new Date(entry.timestamp)
            if (filter.startTime && entryTime < filter.startTime) continue
            if (filter.endTime && entryTime > filter.endTime) continue
          }
        }
        
        logs.push(entry)
      } catch (e) {
        // 忽略解析错误
      }
    }

    return logs
  }

  /**
   * 查询日志(简化接口)
   */
  query(filter?: {
    action?: string
    status?: string
    limit?: number
  }): AuditLogEntry[] {
    const logs = this.queryLogs({
      operation: filter?.action,
      status: filter?.status,
    })
    return logs.slice(-(filter?.limit || 20)).reverse()
  }

  /**
   * 格式化日志为可读文本
   */
  formatLogs(logs: AuditLogEntry[]): string {
    if (logs.length === 0) return '暂无审计日志'

    const lines: string[] = []
    lines.push('### 📋 审计日志\n')

    for (const log of logs) {
      const emoji = log.status === 'success' ? '✅' : log.status === 'failure' ? '❌' : '⚠️'
      lines.push(`${emoji} [${log.timestamp}] ${log.operation} @ ${log.server} - ${log.status}`)
      if (log.command) lines.push(`   命令: ${log.command}`)
      if (log.error) lines.push(`   错误: ${log.error}`)
      if (log.duration) lines.push(`   耗时: ${log.duration}ms`)
      lines.push('')
    }

    return lines.join('\n')
  }

  /**
   * 获取统计信息
   */
  getStats(): {
    total: number
    success: number
    failure: number
    partial: number
    byOperation: Record<string, number>
    byServer: Record<string, number>
  } {
    const logs = this.queryLogs()
    const stats = {
      total: logs.length,
      success: 0,
      failure: 0,
      partial: 0,
      byOperation: {} as Record<string, number>,
      byServer: {} as Record<string, number>
    }

    for (const log of logs) {
      stats[log.status]++
      
      if (log.operation) {
        stats.byOperation[log.operation] = (stats.byOperation[log.operation] || 0) + 1
      }
      
      if (log.server) {
        stats.byServer[log.server] = (stats.byServer[log.server] || 0) + 1
      }
    }

    return stats
  }
}

// 全局审计日志实例
let globalAuditLogger: AuditLogger | null = null

/**
 * 获取全局审计日志
 */
export function getAuditLogger(): AuditLogger {
  if (!globalAuditLogger) {
    globalAuditLogger = new AuditLogger()
  }
  return globalAuditLogger
}
