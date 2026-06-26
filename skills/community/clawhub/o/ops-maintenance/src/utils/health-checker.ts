/**
 * 系统健康检查器 v3.0
 *
 * 全面检查系统健康状态
 * 支持: CPU/内存/磁盘/负载/服务/网络/Docker
 */

import { exec } from 'child_process'
import { promisify } from 'util'
import { getAuditLogger } from './audit-logger.js'

const execAsync = promisify(exec)

// ============================================================
// 类型定义
// ============================================================

export type HealthStatus = 'healthy' | 'degraded' | 'unhealthy'

export interface HealthCheckResult {
  name: string
  status: HealthStatus
  message: string
  value?: number
  unit?: string
  detail?: string
  extra?: Record<string, any>
}

export interface HealthReport {
  hostname: string
  timestamp: string
  overall: HealthStatus
  checks: HealthCheckResult[]
  duration: number
}

// ============================================================
// 健康检查器
// ============================================================

export class HealthChecker {
  private timeout: number

  constructor(timeout: number = 15000) {
    this.timeout = timeout
  }

  /**
   * 执行所有健康检查
   */
  async runAllChecks(): Promise<HealthReport> {
    const start = Date.now()
    const checks: HealthCheckResult[] = []

    const checkList = [
      () => this.checkLoad(),
      () => this.checkMemory(),
      () => this.checkDisk(),
      () => this.checkCPU(),
      () => this.checkSwap(),
      () => this.checkUptime(),
      () => this.checkDNS(),
      () => this.checkDocker(),
    ]

    for (const check of checkList) {
      try {
        const result = await check()
        checks.push(result)
      } catch (error: any) {
        checks.push({
          name: 'unknown',
          status: 'unhealthy',
          message: `检查失败: ${error.message}`,
        })
      }
    }

    const overall = this.computeOverallStatus(checks)

    return {
      hostname: require('os').hostname(),
      timestamp: new Date().toISOString(),
      overall,
      checks,
      duration: Date.now() - start,
    }
  }

  /**
   * 检查单个服务
   */
  async checkService(serviceName: string): Promise<HealthCheckResult> {
    try {
      // 尝试 systemd
      const { stdout } = await execAsync(`systemctl is-active "${serviceName}" 2>/dev/null || echo unknown`, {
        timeout: 5000,
      })
      const status = stdout.trim()

      if (status === 'active') {
        return { name: serviceName, status: 'healthy', message: '运行中' }
      } else if (status === 'inactive' || status === 'failed') {
        return { name: serviceName, status: 'unhealthy', message: `服务状态: ${status}` }
      }

      // macOS: 尝试 pgrep
      try {
        const { stdout: pgrepOut } = await execAsync(`pgrep -f "${serviceName}" | head -1`, { timeout: 5000 })
        if (pgrepOut.trim()) {
          return { name: serviceName, status: 'healthy', message: '运行中(pgrep)' }
        }
      } catch { /* not found */ }

      return { name: serviceName, status: 'unhealthy', message: '未运行' }
    } catch (error: any) {
      return { name: serviceName, status: 'unhealthy', message: `检查失败: ${error.message}` }
    }
  }

  // ----------------------------------------------------------
  // 各项检查
  // ----------------------------------------------------------

  private async checkLoad(): Promise<HealthCheckResult> {
    try {
      const os = require('os')
      const loadAvg = os.loadavg()
      const cpuCount = os.cpus().length
      const load1 = loadAvg[0]
      const ratio = load1 / cpuCount

      const status: HealthStatus = ratio > 1.5 ? 'unhealthy' : ratio > 0.8 ? 'degraded' : 'healthy'

      return {
        name: '系统负载',
        status,
        message: `1分钟负载: ${load1.toFixed(2)} / ${cpuCount}核`,
        value: load1,
        unit: 'load',
        detail: `1min=${loadAvg[0].toFixed(2)}, 5min=${loadAvg[1].toFixed(2)}, 15min=${loadAvg[2].toFixed(2)}`,
        extra: { load1, load5: loadAvg[1], load15: loadAvg[2], cpuCount, ratio },
      }
    } catch (error: any) {
      return { name: '系统负载', status: 'unhealthy', message: `检查失败: ${error.message}` }
    }
  }

