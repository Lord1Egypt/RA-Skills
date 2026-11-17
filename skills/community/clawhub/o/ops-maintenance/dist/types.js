"use strict";
/**
 * 类型定义统一导出
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.ConfigValidationError = exports.ServerHealth = exports.Server = void 0;
class Server {
    constructor(id, host, port, user, name, tags = []) {
        this.id = id;
        this.host = host;
        this.port = port;
        this.user = user;
        this.name = name;
        this.tags = tags;
    }
    static fromSSHConfig(config, idx) {
        const id = `${config.host}:${config.port || 22}:${config.user || 'root'}`;
        return new Server(id, config.host, config.port || 22, config.user || 'root', config.name || `server-${idx || config.host.replace(/\./g, '-')}`, config.tags || []);
    }
    getKey() {
        return `${this.host}:${this.port}:${this.user}`;
    }
    hasTag(tag) {
        return this.tags.includes(tag);
    }
    getDisplayName() {
        return this.name || this.host;
    }
}
exports.Server = Server;
class ServerHealth {
    constructor(server, status, metrics, services, checkedAt = new Date(), error) {
        this.server = server;
        this.status = status;
        this.metrics = metrics;
        this.services = services;
        this.checkedAt = checkedAt;
        this.error = error;
    }
    static healthy(server, metrics, services) {
        return new ServerHealth(server, ServerStatus.HEALTHY, metrics, services);
    }
    static warning(server, metrics, services, reason) {
        return new ServerHealth(server, ServerStatus.WARNING, metrics, services, new Date(), reason);
    }
    static offline(server, error) {
        return new ServerHealth(server, ServerStatus.OFFLINE, undefined, undefined, new Date(), error);
    }
    getDiskUsagePercent() {
        return this.metrics?.disk.usagePercent || 0;
    }
    getMemoryUsagePercent() {
        if (!this.metrics)
            return 0;
        const { total, used } = this.metrics.memory;
        return Math.round((used / total) * 100);
    }
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
class ConfigValidationError extends Error {
    constructor(message, field, value) {
        super(message);
        this.field = field;
        this.value = value;
        this.name = 'ConfigValidationError';
    }
}
exports.ConfigValidationError = ConfigValidationError;
//# sourceMappingURL=types.js.map