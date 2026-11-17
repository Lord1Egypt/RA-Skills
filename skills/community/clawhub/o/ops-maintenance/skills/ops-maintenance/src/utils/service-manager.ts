/**
 * 服务管理工具 v3.0
 *
 * 增强 Docker 容器管理、systemctl 深度信息
 * 本地和远程服务器均可用
 */

import { exec } from 'child_process'
import { promisify } from 'util'
import { validateCommand } from './command-validator.js'

const execAsync = promisify(exec)

// ============================================================
// 类型定义
// ============================================================

export interface DockerContainer {
  id: string
  name: string
  image: string
  status: string
  state: string
  ports: string
  created?: string
  network?: string
}

export interface DockerStats {
  container: string
  cpuPercent: number
  memoryUsage: string
  memoryPercent: number
  networkIO: string
  blockIO: string
  pids: number
}

export interface DockerInspect {
  id: string
  name: string
  image: string
  created: string
  status: string
  ipAddresses: string[]
  ports: Record<string, string>
  volumes: string[]
  env: string[]
  health?: {
    status: string
    failingStreak?: number
    log?: { start: string; exitCode: number; output: string }[]
  }
}

export interface ServiceStatus {
  name: string
  active: boolean
  state: string
  subState?: string
  pid?: number
  memory?: string
  cpu?: string
  uptime?: string
  detail: string
}

export interface ServiceLog {
  name: string
  entries: {
    timestamp: string
    level: string
    message: string
  }[]
}

// ============================================================
// Docker 管理器
// ============================================================

export class DockerManager {
  private timeout: number
  private remoteExec?: (cmd: string) => Promise<string>

  constructor(timeout: number = 15000, remoteExec?: (cmd: string) => Promise<string>) {
    this.timeout = timeout
    this.remoteExec = remoteExec
  }

  private async runCmd(cmd: string): Promise<string> {
    if (this.remoteExec) {
      return this.remoteExec(cmd)
    }
    const { stdout } = await execAsync(cmd, { timeout: this.timeout })
    return stdout
  }

