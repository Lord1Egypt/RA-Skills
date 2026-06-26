/**
 * Configuration Manager
 * 配置管理模块
 */

const fs = require('fs');
const path = require('path');

/**
 * 默认配置
 */
const DEFAULT_CONFIG = {
  db: {
    type: 'better-sqlite3',
    path: './db/gitwork.db',
    host: 'localhost',
    port: 3306,
    pool: {
      min: 2,
      max: 10
    }
  },
  log: {
    level: 'INFO',
    file: './logs/app.log'
  },
  agent: {
    heartbeatInterval: 5 * 60 * 1000,
    syncInterval: 10 * 60 * 1000
  }
};

/**
 * 从环境变量加载配置
 */
function loadFromEnv() {
  const envConfig = {};
  
  // 数据库配置
  if (process.env.DB_TYPE || process.env.DB_PATH || process.env.DB_HOST || process.env.DB_PORT || process.env.DB_USER || process.env.DB_PASSWORD || process.env.DB_NAME || process.env.DB_POOL_MIN || process.env.DB_POOL_MAX || process.env.DB_POOL_ACQUIRE_TIMEOUT || process.env.DB_POOL_IDLE_TIMEOUT) {
    envConfig.db = {};
    if (process.env.DB_TYPE) envConfig.db.type = process.env.DB_TYPE;
    if (process.env.DB_PATH) envConfig.db.path = process.env.DB_PATH;
    if (process.env.DB_HOST) envConfig.db.host = process.env.DB_HOST;
    if (process.env.DB_PORT) envConfig.db.port = parseInt(process.env.DB_PORT);
    if (process.env.DB_USER) envConfig.db.user = process.env.DB_USER;
    if (process.env.DB_PASSWORD) envConfig.db.password = process.env.DB_PASSWORD;
    if (process.env.DB_NAME) envConfig.db.database = process.env.DB_NAME;
    if (process.env.DB_POOL_MIN || process.env.DB_POOL_MAX || process.env.DB_POOL_ACQUIRE_TIMEOUT || process.env.DB_POOL_IDLE_TIMEOUT) {
      envConfig.db.pool = {};
      if (process.env.DB_POOL_MIN) envConfig.db.pool.min = parseInt(process.env.DB_POOL_MIN);
      if (process.env.DB_POOL_MAX) envConfig.db.pool.max = parseInt(process.env.DB_POOL_MAX);
      if (process.env.DB_POOL_ACQUIRE_TIMEOUT) envConfig.db.pool.acquireTimeout = parseInt(process.env.DB_POOL_ACQUIRE_TIMEOUT);
      if (process.env.DB_POOL_IDLE_TIMEOUT) envConfig.db.pool.idleTimeout = parseInt(process.env.DB_POOL_IDLE_TIMEOUT);
    }
  }
  
  // 日志配置
  if (process.env.LOG_LEVEL || process.env.LOG_FILE) {
    envConfig.log = {};
    if (process.env.LOG_LEVEL) envConfig.log.level = process.env.LOG_LEVEL;
    if (process.env.LOG_FILE) envConfig.log.file = process.env.LOG_FILE;
  }
  
  // Agent 配置 (环境变量中的值是分钟数，需要转换为毫秒)
  if (process.env.HEARTBEAT_INTERVAL || process.env.SYNC_INTERVAL) {
    envConfig.agent = {};
    if (process.env.HEARTBEAT_INTERVAL) envConfig.agent.heartbeatInterval = parseInt(process.env.HEARTBEAT_INTERVAL) * 60 * 1000;
    if (process.env.SYNC_INTERVAL) envConfig.agent.syncInterval = parseInt(process.env.SYNC_INTERVAL) * 60 * 1000;
  }
  
  return envConfig;
}

/**
 * 从自定义配置文件加载配置
 */
function loadFromCustomConfig(filePath) {
  if (!fs.existsSync(filePath)) {
    return {};
  }
  try {
    const fileConfig = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    return fileConfig;
  } catch (error) {
    console.warn('Failed to load custom config:', error.message);
    return {};
  }
}

/**
 * 深度合并对象
 */
function deepMerge(target, source) {
  const result = { ...target };
  
  for (const key in source) {
    if (source.hasOwnProperty(key)) {
      if (
        source[key] &&
        typeof source[key] === 'object' &&
        !Array.isArray(source[key]) &&
        target[key] &&
        typeof target[key] === 'object' &&
        !Array.isArray(target[key])
      ) {
        result[key] = deepMerge(target[key], source[key]);
      } else {
        result[key] = source[key];
      }
    }
  }
  
  return result;
}

/**
 * 合并配置
 */
function mergeConfigs(...configs) {
  return configs.reduce((acc, config) => deepMerge(acc, config), {});
}

class Config {
    constructor() {
        this.config = {};
        this.loaded = false;
    }