  private async checkMemory(): Promise<HealthCheckResult> {
    try {
      const os = require('os')
      const totalMem = os.totalmem()
      const freeMem = os.freemem()
      const usedMem = totalMem - freeMem
      const usagePercent = (usedMem / totalMem) * 100

      const status: HealthStatus = usagePercent > 95 ? 'unhealthy' : usagePercent > 85 ? 'degraded' : 'healthy'

      return {
        name: '内存使用',
        status,
        message: `${usagePercent.toFixed(1)}% (${this.formatBytes(usedMem)} / ${this.formatBytes(totalMem)})`,
        value: usagePercent,
        unit: '%',
        extra: { totalMem, freeMem, usedMem, usagePercent },
      }
    } catch (error: any) {
      return { name: '内存使用', status: 'unhealthy', message: `检查失败: ${error.message}` }
    }
  }

  private async checkDisk(): Promise<HealthCheckResult> {
    try {
      const { stdout } = await execAsync('df -h / 2>/dev/null | tail -1', { timeout: 5000 })
      const parts = stdout.trim().split(/\s+/)
      const usageStr = parts[4] || '0%'
      const usagePercent = parseInt(usageStr)

      const status: HealthStatus = usagePercent > 90 ? 'unhealthy' : usagePercent > 80 ? 'degraded' : 'healthy'

      return {
        name: '磁盘使用',
        status,
        message: `${usageStr} (${parts[2] || '?'} / ${parts[1] || '?'})`,
        value: usagePercent,
        unit: '%',
        detail: `挂载点: ${parts[5] || '/'}`,
      }
    } catch (error: any) {
      return { name: '磁盘使用', status: 'unhealthy', message: `检查失败: ${error.message}` }
    }
  }

  private async checkCPU(): Promise<HealthCheckResult> {
    try {
      // 采样1秒的CPU使用率
      const os = require('os')

      const startUsage = process.cpuUsage()
      const startTime = process.hrtime()

      await new Promise(resolve => setTimeout(resolve, 1000))

      const endUsage = process.cpuUsage(startUsage)
      const endTime = process.hrtime(startTime)
      const elapsedUs = endTime[0] * 1e6 + endTime[1] / 1e3

      // 使用系统级方法
      const { stdout } = await execAsync(
        process.platform === 'darwin'
          ? 'top -l 1 -n 0 | grep "CPU usage"'
          : 'grep "cpu " /proc/stat 2>/dev/null || echo "N/A"',
        { timeout: 5000 }
      )

      const cpuMatch = stdout.match(/(\d+\.?\d*)\s*%/)
      const cpuPercent = cpuMatch ? parseFloat(cpuMatch[1]) : 0

      const status: HealthStatus = cpuPercent > 80 ? 'unhealthy' : cpuPercent > 60 ? 'degraded' : 'healthy'

      return {
        name: 'CPU使用率',
        status,
        message: `${cpuPercent.toFixed(1)}%`,
        value: cpuPercent,
        unit: '%',
      }
    } catch {
      return { name: 'CPU使用率', status: 'degraded', message: '无法获取CPU使用率' }
    }
  }

  private async checkSwap(): Promise<HealthCheckResult> {
    try {
      const { stdout } = await execAsync(
        process.platform === 'darwin'
          ? 'sysctl vm.swapusage 2>/dev/null || echo "N/A"'
          : 'free -b 2>/dev/null | grep Swap || echo "N/A"',
        { timeout: 5000 }
      )

      const usageMatch = stdout.match(/(\d+\.?\d*)\s*(M|G|K)?/i)
      const swapUsed = usageMatch ? parseFloat(usageMatch[1]) : 0

      return {
        name: 'Swap使用',
        status: swapUsed > 80 ? 'degraded' : 'healthy',
        message: stdout.trim().substring(0, 80) || '无Swap或未使用',
        value: swapUsed,
      }
    } catch {
      return { name: 'Swap使用', status: 'healthy', message: '未检测到Swap' }
    }
  }

