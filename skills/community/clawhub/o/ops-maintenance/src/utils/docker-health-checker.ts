/**
 * Docker 容器健康巡检器 v1.0
 *
 * 自动巡检 Docker 容器健康状况
 * 检测: 重启次数、OOM Kill、健康检查失败、镜像过期、资源超限、僵尸容器
 */

import { exec } from 'child_process'
import { promisify } from 'util'
import { getAuditLogger } from './audit-logger.js'

const execAsync = promisify(exec)

// ============================================================
// 类型定义
// ============================================================

export type ContainerHealthStatus = 'healthy' | 'warning' | 'critical'

export interface ContainerInfo {
  id: string
  name: string
  image: string
  status: string
  state: string
  created: number
  restartCount: number
  oomKilled: boolean
  healthStatus?: string
  healthFailingStreak?: number
  ports: string[]
  uptime?: string
}

export interface ContainerCheckResult {
  container: string
  image: string
  status: ContainerHealthStatus
  issues: ContainerIssue[]
}

export interface ContainerIssue {
  type: string
  severity: 'warning' | 'critical' | 'info'
  message: string
  suggestion: string
}

export interface DockerHealthReport {
  timestamp: string
  totalContainers: number
  running: number
  stopped: number
  healthy: number
  warning: number
  critical: number
  results: ContainerCheckResult[]
  imageUpdates: ImageUpdateInfo[]
  summary: string
}

export interface ImageUpdateInfo {
  image: string
  currentTag: string
  created: string
  sizeMb: number
  daysOld: number
  needsUpdate: boolean
}

// ============================================================
// 容器健康巡检器
// ============================================================

export class DockerHealthChecker {
  private timeout: number
  private maxRestartCount: number
  private maxImageAgeDays: number

  constructor(options: {
    timeout?: number
    maxRestartCount?: number
    maxImageAgeDays?: number
  } = {}) {
    this.timeout = options.timeout || 15000
    this.maxRestartCount = options.maxRestartCount || 5
    this.maxImageAgeDays = options.maxImageAgeDays || 90
  }

  /**
   * 执行完整的容器健康巡检
   */
  async runFullInspection(): Promise<DockerHealthReport> {
    const start = Date.now()
    const logger = getAuditLogger()

    // 检查 Docker 是否可用
    const dockerAvailable = await this.isDockerAvailable()
    if (!dockerAvailable) {
      return {
        timestamp: new Date().toISOString(),
        totalContainers: 0, running: 0, stopped: 0,
        healthy: 0, warning: 0, critical: 0,
        results: [], imageUpdates: [],
        summary: 'Docker 不可用或未安装'
      }
    }

    // 获取所有容器信息
    const containers = await this.getAllContainers()
    const results: ContainerCheckResult[] = []

    // 逐个检查
    for (const c of containers) {
      const issues = await this.inspectContainer(c)
      const worstSeverity = issues.reduce<ContainerHealthStatus>(
        (acc, i) => i.severity === 'critical' ? 'critical' : (acc === 'critical' ? 'critical' : i.severity === 'warning' ? 'warning' : acc),
        'healthy'
      )
      results.push({
        container: c.name,
        image: c.image,
        status: worstSeverity,
        issues
      })
    }

    // 检查镜像更新
    const imageUpdates = await this.checkImageUpdates()

    // 统计
    const running = containers.filter(c => c.state === 'running').length
    const stopped = containers.filter(c => c.state !== 'running').length
    const healthy = results.filter(r => r.status === 'healthy').length
    const warning = results.filter(r => r.status === 'warning').length
    const critical = results.filter(r => r.status === 'critical').length

    const duration = Date.now() - start
    logger.log({
      timestamp: new Date().toISOString(),
      operation: 'docker-health',
      server: 'local',
      command: 'full-inspection',
      status: 'success',
      duration
    })

    return {
      timestamp: new Date().toISOString(),
      totalContainers: containers.length,
      running, stopped, healthy, warning, critical,
      results, imageUpdates,
      summary: `共 ${containers.length} 个容器: ${healthy}健康 / ${warning}告警 / ${critical}严重`
    }
  }

  /**
   * 检查 Docker 是否可用
   */
  async isDockerAvailable(): Promise<boolean> {
    try {
      await execAsync('docker info', { timeout: 5000 })
      return true
    } catch {
      return false
    }
  }

  /**
   * 获取所有容器信息（含已停止的）
   */
  async getAllContainers(): Promise<ContainerInfo[]> {
    try {
      const { stdout } = await execAsync(
        'docker ps -a --format "{{.ID}}\\t{{.Names}}\\t{{.Image}}\\t{{.Status}}\\t{{.State}}\\t{{.CreatedAt}}\\t{{.Ports}}"',
        { timeout: this.timeout }
      )

      if (!stdout.trim()) return []

      return stdout.trim().split('\n').map(line => {
        const [id, name, image, status, state, created, ports] = line.split('\t')
        return {
          id: id || '',
          name: name || '',
          image: image || '',
          status: status || '',
          state: state || '',
          created: new Date(created || '').getTime() / 1000,
          restartCount: 0,
          oomKilled: false,
          ports: ports ? ports.split(',').filter(Boolean) : []
        }
      })
    } catch {
      return []
    }
  }

