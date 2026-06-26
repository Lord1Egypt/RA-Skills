// ============================================================================
// EO Proactive Notifier - Phase 4.2: Active Notification System
//
// Implements important event push, scheduled reporting, and anomaly alerts.
// ============================================================================

// ============================================================================
// Types
// ============================================================================

import * as fs from 'fs'
import * as path from 'path'
import * as os from 'os'
import { logger } from '../utils/logger.js'

export type NotificationSeverity = 'info' | 'success' | 'warning' | 'error' | 'critical'
export type NotificationChannel = 'feishu' | 'discord' | 'email' | 'webhook' | 'console'

export interface Notification {
  id: string
  severity: NotificationSeverity
  title: string
  message: string
  timestamp: number
  channel: NotificationChannel[]
  read: boolean
  metadata?: Record<string, any>
}

export interface NotificationConfig {
  enableChannel: Record<NotificationChannel, boolean>
  webhookUrl?: string
  emailRecipients?: string[]
  feishuChatId?: string        // Default Feishu chat ID for notifications
  feishuAppId?: string         // Feishu app ID
  feishuAppSecret?: string     // Feishu app secret
  minSeverityToPersist: NotificationSeverity
  maxNotifications: number
  digestMode: 'immediate' | 'hourly' | 'daily'
}

export interface ScheduledReport {
  id: string
  name: string
  schedule: 'hourly' | 'daily' | 'weekly'
  channels: NotificationChannel[]
  template: (context: ReportContext) => string
  enabled: boolean
  lastRun?: number
  nextRun?: number
}

export interface ReportContext {
  period: { start: number; end: number }
  tasksCompleted: number
  tasksFailed: number
  avgResponseTime: number
  activeUsers: number
  keyEvents: string[]
  warnings: string[]
}

export interface AnomalyDetectorConfig {
  enableResponseTimeAlert: boolean
  enableErrorRateAlert: boolean
  enableUserActivityAlert: boolean
  responseTimeThreshold: number       // ms
  errorRateThreshold: number          // 0-1
  userActivityThreshold: number       // absolute change
}

// ============================================================================
// Notification Store
// ============================================================================

class NotificationStore {
  private notifications: Notification[] = []
  private maxNotifications: number
  
  constructor(maxNotifications = 100) {
    this.maxNotifications = maxNotifications
  }
  
  add(notification: Omit<Notification, 'id' | 'timestamp' | 'read'>): string {
    const id = 'notif-' + Date.now() + '-' + Math.random().toString(36).slice(2, 6)
    
    const full: Notification = {
      ...notification,
      id,
      timestamp: Date.now(),
      read: false,
    }
    
    this.notifications.unshift(full)
    
    if (this.notifications.length > this.maxNotifications) {
      this.notifications = this.notifications.slice(0, this.maxNotifications)
    }
    
    return id
  }
  
  markRead(id: string): boolean {
    const notif = this.notifications.find(n => n.id === id)
    if (notif) {
      notif.read = true
      return true
    }
    return false
  }
  
  markAllRead(): void {
    this.notifications.forEach(n => n.read = true)
  }
  
  getUnread(): Notification[] {
    return this.notifications.filter(n => !n.read)
  }
  
  getRecent(limit = 20): Notification[] {
    return this.notifications.slice(0, limit)
  }
  
  getBySeverity(severity: NotificationSeverity): Notification[] {
    return this.notifications.filter(n => n.severity === severity)
  }
  
  clear(): void {
    this.notifications = []
  }
  
  count(): { total: number; unread: number; bySeverity: Record<string, number> } {
    const bySeverity: Record<string, number> = {}
    let unread = 0
    
    this.notifications.forEach(n => {
      bySeverity[n.severity] = (bySeverity[n.severity] || 0) + 1
      if (!n.read) unread++
    })
    
    return { total: this.notifications.length, unread, bySeverity }
  }
}

// ============================================================================
// Channel Dispatcher
// ============================================================================

