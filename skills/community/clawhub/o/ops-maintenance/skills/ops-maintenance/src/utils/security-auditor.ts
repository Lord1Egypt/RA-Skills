/**
 * 安全审计器 v3.0
 *
 * 自动检查系统安全配置
 * 支持: SSH/防火墙/文件权限/Docker/内核参数
 */

import { exec } from 'child_process'
import { promisify } from 'util'
import { existsSync, readFileSync, statSync } from 'fs'
import { getAuditLogger } from './audit-logger.js'

const execAsync = promisify(exec)

// ============================================================
// 类型定义
// ============================================================

export type SecuritySeverity = 'high' | 'medium' | 'low'
export type SecurityCategory = 'ssh' | 'firewall' | 'permissions' | 'docker' | 'kernel' | 'general'

export interface SecurityFinding {
  category: SecurityCategory
  severity: SecuritySeverity
  title: string
  description: string
  remediation: string
  current?: string
  expected?: string
  autoFixable: boolean
}

// ============================================================
// 安全审计器
// ============================================================

export class SecurityAuditor {
  private timeout: number

  constructor(timeout: number = 15000) {
    this.timeout = timeout
  }

  /**
   * 执行所有安全检查
   */
  async runAllChecks(): Promise<SecurityFinding[]> {
    const findings: SecurityFinding[] = []

    const checks = [
      () => this.checkSSH(),
      () => this.checkFirewall(),
      () => this.checkFilePermissions(),
      () => this.checkDockerSecurity(),
      () => this.checkKernelParams(),
    ]

    for (const check of checks) {
      try {
        const results = await check()
        findings.push(...results)
      } catch (error: any) {
        findings.push({
          category: 'general',
          severity: 'medium',
          title: '检查执行失败',
          description: error.message,
          remediation: '检查工具是否可用',
          autoFixable: false,
        })
      }
    }

    const audit = getAuditLogger()
    audit.logSuccess('security_audit', 'local', undefined, undefined, {
      findingsCount: findings.length,
      highCount: findings.filter(f => f.severity === 'high').length,
    })

    return findings
  }

  // ----------------------------------------------------------
  // SSH 安全检查
  // ----------------------------------------------------------

  private async checkSSH(): Promise<SecurityFinding[]> {
    const findings: SecurityFinding[] = []
    const sshdConfigPath = '/etc/ssh/sshd_config'

    if (!existsSync(sshdConfigPath)) {
      // macOS 可能用不同路径
      if (process.platform === 'darwin') {
        return findings // macOS不适用此检查
      }
      findings.push({
        category: 'ssh',
        severity: 'medium',
        title: 'SSH配置文件不存在',
        description: '未找到sshd_config文件',
        remediation: '安装并配置OpenSSH',
        autoFixable: false,
      })
      return findings
    }

    try {
      const config = readFileSync(sshdConfigPath, 'utf-8')

      // 检查PermitRootLogin
      const rootLoginMatch = config.match(/^PermitRootLogin\s+(\S+)/m)
      if (!rootLoginMatch || rootLoginMatch[1] === 'yes') {
        findings.push({
          category: 'ssh',
          severity: 'high',
          title: '允许Root登录',
          description: 'SSH允许root直接登录，存在暴力破解风险',
          remediation: '设置 PermitRootLogin no 或 PermitRootLogin prohibit-password',
          current: rootLoginMatch ? rootLoginMatch[1] : 'yes(默认)',
          expected: 'no 或 prohibit-password',
          autoFixable: true,
        })
      }

      // 检查PasswordAuthentication
      const passwordAuthMatch = config.match(/^PasswordAuthentication\s+(\S+)/m)
      if (!passwordAuthMatch || passwordAuthMatch[1] === 'yes') {
        findings.push({
          category: 'ssh',
          severity: 'high',
          title: '允许密码认证',
          description: 'SSH允许密码登录，容易被暴力破解',
          remediation: '设置 PasswordAuthentication no，使用密钥认证',
          current: passwordAuthMatch ? passwordAuthMatch[1] : 'yes(默认)',
          expected: 'no',
          autoFixable: true,
        })
      }

      // 检查PermitEmptyPasswords
      const emptyPwMatch = config.match(/^PermitEmptyPasswords\s+(\S+)/m)
      if (!emptyPwMatch || emptyPwMatch[1] === 'yes') {
        findings.push({
          category: 'ssh',
          severity: 'high',
          title: '允许空密码',
          description: 'SSH允许空密码登录',
          remediation: '设置 PermitEmptyPasswords no',
          current: emptyPwMatch ? emptyPwMatch[1] : '未设置',
          expected: 'no',
          autoFixable: true,
        })
      }

      // 检查SSH端口
      const portMatch = config.match(/^Port\s+(\S+)/m)
      if (portMatch && portMatch[1] === '22') {
        findings.push({
          category: 'ssh',
          severity: 'medium',
          title: '使用默认SSH端口',
          description: 'SSH使用默认端口22，容易被扫描发现',
          remediation: '修改为非标准端口(如2222)',
          current: '22',
          expected: '非标准端口',
          autoFixable: true,
        })
      }

      // 检查X11Forwarding
      const x11Match = config.match(/^X11Forwarding\s+(\S+)/m)
      if (x11Match && x11Match[1] === 'yes') {
        findings.push({
          category: 'ssh',
          severity: 'low',
          title: '启用X11转发',
          description: 'SSH启用了X11转发，可能增加攻击面',
          remediation: '设置 X11Forwarding no',
          current: 'yes',
          expected: 'no',
          autoFixable: true,
        })
      }

    } catch (error: any) {
      findings.push({
        category: 'ssh',
        severity: 'low',
        title: 'SSH配置读取失败',
        description: error.message,
        remediation: '检查文件权限',
        autoFixable: false,
      })
    }

    return findings
  }

