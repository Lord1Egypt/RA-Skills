/**
 * SSL 证书监控器 v1.0
 *
 * 自动检测域名 SSL/TLS 证书过期时间
 * 支持: 单域名/批量域名检测、提前告警、证书详情、链路检查
 */

import { exec } from 'child_process'
import { promisify } from 'util'
import * as tls from 'tls'
import * as https from 'https'
import { getAuditLogger } from './audit-logger.js'

const execAsync = promisify(exec)

// ============================================================
// 类型定义
// ============================================================

export type CertStatus = 'valid' | 'expiring-soon' | 'expired' | 'error'

export interface CertInfo {
  domain: string
  port: number
  status: CertStatus
  issuer: string
  subject: string
  validFrom: string
  validTo: string
  daysRemaining: number
  protocol: string
  fingerprint?: string
  sanDomains: string[]
  error?: string
}

export interface SSLCheckResult {
  domain: string
  port: number
  status: CertStatus
  cert?: CertInfo
  chainIssues: string[]
  error?: string
}

export interface SSLMonitorReport {
  timestamp: string
  totalChecked: number
  valid: number
  expiringSoon: number
  expired: number
  errors: number
  results: SSLCheckResult[]
  summary: string
}

export interface SSLMonitorConfig {
  domains: string[]
  warnDays: number      // 提前N天告警
  criticalDays: number  // 提前N天严重告警
  timeout: number
  ports?: Record<string, number>  // 指定域名的端口，默认443
}

// ============================================================
// SSL 证书监控器
// ============================================================

export class SSLMonitor {
  private config: SSLMonitorConfig

  constructor(config?: Partial<SSLMonitorConfig>) {
    this.config = {
      domains: config?.domains || [],
      warnDays: config?.warnDays || 30,
      criticalDays: config?.criticalDays || 7,
      timeout: config?.timeout || 10000,
      ports: config?.ports || {}
    }
  }

  /**
   * 检查单个域名的 SSL 证书
   */
  async checkDomain(domain: string, port?: number): Promise<SSLCheckResult> {
    const targetPort = port || this.config.ports?.[domain] || 443
    const chainIssues: string[] = []

    try {
      const certInfo = await this.fetchCertInfo(domain, targetPort)

      // 判断状态
      let status: CertStatus = 'valid'
      if (certInfo.daysRemaining <= 0) {
        status = 'expired'
      } else if (certInfo.daysRemaining <= this.config.criticalDays) {
        status = 'expiring-soon'
      } else if (certInfo.daysRemaining <= this.config.warnDays) {
        status = 'expiring-soon'
      }

      // 检查 SAN 域名是否包含目标域名
      if (certInfo.sanDomains.length > 0) {
        const domainMatch = certInfo.sanDomains.some(san =>
          san === domain || san === `*.${domain.split('.').slice(1).join('.')}`
        )
        if (!domainMatch && certInfo.subject !== domain) {
          chainIssues.push(`证书SAN不包含 ${domain}`)
        }
      }

      // 检查协议版本
      if (certInfo.protocol === 'TLSv1' || certInfo.protocol === 'TLSv1.1') {
        chainIssues.push(`使用不安全协议: ${certInfo.protocol}，建议升级到TLSv1.2+`)
      }

      return { domain, port: targetPort, status, cert: certInfo, chainIssues: [], error: undefined }
    } catch (error: any) {
      return {
        domain, port: targetPort,
        status: 'error' as CertStatus,
        chainIssues: [],
        error: error.message
      }
    }
  }

  /**
   * 批量检查多个域名
   */
  async checkDomains(domains?: string[]): Promise<SSLMonitorReport> {
    const targetDomains = domains || this.config.domains

    if (targetDomains.length === 0) {
      return {
        timestamp: new Date().toISOString(),
        totalChecked: 0, valid: 0, expiringSoon: 0, expired: 0, errors: 0,
        results: [],
        summary: '未指定检查域名'
      }
    }

    const results: SSLCheckResult[] = []

    // 并发检查（最多5个并发）
    const batchSize = 5
    for (let i = 0; i < targetDomains.length; i += batchSize) {
      const batch = targetDomains.slice(i, i + batchSize)
      const batchResults = await Promise.all(
        batch.map(d => this.checkDomain(d))
      )
      results.push(...batchResults)
    }

    // 统计
    const valid = results.filter(r => r.status === 'valid').length
    const expiringSoon = results.filter(r => r.status === 'expiring-soon').length
    const expired = results.filter(r => r.status === 'expired').length
    const errors = results.filter(r => r.status === 'error').length

    // 审计日志
    const logger = getAuditLogger()
    logger.log('ssl-monitor', 'check', 'local', `${targetDomains.length} domains`, 'success', 0)

    return {
      timestamp: new Date().toISOString(),
      totalChecked: results.length,
      valid, expiringSoon, expired, errors,
      results,
      summary: `共检查 ${results.length} 个域名: ${valid}有效 / ${expiringSoon}即将过期 / ${expired}已过期 / ${errors}错误`
    }
  }