class ChannelDispatcher {
  private config: NotificationConfig

  constructor(config: NotificationConfig) {
    this.config = config
  }

  /**
   * Get Feishu config from openclaw.json or environment
   */
  private getFeishuConfig(): { appId?: string; appSecret?: string; chatId?: string } {
    // First check config
    if (this.config.feishuAppId && this.config.feishuAppSecret) {
      return {
        appId: this.config.feishuAppId,
        appSecret: this.config.feishuAppSecret,
        chatId: this.config.feishuChatId,
      }
    }
    // Fallback: read from openclaw.json
    try {
      const configPath = path.join(os.homedir(), '.openclaw', 'openclaw.json')
      if (fs.existsSync(configPath)) {
        const configData = JSON.parse(fs.readFileSync(configPath, 'utf-8'))
        const entries = configData?.plugins?.entries?.['eo-collaboration']
        if (entries?.feishuAppId && entries?.feishuAppSecret) {
          return {
            appId: entries.feishuAppId,
            appSecret: entries.feishuAppSecret,
            chatId: entries.feishuChatId,
          }
        }
      }
    } catch (e) {
      // Ignore errors, will return empty
    }
    return {}
  }
  
  /**
   * Send notification to specified channels.
   */
  async send(notification: Notification): Promise<void> {
    const promises: Promise<void>[] = []
    
    for (const channel of notification.channel) {
      if (!this.config.enableChannel[channel]) continue
      
      switch (channel) {
        case 'console':
          promises.push(this.sendConsole(notification))
          break
        case 'webhook':
          promises.push(this.sendWebhook(notification))
          break
        case 'feishu':
          promises.push(this.sendFeishu(notification))
          break
        case 'discord':
          promises.push(this.sendDiscord(notification))
          break
        case 'email':
          promises.push(this.sendEmail(notification))
          break
      }
    }
    
    await Promise.allSettled(promises)
  }
  
  private async sendConsole(notification: Notification): Promise<void> {
    const emoji: Record<NotificationSeverity, string> = {
      info: 'ℹ️',
      success: '✅',
      warning: '⚠️',
      error: '❌',
      critical: '🚨',
    }
    logger.info(`${emoji[notification.severity]} [${notification.title}] ${notification.message}`)
  }
  