  private async checkUptime(): Promise<HealthCheckResult> {
    try {
      const os = require('os')
      const uptimeSec = os.uptime()
      const days = Math.floor(uptimeSec / 86400)
      const hours = Math.floor((uptimeSec % 86400) / 3600)

      return {
        name: '运行时间',
        status: 'healthy',
        message: `${days}天${hours}小时`,
        value: uptimeSec,
        unit: 's',
      }
    } catch {
      return { name: '运行时间', status: 'healthy', message: '未知' }
    }
  }

  private async checkDNS(): Promise<HealthCheckResult> {
    try {
      const { stdout } = await execAsync(
        'cat /etc/resolv.conf 2>/dev/null | grep nameserver || scutil --dns 2>/dev/null | head -5 || echo "N/A"',
        { timeout: 5000 }
      )

      const nameservers = stdout.match(/nameserver\s+(\S+)/g) || []
      const hasDNS = nameservers.length > 0 || stdout.includes('nameserver')

      return {
        name: 'DNS配置',
        status: hasDNS ? 'healthy' : 'degraded',
        message: hasDNS ? `${nameservers.length || 1}个DNS服务器` : '未检测到DNS配置',
        detail: stdout.trim().substring(0, 100),
      }
    } catch {
      return { name: 'DNS配置', status: 'degraded', message: '无法检测DNS' }
    }
  }

  private async checkDocker(): Promise<HealthCheckResult> {
    try {
      const { stdout } = await execAsync('docker info --format "{{.ServerVersion}}" 2>/dev/null || echo "N/A"', {
        timeout: 5000,
      })

      if (stdout.trim() === 'N/A' || stdout.includes('Cannot connect')) {
        return { name: 'Docker', status: 'degraded', message: 'Docker未运行或未安装' }
      }

      return {
        name: 'Docker',
        status: 'healthy',
        message: `Docker ${stdout.trim()}`,
      }
    } catch {
      return { name: 'Docker', status: 'degraded', message: 'Docker不可用' }
    }
  }

  // ----------------------------------------------------------
  // 工具方法
  // ----------------------------------------------------------

  private computeOverallStatus(checks: HealthCheckResult[]): HealthStatus {
    if (checks.some(c => c.status === 'unhealthy')) return 'unhealthy'
    if (checks.some(c => c.status === 'degraded')) return 'degraded'
    return 'healthy'
  }

  private formatBytes(bytes: number): string {
    const units = ['B', 'KB', 'MB', 'GB', 'TB']
    let unitIdx = 0
    let size = bytes
    while (size >= 1024 && unitIdx < units.length - 1) {
      size /= 1024
      unitIdx++
    }
    return `${size.toFixed(1)}${units[unitIdx]}`
  }
}

// ============================================================
// 格式化函数
// ============================================================

export function formatHealthReport(report: HealthReport): string {
  const lines: string[] = []
  const overallEmoji = { healthy: '✅', degraded: '⚠️', unhealthy: '🔴' }[report.overall]

  lines.push('### 🏥 系统健康检查\n')
  lines.push(`**总体状态**: ${overallEmoji} ${report.overall.toUpperCase()}`)
  lines.push(`**主机**: ${report.hostname} | **耗时**: ${report.duration}ms\n`)

  for (const check of report.checks) {
    const emoji = { healthy: '✅', degraded: '⚠️', unhealthy: '🔴' }[check.status]
    lines.push(`${emoji} **${check.name}**: ${check.message}`)
    if (check.detail) lines.push(`   _${check.detail}_`)
  }

  return lines.join('\n')
}

// ============================================================
// 全局单例
// ============================================================

let globalHealthChecker: HealthChecker | null = null

export function getHealthChecker(): HealthChecker {
  if (!globalHealthChecker) {
    globalHealthChecker = new HealthChecker()
  }
  return globalHealthChecker
}
