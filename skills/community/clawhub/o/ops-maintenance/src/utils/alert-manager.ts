/**
 * 告警管理器 v3.0
 *
 * 支持阈值告警、告警规则配置、多渠道通知（飞书/微信/邮件/Webhook）
 * 告警去重、告警静默、告警升级
 */

import { join } from 'path'
import { existsSync, mkdirSync, readFileSync, writeFileSync, appendFileSync } from 'fs'
import { getAuditLogger } from './audit-logger.js'

// ============================================================
// 类型定义
// ============================================================

/** 告警级别 */
export type AlertLevel = 'info' | 'warning' | 'critical'

/** 通知渠道类型 */
export type NotifyChannel = 'feishu' | 'wechat' | 'email' | 'webhook' | 'console'

/** 告警状态 */
export type AlertStatus = 'firing' | 'resolved' | 'silenced'

/** 告警规则 */
export interface AlertRule {
  id: string
  name: string
  /** 检查类型: disk/memory/load/cpu/service/process_down */
  type: string
  /** 阈值 (百分比或具体值) */
  threshold: number
  /** 告警级别 */
  level: AlertLevel
  /** 持续多久才告警 (秒) */
  duration: number
  /** 检查间隔 (秒) */
  interval: number
  /** 适用的服务器标签 (空=所有) */
  tags?: string[]
  /** 适用的服务器名 (空=所有) */
  servers?: string[]
  /** 通知渠道 */
  channels: NotifyChannel[]
  /** 是否启用 */
  enabled: boolean
  /** 自定义描述 */
  description?: string
}

/** 告警记录 */
export interface AlertRecord {
  id: string
  ruleId: string
  ruleName: string
  type: string
  level: AlertLevel
  status: AlertStatus
  server: string
  message: string
  value: number
  threshold: number
  firedAt: string
  resolvedAt?: string
  silencedUntil?: string
  notifyCount: number
  lastNotifyAt?: string
}

/** 通知渠道配置 */
export interface NotifyConfig {
  feishu?: {
    webhookUrl: string
    /** 飞书机器人名称 */
    botName?: string
  }
  wechat?: {
    webhookUrl: string
  }
  email?: {
    smtpHost: string
    smtpPort: number
    smtpUser: string
    smtpPass: string
    from: string
    to: string[]
  }
  webhook?: {
    url: string
    headers?: Record<string, string>
  }
}

/** 告警管理器配置 */
export interface AlertManagerConfig {
  /** 告警规则列表 */
  rules: AlertRule[]
  /** 通知渠道配置 */
  notify: NotifyConfig
  /** 重复告警间隔 (秒)，默认 3600 (1小时) */
  repeatInterval?: number
  /** 告警静默期 (秒)，同一规则+服务器在静默期内不重复告警 */
  silencePeriod?: number
}

// ============================================================
// 默认告警规则
// ============================================================

export const DEFAULT_ALERT_RULES: AlertRule[] = [
  {
    id: 'disk-warning',
    name: '磁盘使用率警告',
    type: 'disk',
    threshold: 80,
    level: 'warning',
    duration: 60,
    interval: 300,
    channels: ['feishu', 'console'],
    enabled: true,
    description: '磁盘使用率超过80%',
  },
  {
    id: 'disk-critical',
    name: '磁盘使用率严重',
    type: 'disk',
    threshold: 90,
    level: 'critical',
    duration: 30,
    interval: 60,
    channels: ['feishu', 'wechat', 'console'],
    enabled: true,
    description: '磁盘使用率超过90%',
  },
  {
    id: 'memory-warning',
    name: '内存使用率警告',
    type: 'memory',
    threshold: 85,
    level: 'warning',
    duration: 60,
    interval: 300,
    channels: ['feishu', 'console'],
    enabled: true,
    description: '内存使用率超过85%',
  },
  {
    id: 'memory-critical',
    name: '内存使用率严重',
    type: 'memory',
    threshold: 95,
    level: 'critical',
    duration: 30,
    interval: 60,
    channels: ['feishu', 'wechat', 'console'],
    enabled: true,
    description: '内存使用率超过95%',
  },
  {
    id: 'load-warning',
    name: '系统负载警告',
    type: 'load',
    threshold: 5,
    level: 'warning',
    duration: 120,
    interval: 300,
    channels: ['feishu', 'console'],
    enabled: true,
    description: '5分钟平均负载超过5',
  },
  {
    id: 'load-critical',
    name: '系统负载严重',
    type: 'load',
    threshold: 10,
    level: 'critical',
    duration: 60,
    interval: 60,
    channels: ['feishu', 'wechat', 'console'],
    enabled: true,
    description: '5分钟平均负载超过10',
  },
  {
    id: 'service-down',
    name: '服务宕机',
    type: 'service',
    threshold: 0,
    level: 'critical',
    duration: 30,
    interval: 60,
    channels: ['feishu', 'wechat', 'console'],
    enabled: true,
    description: '关键服务停止运行',
  },
  {
    id: 'cpu-warning',
    name: 'CPU使用率警告',
    type: 'cpu',
    threshold: 80,
    level: 'warning',
    duration: 120,
    interval: 300,
    channels: ['feishu', 'console'],
    enabled: true,
    description: 'CPU使用率超过80%',
  },
]

