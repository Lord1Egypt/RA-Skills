/**
 * 配置层类型定义
 * 定义所有核心数据模型和验证 Schema
 */
/**
 * SSH 配置
 */
export interface SSHConfig {
    /** 主机地址（IP或域名） */
    host: string;
    /** SSH 端口，默认 22 */
    port?: number;
    /** 用户名，默认 root */
    user?: string;
    /** 密码认证（可选，如果未提供则使用密钥） */
    password?: string;
    /** 密钥文件路径 */
    keyFile?: string;
    /** 友好名称，用于显示 */
    name?: string;
    /** 标签/分组，用于筛选 */
    tags?: string[];
}
/**
 * 服务器状态枚举
 */
export declare enum ServerStatus {
    HEALTHY = "healthy",
    WARNING = "warning",
    OFFLINE = "offline",
    UNKNOWN = "unknown"
}
/**
 * 服务器实体（领域层核心对象）
 */
export declare class Server {
    readonly id: string;
    readonly host: string;
    readonly port: number;
    readonly user: string;
    readonly name?: string | undefined;
    readonly tags: string[];
    constructor(id: string, host: string, port: number, user: string, name?: string | undefined, tags?: string[]);
    /**
     * 从 SSHConfig 创建 Server
     */
    static fromSSHConfig(config: SSHConfig, idx?: number): Server;
    /**
     * 生成唯一标识
     */
    getKey(): string;
    /**
     * 是否匹配标签
     */
    hasTag(tag: string): boolean;
    /**
     * 显示名称
     */
    getDisplayName(): string;
}
/**
 * 健康状态详细指标
 */
export interface HealthMetrics {
    /** 系统运行时间（如 "34 days, 16:44"） */
    uptime: string;
    /** 负载平均值 [1分钟, 5分钟, 15分钟] */
    loadAverage: [number, number, number];
    /** 内存统计（字节） */
    memory: {
        total: number;
        used: number;
        free: number;
        available: number;
        swapTotal: number;
        swapUsed: number;
    };
    /** 磁盘使用统计 */
    disk: {
        mountPoint: string;
        total: number;
        used: number;
        available: number;
        usagePercent: number;
    };
}
/**
 * 服务状态
 */
export interface ServiceStatus {
    name: string;
    running: boolean;
    pid?: number;
}
/**
 * 服务器健康检查结果
 */
export declare class ServerHealth {
    readonly server: Server;
    readonly status: ServerStatus;
    readonly metrics?: HealthMetrics | undefined;
    readonly services?: ServiceStatus[] | undefined;
    readonly checkedAt: Date;
    readonly error?: string | undefined;
    constructor(server: Server, status: ServerStatus, metrics?: HealthMetrics | undefined, services?: ServiceStatus[] | undefined, checkedAt?: Date, error?: string | undefined);
    /**
     * 从检查结果创建
     */
    static healthy(server: Server, metrics: HealthMetrics, services: ServiceStatus[]): ServerHealth;
    static warning(server: Server, metrics: HealthMetrics, services: ServiceStatus[], reason?: string): ServerHealth;
    static offline(server: Server, error: string): ServerHealth;
    /**
     * 磁盘使用率（0-100）
     */
    getDiskUsagePercent(): number;
    /**
     * 内存使用率（0-100）
     */
    getMemoryUsagePercent(): number;
    /**
     * Swap 使用率（0-100）
     */
    getSwapUsagePercent(): number;
}
/**
 * 集群健康报告
 */
export interface ClusterHealthReport {
    totalServers: number;
    healthy: number;
    warning: number;
    offline: number;
    serverHealth: ServerHealth[];
    generatedAt: Date;
}
/**
 * 配置验证错误
 */
export declare class ConfigValidationError extends Error {
    readonly field?: string | undefined;
    readonly value?: any | undefined;
    constructor(message: string, field?: string | undefined, value?: any | undefined);
}
/**
 * 配置管理器选项
 */
export interface ConfigManagerOptions {
    /** 配置文件路径 */
    configPath?: string;
    /** 是否启用热重载 */
    watch?: boolean;
    /** 配置文件修改轮询间隔（ms） */
    pollInterval?: number;
}
/**
 * 服务器仓库接口（领域层）
 */
export interface IServerRepository {
    /** 获取所有服务器 */
    findAll(): Promise<Server[]>;
    /** 按标签查找 */
    findByTags(tags: string[]): Promise<Server[]>;
    /** 按 ID 查找 */
    findById(id: string): Promise<Server | null>;
    /** 添加服务器 */
    add(server: Server): Promise<void>;
    /** 更新服务器 */
    update(server: Server): Promise<void>;
    /** 删除服务器 */
    remove(host: string): Promise<void>;
    /** 监听配置变更 */
    onChange?(callback: () => void): void;
}
/**
 * 缓存仓库接口
 */
export interface ICacheRepository {
    /** 获取缓存 */
    get<T>(key: string): Promise<T | null>;
    /** 设置缓存 */
    set<T>(key: string, value: T, ttlSeconds?: number): Promise<void>;
    /** 删除缓存 */
    delete(key: string): Promise<void>;
    /** 清空所有缓存 */
    clear(): Promise<void>;
}
/**
 * SSH 凭据
 */
export interface SSHCredentials {
    /** 密码（如果使用密码认证） */
    password?: string;
    /** 密钥文件路径（如果使用密钥认证） */
    keyFile?: string;
    /** 私钥内容（可选，直接提供密钥内容） */
    keyContent?: string;
}
/**
 * 凭据提供者接口
 */
export interface ICredentialsProvider {
    /**
     * 获取服务器的 SSH 凭据
     */
    getCredentials(server: Server): Promise<SSHCredentials | null>;
    /**
     * 更新或存储服务器的凭据
     */
    setCredentials(server: Server, credentials: SSHCredentials): Promise<void>;
}
/**
 * SSH 客户端接口
 */
export interface ISSHClient {
    /** 执行远程命令 */
    execute(server: Server, command: string, timeout?: number): Promise<string>;
    /** 测试连接 */
    testConnection(server: Server): Promise<boolean>;
    /** 关闭连接 */
    disconnect(server: Server): Promise<void>;
    /** 设置凭据提供者 */
    setCredentialsProvider(provider: ICredentialsProvider): void;
}
/**
 * 健康检查策略接口
 */
export interface IHealthCheckStrategy {
    /** 策略名称 */
    name: string;
    /** 优先级（数字越小优先级越高） */
    priority: number;
    /** 执行检查 */
    check(server: Server): Promise<HealthMetrics>;
    /** 是否关键指标（影响总体健康状态） */
    isCritical(): boolean;
}
/**
 * 格式化器接口
 */
export interface IReportFormatter {
    /** 格式化集群报告 */
    formatClusterReport(report: ClusterHealthReport): string;
    /** 格式化单服务器报告 */
    formatServerHealth(health: ServerHealth): string;
    /** 格式化密码过期报告 */
    formatPasswordReport(data: any): string;
}
/**
 * 通知器接口
 */
export interface INotifier {
    /** 发送通知 */
    notify(title: string, message: string, level: 'info' | 'warning' | 'critical'): Promise<void>;
}
/**
 * 邮件通知配置
 */
export interface EmailConfig {
    host: string;
    port: number;
    user: string;
    password: string;
    from: string;
    to: string[];
    ssl?: boolean;
    alertOnly?: boolean;
}
//# sourceMappingURL=schemas.d.ts.map