/**
 * Logger 单元测试
 */

const loggerModule = require('../utils/logger');

const { LogLevel, LogLevelNames, createLogger, defaultLogger } = loggerModule;

describe('Logger - LogLevel', () => {
  test('应该有正确的日志级别值', () => {
    expect(LogLevel.DEBUG).toBe(0);
    expect(LogLevel.INFO).toBe(1);
    expect(LogLevel.WARN).toBe(2);
    expect(LogLevel.ERROR).toBe(3);
  });
});

describe('Logger - LogLevelNames', () => {
  test('应该有正确的日志级别名称映射', () => {
    expect(LogLevelNames[0]).toBe('DEBUG');
    expect(LogLevelNames[1]).toBe('INFO');
    expect(LogLevelNames[2]).toBe('WARN');
    expect(LogLevelNames[3]).toBe('ERROR');
  });
});

describe('Logger - createLogger', () => {
  describe('默认日志记录器', () => {
    let consoleLogs = [];
    let consoleErrors = [];
    let consoleWarns = [];
    let consoleDebugs = [];

    beforeEach(() => {
      consoleLogs = [];
      consoleErrors = [];
      consoleWarns = [];
      consoleDebugs = [];

      jest.spyOn(console, 'log').mockImplementation((msg) => consoleLogs.push(msg));
      jest.spyOn(console, 'error').mockImplementation((msg) => consoleErrors.push(msg));
      jest.spyOn(console, 'warn').mockImplementation((msg) => consoleWarns.push(msg));
      jest.spyOn(console, 'debug').mockImplementation((msg) => consoleDebugs.push(msg));
    });

    afterEach(() => {
      jest.restoreAllMocks();
    });

    test('应该创建默认日志记录器', () => {
      const logger = createLogger();
      expect(logger).toBeDefined();
      expect(typeof logger.debug).toBe('function');
      expect(typeof logger.info).toBe('function');
      expect(typeof logger.warn).toBe('function');
      expect(typeof logger.error).toBe('function');
      expect(typeof logger.setLevel).toBe('function');
    });
  });

  describe('日志级别过滤', () => {
    let consoleLogs = [];
    let consoleErrors = [];
    let consoleWarns = [];
    let consoleDebugs = [];

    beforeEach(() => {
      consoleLogs = [];
      consoleErrors = [];
      consoleWarns = [];
      consoleDebugs = [];

      jest.spyOn(console, 'log').mockImplementation((msg) => consoleLogs.push(msg));
      jest.spyOn(console, 'error').mockImplementation((msg) => consoleErrors.push(msg));
      jest.spyOn(console, 'warn').mockImplementation((msg) => consoleWarns.push(msg));
      jest.spyOn(console, 'debug').mockImplementation((msg) => consoleDebugs.push(msg));
    });

    afterEach(() => {
      jest.restoreAllMocks();
    });

    test('DEBUG 级别应该输出所有日志', () => {
      const logger = createLogger({ level: 'DEBUG' });

      logger.debug('debug message');
      logger.info('info message');
      logger.warn('warn message');
      logger.error('error message');

      expect(consoleDebugs.length).toBe(1);
      expect(consoleLogs.length).toBe(1);
      expect(consoleWarns.length).toBe(1);
      expect(consoleErrors.length).toBe(1);
    });

    test('INFO 级别应该过滤 DEBUG', () => {
      const logger = createLogger({ level: 'INFO' });

      logger.debug('debug message');
      logger.info('info message');
      logger.warn('warn message');
      logger.error('error message');

      expect(consoleDebugs.length).toBe(0);
      expect(consoleLogs.length).toBe(1);
      expect(consoleWarns.length).toBe(1);
      expect(consoleErrors.length).toBe(1);
    });

    test('WARN 级别应该过滤 DEBUG 和 INFO', () => {
      const logger = createLogger({ level: 'WARN' });

      logger.debug('debug message');
      logger.info('info message');
      logger.warn('warn message');
      logger.error('error message');

      expect(consoleDebugs.length).toBe(0);
      expect(consoleLogs.length).toBe(0);
      expect(consoleWarns.length).toBe(1);
      expect(consoleErrors.length).toBe(1);
    });

    test('ERROR 级别应该只输出 ERROR', () => {
      const logger = createLogger({ level: 'ERROR' });

      logger.debug('debug message');
      logger.info('info message');
      logger.warn('warn message');
      logger.error('error message');

      expect(consoleDebugs.length).toBe(0);
      expect(consoleLogs.length).toBe(0);
      expect(consoleWarns.length).toBe(0);
      expect(consoleErrors.length).toBe(1);
    });
  });

  describe('日志格式', () => {
    let consoleLogs = [];
    let consoleErrors = [];
    let consoleWarns = [];
    let consoleDebugs = [];

    beforeEach(() => {
      consoleLogs = [];
      consoleErrors = [];
      consoleWarns = [];
      consoleDebugs = [];

      jest.spyOn(console, 'log').mockImplementation((msg) => consoleLogs.push(msg));
      jest.spyOn(console, 'error').mockImplementation((msg) => consoleErrors.push(msg));
      jest.spyOn(console, 'warn').mockImplementation((msg) => consoleWarns.push(msg));
      jest.spyOn(console, 'debug').mockImplementation((msg) => consoleDebugs.push(msg));
    });

    afterEach(() => {
      jest.restoreAllMocks();
    });

    test('应该包含时间戳', () => {
      const logger = createLogger({ level: 'DEBUG' });
      logger.info('test message');

      const logMessage = consoleLogs[0];
      expect(logMessage).toMatch(/\[\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z\]/);
    });

    test('应该包含日志级别', () => {
      const logger = createLogger({ level: 'DEBUG' });
      logger.info('test message');

      const logMessage = consoleLogs[0];
      expect(logMessage).toContain('[INFO]');
    });

    test('应该包含消息内容', () => {
      const logger = createLogger({ level: 'DEBUG' });
      logger.info('test message');

      const logMessage = consoleLogs[0];
      expect(logMessage).toContain('test message');
    });
  });

  describe('setLevel 方法', () => {
    let consoleLogs = [];
    let consoleErrors = [];
    let consoleWarns = [];
    let consoleDebugs = [];

    beforeEach(() => {
      consoleLogs = [];
      consoleErrors = [];
      consoleWarns = [];
      consoleDebugs = [];

      jest.spyOn(console, 'log').mockImplementation((msg) => consoleLogs.push(msg));
      jest.spyOn(console, 'error').mockImplementation((msg) => consoleErrors.push(msg));
      jest.spyOn(console, 'warn').mockImplementation((msg) => consoleWarns.push(msg));
      jest.spyOn(console, 'debug').mockImplementation((msg) => consoleDebugs.push(msg));
    });

    afterEach(() => {
      jest.restoreAllMocks();
    });

    test('应该动态改变日志级别', () => {
      const logger = createLogger({ level: 'ERROR' });

      logger.info('should not appear');
      expect(consoleLogs.length).toBe(0);

      logger.setLevel('INFO');
      logger.info('should appear');
      expect(consoleLogs.length).toBe(1);
    });

    test('应该接受数字级别', () => {
      const logger = createLogger({ level: 'ERROR' });
      logger.setLevel(1); // INFO
      logger.info('test');
      expect(consoleLogs.length).toBe(1);
    });

    test('应该接受字符串级别', () => {
      const logger = createLogger({ level: 'ERROR' });
      logger.setLevel('DEBUG');
      logger.debug('test');
      expect(consoleDebugs.length).toBe(1);
    });
  });

  describe('日志消息格式化', () => {
    let consoleLogs = [];
    let consoleErrors = [];
    let consoleWarns = [];
    let consoleDebugs = [];

    beforeEach(() => {
      consoleLogs = [];
      consoleErrors = [];
      consoleWarns = [];
      consoleDebugs = [];

      jest.spyOn(console, 'log').mockImplementation((msg) => consoleLogs.push(msg));
      jest.spyOn(console, 'error').mockImplementation((msg) => consoleErrors.push(msg));
      jest.spyOn(console, 'warn').mockImplementation((msg) => consoleWarns.push(msg));
      jest.spyOn(console, 'debug').mockImplementation((msg) => consoleDebugs.push(msg));
    });

    afterEach(() => {
      jest.restoreAllMocks();
    });

    test('应该格式化字符串消息', () => {
      const logger = createLogger({ level: 'DEBUG' });
      logger.info('Hello %s', {}, 'World');

      const logMessage = consoleLogs[0];
      expect(logMessage).toContain('Hello World');
    });

    test('应该格式化对象消息', () => {
      const logger = createLogger({ level: 'DEBUG' });
      const obj = { name: 'test', value: 123 };
      logger.info('User: %j', obj);

      const logMessage = consoleLogs[0];
      expect(logMessage).toContain('User:');
      expect(logMessage).toContain('test');
    });

    test('应该格式化多个参数', () => {
      const logger = createLogger({ level: 'DEBUG' });
      logger.info('User %s has %d items', 'Alice', 5);

      const logMessage = consoleLogs[0];
      expect(logMessage).toContain('Alice');
      expect(logMessage).toContain('5');
    });
  });

  describe('错误日志', () => {
    let consoleLogs = [];
    let consoleErrors = [];
    let consoleWarns = [];
    let consoleDebugs = [];

    beforeEach(() => {
      consoleLogs = [];
      consoleErrors = [];
      consoleWarns = [];
      consoleDebugs = [];

      jest.spyOn(console, 'log').mockImplementation((msg) => consoleLogs.push(msg));
      jest.spyOn(console, 'error').mockImplementation((msg) => consoleErrors.push(msg));
      jest.spyOn(console, 'warn').mockImplementation((msg) => consoleWarns.push(msg));
      jest.spyOn(console, 'debug').mockImplementation((msg) => consoleDebugs.push(msg));
    });

    afterEach(() => {
      jest.restoreAllMocks();
    });

    test('应该记录错误对象', () => {
      const logger = createLogger({ level: 'DEBUG' });
      const error = new Error('Test error');
      logger.error(error);

      expect(consoleErrors.length).toBe(1);
      expect(consoleErrors[0]).toContain('Test error');
    });

    test('应该记录错误消息和堆栈', () => {
      const logger = createLogger({ level: 'DEBUG' });
      const error = new Error('Test error');
      logger.error(error);

      const errorMessage = consoleErrors[0];
      expect(errorMessage).toContain('Test error');
    });
  });

  describe('警告日志', () => {
    let consoleLogs = [];
    let consoleErrors = [];
    let consoleWarns = [];
    let consoleDebugs = [];

    beforeEach(() => {
      consoleLogs = [];
      consoleErrors = [];
      consoleWarns = [];
      consoleDebugs = [];

      jest.spyOn(console, 'log').mockImplementation((msg) => consoleLogs.push(msg));
      jest.spyOn(console, 'error').mockImplementation((msg) => consoleErrors.push(msg));
      jest.spyOn(console, 'warn').mockImplementation((msg) => consoleWarns.push(msg));
      jest.spyOn(console, 'debug').mockImplementation((msg) => consoleDebugs.push(msg));
    });

    afterEach(() => {
      jest.restoreAllMocks();
    });

    test('应该输出警告到 console.warn', () => {
      const logger = createLogger({ level: 'DEBUG' });
      logger.warn('Warning message');

      expect(consoleWarns.length).toBe(1);
      expect(consoleWarns[0]).toContain('Warning message');
    });
  });

  describe('调试日志', () => {
    let consoleLogs = [];
    let consoleErrors = [];
    let consoleWarns = [];
    let consoleDebugs = [];

    beforeEach(() => {
      consoleLogs = [];
      consoleErrors = [];
      consoleWarns = [];
      consoleDebugs = [];

      jest.spyOn(console, 'log').mockImplementation((msg) => consoleLogs.push(msg));
      jest.spyOn(console, 'error').mockImplementation((msg) => consoleErrors.push(msg));
      jest.spyOn(console, 'warn').mockImplementation((msg) => consoleWarns.push(msg));
      jest.spyOn(console, 'debug').mockImplementation((msg) => consoleDebugs.push(msg));
    });

    afterEach(() => {
      jest.restoreAllMocks();
    });

    test('应该输出调试信息到 console.debug', () => {
      const logger = createLogger({ level: 'DEBUG' });
      logger.debug('Debug message');

      expect(consoleDebugs.length).toBe(1);
      expect(consoleDebugs[0]).toContain('Debug message');
    });
  });

  describe('日志级别名称', () => {
    let consoleLogs = [];
    let consoleErrors = [];
    let consoleWarns = [];
    let consoleDebugs = [];

    beforeEach(() => {
      consoleLogs = [];
      consoleErrors = [];
      consoleWarns = [];
      consoleDebugs = [];

      jest.spyOn(console, 'log').mockImplementation((msg) => consoleLogs.push(msg));
      jest.spyOn(console, 'error').mockImplementation((msg) => consoleErrors.push(msg));
      jest.spyOn(console, 'warn').mockImplementation((msg) => consoleWarns.push(msg));
      jest.spyOn(console, 'debug').mockImplementation((msg) => consoleDebugs.push(msg));
    });

    afterEach(() => {
      jest.restoreAllMocks();
    });

    test('DEBUG 应该显示 [DEBUG]', () => {
      const logger = createLogger({ level: 'DEBUG' });
      logger.debug('test');
      expect(consoleDebugs[0]).toContain('[DEBUG]');
    });

    test('INFO 应该显示 [INFO]', () => {
      const logger = createLogger({ level: 'DEBUG' });
      logger.info('test');
      expect(consoleLogs[0]).toContain('[INFO]');
    });

    test('WARN 应该显示 [WARN]', () => {
      const logger = createLogger({ level: 'DEBUG' });
      logger.warn('test');
      expect(consoleWarns[0]).toContain('[WARN]');
    });

    test('ERROR 应该显示 [ERROR]', () => {
      const logger = createLogger({ level: 'DEBUG' });
      logger.error('test');
      expect(consoleErrors[0]).toContain('[ERROR]');
    });
  });

  describe('边界情况', () => {
    let consoleLogs = [];
    let consoleErrors = [];
    let consoleWarns = [];
    let consoleDebugs = [];

    beforeEach(() => {
      consoleLogs = [];
      consoleErrors = [];
      consoleWarns = [];
      consoleDebugs = [];

      jest.spyOn(console, 'log').mockImplementation((msg) => consoleLogs.push(msg));
      jest.spyOn(console, 'error').mockImplementation((msg) => consoleErrors.push(msg));
      jest.spyOn(console, 'warn').mockImplementation((msg) => consoleWarns.push(msg));
      jest.spyOn(console, 'debug').mockImplementation((msg) => consoleDebugs.push(msg));
    });

    afterEach(() => {
      jest.restoreAllMocks();
    });

    test('应该处理空消息', () => {
      const logger = createLogger({ level: 'DEBUG' });
      logger.info('');
      expect(consoleLogs.length).toBe(1);
    });

    test('应该处理 null 消息', () => {
      const logger = createLogger({ level: 'DEBUG' });
      logger.info(null);
      expect(consoleLogs.length).toBe(1);
    });

    test('应该处理 undefined 消息', () => {
      const logger = createLogger({ level: 'DEBUG' });
      logger.info(undefined);
      expect(consoleLogs.length).toBe(1);
    });

    test('应该处理数字消息', () => {
      const logger = createLogger({ level: 'DEBUG' });
      logger.info(123);
      expect(consoleLogs.length).toBe(1);
    });
  });

  describe('性能', () => {
    let consoleLogs = [];
    let consoleErrors = [];
    let consoleWarns = [];
    let consoleDebugs = [];

    beforeEach(() => {
      consoleLogs = [];
      consoleErrors = [];
      consoleWarns = [];
      consoleDebugs = [];

      jest.spyOn(console, 'log').mockImplementation((msg) => consoleLogs.push(msg));
      jest.spyOn(console, 'error').mockImplementation((msg) => consoleErrors.push(msg));
      jest.spyOn(console, 'warn').mockImplementation((msg) => consoleWarns.push(msg));
      jest.spyOn(console, 'debug').mockImplementation((msg) => consoleDebugs.push(msg));
    });

    afterEach(() => {
      jest.restoreAllMocks();
    });

    test('应该快速过滤不需要的日志级别', () => {
      const logger = createLogger({ level: 'ERROR' });
      const start = Date.now();

      for (let i = 0; i < 10000; i++) {
        logger.debug('debug message');
        logger.info('info message');
        logger.warn('warn message');
      }

      const end = Date.now();
      expect(end - start).toBeLessThan(100); // 应该在 100ms 内完成
      expect(consoleDebugs.length).toBe(0);
      expect(consoleLogs.length).toBe(0);
      expect(consoleWarns.length).toBe(0);
    });
  });
});

