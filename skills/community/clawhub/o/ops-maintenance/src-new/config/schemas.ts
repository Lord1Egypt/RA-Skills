/**
 * 配置层类型定义
 * 定义所有核心数据模型和验证 Schema
 */

/**
 * SSH 配置
 */
export interface SSHConfig {
  /** 主机地址（IP或域名） */
  host: string
  /** SSH 端口，默认 22 */
  port?: number
  /** 用户名，默认 root */
  user?: string
  /** 密码认证（可选，如果未提供则使用密钥） */
  password?: string
  /** 密钥文件路径 */
  keyFile?: string
  /** 友好名称，用于显示 */
  name?: string
  /** 标签/分组，用于筛选 */
  tags?: string[]
}

/**
 * 服务器状态枚举
 */
export enum ServerStatus {
  HEALTHY = 'healthy',
  WARNING = 'warning',
  OFFLINE = 'offline',
  UNKNOWN = 'unknown'
}

/**
 * 服务器实体（领域层核心对象）
 */
export class Server {
  constructor(
    public readonly id: string,
    public readonly host: string,
    public readonly port: number,
    public readonly user: string,
    public readonly name?: string,
    public readonly tags: string[] = []
  ) {}

  /**
   * 从 SSHConfig 创建 Server
   */
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

  /**
   * 生成唯一标识
   */
  getKey(): string {
    return `${this.host}:${this.port}:${this.user}`
  }

  /**
   * 是否匹配标签
   */
  hasTag(tag: string): boolean {
    return this.tags.includes(tag)
  }

  /**
   * 显示名称
   */
  getDisplayName(): string {
    return this.name || this.host
  }
}

/**
 * 健康状态详细指标
 */
export interface HealthMetrics {
  /** 系统运行时间（如 "34 days, 16:44"） */
  uptime: string
  /** 负载平均值 [1分钟, 5分钟, 15分钟] */
  loadAverage: [number, number, number]
  /** 内存统计（字节） */
  memory: {
    total: number
    used: number
    free: number
    available: number
    swapTotal: number
    swapUsed: number
  }
  /** 磁盘使用统计 */
  disk: {
    mountPoint: string
    total: number
    used: number
    available: number
    usagePercent: number
  }
}

/**
 * 服务状态
 */
export interface ServiceStatus {
  name: string
  running: boolean
  pid?: number
}

/**
 * 服务器健康检查结果
 */
export class ServerHealth {
  constructor(
    public readonly server: Server,
    public readonly status: ServerStatus,
    public readonly metrics?: HealthMetrics,
    public readonly services?: ServiceStatus[],
    public readonly checkedAt: Date = new Date(),
    public readonly error?: string
  ) {}

  /**
   * 从检查结果创建
   */
  static healthy(server: Server, metrics: HealthMetrics, services: ServiceStatus[]): ServerHealth {
    return new ServerHealth(server, ServerStatus.HEALTHY, metrics, services)
  }

  static warning(server: Server, metrics: HealthMetrics, services: ServiceStatus[], reason?: string): ServerHealth {
    return new ServerHealth(server, ServerStatus.WARNING, metrics, services, new Date(), reason)
  }

  static offline(server: Server, error: string): ServerHealth {
    return new ServerHealth(server, ServerStatus.OFFLINE, undefined, undefined, new Date(), error)
  }

  /**
   * 磁盘使用率（0-100）
   */
  getDiskUsagePercent(): number {
    return this.metrics?.disk.usagePercent || 0
  }

  /**
   * 内存使用率（0-100）
   */
  getMemoryUsagePercent(): number {
    if (!this.metrics) return 0
    const { total, used } = this.metrics.memory
    return Math.round((used / total) * 100)
  }

  /**
   * Swap 使用率（0-100）
   */
  getSwapUsagePercent(): number {
    if (!this.metrics) return 0
    const { swapTotal, swapUsed } = this.metrics.memory
    if (swapTotal === 0) return 0
    return Math.round((swapUsed / swapTotal) * 100)
  }
}

