/**
 * EO Logger Utility
 * 
 * Unified logging utility for EO plugin
 * Can be replaced with OpenClaw api.logger when available
 */

export enum LogLevel {
  DEBUG = 0,
  INFO = 1,
  WARN = 2,
  ERROR = 3,
}

export interface LoggerConfig {
  level: LogLevel;
  prefix?: string;
  enableConsole: boolean;
}

const DEFAULT_CONFIG: LoggerConfig = {
  level: LogLevel.INFO,
  prefix: '[EO]',
  enableConsole: true,
};

class EOLogger {
  private config: LoggerConfig;

  constructor(config: Partial<LoggerConfig> = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
  }

  setLevel(level: LogLevel): void {
    this.config.level = level;
  }

  setPrefix(prefix: string): void {
    this.config.prefix = prefix;
  }

  debug(message: string, ...args: unknown[]): void {
    if (this.config.level <= LogLevel.DEBUG && this.config.enableConsole) {
      console.debug(`${this.config.prefix} ${message}`, ...args);
    }
  }

  info(message: string, ...args: unknown[]): void {
    if (this.config.level <= LogLevel.INFO && this.config.enableConsole) {
      console.info(`${this.config.prefix} ${message}`, ...args);
    }
  }

  warn(message: string, ...args: unknown[]): void {
    if (this.config.level <= LogLevel.WARN && this.config.enableConsole) {
      console.warn(`${this.config.prefix} ${message}`, ...args);
    }
  }

  error(message: string, ...args: unknown[]): void {
    if (this.config.level <= LogLevel.ERROR && this.config.enableConsole) {
      console.error(`${this.config.prefix} ${message}`, ...args);
    }
  }

  log(message: string, ...args: unknown[]): void {
    if (this.config.enableConsole) {
      console.log(`${this.config.prefix} ${message}`, ...args);
    }
  }
}

// Global logger instance
export const logger = new EOLogger({
  level: LogLevel.INFO,
  prefix: '[EO]',
  enableConsole: true,
});

// Convenience loggers for different modules
export const selfLearningLogger = new EOLogger({ prefix: '[SelfLearning]' });
export const ruleLogger = new EOLogger({ prefix: '[RuleStorage]' });
export const patchLogger = new EOLogger({ prefix: '[PatchManager]' });
export const trackerLogger = new EOLogger({ prefix: '[EffectTracker]' });
export const hookLogger = new EOLogger({ prefix: '[Hook]' });
export const toolLogger = new EOLogger({ prefix: '[Tool]' });
