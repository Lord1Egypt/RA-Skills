/**
 * 日志工具
 * 提供分级日志功能
 */
type LogLevel = 'debug' | 'info' | 'warn' | 'error';
interface LoggerConfig {
    level: LogLevel;
    prefix: string;
    enabled: boolean;
}
declare class Logger {
    private config;
    constructor(config?: Partial<LoggerConfig>);
    /**
     * 检查日志级别是否允许输出
     */
    private shouldLog;
    /**
     * 格式化日志消息
     */
    private format;
    /**
     * 输出调试日志
     */
    debug(message: string, ...args: any[]): void;
    /**
     * 输出信息日志
     */
    info(message: string, ...args: any[]): void;
    /**
     * 输出警告日志
     */
    warn(message: string, ...args: any[]): void;
    /**
     * 输出错误日志
     */
    error(message: string, ...args: any[]): void;
    /**
     * 设置日志级别
     */
    setLevel(level: LogLevel): void;
    /**
     * 启用/禁用日志
     */
    setEnabled(enabled: boolean): void;
}
export declare const logger: Logger;
export { Logger };
//# sourceMappingURL=logger.d.ts.map