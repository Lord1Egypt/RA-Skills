/**
 * 类型定义统一导出
 */

export interface SSHConfig {
  host: string
  port?: number
  user?: string
  password?: string
  keyFile?: string
  name?: string
  tags?: string[]
}

export type ServerStatus = 'healthy' | 'warning' | 'offline' | 'unknown'

export class Server {
  constructor(
    public readonly id: string,
    public readonly host: string,
    public readonly port: number,
    public readonly user: string,
    public readonly name?: string,
    public readonly tags: string[] = []
  ) {}

  static fromSSHConfig(config: SSHConfig, idx?: number): Server {
    const id = `${config.host}:${config.port || 22}:${config.user || 'root'}`
    return new Server(
      id,
      config.host,
      config.port || 22,
      config.user || 'root',
      config.name || `server-${idx || config.host.replace(/\./g, '-')}`,
      config.tags || []
    )
  }

  getKey(): string {
    return `${this.host}:${this.port}:${this.user}`
  }

  hasTag(tag: string): boolean {
    return this.tags.includes(tag)
  }

  getDisplayName(): string {
    return this.name || this.host
  }
}

export interface HealthMetrics {
  uptime: string
  loadAverage: [number, number, number]
  memory: {
    total: number
    used: number
    free: number
    available: number
    swapTotal: number
    swapUsed: number
  }
  disk: {
    mountPoint: string
    total: number
    used: number
    available: number
    usagePercent: number
  }
}

export interface ServiceStatus {
  name: string
  running: boolean
}

export class ServerHealth {
  constructor(
    public readonly server: Server,
    public readonly status: ServerStatus,
    public readonly metrics?: HealthMetrics,
    public readonly services?: ServiceStatus[],
    public readonly checkedAt: Date = new Date(),
    public readonly error?: string
  ) {}

  static healthy(server: Server, metrics: HealthMetrics, services: ServiceStatus[]): ServerHealth {
    return new ServerHealth(server, ServerStatus.HEALTHY, metrics, services)
  }

  static warning(server: Server, metrics: HealthMetrics, services: ServiceStatus[], reason?: string): ServerHealth {
    return new ServerHealth(server, ServerStatus.WARNING, metrics, services, new Date(), reason)
  }

  static offline(server: Server, error: string): ServerHealth {
    return new ServerHealth(server, ServerStatus.OFFLINE, undefined, undefined, new Date(), error)
  }

  getDiskUsagePercent(): number {
    return this.metrics?.disk.usagePercent || 0
  }

  getMemoryUsagePercent(): number {
    if (!this.metrics) return 0
    const { total, used } = this.metrics.memory
    return Math.round((used / total) * 100)
  }

  getSwapUsagePercent(): number {
    if (!this.metrics) return 0
    const { swapTotal, swapUsed } = this.metrics.memory
    if (swapTotal === 0) return 0
    return Math.round((swapUsed / swapTotal) * 100)
  }
}

export interface ClusterHealthReport {
  totalServers: number
  healthy: number
  warning: number
  offline: number
  serverHealth: ServerHealth[]
  generatedAt: Date
}

export class ConfigValidationError extends Error {
  constructor(
    message: string,
    public readonly field?: string,
    public readonly value?: any
  ) {
    super(message)
    this.name = 'ConfigValidationError'
  }
}

export interface ConfigManagerOptions {
  configPath?: string
  watch?: boolean
  pollInterval?: number
}

export interface IServerRepository {
  findAll(): Promise<Server[]>
  findByTags(tags: string[]): Promise<Server[]>
  findById(id: string): Promise<Server | null>
  add(server: Server): Promise<void>
  update(server: Server): Promise<void>
  remove(host: string): Promise<void>
  onChange?(callback: () => void): void
}

export interface ICacheRepository {
  get<T>(key: string): Promise<T | null>
  set<T>(key: string, value: T, ttlSeconds?: number): Promise<void>
  delete(key: string): Promise<void>
  clear(): Promise<void>
}

export interface ISSHClient {
  execute(server: Server, command: string, timeout?: number): Promise<string>
  testConnection(server: Server): Promise<boolean>
  disconnect(server: Server): Promise<void>
  setCredentialsProvider(provider: ICredentialsProvider): void
}

export interface IHealthCheckStrategy {
  name: string
  priority: number
  check(server: Server, ssh: ISSHClient): Promise<any>
  isCritical(): boolean
}

export interface IReportFormatter {
  formatClusterReport(report: ClusterHealthReport): string
  formatServerHealth(health: ServerHealth): string
  formatPasswordReport(data: any): string
}

export interface INotifier {
  notify(title: string, message: string, level: 'info' | 'warning' | 'critical'): Promise<void>
}

export interface ICredentialsProvider {
  getCredentials(server: Server): Promise<{ password?: string; keyFile?: string; keyContent?: string } | null>
  setCredentials(server: Server, credentials: any): Promise<void>
}

export type OpsAction = 'health' | 'logs' | 'perf' | 'ports' | 'process' | 'disk' | 'password' | 'passwd' | 'expire'

export interface PasswordUserInfo {
  user: string
  lastChanged: string
  expires: string
  maxDays: string
  status: string
  daysLeft?: number
}

export interface ThresholdConfig {
  diskWarning: number
  diskCritical: number
  memoryWarning: number
  memoryCritical: number
  swapWarning: number
  swapCritical: number
  loadWarningMultiplier: number
  loadCriticalMultiplier: number
}

export interface ContainerOptions {
  configPath?: string
  useConnectionPool?: boolean
  cacheTTL?: number
  logLevel?: string
  environment?: string
}

export interface AppConfig {
  configPath?: string
  useConnectionPool?: boolean
  cacheTTL?: number
  logLevel?: string
  environment?: string
}

export interface LegacyAdapterConfig {
  configPath?: string
  useConnectionPool?: boolean
  cacheTTL?: number
  environment?: string
}