  // ----------------------------------------------------------
  // 防火墙检查
  // ----------------------------------------------------------

  private async checkFirewall(): Promise<SecurityFinding[]> {
    const findings: SecurityFinding[] = []

    try {
      if (process.platform === 'darwin') {
        // macOS: 检查pf或ALF
        const { stdout: alfStatus } = await execAsync(
          '/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate 2>/dev/null || echo "N/A"',
          { timeout: 5000 }
        )

        if (alfStatus.includes('disabled') || alfStatus.includes('off')) {
          findings.push({
            category: 'firewall',
            severity: 'high',
            title: 'macOS防火墙未启用',
            description: '应用防火墙(Application Firewall)处于关闭状态',
            remediation: '系统偏好设置 > 安全性 > 防火墙 > 打开',
            autoFixable: false,
          })
        }
      } else {
        // Linux: 检查iptables/ufw/firewalld
        let firewallActive = false

        // UFW
        try {
          const { stdout } = await execAsync('ufw status 2>/dev/null', { timeout: 5000 })
          if (stdout.includes('active')) {
            firewallActive = true
          } else if (stdout.includes('inactive')) {
            findings.push({
              category: 'firewall',
              severity: 'high',
              title: 'UFW防火墙未启用',
              description: 'UFW防火墙处于禁用状态',
              remediation: '执行 ufw enable',
              autoFixable: true,
            })
          }
        } catch { /* UFW not installed */ }

        // firewalld
        if (!firewallActive) {
          try {
            const { stdout } = await execAsync('firewall-cmd --state 2>/dev/null', { timeout: 5000 })
            if (stdout.includes('running')) {
              firewallActive = true
            }
          } catch { /* firewalld not running */ }
        }

        // iptables
        if (!firewallActive) {
          try {
            const { stdout } = await execAsync('iptables -L 2>/dev/null | wc -l', { timeout: 5000 })
            const lineCount = parseInt(stdout.trim())
            if (lineCount <= 3) {
              findings.push({
                category: 'firewall',
                severity: 'high',
                title: '无防火墙规则',
                description: 'iptables无规则，系统完全暴露',
                remediation: '配置iptables规则或启用ufw/firewalld',
                autoFixable: false,
              })
            }
          } catch { /* iptables not available */ }
        }
      }
    } catch (error: any) {
      findings.push({
        category: 'firewall',
        severity: 'medium',
        title: '防火墙检查失败',
        description: error.message,
        remediation: '手动检查防火墙状态',
        autoFixable: false,
      })
    }

    return findings
  }

