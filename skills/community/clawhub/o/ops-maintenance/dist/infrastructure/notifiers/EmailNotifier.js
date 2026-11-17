"use strict";
/**
 * 邮件通知器 - 使用 nodemailer 发送邮件告警
 */
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.EmailNotifier = void 0;
exports.createEmailNotifier = createEmailNotifier;
const nodemailer_1 = __importDefault(require("nodemailer"));
const schemas_1 = require("../../config/schemas");
const logger_1 = require("../../utils/logger");
const DEFAULT_CONFIG = {
    host: 'smtp.qq.com',
    port: 465,
    user: '',
    password: '',
    ssl: true
};
class EmailNotifier {
    constructor(config = {}) {
        this.transporter = null;
        this.logger = logger_1.Logger.getLogger('EmailNotifier');
        this.config = { ...DEFAULT_CONFIG, from: '', to: [], ...config };
    }
    /**
     * 初始化 SMTP 连接
     */
    async init() {
        if (this.transporter)
            return;
        this.transporter = nodemailer_1.default.createTransport({
            host: this.config.host,
            port: this.config.port,
            secure: this.config.ssl !== false,
            auth: {
                user: this.config.user,
                pass: this.config.password
            }
        });
        // 验证连接
        const info = await this.transporter.verify();
        this.logger.info(`SMTP 连接成功: ${this.config.host}:${this.config.port}`);
    }
    /**
     * 发送通知
     */
    async notify(title, message, level) {
        // 优先检查凭据，未配置则直接跳过
        if (!this.config.user || !this.config.password) {
            this.logger.warn('邮件未配置，跳过通知');
            return;
        }
        if (!this.transporter) {
            await this.init();
        }
        if (!this.transporter)
            return;
        const subject = `[Ops Alert] ${level.toUpperCase()}: ${title}`;
        const color = level === 'critical' ? '🔴' : level === 'warning' ? '🟡' : '🟢';
        const body = `${color} ${title}\\n\\n${message}\\n\\n---\\nSent by Ops Maintenance`;
        const mailOptions = {
            from: this.config.from || this.config.user,
            to: this.config.to.join(','),
            subject,
            text: body
        };
        try {
            const info = await this.transporter.sendMail(mailOptions);
            this.logger.info(`邮件发送成功: ${info.messageId}`);
        }
        catch (error) {
            this.logger.error(`邮件发送失败: ${error.message}`);
            throw error;
        }
    }
    /**
     * 根据健康报告发送告警
     */
    async sendAlert(report) {
        if (this.config.alertOnly !== false) {
            // 检查是否有告警
            const hasAlert = report.warning > 0 || report.offline > 0;
            if (!hasAlert) {
                this.logger.debug('无告警，跳过邮件发送');
                return;
            }
        }
        const lines = [];
        lines.push(`集群健康报告 - ${report.generatedAt.toISOString()}`);
        lines.push(`总数: ${report.totalServers} | 正常: ${report.healthy} | 警告: ${report.warning} | 离线: ${report.offline}`);
        lines.push('');
        for (const health of report.serverHealth) {
            const icon = health.status === schemas_1.ServerStatus.HEALTHY ? '✅' : health.status === schemas_1.ServerStatus.WARNING ? '⚠️' : '❌';
            lines.push(`${icon} ${health.server.getDisplayName()} (${health.server.host}) - ${health.status}`);
            if (health.metrics) {
                const disk = health.getDiskUsagePercent();
                const mem = health.getMemoryUsagePercent();
                if (disk > 70)
                    lines.push(`   磁盘: ${disk}%`);
                if (mem > 70)
                    lines.push(`   内存: ${mem}%`);
            }
        }
        const title = report.offline > 0 ? '服务器离线告警' : report.warning > 0 ? '服务器告警' : '巡检完成';
        await this.notify(title, lines.join('\n'), report.offline > 0 ? 'critical' : 'warning');
    }
    /**
     * 关闭连接
     */
    async close() {
        if (this.transporter) {
            await this.transporter.close();
            this.transporter = null;
        }
    }
}
exports.EmailNotifier = EmailNotifier;
function createEmailNotifier(config) {
    return new EmailNotifier(config);
}
//# sourceMappingURL=EmailNotifier.js.map