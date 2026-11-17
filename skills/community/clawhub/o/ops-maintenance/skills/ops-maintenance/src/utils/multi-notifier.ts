/**
 * 多渠道通知发送器 - Webhook/Slack/钉钉
 *
 * 支持以下通知渠道：
 * - 飞书机器人 (feishu)
 * - 企业微信 (wechat)
 * - 邮件 (email)
 * - Webhook (webhook) - 通用 HTTP 回调
 * - Slack (slack)
 * - 钉钉 (dingtalk)
 * - 控制台 (console)
 */

import { getAuditLogger } from './audit-logger.js'
import https from 'https'
import http from 'http'

// ============================================================
// 类型定义
// ============================================================

export type NotifyChannel = 'feishu' | 'wechat' | 'email' | 'webhook' | 'slack' | 'dingtalk' | 'console'

export interface WebhookConfig {
  url: string
  headers?: Record<string, string>
}

export interface SlackConfig {
  webhookUrl: string
  channel?: string
  username?: string
}

export interface DingTalkConfig {
  webhookUrl: string
  secret?: string
  phoneMobiles?: string[]
  atAll?: boolean
}

export interface NotifyConfig {
  feishu?: {
    webhookUrl: string
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
  webhook?: WebhookConfig
  slack?: SlackConfig
  dingtalk?: DingTalkConfig
}

export interface AlertRecord {
  id: string
  ruleId: string
  ruleName: string
  type: string
  level: 'info' | 'warning' | 'critical'
  status: 'firing' | 'resolved' | 'silenced'
  server: string
  message: string
  value: number
  threshold: number
  firedAt: string
  resolvedAt?: string
}

// ============================================================
// 通知发送器
// ============================================================

export class MultiNotifier {
  private config: NotifyConfig
  private logger = getAuditLogger()

  constructor(config: NotifyConfig) {
    this.config = config
  }

  /**
   * 发送通知到所有配置的渠道
   */
  async send(alert: AlertRecord): Promise<void> {
    const channels = this.getChannelList(alert)

    for (const channel of channels) {
      await this.sendToChannel(channel, alert).catch(err => {
        this.logger.log('multi-notifier', 'send', alert.server, channel, 'error', err.message)
      })
    }
  }

  /**
   * 发送到指定渠道
   */
  private async sendToChannel(channel: NotifyChannel, alert: AlertRecord): Promise<void> {
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
      case 'slack':
        await this.notifySlack(alert)
        break
      case 'dingtalk':
        await this.notifyDingTalk(alert)
        break
      case 'console':
        this.notifyConsole(alert)
        break
    }
  }

  /**
   * 获取需要发送的渠道列表
   */
  private getChannelList(alert: AlertRecord): NotifyChannel[] {
    const channels: NotifyChannel[] = []

    if (this.config.feishu?.webhookUrl) channels.push('feishu')
    if (this.config.wechat?.webhookUrl) channels.push('wechat')
    if (this.config.email?.smtpHost) channels.push('email')
    if (this.config.webhook?.url) channels.push('webhook')
    if (this.config.slack?.webhookUrl) channels.push('slack')
    if (this.config.dingtalk?.webhookUrl) channels.push('dingtalk')
    channels.push('console')

    return channels
  }

  // ============================================================
  // 格式化告警消息
  // ============================================================

  private formatMessage(alert: AlertRecord, server: string, value: number): string {
    const levelText = alert.level === 'critical' ? '严重' : alert.level === 'warning' ? '警告' : '提示'
    return `[${levelText}] ${alert.ruleName} - ${server} - ${message} (值: ${value})`
  }

  // ============================================================
  // 飞书机器人通知
  // ============================================================

  private async notifyFeishu(alert: AlertRecord): Promise<void> {
    const config = this.config.feishu!
    const levelEmoji = alert.level === 'critical' ? '🔴' : alert.level === 'warning' ? '⚠️' : 'ℹ️'
    const statusText = alert.status === 'resolved' ? '已恢复' : '告警中'
    const message = this.formatMessage(alert, alert.server, alert.value)

    const payload = {
      msg_type: 'text',
      content: {
        text: `${levelEmoji} *${alert.ruleName}*\n服务器: ${alert.server}\n消息: ${message}\n状态: ${statusText}\n触发时间: ${new Date(alert.firedAt).toLocaleString()}`,
      },
    }

    await this.postWebhook(config.webhookUrl, payload)
  }

  // ============================================================
  // 企业微信通知
  // ============================================================

  private async notifyWechat(alert: AlertRecord): Promise<void> {
    const config = this.config.wechat!
    const levelEmoji = alert.level === 'critical' ? '🔴' : alert.level === 'warning' ? '⚠️' : 'ℹ️'

    const payload = {
      msgtype: 'text',
      text: {
        content: `${levelEmoji} [${alert.level.toUpperCase()}] ${alert.ruleName}\n服务器: ${alert.server}\n消息: ${message}\n触发时间: ${new Date(alert.firedAt).toLocaleString()}`,
      },
    }

    await this.postWebhook(config.webhookUrl, payload)
  }

  // ============================================================
  // 邮件通知
  // ============================================================

