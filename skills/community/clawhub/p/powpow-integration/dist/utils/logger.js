"use strict";
/**
 * 日志工具
 * 提供分级日志功能
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.Logger = exports.logger = void 0;
const LOG_LEVELS = {
    debug: 0,
    info: 1,
    warn: 2,
    error: 3,
};
class Logger {
    constructor(config = {}) {
        this.config = {
            level: 'info',
            prefix: '[PowPow Skill]',
            enabled: true,
            ...config,
        };
    }
    /**
     * 检查日志级别是否允许输出
     */
    shouldLog(level) {
        if (!this.config.enabled)
            return false;
        return LOG_LEVELS[level] >= LOG_LEVELS[this.config.level];
    }
    /**
     * 格式化日志消息
     */
    format(level, message) {
        const timestamp = new Date().toISOString();
        return `${timestamp} ${this.config.prefix} [${level.toUpperCase()}] ${message}`;
    }
    /**
     * 输出调试日志
     */
    debug(message, ...args) {
        if (this.shouldLog('debug')) {
            console.debug(this.format('debug', message), ...args);
        }
    }
    /**
     * 输出信息日志
     */
    info(message, ...args) {
        if (this.shouldLog('info')) {
            console.info(this.format('info', message), ...args);
        }
    }
    /**
     * 输出警告日志
     */
    warn(message, ...args) {
        if (this.shouldLog('warn')) {
            console.warn(this.format('warn', message), ...args);
        }
    }
    /**
     * 输出错误日志
     */
    error(message, ...args) {
        if (this.shouldLog('error')) {
            console.error(this.format('error', message), ...args);
        }
    }
    /**
     * 设置日志级别
     */
    setLevel(level) {
        this.config.level = level;
    }
    /**
     * 启用/禁用日志
     */
    setEnabled(enabled) {
        this.config.enabled = enabled;
    }
}
exports.Logger = Logger;
// 默认导出单例
exports.logger = new Logger();
//# sourceMappingURL=logger.js.map