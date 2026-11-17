"use strict";
/**
 * 日志工具
 * 基于 Winston 的结构化日志
 */
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.Logger = exports.LogLevel = void 0;
const winston_1 = __importDefault(require("winston"));
/**
 * 日志级别
 */
var LogLevel;
(function (LogLevel) {
    LogLevel["DEBUG"] = "debug";
    LogLevel["INFO"] = "info";
    LogLevel["WARN"] = "warn";
    LogLevel["ERROR"] = "error";
})(LogLevel || (exports.LogLevel = LogLevel = {}));
/**
 * 日志格式
 */
const logFormat = winston_1.default.format.combine(winston_1.default.format.timestamp(), winston_1.default.format.errors({ stack: true }), winston_1.default.format.json());
/**
 * 控制台格式（开发环境）
 */
const consoleFormat = winston_1.default.format.combine(winston_1.default.format.colorize(), winston_1.default.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }), winston_1.default.format.printf(({ timestamp, level, message, ...meta }) => {
    let metaStr = '';
    if (Object.keys(meta).length > 0) {
        metaStr = ` ${JSON.stringify(meta)}`;
    }
    return `${timestamp} [${level.toUpperCase()}] ${message}${metaStr}`;
}));
/**
 * 日志级别映射
 */
const LEVEL_TO_WINSTON = {
    debug: 'debug',
    info: 'info',
    warn: 'warn',
    error: 'error'
};
/**
 *  Logger 单例类
 */
class Logger {
    constructor(context) {
        this.context = context;
        const transports = [
            new winston_1.default.transports.Console({
                format: process.env.NODE_ENV === 'production' ? logFormat : consoleFormat
            })
        ];
        this.logger = winston_1.default.createLogger({
            level: process.env.OPS_LOG_LEVEL || 'info',
            format: logFormat,
            transports,
            exceptionHandlers: transports,
            rejectionHandlers: transports
        });
    }
    /**
     * 获取全局 Logger 实例
     */
    static getLogger(context) {
        if (!Logger.instance) {
            Logger.instance = new Logger(context);
        }
        if (context && !Logger.instance['context']) {
            Logger.instance['context'] = context;
        }
        return Logger.instance;
    }
    /**
     * 设置日志级别
     */
    static setLevel(level) {
        const winstonLogger = Logger.getInstance().logger;
        winstonLogger.level = LEVEL_TO_WINSTON[level] || 'info';
    }
    static getInstance() {
        if (!Logger.instance) {
            Logger.instance = new Logger();
        }
        return Logger.instance;
    }
    /**
     * 记录 Debug 日志
     */
    debug(message, meta) {
        this.log('debug', message, meta);
    }
    /**
     * 记录 Info 日志
     */
    info(message, meta) {
        this.log('info', message, meta);
    }
    /**
     * 记录 Warn 日志
     */
    warn(message, meta) {
        this.log('warn', message, meta);
    }
    /**
     * 记录 Error 日志
     */
    error(message, error) {
        if (error instanceof Error) {
            this.log('error', message, { error: error.message, stack: error.stack });
        }
        else {
            this.log('error', message, { error });
        }
    }
    /**
     * 通用日志方法
     */
    log(level, message, meta) {
        const context = this['context'] ? `[${this['context']}] ` : '';
        const fullMessage = `${context}${message}`;
        if (meta) {
            this.logger.log(level, fullMessage, meta);
        }
        else {
            this.logger.log(level, fullMessage);
        }
    }
    /**
     * 记录请求（HTTP）
     */
    httpRequest(method, url, statusCode, duration) {
        this.info(`${method} ${url} ${statusCode}`, { duration, statusCode });
    }
    /**
     * 记录 SSH 命令执行
     */
    sshCommand(server, command, duration, success) {
        const level = success ? 'debug' : 'error';
        this.log(level, `SSH ${server}: ${command}`, { server, command, duration, success });
    }
    /**
     * 记录配置变更
     */
    configChange(type, details) {
        this.info(`配置变更: ${type}`, details);
    }
}
exports.Logger = Logger;
Logger.instance = null;
//# sourceMappingURL=logger.js.map