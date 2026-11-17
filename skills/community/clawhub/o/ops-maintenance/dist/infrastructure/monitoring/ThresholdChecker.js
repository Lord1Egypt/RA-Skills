"use strict";
/**
 * 阈值检查器 - 简化版
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.ThresholdChecker = exports.ENV_THRESHOLDS = exports.DEFAULT_THRESHOLDS = void 0;
const schemas_1 = require("../config/schemas");
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
class ThresholdChecker {
    constructor(thresholds, environment = 'production') {
        const envConfig = exports.ENV_THRESHOLDS[environment] || exports.DEFAULT_THRESHOLDS;
        this.thresholds = { ...envConfig, ...thresholds };
        this.environment = environment;
    }
    check(serverName, metrics) {
        const checks = [];
        const diskPercent = metrics.disk.usagePercent;
        checks.push(this.checkThreshold('disk', diskPercent, this.thresholds.diskCritical, this.thresholds.diskWarning, `磁盘 ${diskPercent}%`));
        const memPercent = Math.round((metrics.memory.used / metrics.memory.total) * 100);
        checks.push(this.checkThreshold('memory', memPercent, this.thresholds.memoryCritical, this.thresholds.memoryWarning, `内存 ${memPercent}%`));
        if (metrics.memory.swapTotal > 0) {
            const swapPercent = Math.round((metrics.memory.swapUsed / metrics.memory.swapTotal) * 100);
            checks.push(this.checkThreshold('swap', swapPercent, this.thresholds.swapCritical, this.thresholds.swapWarning, `Swap ${swapPercent}%`));
        }
        const hasCritical = checks.some(c => c.status === 'critical');
        const hasWarning = checks.some(c => c.status === 'warning');
        const overallStatus = hasCritical ? schemas_1.ServerStatus.WARNING : hasWarning ? schemas_1.ServerStatus.WARNING : schemas_1.ServerStatus.HEALTHY;
        return { overallStatus, checks };
    }
    checkThreshold(metric, value, critical, warning, message) {
        if (value >= critical)
            return { metric, value, threshold: critical, status: 'critical', message: `🔴 ${message}` };
        if (value >= warning)
            return { metric, value, threshold: warning, status: 'warning', message: `🟡 ${message}` };
        return { metric, value, threshold: warning, status: 'ok', message: `✅ ${message}` };
    }
    getThresholds() { return { ...this.thresholds }; }
    setThresholds(thresholds) { this.thresholds = { ...this.thresholds, ...thresholds }; }
    setEnvironment(env) {
        const envConfig = exports.ENV_THRESHOLDS[env];
        if (envConfig) {
            this.thresholds = { ...envConfig };
            this.environment = env;
        }
    }
}
exports.ThresholdChecker = ThresholdChecker;
//# sourceMappingURL=ThresholdChecker.js.map