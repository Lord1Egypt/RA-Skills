/**
 * Markdown 格式化器
 * 生成美观的 Markdown 格式报告
 */

import type {
  ClusterHealthReport,
  ServerHealth,
  PasswordCheckResult,
  DiskInfo
} from '../../config/schemas'
import type { IReportFormatter } from '../../config/schemas'
import { ServerStatus } from '../../config/schemas'

/**
 * Markdown 格式化器
 */
export class MarkdownFormatter implements IReportFormatter {
  /**
   * 格式化集群健康报告
   */
  formatClusterReport(report: ClusterHealthReport): string {
    const lines: string[] = []

    lines.push('### 🖥️ 服务器集群状态\n')
    lines.push(`**检查时间**: ${report.generatedAt.toLocaleString('zh-CN')}\n`)

    // 概览表格
    lines.push('#### 集群概览')
    lines.push('| 服务器名称 | IP地址 | 端口 | 用户 | 状态 | 运行时间 | 负载(1/5/15) | 内存使用 | 磁盘根分区 | Swap使用 |')
    lines.push('|-----------|--------|------|------|------|----------|-------------|----------|------------|----------|')

    for (const health of report.serverHealth) {
      const row = this.formatServerRow(health)
      lines.push(row)
    }

    lines.push('')

    // 详细报告
    for (const health of report.serverHealth) {
      lines.push(`## 📊 ${health.server.getDisplayName()} 详细健康检查\n`)
      lines.push(this.formatServerHealth(health))
      lines.push('')
    }

    // 优化建议
    lines.push('### 💡 优化建议与操作步骤\n')
    lines.push('| 服务器 | 问题分类 | 严重等级 | 优化建议 | 操作步骤 |')
    lines.push('|--------|----------|----------|----------|----------|')

    const recommendations = this.generateRecommendations(report.serverHealth)
    for (const rec of recommendations) {
      lines.push(`| ${rec.server} | ${rec.category} | ${rec.severity} | ${rec.suggestion} | ${rec.steps} |`)
    }

    return lines.join('\n')
  }

  /**
   * 格式化单服务器行
   */
  private formatServerRow(health: ServerHealth): string {
    const server = health.server
    const statusDisplay = this.getStatusDisplay(health.status)

    // 提取信息
    const uptime = health.metrics?.uptime || '-'
    const load = health.metrics ? `${health.metrics.loadAverage[0].toFixed(2)}, ${health.metrics.loadAverage[1].toFixed(2)}, ${health.metrics.loadAverage[2].toFixed(2)}` : '-'
    const mem = health.metrics ? this.formatMemory(health.metrics) : '-'
    const disk = health.metrics ? this.formatDisk(health.metrics) : '-'
    const swap = health.metrics ? this.formatSwap(health.metrics) : '-'

    return `| ${server.getDisplayName()} | ${server.host} | ${server.port} | ${server.user} | ${statusDisplay} | ${uptime} | ${load} | ${mem} | ${disk} | ${swap} |`
  }

  /**
   * 格式化整台服务器健康详情
   */
  private formatServerHealth(health: ServerHealth): string {
    const lines: string[] = []

    // 系统信息
    lines.push('**系统:**')
    if (health.metrics) {
      const uptime = `uptime: ${health.metrics.uptime}`
      const memory = `内存: ${this.formatMemoryDetailed(health.metrics)}`
      const disk = `磁盘: ${this.formatDiskDetailed(health.metrics)}`
      lines.push(`\`\`\`\n${uptime}\n${memory}\n${disk}\n\`\`\``)
    } else {
      lines.push('`无可用数据`')
    }
    lines.push('')

    // 服务状态
    lines.push('**服务状态:**')
    if (health.services && health.services.length > 0) {
      for (const svc of health.services) {
        const emoji = svc.running ? '✅' : '❌'
        lines.push(`- ${svc.name}: ${emoji} ${svc.running ? '运行中' : '已停止'}`)
      }
    } else {
      lines.push('- 无服务状态信息')
    }

    if (health.error) {
      lines.push(`\n**错误**: \`${health.error}\``)
    }

    return lines.join('\n')
  }

