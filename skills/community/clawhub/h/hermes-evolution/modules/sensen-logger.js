/**
 * SENSEN Logger - P2-1 日志结构化
 * 从 console.log → JSON+级别+上下文
 * 
 * 支持：
 * 1. 多级别：DEBUG / INFO / WARN / ERROR
 * 2. 上下文：module / taskId / agent / correlationId
 * 3. 输出：控制台（彩色）+ 文件（JSON）
 * 4. 可配置：按模块/级别过滤
 */

const fs = require('fs');
const path = require('path');

const LOG_DIR = path.join(__dirname, 'logs');
const LOG_FILE = path.join(LOG_DIR, `sensen-${new Date().toISOString().split('T')[0]}.log`);

// 日志级别
const LogLevel = {
  DEBUG: 0,
  INFO: 1,
  WARN: 2,
  ERROR: 3
};

const LevelNames = ['DEBUG', 'INFO', 'WARN', 'ERROR'];

// 颜色代码
const Colors = {
  DEBUG: '\x1b[36m',   // 青色
  INFO: '\x1b[32m',    // 绿色
  WARN: '\x1b[33m',    // 黄色
  ERROR: '\x1b[31m',   // 红色
  RESET: '\x1b[0m'
};

/**
 * Logger 类
 */
class SensenLogger {
  constructor(options = {}) {
    this.name = options.name || 'SENSEN';
    this.level = options.level || LogLevel.INFO;
    this.showTimestamp = options.showTimestamp !== false;
    this.showModule = options.showModule !== false;
    this.outputToFile = options.outputToFile !== false;
    
    // 确保日志目录存在
    if (this.outputToFile && !fs.existsSync(LOG_DIR)) {
      fs.mkdirSync(LOG_DIR, { recursive: true });
    }
  }

  /**
   * 格式化日志消息
   */
  format(level, levelName, message, context = {}) {
    const entry = {
      timestamp: new Date().toISOString(),
      level: levelName,
      levelValue: level,
      name: this.name,
      message,
      pid: process.pid,
      ...context
    };

    // 添加调用位置（简化）
    if (context._caller) {
      entry.caller = context._caller;
      delete entry._caller;
    }

    return entry;
  }

  /**
   * 输出到控制台（彩色）
   */
  toConsole(entry) {
    const color = Colors[entry.level] || Colors.RESET;
    const parts = [];

    if (this.showTimestamp) {
      const time = new Date(entry.timestamp).toLocaleTimeString('zh-CN', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        fractionalSecondDigits: 3
      });
      parts.push(`\x1b[90m${time}\x1b[0m`);
    }

    parts.push(`${color}[${entry.level}]\x1b[0m`);

    if (this.showModule) {
      parts.push(`\x1b[35m${entry.name}\x1b[0m`);
    }

    parts.push(entry.message);

    // 如果有上下文，附加关键信息
    if (entry.taskId) {
      parts.push(`\x1b[90m[task:${entry.taskId.slice(-8)}]\x1b[0m`);
    }
    if (entry.agent) {
      parts.push(`\x1b[90m[@${entry.agent}]\x1b[0m`);
    }

    console.log(parts.join(' '));
  }

  /**
   * 输出到文件（JSON）
   */
  toFile(entry) {
    if (!this.outputToFile) return;

    const line = JSON.stringify(entry) + '\n';
    fs.appendFileSync(LOG_FILE, line, 'utf-8');
  }

  /**
   * 记录日志
   */
  log(level, levelName, message, context = {}) {
    if (level < this.level) return;

    // 捕获调用位置
    const err = new Error();
    const stack = err.stack.split('\n');
    if (stack[3]) {
      const match = stack[3].match(/\/([^\/]+:\d+:\d+)/);
      if (match) {
        context._caller = match[1];
      }
    }

    const entry = this.format(level, levelName, message, context);
    this.toConsole(entry);
    this.toFile(entry);

    return entry;
  }

  /**
   * DEBUG 级别
   */
  debug(message, context = {}) {
    return this.log(LogLevel.DEBUG, 'DEBUG', message, context);
  }

  /**
   * INFO 级别
   */
  info(message, context = {}) {
    return this.log(LogLevel.INFO, 'INFO', message, context);
  }

  /**
   * WARN 级别
   */
  warn(message, context = {}) {
    return this.log(LogLevel.WARN, 'WARN', message, context);
  }

  /**
   * ERROR 级别
   */
  error(message, context = {}) {
    return this.log(LogLevel.ERROR, 'ERROR', message, context);
  }

  /**
   * 创建子Logger（带模块名）
   */
  child(moduleName) {
    return new SensenLogger({
      name: `${this.name}/${moduleName}`,
      level: this.level,
      showTimestamp: this.showTimestamp,
      showModule: this.showModule,
      outputToFile: this.outputToFile
    });
  }
}

// 全局默认Logger
const defaultLogger = new SensenLogger({
  name: 'SENSEN',
  level: LogLevel.INFO,
  outputToFile: true
});

/**
 * 快捷函数
 */
function createLogger(name, level) {
  return new SensenLogger({ name, level: level || LogLevel.INFO });
}

// 导出
module.exports = {
  SensenLogger,
  SensenLogger: SensenLogger,
  LogLevel,
  LevelNames,
  createLogger,
  defaultLogger,
  LOG_DIR,
  LOG_FILE
};
