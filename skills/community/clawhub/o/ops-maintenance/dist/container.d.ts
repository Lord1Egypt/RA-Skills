/**
 * 依赖注入容器
 * 管理所有核心组件的生命周期和依赖关系
 */
import type { IServerRepository, ISSHClient, ICacheRepository, EmailConfig } from './config/schemas';
import { ConnectionPool } from './infrastructure/ssh/ConnectionPool';
import { HealthChecker } from './infrastructure/monitoring/HealthChecker';
import { ThresholdChecker } from './infrastructure/monitoring/ThresholdChecker';
import { HealthCheckUseCase } from './core/usecases/HealthCheckUseCase';
import { PasswordCheckUseCase } from './core/usecases/PasswordCheckUseCase';
import { DiskCheckUseCase } from './core/usecases/DiskCheckUseCase';
import { CLI } from './presentation/cli/CLI';
import { ConfigManager } from './config/loader';
/**
 * 容器配置选项
 */
export interface ContainerOptions {
    /** 配置文件路径 */
    configPath?: string;
    /** 是否启用连接池 */
    useConnectionPool?: boolean;
    /** 缓存 TTL（秒）*/
    cacheTTL?: number;
    /** 日志级别 */
    logLevel?: string;
    /** 环境 */
    environment?: string;
    /** 邮件通知配置 */
    email?: Partial<EmailConfig>;
}
/**
 * 依赖注入容器
 */
export declare class Container {
    private options;
    private initialized;
    private serverRepository?;
    private sshClient?;
    private connectionPool?;
    private cache?;
    private healthChecker?;
    private thresholdChecker?;
    private configManager?;
    private credentialsProvider?;
    private emailNotifier?;
    constructor(options?: ContainerOptions);
    /**
     * 初始化容器
     */
    init(): Promise<void>;
    /**
     * 获取服务器仓库
     */
    getServerRepository(): IServerRepository;
    /**
     * 获取 SSH 客户端
     */
    getSSHClient(): ISSHClient;
    /**
     * 获取缓存
     */
    getCache(): ICacheRepository;
    /**
     * 获取健康检查器
     */
    getHealthChecker(): HealthChecker;
    /**
     * 获取阈值检查器
     */
    getThresholdChecker(): ThresholdChecker;
    /**
     * 获取连接池
     */
    getConnectionPool(): ConnectionPool | undefined;
    /**
     * 创建 CLI 实例并注入依赖
     */
    createCLI(): CLI;
    /**
     * 获取 ConfigManager
     */
    getConfigManager(): ConfigManager;
    /**
     * 创建健康检查用例
     */
    createHealthCheckUseCase(): HealthCheckUseCase;
    /**
     * 创建密码检查用例
     */
    createPasswordCheckUseCase(): PasswordCheckUseCase;
    /**
     * 创建磁盘检查用例
     */
    createDiskCheckUseCase(): DiskCheckUseCase;
    /**
     * 关闭容器（清理资源）
     */
    shutdown(): Promise<void>;
}
/**
 * 获取全局容器
 */
export declare function getContainer(options?: ContainerOptions): Container;
/**
 * 初始化全局容器
 */
export declare function initContainer(options?: ContainerOptions): Promise<Container>;
//# sourceMappingURL=container.d.ts.map