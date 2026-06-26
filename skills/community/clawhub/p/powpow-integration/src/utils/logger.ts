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

const LOG_LEVELS: Record<LogLevel, number> = {
  debug: 0,
  info: 1,
  warn: 2,
  error: 3,
};

class Logger {
  private config: LoggerConfig;

  constructor(config: Partial<LoggerConfig> = {}) {
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
  private shouldLog(level: LogLevel): boolean {
    if (!this.config.enabled) return false;
    return LOG_LEVELS[level] >= LOG_LEVELS[this.config.level];
  }

  /**
   * 格式化日志消息
   */
  private format(level: LogLevel, message: string): string {
    const timestamp = new Date().toISOString();
    return `${timestamp} ${this.config.prefix} [${level.toUpperCase()}] ${message}`;
  }

  /**
   * 输出调试日志
   */
  debug(message: string, ...args: any[]): void {
    if (this.shouldLog('debug')) {
      console.debug(this.format('debug', message), ...args);
    }
  }

  /**
   * 输出信息日志
   */
  info(message: string, ...args: any[]): void {
    if (this.shouldLog('info')) {
      console.info(this.format('info', message), ...args);
    }
  }

  /**
   * 输出警告日志
   */
  warn(message: string, ...args: any[]): void {
    if (this.shouldLog('warn')) {
      console.warn(this.format('warn', message), ...args);
    }
  }

  /**
   * 输出错误日志
   */
  error(message: string, ...args: any[]): void {
    if (this.shouldLog('error')) {
      console.error(this.format('error', message), ...args);
    }
  }

  /**
   * 设置日志级别
   */
  setLevel(level: LogLevel): void {
    this.config.level = level;
  }

  /**
   * 启用/禁用日志
   */
  setEnabled(enabled: boolean): void {
    this.config.enabled = enabled;
  }
}

// 默认导出单例
export const logger = new Logger();
export { Logger };