  /**
   * 获取证书详细信息
   */
  private fetchCertInfo(domain: string, port: number): Promise<CertInfo> {
    return new Promise((resolve, reject) => {
      const start = Date.now()

      const socket = tls.connect({
        host: domain,
        port,
        rejectUnauthorized: false, // 允许自签名证书
        timeout: this.timeout
      }, () => {
        const cert = socket.getPeerCertificate()
        const protocol = socket.getProtocol() || 'unknown'

        if (!cert || Object.keys(cert).length === 0) {
          socket.destroy()
          reject(new Error('无法获取证书信息'))
          return
        }

        const validFrom = cert.valid_from ? new Date(cert.valid_from).toISOString() : ''
        const validTo = cert.valid_to ? new Date(cert.valid_to).toISOString() : ''
        const daysRemaining = cert.valid_to
          ? Math.floor((new Date(cert.valid_to).getTime() - Date.now()) / 86400000)
          : -1

        // 解析SAN域名
        const sanDomains: string[] = []
        if (cert.subjectaltname) {
          const sanMatch = cert.subjectaltname.match(/DNS:([^,\s]+)/g)
          if (sanMatch) {
            sanMatch.forEach(san => {
              sanDomains.push(san.replace('DNS:', ''))
            })
          }
        }

        // 解析 issuer
        const issuer = typeof cert.issuer === 'object'
          ? Object.entries(cert.issuer).map(([k, v]) => v).join(' ')
          : String(cert.issuer || 'Unknown')

        // 解析 subject
        const subject = typeof cert.subject === 'object'
          ? Object.entries(cert.subject).map(([k, v]) => v).join(' ')
          : String(cert.subject || domain)

        const certInfo: CertInfo = {
          domain,
          port,
          status: daysRemaining <= 0 ? 'expired' : (daysRemaining <= this.config.warnDays ? 'expiring-soon' : 'valid'),
          issuer,
          subject,
          validFrom,
          validTo,
          daysRemaining,
          protocol,
          fingerprint: cert.fingerprint || undefined,
          sanDomains
        }

        socket.destroy()
        resolve(certInfo)
      })

      socket.on('error', (err) => {
        reject(new Error(`连接失败: ${err.message}`))
      })

      socket.on('timeout', () => {
        socket.destroy()
        reject(new Error(`连接超时 (${this.timeout}ms)`))
      })

      // 安全超时
      setTimeout(() => {
        if (!socket.destroyed) {
          socket.destroy()
          reject(new Error('全局超时'))
        }
      }, this.timeout + 2000)
    })
  }

  /**
   * 检查域名是否使用 openssl (备用方法)
   */
  async checkWithOpenSSL(domain: string, port: number = 443): Promise<CertInfo | null> {
    try {
      const { stdout } = await execAsync(
        `echo | openssl s_client -connect ${domain}:${port} -servername ${domain} 2>/dev/null | openssl x509 -noout -dates -issuer -subject -fingerprint -ext subjectAltName 2>/dev/null`,
        { timeout: this.timeout }
      )

      if (!stdout.trim()) return null

      const notBefore = stdout.match(/notBefore=(.+)/)?.[1] || ''
      const notAfter = stdout.match(/notAfter=(.+)/)?.[1] || ''
      const issuer = stdout.match(/issuer=(.+)/)?.[1] || 'Unknown'
      const subject = stdout.match(/subject=(.+)/)?.[1] || domain
      const fingerprint = stdout.match(/sha1Fingerprint=(.+)/)?.[1] || undefined

      const validTo = notAfter ? new Date(notAfter).toISOString() : ''
      const daysRemaining = notAfter
        ? Math.floor((new Date(notAfter).getTime() - Date.now()) / 86400000)
        : -1

      // 解析SAN
      const sanDomains: string[] = []
      const sanMatch = stdout.match(/DNS:([^,\s]+)/g)
      if (sanMatch) {
        sanMatch.forEach(san => sanDomains.push(san.replace('DNS:', '')))
      }

      return {
        domain, port,
        status: daysRemaining <= 0 ? 'expired' : (daysRemaining <= this.config.warnDays ? 'expiring-soon' : 'valid'),
        issuer, subject,
        validFrom: notBefore ? new Date(notBefore).toISOString() : '',
        validTo, daysRemaining,
        protocol: 'unknown',
        fingerprint,
        sanDomains
      }
    } catch {
      return null
    }
  }