  /**
   * 格式化内存使用
   */
  private formatMemory(metrics: any): string {
    if (!metrics.memory.total) return '-'
    const used = this.formatBytes(metrics.memory.used)
    const total = this.formatBytes(metrics.memory.total)
    return `${used}/${total}`
  }

  /**
   * 格式化磁盘使用
   */
  private formatDisk(metrics: any): string {
    if (!metrics.disk.total) return '-'
    const used = this.formatBytes(metrics.disk.used)
    const total = this.formatBytes(metrics.disk.total)
    const percent = metrics.disk.usagePercent
    return `${used}/${total} (${percent}%)`
  }

  /**
   * 格式化 Swap
   */
  private formatSwap(metrics: any): string {
    if (!metrics.memory.swapTotal) return '-'
    const used = this.formatBytes(metrics.memory.swapUsed)
    const total = this.formatBytes(metrics.memory.swapTotal)
    return `${used}/${total}`
  }

  /**
   * 详细内存信息
   */
  private formatMemoryDetailed(metrics: any): string {
    if (!metrics.memory.total) return 'N/A'
    const total = this.formatBytes(metrics.memory.total)
    const used = this.formatBytes(metrics.memory.used)
    const available = this.formatBytes(metrics.memory.available)
    const swap = metrics.memory.swapTotal > 0
      ? `, Swap: ${this.formatBytes(metrics.memory.swapUsed)}/${this.formatBytes(metrics.memory.swapTotal)}`
      : ''
    return `Total: ${total}, Used: ${used}, Available: ${available}${swap}`
  }

  /**
   * 详细磁盘信息
   */
  private formatDiskDetailed(metrics: any): string {
    if (!metrics.disk.total) return 'N/A'
    const total = this.formatBytes(metrics.disk.total)
    const used = this.formatBytes(metrics.disk.used)
    const avail = this.formatBytes(metrics.disk.available)
    const mount = metrics.disk.mountPoint
    return `${mount}: Total: ${total}, Used: ${used}, Avail: ${avail}`
  }

  /**
   * 格式化字节
   */
  private formatBytes(bytes: number): string {
    if (bytes >= 1099511627776) {
      return `${(bytes / 1099511627776).toFixed(1)}TiB`
    } else if (bytes >= 1073741824) {
      return `${(bytes / 1073741824).toFixed(1)}GiB`
    } else if (bytes >= 1048576) {
      return `${(bytes / 1048576).toFixed(1)}MiB`
    } else if (bytes >= 1024) {
      return `${(bytes / 1024).toFixed(1)}KiB`
    }
    return `${bytes}B`
  }

  /**
   * 获取状态显示
   */
  private getStatusDisplay(status: ServerStatus): string {
    switch (status) {
      case ServerStatus.HEALTHY:
        return '✅ 健康'
      case ServerStatus.WARNING:
        return '⚠️ 警告'
      case ServerStatus.OFFLINE:
        return '❌ 离线'
      default:
        return '❓ 未知'
    }
  }