  /** 列出容器 */
  async listContainers(all: boolean = false): Promise<DockerContainer[]> {
    try {
      const format = '--format "{{.ID}}|{{.Names}}|{{.Image}}|{{.Status}}|{{.State}}|{{.Ports}}"'
      const cmd = `docker ps ${all ? '-a' : ''} ${format}`
      const output = await this.runCmd(cmd)

      return output.trim().split('\n')
        .filter(l => l.trim())
        .map(line => {
          const parts = line.replace(/"/g, '').split('|')
          return {
            id: parts[0]?.trim() || '',
            name: parts[1]?.trim() || '',
            image: parts[2]?.trim() || '',
            status: parts[3]?.trim() || '',
            state: parts[4]?.trim() || '',
            ports: parts[5]?.trim() || '',
          }
        })
    } catch (error: any) {
      throw new Error(`获取容器列表失败: ${error.message}`)
    }
  }

  /** 获取容器资源使用 */
  async getStats(container?: string): Promise<DockerStats[]> {
    try {
      const cmd = container
        ? `docker stats --no-stream --format "{{.Container}}|{{.CPUPerc}}|{{.MemUsage}}|{{.MemPerc}}|{{.NetIO}}|{{.BlockIO}}|{{.PIDs}}" ${container}`
        : `docker stats --no-stream --format "{{.Container}}|{{.CPUPerc}}|{{.MemUsage}}|{{.MemPerc}}|{{.NetIO}}|{{.BlockIO}}|{{.PIDs}}"`

      const output = await this.runCmd(cmd)

      return output.trim().split('\n')
        .filter(l => l.trim())
        .map(line => {
          const parts = line.replace(/"/g, '').split('|')
          return {
            container: parts[0]?.trim() || '',
            cpuPercent: parseFloat(parts[1]?.replace('%', '') || '0'),
            memoryUsage: parts[2]?.trim() || '',
            memoryPercent: parseFloat(parts[3]?.replace('%', '') || '0'),
            networkIO: parts[4]?.trim() || '',
            blockIO: parts[5]?.trim() || '',
            pids: parseInt(parts[6]) || 0,
          }
        })
    } catch (error: any) {
      throw new Error(`获取容器状态失败: ${error.message}`)
    }
  }

  /** 检查容器详情 */
  async inspectContainer(nameOrId: string): Promise<DockerInspect> {
    try {
      const cmd = `docker inspect ${nameOrId}`
      const output = await this.runCmd(cmd)
      const data = JSON.parse(output)[0]

      // 提取网络信息
      const networks = data.NetworkSettings?.Networks || {}
      const ipAddresses = Object.values(networks as any[])
        .map((n: any) => n.IPAddress)
        .filter(Boolean)

      // 提取端口映射
      const ports: Record<string, string> = {}
      const portBindings = data.HostConfig?.PortBindings || {}
      for (const [containerPort, bindings] of Object.entries(portBindings)) {
        const b = (bindings as any[])?.[0]
        if (b) {
          ports[containerPort] = `${b.HostIp}:${b.HostPort}`
        }
      }

      // 提取环境变量
      const env = (data.Config?.Env || []) as string[]

      // 提取挂载
      const mounts = (data.Mounts || []) as any[]
      const volumes = mounts.map(m => `${m.Source}:${m.Destination}`)

      // 健康检查
      const health = data.State?.Health ? {
        status: data.State.Health.Status,
        failingStreak: data.State.Health.FailingStreak,
        log: data.State.Health.Log?.slice(-5).map((l: any) => ({
          start: l.Start,
          exitCode: l.ExitCode,
          output: l.Output?.substring(0, 200),
        })),
      } : undefined

      return {
        id: data.Id?.substring(0, 12),
        name: data.Name?.replace(/^\//, ''),
        image: data.Config?.Image,
        created: data.Created,
        status: data.State?.Status,
        ipAddresses,
        ports,
        volumes,
        env: env.map(e => e.split('=')[0] + '=' + (e.includes('=') ? '***' : '')), // 隐藏敏感值
        health,
      }
    } catch (error: any) {
      throw new Error(`检查容器失败: ${error.message}`)
    }
  }

  /** 获取容器日志 */
  async getLogs(nameOrId: string, lines: number = 50, since?: string): Promise<string> {
    try {
      const sinceArg = since ? `--since ${since}` : ''
      const cmd = `docker logs --tail ${lines} ${sinceArg} ${nameOrId} 2>&1`
      return await this.runCmd(cmd)
    } catch (error: any) {
      throw new Error(`获取容器日志失败: ${error.message}`)
    }
  }

  /** 列出镜像 */
  async listImages(): Promise<{ repository: string; tag: string; size: string; id: string }[]> {
    try {
      const cmd = 'docker images --format "{{.Repository}}|{{.Tag}}|{{.Size}}|{{.ID}}"'
      const output = await this.runCmd(cmd)

      return output.trim().split('\n')
        .filter(l => l.trim())
        .map(line => {
          const parts = line.replace(/"/g, '').split('|')
          return {
            repository: parts[0]?.trim() || '',
            tag: parts[1]?.trim() || '',
            size: parts[2]?.trim() || '',
            id: parts[3]?.trim()?.substring(0, 12) || '',
          }
        })
    } catch (error: any) {
      throw new Error(`获取镜像列表失败: ${error.message}`)
    }
  }

  // ----------------------------------------------------------
  // 格式化输出
  // ----------------------------------------------------------

  formatContainerList(containers: DockerContainer[]): string {
    if (containers.length === 0) return '无运行中的容器'

    const lines: string[] = []
    lines.push('### 🐳 Docker 容器\n')

    for (const c of containers) {
      const stateEmoji = c.state === 'running' ? '✅' : '⏹️'
      lines.push(`${stateEmoji} **${c.name}** (\`${c.id}\`)`)
      lines.push(`   镜像: ${c.image} | 状态: ${c.status}`)
      if (c.ports) lines.push(`   端口: ${c.ports}`)
      lines.push('')
    }

    return lines.join('\n')
  }

  formatStats(stats: DockerStats[]): string {
    if (stats.length === 0) return '无容器资源数据'

    const lines: string[] = []
    lines.push('### 📊 Docker 资源使用\n')
    lines.push('| 容器 | CPU | 内存 | 内存% | 网络 | 磁盘 | PID |')
    lines.push('|------|-----|------|-------|------|------|-----|')

    for (const s of stats) {
      lines.push(`| ${s.container} | ${s.cpuPercent.toFixed(1)}% | ${s.memoryUsage} | ${s.memoryPercent.toFixed(1)}% | ${s.networkIO} | ${s.blockIO} | ${s.pids} |`)
    }

    return lines.join('\n')
  }

  formatInspect(info: DockerInspect): string {
    const lines: string[] = []
    lines.push(`### 🔍 容器详情: ${info.name}\n`)
    lines.push(`- **ID**: ${info.id}`)
    lines.push(`- **镜像**: ${info.image}`)
    lines.push(`- **状态**: ${info.status}`)
    lines.push(`- **创建时间**: ${info.created}`)
    if (info.ipAddresses.length > 0) {
      lines.push(`- **IP地址**: ${info.ipAddresses.join(', ')}`)
    }
    if (Object.keys(info.ports).length > 0) {
      lines.push('- **端口映射**:')
      for (const [k, v] of Object.entries(info.ports)) {
        lines.push(`  - ${k} -> ${v}`)
      }
    }
    if (info.volumes.length > 0) {
      lines.push('- **挂载**:')
      for (const v of info.volumes) {
        lines.push(`  - ${v}`)
      }
    }
    if (info.health) {
      const healthEmoji = info.health.status === 'healthy' ? '💚' : '💔'
      lines.push(`- **健康检查**: ${healthEmoji} ${info.health.status}`)
      if (info.health.failingStreak) {
        lines.push(`  - 连续失败: ${info.health.failingStreak} 次`)
      }
    }

    return lines.join('\n')
  }
}

// ============================================================
// 服务管理器 (systemd)
// ============================================================

export class ServiceManager {
  private timeout: number
  private remoteExec?: (cmd: string) => Promise<string>

  constructor(timeout: number = 10000, remoteExec?: (cmd: string) => Promise<string>) {
    this.timeout = timeout
    this.remoteExec = remoteExec
  }

  private async runCmd(cmd: string): Promise<string> {
    if (this.remoteExec) {
      return this.remoteExec(cmd)
    }
    const { stdout } = await execAsync(cmd, { timeout: this.timeout })
    return stdout
  }

  /** 获取服务状态 (systemd) */
  async getStatus(serviceName: string): Promise<ServiceStatus> {
    try {
      const cmd = `systemctl status ${serviceName} 2>&1 || true`
      const output = await this.runCmd(cmd)

      const active = output.includes('Active: active')
      const stateMatch = output.match(/Active:\s*(\S+)\s*(\([^)]+\))?/)
      const state = stateMatch ? stateMatch[1] : 'unknown'
      const subState = stateMatch?.[2]?.replace(/[()]/g, '')

      const pidMatch = output.match(/Main PID:\s*(\d+)/)
      const pid = pidMatch ? parseInt(pidMatch[1]) : undefined

      const memMatch = output.match(/Memory:\s*([\d.]+\s*\w+)/)
      const memory = memMatch?.[1]

      const cpuMatch = output.match(/CPU:\s*([\d.]+\w+)/)
      const cpu = cpuMatch?.[1]

      return {
        name: serviceName,
        active,
        state,
        subState,
        pid,
        memory,
        cpu,
        detail: output.trim(),
      }
    } catch (error: any) {
      return {
        name: serviceName,
        active: false,
        state: 'error',
        detail: `获取服务状态失败: ${error.message}`,
      }
    }
  }

  /** 获取服务日志 (journalctl) */
  async getLogs(serviceName: string, lines: number = 50, since?: string): Promise<ServiceLog> {
    try {
      const sinceArg = since ? `--since "${since}"` : ''
      const cmd = `journalctl -u ${serviceName} -n ${lines} --no-pager ${sinceArg} -o short-iso 2>&1`
      const output = await this.runCmd(cmd)

      const entries = output.trim().split('\n')
        .filter(l => l.trim() && !l.startsWith('--'))
        .map(line => {
          const match = line.match(/^(\S+)\s+(\S+)\s+(.+)/)
          return {
            timestamp: match?.[1] || '',
            level: 'info', // journalctl 不直接提供级别
            message: match?.[3] || line,
          }
        })

      return { name: serviceName, entries }
    } catch (error: any) {
      return { name: serviceName, entries: [] }
    }
  }

  /** 批量检查服务状态 */
  async batchStatus(services: string[]): Promise<ServiceStatus[]> {
    const results: ServiceStatus[] = []
    for (const svc of services) {
      results.push(await this.getStatus(svc))
    }
    return results
  }

  /** 格式化服务状态 */
  formatStatus(status: ServiceStatus): string {
    const emoji = status.active ? '✅' : '❌'
    const lines: string[] = []
    lines.push(`### ⚙️ 服务状态: ${status.name}\n`)
    lines.push(`${emoji} **${status.state}** ${status.subState ? `(${status.subState})` : ''}`)
    if (status.pid) lines.push(`- PID: ${status.pid}`)
    if (status.memory) lines.push(`- 内存: ${status.memory}`)
    if (status.cpu) lines.push(`- CPU: ${status.cpu}`)
    return lines.join('\n')
  }

  /** 格式化批量状态 */
  formatBatchStatus(statuses: ServiceStatus[]): string {
    const lines: string[] = []
    lines.push('### ⚙️ 服务状态总览\n')

    for (const s of statuses) {
      const emoji = s.active ? '✅' : '❌'
      lines.push(`${emoji} **${s.name}**: ${s.state} ${s.subState || ''}`)
      if (s.memory) lines.push(`   内存: ${s.memory} | CPU: ${s.cpu || 'N/A'}`)
    }

    return lines.join('\n')
  }
}
