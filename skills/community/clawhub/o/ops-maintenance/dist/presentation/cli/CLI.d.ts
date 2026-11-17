/**
 * CLI 入口模块
 * 协调所有组件完成命令执行
 */
import type { ISSHClient, IServerRepository } from '../../config/schemas';
import { type EmailConfig } from '../../config/schemas';
import type { ICacheRepository } from '../../config/schemas';
/**
 * CLI 应用主类
 */
export declare class CLI {
    private parser;
    private markdownFormatter;
    private jsonFormatter;
    private logger;
    private serverRepo?;
    private sshClient?;
    private cache?;
    private emailConfig?;
    constructor();
    /**
     * 注入依赖
     */
    setDependencies(serverRepo: IServerRepository, ssh: ISSHClient, cache: ICacheRepository, emailConfig?: Partial<EmailConfig>): void;
    /**
     * 执行命令
     */
    execute(args: string[]): Promise<string>;
    /**
     * 分派命令到对应的用例
     */
    private dispatch;
    /**
     * 执行健康检查
     */
    private executeHealthCheck;
    /**
     * 执行密码检查
     */
    private executePasswordCheck;
    /**
     * 执行磁盘检查
     */
    private executeDiskCheck;
    /**
     * 执行日志分析（占位）
     */
    private executeLogAnalysis;
    /**
     * 执行性能检查（占位）
     */
    private executePerformanceCheck;
    /**
     * 执行端口检查（占位）
     */
    private executePortCheck;
    /**
     * 执行进程检查（占位）
     */
    private executeProcessCheck;
    /**
     * 格式化输出
     */
    private formatOutput;
    /**
     * 格式化磁盘检查的 Markdown
     */
    private formatDiskMarkdown;
    /**
     * 格式化错误
     */
    private formatError;
    /**
     * 格式化字节
     */
    private formatBytes;
    /**
     * 获取帮助信息
     */
    getHelp(): string;
    /**
     * 执行邮件配置测试
     */
    private executeEmailConfig;
}
//# sourceMappingURL=CLI.d.ts.map