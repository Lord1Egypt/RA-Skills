// ============================================================================
// EO Proactive Notifier - Phase 4.2: Active Notification System
//
// Implements important event push, scheduled reporting, and anomaly alerts.
// ============================================================================
// ============================================================================
// Types
// ============================================================================
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import { logger } from '../utils/logger.js';
// ============================================================================
// Notification Store
// ============================================================================
class NotificationStore {
    notifications = [];
    maxNotifications;
    constructor(maxNotifications = 100) {
        this.maxNotifications = maxNotifications;
    }
    add(notification) {
        const id = 'notif-' + Date.now() + '-' + Math.random().toString(36).slice(2, 6);
        const full = {
            ...notification,
            id,
            timestamp: Date.now(),
            read: false,
        };
        this.notifications.unshift(full);
        if (this.notifications.length > this.maxNotifications) {
            this.notifications = this.notifications.slice(0, this.maxNotifications);
        }
        return id;
    }
    markRead(id) {
        const notif = this.notifications.find(n => n.id === id);
        if (notif) {
            notif.read = true;
            return true;
        }
        return false;
    }
    markAllRead() {
        this.notifications.forEach(n => n.read = true);
    }
    getUnread() {
        return this.notifications.filter(n => !n.read);
    }
    getRecent(limit = 20) {
        return this.notifications.slice(0, limit);
    }
    getBySeverity(severity) {
        return this.notifications.filter(n => n.severity === severity);
    }
    clear() {
        this.notifications = [];
    }
    count() {
        const bySeverity = {};
        let unread = 0;
        this.notifications.forEach(n => {
            bySeverity[n.severity] = (bySeverity[n.severity] || 0) + 1;
            if (!n.read)
                unread++;
        });
        return { total: this.notifications.length, unread, bySeverity };
    }
}
// ============================================================================
// Channel Dispatcher
// ============================================================================
class ChannelDispatcher {
    config;
    constructor(config) {
        this.config = config;
    }
    /**
     * Get Feishu config from openclaw.json or environment
     */
    getFeishuConfig() {
        // First check config
        if (this.config.feishuAppId && this.config.feishuAppSecret) {
            return {
                appId: this.config.feishuAppId,
                appSecret: this.config.feishuAppSecret,
                chatId: this.config.feishuChatId,
            };
        }
        // Fallback: read from openclaw.json
        try {
            const configPath = path.join(os.homedir(), '.openclaw', 'openclaw.json');
            if (fs.existsSync(configPath)) {
                const configData = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
                const entries = configData?.plugins?.entries?.['eo-collaboration'];
                if (entries?.feishuAppId && entries?.feishuAppSecret) {
                    return {
                        appId: entries.feishuAppId,
                        appSecret: entries.feishuAppSecret,
                        chatId: entries.feishuChatId,
                    };
                }
            }
        }
        catch (e) {
            // Ignore errors, will return empty
        }
        return {};
    }
    /**
     * Send notification to specified channels.
     */
    async send(notification) {
        const promises = [];
        for (const channel of notification.channel) {
            if (!this.config.enableChannel[channel])
                continue;
            switch (channel) {
                case 'console':
                    promises.push(this.sendConsole(notification));
                    break;
                case 'webhook':
                    promises.push(this.sendWebhook(notification));
                    break;
                case 'feishu':
                    promises.push(this.sendFeishu(notification));
                    break;
                case 'discord':
                    promises.push(this.sendDiscord(notification));
                    break;
                case 'email':
                    promises.push(this.sendEmail(notification));
                    break;
            }
        }
        await Promise.allSettled(promises);
    }
    async sendConsole(notification) {
        const emoji = {
            info: 'ℹ️',
            success: '✅',
            warning: '⚠️',
            error: '❌',
            critical: '🚨',
        };
        logger.info(`${emoji[notification.severity]} [${notification.title}] ${notification.message}`);
    }
    async sendWebhook(notification) {
        if (!this.config.webhookUrl)
            return;
        const colorMap = {
            info: 0x3498db,
            success: 0x2ecc71,
            warning: 0xf39c12,
            error: 0xe74c3c,
            critical: 0x8e44ad,
        };
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
            });
        }
        catch (e) {
            console.error('[ChannelDispatcher] Webhook failed:', e);
        }
    }
    async sendFeishu(notification) {
        // Get Feishu config from openclaw.json or environment
        const feishuConfig = this.getFeishuConfig();
        // Use chat_id from notification metadata if provided, otherwise use config default
        const chatId = notification.metadata?.feishuChatId || feishuConfig.chatId;
        if (!chatId) {
            console.warn('[ChannelDispatcher] Feishu chat_id not configured, skipping notification');
            return;
        }
        try {
            const appId = feishuConfig.appId;
            const appSecret = feishuConfig.appSecret;
            if (!appId || !appSecret) {
                console.warn('[ChannelDispatcher] Feishu app credentials not configured');
                return;
            }
            // Get tenant access token
            const tokenResponse = await fetch('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ app_id: appId, app_secret: appSecret }),
            });
            if (!tokenResponse.ok) {
                console.error('[ChannelDispatcher] Failed to get Feishu tenant access token:', tokenResponse.status);
                return;
            }
            const tokenData = await tokenResponse.json();
            const token = tokenData.tenant_access_token;
            if (!token) {
                console.error('[ChannelDispatcher] No tenant_access_token in response:', tokenData.msg);
                return;
            }
            // Build rich text message with emoji prefix
            const emojiMap = {
                info: 'ℹ️',
                success: '✅',
                warning: '⚠️',
                error: '❌',
                critical: '🚨',
            };
            const emoji = emojiMap[notification.severity] || 'ℹ️';
            const title = `${emoji} ${notification.title}`;
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
            });
            if (!messageResponse.ok) {
                const errorText = await messageResponse.text();
                console.error('[ChannelDispatcher] Feishu message send failed:', messageResponse.status, errorText);
                return;
            }
            const result = await messageResponse.json();
            if (result.code !== 0) {
                console.error('[ChannelDispatcher] Feishu API error:', result.msg);
                return;
            }
            logger.debug(`Feishu notification sent successfully to chat ${chatId}`);
        }
        catch (e) {
            console.error('[ChannelDispatcher] Feishu send failed:', e);
        }
    }
    async sendDiscord(notification) {
        // Discord webhook integration
        logger.debug(`Discord would send: ${notification.title}`);
    }
    async sendEmail(notification) {
        if (!this.config.emailRecipients?.length)
            return;
        // Email integration would go here
        logger.debug(`Email would send to ${this.config.emailRecipients.join(', ')}: ${notification.title}`);
    }
}
// ============================================================================
// Anomaly Detector
// ============================================================================
class AnomalyDetector {
    config;
    history = {
        responseTime: [],
        errorRate: [],
        userActivity: [],
    };
    constructor(config) {
        this.config = config;
    }
    /**
     * Record a data point.
     */
    record(data) {
        if (data.responseTime !== undefined) {
            this.history.responseTime.push(data.responseTime);
            if (this.history.responseTime.length > 100)
                this.history.responseTime.shift();
        }
        if (data.errorRate !== undefined) {
            this.history.errorRate.push(data.errorRate);
            if (this.history.errorRate.length > 100)
                this.history.errorRate.shift();
        }
        if (data.userActivity !== undefined) {
            this.history.userActivity.push(data.userActivity);
            if (this.history.userActivity.length > 100)
                this.history.userActivity.shift();
        }
    }
    /**
     * Check for anomalies.
     */
    check() {
        const anomalies = [];
        // Check response time
        if (this.config.enableResponseTimeAlert && this.history.responseTime.length >= 10) {
            const avg = this.average(this.history.responseTime.slice(-10));
            const current = this.history.responseTime[this.history.responseTime.length - 1];
            if (current > this.config.responseTimeThreshold) {
                anomalies.push({
                    type: 'response_time',
                    severity: current > this.config.responseTimeThreshold * 2 ? 'critical' : 'warning',
                    message: `Response time elevated: ${current}ms (avg: ${avg.toFixed(0)}ms, threshold: ${this.config.responseTimeThreshold}ms)`,
                });
            }
        }
        // Check error rate
        if (this.config.enableErrorRateAlert && this.history.errorRate.length >= 10) {
            const avg = this.average(this.history.errorRate.slice(-10));
            const current = this.history.errorRate[this.history.errorRate.length - 1];
            if (current > this.config.errorRateThreshold) {
                anomalies.push({
                    type: 'error_rate',
                    severity: current > this.config.errorRateThreshold * 2 ? 'critical' : 'error',
                    message: `Error rate elevated: ${(current * 100).toFixed(1)}% (avg: ${(avg * 100).toFixed(1)}%, threshold: ${(this.config.errorRateThreshold * 100).toFixed(1)}%)`,
                });
            }
        }
        // Check user activity
        if (this.config.enableUserActivityAlert && this.history.userActivity.length >= 2) {
            const current = this.history.userActivity[this.history.userActivity.length - 1];
            const previous = this.history.userActivity[this.history.userActivity.length - 2];
            const change = Math.abs(current - previous) / Math.max(previous, 1);
            if (change > this.config.userActivityThreshold) {
                anomalies.push({
                    type: 'user_activity',
                    severity: 'info',
                    message: `User activity change detected: ${previous} → ${current} (${(change * 100).toFixed(0)}% change)`,
                });
            }
        }
        return anomalies;
    }
    average(arr) {
        return arr.reduce((a, b) => a + b, 0) / arr.length;
    }
}
// ============================================================================
// Proactive Notifier (Main Class)
// ============================================================================
export class ProactiveNotifier {
    config;
    store;
    dispatcher;
    anomalyDetector;
    scheduledReports = new Map();
    reportInterval;
    constructor(config) {
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
        };
        this.store = new NotificationStore(this.config.maxNotifications);
        this.dispatcher = new ChannelDispatcher(this.config);
        this.anomalyDetector = new AnomalyDetector({
            enableResponseTimeAlert: true,
            enableErrorRateAlert: true,
            enableUserActivityAlert: false,
            responseTimeThreshold: 2000,
            errorRateThreshold: 0.05,
            userActivityThreshold: 0.5,
        });
    }
    // ============================================================================
    // Notifications
    // ============================================================================
    /**
     * Send a notification.
     */
    async notify(severity, title, message, channels, metadata) {
        const notification = this.store.add({
            severity,
            title,
            message,
            channel: channels || ['console'],
            metadata,
        });
        // Send immediately
        const notif = this.store.getRecent(1)[0];
        if (notif) {
            await this.dispatcher.send(notif);
        }
        return notification;
    }
    /**
     * Notify success.
     */
    success(title, message) {
        return this.notify('success', title, message);
    }
    /**
     * Notify warning.
     */
    warning(title, message) {
        return this.notify('warning', title, message);
    }
    /**
     * Notify error.
     */
    error(title, message) {
        return this.notify('error', title, message);
    }
    /**
     * Notify critical.
     */
    critical(title, message) {
        return this.notify('critical', title, message);
    }
    // ============================================================================
    // Scheduled Reports
    // ============================================================================
    /**
     * Schedule a report.
     */
    scheduleReport(report) {
        const nextRun = this.calculateNextRun(report.schedule);
        this.scheduledReports.set(report.id, { ...report, nextRun });
    }
    /**
     * Generate and send a scheduled report.
     */
    async generateReport(report) {
        const now = Date.now();
        const periodStart = report.lastRun || now - 86400000;
        const context = {
            period: { start: periodStart, end: now },
            tasksCompleted: Math.floor(Math.random() * 50), // Placeholder
            tasksFailed: Math.floor(Math.random() * 5), // Placeholder
            avgResponseTime: Math.floor(Math.random() * 1000),
            activeUsers: Math.floor(Math.random() * 100),
            keyEvents: ['System running normally'],
            warnings: [],
        };
        const content = report.template(context);
        await this.notify('info', `📊 ${report.name}`, content, report.channels);
        report.lastRun = now;
        report.nextRun = this.calculateNextRun(report.schedule);
    }
    /**
     * Start scheduled reports.
     */
    startReports() {
        if (this.reportInterval)
            return;
        // Check every minute
        this.reportInterval = setInterval(async () => {
            const now = Date.now();
            for (const report of this.scheduledReports.values()) {
                if (!report.enabled || !report.nextRun)
                    continue;
                if (now >= report.nextRun) {
                    try {
                        await this.generateReport(report);
                    }
                    catch (e) {
                        console.error(`[ProactiveNotifier] Report ${report.name} failed:`, e);
                    }
                }
            }
        }, 60000);
    }
    /**
     * Stop scheduled reports.
     */
    stopReports() {
        if (this.reportInterval) {
            clearInterval(this.reportInterval);
            this.reportInterval = undefined;
        }
    }
    /**
     * Calculate next run time.
     */
    calculateNextRun(schedule) {
        const now = Date.now();
        switch (schedule) {
            case 'hourly': {
                const nextHour = new Date();
                nextHour.setHours(nextHour.getHours() + 1, 0, 0, 0);
                return nextHour.getTime();
            }
            case 'daily': {
                const nextDay = new Date();
                nextDay.setDate(nextDay.getDate() + 1);
                nextDay.setHours(9, 0, 0, 0);
                return nextDay.getTime();
            }
            case 'weekly': {
                const nextWeek = new Date();
                nextWeek.setDate(nextWeek.getDate() + (7 - nextWeek.getDay()));
                nextWeek.setHours(9, 0, 0, 0);
                return nextWeek.getTime();
            }
            default:
                return now + 3600000;
        }
    }
    // ============================================================================
    // Anomaly Detection
    // ============================================================================
    /**
     * Record metrics for anomaly detection.
     */
    recordMetrics(data) {
        this.anomalyDetector.record(data);
    }
    /**
     * Check for anomalies and notify if found.
     */
    async checkAnomalies() {
        const anomalies = this.anomalyDetector.check();
        for (const anomaly of anomalies) {
            await this.notify(anomaly.severity, `⚠️ Anomaly: ${anomaly.type}`, anomaly.message);
        }
    }
    // ============================================================================
    // Query
    // ============================================================================
    /**
     * Get unread notifications.
     */
    getUnread() {
        return this.store.getUnread();
    }
    /**
     * Get recent notifications.
     */
    getRecent(limit = 20) {
        return this.store.getRecent(limit);
    }
    /**
     * Get notification statistics.
     */
    getStats() {
        return this.store.count();
    }
    /**
     * Mark notification as read.
     */
    markRead(id) {
        return this.store.markRead(id);
    }
    /**
     * Mark all as read.
     */
    markAllRead() {
        this.store.markAllRead();
    }
}
// ============================================================================
// Global Instance
// ============================================================================
export const proactiveNotifier = new ProactiveNotifier();
export default ProactiveNotifier;
//# sourceMappingURL=proactive-notifier.js.map