  /**
   * 深度检查单个容器
   */
  async inspectContainer(container: ContainerInfo): Promise<ContainerIssue[]> {
    const issues: ContainerIssue[] = []

    // 1. 检查容器状态
    if (container.state !== 'running') {
      issues.push({
        type: 'container-stopped',
        severity: 'critical',
        message: `容器已停止: ${container.status}`,
        suggestion: '检查容器日志: docker logs ' + container.name
      })
      return issues // 停止的容器不需要继续检查
    }

    // 2. 获取容器详情 (inspect)
    try {
      const { stdout } = await execAsync(
        `docker inspect --format '{{.RestartCount}}|{{.State.OomKilled}}|{{.State.Health.Status}}|{{.State.Health.FailingStreak}}|{{.State.StartedAt}}' ${container.id}`,
        { timeout: this.timeout }
      )

      const [restartStr, oomStr, healthStr, failingStr, startedAt] = stdout.trim().split('|')
      container.restartCount = parseInt(restartStr || '0', 10)
      container.oomKilled = oomStr === 'true'
      container.healthStatus = healthStr || undefined
      container.healthFailingStreak = parseInt(failingStr || '0', 10)

      // 计算运行时间
      if (startedAt && startedAt !== '<nil>') {
        const startMs = new Date(startedAt).getTime()
        const uptimeMs = Date.now() - startMs
        container.uptime = this.formatDuration(uptimeMs)
      }
    } catch {
      // inspect 失败，用基本信息
    }

    // 3. 重启次数检查
    if (container.restartCount > this.maxRestartCount) {
      issues.push({
        type: 'restart-exceeded',
        severity: 'critical',
        message: `重启次数 ${container.restartCount} 次超过阈值 ${this.maxRestartCount}`,
        suggestion: '检查应用是否崩溃: docker logs --tail 100 ' + container.name
      })
    } else if (container.restartCount > 0) {
      issues.push({
        type: 'restart-detected',
        severity: 'warning',
        message: `容器已重启 ${container.restartCount} 次`,
        suggestion: '关注重启原因: docker logs --tail 50 ' + container.name
      })
    }

    // 4. OOM Kill 检查
    if (container.oomKilled) {
      issues.push({
        type: 'oom-killed',
        severity: 'critical',
        message: '容器因内存不足被 OOM Kill',
        suggestion: '增加内存限制: docker update --memory 512m ' + container.name
      })
    }

    // 5. 健康检查失败
    if (container.healthStatus === 'unhealthy') {
      issues.push({
        type: 'health-check-failing',
        severity: 'critical',
        message: `健康检查失败 ${container.healthFailingStreak || '?'} 次`,
        suggestion: '检查健康检查命令和容器内服务状态'
      })
    } else if (container.healthStatus === 'starting') {
      issues.push({
        type: 'health-check-starting',
        severity: 'warning',
        message: '健康检查仍在启动中',
        suggestion: '服务启动较慢，关注是否正常'
      })
    }

    // 6. 资源使用检查
    try {
      const { stdout } = await execAsync(
        `docker stats ${container.id} --no-stream --format "{{.CPUPerc}}|{{.MemUsage}}|{{.MemPerc}}|{{.NetIO}}|{{.BlockIO}}"`,
        { timeout: 10000 }
      )

      const [cpuPerc, memUsage, memPerc, netIo, blockIo] = stdout.trim().split('|')
      const cpuNum = parseFloat(cpuPerc?.replace('%', '') || '0')
      const memNum = parseFloat(memPerc?.replace('%', '') || '0')

      if (cpuNum > 90) {
        issues.push({
          type: 'cpu-overuse',
          severity: 'critical',
          message: `CPU 使用率 ${cpuNum.toFixed(1)}%`,
          suggestion: '检查进程负载或增加 CPU 限制'
        })
      } else if (cpuNum > 70) {
        issues.push({
          type: 'cpu-high',
          severity: 'warning',
          message: `CPU 使用率 ${cpuNum.toFixed(1)}%`,
          suggestion: '关注 CPU 使用趋势'
        })
      }

      if (memNum > 90) {
        issues.push({
          type: 'memory-overuse',
          severity: 'critical',
          message: `内存使用率 ${memNum.toFixed(1)}% (${memUsage?.trim()})`,
          suggestion: '增加内存限制或检查内存泄漏'
        })
      } else if (memNum > 75) {
        issues.push({
          type: 'memory-high',
          severity: 'warning',
          message: `内存使用率 ${memNum.toFixed(1)}% (${memUsage?.trim()})`,
          suggestion: '关注内存使用趋势'
        })
      }
    } catch {
      // stats 获取失败，跳过
    }

    // 7. 僵尸容器检查（运行时间极短且频繁重启）
    if (container.uptime) {
      const uptimeMatch = container.uptime.match(/(\d+)\s*秒/)
      if (uptimeMatch && parseInt(uptimeMatch[1]) < 60 && container.restartCount > 3) {
        issues.push({
          type: 'zombie-container',
          severity: 'critical',
          message: `容器运行仅 ${container.uptime}，已重启 ${container.restartCount} 次，疑似启动即崩溃`,
          suggestion: '检查启动命令和配置: docker inspect ' + container.name
        })
      }
    }

    return issues
  }