/**
 * 集群健康报告
 */
export interface ClusterHealthReport {
  totalServers: number
  healthy: number
  warning: number
  offline: number
  serverHealth: ServerHealth[]
  generatedAt: Date
}

/**
 * 配置验证错误
 */
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

/**
 * 配置管理器选项
 */
export interface ConfigManagerOptions {
  /** 配置文件路径 */
  configPath?: string
  /** 是否启用热重载 */
  watch?: boolean
  /** 配置文件修改轮询间隔（ms） */
  pollInterval?: number
}

/**
 * 服务器仓库接口（领域层）
 */
export interface IServerRepository {
  /** 获取所有服务器 */
  findAll(): Promise<Server[]>
  /** 按标签查找 */
  findByTags(tags: string[]): Promise<Server[]>
  /** 按 ID 查找 */
  findById(id: string): Promise<Server | null>
  /** 添加服务器 */
  add(server: Server): Promise<void>
  /** 更新服务器 */
  update(server: Server): Promise<void>
  /** 删除服务器 */
  remove(host: string): Promise<void>
  /** 监听配置变更 */
  onChange?(callback: () => void): void
}

/**
 * 缓存仓库接口
 */
export interface ICacheRepository {
  /** 获取缓存 */
  get<T>(key: string): Promise<T | null>
  /** 设置缓存 */
  set<T>(key: string, value: T, ttlSeconds?: number): Promise<void>
  /** 删除缓存 */
  delete(key: string): Promise<void>
  /** 清空所有缓存 */
  clear(): Promise<void>
}

/**
 * SSH 凭据
 */
export interface SSHCredentials {
  /** 密码（如果使用密码认证） */
  password?: string
  /** 密钥文件路径（如果使用密钥认证） */
  keyFile?: string
  /** 私钥内容（可选，直接提供密钥内容） */
  keyContent?: string
}

/**
 * 凭据提供者接口
 */
export interface ICredentialsProvider {
  /**
   * 获取服务器的 SSH 凭据
   */
  getCredentials(server: Server): Promise<SSHCredentials | null>
  /**
   * 更新或存储服务器的凭据
   */
  setCredentials(server: Server, credentials: SSHCredentials): Promise<void>
}

/**
 * SSH 客户端接口
 */
export interface ISSHClient {
  /** 执行远程命令 */
  execute(server: Server, command: string, timeout?: number): Promise<string>
  /** 测试连接 */
  testConnection(server: Server): Promise<boolean>
  /** 关闭连接 */
  disconnect(server: Server): Promise<void>
  /** 设置凭据提供者 */
  setCredentialsProvider(provider: ICredentialsProvider): void
}

/**
 * 健康检查策略接口
 */
export interface IHealthCheckStrategy {
  /** 策略名称 */
  name: string
  /** 优先级（数字越小优先级越高） */
  priority: number
  /** 执行检查 */
  check(server: Server): Promise<HealthMetrics>
  /** 是否关键指标（影响总体健康状态） */
  isCritical(): boolean
}

/**
 * 格式化器接口
 */
export interface IReportFormatter {
  /** 格式化集群报告 */
  formatClusterReport(report: ClusterHealthReport): string
  /** 格式化单服务器报告 */
  formatServerHealth(health: ServerHealth): string
  /** 格式化密码过期报告 */
  formatPasswordReport(data: any): string
}

/**
 * 通知器接口
 */
export interface INotifier {
  /** 发送通知 */
  notify(title: string, message: string, level: 'info' | 'warning' | 'critical'): Promise<void>
}

/**
 * 邮件通知配置
 */
export interface EmailConfig {
  host: string
  port: number
  user: string
  password: string
  from: string
  to: string[]
  ssl?: boolean
  alertOnly?: boolean
}