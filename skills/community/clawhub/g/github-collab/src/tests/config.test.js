/**
 * Config 单元测试
 */

const configModule = require('../core/config-manager');

const { DEFAULT_CONFIG, getConfig, loadFromEnv, loadFromCustomConfig, mergeConfigs } = configModule;

describe('Config - DEFAULT_CONFIG', () => {
  test('应该有正确的默认结构', () => {
    expect(DEFAULT_CONFIG).toBeDefined();
    expect(DEFAULT_CONFIG.db).toBeDefined();
    expect(DEFAULT_CONFIG.log).toBeDefined();
    expect(DEFAULT_CONFIG.agent).toBeDefined();
  });

  test('数据库配置应该有默认值', () => {
    expect(DEFAULT_CONFIG.db.type).toBe('better-sqlite3');
    expect(DEFAULT_CONFIG.db.path).toBe('./db/gitwork.db');
    expect(DEFAULT_CONFIG.db.host).toBe('localhost');
    expect(DEFAULT_CONFIG.db.port).toBe(3306);
    expect(DEFAULT_CONFIG.db.pool).toBeDefined();
    expect(DEFAULT_CONFIG.db.pool.min).toBe(2);
    expect(DEFAULT_CONFIG.db.pool.max).toBe(10);
  });

  test('日志配置应该有默认值', () => {
    expect(DEFAULT_CONFIG.log.level).toBe('INFO');
    expect(DEFAULT_CONFIG.log.file).toBe('./logs/app.log');
  });

  test('Agent 配置应该有默认值', () => {
    expect(DEFAULT_CONFIG.agent.heartbeatInterval).toBe(5 * 60 * 1000);
    expect(DEFAULT_CONFIG.agent.syncInterval).toBe(10 * 60 * 1000);
  });
});

describe('Config - loadFromEnv', () => {
  beforeEach(() => {
    // 清理所有相关环境变量
    const envVars = Object.keys(process.env).filter(
      (k) =>
        k.startsWith('DB_') ||
        k.startsWith('LOG_') ||
        k.startsWith('HEARTBEAT_') ||
        k.startsWith('SYNC_')
    );
    envVars.forEach((k) => delete process.env[k]);
  });

  test('应该返回空对象当没有环境变量', () => {
    const result = loadFromEnv();
    expect(result).toEqual({});
  });

  test('应该从环境变量加载数据库类型', () => {
    process.env.DB_TYPE = 'mysql';
    const result = loadFromEnv();
    expect(result.db.type).toBe('mysql');
  });

  test('应该从环境变量加载数据库路径', () => {
    process.env.DB_PATH = '/custom/path.db';
    const result = loadFromEnv();
    expect(result.db.path).toBe('/custom/path.db');
  });

  test('应该从环境变量加载数据库主机', () => {
    process.env.DB_HOST = 'remote.host.com';
    const result = loadFromEnv();
    expect(result.db.host).toBe('remote.host.com');
  });

  test('应该从环境变量加载数据库端口', () => {
    process.env.DB_PORT = '5432';
    const result = loadFromEnv();
    expect(result.db.port).toBe(5432);
  });

  test('应该从环境变量加载数据库用户', () => {
    process.env.DB_USER = 'admin';
    const result = loadFromEnv();
    expect(result.db.user).toBe('admin');
  });

  test('应该从环境变量加载数据库密码', () => {
    process.env.DB_PASSWORD = 'secret123';
    const result = loadFromEnv();
    expect(result.db.password).toBe('secret123');
  });

  test('应该从环境变量加载数据库名称', () => {
    process.env.DB_NAME = 'myapp';
    const result = loadFromEnv();
    expect(result.db.database).toBe('myapp');
  });

  test('应该从环境变量加载连接池配置', () => {
    process.env.DB_POOL_MIN = '5';
    process.env.DB_POOL_MAX = '20';
    process.env.DB_POOL_ACQUIRE_TIMEOUT = '60000';
    process.env.DB_POOL_IDLE_TIMEOUT = '30000';
    const result = loadFromEnv();
    expect(result.db.pool.min).toBe(5);
    expect(result.db.pool.max).toBe(20);
    expect(result.db.pool.acquireTimeout).toBe(60000);
    expect(result.db.pool.idleTimeout).toBe(30000);
  });

  test('应该从环境变量加载日志级别', () => {
    process.env.LOG_LEVEL = 'DEBUG';
    const result = loadFromEnv();
    expect(result.log.level).toBe('DEBUG');
  });

  test('应该从环境变量加载日志文件路径', () => {
    process.env.LOG_FILE = '/var/log/app.log';
    const result = loadFromEnv();
    expect(result.log.file).toBe('/var/log/app.log');
  });

  test('应该从环境变量加载心跳间隔', () => {
    process.env.HEARTBEAT_INTERVAL = '10';
    const result = loadFromEnv();
    expect(result.agent.heartbeatInterval).toBe(10 * 60 * 1000);
  });

  test('应该从环境变量加载同步间隔', () => {
    process.env.SYNC_INTERVAL = '15';
    const result = loadFromEnv();
    expect(result.agent.syncInterval).toBe(15 * 60 * 1000);
  });

  test('应该合并所有环境变量', () => {
    process.env.DB_TYPE = 'postgres';
    process.env.DB_HOST = 'db.example.com';
    process.env.LOG_LEVEL = 'ERROR';
    const result = loadFromEnv();
    expect(result.db.type).toBe('postgres');
    expect(result.db.host).toBe('db.example.com');
    expect(result.log.level).toBe('ERROR');
  });
});

