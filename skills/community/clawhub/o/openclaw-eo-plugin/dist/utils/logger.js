/**
 * EO Logger Utility
 *
 * Unified logging utility for EO plugin
 * Can be replaced with OpenClaw api.logger when available
 */
export var LogLevel;
(function (LogLevel) {
    LogLevel[LogLevel["DEBUG"] = 0] = "DEBUG";
    LogLevel[LogLevel["INFO"] = 1] = "INFO";
    LogLevel[LogLevel["WARN"] = 2] = "WARN";
    LogLevel[LogLevel["ERROR"] = 3] = "ERROR";
})(LogLevel || (LogLevel = {}));
const DEFAULT_CONFIG = {
    level: LogLevel.INFO,
    prefix: '[EO]',
    enableConsole: true,
};
class EOLogger {
    config;
    constructor(config = {}) {
        this.config = { ...DEFAULT_CONFIG, ...config };
    }
    setLevel(level) {
        this.config.level = level;
    }
    setPrefix(prefix) {
        this.config.prefix = prefix;
    }
    debug(message, ...args) {
        if (this.config.level <= LogLevel.DEBUG && this.config.enableConsole) {
            console.debug(`${this.config.prefix} ${message}`, ...args);
        }
    }
    info(message, ...args) {
        if (this.config.level <= LogLevel.INFO && this.config.enableConsole) {
            console.info(`${this.config.prefix} ${message}`, ...args);
        }
    }
    warn(message, ...args) {
        if (this.config.level <= LogLevel.WARN && this.config.enableConsole) {
            console.warn(`${this.config.prefix} ${message}`, ...args);
        }
    }
    error(message, ...args) {
        if (this.config.level <= LogLevel.ERROR && this.config.enableConsole) {
            console.error(`${this.config.prefix} ${message}`, ...args);
        }
    }
    log(message, ...args) {
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
//# sourceMappingURL=logger.js.map