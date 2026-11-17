"use strict";
/**
 * 公共类型和常量
 * 所有模块导入此文件，避免循环依赖
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.ENV_THRESHOLDS = exports.DEFAULT_THRESHOLDS = exports.ServerHealth = exports.Server = exports.ServerStatus = void 0;
var ServerStatus;
(function (ServerStatus) {
    ServerStatus["HEALTHY"] = "healthy";
    ServerStatus["WARNING"] = "warning";
    ServerStatus["OFFLINE"] = "offline";
    ServerStatus["UNKNOWN"] = "unknown";
})(ServerStatus || (exports.ServerStatus = ServerStatus = {}));
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
    getKey() { return `${this.host}:${this.port}:${this.user}`; }
    hasTag(tag) { return this.tags.includes(tag); }
    getDisplayName() { return this.name || this.host; }
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
    getDiskUsagePercent() { return this.metrics?.disk.usagePercent || 0; }
    getMemoryUsagePercent() {
        if (!this.metrics)
            return 0;
        return Math.round((this.metrics.memory.used / this.metrics.memory.total) * 100);
    }
    getSwapUsagePercent() {
        if (!this.metrics)
            return 0;
        const { swapTotal, swapUsed } = this.metrics.memory;
        return swapTotal === 0 ? 0 : Math.round((swapUsed / swapTotal) * 100);
    }
}
exports.ServerHealth = ServerHealth;
// ============ 常量和默认值 ============
exports.DEFAULT_THRESHOLDS = {
    diskWarning: 80, diskCritical: 90,
    memoryWarning: 80, memoryCritical: 90,
    swapWarning: 70, swapCritical: 90,
    loadWarningMultiplier: 1.0, loadCriticalMultiplier: 2.0
};
exports.ENV_THRESHOLDS = {
    production: { ...exports.DEFAULT_THRESHOLDS, diskWarning: 75, diskCritical: 85, memoryWarning: 75, memoryCritical: 85 },
    staging: { ...exports.DEFAULT_THRESHOLDS, diskWarning: 85, diskCritical: 95, memoryWarning: 85, memoryCritical: 95 },
    development: exports.DEFAULT_THRESHOLDS
};
//# sourceMappingURL=common.js.map