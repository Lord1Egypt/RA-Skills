/**
 * 磁盘检查用例
 */

import type { Server, IServerRepository, ISSHClient } from '../config/schemas'

/**
 * 磁盘使用信息
 */
export interface DiskInfo {
  server: string
  total: number
  used: number
  available: number
  mountPoint: string
  usagePercent: number
  largeDirectories?: Array<{
    path: string
    size: number
  }>
}

/**
 * 磁盘检查用例
 */
export class DiskCheckUseCase {
  constructor(
    private serverRepo: IServerRepository,
    private ssh: ISSHClient
  ) {}

  /**
   * 执行磁盘检查
   */
  async execute(tags?: string[]): Promise<DiskInfo[]> {
    const servers = await this.resolveServers(tags)
    const results: DiskInfo[] = []

    for (const server of servers) {
      try {
        const diskInfo = await this.checkServerDisk(server)
        results.push(diskInfo)
      } catch (error: any) {
        results.push({
          server: server.name || server.host,
          total: 0,
          used: 0,
          available: 0,
          mountPoint: '/',
          usagePercent: 0,
          largeDirectories: []
        })
      }
    }

    return results
  }

  /**
   * 检查单台服务器磁盘
   */
  private async checkServerDisk(server: Server): Promise<DiskInfo> {
    // 1. 获取根分区信息
    const dfOutput = await this.ssh.execute(server, 'df -k / 2>/dev/null | tail -1')
    const parts = dfOutput.trim().split(/\s+/)

    if (parts.length < 6) {
      throw new Error('磁盘信息解析失败')
    }

    const totalKb = parseInt(parts[1])
    const usedKb = parseInt(parts[2])
    const availKb = parseInt(parts[3])
    const usagePercent = parseFloat(parts[4].replace('%', ''))
    const mountPoint = parts[5]

    // 2. 获取大目录列表（可选，较耗时）
    let largeDirectories: Array<{ path: string; size: number }> = []
    try {
      const duOutput = await this.ssh.execute(server, 'du -k /* 2>/dev/null | sort -rn | head -10')
      const lines = duOutput.trim().split('\n')
      largeDirectories = lines.slice(0, 10).map(line => {
        const [sizeKb, ...pathParts] = line.trim().split(/\s+/)
        return {
          path: pathParts.join(' '),
          size: parseInt(sizeKb) * 1024 // 转换为字节
        }
      }).filter(d => d.size > 0)
    } catch {
      // 忽略大目录检查失败
    }

    return {
      server: server.name || server.host,
      total: totalKb * 1024,
      used: usedKb * 1024,
      available: availKb * 1024,
      mountPoint,
      usagePercent,
      largeDirectories
    }
  }

  /**
   * 解析服务器列表
   */
  private async resolveServers(tags?: string[]): Promise<Server[]> {
    if (tags && tags.length > 0) {
      return this.serverRepo.findByTags(tags)
    }
    return this.serverRepo.findAll()
  }

  /**
   * 识别需要清理的大目录
   */
  analyzeLargeDirectories(dirs: Array<{ path: string; size: number }>): Array<{ path: string; size: string; suggestion: string }> {
    const suggestions = dirs.map(dir => {
      let sizeStr = this.formatBytes(dir.size)
      let suggestion = ''

      // 根据目录路径提供清理建议
      if (dir.path.includes('/var/log')) {
        suggestion = '清理或归档日志文件'
      } else if (dir.path.includes('/tmp')) {
        suggestion = '删除临时文件'
      } else if (dir.path.includes('/home')) {
        suggestion = '检查用户文件或备份'
      } else if (dir.path.includes('/docker')) {
        suggestion = '清理未使用的镜像和容器'
      } else {
        suggestion = '检查并清理不再需要的文件'
      }

      return {
        path: dir.path,
        size: sizeStr,
        suggestion
      }
    })

    return suggestions.sort((a, b) => {
      // 按大小排序（简单处理）
      return 0
    })
  }

  /**
   * 格式化字节
   */
  private formatBytes(bytes: number): string {
    if (bytes >= 1073741824) {
      return `${(bytes / 1073741824).toFixed(1)}GB`
    } else if (bytes >= 1048576) {
      return `${(bytes / 1048576).toFixed(1)}MB`
    } else if (bytes >= 1024) {
      return `${(bytes / 1024).toFixed(1)}KB`
    }
    return `${bytes}B`
  }
}