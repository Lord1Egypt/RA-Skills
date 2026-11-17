/**
 * JSON 格式化器
 * 输出机器可读的 JSON 格式
 */

import type {
  ClusterHealthReport,
  ServerHealth,
  PasswordCheckResult,
  DiskInfo
} from '../../config/schemas'

/**
 * JSON 格式化器
 */
export class JsonFormatter {
  /**
   * 格式化集群健康报告为 JSON
   */
  formatClusterReport(report: ClusterHealthReport): string {
    const output = {
      type: 'cluster-health',
      generatedAt: report.generatedAt.toISOString(),
      summary: {
        totalServers: report.totalServers,
        healthy: report.healthy,
        warning: report.warning,
        offline: report.offline
      },
      servers: report.serverHealth.map(health => this.formatServerHealth(health))
    }

    return JSON.stringify(output, null, 2)
  }

  /**
   * 格式化单服务器健康状态
   */
  private formatServerHealth(health: ServerHealth): any {
    return {
      server: {
        id: health.server.id,
        host: health.server.host,
        port: health.server.port,
        user: health.server.user,
        name: health.server.name,
        tags: health.server.tags
      },
      status: health.status,
      checkedAt: health.checkedAt.toISOString(),
      error: health.error || null,
      metrics: health.metrics ? {
        uptime: health.metrics.uptime,
        loadAverage: health.metrics.loadAverage,
        memory: {
          total: health.metrics.memory.total,
          used: health.metrics.memory.used,
          free: health.metrics.memory.free,
          available: health.metrics.memory.available,
          swapTotal: health.metrics.memory.swapTotal,
          swapUsed: health.metrics.memory.swapUsed
        },
        disk: {
          mountPoint: health.metrics.disk.mountPoint,
          total: health.metrics.disk.total,
          used: health.metrics.disk.used,
          available: health.metrics.disk.available,
          usagePercent: health.metrics.disk.usagePercent
        }
      } : null,
      services: health.services || []
    }
  }

  /**
   * 格式化密码检查结果
   */
  formatPasswordReport(results: PasswordCheckResult[]): string {
    const output = {
      type: 'password-check',
      generatedAt: new Date().toISOString(),
      results: results.map(r => ({
        server: r.server,
        status: r.status,
        details: r.details,
        users: r.users.map(u => ({
          user: u.user,
          lastChanged: u.lastChanged,
          expires: u.expires,
          maxDays: u.maxDays,
          status: u.status,
          daysLeft: u.daysLeft
        }))
      }))
    }

    return JSON.stringify(output, null, 2)
  }

  /**
   * 格式化磁盘检查结果
   */
  formatDiskReport(disks: DiskInfo[]): string {
    const output = {
      type: 'disk-check',
      generatedAt: new Date().toISOString(),
      disks: disks.map(d => ({
        server: d.server,
        total: d.total,
        used: d.used,
        available: d.available,
        mountPoint: d.mountPoint,
        usagePercent: d.usagePercent,
        largeDirectories: d.largeDirectories
      }))
    }

    return JSON.stringify(output, null, 2)
  }
}