/**
 * Jest Configuration
 * 
 * 单元测试框架配置
 */

module.exports = {
  // 测试环境
  testEnvironment: 'node',
  
  // 测试文件匹配模式
  testMatch: [
    '**/src/tests/**/*.test.js',
    '**/src/**/*.test.js',
    '**/tests/**/*.test.js',
    '**/tests/**/*.spec.js'
  ],
  
  // 测试文件排除模式
  testPathIgnorePatterns: [
    '/node_modules/',
    '/coverage/',
    '/dist/'
  ],
  
  // 模块名称映射
  moduleNameMapper: {},
  
  // 模块路径别名
  moduleDirectories: [
    'node_modules',
    '<rootDir>'
  ],
  
  // 模块文件扩展名
  moduleFileExtensions: [
    'js',
    'json',
    'node'
  ],
  
  // 覆盖率收集的文件
  collectCoverageFrom: [
    '**/*.js',
    '!**/node_modules/**',
    '!**/tests/**',
    '!**/coverage/**',
    '!**/*.test.js',
    '!**/*.spec.js',
    '!**/scripts/**',
    '!**/*.config.js'
  ],
  
  // 覆盖率阈值
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  },
  
  // 覆盖率报告格式
  coverageReporters: [
    'text',
    'html',
    'lcov',
    'text-summary'
  ],
  
  // 覆盖率报告目录
  coverageDirectory: 'coverage',
  
  // 覆盖率水印
  coveragePathIgnorePatterns: [
    '/node_modules/',
    '/tests/',
    '/coverage/',
    '/scripts/'
  ],
  
  // 是否收集覆盖率
  collectCoverage: true,
  
  // 覆盖率缓存
  // coverageCache: true,
  
  // 是否清除覆盖率缓存
  clearMocks: true,
  
  // 是否重置模块状态
  resetMocks: false,
  
  // 是否恢复 spies
  restoreMocks: false,
  
  // 是否重置模块
  resetModules: false,
  
  // 测试超时时间（毫秒）
  testTimeout: 10000,
  
  // 是否随机运行测试
  randomize: false,
  
  // 是否并行运行测试
  maxWorkers: '50%',
  
  // 是否使用缓存
  cache: true,
  
  // 缓存目录
  cacheDirectory: '<rootDir>/.jest_cache',
  
  // 是否检测全局变量泄漏
  detectLeaks: false,
  
  // 是否检测 Open Handles
  detectOpenHandles: false,
  
  // 错误栈跟踪
  errorOnDeprecated: false,
  
  // 是否强制退出
  forceExit: false,
  
  // 是否全局安装
  globalSetup: null,
  globalTeardown: null,
  
  // 全局变量
  globals: {},
  
  // 钩子
  setupFiles: [],
  setupFilesAfterEnv: [],
  
  // 预处理器
  transform: {},
  
  // 预处理器忽略
  transformIgnorePatterns: [
    '/node_modules/'
  ],
  
  // 快照目录
  snapshotSerializers: [],
  
  // 是否更新快照
  updateSnapshot: false,
  
  // 是否使用 verbose 模式
  verbose: true,
  
  // 是否显示提示信息
  // watchPlugins: [
  //   'jest-watch-typeahead/filename',
  //   'jest-watch-typeahead/testname'
  // ],
  
  // 是否静默
  silent: false,
  
  // 是否显示堆栈跟踪
  bail: false,
  
  // 是否只运行失败的测试
  onlyFailures: false
};