  /**
   * 生成优化建议
   */
  private generateRecommendations(serverHealth: ServerHealth[]): any[] {
    const recommendations: any[] = []

    for (const health of serverHealth) {
      const serverName = health.server.getDisplayName()

      if (health.status === ServerStatus.OFFLINE) {
        recommendations.push({
          server: serverName,
          category: '连接问题',
          severity: '🔴 高',
          suggestion: 'SSH 连接失败，服务器不可达',
          steps: '1. 检查网络连通性<br>2. 确认 SSH 服务运行状态<br>3. 检查防火墙规则<br>4. 验证用户名/密码/密钥配置'
        })
        continue
      }

      if (!health.metrics) continue

      const diskPct = health.metrics.disk.usagePercent
      const memPct = Math.round((health.metrics.memory.used / health.metrics.memory.total) * 100)
      const swapPct = health.metrics.memory.swapTotal > 0
        ? Math.round((health.metrics.memory.swapUsed / health.metrics.memory.swapTotal) * 100)
        : 0
      const load1 = health.metrics.loadAverage[0]
      // 假设4核
      const loadRatio = load1 / 4

      // 磁盘检查
      if (diskPct >= 90) {
        recommendations.push({
          server: serverName,
          category: '磁盘空间',
          severity: '🔴 高',
          suggestion: `根分区使用率超过 90% (${diskPct}%)，空间紧张`,
          steps: '1. 清理日志文件<br>2. 删除临时不用的文件<br>3. 清理包管理器缓存<br>4. 扩展磁盘容量'
        })
      } else if (diskPct >= 80) {
        recommendations.push({
          server: serverName,
          category: '磁盘空间',
          severity: '🟡 中',
          suggestion: `根分区使用率超过 80% (${diskPct}%)，建议清理`,
          steps: '1. 查找大文件并清理<br>2. 归档旧日志<br>3. 清理未使用的软件包'
        })
      }

      // 内存检查
      if (memPct >= 90) {
        recommendations.push({
          server: serverName,
          category: '内存瓶颈',
          severity: '🔴 高',
          suggestion: `物理内存使用率超过 90% (${memPct}%)`,
          steps: '1. 立即重启高内存进程<br>2. 增加 swap 空间<br>3. 增加物理内存<br>4. 优化应用配置'
        })
      } else if (memPct >= 80) {
        recommendations.push({
          server: serverName,
          category: '内存压力',
          severity: '🟡 中',
          suggestion: `物理内存使用率超过 80% (${memPct}%)`,
          steps: '1. 监控内存使用趋势<br>2. 识别内存消耗大户<br>3. 优化 JVM/应用堆配置'
        })
      }

      // Swap 检查
      if (swapPct >= 90) {
        recommendations.push({
          server: serverName,
          category: '内存瓶颈',
          severity: '🔴 高',
          suggestion: `Swap 使用率超过 90% (${swapPct}%)，内存严重不足`,
          steps: '1. 增加物理内存<br>2. 优化应用内存使用<br>3. 检查内存泄漏<br>4. 调整 swappiness 参数'
        })
      } else if (swapPct >= 70) {
        recommendations.push({
          server: serverName,
          category: '内存压力',
          severity: '🟡 中',
          suggestion: `Swap 使用率超过 70% (${swapPct}%)`,
          steps: '1. 监控内存使用趋势<br>2. 识别高内存占用进程<br>3. 考虑增加内存'
        })
      }

      // 负载检查
      if (loadRatio >= 1.5) {
        recommendations.push({
          server: serverName,
          category: '系统负载',
          severity: '🔴 高',
          suggestion: `1分钟负载 ${load1.toFixed(2)} 超过 CPU 核数 1.5 倍`,
          steps: '1. 检查 CPU 密集型进程<br>2. 优化应用性能<br>3. 考虑水平扩展'
        })
      }
    }

    // 如果没有发现问题
    if (recommendations.length === 0 && report.serverHealth.every(h => h.status === ServerStatus.HEALTHY)) {
      recommendations.push({
        server: '所有服务器',
        category: '状态良好',
        severity: '🟢 低',
        suggestion: '所有服务器运行状态正常',
        steps: '继续保持定期巡检，关注趋势变化'
      })
    }

    return recommendations
  }

