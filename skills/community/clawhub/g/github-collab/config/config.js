/**
 * 统一配置文件
 * 整合环境变量、数据库配置、Agent 配置等
 */

// 环境变量
require('dotenv').config();

module.exports = {
  // 应用配置
  app: {
    name: 'github-collab',
    version: '2.0.0',
    port: process.env.PORT || 3000,
    env: process.env.NODE_ENV || 'development'
  },

  // 数据库配置
  database: {
    path: process.env.DB_PATH || './src/db/github-collab.db',
    backupPath: process.env.DB_BACKUP_PATH || './src/db/backup',
    maxConnections: parseInt(process.env.DB_MAX_CONNECTIONS) || 10
  },

  // 缓存配置
  cache: {
    maxSize: parseInt(process.env.CACHE_MAX_SIZE) || 1000,
    defaultTTL: parseInt(process.env.CACHE_DEFAULT_TTL) || 3600000, // 1 小时
    enabled: process.env.CACHE_ENABLED !== 'false'
  },

  // Agent 配置
  agent: {
    defaultTimeout: parseInt(process.env.AGENT_DEFAULT_TIMEOUT) || 300000, // 5 分钟
    maxRetries: parseInt(process.env.AGENT_MAX_RETRIES) || 3,
    healthCheckInterval: parseInt(process.env.AGENT_HEALTH_CHECK_INTERVAL) || 60000 // 1 分钟
  },

  // 任务配置
  task: {
    defaultPriority: 5,
    maxDependencies: 10,
    autoAssign: process.env.TASK_AUTO_ASSIGN !== 'false'
  },

  // 日志配置
  logger: {
    level: process.env.LOG_LEVEL || 'info',
    file: process.env.LOG_FILE || './logs/app.log',
    maxSize: process.env.LOG_MAX_SIZE || '10M',
    maxFiles: process.env.LOG_MAX_FILES || 5
  },

  // Git 配置
  git: {
    commitMessageFormat: process.env.GIT_COMMIT_MESSAGE_FORMAT || 'feat: %s',
    branchPrefix: process.env.GIT_BRANCH_PREFIX || 'feature/',
    autoCommit: process.env.GIT_AUTO_COMMIT !== 'false'
  },

  // GitHub API 配置
  github: {
    token: process.env.GITHUB_TOKEN,
    apiVersion: process.env.GITHUB_API_VERSION || '2022-11-28',
    rateLimit: {
      maxRequests: parseInt(process.env.GITHUB_RATE_LIMIT_MAX) || 5000,
      windowMs: parseInt(process.env.GITHUB_RATE_LIMIT_WINDOW) || 3600000 // 1 小时
    }
  },

  // 性能监控配置
  monitoring: {
    enabled: process.env.MONITORING_ENABLED !== 'false',
    reportInterval: parseInt(process.env.MONITORING_REPORT_INTERVAL) || 300000 // 5 分钟
  },

  // 测试配置
  test: {
    coverageThreshold: parseInt(process.env.TEST_COVERAGE_THRESHOLD) || 80,
    timeout: parseInt(process.env.TEST_TIMEOUT) || 10000
  }
};