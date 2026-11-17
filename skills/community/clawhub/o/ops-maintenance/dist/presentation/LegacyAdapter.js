"use strict";
/**
 * 向后兼容适配器
 * 将旧版 API 调用转换为新版架构
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.LegacyAdapter = void 0;
exports.getLegacyAdapter = getLegacyAdapter;
exports.initLegacyAdapter = initLegacyAdapter;
const container_1 = require("../container");
const HealthCheckUseCase_1 = require("../core/usecases/HealthCheckUseCase");
const PasswordCheckUseCase_1 = require("../core/usecases/PasswordCheckUseCase");
const MarkdownFormatter_1 = require("../presentation/formatters/MarkdownFormatter");
const ThresholdChecker_1 = require("../infrastructure/monitoring/ThresholdChecker");
const HealthChecker_1 = require("../infrastructure/monitoring/HealthChecker");
/**
 * 向后兼容适配器
 * 提供与旧版完全相同的导出函数签名
 */
class LegacyAdapter {
    constructor(config) {
        this.config = config;
        this.initialized = false;
    }
    /**
     * 初始化适配器
     */
    async init() {
        if (this.initialized)
            return;
        this.container = new container_1.Container({
            configPath: this.config?.configPath,
            useConnectionPool: this.config?.useConnectionPool ?? true,
            cacheTTL: this.config?.cacheTTL ?? 30,
            environment: this.config?.environment ?? 'production'
        });
        await this.container.init();
        this.serverRepo = this.container.getServerRepository();
        this.sshClient = this.container.getSSHClient();
        this.cache = this.container.getCache();
        this.initialized = true;
    }
    /**
     * 确保已初始化
     */
    ensureInitialized() {
        if (!this.initialized) {
            throw new Error('适配器未初始化，请先调用 init()');
        }
    }
    // ============ 配置管理函数（兼容旧版） ============
    async loadServers() {
        this.ensureInitialized();
        return this.serverRepo.findAll();
    }
    async loadServerState() {
        return null;
    }
    async saveServerState(state) { }
    calculateServerChecksums(servers) {
        return servers.map(s => `${s.host}:${s.port || 22}:${s.user || 'root'}`).sort();
    }
    async detectNewServers() {
        const allServers = await this.loadServers();
        return {
            newServers: [],
            allServers,
            message: `当前配置了 ${allServers.length} 台服务器`
        };
    }
    async addServer(config) {
        this.ensureInitialized();
        const server = Server.fromSSHConfig(config);
        await this.serverRepo.add(server);
    }
    async removeServer(host) {
        this.ensureInitialized();
        await this.serverRepo.remove(host);
    }
    async getServersByTag(tag) {
        this.ensureInitialized();
        return this.serverRepo.findByTags([tag]);
    }
    async batchAddServers(servers) {
        this.ensureInitialized();
        const results = [];
        let success = 0;
        let failed = 0;
        for (const serverStr of servers) {
            try {
                const config = this.parseServerString(serverStr);
                await this.addServer(config);
                success++;
                results.push(`✅ ${config.name || config.host}:${config.port || 22} - 已添加`);
            }
            catch (error) {
                failed++;
                results.push(`❌ ${serverStr} - ${error.message}`);
            }
        }
        return { success, failed, details: results };
    }
    async importServersFromText(text) {
        this.ensureInitialized();
        try {
            const parsed = JSON.parse(text);
            const arr = Array.isArray(parsed) ? parsed : [parsed];
            const servers = [];
            for (const item of arr) {
                if (item.host) {
                    const config = {
                        host: item.host,
                        port: item.port || 22,
                        user: item.user,
                        name: item.name,
                        tags: item.tags
                    };
                    const server = Server.fromSSHConfig(config);
                    servers.push(server);
                    await this.addServer(config);
                }
            }
            return { success: servers.length, failed: 0, servers };
        }
        catch {
            return { success: 0, failed: 0, servers: [] };
        }
    }
    parseServerString(serverStr) {
        let host = serverStr;
        let user;
        let port;
        if (host.includes('@')) {
            const parts = host.split('@');
            user = parts[0];
            host = parts[1];
        }
        if (host.includes(':')) {
            const parts = host.split(':');
            host = parts[0];
            port = parseInt(parts[1]);
        }
        const name = `server-${host.replace(/\./g, '-')}`;
        return { host, port: port || 22, user, name };
    }
    // ============ 运维操作函数（兼容旧版） ============
    async checkAllServersHealth(tags, serverList) {
        this.ensureInitialized();
        const useCase = new HealthCheckUseCase_1.HealthCheckUseCase(this.serverRepo, this.sshClient, this.cache, new HealthChecker_1.HealthChecker(), new ThresholdChecker(ThresholdChecker_1.DEFAULT_THRESHOLDS));
        const report = await useCase.execute({ tags, servers: serverList, force: false });
        return report.serverHealth.map(h => ({
            server: h.server.getDisplayName(),
            status: this.formatStatus(h.status),
            details: this.formatDetails(h)
        }));
    }
    formatStatus(status) {
        switch (status) {
            case 'healthy':
                return '✅ 健康';
            case 'warning':
                return '⚠️ 警告';
            case 'offline':
                return '❌ 离线';
            default:
                return '❓ 未知';
        }
    }
    formatDetails(health) {
        if (!health.metrics)
            return '无数据';
        const load = health.metrics.loadAverage;
        return `负载: ${load ? `${load[0].toFixed(2)}, ${load[1].toFixed(2)}, ${load[2].toFixed(2)}` : 'N/A'}`;
    }
    async checkRemoteHealth(config, services = ['nginx', 'docker', 'postgresql', 'redis-server']) {
        this.ensureInitialized();
        const server = Server.fromSSHConfig(config);
        const useCase = new HealthCheckUseCase_1.HealthCheckUseCase(this.serverRepo, this.sshClient, this.cache, new HealthChecker_1.HealthChecker(), new ThresholdChecker(ThresholdChecker_1.DEFAULT_THRESHOLDS));
        const health = await useCase.execute({ servers: [server] });
        if (health.serverHealth.length === 0) {
            return `❌ **连接失败**: 无法连接到 ${config.host}`;
        }
        const h = health.serverHealth[0];
        const formatter = new MarkdownFormatter_1.MarkdownFormatter();
        return formatter.formatServerHealth(h);
    }
    async checkAllServersPasswordExpiration(tags) {
        this.ensureInitialized();
        const useCase = new PasswordCheckUseCase_1.PasswordCheckUseCase(this.serverRepo, this.sshClient);
        return await useCase.execute(tags);
    }
    async checkAllServersPasswordExpirationReport(tags) {
        this.ensureInitialized();
        const useCase = new PasswordCheckUseCase_1.PasswordCheckUseCase(this.serverRepo, this.sshClient);
        const results = await useCase.execute(tags);
        const formatter = new MarkdownFormatter_1.MarkdownFormatter();
        return formatter.formatPasswordReport({ results });
    }
    async getClusterSummary() {
        this.ensureInitialized();
        const useCase = new HealthCheckUseCase_1.HealthCheckUseCase(this.serverRepo, this.sshClient, this.cache, new HealthChecker_1.HealthChecker(), new ThresholdChecker(ThresholdChecker_1.DEFAULT_THRESHOLDS));
        const report = await useCase.execute();
        const formatter = new MarkdownFormatter_1.MarkdownFormatter();
        return formatter.formatClusterReport(report);
    }
    async runRemoteCommand(config, command) {
        this.ensureInitialized();
        const server = Server.fromSSHConfig(config);
        try {
            return await this.sshClient.execute(server, command);
        }
        catch (error) {
            return `错误: ${error.message}`;
        }
    }
    async runCommand(cmd, timeout = 10000) {
        if (process.platform === 'win32') {
            return '⚠️ 当前系统为 Windows，runCommand 只能在 Linux/macOS 上执行。';
        }
        const { exec } = require('child_process');
        const { promisify } = require('util');
        const execAsync = promisify(exec);
        try {
            const { stdout, stderr } = await execAsync(cmd, { timeout, shell: '/bin/zsh' });
            return stdout || stderr || '(无输出)';
        }
        catch (error) {
            return `命令执行失败: ${error.message}`;
        }
    }
    async executeOnAllServers(command, tags) {
        this.ensureInitialized();
        const servers = tags
            ? await this.serverRepo.findByTags(tags)
            : await this.serverRepo.findAll();
        const results = [];
        await Promise.all(servers.map(async (server) => {
            try {
                const output = await this.sshClient.execute(server, command);
                results.push({ server: server.getDisplayName(), output });
            }
            catch (error) {
                results.push({ server: server.getDisplayName(), output: `错误: ${error.message}` });
            }
        }));
        return results;
    }
    // 占位函数（旧版未完全实现的功能）
    async checkRemotePort(config, port) {
        return `端口检查功能尚未完全实现`;
    }
    async checkRemoteProcess(config, name) {
        return `进程检查功能尚未完全实现`;
    }
    async checkRemoteDisk(config) {
        return `磁盘检查: ${config.host}`;
    }
    async checkRemotePerformance(config) {
        return `性能检查功能尚未完全实现`;
    }
    async checkRemoteLogs(config, pattern, lines) {
        return `日志检查功能尚未完全实现`;
    }
    async executeOp(action, arg) {
        const actions = {
            'health': () => this.getClusterSummary(),
            'check': () => this.getClusterSummary(),
            'cluster': () => this.getClusterSummary(),
            'password': () => this.checkAllServersPasswordExpirationReport(),
            'passwd': () => this.checkAllServersPasswordExpirationReport(),
            'expire': () => this.checkAllServersPasswordExpirationReport(),
            'disk': () => this.checkRemoteDisk({ host: 'local' }),
            'logs': () => Promise.resolve('日志检查未实现'),
            'log': () => Promise.resolve('日志检查未实现'),
            'perf': () => Promise.resolve('性能检查未实现'),
            'performance': () => Promise.resolve('性能检查未实现'),
            'ports': () => Promise.resolve('端口检查未实现'),
            'port': () => Promise.resolve('端口检查未实现'),
            'process': () => Promise.resolve('进程检查未实现'),
            'proc': () => Promise.resolve('进程检查未实现')
        };
        const fn = actions[action.toLowerCase()];
        if (fn) {
            return fn();
        }
        return `未知操作: ${action}`;
    }
    async executeRemoteOp(action, config, arg) {
        return await this.executeOp(action, arg);
    }
    async shutdown() {
        if (this.container) {
            await this.container.shutdown();
        }
    }
}
exports.LegacyAdapter = LegacyAdapter;
// 全局实例
let globalAdapter = null;
/**
 * 获取全局适配器
 */
function getLegacyAdapter(config) {
    if (!globalAdapter) {
        globalAdapter = new LegacyAdapter(config);
    }
    return globalAdapter;
}
/**
 * 初始化全局适配器
 */
async function initLegacyAdapter(config) {
    const adapter = getLegacyAdapter(config);
    await adapter.init();
    return adapter;
}
//# sourceMappingURL=LegacyAdapter.js.map