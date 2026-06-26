/**
 * EO Logger Utility
 *
 * Unified logging utility for EO plugin
 * Can be replaced with OpenClaw api.logger when available
 */
export declare enum LogLevel {
    DEBUG = 0,
    INFO = 1,
    WARN = 2,
    ERROR = 3
}
export interface LoggerConfig {
    level: LogLevel;
    prefix?: string;
    enableConsole: boolean;
}
declare class EOLogger {
    private config;
    constructor(config?: Partial<LoggerConfig>);
    setLevel(level: LogLevel): void;
    setPrefix(prefix: string): void;
    debug(message: string, ...args: unknown[]): void;
    info(message: string, ...args: unknown[]): void;
    warn(message: string, ...args: unknown[]): void;
    error(message: string, ...args: unknown[]): void;
    log(message: string, ...args: unknown[]): void;
}
export declare const logger: EOLogger;
export declare const selfLearningLogger: EOLogger;
export declare const ruleLogger: EOLogger;
export declare const patchLogger: EOLogger;
export declare const trackerLogger: EOLogger;
export declare const hookLogger: EOLogger;
export declare const toolLogger: EOLogger;
export {};
//# sourceMappingURL=logger.d.ts.map