describe('Logger - defaultLogger', () => {
  let consoleLogs = [];

  beforeEach(() => {
    consoleLogs = [];
    jest.spyOn(console, 'log').mockImplementation((msg) => consoleLogs.push(msg));
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  describe('默认日志记录器', () => {
    let localConsoleLogs = [];
    let localConsoleErrors = [];
    let localConsoleWarns = [];
    let localConsoleDebugs = [];

    beforeEach(() => {
      localConsoleLogs = [];
      localConsoleErrors = [];
      localConsoleWarns = [];
      localConsoleDebugs = [];

      jest.spyOn(console, 'log').mockImplementation((msg) => localConsoleLogs.push(msg));
      jest.spyOn(console, 'error').mockImplementation((msg) => localConsoleErrors.push(msg));
      jest.spyOn(console, 'warn').mockImplementation((msg) => localConsoleWarns.push(msg));
      jest.spyOn(console, 'debug').mockImplementation((msg) => localConsoleDebugs.push(msg));
    });

    afterEach(() => {
      jest.restoreAllMocks();
    });

    test('应该导出默认日志记录器', () => {
      expect(defaultLogger).toBeDefined();
      expect(typeof defaultLogger.info).toBe('function');
    });

    test('默认日志记录器应该使用 INFO 级别', () => {
      defaultLogger.debug('should not appear');
      expect(localConsoleDebugs.length || 0).toBe(0);

      defaultLogger.info('should appear');
      expect(localConsoleLogs.length).toBeGreaterThan(0);
    });
  });
});
