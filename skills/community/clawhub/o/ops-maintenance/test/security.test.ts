/**
 * 安全功能测试
 * 
 * 测试 ops-maintenance v2.1 的安全改进功能
 */


import { 
  encrypt, 
  decrypt, 
  isEncrypted,
  saveServersSecurely,
  loadServersSecurely
} from '../skills/ops-maintenance/src/utils/crypto'
import { 
  validateCommand, 
  validateCommands 
} from '../skills/ops-maintenance/src/utils/command-validator'
import { getSSHPool } from '../skills/ops-maintenance/src/utils/ssh-pool'

describe('密码加密功能', () => {
  it('应该成功加密密码', async () => {
    const password = 'test-password-123'
    const encrypted = await encrypt(password)
    
    expect(encrypted).toBeDefined()
    expect(encrypted).not.toBe(password)
    expect(isEncrypted(encrypted)).toBe(true)
  })

  it('应该成功解密密码', async () => {
    const password = 'test-password-123'
    const encrypted = await encrypt(password)
    const decrypted = await decrypt(encrypted)
    
    expect(decrypted).toBe(password)
  })

  it('应该检测加密格式', () => {
    expect(isEncrypted('abc123:def456:789012')).toBe(true)
    expect(isEncrypted('plain-text')).toBe(false)
    expect(isEncrypted('')).toBe(false)
  })

  it('应该拒绝无效的加密格式', async () => {
    await expect(decrypt('invalid-format')).rejects.toThrow()
  })
})

describe('命令验证功能', () => {
  describe('允许的命令', () => {
    it('应该允许系统信息命令', () => {
      expect(validateCommand('uptime').safe).toBe(true)
      expect(validateCommand('free -h').safe).toBe(true)
      expect(validateCommand('df -h').safe).toBe(true)
      expect(validateCommand('ps aux').safe).toBe(true)
    })

    it('应该允许日志查看命令', () => {
      expect(validateCommand('tail -n 100 /var/log/syslog').safe).toBe(true)
      expect(validateCommand('cat /var/log/messages').safe).toBe(true)
    })

    it('应该允许网络命令', () => {
      expect(validateCommand('ping -c 4 google.com').safe).toBe(true)
      
    })
  })

  describe('禁止的命令', () => {
    it('应该禁止删除命令', () => {
      expect(validateCommand('rm -rf /').safe).toBe(false)
      expect(validateCommand('del file.txt').safe).toBe(false)
    })

    it('应该禁止修改系统命令', () => {
      expect(validateCommand('chmod 777 /etc/passwd').safe).toBe(false)
      expect(validateCommand('useradd test').safe).toBe(false)
    })

    it('应该禁止系统关机命令', () => {
      expect(validateCommand('shutdown -h now').safe).toBe(false)
      expect(validateCommand('reboot').safe).toBe(false)
    })
  })
})