  /**
   * 格式化密码过期报告
   */
  formatPasswordReport(data: any): string {
    const lines: string[] = []
    const results = data.results || data

    lines.push('### 🔐 服务器密码过期检查\n')

    // 服务器概览
    lines.push('#### 服务器概览')
    lines.push('| 服务器名称 | IP地址 | 状态 | 概要 |')
    lines.push('|-----------|--------|------|------|')

    for (const result of results) {
      const statusEmoji = this.getPasswordStatusEmoji(result.status)
      lines.push(`| ${result.server} | ${result.host || '-'} | ${statusEmoji} ${result.status} | ${result.details} |`)
    }

    lines.push('')

    // 详细用户信息
    for (const result of results) {
      lines.push(`#### 📊 ${result.server}`)

      if (result.users && result.users.length > 0) {
        lines.push('| 用户 | 上次修改 | 过期日期 | 最大天数 | 剩余天数 | 状态 |')
        lines.push('|------|----------|----------|----------|----------|------|')

        for (const user of result.users) {
          const daysLeftStr = user.daysLeft !== undefined
            ? (user.daysLeft < 0 ? `已过期${Math.abs(user.daysLeft)}天` : `${user.daysLeft}天`)
            : '-'
          const userStatusEmoji = this.getPasswordStatusEmoji(user.status)
          lines.push(`| ${user.user} | ${user.lastChanged} | ${user.expires} | ${user.maxDays} | ${daysLeftStr} | ${userStatusEmoji} ${user.status} |`)
        }
      } else if (result.status.includes('检查失败')) {
        lines.push(`**连接失败**: ${result.details}`)
      } else {
        lines.push('未找到需要检查的本地用户')
      }

      lines.push('')
    }

    // 优化建议
    lines.push('### 💡 优化建议\n')
    const hasExpired = results.some((r: any) => r.status.includes('已过期') || r.status.includes('即将过期') || r.status.includes('永不过期'))

    if (hasExpired) {
      lines.push('| 服务器 | 用户 | 严重等级 | 建议 | 操作步骤 |')
      lines.push('|--------|------|----------|------|----------|')

      for (const result of results) {
        if (result.users) {
          for (const user of result.users) {
            if (user.status.includes('已过期')) {
              lines.push(`| ${result.server} | ${user.user} | 🔴 高 | 密码已过期 | 1. 立即修改密码<br>2. 检查密码策略<br>3. 更新相关应用配置<br>`)
            } else if (user.status.includes('即将过期')) {
              lines.push(`| ${result.server} | ${user.user} | 🟡 中 | 密码即将过期(${user.daysLeft}天) | 1. 计划修改密码<br>2. 通知相关人员<br>`)
            } else if (user.status.includes('永不过期')) {
              lines.push(`| ${result.server} | ${user.user} | ⚠️ 警告 | 密码永不过期（安全风险） | 1. 设置合理过期时间<br>2. 定期强制修改密码<br>`)
            }
          }
        }
      }
    } else {
      lines.push('| 服务器 | 严重等级 | 状态 | 说明 |')
      lines.push('|--------|----------|------|------|')
      lines.push('| 所有服务器 | 🟢 低 | 正常 | 所有可达服务器密码状态正常，建议定期巡检 |')
    }

    return lines.join('\n')
  }

  /**
   * 格式化服务器健康详情
   */
  formatServerHealth(health: ServerHealth): string {
    return this.formatServerHealthDetailed(health)
  }

  private formatServerHealthDetailed(health: ServerHealth): string {
    const lines: string[] = []

    lines.push(`### 🩺 远程服务器健康检查 (${health.server.host})\n`)

    // 系统信息
    lines.push('**系统:**')
    if (health.metrics) {
      lines.push('```')
      lines.push(`uptime: ${health.metrics.uptime}`)
      lines.push(`load average: ${health.metrics.loadAverage.map(l => l.toFixed(2)).join(', ')}`)
      lines.push(`memory: total=${this.formatBytes(health.metrics.memory.total)}, used=${this.formatBytes(health.metrics.memory.used)}`)
      lines.push(`disk: ${health.metrics.disk.mountPoint} ${this.formatBytes(health.metrics.disk.used)}/${this.formatBytes(health.metrics.disk.total)} (${health.metrics.disk.usagePercent}%)`)
      lines.push('```\n')
    } else {
      lines.push('`无可用数据`\n')
    }

    // 服务状态
    lines.push('**服务状态:**')
    if (health.services && health.services.length > 0) {
      for (const svc of health.services) {
        const emoji = svc.running ? '✅' : '❌'
        lines.push(`- ${svc.name}: ${emoji} ${svc.running ? '运行中' : '已停止'}`)
      }
    } else {
      lines.push('- 无服务状态信息')
    }

    if (health.error) {
      lines.push(`\n**错误**: \`${health.error}\``)
    }

    return lines.join('\n')
  }

  /**
   * 辅助：获取密码状态 emoji
   */
  private getPasswordStatusEmoji(status: string): string {
    if (status.includes('已过期')) return '❌'
    if (status.includes('即将过期')) return '⚠️'
    if (status.includes('永不过期')) return '⚠️'
    if (status.includes('正常')) return '✅'
    return '❓'
  }
}