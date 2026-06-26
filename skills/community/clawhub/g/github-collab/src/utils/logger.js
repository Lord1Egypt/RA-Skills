/**
 * Logger - 日志工具
 */

const fs = require('fs');
const path = require('path');

/**
 * 日志级别
 */
const LogLevel = {
  DEBUG: 0,
  INFO: 1,
  WARN: 2,
  ERROR: 3
};

/**
 * 日志级别名称
 */
const LogLevelNames = {
  0: 'DEBUG',
  1: 'INFO',
  2: 'WARN',
  3: 'ERROR'
};

/**
 * 创建日志记录器
 */
function createLogger(options = {}) {
  let currentLevel = options.level || 'INFO';
  let currentLogLevel = (LogLevel[currentLevel] !== undefined) ? LogLevel[currentLevel] : LogLevel.INFO;
  const logFile = options.file || null;
  
  // 确保日志目录存在
  if (logFile) {
    const logDir = path.dirname(logFile);
    if (!fs.existsSync(logDir)) {
      fs.mkdirSync(logDir, { recursive: true });
    }
  }
  
  /**
   * 格式化日志消息（支持 printf 风格）
   */
  function formatMessage(level, message, meta, ...args) {
    const timestamp = new Date().toISOString();
    const levelName = LogLevelNames[level];
    
    // 处理非字符串消息
    if (typeof message !== 'string') {
      message = String(message);
    }
    
    // 处理 printf 风格的格式化
    let formattedMessage = message;
    if (args.length > 0) {
      // 使用正则表达式替换所有 %s 和 %d
      let argIndex = 0;
      formattedMessage = formattedMessage.replace(/%[sd]/g, (match) => {
        if (argIndex < args.length) {
          return args[argIndex++];
        }
        return match;
      });
    }
    
    const metaStr = Object.keys(meta).length > 0 ? JSON.stringify(meta) : '';
    
    return `[${timestamp}] [${levelName}] ${formattedMessage}${metaStr ? ' ' + metaStr : ''}`;
  }
  
  /**
   * 写入日志文件
   */
  function writeToFile(message) {
    if (!logFile) return;
    
    try {
      fs.appendFileSync(logFile, message + '\n');
    } catch (error) {
      console.error('Failed to write log file:', error.message);
    }
  }
  
  /**
   * 输出日志
   */
  function log(level, message, meta = {}, ...args) {
    if (level < currentLogLevel) return;
    
    const formatted = formatMessage(level, message, meta, ...args);
    
    // 控制台输出
    switch (level) {
      case LogLevel.DEBUG:
        console.debug(formatted);
        break;
      case LogLevel.INFO:
        console.log(formatted);
        break;
      case LogLevel.WARN:
        console.warn(formatted);
        break;
      case LogLevel.ERROR:
        console.error(formatted);
        break;
      default:
        console.log(formatted);
    }
    
    // 文件输出
    writeToFile(formatted);
  }
  
  const logger = {
    debug: (message, meta = {}, ...args) => log(LogLevel.DEBUG, message, meta, ...args),
    info: (message, meta = {}, ...args) => log(LogLevel.INFO, message, meta, ...args),
    warn: (message, meta = {}, ...args) => log(LogLevel.WARN, message, meta, ...args),
    error: (message, meta = {}, ...args) => log(LogLevel.ERROR, message, meta, ...args),
    setLevel: (newLevel) => {
      // 就地修改日志级别
      if (typeof newLevel === 'string') {
        currentLogLevel = (LogLevel[newLevel] !== undefined) ? LogLevel[newLevel] : currentLogLevel;
      } else if (typeof newLevel === 'number') {
        currentLogLevel = newLevel;
      }
      return logger;
    }
  };
  
  return logger;
}

// 默认日志记录器
const defaultLogger = createLogger();

module.exports = {
  LogLevel,
  LogLevelNames,
  createLogger,
  defaultLogger
};