  /**
   * 检查镜像更新情况
   */
  async checkImageUpdates(): Promise<ImageUpdateInfo[]> {
    try {
      const { stdout } = await execAsync(
        'docker images --format "{{.Repository}}:{{.Tag}}\\t{{.CreatedAt}}\\t{{.Size}}"',
        { timeout: this.timeout }
      )

      if (!stdout.trim()) return []

      const images: ImageUpdateInfo[] = []
      const seen = new Set<string>()

      for (const line of stdout.trim().split('\n')) {
        const [imageTag, createdAt, size] = line.split('\t')
        if (!imageTag || imageTag.includes('<none>') || seen.has(imageTag)) continue
        seen.add(imageTag)

        // 计算镜像天数
        const createdDate = new Date(createdAt || '')
        const daysOld = Math.floor((Date.now() - createdDate.getTime()) / 86400000)
        const sizeStr = size || '0'
        const sizeMb = parseFloat(sizeStr.replace(/[^\d.]/g, '')) || 0

        images.push({
          image: imageTag,
          currentTag: imageTag.split(':').pop() || 'latest',
          created: createdAt || '',
          sizeMb,
          daysOld,
          needsUpdate: daysOld > this.maxImageAgeDays
        })
      }

      return images
    } catch {
      return []
    }
  }

  /**
   * 只检查指定容器
   */
  async inspectByName(name: string): Promise<ContainerCheckResult | null> {
    const containers = await this.getAllContainers()
    const target = containers.find(c => c.name === name || c.id.startsWith(name))
    if (!target) return null

    const issues = await this.inspectContainer(target)
    const worstSeverity = issues.reduce<ContainerHealthStatus>(
      (acc, i) => i.severity === 'critical' ? 'critical' : (acc === 'critical' ? 'critical' : i.severity === 'warning' ? 'warning' : acc),
      'healthy'
    )

    return {
      container: target.name,
      image: target.image,
      status: worstSeverity,
      issues
    }
  }

  /**
   * 格式化巡检报告
   */
  formatReport(report: DockerHealthReport): string {
    const lines: string[] = []

    lines.push('='.repeat(60))
    lines.push('  Docker 容器健康巡检报告')
    lines.push('='.repeat(60))
    lines.push(`  时间: ${report.timestamp}`)
    lines.push(`  ${report.summary}`)
    lines.push('-'.repeat(60))

    // 有问题的容器
    const problemContainers = report.results.filter(r => r.status !== 'healthy')
    if (problemContainers.length > 0) {
      lines.push('')
      lines.push('  [ 问题容器 ]')
      for (const r of problemContainers) {
        const mark = r.status === 'critical' ? '!!!' : ' ! '
        lines.push(`  [${mark}] ${r.container} (${r.image})`)
        for (const issue of r.issues) {
          lines.push(`       ${issue.type}: ${issue.message}`)
          lines.push(`       -> ${issue.suggestion}`)
        }
      }
    }

    // 镜像更新
    const oldImages = report.imageUpdates.filter(i => i.needsUpdate)
    if (oldImages.length > 0) {
      lines.push('')
      lines.push('  [ 镜像过期 ]')
      for (const img of oldImages) {
        lines.push(`  [!] ${img.image} - ${img.daysOld}天前创建 (${img.sizeMb}MB)`)
        lines.push(`      -> docker pull ${img.image}`)
      }
    }

    // 健康容器
    const healthyContainers = report.results.filter(r => r.status === 'healthy')
    if (healthyContainers.length > 0) {
      lines.push('')
      lines.push('  [ 健康容器 ]')
      for (const r of healthyContainers) {
        lines.push(`  [OK] ${r.container} (${r.image})`)
      }
    }

    lines.push('')
    lines.push('='.repeat(60))
    return lines.join('\n')
  }

  /**
   * 格式化时间
   */
  private formatDuration(ms: number): string {
    const seconds = Math.floor(ms / 1000)
    if (seconds < 60) return `${seconds} 秒`
    const minutes = Math.floor(seconds / 60)
    if (minutes < 60) return `${minutes} 分钟`
    const hours = Math.floor(minutes / 60)
    if (hours < 24) return `${hours} 小时`
    const days = Math.floor(hours / 24)
    return `${days} 天`
  }
}
