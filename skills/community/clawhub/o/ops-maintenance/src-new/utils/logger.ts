/**
 * 日志工具
 * 基于 Winston 的结构化日志
 */

import winston from 'winston'

/**
 * 日志级别
 */
export enum LogLevel {
  DEBUG = 'debug',
  INFO = 'info',
  WARN = 'warn',
  ERROR = 'error'
}

/**
 * 日志格式
 */
const logFormat = winston.format.combine(
  winston.format.timestamp(),
  winston.format.errors({ stack: true }),
  winston.format.json()
)

/**
 * 控制台格式（开发环境）
 */
const consoleFormat = winston.format.combine(
  winston.format.colorize(),
  winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
  winston.format.printf(({ timestamp, level, message, ...meta }) => {
    let metaStr = ''
    if (Object.keys(meta).length > 0) {
      metaStr = ` ${JSON.stringify(meta)}`
    }
    return `${timestamp} [${level.toUpperCase()}] ${message}${metaStr}`
  })
)

/**
 * 日志级别映射
 */
const LEVEL_TO_WINSTON: Record<string, string> = {
  debug: 'debug',
  info: 'info',
  warn: 'warn',
  error: 'error'
}

/**
 *  Logger 单例类
 */
export class Logger {
  private static instance: Logger | null = null
  private logger: winston.Logger

  private constructor(private context?: string) {
    const transports = [
      new winston.transports.Console({
        format: process.env.NODE_ENV === 'production' ? logFormat : consoleFormat
      })
    ]

    this.logger = winston.createLogger({
      level: process.env.OPS_LOG_LEVEL || 'info',
      format: logFormat,
      transports,
      exceptionHandlers: transports,
      rejectionHandlers: transports
    })
  }

  /**
   * 获取全局 Logger 实例
   */
  static getLogger(context?: string): Logger {
    if (!Logger.instance) {
      Logger.instance = new Logger(context)
    }
    if (context && !Logger.instance['context']) {
      Logger.instance['context'] = context
    }
    return Logger.instance
  }

  /**
   * 设置日志级别
   */
  static setLevel(level: LogLevel | string): void {
    const winstonLogger = Logger.getInstance().logger
    winstonLogger.level = LEVEL_TO_WINSTON[level] || 'info'
  }

  private static getInstance(): Logger {
    if (!Logger.instance) {
      Logger.instance = new Logger()
    }
    return Logger.instance
  }

  /**
   * 记录 Debug 日志
   */
  debug(message: string, meta?: any): void {
    this.log('debug', message, meta)
  }

  /**
   * 记录 Info 日志
   */
  info(message: string, meta?: any): void {
    this.log('info', message, meta)
  }

  /**
   * 记录 Warn 日志
   */
  warn(message: string, meta?: any): void {
    this.log('warn', message, meta)
  }

  /**
   * 记录 Error 日志
   */
  error(message: string, error?: Error | any): void {
    if (error instanceof Error) {
      this.log('error', message, { error: error.message, stack: error.stack })
    } else {
      this.log('error', message, { error })
    }
  }

  /**
   * 通用日志方法
   */
  private log(level: string, message: string, meta?: any): void {
    const context = this['context'] ? `[${this['context']}] ` : ''
    const fullMessage = `${context}${message}`

    if (meta) {
      this.logger.log(level, fullMessage, meta)
    } else {
      this.logger.log(level, fullMessage)
    }
  }

  /**
   * 记录请求（HTTP）
   */
  httpRequest(method: string, url: string, statusCode: number, duration: number): void {
    this.info(`${method} ${url} ${statusCode}`, { duration, statusCode })
  }

  /**
   * 记录 SSH 命令执行
   */
  sshCommand(server: string, command: string, duration: number, success: boolean): void {
    const level = success ? 'debug' : 'error'
    this.log(level, `SSH ${server}: ${command}`, { server, command, duration, success })
  }

  /**
   * 记录配置变更
   */
  configChange(type: string, details: any): void {
    this.info(`配置变更: ${type}`, details)
  }
}