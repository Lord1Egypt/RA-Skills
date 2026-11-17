"use strict";
/**
 * 配置层类型定义
 * 定义所有核心数据模型和验证 Schema
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.ConfigValidationError = exports.ServerHealth = exports.Server = exports.ServerStatus = void 0;
/**
 * 服务器状态枚举
 */
var ServerStatus;
(function (ServerStatus) {
    ServerStatus["HEALTHY"] = "healthy";
    ServerStatus["WARNING"] = "warning";
    ServerStatus["OFFLINE"] = "offline";
    ServerStatus["UNKNOWN"] = "unknown";
})(ServerStatus || (exports.ServerStatus = ServerStatus = {}));
/**
 * 服务器实体（领域层核心对象）
 */
class Server {
    constructor(id, host, port, user, name, tags = []) {
        this.id = id;
        this.host = host;
        this.port = port;
        this.user = user;
        this.name = name;
        this.tags = tags;
    }
    /**
     * 从 SSHConfig 创建 Server
     */
    static fromSSHConfig(config, idx) {
        const id = `${config.host}:${config.port || 22}:${config.user || 'root'}`;
        return new Server(id, config.host, config.port || 22, config.user || 'root', config.name || `server-${idx || config.host.replace(/\./g, '-')}`, config.tags || []);
    }
    /**
     * 生成唯一标识
     */
    getKey() {
        return `${this.host}:${this.port}:${this.user}`;
    }
    /**
     * 是否匹配标签
     */
    hasTag(tag) {
        return this.tags.includes(tag);
    }
    /**
     * 显示名称
     */
    getDisplayName() {
        return this.name || this.host;
    }
}
exports.Server = Server;
/**
 * 服务器健康检查结果
 */
class ServerHealth {
    constructor(server, status, metrics, services, checkedAt = new Date(), error) {
        this.server = server;
        this.status = status;
        this.metrics = metrics;
        this.services = services;
        this.checkedAt = checkedAt;
        this.error = error;
    }
    /**
     * 从检查结果创建
     */
    static healthy(server, metrics, services) {
        return new ServerHealth(server, ServerStatus.HEALTHY, metrics, services);
    }
    static warning(server, metrics, services, reason) {
        return new ServerHealth(server, ServerStatus.WARNING, metrics, services, new Date(), reason);
    }
    static offline(server, error) {
        return new ServerHealth(server, ServerStatus.OFFLINE, undefined, undefined, new Date(), error);
    }
    /**
     * 磁盘使用率（0-100）
     */
    getDiskUsagePercent() {
        return this.metrics?.disk.usagePercent || 0;
    }
    /**
     * 内存使用率（0-100）
     */
    getMemoryUsagePercent() {
        if (!this.metrics)
            return 0;
        const { total, used } = this.metrics.memory;
        return Math.round((used / total) * 100);
    }
    /**
     * Swap 使用率（0-100）
     */
    getSwapUsagePercent() {
        if (!this.metrics)
            return 0;
        const { swapTotal, swapUsed } = this.metrics.memory;
        if (swapTotal === 0)
            return 0;
        return Math.round((swapUsed / swapTotal) * 100);
    }
}
exports.ServerHealth = ServerHealth;
/**
 * 配置验证错误
 */
class ConfigValidationError extends Error {
    constructor(message, field, value) {
        super(message);
        this.field = field;
        this.value = value;
        this.name = 'ConfigValidationError';
    }
}
exports.ConfigValidationError = ConfigValidationError;
//# sourceMappingURL=schemas.js.map