// ============================================================
// 告警管理器
// ============================================================

export class AlertManager {
  private configDir: string
  private alertFile: string
  private configFile: string
  private rules: AlertRule[]
  private notify: NotifyConfig
  private repeatInterval: number
  private silencePeriod: number
  private activeAlerts: Map<string, AlertRecord> = new Map()

  constructor(config?: Partial<AlertManagerConfig>) {
    this.configDir = join(process.env.HOME || '~', '.config/ops-maintenance')
    this.alertFile = join(this.configDir, 'alerts.json')
    this.configFile = join(this.configDir, 'alert-config.json')

    // 确保目录存在
    if (!existsSync(this.configDir)) {
      mkdirSync(this.configDir, { recursive: true })
    }

    // 加载或使用默认配置
    const loadedConfig = this.loadConfig()
    this.rules = config?.rules || loadedConfig.rules || DEFAULT_ALERT_RULES
    this.notify = config?.notify || loadedConfig.notify || {}
    this.repeatInterval = config?.repeatInterval || loadedConfig.repeatInterval || 3600
    this.silencePeriod = config?.silencePeriod || loadedConfig.silencePeriod || 600

    // 加载活跃告警
    this.loadAlerts()
  }

  // ----------------------------------------------------------
  // 配置管理
  // ----------------------------------------------------------

  /** 加载告警配置 */
  private loadConfig(): Partial<AlertManagerConfig> {
    if (existsSync(this.configFile)) {
      try {
        const content = readFileSync(this.configFile, 'utf-8')
        return JSON.parse(content)
      } catch {
        return {}
      }
    }
    return {}
  }

  /** 保存告警配置 */
  saveConfig(): void {
    const config: AlertManagerConfig = {
      rules: this.rules,
      notify: this.notify,
      repeatInterval: this.repeatInterval,
      silencePeriod: this.silencePeriod,
    }
    writeFileSync(this.configFile, JSON.stringify(config, null, 2))
  }

  /** 获取所有规则 */
  getRules(): AlertRule[] {
    return [...this.rules]
  }

  /** 添加/更新规则 */
  upsertRule(rule: AlertRule): void {
    const idx = this.rules.findIndex(r => r.id === rule.id)
    if (idx >= 0) {
      this.rules[idx] = rule
    } else {
      this.rules.push(rule)
    }
    this.saveConfig()
  }

  /** 删除规则 */
  removeRule(ruleId: string): boolean {
    const idx = this.rules.findIndex(r => r.id === ruleId)
    if (idx >= 0) {
      this.rules.splice(idx, 1)
      this.saveConfig()
      return true
    }
    return false
  }

  /** 启用/禁用规则 */
  toggleRule(ruleId: string, enabled: boolean): boolean {
    const rule = this.rules.find(r => r.id === ruleId)
    if (rule) {
      rule.enabled = enabled
      this.saveConfig()
      return true
    }
    return false
  }

  /** 更新通知渠道配置 */
  updateNotifyConfig(channel: NotifyChannel, config: any): void {
    (this.notify as any)[channel] = config
    this.saveConfig()
  }

  // ----------------------------------------------------------
  // 告警触发
  // ----------------------------------------------------------

