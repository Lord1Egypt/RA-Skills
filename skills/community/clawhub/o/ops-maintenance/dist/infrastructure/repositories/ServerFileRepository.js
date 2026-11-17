"use strict";
/**
 * 服务器文件仓库实现
 * 基于 JSON 文件的服务器配置存储
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.ServerFileRepository = void 0;
exports.createServerRepository = createServerRepository;
const fs_1 = require("fs");
const util_1 = require("util");
const loader_1 = require("../../config/loader");
const mkdir = (0, util_1.promisify)(fs_1.mkdir);
const readFileAsync = (0, util_1.promisify)(fs_1.readFile);
const writeFileAsync = (0, util_1.promisify)(fs_1.writeFile);
/**
 * 服务器文件仓库
 *
 * 职责：
 * - 持久化服务器配置到 JSON 文件
 * - 支持运行时 CRUD 操作（通过 ConfigManager）
 * - 支持标签筛选
 * - 支持配置变更通知
 */
class ServerFileRepository {
    constructor(configPath, externalConfigManager) {
        this.externalConfigManager = externalConfigManager;
        this.onChangeCallbacks = [];
        this.configManager = externalConfigManager || new loader_1.ConfigManager({ configPath });
    }
    /**
     * 设置外部 ConfigManager（用于依赖注入）
     */
    setConfigManager(configManager) {
        this.configManager = configManager;
    }
    /**
     * 初始化仓库
     */
    async init() {
        await this.configManager.start();
        // 监听配置变更
        this.configManager.on('change', () => {
            this.notifyChange();
        });
    }
    /**
     * 获取所有服务器
     */
    async findAll() {
        return this.configManager.getAll();
    }
    /**
     * 按标签查找服务器
     */
    async findByTags(tags) {
        return this.configManager.getByTags(tags);
    }
    /**
     * 按 ID 查找
     */
    async findById(id) {
        return this.configManager.getById(id) || null;
    }
    /**
     * 添加服务器
     */
    async add(server) {
        const config = {
            host: server.host,
            port: server.port,
            user: server.user,
            name: server.name,
            tags: server.tags
        };
        await this.configManager.add(config);
    }
    /**
     * 更新服务器
     */
    async update(server) {
        await this.configManager.update(server);
    }
    /**
     * 删除服务器
     */
    async remove(host) {
        await this.configManager.remove(host);
    }
    /**
     * 监听配置变更
     */
    onChange(callback) {
        this.onChangeCallbacks.push(callback);
    }
    /**
     * 通知所有监听者
     */
    notifyChange() {
        for (const callback of this.onChangeCallbacks) {
            try {
                callback();
            }
            catch (error) {
                console.error('配置变更回调执行失败:', error);
            }
        }
    }
    /**
     * 获取配置管理器（高级用法）
     */
    getConfigManager() {
        return this.configManager;
    }
    /**
     * 获取热重载功能
     */
    async reload() {
        await this.configManager.hotReload();
    }
    /**
     * 停止仓库
     */
    stop() {
        this.configManager.stop();
    }
}
exports.ServerFileRepository = ServerFileRepository;
/**
 * 创建服务器仓库实例
 */
function createServerRepository(configPath) {
    return new ServerFileRepository(configPath);
}
//# sourceMappingURL=ServerFileRepository.js.map