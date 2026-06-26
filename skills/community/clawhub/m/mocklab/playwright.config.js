import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',

  // 测试超时时间
  timeout: 30 * 1000,

  // 断言超时
  expect: {
    timeout: 5000
  },

  // 失败时重试次数
  fullyParallel: false,
  retries: process.env.CI ? 2 : 0,

  // 并发执行的 worker 数量
  workers: process.env.CI ? 1 : 3,

  // 测试报告
  reporter: [
    ['html', { outputFolder: 'test-results/html' }],
    ['list'],
    ['json', { outputFile: 'test-results/results.json' }]
  ],

  use: {
    // 基础 URL
    baseURL: 'http://localhost:18080',

    // 截图设置
    screenshot: 'only-on-failure',

    // 视频录制
    video: 'retain-on-failure',

    // 追踪
    trace: 'on-first-retry',

    // 浏览器设置
    viewport: { width: 1280, height: 720 },
    ignoreHTTPSErrors: true,

    // 设置较长的超时，防止异步加载问题
    actionTimeout: 10000,
    navigationTimeout: 30000,
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    // 如果需要测试更多浏览器，取消注释
    // {
    //   name: 'firefox',
    //   use: { ...devices['Desktop Firefox'] },
    // },
    // {
    //   name: 'webkit',
    //   use: { ...devices['Desktop Safari'] },
    // },
  ],

  // 测试前启动 MockLab 服务器（可选）
  // webServer: {
  //   command: 'python mock_server.py --port 18080',
  //   url: 'http://localhost:18080',
  //   timeout: 120 * 1000,
  //   reuseExistingServer: !process.env.CI,
  // },
});
