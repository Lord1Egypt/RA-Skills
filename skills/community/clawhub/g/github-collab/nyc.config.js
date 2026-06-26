/**
 * Istanbul/NYC Coverage Configuration
 */

module.exports = {
  // 报告格式
  reporter: ['text', 'html', 'lcov', 'text-summary'],
  
  // 报告输出目录
  reportDir: 'coverage',
  
  // 覆盖率阈值
  thresholds: {
    global: {
      lines: 80,
      functions: 80,
      branches: 80,
      statements: 80
    }
  },
  
  // 排除的文件
  exclude: [
    'tests/**',
    'coverage/**',
    'node_modules/**',
    '**/*.test.js',
    '**/*.spec.js',
    'scripts/**',
    'config.local.js'
  ],
  
  // 包含的文件
  include: [
    'utils.js',
    'config.js',
    'logger.js',
    'db.js',
    'db-optimized.js',
    'cache.js',
    'agent.js',
    'worker.js',
    'api/**',
    'services/**',
    'middleware/**'
  ],
  
  // 检查覆盖率
  check-coverage: true,
  
  // 覆盖率检查选项
  branches: 80,
  lines: 80,
  functions: 80,
  statements: 80,
  
  // 是否生成覆盖率徽章
  watermarks: {
    statements: [50, 80],
    lines: [50, 80],
    functions: [50, 80],
    branches: [50, 80]
  },
  
  // 临时文件目录
  tempDir: '.nyc_output',
  
  // 是否清除临时文件
  clean: true,
  
  // 是否清除报告目录
  cleanTempFiles: true,
  
  // 扩展名
  extension: ['.js'],
  
  // 是否使用 instrumenter
  instrumenter: './node_modules/@istanbuljs/nyc-config-babel/node_modules/babel-plugin-istanbul',
  
  // 是否并行运行测试
  parallel: false,
  
  // 是否使用 worker 线程
  useSpawnWrap: true,
  
  // 是否使用 cache
  cache: true,
  
  // 缓存目录
  cacheDir: '.nyc_output/cache'
};