  private async notifyEmail(alert: AlertRecord): Promise<void> {
    const config = this.config.email!
    // 注意：实际生产环境应使用 nodemailer，这里使用简化的 HTTP 方式
    // 如果需要完整邮件支持，请在 AlertManager 中使用 nodemailer
    console.log(`[Email] 待发送到 ${config.from} -> ${config.to.join(', ')}`)
    console.log(`[Email] 主题: [${alert.level.toUpperCase()}] ${alert.ruleName}`)
    console.log(`[Email] 内容: ${message}`)
  }

  // ============================================================
  // 通用 Webhook 通知
  // ============================================================

  private async notifyWebhook(alert: AlertRecord): Promise<void> {
    const config = this.config.webhook!
    const payload = {
      alert: {
        id: alert.id,
        ruleId: alert.ruleId,
        ruleName: alert.ruleName,
        level: alert.level,
        status: alert.status,
        server: alert.server,
        message: message,
        value: alert.value,
        threshold: alert.threshold,
        firedAt: alert.firedAt,
      },
      timestamp: new Date().toISOString(),
    }

    await this.postWebhook(config.url, payload, config.headers)
  }

  // ============================================================
  // Slack 通知
  // ============================================================

  private async notifySlack(alert: AlertRecord): Promise<void> {
    const config = this.config.slack!
    const levelColor = alert.level === 'critical' ? '#FF0000' : alert.level === 'warning' ? '#FFA500' : '#36A64F'
    const statusText = alert.status === 'resolved' ? ':white_check_mark: 已恢复' : ':exclamation: 告警中'

    const payload = {
      channel: config.channel,
      username: config.username || 'Ops-Maintenance',
      attachments: [{
        color: levelColor,
        title: `${alert.ruleName} - ${alert.level.toUpperCase()}`,
        text: `**服务器:** ${alert.server}\n**消息:** ${message}\n**状态:** ${statusText}\n**触发时间:** ${new Date(alert.firedAt).toLocaleString()}`,
        footer: 'Ops Maintenance Alert',
        ts: Math.floor(Date.now() / 1000),
      }],
    }

    await this.postWebhook(config.webhookUrl, payload)
  }

  // ============================================================
  // 钉钉通知
  // ============================================================

  private async notifyDingTalk(alert: AlertRecord): Promise<void> {
    const config = this.config.dingtalk!
    const levelEmoji = alert.level === 'critical' ? 'ERROR' : alert.level === 'warning' ? 'WARN' : 'INFO'
    const statusText = alert.status === 'resolved' ? '已恢复' : '告警中'

    const payload = {
      msgtype: 'markdown',
      markdown: {
        title: `[${levelEmoji}] ${alert.ruleName}`,
        text: `## ${levelEmoji} ${alert.ruleName}\n\n> **服务器:** ${alert.server}\n> **消息:** ${message}\n> **状态:** ${statusText}\n> **触发时间:** ${new Date(alert.firedAt).toLocaleString()}`,
      },
      at: {
        atMobiles: config.phoneMobiles || [],
        isAtAll: config.atAll || false,
      },
    }

    await this.postWebhook(config.webhookUrl, payload)
  }

  // ============================================================
  // 控制台输出
  // ============================================================

  private notifyConsole(alert: AlertRecord): void {
    const timestamp = new Date().toLocaleString()
    const levelColor = alert.level === 'critical' ? '\x1b[31m' : alert.level === 'warning' ? '\x1b[33m' : '\x1b[36m'
    const resetColor = '\x1b[0m'

    console.log(`${levelColor}[${alert.level.toUpperCase()}]${resetColor} ${timestamp} | ${alert.server} | ${alert.ruleName}: ${message}`)
  }

  // ============================================================
  // 通用 HTTP POST
  // ============================================================

  private postWebhook(url: string, payload: object, headers?: Record<string, string>): Promise<void> {
    return new Promise((resolve, reject) => {
      let parsedUrl: any
      try {
        parsedUrl = new URL(url)
      } catch (e) {
        reject(new Error(`Invalid webhook URL: ${url}`))
        return
      }

      const isHttps = parsedUrl.protocol === 'https:'
      const options = {
        hostname: parsedUrl.hostname,
        port: parsedUrl.port || (isHttps ? 443 : 80),
        path: parsedUrl.pathname + parsedUrl.search,
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(headers || {}),
        },
      }

      const req = (isHttps ? https : http).request(options, (res) => {
        let data = ''
        res.on('data', chunk => { data += chunk })
        res.on('end', () => {
          if (res.statusCode && res.statusCode >= 200 && res.statusCode < 300) {
            resolve()
          } else {
            reject(new Error(`Webhook returned ${res.statusCode}: ${data}`))
          }
        })
      })

      req.on('error', reject)
      req.setTimeout(10000, () => {
        req.destroy()
        reject(new Error('Webhook request timeout'))
      })
      req.write(JSON.stringify(payload))
      req.end()
    })
  }
}

// ============================================================
// 单例管理
// ============================================================

let notifier: MultiNotifier | null = null

export function getMultiNotifier(config: NotifyConfig): MultiNotifier {
  if (!notifier) {
    notifier = new MultiNotifier(config)
  }
  return notifier
}

export function resetMultiNotifier(): void {
  notifier = null
}
