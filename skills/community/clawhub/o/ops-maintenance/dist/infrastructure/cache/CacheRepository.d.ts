/**
 * 缓存仓库接口实现
 * 支持内存缓存和文件缓存
 */
import type { ICacheRepository } from '../../config/schemas';
/**
 * 内存缓存实现
 */
export declare class MemoryCache implements ICacheRepository {
    private ttlSeconds;
    private cache;
    private cleanupInterval;
    constructor(ttlSeconds?: number);
    get<T>(key: string): Promise<T | null>;
    set<T>(key: string, value: T, ttlSeconds?: number): Promise<void>;
    delete(key: string): Promise<void>;
    clear(): Promise<void>;
    /**
     * 启动清理任务（定期删除过期缓存）
     */
    private startCleanup;
    /**
     * 停止清理任务
     */
    stop(): void;
    /**
     * 获取缓存统计
     */
    getStats(): {
        size: number;
        keys: string[];
    };
}
/**
 * 文件缓存实现
 * 适用于进程重启后缓存持久化
 */
export declare class FileCache implements ICacheRepository {
    private ttlSeconds;
    private cacheDir;
    private defaultTTL;
    constructor(cacheDir?: string, ttlSeconds?: number);
    private getCacheFilePath;
    get<T>(key: string): Promise<T | null>;
    set<T>(key: string, value: T, ttlSeconds?: number): Promise<void>;
    delete(key: string): Promise<void>;
    clear(): Promise<void>;
    /**
     * 清理过期缓存
     */
    cleanup(): Promise<number>;
}
/**
 * 缓存工厂
 */
export declare class CacheFactory {
    static createMemoryCache(ttl?: number): MemoryCache;
    static createFileCache(cacheDir?: string, ttl?: number): FileCache;
    /**
     * 创建分层缓存（先内存后文件）
     */
    static createTieredCache(memoryCache: MemoryCache, fileCache: FileCache): TieredCache;
}
/**
 * 分层缓存（Memory + File）
 */
export declare class TieredCache implements ICacheRepository {
    private memory;
    private file;
    constructor(memory: MemoryCache, file: FileCache);
    get<T>(key: string): Promise<T | null>;
    set<T>(key: string, value: T, ttlSeconds?: number): Promise<void>;
    delete(key: string): Promise<void>;
    clear(): Promise<void>;
}
//# sourceMappingURL=CacheRepository.d.ts.map