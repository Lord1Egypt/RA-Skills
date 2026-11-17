/**
 * 密码过期检查用例
 */

import type {
  Server,
  PasswordUserInfo,
  IServerRepository,
  ISSHClient
} from '../config/schemas'

/**
 * 密码检查结果
 */
export interface PasswordCheckResult {
  server: string
  status: 'ok' | 'warning' | 'critical'
  details: string
  users: PasswordUserInfo[]
}

/**
 * 密码过期检查用例
 */
export class PasswordCheckUseCase {
  constructor(
    private serverRepo: IServerRepository,
    private ssh: ISSHClient
  ) {}

  /**
   * 执行密码过期检查
   */
  async execute(tags?: string[]): Promise<PasswordCheckResult[]> {
    const servers = await this.resolveServers(tags)
    const results: PasswordCheckResult[] = []

    for (const server of servers) {
      try {
        const userInfos = await this.checkServerPasswords(server)
        const { status, details } = this.evaluateServerStatus(userInfos)

        results.push({
          server: server.name || server.host,
          status,
          details,
          users: userInfos
        })
      } catch (error: any) {
        results.push({
          server: server.name || server.host,
          status: 'critical',
          details: `连接失败: ${error.message}`,
          users: []
        })
      }
    }

    return results
  }

  /**
   * 检查单台服务器的密码
   */
  private async checkServerPasswords(server: Server): Promise<PasswordUserInfo[]> {
    // 1. 获取有密码的用户列表
    const usersOutput = await this.ssh.execute(server, 'cat /etc/shadow 2>/dev/null | cut -d: -f1 | grep -v "^[$!*]$" | head -20')
    const users = usersOutput.trim().split('\n').filter(u => u.trim())

    if (users.length === 0) {
      return []
    }

    // 2. 检查每个用户的密码过期信息
    const userInfos: PasswordUserInfo[] = []
    for (const user of users) {
      const info = await this.getUserPasswordInfo(server, user.trim())
      if (info) {
        userInfos.push(info)
      }
    }

    return userInfos
  }

  /**
   * 获取单个用户的密码信息
   */
  private async getUserPasswordInfo(server: Server, username: string): Promise<PasswordUserInfo | null> {
    try {
      const output = await this.ssh.execute(server, `chage -l "${username}" 2>/dev/null`)

      const lastChanged = this.extractValue(output, /Last password change\s*:\s*(.+)/)
      const expires = this.extractValue(output, /Password expires\s*:\s*(.+)/)
      const maxDays = this.extractValue(output, /Maximum number of days between password change\s*:\s*(.+)/)

      let status = '✅ 有效'
      let daysLeft: number | undefined

      if (expires === 'never') {
        status = '⚠️ 永不过期'
      } else if (expires !== '-') {
        try {
          const expDate = new Date(expires)
          const now = new Date()
          daysLeft = Math.ceil((expDate.getTime() - now.getTime()) / (1000 * 60 * 60 * 24))

          if (daysLeft < 0) {
            status = '❌ 已过期'
          } else if (daysLeft <= 7) {
            status = '⚠️ 即将过期'
          }
        } catch {
          status = '❌ 检查失败'
        }
      }

      return {
        user: username,
        lastChanged,
        expires,
        maxDays,
        status,
        daysLeft
      }
    } catch {
      return null
    }
  }

  /**
   * 从 chage 输出中提取值
   */
  private extractValue(output: string, regex: RegExp): string {
    const match = output.match(regex)
    return match ? match[1].trim() : '-'
  }

  /**
   * 评估服务器整体状态
   */
  private evaluateServerStatus(users: PasswordUserInfo[]): { status: string; details: string } {
    if (users.length === 0) {
      return { status: 'ok', details: '无密码用户' }
    }

    const expired = users.filter(u => u.status.includes('已过期'))
    const warning = users.filter(u => u.status.includes('即将过期'))

    if (expired.length > 0) {
      return {
        status: 'critical',
        details: `${expired.length} 个用户密码已过期: ${expired.map(u => u.user).join(', ')}`
      }
    }

    if (warning.length > 0) {
      return {
        status: 'warning',
        details: `${warning.length} 个用户即将过期: ${warning.map(u => `${u.user}(${u.daysLeft}天)`).join(', ')}`
      }
    }

    return { status: 'ok', details: `共 ${users.length} 个用户，密码状态正常` }
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
}