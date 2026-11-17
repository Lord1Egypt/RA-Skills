/**
 * 密码加密/解密工具
 * 
 * 使用AES-256-GCM加密敏感信息（如SSH密码）
 */

import { createCipheriv, createDecipheriv, randomBytes, scrypt } from 'crypto'
import { readFile, writeFile } from 'fs/promises'
import { join } from 'path'
import { existsSync } from 'fs'

/**
 * 加密密钥文件路径
 */
function getKeyPath(): string {
  return join(process.env.HOME || '~', '.config/ops-maintenance/.key')
}

/**
 * 配置目录
 */
function getConfigDir(): string {
  return join(process.env.HOME || '~', '.config/ops-maintenance')
}

/**
 * 生成或加载加密密钥
 */
async function getOrGenerateKey(): Promise<Buffer> {
  const keyPath = getKeyPath()
  const configDir = getConfigDir()

  // 确保目录存在
  if (!existsSync(configDir)) {
    await writeFile(configDir, '')
  }

  // 尝试加载现有密钥
  if (existsSync(keyPath)) {
    try {
      const keyData = await readFile(keyPath)
      return keyData
    } catch (e) {
      // 忽略错误，生成新密钥
    }
  }

  // 生成新密钥（32字节 = 256位）
  const key = randomBytes(32)
  await writeFile(keyPath, key, { mode: 0o600 }) // 仅用户可读写

  return key
}

/**
 * 加密文本
 */
export async function encrypt(text: string): Promise<string> {
  const key = await getOrGenerateKey()
  const iv = randomBytes(16) // 初始化向量
  const cipher = createCipheriv('aes-256-gcm', key, iv)

  let encrypted = cipher.update(text, 'utf8', 'hex')
  encrypted += cipher.final('hex')

  const authTag = cipher.getAuthTag()

  // 格式: iv:authTag:encrypted
  return `${iv.toString('hex')}:${authTag.toString('hex')}:${encrypted}`
}

/**
 * 解密文本
 */
export async function decrypt(encryptedText: string): Promise<string> {
  const key = await getOrGenerateKey()
  const parts = encryptedText.split(':')

  if (parts.length !== 3) {
    throw new Error('无效的加密格式')
  }

  const iv = Buffer.from(parts[0], 'hex')
  const authTag = Buffer.from(parts[1], 'hex')
  const encrypted = parts[2]

  const decipher = createDecipheriv('aes-256-gcm', key, iv)
  decipher.setAuthTag(authTag)

  let decrypted = decipher.update(encrypted, 'hex', 'utf8')
  decrypted += decipher.final('utf8')

  return decrypted
}

/**
 * 检查密码是否已加密
 */
export function isEncrypted(text: string): boolean {
  // 加密格式: hex:hex:hex
  const parts = text.split(':')
  if (parts.length !== 3) return false

  // 检查每部分是否为有效的hex
  return parts.every(part => /^[0-9a-fA-F]+$/.test(part))
}

/**
 * 安全地保存服务器配置（自动加密密码）
 */
export async function saveServersSecurely(servers: any[]): Promise<void> {
  const configDir = getConfigDir()
  const configPath = join(configDir, 'servers.json')

  // 加密所有密码
  const encryptedServers = await Promise.all(
    servers.map(async (server) => {
      const encrypted = { ...server }
      if (server.password && !isEncrypted(server.password)) {
        encrypted.password = await encrypt(server.password)
      }
      return encrypted
    })
  )

  await writeFile(configPath, JSON.stringify(encryptedServers, null, 2), { mode: 0o600 })
}

/**
 * 加载服务器配置（自动解密密码）
 */
export async function loadServersSecurely(): Promise<any[]> {
  const configPath = join(getConfigDir(), 'servers.json')

  try {
    const content = await readFile(configPath, 'utf8')
    const servers = JSON.parse(content)

    // 解密所有密码
    const decryptedServers = await Promise.all(
      servers.map(async (server: any) => {
        const decrypted = { ...server }
        if (server.password && isEncrypted(server.password)) {
          try {
            decrypted.password = await decrypt(server.password)
          } catch (e) {
            // 解密失败，保持原样
            console.warn(`警告: 无法解密服务器 ${server.host} 的密码`)
          }
        }
        return decrypted
      })
    )

    return decryptedServers
  } catch {
    return []
  }
}
