"use strict";
/**
 * 健康检查策略 - 简化版
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.HealthChecker = exports.DiskCheck = exports.MemoryCheck = exports.LoadAverageCheck = exports.BaseHealthCheckStrategy = void 0;
exports.checkServices = checkServices;
class BaseHealthCheckStrategy {
    async execute(server, ssh) {
        try {
            const metrics = await this.check(server, ssh);
            return { success: true, metrics };
        }
        catch (error) {
            return { success: false, error: error.message };
        }
    }
}
exports.BaseHealthCheckStrategy = BaseHealthCheckStrategy;
class LoadAverageCheck extends BaseHealthCheckStrategy {
    constructor() {
        super(...arguments);
        this.name = 'load_average';
        this.priority = 1;
    }
    isCritical() { return true; }
    async check(server, ssh) {
        const output = await ssh.execute(server, 'uptime');
        const match = output.match(/load average:\s+([\d.]+),\s+([\d.]+),\s+([\d.]+)/);
        if (!match)
            throw new Error('无法解析负载');
        return {
            uptime: output.match(/up\s+([^,]+),/)?.[1]?.trim() || 'N/A',
            loadAverage: [parseFloat(match[1]), parseFloat(match[2]), parseFloat(match[3])],
            memory: { total: 0, used: 0, free: 0, available: 0, swapTotal: 0, swapUsed: 0 },
            disk: { mountPoint: '/', total: 0, used: 0, available: 0, usagePercent: 0 }
        };
    }
}
exports.LoadAverageCheck = LoadAverageCheck;
class MemoryCheck extends BaseHealthCheckStrategy {
    constructor() {
        super(...arguments);
        this.name = 'memory_usage';
        this.priority = 2;
    }
    isCritical() { return true; }
    async check(server, ssh) {
        const output = await ssh.execute(server, 'free -k 2>/dev/null || free 2>/dev/null');
        const memLine = output.split('\n').find(l => l.startsWith('Mem:'));
        if (!memLine)
            throw new Error('无法解析内存');
        const parts = memLine.trim().split(/\s+/);
        const total = parseInt(parts[1]);
        const used = parseInt(parts[2]);
        const free = parseInt(parts[3]);
        const available = parseInt(parts[6] || parts[4]);
        const swapLine = output.split('\n').find(l => l.startsWith('Swap:'));
        let swapTotal = 0, swapUsed = 0;
        if (swapLine) {
            const sw = swapLine.trim().split(/\s+/);
            swapTotal = parseInt(sw[1]);
            swapUsed = parseInt(sw[2]);
        }
        return {
            uptime: 'N/A',
            loadAverage: [0, 0, 0],
            memory: { total, used, free, available, swapTotal, swapUsed },
            disk: { mountPoint: '/', total: 0, used: 0, available: 0, usagePercent: 0 }
        };
    }
}
exports.MemoryCheck = MemoryCheck;
class DiskCheck extends BaseHealthCheckStrategy {
    constructor() {
        super(...arguments);
        this.name = 'disk_usage';
        this.priority = 3;
    }
    isCritical() { return true; }
    async check(server, ssh) {
        const output = await ssh.execute(server, 'df -k / 2>/dev/null | tail -1');
        const parts = output.trim().split(/\s+/);
        if (parts.length < 6)
            throw new Error('无法解析磁盘');
        const total = parseInt(parts[1]) * 1024;
        const used = parseInt(parts[2]) * 1024;
        const available = parseInt(parts[3]) * 1024;
        const usagePercent = parseFloat(parts[4].replace('%', ''));
        return {
            uptime: 'N/A',
            loadAverage: [0, 0, 0],
            memory: { total: 0, used: 0, free: 0, available: 0, swapTotal: 0, swapUsed: 0 },
            disk: { mountPoint: parts[5], total, used, available, usagePercent }
        };
    }
}
exports.DiskCheck = DiskCheck;
class HealthChecker {
    constructor(strategies) {
        this.strategies = strategies || [
            new LoadAverageCheck(),
            new MemoryCheck(),
            new DiskCheck()
        ];
        this.strategies.sort((a, b) => a.priority - b.priority);
    }
    async checkAll(server, ssh) {
        const result = {
            uptime: 'N/A',
            loadAverage: [0, 0, 0],
            memory: { total: 0, used: 0, free: 0, available: 0, swapTotal: 0, swapUsed: 0 },
            disk: { mountPoint: '/', total: 0, used: 0, available: 0, usagePercent: 0 }
        };
        await Promise.all(this.strategies.map(async (s) => {
            const res = await s.execute(server, ssh);
            if (res.success && res.metrics) {
                Object.assign(result, res.metrics);
            }
        }));
        return result;
    }
}
exports.HealthChecker = HealthChecker;
async function checkServices(server, ssh, services = ['nginx', 'docker', 'postgresql', 'redis-server']) {
    const results = [];
    for (const svc of services) {
        try {
            const status = await ssh.execute(server, `systemctl is-active ${svc} 2>/dev/null || echo "stopped"`);
            results.push({ name: svc, running: status.trim() === 'active' });
        }
        catch {
            results.push({ name: svc, running: false });
        }
    }
    return results;
}
//# sourceMappingURL=HealthChecker.js.map