  /**
   * 评估检查结果并触发告警
   *
   * @param type 检查类型 (disk/memory/load/cpu/service)
   * @param server 服务器标识
   * @param value 实际值
   * @param extra 额外信息
   */
  evaluate(type: string, server: string, value: number, extra?: Record<string, any>): AlertRecord | null {
    const matchedRules = this.rules.filter(r =>
      r.enabled && r.type === type && this.ruleMatchesServer(r, server)
    )

    // 按阈值从高到低排序，优先触发最高级别的告警
    matchedRules.sort((a, b) => b.threshold - a.threshold)

    for (const rule of matchedRules) {
      const isBreached = value >= rule.threshold || (type === 'service' && value <= rule.threshold)

      if (isBreached) {
        const alertKey = `${rule.id}:${server}`
        const existing = this.activeAlerts.get(alertKey)

        if (existing && existing.status === 'firing') {
          // 已有活跃告警，检查是否需要重复通知
          const now = Date.now()
          const lastNotify = existing.lastNotifyAt ? new Date(existing.lastNotifyAt).getTime() : 0
          const elapsed = (now - lastNotify) / 1000

          if (elapsed >= this.repeatInterval) {
            existing.value = value
            existing.notifyCount++
            existing.lastNotifyAt = new Date().toISOString()
            this.sendNotification(existing, rule)
            this.saveAlerts()
          }
          return existing
        }

        if (existing && existing.status === 'silenced') {
          // 静默期中，跳过
          if (existing.silencedUntil && new Date(existing.silencedUntil) > new Date()) {
            return null
          }
          // 静默期结束，重新触发
          existing.status = 'firing'
          existing.silencedUntil = undefined
        }

        // 新告警
        const alert: AlertRecord = {
          id: `alert-${Date.now()}-${Math.random().toString(36).substr(2, 6)}`,
          ruleId: rule.id,
          ruleName: rule.name,
          type,
          level: rule.level,
          status: 'firing',
          server,
          message: this.formatMessage(rule, server, value, extra),
          value,
          threshold: rule.threshold,
          firedAt: new Date().toISOString(),
          notifyCount: 1,
          lastNotifyAt: new Date().toISOString(),
        }

        this.activeAlerts.set(alertKey, alert)
        this.sendNotification(alert, rule)
        this.saveAlerts()

        // 审计日志
        const audit = getAuditLogger()
        audit.log({
          timestamp: new Date().toISOString(),
          operation: 'alert_fired',
          server,
          status: 'success',
          metadata: { ruleId: rule.id, level: rule.level, value, threshold: rule.threshold },
        })

        return alert
      } else {
        // 阈值恢复正常
        const alertKey = `${rule.id}:${server}`
        const existing = this.activeAlerts.get(alertKey)
        if (existing && existing.status === 'firing') {
          existing.status = 'resolved'
          existing.resolvedAt = new Date().toISOString()
          this.sendResolvedNotification(existing, rule)
          this.saveAlerts()
        }
      }
    }

    return null
  }

  /** 检查规则是否匹配服务器 */
  private ruleMatchesServer(rule: AlertRule, server: string): boolean {
    if (!rule.tags?.length && !rule.servers?.length) return true
    if (rule.servers?.length && rule.servers.includes(server)) return true
    // tags 匹配需要服务器配置中有 tags，这里简化处理
    return true
  }

  // ----------------------------------------------------------
  // 告警操作
  // ----------------------------------------------------------

  /** 静默告警 */
  silence(alertKey: string, durationSeconds: number = 3600): boolean {
    const alert = this.activeAlerts.get(alertKey)
    if (alert) {
      alert.status = 'silenced'
      alert.silencedUntil = new Date(Date.now() + durationSeconds * 1000).toISOString()
      this.saveAlerts()
      return true
    }
    return false
  }

  /** 解除静默 */
  unsilence(alertKey: string): boolean {
    const alert = this.activeAlerts.get(alertKey)
    if (alert && alert.status === 'silenced') {
      alert.status = 'firing'
      alert.silencedUntil = undefined
      this.saveAlerts()
      return true
    }
    return false
  }

  /** 获取所有活跃告警 */
  getActiveAlerts(): AlertRecord[] {
    return Array.from(this.activeAlerts.values()).filter(a => a.status === 'firing')
  }

  /** 获取所有告警 (含已恢复) */
  getAllAlerts(): AlertRecord[] {
    return Array.from(this.activeAlerts.values())
  }

  /** 获取告警统计 */
  getAlertStats(): {
    total: number
    firing: number
    resolved: number
    silenced: number
    byLevel: Record<string, number>
    byType: Record<string, number>
    byServer: Record<string, number>
  } {
    const alerts = this.getAllAlerts()
    const stats = {
      total: alerts.length,
      firing: 0,
      resolved: 0,
      silenced: 0,
      byLevel: {} as Record<string, number>,
      byType: {} as Record<string, number>,
      byServer: {} as Record<string, number>,
    }

    for (const alert of alerts) {
      stats[alert.status]++
      stats.byLevel[alert.level] = (stats.byLevel[alert.level] || 0) + 1
      stats.byType[alert.type] = (stats.byType[alert.type] || 0) + 1
      stats.byServer[alert.server] = (stats.byServer[alert.server] || 0) + 1
    }

    return stats
  }

