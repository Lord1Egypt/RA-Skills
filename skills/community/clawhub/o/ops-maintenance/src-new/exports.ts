/**
 * 统一导出文件
 * 明确区分类型导出和值导出
 */

// 类型导出
export type {
  SSHConfig,
  HealthMetrics,
  ServiceStatus,
  ServerHealth,
  ClusterHealthReport,
  PasswordUserInfo,
  ThresholdConfig,
  IServerRepository,
  ICacheRepository,
  ISSHClient,
  IHealthCheckStrategy,
  IReportFormatter,
  INotifier,
  ICredentialsProvider,
  SSHCredentials,
  OpsAction
} from './config/schemas'

// 值和类型导出（类和枚举）
export { Server, ServerStatus } from './config/schemas'

// 接口（需要值导入，因为包含静态方法）
export { ConfigValidationError } from './config/validator'

// 实用工具类
export { MemoryCache, FileCache, TieredCache, CacheFactory } from './infrastructure/cache/CacheRepository'
export { SSHClient } from './infrastructure/ssh/SSHClient'
export { ConnectionPool } from './infrastructure/ssh/ConnectionPool'
export { HealthChecker, LoadAverageCheck, MemoryCheck, DiskCheck, ServiceStatusCheck, checkServices } from './infrastructure/monitoring/HealthChecker'
export { ThresholdChecker, DEFAULT_THRESHOLDS, ENV_THRESHOLDS } from './infrastructure/monitoring/ThresholdChecker'
export { ServerFileRepository, createServerRepository } from './infrastructure/repositories/ServerFileRepository'
export { ConfigManagerCredentialsProvider, EnvironmentCredentialsProvider } from './infrastructure/repositories/CredentialsRepository'

// UseCases
export { HealthCheckUseCase } from './core/usecases/HealthCheckUseCase'
export { PasswordCheckUseCase } from './core/usecases/PasswordCheckUseCase'
export { DiskCheckUseCase } from './core/usecases/DiskCheckUseCase'

// Presentation
export { MarkdownFormatter } from './presentation/formatters/MarkdownFormatter'
export { JsonFormatter } from './presentation/formatters/JsonFormatter'
export { CommandParser, ParsedCommand } from './presentation/cli/CommandDispatcher'
export { CLI } from './presentation/cli/CLI'

// Container
export { Container, getContainer, initContainer } from './container'
export type { ContainerOptions } from './container'

// App
export { OpsMaintenanceApp, AppConfig, main } from './index'

// Legacy
export { LegacyAdapter, getLegacyAdapter, initLegacyAdapter } from './presentation/LegacyAdapter'
export type { LegacyAdapterConfig } from './presentation/LegacyAdapter'

// 向后兼容（旧版 API）
export * from './legacy'