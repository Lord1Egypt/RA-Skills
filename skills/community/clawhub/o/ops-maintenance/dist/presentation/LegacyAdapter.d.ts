/**
 * 向后兼容适配器
 * 将旧版 API 调用转换为新版架构
 */
import type { Server, SSHConfig, PasswordUserInfo } from '../config/schemas';
/**
 * 适配器配置
 */
export interface LegacyAdapterConfig {
    configPath?: string;
    useConnectionPool?: boolean;
    cacheTTL?: number;
    environment?: string;
}
/**
 * 向后兼容适配器
 * 提供与旧版完全相同的导出函数签名
 */
export declare class LegacyAdapter {
    private config?;
    private container?;
    private serverRepo?;
    private sshClient?;
    private cache?;
    private initialized;
    constructor(config?: LegacyAdapterConfig | undefined);
    /**
     * 初始化适配器
     */
    init(): Promise<void>;
    /**
     * 确保已初始化
     */
    private ensureInitialized;
    loadServers(): Promise<Server[]>;
    loadServerState(): Promise<any>;
    saveServerState(state: any): Promise<void>;
    calculateServerChecksums(servers: Server[]): string[];
    detectNewServers(): Promise<{
        newServers: Server[];
        allServers: Server[];
        message: string;
    }>;
    addServer(config: SSHConfig): Promise<void>;
    removeServer(host: string): Promise<void>;
    getServersByTag(tag: string): Promise<Server[]>;
    batchAddServers(servers: string[]): Promise<{
        success: number;
        failed: number;
        details: string[];
    }>;
    importServersFromText(text: string): Promise<{
        success: number;
        failed: number;
        servers: Server[];
    }>;
    private parseServerString;
    checkAllServersHealth(tags?: string[], serverList?: Server[]): Promise<{
        server: string;
        status: string;
        details: string;
    }[]>;
    private formatStatus;
    private formatDetails;
    checkRemoteHealth(config: SSHConfig, services?: string[]): Promise<string>;
    checkAllServersPasswordExpiration(tags?: string[]): Promise<Array<{
        server: string;
        status: string;
        details: string;
        users?: PasswordUserInfo[];
    }>>;
    checkAllServersPasswordExpirationReport(tags?: string[]): Promise<string>;
    getClusterSummary(): Promise<string>;
    runRemoteCommand(config: SSHConfig, command: string): Promise<string>;
    runCommand(cmd: string, timeout?: number): Promise<string>;
    executeOnAllServers(command: string, tags?: string[]): Promise<{
        server: string;
        output: string;
    }[]>;
    checkRemotePort(config: SSHConfig, port?: number): Promise<string>;
    checkRemoteProcess(config: SSHConfig, name?: string): Promise<string>;
    checkRemoteDisk(config: SSHConfig): Promise<string>;
    checkRemotePerformance(config: SSHConfig): Promise<string>;
    checkRemoteLogs(config: SSHConfig, pattern?: string, lines?: number): Promise<string>;
    executeOp(action: string, arg?: string): Promise<string>;
    executeRemoteOp(action: string, config: SSHConfig, arg?: string): Promise<string>;
    shutdown(): Promise<void>;
}
/**
 * 获取全局适配器
 */
export declare function getLegacyAdapter(config?: LegacyAdapterConfig): LegacyAdapter;
/**
 * 初始化全局适配器
 */
export declare function initLegacyAdapter(config?: LegacyAdapterConfig): Promise<LegacyAdapter>;
//# sourceMappingURL=LegacyAdapter.d.ts.map