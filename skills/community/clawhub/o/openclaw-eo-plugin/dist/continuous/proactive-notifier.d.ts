export type NotificationSeverity = 'info' | 'success' | 'warning' | 'error' | 'critical';
export type NotificationChannel = 'feishu' | 'discord' | 'email' | 'webhook' | 'console';
export interface Notification {
    id: string;
    severity: NotificationSeverity;
    title: string;
    message: string;
    timestamp: number;
    channel: NotificationChannel[];
    read: boolean;
    metadata?: Record<string, any>;
}
export interface NotificationConfig {
    enableChannel: Record<NotificationChannel, boolean>;
    webhookUrl?: string;
    emailRecipients?: string[];
    feishuChatId?: string;
    feishuAppId?: string;
    feishuAppSecret?: string;
    minSeverityToPersist: NotificationSeverity;
    maxNotifications: number;
    digestMode: 'immediate' | 'hourly' | 'daily';
}
export interface ScheduledReport {
    id: string;
    name: string;
    schedule: 'hourly' | 'daily' | 'weekly';
    channels: NotificationChannel[];
    template: (context: ReportContext) => string;
    enabled: boolean;
    lastRun?: number;
    nextRun?: number;
}
export interface ReportContext {
    period: {
        start: number;
        end: number;
    };
    tasksCompleted: number;
    tasksFailed: number;
    avgResponseTime: number;
    activeUsers: number;
    keyEvents: string[];
    warnings: string[];
}
export interface AnomalyDetectorConfig {
    enableResponseTimeAlert: boolean;
    enableErrorRateAlert: boolean;
    enableUserActivityAlert: boolean;
    responseTimeThreshold: number;
    errorRateThreshold: number;
    userActivityThreshold: number;
}
export declare class ProactiveNotifier {
    private config;
    private store;
    private dispatcher;
    private anomalyDetector;
    private scheduledReports;
    private reportInterval?;
    constructor(config?: Partial<NotificationConfig>);
    /**
     * Send a notification.
     */
    notify(severity: NotificationSeverity, title: string, message: string, channels?: NotificationChannel[], metadata?: Record<string, any>): Promise<string>;
    /**
     * Notify success.
     */
    success(title: string, message: string): Promise<string>;
    /**
     * Notify warning.
     */
    warning(title: string, message: string): Promise<string>;
    /**
     * Notify error.
     */
    error(title: string, message: string): Promise<string>;
    /**
     * Notify critical.
     */
    critical(title: string, message: string): Promise<string>;
    /**
     * Schedule a report.
     */
    scheduleReport(report: Omit<ScheduledReport, 'nextRun'>): void;
    /**
     * Generate and send a scheduled report.
     */
    private generateReport;
    /**
     * Start scheduled reports.
     */
    startReports(): void;
    /**
     * Stop scheduled reports.
     */
    stopReports(): void;
    /**
     * Calculate next run time.
     */
    private calculateNextRun;
    /**
     * Record metrics for anomaly detection.
     */
    recordMetrics(data: {
        responseTime?: number;
        errorRate?: number;
        userActivity?: number;
    }): void;
    /**
     * Check for anomalies and notify if found.
     */
    checkAnomalies(): Promise<void>;
    /**
     * Get unread notifications.
     */
    getUnread(): Notification[];
    /**
     * Get recent notifications.
     */
    getRecent(limit?: number): Notification[];
    /**
     * Get notification statistics.
     */
    getStats(): {
        total: number;
        unread: number;
        bySeverity: Record<string, number>;
    };
    /**
     * Mark notification as read.
     */
    markRead(id: string): boolean;
    /**
     * Mark all as read.
     */
    markAllRead(): void;
}
export declare const proactiveNotifier: ProactiveNotifier;
export default ProactiveNotifier;
//# sourceMappingURL=proactive-notifier.d.ts.map