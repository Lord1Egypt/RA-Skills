/**
 * CLI 命令解析器
 */
/**
 * 命令参数
 */
export interface CommandArgs {
    action: string;
    target?: string;
    arg?: string;
    tags?: string[];
    format?: 'markdown' | 'json';
}
/**
 * 命令解析结果
 */
export interface ParsedCommand {
    action: string;
    target?: {
        user: string;
        host: string;
        port?: number;
    };
    arg?: string;
    tags?: string[];
    format: 'markdown' | 'json';
}
/**
 * 命令解析器
 */
export declare class CommandParser {
    private static readonly VALID_ACTIONS;
    /**
     * 解析命令行参数
     */
    parse(args: string[]): ParsedCommand;
    /**
     * 是否为有效操作
     */
    private isValidAction;
    /**
     * 解析剩余参数
     */
    private parseRest;
    /**
     * 解析目标服务器 (user@host:port)
     */
    private parseTarget;
    /**
     * 获取帮助信息
     */
    getHelp(): string;
}
//# sourceMappingURL=CommandDispatcher.d.ts.map