  private async sendWebhook(notification: Notification): Promise<void> {
    if (!this.config.webhookUrl) return
    
    const colorMap: Record<NotificationSeverity, number> = {
      info: 0x3498db,
      success: 0x2ecc71,
      warning: 0xf39c12,
      error: 0xe74c3c,
      critical: 0x8e44ad,
    }
    
    try {
      await fetch(this.config.webhookUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          embeds: [{
            title: notification.title,
            description: notification.message,
            color: colorMap[notification.severity],
            timestamp: new Date(notification.timestamp).toISOString(),
            fields: notification.metadata 
              ? Object.entries(notification.metadata).map(([k, v]) => ({ name: k, value: String(v) }))
              : [],
          }],
        }),
      })
    } catch (e) {
      console.error('[ChannelDispatcher] Webhook failed:', e)
    }
  }
  
  private async sendFeishu(notification: Notification): Promise<void> {
    // Get Feishu config from openclaw.json or environment
    const feishuConfig = this.getFeishuConfig()

    // Use chat_id from notification metadata if provided, otherwise use config default
    const chatId = (notification.metadata as any)?.feishuChatId || feishuConfig.chatId
    if (!chatId) {
      console.warn('[ChannelDispatcher] Feishu chat_id not configured, skipping notification')
      return
    }

    try {
      const appId = feishuConfig.appId
      const appSecret = feishuConfig.appSecret

      if (!appId || !appSecret) {
        console.warn('[ChannelDispatcher] Feishu app credentials not configured')
        return
      }

      // Get tenant access token
      const tokenResponse = await fetch('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ app_id: appId, app_secret: appSecret }),
      })

      if (!tokenResponse.ok) {
        console.error('[ChannelDispatcher] Failed to get Feishu tenant access token:', tokenResponse.status)
        return
      }

      const tokenData = await tokenResponse.json() as { tenant_access_token?: string; msg?: string }
      const token = tokenData.tenant_access_token

      if (!token) {
        console.error('[ChannelDispatcher] No tenant_access_token in response:', tokenData.msg)
        return
      }

      // Build rich text message with emoji prefix
      const emojiMap: Record<NotificationSeverity, string> = {
        info: 'ℹ️',
        success: '✅',
        warning: '⚠️',
        error: '❌',
        critical: '🚨',
      }
      const emoji = emojiMap[notification.severity] || 'ℹ️'
      const title = `${emoji} ${notification.title}`

      // Send message using Feishu API
      const messageResponse = await fetch('https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          receive_id: chatId,
          msg_type: 'text',
          content: JSON.stringify({
            text: `${title}\n\n${notification.message}`,
          }),
        }),
      })

      if (!messageResponse.ok) {
        const errorText = await messageResponse.text()
        console.error('[ChannelDispatcher] Feishu message send failed:', messageResponse.status, errorText)
        return
      }

      const result = await messageResponse.json() as { code?: number; msg?: string }
      if (result.code !== 0) {
        console.error('[ChannelDispatcher] Feishu API error:', result.msg)
        return
      }

      logger.debug(`Feishu notification sent successfully to chat ${chatId}`)
    } catch (e) {
      console.error('[ChannelDispatcher] Feishu send failed:', e)
    }
  }
  
  private async sendDiscord(notification: Notification): Promise<void> {
    // Discord webhook integration
    logger.debug(`Discord would send: ${notification.title}`)
  }
  
  private async sendEmail(notification: Notification): Promise<void> {
    if (!this.config.emailRecipients?.length) return
    // Email integration would go here
    logger.debug(`Email would send to ${this.config.emailRecipients.join(', ')}: ${notification.title}`)
  }
}

// ============================================================================
// Anomaly Detector
// ============================================================================

class AnomalyDetector {
  private config: AnomalyDetectorConfig
  private history: {
    responseTime: number[]
    errorRate: number[]
    userActivity: number[]
  } = {
    responseTime: [],
    errorRate: [],
    userActivity: [],
  }
  
  constructor(config: AnomalyDetectorConfig) {
    this.config = config
  }
  
  /**
   * Record a data point.
   */
  record(data: { responseTime?: number; errorRate?: number; userActivity?: number }): void {
    if (data.responseTime !== undefined) {
      this.history.responseTime.push(data.responseTime)
      if (this.history.responseTime.length > 100) this.history.responseTime.shift()
    }
    if (data.errorRate !== undefined) {
      this.history.errorRate.push(data.errorRate)
      if (this.history.errorRate.length > 100) this.history.errorRate.shift()
    }
    if (data.userActivity !== undefined) {
      this.history.userActivity.push(data.userActivity)
      if (this.history.userActivity.length > 100) this.history.userActivity.shift()
    }
  }
  
