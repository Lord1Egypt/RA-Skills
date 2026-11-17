/**
 * 服务器文件仓库实现
 * 基于 JSON 文件的服务器配置存储
 */

import { readFile, writeFile, existsSync, mkdir as fsMkdir } from 'fs'
import { join } from 'path'
import { promisify } from 'util'
import type { Server, SSHConfig, IServerRepository } from '../../config/schemas'
import { ConfigManager } from '../../config/loader'
import { validateServersList } from '../../config/validator'

const mkdir = promisify(fsMkdir)
const readFileAsync = promisify(readFile)
const writeFileAsync = promisify(writeFile)

/**
 * 服务器文件仓库
 *
 * 职责：
 * - 持久化服务器配置到 JSON 文件
 * - 支持运行时 CRUD 操作（通过 ConfigManager）
 * - 支持标签筛选
 * - 支持配置变更通知
 */
export class ServerFileRepository implements IServerRepository {
  private configManager: ConfigManager
  private onChangeCallbacks: Array<() => void> = []

  constructor(configPath?: string, private externalConfigManager?: ConfigManager) {
    this.configManager = externalConfigManager || new ConfigManager({ configPath })
  }

  /**
   * 设置外部 ConfigManager（用于依赖注入）
   */
  setConfigManager(configManager: ConfigManager): void {
    this.configManager = configManager
  }

  /**
   * 初始化仓库
   */
  async init(): Promise<void> {
    await this.configManager.start()

    // 监听配置变更
    this.configManager.on('change', () => {
      this.notifyChange()
    })
  }

  /**
   * 获取所有服务器
   */
  async findAll(): Promise<Server[]> {
    return this.configManager.getAll()
  }

  /**
   * 按标签查找服务器
   */
  async findByTags(tags: string[]): Promise<Server[]> {
    return this.configManager.getByTags(tags)
  }

  /**
   * 按 ID 查找
   */
  async findById(id: string): Promise<Server | null> {
    return this.configManager.getById(id) || null
  }

  /**
   * 添加服务器
   */
  async add(server: Server): Promise<void> {
    const config: SSHConfig = {
      host: server.host,
      port: server.port,
      user: server.user,
      name: server.name,
      tags: server.tags
    }
    await this.configManager.add(config)
  }

  /**
   * 更新服务器
   */
  async update(server: Server): Promise<void> {
    await this.configManager.update(server)
  }

  /**
   * 删除服务器
   */
  async remove(host: string): Promise<void> {
    await this.configManager.remove(host)
  }

  /**
   * 监听配置变更
   */
  onChange(callback: () => void): void {
    this.onChangeCallbacks.push(callback)
  }

  /**
   * 通知所有监听者
   */
  private notifyChange(): void {
    for (const callback of this.onChangeCallbacks) {
      try {
        callback()
      } catch (error) {
        console.error('配置变更回调执行失败:', error)
      }
    }
  }

  /**
   * 获取配置管理器（高级用法）
   */
  getConfigManager(): ConfigManager {
    return this.configManager
  }

  /**
   * 获取热重载功能
   */
  async reload(): Promise<void> {
    await this.configManager.hotReload()
  }

  /**
   * 停止仓库
   */
  stop(): void {
    this.configManager.stop()
  }
}

/**
 * 创建服务器仓库实例
 */
export function createServerRepository(configPath?: string): ServerFileRepository {
  return new ServerFileRepository(configPath)
}