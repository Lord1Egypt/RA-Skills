/**
 * 凭据仓库实现
 * 从配置文件读取凭据（密码或密钥）
 *
 * 注意：为安全起见，密码建议存储在系统密钥环（如 macOS Keychain、Linux Secret Service）
 * 或环境变量中。本实现从配置文件读取（生产环境不推荐）。
 */

import { existsSync, readFileSync } from 'fs'
import type { Server, SSHCredentials, ICredentialsProvider } from '../../config/schemas'
import { ConfigManager } from '../../config/loader'

/**
 * 基于 ConfigManager 的凭据提供者
 *
 * 凭据存储方案（按优先级）：
 * 1. 环境变量: OPS_CRED_<HOST>={user:password} 或 OPS_CRED_<HOST>_KEY 文件路径
 * 2. 配置文件附加字段（不推荐生产使用）
 * 3. SSH 默认密钥 (~/.ssh/id_rsa)
 */
export class ConfigManagerCredentialsProvider implements ICredentialsProvider {
  constructor(private configManager: ConfigManager) {}

  /**
   * 获取服务器凭据
   */
  async getCredentials(server: Server): Promise<SSHCredentials | null> {
    // 方案1：从环境变量获取
    const envCred = this.getFromEnvironment(server)
    if (envCred) return envCred

    // 方案2：从配置文件获取（需要扩展配置文件支持密码存储）
    // 注意：生产环境应将密码存储在密钥环中
    const fileCred = await this.getFromConfigFile(server)
    if (fileCred) return fileCred

    // 方案3：尝试默认 SSH 密钥
    const defaultKey = this.getDefaultSSHKey()
    if (defaultKey) {
      return { keyFile: defaultKey }
    }

    return null
  }

  /**
   * 从环境变量读取凭据
   *
   * 格式：
   * - OPS_CRED_<HOST>="username:password" 或 OPS_CRED_<HOST>="password"
   * - OPS_KEY_<HOST>=/path/to/private/key
   *
   * 示例：
   * - OPS_CRED_10_119_120_143="salt:Giten!#202501Tab*&"
   * - OPS_KEY_10_119_120_143=/home/user/.ssh/id_rsa
   */
  private getFromEnvironment(server: Server): SSHCredentials | null {
    const hostKey = server.host.replace(/[.:]/g, '_') // 替换 . 和 :
    const passwordEnv = `OPS_CRED_${hostKey}`
    const keyEnv = `OPS_KEY_${hostKey}`

    // 尝试密码
    const passwordEnvValue = process.env[passwordEnv]
    if (passwordEnvValue) {
      // 格式可以是 "user:password" 或直接 "password"
      if (passwordEnvValue.includes(':')) {
        const [user, pass] = passwordEnvValue.split(':', 2)
        // 验证用户名
        if (user !== server.user) {
          console.warn(`环境变量 ${passwordEnv} 的用户名 ${user} 与配置的用户 ${server.user} 不匹配`)
        }
        return { password: pass }
      } else {
        return { password: passwordEnvValue }
      }
    }

    // 尝试密钥文件路径
    const keyFilePath = process.env[keyEnv]
    if (keyFilePath && existsSync(keyFilePath)) {
      return { keyFile: keyFilePath }
    }

    return null
  }

  /**
   * 从配置文件获取凭据（扩展方案）
   *
   * 服务器配置文件扩展格式：
   * {
   *   "host": "10.119.120.143",
   *   "user": "salt",
   *   "password": "xxxxx",  // 密码（生产环境不推荐）
   *   "keyFile": "/path/to/key", // 密钥路径
   *   "keyContent": "-----BEGIN...", // 密钥内容（base64）
   *   "name": "...",
   *   "tags": [...]
   * }
   */
  private async getFromConfigFile(server: Server): Promise<SSHCredentials | null> {
    // 读取原配置文件（包含敏感信息）
    // 实际使用时，配置文件应单独存储凭据（如 encrypted creds file）
    // 这里先返回 null，后续再实现
    return null
  }

  /**
   * 获取默认 SSH 密钥路径
   */
  private getDefaultSSHKey(): string | null {
    const home = process.env.HOME || process.env.USERPROFILE
    if (!home) return null

    const candidates = [
      join(home, '.ssh', 'id_rsa'),
      join(home, '.ssh', 'id_ed25519'),
      join(home, '.ssh', 'id_dsa'),
      join(home, '.ssh', 'id_ecdsa')
    ]

    for (const key of candidates) {
      if (existsSync(key)) {
        return key
      }
    }

    return null
  }

  /**
   * 保存凭据（运行时添加）
   */
  async setCredentials(server: Server, credentials: SSHCredentials): Promise<void> {
    // 这里可以实现运行时凭据缓存
    // 但不持久化到文件（避免安全风险）
    console.warn('注意：运行时设置的凭据不会持久化，进程重启后需重新配置')
  }
}

/**
 * 环境变量凭据提供者（最安全）
 * 所有凭据通过环境变量注入，不存储在文件中
 */
export class EnvironmentCredentialsProvider implements ICredentialsProvider {
  async getCredentials(server: Server): Promise<SSHCredentials | null> {
    return this.loadFromEnvironment(server)
  }

  async setCredentials(server: Server, credentials: SSHCredentials): Promise<void> {
    throw new Error('环境变量凭据提供者不支持写入，请使用 export 命令设置环境变量')
  }

  private getFromEnvironment(server: Server): SSHCredentials | null {
    const hostKey = server.host.replace(/[.:]/g, '_')
    const passwordEnv = `OPS_CRED_${hostKey}`
    const keyEnv = `OPS_KEY_${hostKey}`

    const passwordEnvValue = process.env[passwordEnv]
    if (passwordEnvValue) {
      if (passwordEnvValue.includes(':')) {
        const [, pass] = passwordEnvValue.split(':', 2)
        return { password: pass }
      }
      return { password: passwordEnvValue }
    }

    const keyFilePath = process.env[keyEnv]
    if (keyFilePath && existsSync(keyFilePath)) {
      return { keyFile: keyFilePath }
    }

    return null
  }
}

// 辅助函数
function join(...paths: string[]): string {
  return paths.join('/').replace(/\\/g, '/')
}