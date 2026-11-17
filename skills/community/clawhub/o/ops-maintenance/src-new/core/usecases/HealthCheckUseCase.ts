/**
 * 健康检查用例
 * 协调多个组件完成服务器健康检查
 */

import type {
  Server,
  ServerHealth,
  ServerStatus,
  HealthMetrics,
  ServiceStatus,
  ClusterHealthReport,
  IServerRepository,
  ISSHClient
} from '../config/schemas'
import { HealthChecker } from '../../infrastructure/monitoring/HealthChecker'
import { ThresholdChecker } from '../../infrastructure/monitoring/ThresholdChecker'
import { checkServices } from '../../infrastructure/monitoring/HealthChecker'
import type { ICacheRepository } from '../config/schemas'

/**
 * 健康检查用例输入
 */
export interface HealthCheckInput {
  /** 标签筛选 */
  tags?: string[]
  /** 指定服务器列表（覆盖标签筛选） */
  servers?: Server[]
  /** 是否强制刷新（忽略缓存） */
  force?: boolean
  /** 检查的服务列表 */
  services?: string[]
}

/**
 * 健康检查用例
 */
export class HealthCheckUseCase {
  constructor(
    private serverRepo: IServerRepository,
    private ssh: ISSHClient,
    private cache: ICacheRepository,
    private healthChecker: HealthChecker,
    private thresholdChecker: ThresholdChecker
  ) {}

  /**
   * 执行健康检查
   */
  async execute(input: HealthCheckInput = {}): Promise<ClusterHealthReport> {
    // 1. 获取目标服务器列表
    const targetServers = await this.resolveServers(input.tags, input.servers)

    // 2. 并发检查每台服务器
    const healthPromises = targetServers.map(server =>
      this.checkSingleServer(server, input.services, input.force)
    )

    const serverHealthList = await Promise.allSettled(healthPromises)

    // 3. 构建报告
    const serverHealth: ServerHealth[] = serverHealthList
      .filter((result): result is PromiseFulfilledResult<ServerHealth> => result.status === 'fulfilled')
      .map(result => result.value)

    const report: ClusterHealthReport = {
      totalServers: targetServers.length,
      healthy: serverHealth.filter(h => h.status === ServerStatus.HEALTHY).length,
      warning: serverHealth.filter(h => h.status === ServerStatus.WARNING).length,
      offline: serverHealth.filter(h => h.status === ServerStatus.OFFLINE).length,
      serverHealth,
      generatedAt: new Date()
    }

    return report
  }

  /**
   * 检查单台服务器
   */
  private async checkSingleServer(
    server: Server,
    services?: string[],
    force: boolean = false
  ): Promise<ServerHealth> {
    const cacheKey = `health:${server.id}`

    // 尝试从缓存获取（非强制刷新）
    if (!force) {
      const cached = await this.cache.get<ServerHealth>(cacheKey)
      if (cached && this.isCacheValid(cached)) {
        return cached
      }
    }

    try {
      // 1. 测试连接
      const isConnected = await this.ssh.testConnection(server)
      if (!isConnected) {
        return ServerHealth.offline(server, 'SSH 连接失败')
      }

      // 2. 执行健康检查（收集指标）
      const metrics = await this.healthChecker.checkAll(server, this.ssh)

      // 3. 检查服务状态
      const serviceList = services ?? ['nginx', 'docker', 'postgresql', 'redis-server']
      const serviceStatus = await checkServices(server, this.ssh, serviceList)

      // 4. 阈值评估
      const { overallStatus } = this.thresholdChecker.check(server.name, metrics)

      // 5. 构建健康对象
      const health = ServerHealth.healthy(server, metrics, serviceStatus)

      // 缓存结果
      await this.cache.set(cacheKey, health, 30) // 缓存 30 秒

      return health
    } catch (error: any) {
      return ServerHealth.offline(server, error.message)
    }
  }

  /**
   * 解析目标服务器列表
   */
  private async resolveServers(
    tags?: string[],
    explicitServers?: Server[]
  ): Promise<Server[]> {
    if (explicitServers && explicitServers.length > 0) {
      return explicitServers
    }

    if (tags && tags.length > 0) {
      return this.serverRepo.findByTags(tags)
    }

    return this.serverRepo.findAll()
  }

  /**
   * 检查缓存是否有效
   */
  private isCacheValid(health: ServerHealth): boolean {
    const now = new Date()
    const checkedAt = health.checkedAt
    const ageSeconds = (now.getTime() - checkedAt.getTime()) / 1000

    // 缓存有效期为 30 秒
    return ageSeconds < 30
  }
}