  /**
   * 从配置文件加载域名列表
   */
  static loadDomainsFromConfig(configPath: string): string[] {
    try {
      const fs = require('fs')
      const content = fs.readFileSync(configPath, 'utf-8')
      const config = JSON.parse(content)
      return Array.isArray(config.domains) ? config.domains : []
    } catch {
      return []
    }
  }

  /**
   * 格式化监控报告
   */
  formatReport(report: SSLMonitorReport): string {
    const lines: string[] = []

    lines.push('='.repeat(60))
    lines.push('  SSL 证书监控报告')
    lines.push('='.repeat(60))
    lines.push(`  时间: ${report.timestamp}`)
    lines.push(`  ${report.summary}`)
    lines.push('-'.repeat(60))

    // 已过期
    const expired = report.results.filter(r => r.status === 'expired')
    if (expired.length > 0) {
      lines.push('')
      lines.push('  [ !!! 已过期 ]')
      for (const r of expired) {
        lines.push(`  !!! ${r.domain}:${r.port}`)
        if (r.cert) {
          lines.push(`      过期时间: ${r.cert.validTo}`)
          lines.push(`      颁发者: ${r.cert.issuer}`)
        }
      }
    }

    // 即将过期
    const expiring = report.results.filter(r => r.status === 'expiring-soon')
    if (expiring.length > 0) {
      lines.push('')
      lines.push('  [ ! 即将过期 ]')
      for (const r of expiring) {
        const days = r.cert?.daysRemaining || '?'
        const mark = (r.cert?.daysRemaining || 999) <= this.config.criticalDays ? '!!!' : ' ! '
        lines.push(`  [${mark}] ${r.domain}:${r.port} - 剩余 ${days} 天`)
        if (r.cert) {
          lines.push(`      过期时间: ${r.cert.validTo}`)
          lines.push(`      颁发者: ${r.cert.issuer}`)
        }
        if (r.chainIssues.length > 0) {
          for (const ci of r.chainIssues) {
            lines.push(`      [链路] ${ci}`)
          }
        }
      }
    }

    // 错误
    const errored = report.results.filter(r => r.status === 'error')
    if (errored.length > 0) {
      lines.push('')
      lines.push('  [ X 连接错误 ]')
      for (const r of errored) {
        lines.push(`  [X] ${r.domain}:${r.port} - ${r.error}`)
      }
    }

    // 有效
    const valid = report.results.filter(r => r.status === 'valid')
    if (valid.length > 0) {
      lines.push('')
      lines.push('  [ OK 有效证书 ]')
      for (const r of valid) {
        const days = r.cert?.daysRemaining || '?'
        const protocol = r.cert?.protocol || '?'
        lines.push(`  [OK] ${r.domain}:${r.port} - 剩余${days}天 (${protocol})`)
        if (r.chainIssues.length > 0) {
          for (const ci of r.chainIssues) {
            lines.push(`      [注意] ${ci}`)
          }
        }
      }
    }

    lines.push('')
    lines.push('='.repeat(60))
    return lines.join('\n')
  }

  /**
   * 生成告警信息（供告警系统使用）
   */
  generateAlerts(report: SSLMonitorReport): Array<{
    ruleId: string
    server: string
    severity: 'critical' | 'warning'
    message: string
  }> {
    const alerts: Array<{
      ruleId: string
      server: string
      severity: 'critical' | 'warning'
      message: string
    }> = []

    for (const r of report.results) {
      if (r.status === 'expired') {
        alerts.push({
          ruleId: 'ssl-expired',
          server: r.domain,
          severity: 'critical',
          message: `SSL证书已过期: ${r.domain}`
        })
      } else if (r.status === 'expiring-soon') {
        const days = r.cert?.daysRemaining || 0
        alerts.push({
          ruleId: days <= this.config.criticalDays ? 'ssl-critical' : 'ssl-warning',
          server: r.domain,
          severity: days <= this.config.criticalDays ? 'critical' : 'warning',
          message: `SSL证书将在${days}天后过期: ${r.domain}`
        })
      }
    }

    return alerts
  }
}
