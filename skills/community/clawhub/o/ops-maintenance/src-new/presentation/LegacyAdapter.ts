/**
 * 向后兼容适配器
 * 将旧版 API 调用转换为新版架构
 */

import type {
  Server,
  SSHConfig,
  IServerRepository,
  ISSHClient,
  ICacheRepository,
  OpsAction,
  ClusterHealthReport,
  PasswordUserInfo
} from '../config/schemas'
import { ServerFileRepository } from '../infrastructure/repositories/ServerFileRepository'
import { SSHClient } from '../infrastructure/ssh/SSHClient'
import { MemoryCache } from '../infrastructure/cache/CacheRepository'
import { ConfigManagerCredentialsProvider } from '../infrastructure/repositories/CredentialsRepository'
import { ConfigManager } from '../config/loader'
import { Container } from '../container'
import { HealthCheckUseCase } from '../core/usecases/HealthCheckUseCase'
import { PasswordCheckUseCase } from '../core/usecases/PasswordCheckUseCase'
import { DiskCheckUseCase } from '../core/usecases/DiskCheckUseCase'
import { MarkdownFormatter } from '../presentation/formatters/MarkdownFormatter'
import { JsonFormatter } from '../presentation/formatters/JsonFormatter'
import { DEFAULT_THRESHOLDS } from '../infrastructure/monitoring/ThresholdChecker'
import { HealthChecker } from '../infrastructure/monitoring/HealthChecker'

/**
 * 适配器配置
 */
export interface LegacyAdapterConfig {
  configPath?: string
  useConnectionPool?: boolean
  cacheTTL?: number
  environment?: string
}

/**
 * 向后兼容适配器
 * 提供与旧版完全相同的导出函数签名
 */
export class LegacyAdapter {
  private container?: Container
  private serverRepo?: IServerRepository
  private sshClient?: ISSHClient
  private cache?: ICacheRepository
  private initialized: boolean = false

  constructor(private config?: LegacyAdapterConfig) {}

  /**
   * 初始化适配器
   */
  async init(): Promise<void> {
    if (this.initialized) return

    this.container = new Container({
      configPath: this.config?.configPath,
      useConnectionPool: this.config?.useConnectionPool ?? true,
      cacheTTL: this.config?.cacheTTL ?? 30,
      environment: this.config?.environment ?? 'production'
    })

    await this.container.init()

    this.serverRepo = this.container.getServerRepository()
    this.sshClient = this.container.getSSHClient()
    this.cache = this.container.getCache()

    this.initialized = true
  }

  /**
   * 确保已初始化
   */
  private ensureInitialized(): void {
    if (!this.initialized) {
      throw new Error('适配器未初始化，请先调用 init()')
    }
  }

  // ============ 配置管理函数（兼容旧版） ============

  async loadServers(): Promise<Server[]> {
    this.ensureInitialized()
    return this.serverRepo!.findAll()
  }

  async loadServerState(): Promise<any> {
    return null
  }

  async saveServerState(state: any): Promise<void> {}

  calculateServerChecksums(servers: Server[]): string[] {
    return servers.map(s => `${s.host}:${s.port || 22}:${s.user || 'root'}`).sort()
  }

  async detectNewServers(): Promise<{
    newServers: Server[];
    allServers: Server[];
    message: string;
  }> {
    const allServers = await this.loadServers()
    return {
      newServers: [],
      allServers,
      message: `当前配置了 ${allServers.length} 台服务器`
    }
  }

  async addServer(config: SSHConfig): Promise<void> {
    this.ensureInitialized()
    const server = Server.fromSSHConfig(config)
    await this.serverRepo!.add(server)
  }

  async removeServer(host: string): Promise<void> {
    this.ensureInitialized()
    await this.serverRepo!.remove(host)
  }

  async getServersByTag(tag: string): Promise<Server[]> {
    this.ensureInitialized()
    return this.serverRepo!.findByTags([tag])
  }

  async batchAddServers(servers: string[]): Promise<{ success: number; failed: number; details: string[] }> {
    this.ensureInitialized()
    const results: string[] = []
    let success = 0
    let failed = 0

    for (const serverStr of servers) {
      try {
        const config = this.parseServerString(serverStr)
        await this.addServer(config)
        success++
        results.push(`✅ ${config.name || config.host}:${config.port || 22} - 已添加`)
      } catch (error: any) {
        failed++
        results.push(`❌ ${serverStr} - ${error.message}`)
      }
    }

    return { success, failed, details: results }
  }

