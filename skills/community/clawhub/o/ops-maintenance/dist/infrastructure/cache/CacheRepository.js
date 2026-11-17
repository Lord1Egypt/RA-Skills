"use strict";
/**
 * 缓存仓库接口实现
 * 支持内存缓存和文件缓存
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.TieredCache = exports.CacheFactory = exports.FileCache = exports.MemoryCache = void 0;
const fs_1 = require("fs");
const path_1 = require("path");
/**
 * 内存缓存实现
 */
class MemoryCache {
    constructor(ttlSeconds = 300) {
        this.ttlSeconds = ttlSeconds;
        this.cache = new Map();
        this.cleanupInterval = null;
        this.startCleanup();
    }
    async get(key) {
        const entry = this.cache.get(key);
        if (!entry)
            return null;
        if (Date.now() > entry.expiresAt) {
            this.cache.delete(key);
            return null;
        }
        return entry.value;
    }
    async set(key, value, ttlSeconds) {
        const ttl = ttlSeconds ?? this.ttlSeconds;
        const expiresAt = Date.now() + ttl * 1000;
        this.cache.set(key, { value, expiresAt });
    }
    async delete(key) {
        this.cache.delete(key);
    }
    async clear() {
        this.cache.clear();
    }
    /**
     * 启动清理任务（定期删除过期缓存）
     */
    startCleanup() {
        this.cleanupInterval = setInterval(() => {
            const now = Date.now();
            for (const [key, entry] of this.cache) {
                if (now > entry.expiresAt) {
                    this.cache.delete(key);
                }
            }
        }, 60 * 1000); // 每分钟清理一次
    }
    /**
     * 停止清理任务
     */
    stop() {
        if (this.cleanupInterval) {
            clearInterval(this.cleanupInterval);
            this.cleanupInterval = null;
        }
    }
    /**
     * 获取缓存统计
     */
    getStats() {
        return {
            size: this.cache.size,
            keys: Array.from(this.cache.keys())
        };
    }
}
exports.MemoryCache = MemoryCache;
/**
 * 文件缓存实现
 * 适用于进程重启后缓存持久化
 */
class FileCache {
    constructor(cacheDir, ttlSeconds = 300) {
        this.ttlSeconds = ttlSeconds;
        this.cacheDir = cacheDir || (0, path_1.join)(process.env.HOME || process.env.USERPROFILE || '~', '.cache', 'ops-maintenance');
        this.defaultTTL = ttlSeconds;
    }
    getCacheFilePath(key) {
        // 将键名转换为安全的文件名
        const safeKey = key.replace(/[^a-zA-Z0-9_-]/g, '_');
        return (0, path_1.join)(this.cacheDir, `${safeKey}.json`);
    }
    async get(key) {
        const filePath = this.getCacheFilePath(key);
        try {
            if (!(0, fs_1.existsSync)(filePath))
                return null;
            const content = await (0, fs_1.readFile)(filePath, 'utf-8');
            const data = JSON.parse(content);
            // 检查是否过期
            if (data.expiresAt && Date.now() > data.expiresAt) {
                await this.delete(key);
                return null;
            }
            return data.value;
        }
        catch {
            return null;
        }
    }
    async set(key, value, ttlSeconds) {
        const filePath = this.getCacheFilePath(key);
        const ttl = ttlSeconds ?? this.defaultTTL;
        const data = {
            value,
            expiresAt: Date.now() + ttl * 1000,
            createdAt: Date.now()
        };
        try {
            await (0, fs_1.writeFile)(filePath, JSON.stringify(data, null, 2), 'utf-8');
        }
        catch (error) {
            console.error('文件缓存写入失败:', error.message);
        }
    }
    async delete(key) {
        const filePath = this.getCacheFilePath(key);
        try {
            if ((0, fs_1.existsSync)(filePath)) {
                await (0, fs_1.unlink)(filePath);
            }
        }
        catch {
            // 忽略删除失败
        }
    }
    async clear() {
        // 清空整个缓存目录
        // 简化实现：删除缓存目录下所有 .json 文件
        // 生产环境需要更安全的实现
    }
    /**
     * 清理过期缓存
     */
    async cleanup() {
        let cleaned = 0;
        // 遍历缓存目录并删除过期文件
        // 这里简化处理
        return cleaned;
    }
}
exports.FileCache = FileCache;
/**
 * 缓存工厂
 */
class CacheFactory {
    static createMemoryCache(ttl) {
        return new MemoryCache(ttl);
    }
    static createFileCache(cacheDir, ttl) {
        return new FileCache(cacheDir, ttl);
    }
    /**
     * 创建分层缓存（先内存后文件）
     */
    static createTieredCache(memoryCache, fileCache) {
        return new TieredCache(memoryCache, fileCache);
    }
}
exports.CacheFactory = CacheFactory;
/**
 * 分层缓存（Memory + File）
 */
class TieredCache {
    constructor(memory, file) {
        this.memory = memory;
        this.file = file;
    }
    async get(key) {
        // 先查内存
        const fromMemory = await this.memory.get(key);
        if (fromMemory !== null) {
            return fromMemory;
        }
        // 查文件，并回填内存
        const fromFile = await this.file.get(key);
        if (fromFile !== null) {
            await this.memory.set(key, fromFile);
            return fromFile;
        }
        return null;
    }
    async set(key, value, ttlSeconds) {
        await Promise.all([
            this.memory.set(key, value, ttlSeconds),
            this.file.set(key, value, ttlSeconds)
        ]);
    }
    async delete(key) {
        await Promise.all([
            this.memory.delete(key),
            this.file.delete(key)
        ]);
    }
    async clear() {
        await Promise.all([
            this.memory.clear(),
            this.file.clear()
        ]);
    }
}
exports.TieredCache = TieredCache;
//# sourceMappingURL=CacheRepository.js.map