"use strict";
/**
 * 配置管理器 - 简化版
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.ConfigManager = void 0;
const fs_1 = require("fs");
const path_1 = require("path");
const util_1 = require("util");
const mkdir = (0, util_1.promisify)(fs_1.mkdir);
const readFileAsync = (0, util_1.promisify)(fs_1.readFile);
const writeFileAsync = (0, util_1.promisify)(fs_1.writeFile);
function getConfigPath() {
    const home = process.env.HOME || process.env.USERPROFILE || '~';
    return (0, path_1.join)(home, '.config', 'ops-maintenance', 'servers.json');
}
function getServerKey(config) {
    return `${config.host}:${config.port || 22}:${config.user || 'root'}`;
}
class ConfigManager {
    constructor(configPath) {
        this.servers = [];
        this.mtime = 0;
        this.configPath = configPath || getConfigPath();
    }
    async start() {
        await this.load();
    }
    async load() {
        try {
            if (!(0, fs_1.existsSync)(this.configPath)) {
                await this.save([]);
                this.servers = [];
                return;
            }
            const content = await readFileAsync(this.configPath, 'utf-8');
            const configs = JSON.parse(content);
            this.servers = configs.map((cfg, idx) => ({
                id: getServerKey(cfg),
                host: cfg.host,
                port: cfg.port || 22,
                user: cfg.user || 'root',
                name: cfg.name || `server-${idx}`,
                tags: cfg.tags || []
            }));
            const { statSync } = await Promise.resolve().then(() => __importStar(require('fs')));
            const stats = statSync(this.configPath);
            this.mtime = Math.floor(stats.mtimeMs);
        }
        catch (error) {
            console.error('配置加载失败:', error.message);
            throw error;
        }
    }
    async save(servers) {
        if (servers !== undefined) {
            this.servers = servers;
        }
        const configDir = this.configPath.replace(/[^/\\]+$/, '');
        if (!(0, fs_1.existsSync)(configDir)) {
            await mkdir(configDir, { recursive: true });
        }
        const configs = this.servers.map(s => ({
            host: s.host,
            port: s.port,
            user: s.user,
            name: s.name,
            tags: s.tags
        }));
        await writeFileAsync(this.configPath, JSON.stringify(configs, null, 2) + '\n', 'utf-8');
    }
    getAll() {
        return [...this.servers];
    }
    getByTags(tags) {
        return this.servers.filter(s => tags.every(t => s.tags.includes(t)));
    }
    getById(id) {
        return this.servers.find(s => s.id === id) || null;
    }
    getByHost(host) {
        return this.servers.find(s => s.host === host) || null;
    }
    async add(config) {
        const server = {
            id: getServerKey(config),
            host: config.host,
            port: config.port || 22,
            user: config.user || 'root',
            name: config.name,
            tags: config.tags || []
        };
        const existing = this.getByHost(server.host);
        if (existing) {
            const idx = this.servers.findIndex(s => s.host === server.host);
            if (idx >= 0)
                this.servers[idx] = server;
        }
        else {
            this.servers.push(server);
        }
        await this.save();
        return server;
    }
    async update(server) {
        const idx = this.servers.findIndex(s => s.id === server.id);
        if (idx >= 0) {
            this.servers[idx] = server;
            await this.save();
        }
    }
    async remove(host) {
        const idx = this.servers.findIndex(s => s.host === host);
        if (idx >= 0) {
            this.servers.splice(idx, 1);
            await this.save();
            return true;
        }
        return false;
    }
    async hotReload() {
        await this.load();
    }
    stop() { }
    getConfigPath() {
        return this.configPath;
    }
    get count() {
        return this.servers.length;
    }
}
exports.ConfigManager = ConfigManager;
//# sourceMappingURL=loader.js.map