  // ----------------------------------------------------------
  // 文件权限检查
  // ----------------------------------------------------------

  private async checkFilePermissions(): Promise<SecurityFinding[]> {
    const findings: SecurityFinding[] = []

    const criticalFiles = [
      { path: '/etc/shadow', expectedMode: '640', desc: '密码文件' },
      { path: '/etc/ssh/sshd_config', expectedMode: '600', desc: 'SSH配置' },
      { path: '/etc/gshadow', expectedMode: '640', desc: '组密码文件' },
    ]

    for (const file of criticalFiles) {
      if (existsSync(file.path)) {
        try {
          const stat = statSync(file.path)
          const mode = (stat.mode & 0o777).toString(8)

          // 检查是否过于开放
          if (mode !== file.expectedMode && parseInt(mode) > parseInt(file.expectedMode)) {
            findings.push({
              category: 'permissions',
              severity: parseInt(mode) > 640 ? 'high' : 'medium',
              title: `${file.desc}权限过于开放`,
              description: `${file.path} 权限为 ${mode}，应为 ${file.expectedMode}`,
              remediation: `chmod ${file.expectedMode} ${file.path}`,
              current: mode,
              expected: file.expectedMode,
              autoFixable: true,
            })
          }
        } catch { /* skip */ }
      }
    }

    // 检查SSH密钥权限
    const sshDir = `${process.env.HOME}/.ssh`
    if (existsSync(sshDir)) {
      try {
        const idRsa = `${sshDir}/id_rsa`
        if (existsSync(idRsa)) {
          const stat = statSync(idRsa)
          const mode = (stat.mode & 0o777).toString(8)
          if (mode !== '600') {
            findings.push({
              category: 'permissions',
              severity: 'high',
              title: 'SSH私钥权限不安全',
              description: `私钥 ${idRsa} 权限为 ${mode}，应为 600`,
              remediation: `chmod 600 ${idRsa}`,
              current: mode,
              expected: '600',
              autoFixable: true,
            })
          }
        }
      } catch { /* skip */ }
    }

    return findings
  }

  // ----------------------------------------------------------
  // Docker 安全检查
  // ----------------------------------------------------------

  private async checkDockerSecurity(): Promise<SecurityFinding[]> {
    const findings: SecurityFinding[] = []

    try {
      // 检查Docker是否运行
      const { stdout: dockerInfo } = await execAsync('docker info --format "{{.SecurityOptions}}" 2>/dev/null || echo "N/A"', {
        timeout: 5000,
      })

      if (dockerInfo.trim() === 'N/A' || dockerInfo.includes('Cannot connect')) {
        return findings // Docker未运行，跳过
      }

      // 检查是否以root运行Docker
      try {
        const { stdout: dockerSock } = await execAsync('ls -la /var/run/docker.sock 2>/dev/null', { timeout: 5000 })
        if (dockerSock.includes('srw') && dockerSock.includes('root')) {
          findings.push({
            category: 'docker',
            severity: 'medium',
            title: 'Docker socket权限较宽',
            description: 'Docker socket可被root组访问，普通用户加入docker组等同root',
            remediation: '限制docker组访问，或使用rootless docker',
            autoFixable: false,
          })
        }
      } catch { /* skip */ }

      // 检查是否有特权容器
      try {
        const { stdout: containers } = await execAsync(
          'docker ps --format "{{.Names}} {{.ID}}" 2>/dev/null',
          { timeout: 5000 }
        )

        for (const line of containers.trim().split('\n').filter(l => l.trim())) {
          const [name, id] = line.trim().split(/\s+/)
          try {
            const { stdout: inspect } = await execAsync(
              `docker inspect --format "{{.HostConfig.Privileged}}" ${id} 2>/dev/null`,
              { timeout: 5000 }
            )
            if (inspect.trim() === 'true') {
              findings.push({
                category: 'docker',
                severity: 'high',
                title: `特权容器: ${name}`,
                description: `容器 ${name} 以特权模式运行，拥有宿主机全部权限`,
                remediation: `移除 --privileged 标志，使用 --cap-add 指定所需能力`,
                autoFixable: false,
              })
            }
          } catch { /* skip */ }
        }
      } catch { /* no containers */ }

    } catch { /* Docker not available */ }

    return findings
  }