  /**
   * Check for anomalies.
   */
  check(): { type: string; severity: NotificationSeverity; message: string }[] {
    const anomalies: { type: string; severity: NotificationSeverity; message: string }[] = []
    
    // Check response time
    if (this.config.enableResponseTimeAlert && this.history.responseTime.length >= 10) {
      const avg = this.average(this.history.responseTime.slice(-10))
      const current = this.history.responseTime[this.history.responseTime.length - 1]
      
      if (current > this.config.responseTimeThreshold) {
        anomalies.push({
          type: 'response_time',
          severity: current > this.config.responseTimeThreshold * 2 ? 'critical' : 'warning',
          message: `Response time elevated: ${current}ms (avg: ${avg.toFixed(0)}ms, threshold: ${this.config.responseTimeThreshold}ms)`,
        })
      }
    }
    
    // Check error rate
    if (this.config.enableErrorRateAlert && this.history.errorRate.length >= 10) {
      const avg = this.average(this.history.errorRate.slice(-10))
      const current = this.history.errorRate[this.history.errorRate.length - 1]
      
      if (current > this.config.errorRateThreshold) {
        anomalies.push({
          type: 'error_rate',
          severity: current > this.config.errorRateThreshold * 2 ? 'critical' : 'error',
          message: `Error rate elevated: ${(current * 100).toFixed(1)}% (avg: ${(avg * 100).toFixed(1)}%, threshold: ${(this.config.errorRateThreshold * 100).toFixed(1)}%)`,
        })
      }
    }
    
    // Check user activity
    if (this.config.enableUserActivityAlert && this.history.userActivity.length >= 2) {
      const current = this.history.userActivity[this.history.userActivity.length - 1]
      const previous = this.history.userActivity[this.history.userActivity.length - 2]
      const change = Math.abs(current - previous) / Math.max(previous, 1)
      
      if (change > this.config.userActivityThreshold) {
        anomalies.push({
          type: 'user_activity',
          severity: 'info',
          message: `User activity change detected: ${previous} → ${current} (${(change * 100).toFixed(0)}% change)`,
        })
      }
    }
    
    return anomalies
  }
  
  private average(arr: number[]): number {
    return arr.reduce((a, b) => a + b, 0) / arr.length
  }
}

// ============================================================================
// Proactive Notifier (Main Class)
// ============================================================================

export class ProactiveNotifier {
  private config: NotificationConfig
  private store: NotificationStore
  private dispatcher: ChannelDispatcher
  private anomalyDetector: AnomalyDetector
  private scheduledReports: Map<string, ScheduledReport> = new Map()
  private reportInterval?: NodeJS.Timeout
  
  constructor(config?: Partial<NotificationConfig>) {
    this.config = {
      enableChannel: {
        feishu: true,
        discord: false,
        email: false,
        webhook: true,
        console: true,
      },
      minSeverityToPersist: 'warning',
      maxNotifications: 100,
      digestMode: 'immediate',
      ...config,
    }
    
    this.store = new NotificationStore(this.config.maxNotifications)
    this.dispatcher = new ChannelDispatcher(this.config)
    this.anomalyDetector = new AnomalyDetector({
      enableResponseTimeAlert: true,
      enableErrorRateAlert: true,
      enableUserActivityAlert: false,
      responseTimeThreshold: 2000,
      errorRateThreshold: 0.05,
      userActivityThreshold: 0.5,
    })
  }
  
  // ============================================================================
  // Notifications
  // ============================================================================
  
  /**
   * Send a notification.
   */
  async notify(
    severity: NotificationSeverity,
    title: string,
    message: string,
    channels?: NotificationChannel[],
    metadata?: Record<string, any>
  ): Promise<string> {
    const notification = this.store.add({
      severity,
      title,
      message,
      channel: channels || ['console'],
      metadata,
    })
    
    // Send immediately
    const notif = this.store.getRecent(1)[0]
    if (notif) {
      await this.dispatcher.send(notif)
    }
    
    return notification
  }
  
  /**
   * Notify success.
   */
  success(title: string, message: string): Promise<string> {
    return this.notify('success', title, message)
  }
  
  /**
   * Notify warning.
   */
  warning(title: string, message: string): Promise<string> {
    return this.notify('warning', title, message)
  }
  
  /**
   * Notify error.
   */
  error(title: string, message: string): Promise<string> {
    return this.notify('error', title, message)
  }
  
  /**
   * Notify critical.
   */
  critical(title: string, message: string): Promise<string> {
    return this.notify('critical', title, message)
  }
  
  // ============================================================================
  // Scheduled Reports
  // ============================================================================
  
  /**
   * Schedule a report.
   */
  scheduleReport(report: Omit<ScheduledReport, 'nextRun'>): void {
    const nextRun = this.calculateNextRun(report.schedule)
    this.scheduledReports.set(report.id, { ...report, nextRun })
  }
  