describe('Config - loadFromCustomConfig', () => {
  test('应该返回空对象当路径为空', () => {
    expect(loadFromCustomConfig(null)).toEqual({});
    expect(loadFromCustomConfig('')).toEqual({});
    expect(loadFromCustomConfig()).toEqual({});
  });

  test('应该返回空对象当文件不存在', () => {
    const result = loadFromCustomConfig('/nonexistent/path/config.json');
    expect(result).toEqual({});
  });

  test('应该从自定义文件加载配置', () => {
    const fs = require('fs');
    const path = require('path');
    const testConfig = {
      db: { type: 'sqlite', path: ':memory:' },
      log: { level: 'DEBUG' }
    };
    const testPath = path.join(__dirname, 'test-config.json');

    try {
      fs.writeFileSync(testPath, JSON.stringify(testConfig));
      const result = loadFromCustomConfig(testPath);
      expect(result.db.type).toBe('sqlite');
      expect(result.db.path).toBe(':memory:');
      expect(result.log.level).toBe('DEBUG');
    } finally {
      if (fs.existsSync(testPath)) {
        fs.unlinkSync(testPath);
      }
    }
  });

  test('应该返回空对象当配置文件无效', () => {
    const fs = require('fs');
    const path = require('path');
    const testPath = path.join(__dirname, 'invalid-config.json');

    try {
      fs.writeFileSync(testPath, 'invalid json {');
      const result = loadFromCustomConfig(testPath);
      expect(result).toEqual({});
    } finally {
      if (fs.existsSync(testPath)) {
        fs.unlinkSync(testPath);
      }
    }
  });
});

