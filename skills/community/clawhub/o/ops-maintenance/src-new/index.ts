// 重新导出旧版兼容 API（保持向后兼容）
export * from './legacy'

// 导出新架构类型和类
export type {
  Server,
  SSHConfig,
  SSHConfig,
  ServerStatus,
  HealthMetrics,
  ServiceStatus,
  ServerHealth,
  ClusterHealthReport,
  PasswordUserInfo,
  ThresholdConfig
} from './config/schemas'

export {
  Server,
  ServerStatus
} from './config/schemas'

export { Container } from './container'
export { OpsMaintenanceApp } from './index'
export { LegacyAdapter, initLegacyAdapter } from './presentation/LegacyAdapter'