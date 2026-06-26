/**
 * 日志工具
 */
declare class Logger {
    private prefix;
    private formatMessage;
    debug(message: string, ...args: any[]): void;
    info(message: string, ...args: any[]): void;
    warn(message: string, ...args: any[]): void;
    error(message: string, ...args: any[]): void;
}
export declare const logger: Logger;
export {};
