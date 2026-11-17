/**
 * 依赖注入容器
 * 管理所有核心组件的生命周期和依赖关系
 */

import type {
  IServerRepository,
  ISSHClient,
  ICacheRepository,
  EmailConfig,
  ICredentialsProvider
} from './config/schemas'
import { ServerFileRepository } from './infrastructure/repositories/ServerFileRepository'
import { SSHClient } from './infrastructure/ssh/SSHClient'
import { ConnectionPool } from './infrastructure/ssh/ConnectionPool'
import { MemoryCache } from './infrastructure/cache/CacheRepository'
import { HealthChecker } from './infrastructure/monitoring/HealthChecker'
import { ThresholdChecker, DEFAULT_THRESHOLDS } from './infrastructure/monitoring/ThresholdChecker'
import { HealthCheckUseCase } from './core/usecases/HealthCheckUseCase'
import { PasswordCheckUseCase } from './core/usecases/PasswordCheckUseCase'
import { DiskCheckUseCase } from './core/usecases/DiskCheckUseCase'
import { CLI } from './presentation/cli/CLI'
import { ConfigManagerCredentialsProvider } from './infrastructure/repositories/CredentialsRepository'
import { ConfigManager } from './config/loader'
import { EmailNotifier } from './infrastructure/notifiers/EmailNotifier'

/**
 * 容器配置选项
 */
export interface ContainerOptions {
  /** 配置文件路径 */
  configPath?: string
  /** 是否启用连接池 */
  useConnectionPool?: boolean
  /** 缓存 TTL（秒）*/
  cacheTTL?: number
  /** 日志级别 */
  logLevel?: string
  /** 环境 */
  environment?: string
  /** 邮件通知配置 */
  email?: Partial<EmailConfig>
}

/**
 * 依赖注入容器
 */
export class Container {
  private options: ContainerOptions
  private initialized: boolean = false

  // 单例实例
  private serverRepository?: IServerRepository
  private sshClient?: ISSHClient
  private connectionPool?: ConnectionPool
  private cache?: ICacheRepository
  private healthChecker?: HealthChecker
  private thresholdChecker?: ThresholdChecker
  private configManager?: ConfigManager
  private credentialsProvider?: ICredentialsProvider
  private emailNotifier?: EmailNotifier

  constructor(options: ContainerOptions = {}) {
    this.options = {
      configPath: options.configPath,
      useConnectionPool: options.useConnectionPool ?? true,
      cacheTTL: options.cacheTTL ?? 30,
      logLevel: options.logLevel ?? (process.env.NODE_ENV === 'production' ? 'info' : 'debug'),
      environment: options.environment ?? 'production',
      email: options.email
    }
  }

  /**
   * 初始化容器
   */
  async init(): Promise<void> {
    if (this.initialized) return

    // 1. 初始化日志
    // Logger.setLevel(this.options.logLevel) // TODO

    // 2. 初始化缓存
    this.cache = new MemoryCache(this.options.cacheTTL)

    // 3. 初始化 ConfigManager（作为配置和凭据来源）
    this.configManager = new ConfigManager({ configPath: this.options.configPath })
    await this.configManager.start()

    // 4. 初始化服务器仓库（基于 ConfigManager）
    this.serverRepository = new ServerFileRepository(undefined, this.configManager)
    await this.serverRepository.init()

    // 5. 初始化凭据提供者
    this.credentialsProvider = new ConfigManagerCredentialsProvider(this.configManager)

    // 6. 初始化 SSH 客户端
    this.sshClient = new SSHClient()
    this.sshClient.setCredentialsProvider(this.credentialsProvider)

    // 7. 初始化连接池
    if (this.options.useConnectionPool) {
      this.connectionPool = new ConnectionPool(this.sshClient)
      this.connectionPool.start()
    }

    // 8. 初始化监控组件
    this.healthChecker = new HealthChecker()
    this.thresholdChecker = new ThresholdChecker(undefined, this.options.environment)

    // 9. 初始化邮件通知器（如果有配置）
    if (this.options.email?.user && this.options.email?.password) {
      this.emailNotifier = new EmailNotifier(this.options.email)
      this.emailNotifier.init().catch(e => {
        console.warn('邮件初始化失败，告警功能不可用:', e.message)
      })
    }

    this.initialized = true
  }

  /**
   * 获取服务器仓库
   */
  getServerRepository(): IServerRepository {
    if (!this.serverRepository) {
      throw new Error('容器未初始化，请先调用 init()')
    }
    return this.serverRepository
  }

  /**
   * 获取 SSH 客户端
   */
  getSSHClient(): ISSHClient {
    if (!this.sshClient) {
      throw new Error('容器未初始化，请先调用 init()')
    }
    return this.sshClient
  }

  /**
   * 获取缓存
   */
  getCache(): ICacheRepository {
    if (!this.cache) {
      throw new Error('容器未初始化，请先调用 init()')
    }
    return this.cache
  }

  /**
   * 获取健康检查器
   */
  getHealthChecker(): HealthChecker {
    if (!this.healthChecker) {
      throw new Error('容器未初始化')
    }
    return this.healthChecker
  }

  /**
   * 获取阈值检查器
   */
  getThresholdChecker(): ThresholdChecker {
    if (!this.thresholdChecker) {
      throw new Error('容器未初始化')
    }
    return this.thresholdChecker
  }

  /**
   * 获取连接池
   */
  getConnectionPool(): ConnectionPool | undefined {
    return this.connectionPool
  }

  /**
   * 创建 CLI 实例并注入依赖
   */
  createCLI(): CLI {
    const cli = new CLI()
    cli.setDependencies(
      this.getServerRepository(),
      this.getSSHClient(),
      this.getCache(),
      this.options.email as EmailConfig | undefined
    )
    return cli
  }

  /**
   * 获取 ConfigManager
   */
  getConfigManager(): ConfigManager {
    if (!this.configManager) {
      throw new Error('容器未初始化')
    }
    return this.configManager
  }

  /**
   * 创建健康检查用例
   */
  createHealthCheckUseCase(): HealthCheckUseCase {
    return new HealthCheckUseCase(
      this.getServerRepository(),
      this.getSSHClient(),
      this.getCache(),
      this.getHealthChecker(),
      this.getThresholdChecker()
    )
  }

  /**
   * 创建密码检查用例
   */
  createPasswordCheckUseCase(): PasswordCheckUseCase {
    return new PasswordCheckUseCase(
      this.getServerRepository(),
      this.getSSHClient()
    )
  }

  /**
   * 创建磁盘检查用例
   */
  createDiskCheckUseCase(): DiskCheckUseCase {
    return new DiskCheckUseCase(
      this.getServerRepository(),
      this.getSSHClient()
    )
  }

  /**
   * 关闭容器（清理资源）
   */
  async shutdown(): Promise<void> {
    if (this.connectionPool) {
      this.connectionPool.stop()
    }
    if (this.sshClient) {
      await this.sshClient.disconnectAll()
    }
    if (this.configManager) {
      this.configManager.stop()
    }
    this.initialized = false
  }
}

/**
 * 全局容器实例
 */
let globalContainer: Container | null = null

/**
 * 获取全局容器
 */
export function getContainer(options?: ContainerOptions): Container {
  if (!globalContainer) {
    globalContainer = new Container(options)
  }
  return globalContainer
}

/**
 * 初始化全局容器
 */
export async function initContainer(options?: ContainerOptions): Promise<Container> {
  const container = getContainer(options)
  await container.init()
  return container
}