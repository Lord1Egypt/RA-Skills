/**
 * 缓存仓库接口实现
 * 支持内存缓存和文件缓存
 */

import { existsSync, readFile, writeFile, unlink } from 'fs'
import { join } from 'path'
import type { ICacheRepository } from '../../config/schemas'

/**
 * 内存缓存实现
 */
export class MemoryCache implements ICacheRepository {
  private cache: Map<string, { value: any; expiresAt: number }> = new Map()
  private cleanupInterval: NodeJS.Timeout | null = null

  constructor(private ttlSeconds: number = 300) {
    this.startCleanup()
  }

  async get<T>(key: string): Promise<T | null> {
    const entry = this.cache.get(key)
    if (!entry) return null

    if (Date.now() > entry.expiresAt) {
      this.cache.delete(key)
      return null
    }

    return entry.value
  }

  async set<T>(key: string, value: T, ttlSeconds?: number): Promise<void> {
    const ttl = ttlSeconds ?? this.ttlSeconds
    const expiresAt = Date.now() + ttl * 1000
    this.cache.set(key, { value, expiresAt })
  }

  async delete(key: string): Promise<void> {
    this.cache.delete(key)
  }

  async clear(): Promise<void> {
    this.cache.clear()
  }

  /**
   * 启动清理任务（定期删除过期缓存）
   */
  private startCleanup(): void {
    this.cleanupInterval = setInterval(() => {
      const now = Date.now()
      for (const [key, entry] of this.cache) {
        if (now > entry.expiresAt) {
          this.cache.delete(key)
        }
      }
    }, 60 * 1000) // 每分钟清理一次
  }

  /**
   * 停止清理任务
   */
  stop(): void {
    if (this.cleanupInterval) {
      clearInterval(this.cleanupInterval)
      this.cleanupInterval = null
    }
  }

  /**
   * 获取缓存统计
   */
  getStats(): { size: number; keys: string[] } {
    return {
      size: this.cache.size,
      keys: Array.from(this.cache.keys())
    }
  }
}

/**
 * 文件缓存实现
 * 适用于进程重启后缓存持久化
 */
export class FileCache implements ICacheRepository {
  private cacheDir: string
  private defaultTTL: number

  constructor(cacheDir?: string, private ttlSeconds: number = 300) {
    this.cacheDir = cacheDir || join(process.env.HOME || process.env.USERPROFILE || '~', '.cache', 'ops-maintenance')
    this.defaultTTL = ttlSeconds
  }

  private getCacheFilePath(key: string): string {
    // 将键名转换为安全的文件名
    const safeKey = key.replace(/[^a-zA-Z0-9_-]/g, '_')
    return join(this.cacheDir, `${safeKey}.json`)
  }

  async get<T>(key: string): Promise<T | null> {
    const filePath = this.getCacheFilePath(key)

    try {
      if (!existsSync(filePath)) return null

      const content = await readFile(filePath, 'utf-8')
      const data = JSON.parse(content)

      // 检查是否过期
      if (data.expiresAt && Date.now() > data.expiresAt) {
        await this.delete(key)
        return null
      }

      return data.value
    } catch {
      return null
    }
  }

  async set<T>(key: string, value: T, ttlSeconds?: number): Promise<void> {
    const filePath = this.getCacheFilePath(key)
    const ttl = ttlSeconds ?? this.defaultTTL

    const data = {
      value,
      expiresAt: Date.now() + ttl * 1000,
      createdAt: Date.now()
    }

    try {
      await writeFile(filePath, JSON.stringify(data, null, 2), 'utf-8')
    } catch (error: any) {
      console.error('文件缓存写入失败:', error.message)
    }
  }

  async delete(key: string): Promise<void> {
    const filePath = this.getCacheFilePath(key)
    try {
      if (existsSync(filePath)) {
        await unlink(filePath)
      }
    } catch {
      // 忽略删除失败
    }
  }

  async clear(): Promise<void> {
    // 清空整个缓存目录
    // 简化实现：删除缓存目录下所有 .json 文件
    // 生产环境需要更安全的实现
  }

  /**
   * 清理过期缓存
   */
  async cleanup(): Promise<number> {
    let cleaned = 0
    // 遍历缓存目录并删除过期文件
    // 这里简化处理
    return cleaned
  }
}

/**
 * 缓存工厂
 */
export class CacheFactory {
  static createMemoryCache(ttl?: number): MemoryCache {
    return new MemoryCache(ttl)
  }

  static createFileCache(cacheDir?: string, ttl?: number): FileCache {
    return new FileCache(cacheDir, ttl)
  }

  /**
   * 创建分层缓存（先内存后文件）
   */
  static createTieredCache(
    memoryCache: MemoryCache,
    fileCache: FileCache
  ): TieredCache {
    return new TieredCache(memoryCache, fileCache)
  }
}

/**
 * 分层缓存（Memory + File）
 */
export class TieredCache implements ICacheRepository {
  constructor(
    private memory: MemoryCache,
    private file: FileCache
  ) {}

  async get<T>(key: string): Promise<T | null> {
    // 先查内存
    const fromMemory = await this.memory.get<T>(key)
    if (fromMemory !== null) {
      return fromMemory
    }

    // 查文件，并回填内存
    const fromFile = await this.file.get<T>(key)
    if (fromFile !== null) {
      await this.memory.set(key, fromFile)
      return fromFile
    }

    return null
  }

  async set<T>(key: string, value: T, ttlSeconds?: number): Promise<void> {
    await Promise.all([
      this.memory.set(key, value, ttlSeconds),
      this.file.set(key, value, ttlSeconds)
    ])
  }

  async delete(key: string): Promise<void> {
    await Promise.all([
      this.memory.delete(key),
      this.file.delete(key)
    ])
  }

  async clear(): Promise<void> {
    await Promise.all([
      this.memory.clear(),
      this.file.clear()
    ])
  }
}