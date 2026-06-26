/**
 * SFTP文件传输工具
 * 
 * 提供文件上传、下载、目录操作等功能
 */

import SftpClient from 'ssh2-sftp-client'
import { ConnectionConfig, getSSHPool } from './ssh-pool.js'

export interface FileTransferOptions {
  localPath: string
  remotePath: string
  mode?: 'upload' | 'download'
}

export interface DirectoryOptions {
  path: string
  recursive?: boolean
}

/**
 * SFTP客户端封装
 */
export class SFTPManager {
  private pool: ReturnType<typeof getSSHPool>

  constructor() {
    this.pool = getSSHPool()
  }

  /**
   * 获取SFTP客户端
   */
  private async getSFTPClient(config: ConnectionConfig): Promise<SftpClient> {
    const client = await this.pool.getConnection(config)
    const sftp = new SftpClient()
    
    // 使用SSH连接创建SFTP会话
    // 注意：这里需要重新实现，因为ssh2-sftp-client需要自己的连接
    // 为了简化，我们创建新的SFTP连接
    await sftp.connect({
      host: config.host,
      port: config.port || 22,
      username: config.user || 'root',
      privateKey: config.keyFile ? require('fs').readFileSync(config.keyFile) : undefined,
      password: config.password,
      readyTimeout: 15000
    })
    
    return sftp
  }

  /**
   * 上传文件
   */
  async uploadFile(
    config: ConnectionConfig,
    localPath: string,
    remotePath: string
  ): Promise<void> {
    const sftp = await this.getSFTPClient(config)
    
    try {
      await sftp.fastPut(localPath, remotePath)
    } finally {
      await sftp.end()
    }
  }

  /**
   * 下载文件
   */
  async downloadFile(
    config: ConnectionConfig,
    remotePath: string,
    localPath: string
  ): Promise<void> {
    const sftp = await this.getSFTPClient(config)
    
    try {
      await sftp.fastGet(remotePath, localPath)
    } finally {
      await sftp.end()
    }
  }

  /**
   * 列出目录
   */
  async listDirectory(
    config: ConnectionConfig,
    remotePath: string
  ): Promise<any[]> {
    const sftp = await this.getSFTPClient(config)
    
    try {
      return await sftp.list(remotePath)
    } finally {
      await sftp.end()
    }
  }

  /**
   * 创建目录
   */
  async createDirectory(
    config: ConnectionConfig,
    remotePath: string,
    recursive: boolean = true
  ): Promise<void> {
    const sftp = await this.getSFTPClient(config)
    
    try {
      if (recursive) {
        await sftp.mkdir(remotePath, true)
      } else {
        await sftp.mkdir(remotePath)
      }
    } finally {
      await sftp.end()
    }
  }

  /**
   * 删除文件
   */
  async deleteFile(
    config: ConnectionConfig,
    remotePath: string
  ): Promise<void> {
    const sftp = await this.getSFTPClient(config)
    
    try {
      await sftp.delete(remotePath)
    } finally {
      await sftp.end()
    }
  }

  /**
   * 删除目录
   */
  async deleteDirectory(
    config: ConnectionConfig,
    remotePath: string,
    recursive: boolean = true
  ): Promise<void> {
    const sftp = await this.getSFTPClient(config)
    
    try {
      if (recursive) {
        await sftp.rmdir(remotePath, true)
      } else {
        await sftp.rmdir(remotePath)
      }
    } finally {
      await sftp.end()
    }
  }

  /**
   * 检查文件是否存在
   */
  async fileExists(
    config: ConnectionConfig,
    remotePath: string
  ): Promise<boolean> {
    const sftp = await this.getSFTPClient(config)
    
    try {
      try {
        await sftp.stat(remotePath)
        return true
      } catch (e) {
        return false
      }
    } finally {
      await sftp.end()
    }
  }

  /**
   * 获取文件信息
   */
  async getFileInfo(
    config: ConnectionConfig,
    remotePath: string
  ): Promise<any> {
    const sftp = await this.getSFTPClient(config)
    
    try {
      return await sftp.stat(remotePath)
    } finally {
      await sftp.end()
    }
  }
}

// 全局SFTP管理器实例
let globalSFTPManager: SFTPManager | null = null

/**
 * 获取全局SFTP管理器
 */
export function getSFTPManager(): SFTPManager {
  if (!globalSFTPManager) {
    globalSFTPManager = new SFTPManager()
  }
  return globalSFTPManager
}
