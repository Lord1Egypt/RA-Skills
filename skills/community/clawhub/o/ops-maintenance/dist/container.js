"use strict";
/**
 * 依赖注入容器
 * 管理所有核心组件的生命周期和依赖关系
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.Container = void 0;
exports.getContainer = getContainer;
exports.initContainer = initContainer;
const ServerFileRepository_1 = require("./infrastructure/repositories/ServerFileRepository");
const SSHClient_1 = require("./infrastructure/ssh/SSHClient");
const ConnectionPool_1 = require("./infrastructure/ssh/ConnectionPool");
const CacheRepository_1 = require("./infrastructure/cache/CacheRepository");
const HealthChecker_1 = require("./infrastructure/monitoring/HealthChecker");
const ThresholdChecker_1 = require("./infrastructure/monitoring/ThresholdChecker");
const HealthCheckUseCase_1 = require("./core/usecases/HealthCheckUseCase");
const PasswordCheckUseCase_1 = require("./core/usecases/PasswordCheckUseCase");
const DiskCheckUseCase_1 = require("./core/usecases/DiskCheckUseCase");
const CLI_1 = require("./presentation/cli/CLI");
const CredentialsRepository_1 = require("./infrastructure/repositories/CredentialsRepository");
const loader_1 = require("./config/loader");
const EmailNotifier_1 = require("./infrastructure/notifiers/EmailNotifier");
/**
 * 依赖注入容器
 */
class Container {
    constructor(options = {}) {
        this.initialized = false;
        this.options = {
            configPath: options.configPath,
            useConnectionPool: options.useConnectionPool ?? true,
            cacheTTL: options.cacheTTL ?? 30,
            logLevel: options.logLevel ?? (process.env.NODE_ENV === 'production' ? 'info' : 'debug'),
            environment: options.environment ?? 'production',
            email: options.email
        };
    }
    /**
     * 初始化容器
     */
    async init() {
        if (this.initialized)
            return;
        // 1. 初始化日志
        // Logger.setLevel(this.options.logLevel) // TODO
        // 2. 初始化缓存
        this.cache = new CacheRepository_1.MemoryCache(this.options.cacheTTL);
        // 3. 初始化 ConfigManager（作为配置和凭据来源）
        this.configManager = new loader_1.ConfigManager({ configPath: this.options.configPath });
        await this.configManager.start();
        // 4. 初始化服务器仓库（基于 ConfigManager）
        this.serverRepository = new ServerFileRepository_1.ServerFileRepository(undefined, this.configManager);
        await this.serverRepository.init();
        // 5. 初始化凭据提供者
        this.credentialsProvider = new CredentialsRepository_1.ConfigManagerCredentialsProvider(this.configManager);
        // 6. 初始化 SSH 客户端
        this.sshClient = new SSHClient_1.SSHClient();
        this.sshClient.setCredentialsProvider(this.credentialsProvider);
        // 7. 初始化连接池
        if (this.options.useConnectionPool) {
            this.connectionPool = new ConnectionPool_1.ConnectionPool(this.sshClient);
            this.connectionPool.start();
        }
        // 8. 初始化监控组件
        this.healthChecker = new HealthChecker_1.HealthChecker();
        this.thresholdChecker = new ThresholdChecker_1.ThresholdChecker(undefined, this.options.environment);
        // 9. 初始化邮件通知器（如果有配置）
        if (this.options.email?.user && this.options.email?.password) {
            this.emailNotifier = new EmailNotifier_1.EmailNotifier(this.options.email);
            this.emailNotifier.init().catch(e => {
                console.warn('邮件初始化失败，告警功能不可用:', e.message);
            });
        }
        this.initialized = true;
    }
    /**
     * 获取服务器仓库
     */
    getServerRepository() {
        if (!this.serverRepository) {
            throw new Error('容器未初始化，请先调用 init()');
        }
        return this.serverRepository;
    }
    /**
     * 获取 SSH 客户端
     */
    getSSHClient() {
        if (!this.sshClient) {
            throw new Error('容器未初始化，请先调用 init()');
        }
        return this.sshClient;
    }
    /**
     * 获取缓存
     */
    getCache() {
        if (!this.cache) {
            throw new Error('容器未初始化，请先调用 init()');
        }
        return this.cache;
    }
    /**
     * 获取健康检查器
     */
    getHealthChecker() {
        if (!this.healthChecker) {
            throw new Error('容器未初始化');
        }
        return this.healthChecker;
    }
    /**
     * 获取阈值检查器
     */
    getThresholdChecker() {
        if (!this.thresholdChecker) {
            throw new Error('容器未初始化');
        }
        return this.thresholdChecker;
    }
    /**
     * 获取连接池
     */
    getConnectionPool() {
        return this.connectionPool;
    }
    /**
     * 创建 CLI 实例并注入依赖
     */
    createCLI() {
        const cli = new CLI_1.CLI();
        cli.setDependencies(this.getServerRepository(), this.getSSHClient(), this.getCache(), this.options.email);
        return cli;
    }
    /**
     * 获取 ConfigManager
     */
    getConfigManager() {
        if (!this.configManager) {
            throw new Error('容器未初始化');
        }
        return this.configManager;
    }
    /**
     * 创建健康检查用例
     */
    createHealthCheckUseCase() {
        return new HealthCheckUseCase_1.HealthCheckUseCase(this.getServerRepository(), this.getSSHClient(), this.getCache(), this.getHealthChecker(), this.getThresholdChecker());
    }
    /**
     * 创建密码检查用例
     */
    createPasswordCheckUseCase() {
        return new PasswordCheckUseCase_1.PasswordCheckUseCase(this.getServerRepository(), this.getSSHClient());
    }
    /**
     * 创建磁盘检查用例
     */
    createDiskCheckUseCase() {
        return new DiskCheckUseCase_1.DiskCheckUseCase(this.getServerRepository(), this.getSSHClient());
    }
    /**
     * 关闭容器（清理资源）
     */
    async shutdown() {
        if (this.connectionPool) {
            this.connectionPool.stop();
        }
        if (this.sshClient) {
            await this.sshClient.disconnectAll();
        }
        if (this.configManager) {
            this.configManager.stop();
        }
        this.initialized = false;
    }
}
exports.Container = Container;
/**
 * 全局容器实例
 */
let globalContainer = null;
/**
 * 获取全局容器
 */
function getContainer(options) {
    if (!globalContainer) {
        globalContainer = new Container(options);
    }
    return globalContainer;
}
/**
 * 初始化全局容器
 */
async function initContainer(options) {
    const container = getContainer(options);
    await container.init();
    return container;
}
//# sourceMappingURL=container.js.map