describe('Config - mergeConfigs', () => {
  test('应该合并三个配置对象', () => {
    const defaults = { a: 1, b: 2 };
    const env = { b: 3 };
    const custom = { c: 4 };

    const result = mergeConfigs(defaults, env, custom);
    expect(result.a).toBe(1);
    expect(result.b).toBe(3);
    expect(result.c).toBe(4);
  });

  test('自定义配置应该覆盖环境变量', () => {
    const defaults = { db: { type: 'sqlite' } };
    const env = { db: { type: 'mysql' } };
    const custom = { db: { type: 'postgres' } };

    const result = mergeConfigs(defaults, env, custom);
    expect(result.db.type).toBe('postgres');
  });

  test('环境变量应该覆盖默认配置', () => {
    const defaults = { db: { type: 'sqlite' } };
    const env = { db: { type: 'mysql' } };
    const custom = {};

    const result = mergeConfigs(defaults, env, custom);
    expect(result.db.type).toBe('mysql');
  });

  test('应该递归合并嵌套对象', () => {
    const defaults = { db: { host: 'localhost', port: 3306 } };
    const env = { db: { host: 'remote.com' } };
    const custom = {};

    const result = mergeConfigs(defaults, env, custom);
    expect(result.db.host).toBe('remote.com');
    expect(result.db.port).toBe(3306);
  });

  test('应该正确处理嵌套的 pool 配置', () => {
    const defaults = {
      db: {
        pool: { min: 2, max: 10, acquireTimeout: 30000 }
      }
    };
    const env = {
      db: {
        pool: { min: 5, max: 20 }
      }
    };
    const custom = {};

    const result = mergeConfigs(defaults, env, custom);
    expect(result.db.pool.min).toBe(5);
    expect(result.db.pool.max).toBe(20);
    expect(result.db.pool.acquireTimeout).toBe(30000);
  });
});

describe('Config - getConfig', () => {
  beforeEach(() => {
    // 清理所有相关环境变量
    const envVars = Object.keys(process.env).filter(
      (k) =>
        k.startsWith('DB_') ||
        k.startsWith('LOG_') ||
        k.startsWith('HEARTBEAT_') ||
        k.startsWith('SYNC_')
    );
    envVars.forEach((k) => delete process.env[k]);
  });

  test('应该返回默认配置当没有环境变量和自定义配置', () => {
    const result = getConfig();
    expect(result.db.type).toBe('better-sqlite3');
    expect(result.db.path).toBe('./db/gitwork.db');
    expect(result.log.level).toBe('INFO');
  });

  test('应该使用环境变量覆盖默认配置', () => {
    process.env.DB_TYPE = 'mysql';
    process.env.LOG_LEVEL = 'DEBUG';

    const result = getConfig();
    expect(result.db.type).toBe('mysql');
    expect(result.log.level).toBe('DEBUG');
    // 其他配置应该保持默认
    expect(result.db.path).toBe('./db/gitwork.db');
  });

  test('应该使用自定义配置覆盖默认配置', () => {
    const fs = require('fs');
    const path = require('path');
    const testConfig = {
      db: { type: 'sqlite', path: ':memory:' }
    };
    const testPath = path.join(__dirname, 'test-get-config.json');

    try {
      fs.writeFileSync(testPath, JSON.stringify(testConfig));
      const result = getConfig(testPath);
      expect(result.db.type).toBe('sqlite');
      expect(result.db.path).toBe(':memory:');
    } finally {
      if (fs.existsSync(testPath)) {
        fs.unlinkSync(testPath);
      }
    }
  });

  test('自定义配置应该优先于环境变量', () => {
    process.env.DB_TYPE = 'mysql';

    const fs = require('fs');
    const path = require('path');
    const testConfig = { db: { type: 'postgres' } };
    const testPath = path.join(__dirname, 'test-priority.json');

    try {
      fs.writeFileSync(testPath, JSON.stringify(testConfig));
      const result = getConfig(testPath);
      expect(result.db.type).toBe('postgres');
    } finally {
      if (fs.existsSync(testPath)) {
        fs.unlinkSync(testPath);
      }
    }
  });

  test('应该保留默认配置中未覆盖的值', () => {
    process.env.DB_TYPE = 'mysql';

    const result = getConfig();
    expect(result.db.type).toBe('mysql');
    expect(result.db.host).toBe('localhost'); // 默认值
    expect(result.db.port).toBe(3306); // 默认值
    expect(result.log.level).toBe('INFO'); // 默认值
    expect(result.agent.heartbeatInterval).toBe(5 * 60 * 1000); // 默认值
  });
});