  /** 清理已恢复的旧告警 (默认7天前) */
  cleanup(daysOld: number = 7): number {
    const cutoff = new Date(Date.now() - daysOld * 86400000)
    let removed = 0

    for (const [key, alert] of this.activeAlerts.entries()) {
      if (alert.status === 'resolved' && alert.resolvedAt && new Date(alert.resolvedAt) < cutoff) {
        this.activeAlerts.delete(key)
        removed++
      }
    }

    if (removed > 0) this.saveAlerts()
    return removed
  }

  // ----------------------------------------------------------
  // 通知发送
  // ----------------------------------------------------------

  /** 发送告警通知 */
  private async sendNotification(alert: AlertRecord, rule: AlertRule): Promise<void> {
    const channels = rule.channels

    for (const channel of channels) {
      try {
        switch (channel) {
          case 'feishu':
            await this.notifyFeishu(alert)
            break
          case 'wechat':
            await this.notifyWechat(alert)
            break
          case 'email':
            await this.notifyEmail(alert)
            break
          case 'webhook':
            await this.notifyWebhook(alert)
            break
          case 'console':
            this.notifyConsole(alert)
            break
        }
      } catch (error: any) {
        // 通知失败不影响主流程，记录审计日志
        const audit = getAuditLogger()
        audit.logFailure('alert_notify', alert.server, error.message, undefined, { channel, alertId: alert.id })
      }
    }
  }

  /** 发送恢复通知 */
  private async sendResolvedNotification(alert: AlertRecord, rule: AlertRule): Promise<void> {
    const resolvedAlert: AlertRecord = {
      ...alert,
      message: `✅ [已恢复] ${alert.message}`,
    }
    // 恢复通知只发一次，用默认渠道
    const channels = rule.channels.includes('feishu') ? ['feishu'] : ['console']
    for (const channel of channels) {
      try {
        switch (channel) {
          case 'feishu':
            await this.notifyFeishu(resolvedAlert)
            break
          default:
            this.notifyConsole(resolvedAlert)
        }
      } catch {
        // ignore
      }
    }
  }

  /** 飞书通知 */
  private async notifyFeishu(alert: AlertRecord): Promise<void> {
    const feishuConfig = this.notify.feishu
    if (!feishuConfig?.webhookUrl) {
      console.warn('[AlertManager] 飞书通知未配置 webhookUrl')
      return
    }

    const levelEmoji = { info: 'ℹ️', warning: '⚠️', critical: '🔴' }
    const payload = {
      msg_type: 'interactive',
      card: {
        header: {
          title: { tag: 'plain_text', content: `${levelEmoji[alert.level]} 运维告警: ${alert.ruleName}` },
          template: alert.level === 'critical' ? 'red' : alert.level === 'warning' ? 'orange' : 'blue',
        },
        elements: [
          { tag: 'div', text: { tag: 'lark_md', content: `**服务器**: ${alert.server}\n**类型**: ${alert.type}\n**当前值**: ${alert.value}\n**阈值**: ${alert.threshold}\n**时间**: ${alert.firedAt}` } },
          { tag: 'div', text: { tag: 'lark_md', content: alert.message } },
        ],
      },
    }

    const response = await fetch(feishuConfig.webhookUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })

