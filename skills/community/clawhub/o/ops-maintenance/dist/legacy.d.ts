/**
 * 向后兼容导出层
 * 提供与旧版 ops-maintenance 完全相同的导出函数
 *
 * 旧版模块使用方式：
 *   const { loadServers, addServer, checkAllServersHealth, ... } = require('./dist/index')
 *
 * 新版通过此适配器透明地使用新架构
 */
import type { Server, SSHConfig, PasswordUserInfo } from './config/schemas';
/**
 * 加载服务器列表
 * @deprecated 建议使用 Container + Repository 模式
 */
export declare function loadServers(): Promise<Server[]>;
/**
 * 加载服务器状态追踪
 * @deprecated 内部使用
 */
export declare function loadServerState(): Promise<any>;
/**
 * 保存服务器状态追踪
 * @deprecated 内部使用
 */
export declare function saveServerState(state: any): Promise<void>;
/**
 * 计算服务器列表的校验和数组
 * @deprecated 内部使用
 */
export declare function calculateServerChecksums(servers: Server[]): string[];
/**
 * 检测新增服务器
 * @deprecated 内部使用
 */
export declare function detectNewServers(): Promise<{
    newServers: Server[];
    allServers: Server[];
    message: string;
}>;
/**
 * 添加服务器
 * @deprecated 建议使用 ServerRepository.add()
 */
export declare function addServer(config: SSHConfig): Promise<void>;
/**
 * 移除服务器
 * @deprecated 建议使用 ServerRepository.remove()
 */
export declare function removeServer(host: string): Promise<void>;
/**
 * 按标签筛选服务器
 * @deprecated 建议使用 ServerRepository.findByTags()
 */
export declare function getServersByTag(tag: string): Promise<Server[]>;
/**
 * 批量检查所有服务器健康状态
 */
export declare function checkAllServersHealth(tags?: string[], serverList?: Server[]): Promise<{
    server: string;
    status: string;
    details: string;
}[]>;
/**
 * 批量执行命令到所有服务器
 */
export declare function executeOnAllServers(command: string, tags?: string[]): Promise<{
    server: string;
    output: string;
}[]>;
/**
 * 批量添加服务器
 */
export declare function batchAddServers(servers: string[]): Promise<{
    success: number;
    failed: number;
    details: string[];
}>;
/**
 * 从文本批量导入服务器
 */
export declare function importServersFromText(text: string): Promise<{
    success: number;
    failed: number;
    servers: Server[];
}>;
/**
 * 批量检查所有服务器密码过期状态
 */
export declare function checkAllServersPasswordExpiration(tags?: string[]): Promise<Array<{
    server: string;
    status: string;
    details: string;
    users?: PasswordUserInfo[];
}>>;
/**
 * 生成密码过期检查报告
 */
export declare function checkAllServersPasswordExpirationReport(tags?: string[]): Promise<string>;
/**
 * 获取集群摘要
 */
export declare function getClusterSummary(): Promise<string>;
/**
 * 远程命令执行
 */
export declare function runRemoteCommand(config: SSHConfig, command: string): Promise<string>;
/**
 * 本地命令执行
 */
export declare function runCommand(cmd: string, timeout?: number): Promise<string>;
/**
 * 远程服务器健康检查
 */
export declare function checkRemoteHealth(config: SSHConfig, services?: string[]): Promise<string>;
/**
 * 远程服务器端口检查
 * @deprecated 未完全实现
 */
export declare function checkRemotePort(config: SSHConfig, port?: number): Promise<string>;
/**
 * 远程服务器进程检查
 * @deprecated 未完全实现
 */
export declare function checkRemoteProcess(config: SSHConfig, name?: string): Promise<string>;
/**
 * 远程服务器磁盘检查
 */
export declare function checkRemoteDisk(config: SSHConfig): Promise<string>;
/**
 * 远程服务器性能检查
 * @deprecated 未完全实现
 */
export declare function checkRemotePerformance(config: SSHConfig): Promise<string>;
/**
 * 远程服务器日志检查
 * @deprecated 未完全实现
 */
export declare function checkRemoteLogs(config: SSHConfig, pattern?: string, lines?: number): Promise<string>;
/**
 * 运维操作执行入口
 */
export type OpsAction = 'health' | 'logs' | 'perf' | 'ports' | 'process' | 'disk' | 'password' | 'passwd' | 'expire';
/**
 * 本地运维操作
 */
export declare function executeOp(action: string, arg?: string): Promise<string>;
/**
 * 远程运维操作
 */
export declare function executeRemoteOp(action: string, config: SSHConfig, arg?: string): Promise<string>;
/**
 * 获取容器实例（新 API）
 */
export declare function getContainer(): any;
/**
 * 初始化容器（新 API）
 */
export declare function initContainer(options?: any): Promise<any>;
/**
 * 创建 OpsMaintenanceApp（新 API）
 */
export declare function createApp(config?: any): any;
//# sourceMappingURL=legacy.d.ts.map