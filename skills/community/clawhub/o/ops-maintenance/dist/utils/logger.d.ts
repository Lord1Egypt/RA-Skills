/**
 * 日志工具
 * 基于 Winston 的结构化日志
 */
/**
 * 日志级别
 */
export declare enum LogLevel {
    DEBUG = "debug",
    INFO = "info",
    WARN = "warn",
    ERROR = "error"
}
/**
 *  Logger 单例类
 */
export declare class Logger {
    private context?;
    private static instance;
    private logger;
    private constructor();
    /**
     * 获取全局 Logger 实例
     */
    static getLogger(context?: string): Logger;
    /**
     * 设置日志级别
     */
    static setLevel(level: LogLevel | string): void;
    private static getInstance;
    /**
     * 记录 Debug 日志
     */
    debug(message: string, meta?: any): void;
    /**
     * 记录 Info 日志
     */
    info(message: string, meta?: any): void;
    /**
     * 记录 Warn 日志
     */
    warn(message: string, meta?: any): void;
    /**
     * 记录 Error 日志
     */
    error(message: string, error?: Error | any): void;
    /**
     * 通用日志方法
     */
    private log;
    /**
     * 记录请求（HTTP）
     */
    httpRequest(method: string, url: string, statusCode: number, duration: number): void;
    /**
     * 记录 SSH 命令执行
     */
    sshCommand(server: string, command: string, duration: number, success: boolean): void;
    /**
     * 记录配置变更
     */
    configChange(type: string, details: any): void;
}
//# sourceMappingURL=logger.d.ts.map