  async importServersFromText(text: string): Promise<{ success: number; failed: number; servers: Server[] }> {
    this.ensureInitialized()
    try {
      const parsed = JSON.parse(text)
      const arr = Array.isArray(parsed) ? parsed : [parsed]
      const servers: Server[] = []

      for (const item of arr) {
        if (item.host) {
          const config: SSHConfig = {
            host: item.host,
            port: item.port || 22,
            user: item.user,
            name: item.name,
            tags: item.tags
          }
          const server = Server.fromSSHConfig(config)
          servers.push(server)
          await this.addServer(config)
        }
      }

      return { success: servers.length, failed: 0, servers }
    } catch {
      return { success: 0, failed: 0, servers: [] }
    }
  }

  private parseServerString(serverStr: string): SSHConfig {
    let host = serverStr
    let user: string | undefined
    let port: number | undefined

    if (host.includes('@')) {
      const parts = host.split('@')
      user = parts[0]
      host = parts[1]
    }

    if (host.includes(':')) {
      const parts = host.split(':')
      host = parts[0]
      port = parseInt(parts[1])
    }

    const name = `server-${host.replace(/\./g, '-')}`
    return { host, port: port || 22, user, name }
  }

  // ============ 运维操作函数（兼容旧版） ============

  async checkAllServersHealth(
    tags?: string[],
    serverList?: Server[]
  ): Promise<{ server: string; status: string; details: string }[]> {
    this.ensureInitialized()

    const useCase = new HealthCheckUseCase(
      this.serverRepo!,
      this.sshClient!,
      this.cache!,
      new HealthChecker(),
      new ThresholdChecker(DEFAULT_THRESHOLDS)
    )

    const report = await useCase.execute({ tags, servers: serverList, force: false })

    return report.serverHealth.map(h => ({
      server: h.server.getDisplayName(),
      status: this.formatStatus(h.status),
      details: this.formatDetails(h)
    }))
  }

  private formatStatus(status: string): string {
    switch (status) {
      case 'healthy':
        return '✅ 健康'
      case 'warning':
        return '⚠️ 警告'
      case 'offline':
        return '❌ 离线'
      default:
        return '❓ 未知'
    }
  }

  private formatDetails(health: any): string {
    if (!health.metrics) return '无数据'
    const load = health.metrics.loadAverage
    return `负载: ${load ? `${load[0].toFixed(2)}, ${load[1].toFixed(2)}, ${load[2].toFixed(2)}` : 'N/A'}`
  }

  async checkRemoteHealth(
    config: SSHConfig,
    services: string[] = ['nginx', 'docker', 'postgresql', 'redis-server']
  ): Promise<string> {
    this.ensureInitialized()

    const server = Server.fromSSHConfig(config)
    const useCase = new HealthCheckUseCase(
      this.serverRepo!,
      this.sshClient!,
      this.cache!,
      new HealthChecker(),
      new ThresholdChecker(DEFAULT_THRESHOLDS)
    )

    const health = await useCase.execute({ servers: [server] })

    if (health.serverHealth.length === 0) {
      return `❌ **连接失败**: 无法连接到 ${config.host}`
    }

    const h = health.serverHealth[0]
    const formatter = new MarkdownFormatter()
    return formatter.formatServerHealth(h)
  }

  async checkAllServersPasswordExpiration(
    tags?: string[]
  ): Promise<Array<{ server: string; status: string; details: string; users?: PasswordUserInfo[] }>> {
    this.ensureInitialized()
    const useCase = new PasswordCheckUseCase(this.serverRepo!, this.sshClient!)
    return await useCase.execute(tags)
  }

  async checkAllServersPasswordExpirationReport(tags?: string[]): Promise<string> {
    this.ensureInitialized()
    const useCase = new PasswordCheckUseCase(this.serverRepo!, this.sshClient!)
    const results = await useCase.execute(tags)

    const formatter = new MarkdownFormatter()
    return formatter.formatPasswordReport({ results })
  }

  async getClusterSummary(): Promise<string> {
    this.ensureInitialized()

    const useCase = new HealthCheckUseCase(
      this.serverRepo!,
      this.sshClient!,
      this.cache!,
      new HealthChecker(),
      new ThresholdChecker(DEFAULT_THRESHOLDS)
    )

    const report = await useCase.execute()
    const formatter = new MarkdownFormatter()
    return formatter.formatClusterReport(report)
  }

