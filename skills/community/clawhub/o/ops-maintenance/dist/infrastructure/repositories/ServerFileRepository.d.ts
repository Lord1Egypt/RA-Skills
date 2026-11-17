/**
 * 服务器文件仓库实现
 * 基于 JSON 文件的服务器配置存储
 */
import type { Server, IServerRepository } from '../../config/schemas';
import { ConfigManager } from '../../config/loader';
/**
 * 服务器文件仓库
 *
 * 职责：
 * - 持久化服务器配置到 JSON 文件
 * - 支持运行时 CRUD 操作（通过 ConfigManager）
 * - 支持标签筛选
 * - 支持配置变更通知
 */
export declare class ServerFileRepository implements IServerRepository {
    private externalConfigManager?;
    private configManager;
    private onChangeCallbacks;
    constructor(configPath?: string, externalConfigManager?: ConfigManager | undefined);
    /**
     * 设置外部 ConfigManager（用于依赖注入）
     */
    setConfigManager(configManager: ConfigManager): void;
    /**
     * 初始化仓库
     */
    init(): Promise<void>;
    /**
     * 获取所有服务器
     */
    findAll(): Promise<Server[]>;
    /**
     * 按标签查找服务器
     */
    findByTags(tags: string[]): Promise<Server[]>;
    /**
     * 按 ID 查找
     */
    findById(id: string): Promise<Server | null>;
    /**
     * 添加服务器
     */
    add(server: Server): Promise<void>;
    /**
     * 更新服务器
     */
    update(server: Server): Promise<void>;
    /**
     * 删除服务器
     */
    remove(host: string): Promise<void>;
    /**
     * 监听配置变更
     */
    onChange(callback: () => void): void;
    /**
     * 通知所有监听者
     */
    private notifyChange;
    /**
     * 获取配置管理器（高级用法）
     */
    getConfigManager(): ConfigManager;
    /**
     * 获取热重载功能
     */
    reload(): Promise<void>;
    /**
     * 停止仓库
     */
    stop(): void;
}
/**
 * 创建服务器仓库实例
 */
export declare function createServerRepository(configPath?: string): ServerFileRepository;
//# sourceMappingURL=ServerFileRepository.d.ts.map