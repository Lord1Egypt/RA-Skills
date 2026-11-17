/**
 * 健康检查策略 - 简化版
 */

import type { Server, HealthMetrics, ServiceStatus } from '../config/schemas'
import type { ISSHClient } from '../config/schemas'

export interface IHealthCheckStrategy {
  name: string
  priority: number
  check(server: Server, ssh: ISSHClient): Promise<HealthMetrics>
  isCritical(): boolean
}

export abstract class BaseHealthCheckStrategy implements IHealthCheckStrategy {
  abstract name: string
  abstract priority: number
  abstract isCritical(): boolean
  abstract check(server: Server, ssh: ISSHClient): Promise<HealthMetrics>

  async execute(server: Server, ssh: ISSHClient) {
    try {
      const metrics = await this.check(server, ssh)
      return { success: true, metrics }
    } catch (error: any) {
      return { success: false, error: error.message }
    }
  }
}

export class LoadAverageCheck extends BaseHealthCheckStrategy {
  name = 'load_average'
  priority = 1
  isCritical() { return true }

  async check(server: Server, ssh: ISSHClient): Promise<HealthMetrics> {
    const output = await ssh.execute(server, 'uptime')
    const match = output.match(/load average:\s+([\d.]+),\s+([\d.]+),\s+([\d.]+)/)
    if (!match) throw new Error('无法解析负载')

    return {
      uptime: output.match(/up\s+([^,]+),/)?.[1]?.trim() || 'N/A',
      loadAverage: [parseFloat(match[1]), parseFloat(match[2]), parseFloat(match[3])],
      memory: { total: 0, used: 0, free: 0, available: 0, swapTotal: 0, swapUsed: 0 },
      disk: { mountPoint: '/', total: 0, used: 0, available: 0, usagePercent: 0 }
    }
  }
}

export class MemoryCheck extends BaseHealthCheckStrategy {
  name = 'memory_usage'
  priority = 2
  isCritical() { return true }

  async check(server: Server, ssh: ISSHClient): Promise<HealthMetrics> {
    const output = await ssh.execute(server, 'free -k 2>/dev/null || free 2>/dev/null')
    const memLine = output.split('\n').find(l => l.startsWith('Mem:'))
    if (!memLine) throw new Error('无法解析内存')

    const parts = memLine.trim().split(/\s+/)
    const total = parseInt(parts[1])
    const used = parseInt(parts[2])
    const free = parseInt(parts[3])
    const available = parseInt(parts[6] || parts[4])

    const swapLine = output.split('\n').find(l => l.startsWith('Swap:'))
    let swapTotal = 0, swapUsed = 0
    if (swapLine) {
      const sw = swapLine.trim().split(/\s+/)
      swapTotal = parseInt(sw[1])
      swapUsed = parseInt(sw[2])
    }

    return {
      uptime: 'N/A',
      loadAverage: [0, 0, 0],
      memory: { total, used, free, available, swapTotal, swapUsed },
      disk: { mountPoint: '/', total: 0, used: 0, available: 0, usagePercent: 0 }
    }
  }
}

export class DiskCheck extends BaseHealthCheckStrategy {
  name = 'disk_usage'
  priority = 3
  isCritical() { return true }

  async check(server: Server, ssh: ISSHClient): Promise<HealthMetrics> {
    const output = await ssh.execute(server, 'df -k / 2>/dev/null | tail -1')
    const parts = output.trim().split(/\s+/)
    if (parts.length < 6) throw new Error('无法解析磁盘')

    const total = parseInt(parts[1]) * 1024
    const used = parseInt(parts[2]) * 1024
    const available = parseInt(parts[3]) * 1024
    const usagePercent = parseFloat(parts[4].replace('%', ''))

    return {
      uptime: 'N/A',
      loadAverage: [0, 0, 0],
      memory: { total: 0, used: 0, free: 0, available: 0, swapTotal: 0, swapUsed: 0 },
      disk: { mountPoint: parts[5], total, used, available, usagePercent }
    }
  }
}

export class HealthChecker {
  private strategies: IHealthCheckStrategy[]

  constructor(strategies?: IHealthCheckStrategy[]) {
    this.strategies = strategies || [
      new LoadAverageCheck(),
      new MemoryCheck(),
      new DiskCheck()
    ]
    this.strategies.sort((a, b) => a.priority - b.priority)
  }

  async checkAll(server: Server, ssh: ISSHClient): Promise<HealthMetrics> {
    const result: Partial<HealthMetrics> = {
      uptime: 'N/A',
      loadAverage: [0, 0, 0],
      memory: { total: 0, used: 0, free: 0, available: 0, swapTotal: 0, swapUsed: 0 },
      disk: { mountPoint: '/', total: 0, used: 0, available: 0, usagePercent: 0 }
    }

    await Promise.all(this.strategies.map(async s => {
      const res = await s.execute(server, ssh)
      if (res.success && res.metrics) {
        Object.assign(result, res.metrics)
      }
    }))

    return result as HealthMetrics
  }
}

export async function checkServices(server: Server, ssh: ISSHClient, services: string[] = ['nginx', 'docker', 'postgresql', 'redis-server']): Promise<ServiceStatus[]> {
  const results: ServiceStatus[] = []
  for (const svc of services) {
    try {
      const status = await ssh.execute(server, `systemctl is-active ${svc} 2>/dev/null || echo "stopped"`)
      results.push({ name: svc, running: status.trim() === 'active' })
    } catch {
      results.push({ name: svc, running: false })
    }
  }
  return results
}