    if (!response.ok) {
      throw new Error(`飞书通知失败: ${response.status} ${await response.text()}`)
    }
  }

  /** 微信通知 (企业微信机器人) */
  private async notifyWechat(alert: AlertRecord): Promise<void> {
    const wechatConfig = this.notify.wechat
    if (!wechatConfig?.webhookUrl) {
      console.warn('[AlertManager] 微信通知未配置 webhookUrl')
      return
    }

    const levelEmoji = { info: 'ℹ️', warning: '⚠️', critical: '🔴' }
    const payload = {
      msgtype: 'markdown',
      markdown: {
        content: `${levelEmoji[alert.level]} 运维告警: ${alert.ruleName}\n>服务器: <font color="comment">${alert.server}</font>\n>类型: ${alert.type}\n>当前值: ${alert.value} / 阈值: ${alert.threshold}\n>时间: ${alert.firedAt}\n\n${alert.message}`,
      },
    }

    const response = await fetch(wechatConfig.webhookUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })

    if (!response.ok) {
      throw new Error(`微信通知失败: ${response.status} ${await response.text()}`)
    }
  }

  /** 邮件通知 */
  private async notifyEmail(alert: AlertRecord): Promise<void> {
    const emailConfig = this.notify.email
    if (!emailConfig) {
      console.warn('[AlertManager] 邮件通知未配置')
      return
    }

    // 邮件发送需要 nodemailer，如果未安装则降级为 console
    try {
      const nodemailer = await import('nodemailer')
      const transporter = nodemailer.createTransport({
        host: emailConfig.smtpHost,
        port: emailConfig.smtpPort,
        auth: { user: emailConfig.smtpUser, pass: emailConfig.smtpPass },
      })

      await transporter.sendMail({
        from: emailConfig.from,
        to: emailConfig.to.join(','),
        subject: `[${alert.level.toUpperCase()}] 运维告警: ${alert.ruleName} - ${alert.server}`,
        text: `${alert.message}\n\n服务器: ${alert.server}\n类型: ${alert.type}\n当前值: ${alert.value}\n阈值: ${alert.threshold}\n时间: ${alert.firedAt}`,
      })
    } catch {
      // nodemailer 未安装，降级为 console
      this.notifyConsole(alert)
    }
  }

  /** Webhook 通知 */
  private async notifyWebhook(alert: AlertRecord): Promise<void> {
    const webhookConfig = this.notify.webhook
    if (!webhookConfig?.url) {
      console.warn('[AlertManager] Webhook通知未配置 url')
      return
    }

    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...webhookConfig.headers,
    }

    const response = await fetch(webhookConfig.url, {
      method: 'POST',
      headers,
      body: JSON.stringify(alert),
    })

    if (!response.ok) {
      throw new Error(`Webhook通知失败: ${response.status} ${await response.text()}`)
    }
  }

  /** 控制台通知 (兜底) */
  private notifyConsole(alert: AlertRecord): void {
    const levelEmoji = { info: 'ℹ️', warning: '⚠️', critical: '🔴' }
    console.log(`\n${levelEmoji[alert.level]} [${alert.level.toUpperCase()}] ${alert.ruleName}`)
    console.log(`   服务器: ${alert.server}`)
    console.log(`   类型: ${alert.type} | 当前值: ${alert.value} | 阈值: ${alert.threshold}`)
    console.log(`   ${alert.message}`)
    console.log(`   时间: ${alert.firedAt}\n`)
  }

  // ----------------------------------------------------------
  // 告警消息格式化
  // ----------------------------------------------------------

  private formatMessage(rule: AlertRule, server: string, value: number, extra?: Record<string, any>): string {
    const messages: Record<string, string> = {
      disk: `服务器 ${server} 磁盘使用率 ${value}% 超过阈值 ${rule.threshold}%`,
      memory: `服务器 ${server} 内存使用率 ${value}% 超过阈值 ${rule.threshold}%`,
      load: `服务器 ${server} 系统负载 ${value} 超过阈值 ${rule.threshold}`,
      cpu: `服务器 ${server} CPU使用率 ${value}% 超过阈值 ${rule.threshold}%`,
      service: `服务器 ${server} 关键服务停止运行`,
      process_down: `服务器 ${server} 关键进程已停止`,
    }

    let msg = messages[rule.type] || `${rule.name}: 服务器 ${server}，当前值 ${value}，阈值 ${rule.threshold}`

    if (extra?.serviceName) {
      msg += ` (服务: ${extra.serviceName})`
    }
    if (extra?.processName) {
      msg += ` (进程: ${extra.processName})`
    }
    if (rule.description) {
      msg += `\n${rule.description}`
    }

    return msg
  }

  // ----------------------------------------------------------
  // 持久化
  // ----------------------------------------------------------

  private loadAlerts(): void {
    if (existsSync(this.alertFile)) {
      try {
        const content = readFileSync(this.alertFile, 'utf-8')
        const alerts: AlertRecord[] = JSON.parse(content)
        for (const alert of alerts) {
          const key = `${alert.ruleId}:${alert.server}`
          this.activeAlerts.set(key, alert)
        }
      } catch {
        // ignore
      }
    }
  }

  private saveAlerts(): void {
    const alerts = Array.from(this.activeAlerts.values())
    writeFileSync(this.alertFile, JSON.stringify(alerts, null, 2))
  }
}

// ============================================================
// 全局单例
// ============================================================

let globalAlertManager: AlertManager | null = null

export function getAlertManager(config?: Partial<AlertManagerConfig>): AlertManager {
  if (!globalAlertManager) {
    globalAlertManager = new AlertManager(config)
  }
  return globalAlertManager
}

/** 重置全局实例 (测试用) */
export function resetAlertManager(): void {
  globalAlertManager = null
}