  /**
   * Generate and send a scheduled report.
   */
  private async generateReport(report: ScheduledReport): Promise<void> {
    const now = Date.now()
    const periodStart = report.lastRun || now - 86400000
    
    const context: ReportContext = {
      period: { start: periodStart, end: now },
      tasksCompleted: Math.floor(Math.random() * 50), // Placeholder
      tasksFailed: Math.floor(Math.random() * 5),     // Placeholder
      avgResponseTime: Math.floor(Math.random() * 1000),
      activeUsers: Math.floor(Math.random() * 100),
      keyEvents: ['System running normally'],
      warnings: [],
    }
    
    const content = report.template(context)
    
    await this.notify(
      'info',
      `📊 ${report.name}`,
      content,
      report.channels
    )
    
    report.lastRun = now
    report.nextRun = this.calculateNextRun(report.schedule)
  }
  
  /**
   * Start scheduled reports.
   */
  startReports(): void {
    if (this.reportInterval) return
    
    // Check every minute
    this.reportInterval = setInterval(async () => {
      const now = Date.now()
      
      for (const report of this.scheduledReports.values()) {
        if (!report.enabled || !report.nextRun) continue
        
        if (now >= report.nextRun) {
          try {
            await this.generateReport(report)
          } catch (e) {
            console.error(`[ProactiveNotifier] Report ${report.name} failed:`, e)
          }
        }
      }
    }, 60000)
  }
  
  /**
   * Stop scheduled reports.
   */
  stopReports(): void {
    if (this.reportInterval) {
      clearInterval(this.reportInterval)
      this.reportInterval = undefined
    }
  }
  
  /**
   * Calculate next run time.
   */
  private calculateNextRun(schedule: ScheduledReport['schedule']): number {
    const now = Date.now()
    
    switch (schedule) {
      case 'hourly': {
        const nextHour = new Date()
        nextHour.setHours(nextHour.getHours() + 1, 0, 0, 0)
        return nextHour.getTime()
      }
      case 'daily': {
        const nextDay = new Date()
        nextDay.setDate(nextDay.getDate() + 1)
        nextDay.setHours(9, 0, 0, 0)
        return nextDay.getTime()
      }
      case 'weekly': {
        const nextWeek = new Date()
        nextWeek.setDate(nextWeek.getDate() + (7 - nextWeek.getDay()))
        nextWeek.setHours(9, 0, 0, 0)
        return nextWeek.getTime()
      }
      default:
        return now + 3600000
    }
  }
  
  // ============================================================================
  // Anomaly Detection
  // ============================================================================
  
  /**
   * Record metrics for anomaly detection.
   */
  recordMetrics(data: { responseTime?: number; errorRate?: number; userActivity?: number }): void {
    this.anomalyDetector.record(data)
  }
  
  /**
   * Check for anomalies and notify if found.
   */
  async checkAnomalies(): Promise<void> {
    const anomalies = this.anomalyDetector.check()
    
    for (const anomaly of anomalies) {
      await this.notify(anomaly.severity, `⚠️ Anomaly: ${anomaly.type}`, anomaly.message)
    }
  }
  
  // ============================================================================
  // Query
  // ============================================================================
  
  /**
   * Get unread notifications.
   */
  getUnread(): Notification[] {
    return this.store.getUnread()
  }
  
  /**
   * Get recent notifications.
   */
  getRecent(limit = 20): Notification[] {
    return this.store.getRecent(limit)
  }
  
  /**
   * Get notification statistics.
   */
  getStats(): { total: number; unread: number; bySeverity: Record<string, number> } {
    return this.store.count()
  }
  
  /**
   * Mark notification as read.
   */
  markRead(id: string): boolean {
    return this.store.markRead(id)
  }
  
  /**
   * Mark all as read.
   */
  markAllRead(): void {
    this.store.markAllRead()
  }
}

// ============================================================================
// Global Instance
// ============================================================================

export const proactiveNotifier = new ProactiveNotifier()

export default ProactiveNotifier
