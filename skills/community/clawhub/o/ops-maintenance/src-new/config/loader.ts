/**
 * 配置管理器 - 简化版
 */

import { readFile, writeFile, existsSync, mkdir as fsMkdir } from 'fs'
import { join } from 'path'
import { promisify } from 'util'
import { Server, SSHConfig } from '../types'

const mkdir = promisify(fsMkdir)
const readFileAsync = promisify(readFile)
const writeFileAsync = promisify(writeFile)

function getConfigPath(): string {
  const home = process.env.HOME || process.env.USERPROFILE || '~'
  return join(home, '.config', 'ops-maintenance', 'servers.json')
}

function getServerKey(config: SSHConfig): string {
  return `${config.host}:${config.port || 22}:${config.user || 'root'}`
}

export class ConfigManager {
  private servers: Server[] = []
  private configPath: string
  private mtime = 0

  constructor(configPath?: string) {
    this.configPath = configPath || getConfigPath()
  }

  async start(): Promise<void> {
    await this.load()
  }

  async load(): Promise<void> {
    try {
      if (!existsSync(this.configPath)) {
        await this.save([])
        this.servers = []
        return
      }

      const content = await readFileAsync(this.configPath, 'utf-8')
      const configs: any[] = JSON.parse(content)

      this.servers = configs.map((cfg, idx) => ({
        id: getServerKey(cfg),
        host: cfg.host,
        port: cfg.port || 22,
        user: cfg.user || 'root',
        name: cfg.name || `server-${idx}`,
        tags: cfg.tags || []
      }))

      const { statSync } = await import('fs')
      const stats = statSync(this.configPath)
      this.mtime = Math.floor(stats.mtimeMs)
    } catch (error: any) {
      console.error('配置加载失败:', error.message)
      throw error
    }
  }

  async save(servers?: Server[]): Promise<void> {
    if (servers !== undefined) {
      this.servers = servers
    }

    const configDir = this.configPath.replace(/[^/\\]+$/, '')
    if (!existsSync(configDir)) {
      await mkdir(configDir, { recursive: true })
    }

    const configs = this.servers.map(s => ({
      host: s.host,
      port: s.port,
      user: s.user,
      name: s.name,
      tags: s.tags
    }))

    await writeFileAsync(this.configPath, JSON.stringify(configs, null, 2) + '\n', 'utf-8')
  }

  getAll(): Server[] {
    return [...this.servers]
  }

  getByTags(tags: string[]): Server[] {
    return this.servers.filter(s => tags.every(t => s.tags.includes(t)))
  }

  getById(id: string): Server | null {
    return this.servers.find(s => s.id === id) || null
  }

  getByHost(host: string): Server | null {
    return this.servers.find(s => s.host === host) || null
  }

  async add(config: SSHConfig): Promise<Server> {
    const server: Server = {
      id: getServerKey(config),
      host: config.host,
      port: config.port || 22,
      user: config.user || 'root',
      name: config.name,
      tags: config.tags || []
    }

    const existing = this.getByHost(server.host)
    if (existing) {
      const idx = this.servers.findIndex(s => s.host === server.host)
      if (idx >= 0) this.servers[idx] = server
    } else {
      this.servers.push(server)
    }

    await this.save()
    return server
  }

  async update(server: Server): Promise<void> {
    const idx = this.servers.findIndex(s => s.id === server.id)
    if (idx >= 0) {
      this.servers[idx] = server
      await this.save()
    }
  }

  async remove(host: string): Promise<boolean> {
    const idx = this.servers.findIndex(s => s.host === host)
    if (idx >= 0) {
      this.servers.splice(idx, 1)
      await this.save()
      return true
    }
    return false
  }

  async hotReload(): Promise<void> {
    await this.load()
  }

  stop(): void {}

  getConfigPath(): string {
    return this.configPath
  }

  get count(): number {
    return this.servers.length
  }
}