  // ----------------------------------------------------------
  // 内核参数检查
  // ----------------------------------------------------------

  private async checkKernelParams(): Promise<SecurityFinding[]> {
    const findings: SecurityFinding[] = []

    if (process.platform === 'darwin') {
      return findings // macOS 不适用 sysctl 安全检查
    }

    const securityParams = [
      { key: 'net.ipv4.ip_forward', expected: '0', desc: 'IP转发', severity: 'high' as SecuritySeverity },
      { key: 'net.ipv4.conf.all.send_redirects', expected: '0', desc: 'ICMP重定向', severity: 'medium' as SecuritySeverity },
      { key: 'net.ipv4.conf.all.accept_redirects', expected: '0', desc: '接受ICMP重定向', severity: 'medium' as SecuritySeverity },
      { key: 'net.ipv4.conf.all.log_martians', expected: '1', desc: '记录可疑包', severity: 'low' as SecuritySeverity },
      { key: 'kernel.randomize_va_space', expected: '2', desc: 'ASLR地址随机化', severity: 'high' as SecuritySeverity },
    ]

    for (const param of securityParams) {
      try {
        const { stdout } = await execAsync(`sysctl -n ${param.key} 2>/dev/null || echo "N/A"`, {
          timeout: 5000,
        })
        const value = stdout.trim()

        if (value === 'N/A') continue

        if (value !== param.expected) {
          findings.push({
            category: 'kernel',
            severity: param.severity,
            title: `${param.desc}配置不安全`,
            description: `内核参数 ${param.key} = ${value}，应为 ${param.expected}`,
            remediation: `sysctl -w ${param.key}=${param.expected}`,
            current: value,
            expected: param.expected,
            autoFixable: true,
          })
        }
      } catch { /* param not found */ }
    }

    return findings
  }

  // ----------------------------------------------------------
  // 格式化输出
  // ----------------------------------------------------------

  formatFindings(findings: SecurityFinding[]): string {
    if (findings.length === 0) {
      return '### 🔒 安全审计\n\n✅ 未发现安全问题'
    }

    const lines: string[] = []
    lines.push('### 🔒 安全审计\n')

    // 按严重程度分组
    const high = findings.filter(f => f.severity === 'high')
    const medium = findings.filter(f => f.severity === 'medium')
    const low = findings.filter(f => f.severity === 'low')

    lines.push(`**发现**: 🔴 ${high.length} 高危 | ⚠️ ${medium.length} 中危 | ℹ️ ${low.length} 低危\n`)

    if (high.length > 0) {
      lines.push('#### 🔴 高危发现')
      for (const f of high) {
        lines.push(`- **[${f.category}] ${f.title}**`)
        lines.push(`  ${f.description}`)
        lines.push(`  修复: \`${f.remediation}\``)
        lines.push('')
      }
    }

    if (medium.length > 0) {
      lines.push('#### ⚠️ 中危发现')
      for (const f of medium) {
        lines.push(`- **[${f.category}] ${f.title}**`)
        lines.push(`  修复: \`${f.remediation}\``)
      }
      lines.push('')
    }

    if (low.length > 0) {
      lines.push('#### ℹ️ 低危发现')
      for (const f of low) {
        lines.push(`- [${f.category}] ${f.title}`)
      }
    }

    return lines.join('\n')
  }
}

// ============================================================
// 全局单例
// ============================================================

let globalSecurityAuditor: SecurityAuditor | null = null

export function getSecurityAuditor(): SecurityAuditor {
  if (!globalSecurityAuditor) {
    globalSecurityAuditor = new SecurityAuditor()
  }
  return globalSecurityAuditor
}
