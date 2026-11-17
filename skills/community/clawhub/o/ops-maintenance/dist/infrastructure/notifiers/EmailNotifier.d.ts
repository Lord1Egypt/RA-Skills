/**
 * 邮件通知器 - 使用 nodemailer 发送邮件告警
 */
import type { ClusterHealthReport, INotifier, EmailConfig } from '../../config/schemas';
export declare class EmailNotifier implements INotifier {
    private transporter;
    private config;
    private logger;
    constructor(config?: Partial<EmailConfig>);
    /**
     * 初始化 SMTP 连接
     */
    init(): Promise<void>;
    /**
     * 发送通知
     */
    notify(title: string, message: string, level: 'info' | 'warning' | 'critical'): Promise<void>;
    /**
     * 根据健康报告发送告警
     */
    sendAlert(report: ClusterHealthReport): Promise<void>;
    /**
     * 关闭连接
     */
    close(): Promise<void>;
}
export declare function createEmailNotifier(config: Partial<EmailConfig>): EmailNotifier;
//# sourceMappingURL=EmailNotifier.d.ts.map