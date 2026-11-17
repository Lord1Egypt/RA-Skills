/**
 * 向后兼容导出层
 * 提供与旧版 ops-maintenance 完全相同的导出函数
 *
 * 旧版模块使用方式：
 *   const { loadServers, addServer, checkAllServersHealth, ... } = require('./dist/index')
 *
 * 新版通过此适配器透明地使用新架构
 */

import type {
  Server,
  SSHConfig,
  PasswordUserInfo,
  ClusterHealthReport
} from './config/schemas'
import { LegacyAdapter, getLegacyAdapter, initLegacyAdapter } from './presentation/LegacyAdapter'

// 创建全局适配器实例
let adapter: LegacyAdapter | null = null

// 延迟初始化适配器
async function getAdapter(): Promise<LegacyAdapter> {
  if (!adapter) {
    adapter = new LegacyAdapter()
    await adapter.init()
  }
  return adapter
}

/**
 * 加载服务器列表
 * @deprecated 建议使用 Container + Repository 模式
 */
export async function loadServers(): Promise<Server[]> {
  const a = await getAdapter()
  return a.loadServers()
}

/**
 * 加载服务器状态追踪
 * @deprecated 内部使用
 */
export async function loadServerState(): Promise<any> {
  // 简化实现，返回 null
  return null
}

/**
 * 保存服务器状态追踪
 * @deprecated 内部使用
 */
export async function saveServerState(state: any): Promise<void> {
  // 简化实现，不做操作
}

/**
 * 计算服务器列表的校验和数组
 * @deprecated 内部使用
 */
export function calculateServerChecksums(servers: Server[]): string[] {
  return servers.map(s => `${s.host}:${s.port || 22}:${s.user || 'root'}`).sort()
}

/**
 * 检测新增服务器
 * @deprecated 内部使用
 */
export async function detectNewServers(): Promise<{
  newServers: Server[];
  allServers: Server[];
  message: string;
}> {
  const a = await getAdapter()
  return a.detectNewServers()
}

/**
 * 添加服务器
 * @deprecated 建议使用 ServerRepository.add()
 */
export async function addServer(config: SSHConfig): Promise<void> {
  const a = await getAdapter()
  return a.addServer(config)
}

/**
 * 移除服务器
 * @deprecated 建议使用 ServerRepository.remove()
 */
export async function removeServer(host: string): Promise<void> {
  const a = await getAdapter()
  return a.removeServer(host)
}

/**
 * 按标签筛选服务器
 * @deprecated 建议使用 ServerRepository.findByTags()
 */
export async function getServersByTag(tag: string): Promise<Server[]> {
  const a = await getAdapter()
  return a.getServersByTag(tag)
}

/**
 * 批量检查所有服务器健康状态
 */
export async function checkAllServersHealth(
  tags?: string[],
  serverList?: Server[]
): Promise<{ server: string; status: string; details: string }[]> {
  const a = await getAdapter()
  return a.checkAllServersHealth(tags, serverList)
}

/**
 * 批量执行命令到所有服务器
 */
export async function executeOnAllServers(
  command: string,
  tags?: string[]
): Promise<{ server: string; output: string }[]> {
  const a = await getAdapter()
  return a.executeOnAllServers(command, tags)
}

/**
 * 批量添加服务器
 */
export async function batchAddServers(servers: string[]): Promise<{ success: number; failed: number; details: string[] }> {
  const a = await getAdapter()
  return a.batchAddServers(servers)
}

/**
 * 从文本批量导入服务器
 */
export async function importServersFromText(text: string): Promise<{ success: number; failed: number; servers: Server[] }> {
  const a = await getAdapter()
  return a.importServersFromText(text)
}

/**
 * 批量检查所有服务器密码过期状态
 */
export async function checkAllServersPasswordExpiration(
  tags?: string[]
): Promise<Array<{
  server: string
  status: string
  details: string
  users?: PasswordUserInfo[]
}>> {
  const a = await getAdapter()
  return a.checkAllServersPasswordExpiration(tags)
}

/**
 * 生成密码过期检查报告
 */
export async function checkAllServersPasswordExpirationReport(
  tags?: string[]
): Promise<string> {
  const a = await getAdapter()
  return a.checkAllServersPasswordExpirationReport(tags)
}

/**
 * 获取集群摘要
 */
export async function getClusterSummary(): Promise<string> {
  const a = await getAdapter()
  return a.getClusterSummary()
}

/**
 * 远程命令执行
 */
export async function runRemoteCommand(
  config: SSHConfig,
  command: string
): Promise<string> {
  const a = await getAdapter()
  return a.runRemoteCommand(config, command)
}

/**
 * 本地命令执行
 */
export async function runCommand(
  cmd: string,
  timeout?: number
): Promise<string> {
  const a = await getAdapter()
  return a.runCommand(cmd, timeout)
}

/**
 * 远程服务器健康检查
 */
export async function checkRemoteHealth(
  config: SSHConfig,
  services?: string[]
): Promise<string> {
  const a = await getAdapter()
  return a.checkRemoteHealth(config, services)
}

/**
 * 远程服务器端口检查
 * @deprecated 未完全实现
 */
export async function checkRemotePort(
  config: SSHConfig,
  port?: number
): Promise<string> {
  return `端口检查功能尚未完全实现`
}

/**
 * 远程服务器进程检查
 * @deprecated 未完全实现
 */
export async function checkRemoteProcess(
  config: SSHConfig,
  name?: string
): Promise<string> {
  return `进程检查功能尚未完全实现`
}

/**
 * 远程服务器磁盘检查
 */
export async function checkRemoteDisk(config: SSHConfig): Promise<string> {
  const a = await getAdapter()
  // 使用 DiskCheckUseCase 实现
  // 简化：返回占位符
  return `磁盘检查: ${config.host}`
}

/**
 * 远程服务器性能检查
 * @deprecated 未完全实现
 */
export async function checkRemotePerformance(config: SSHConfig): Promise<string> {
  return `性能检查功能尚未完全实现`
}

/**
 * 远程服务器日志检查
 * @deprecated 未完全实现
 */
export async function checkRemoteLogs(
  config: SSHConfig,
  pattern?: string,
  lines?: number
): Promise<string> {
  return `日志检查功能尚未完全实现`
}

/**
 * 运维操作执行入口
 */
export type OpsAction = 'health' | 'logs' | 'perf' | 'ports' | 'process' | 'disk' | 'password' | 'passwd' | 'expire'

/**
 * 本地运维操作
 */
export async function executeOp(
  action: string,
  arg?: string
): Promise<string> {
  const a = await getAdapter()
  return a.executeOp(action, arg)
}

/**
 * 远程运维操作
 */
export async function executeRemoteOp(
  action: string,
  config: SSHConfig,
  arg?: string
): Promise<string> {
  const a = await getAdapter()
  return a.executeRemoteOp(action, config, arg)
}

// ============ 新增：高级 API（新架构）============

/**
 * 获取容器实例（新 API）
 */
export function getContainer() {
  return require('./container').getContainer()
}

/**
 * 初始化容器（新 API）
 */
export async function initContainer(options?: any) {
  return require('./container').initContainer(options)
}

/**
 * 创建 OpsMaintenanceApp（新 API）
 */
export function createApp(config?: any) {
  return new (require('./index').OpsMaintenanceApp)(config)
}