    /**
     * 加载配置
     */
    async load() {
        if (this.loaded) return;
        
        // 从环境变量加载
        this.config.github = {
            token: process.env.GITHUB_TOKEN || '',
            owner: process.env.GITHUB_OWNER || 'default-owner'
        };

        this.config.agents = {
            dev_count: parseInt(process.env.DEV_AGENT_COUNT) || 2,
            test_count: parseInt(process.env.TEST_AGENT_COUNT) || 1,
            review_count: parseInt(process.env.REVIEW_AGENT_COUNT) || 1
        };

        this.config.logging = {
            level: process.env.LOG_LEVEL || 'info',
            file: process.env.LOG_FILE || 'github-collab.log'
        };

        // 默认 QQ 配置（不依赖数据库）
        this.config.qq = {
            enabled: process.env.QQ_ENABLED === 'true',
            token: process.env.QQ_TOKEN || '',
            defaultTarget: process.env.QQ_TARGET || '',
            agentAddresses: {},
            dbConfigured: false
        };

        // 从配置文件加载（如果存在）
        const configPath = path.join(__dirname, '.github-collab-config.json');
        if (fs.existsSync(configPath)) {
            try {
                const fileConfig = JSON.parse(fs.readFileSync(configPath, 'utf8'));
                this.config = { ...this.config, ...fileConfig };
            } catch (error) {
                console.warn('Failed to load config file:', error.message);
            }
        }

        this.loaded = true;
        console.log('[Config] Configuration loaded');
    }

    /**
     * 获取配置
     * @param {string} key - 配置键（支持点号分隔）
     * @returns {any} - 配置值
     */
    get(key) {
        if (!this.loaded) {
            return this.config[key];
        }
        const keys = key.split('.');
        let value = this.config;
        for (const k of keys) {
            value = value?.[k];
        }
        return value;
    }

    /**
     * 获取全部配置
     * @returns {object} - 全部配置
     */
    getAll() {
        return this.config;
    }

    /**
     * 获取配置对象（兼容旧版 API）
     * @returns {object} - 配置对象
     */
    getConfig() {
        // 将 Config 类的配置转换为旧版 API 格式
        const config = this.config;
        return {
            db: {
                type: config.db?.type || DEFAULT_CONFIG.db.type,
                path: config.db?.path || DEFAULT_CONFIG.db.path,
                host: config.db?.host || DEFAULT_CONFIG.db.host,
                port: config.db?.port || DEFAULT_CONFIG.db.port,
                pool: config.db?.pool || DEFAULT_CONFIG.db.pool
            },
            log: {
                level: config.log?.level || DEFAULT_CONFIG.log.level,
                file: config.log?.file || DEFAULT_CONFIG.log.file
            },
            agent: {
                heartbeatInterval: config.agent?.heartbeatInterval || DEFAULT_CONFIG.agent.heartbeatInterval,
                syncInterval: config.agent?.syncInterval || DEFAULT_CONFIG.agent.syncInterval
            }
        };
    }

    /**
     * 设置配置
     * @param {string} key - 配置键
     * @param {any} value - 配置值
     */
    set(key, value) {
        const keys = key.split('.');
        let config = this.config;
        for (let i = 0; i < keys.length - 1; i++) {
            if (!config[keys[i]]) {
                config[keys[i]] = {};
            }
            config = config[keys[i]];
        }
        config[keys[keys.length - 1]] = value;
    }

    /**
     * 保存配置到文件
     */
    save() {
        const configPath = path.join(__dirname, '.github-collab-config.json');
        fs.writeFileSync(configPath, JSON.stringify(this.config, null, 2));
        console.log('[Config] Configuration saved to:', configPath);
    }

    /**
     * 重新加载配置
     */
    reload() {
        this.loaded = false;
        this.load();
    }
}

// 创建单例
const configInstance = new Config();

/**
 * 获取配置实例
 * @param {string} configPath - 可选的配置文件路径
 * @returns {object} - 配置对象
 */
function getConfig(configPath) {
    // 从默认配置开始
    const config = {
        db: { ...DEFAULT_CONFIG.db },
        log: { ...DEFAULT_CONFIG.log },
        agent: { ...DEFAULT_CONFIG.agent }
    };
    
    // 环境变量覆盖默认配置
    const envConfig = loadFromEnv();
    if (envConfig.db) config.db = { ...config.db, ...envConfig.db };
    if (envConfig.log) config.log = { ...config.log, ...envConfig.log };
    if (envConfig.agent) config.agent = { ...config.agent, ...envConfig.agent };
    
    // 如果提供了配置文件路径，加载该配置
    if (configPath) {
        const fs = require('fs');
        const path = require('path');
        
        const absolutePath = path.isAbsolute(configPath) ? configPath : path.join(process.cwd(), configPath);
        if (fs.existsSync(absolutePath)) {
            const fileConfig = JSON.parse(fs.readFileSync(absolutePath, 'utf8'));
            if (fileConfig.db) config.db = { ...config.db, ...fileConfig.db };
            if (fileConfig.log) config.log = { ...config.log, ...fileConfig.log };
            if (fileConfig.agent) config.agent = { ...config.agent, ...fileConfig.agent };
        }
    }
    
    return config;
}

/**
 * 初始化配置（异步）
 * @returns {Promise<void>}
 */
async function initConfig() {
    await configInstance.load();
}

module.exports = { 
  Config, 
  getConfig, 
  initConfig,
  DEFAULT_CONFIG,
  loadFromEnv,
  loadFromCustomConfig,
  mergeConfigs
};