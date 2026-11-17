"use strict";
/**
 * 健康检查用例
 * 协调多个组件完成服务器健康检查
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.HealthCheckUseCase = void 0;
const HealthChecker_1 = require("../../infrastructure/monitoring/HealthChecker");
/**
 * 健康检查用例
 */
class HealthCheckUseCase {
    constructor(serverRepo, ssh, cache, healthChecker, thresholdChecker) {
        this.serverRepo = serverRepo;
        this.ssh = ssh;
        this.cache = cache;
        this.healthChecker = healthChecker;
        this.thresholdChecker = thresholdChecker;
    }
    /**
     * 执行健康检查
     */
    async execute(input = {}) {
        // 1. 获取目标服务器列表
        const targetServers = await this.resolveServers(input.tags, input.servers);
        // 2. 并发检查每台服务器
        const healthPromises = targetServers.map(server => this.checkSingleServer(server, input.services, input.force));
        const serverHealthList = await Promise.allSettled(healthPromises);
        // 3. 构建报告
        const serverHealth = serverHealthList
            .filter((result) => result.status === 'fulfilled')
            .map(result => result.value);
        const report = {
            totalServers: targetServers.length,
            healthy: serverHealth.filter(h => h.status === ServerStatus.HEALTHY).length,
            warning: serverHealth.filter(h => h.status === ServerStatus.WARNING).length,
            offline: serverHealth.filter(h => h.status === ServerStatus.OFFLINE).length,
            serverHealth,
            generatedAt: new Date()
        };
        return report;
    }
    /**
     * 检查单台服务器
     */
    async checkSingleServer(server, services, force = false) {
        const cacheKey = `health:${server.id}`;
        // 尝试从缓存获取（非强制刷新）
        if (!force) {
            const cached = await this.cache.get(cacheKey);
            if (cached && this.isCacheValid(cached)) {
                return cached;
            }
        }
        try {
            // 1. 测试连接
            const isConnected = await this.ssh.testConnection(server);
            if (!isConnected) {
                return ServerHealth.offline(server, 'SSH 连接失败');
            }
            // 2. 执行健康检查（收集指标）
            const metrics = await this.healthChecker.checkAll(server, this.ssh);
            // 3. 检查服务状态
            const serviceList = services ?? ['nginx', 'docker', 'postgresql', 'redis-server'];
            const serviceStatus = await (0, HealthChecker_1.checkServices)(server, this.ssh, serviceList);
            // 4. 阈值评估
            const { overallStatus } = this.thresholdChecker.check(server.name, metrics);
            // 5. 构建健康对象
            const health = ServerHealth.healthy(server, metrics, serviceStatus);
            // 缓存结果
            await this.cache.set(cacheKey, health, 30); // 缓存 30 秒
            return health;
        }
        catch (error) {
            return ServerHealth.offline(server, error.message);
        }
    }
    /**
     * 解析目标服务器列表
     */
    async resolveServers(tags, explicitServers) {
        if (explicitServers && explicitServers.length > 0) {
            return explicitServers;
        }
        if (tags && tags.length > 0) {
            return this.serverRepo.findByTags(tags);
        }
        return this.serverRepo.findAll();
    }
    /**
     * 检查缓存是否有效
     */
    isCacheValid(health) {
        const now = new Date();
        const checkedAt = health.checkedAt;
        const ageSeconds = (now.getTime() - checkedAt.getTime()) / 1000;
        // 缓存有效期为 30 秒
        return ageSeconds < 30;
    }
}
exports.HealthCheckUseCase = HealthCheckUseCase;
//# sourceMappingURL=HealthCheckUseCase.js.map