  async runRemoteCommand(config: SSHConfig, command: string): Promise<string> {
    this.ensureInitialized()
    const server = Server.fromSSHConfig(config)
    try {
      return await this.sshClient!.execute(server, command)
    } catch (error: any) {
      return `错误: ${error.message}`
    }
  }

  async runCommand(cmd: string, timeout: number = 10000): Promise<string> {
    if (process.platform === 'win32') {
      return '⚠️ 当前系统为 Windows，runCommand 只能在 Linux/macOS 上执行。'
    }

    const { exec } = require('child_process')
    const { promisify } = require('util')
    const execAsync = promisify(exec)

    try {
      const { stdout, stderr } = await execAsync(cmd, { timeout, shell: '/bin/zsh' })
      return stdout || stderr || '(无输出)'
    } catch (error: any) {
      return `命令执行失败: ${error.message}`
    }
  }

  async executeOnAllServers(command: string, tags?: string[]): Promise<{ server: string; output: string }[]> {
    this.ensureInitialized()
    const servers = tags
      ? await this.serverRepo!.findByTags(tags)
      : await this.serverRepo!.findAll()

    const results: { server: string; output: string }[] = []

    await Promise.all(servers.map(async (server) => {
      try {
        const output = await this.sshClient!.execute(server, command)
        results.push({ server: server.getDisplayName(), output })
      } catch (error: any) {
        results.push({ server: server.getDisplayName(), output: `错误: ${error.message}` })
      }
    }))

    return results
  }

  // 占位函数（旧版未完全实现的功能）
  async checkRemotePort(config: SSHConfig, port?: number): Promise<string> {
    return `端口检查功能尚未完全实现`
  }

  async checkRemoteProcess(config: SSHConfig, name?: string): Promise<string> {
    return `进程检查功能尚未完全实现`
  }

  async checkRemoteDisk(config: SSHConfig): Promise<string> {
    return `磁盘检查: ${config.host}`
  }

  async checkRemotePerformance(config: SSHConfig): Promise<string> {
    return `性能检查功能尚未完全实现`
  }

  async checkRemoteLogs(config: SSHConfig, pattern?: string, lines?: number): Promise<string> {
    return `日志检查功能尚未完全实现`
  }

  async executeOp(action: string, arg?: string): Promise<string> {
    const actions: Record<string, () => Promise<string>> = {
      'health': () => this.getClusterSummary(),
      'check': () => this.getClusterSummary(),
      'cluster': () => this.getClusterSummary(),
      'password': () => this.checkAllServersPasswordExpirationReport(),
      'passwd': () => this.checkAllServersPasswordExpirationReport(),
      'expire': () => this.checkAllServersPasswordExpirationReport(),
      'disk': () => this.checkRemoteDisk({ host: 'local' }),
      'logs': () => Promise.resolve('日志检查未实现'),
      'log': () => Promise.resolve('日志检查未实现'),
      'perf': () => Promise.resolve('性能检查未实现'),
      'performance': () => Promise.resolve('性能检查未实现'),
      'ports': () => Promise.resolve('端口检查未实现'),
      'port': () => Promise.resolve('端口检查未实现'),
      'process': () => Promise.resolve('进程检查未实现'),
      'proc': () => Promise.resolve('进程检查未实现')
    }

    const fn = actions[action.toLowerCase()]
    if (fn) {
      return fn()
    }
    return `未知操作: ${action}`
  }

  async executeRemoteOp(action: string, config: SSHConfig, arg?: string): Promise<string> {
    return await this.executeOp(action, arg)
  }

  async shutdown(): Promise<void> {
    if (this.container) {
      await this.container.shutdown()
    }
  }
}

// 全局实例
let globalAdapter: LegacyAdapter | null = null

/**
 * 获取全局适配器
 */
export function getLegacyAdapter(config?: LegacyAdapterConfig): LegacyAdapter {
  if (!globalAdapter) {
    globalAdapter = new LegacyAdapter(config)
  }
  return globalAdapter
}

/**
 * 初始化全局适配器
 */
export async function initLegacyAdapter(config?: LegacyAdapterConfig): Promise<LegacyAdapter> {
  const adapter = getLegacyAdapter(config)
  await adapter.init()
  return adapter
}