/**
 * 示例：在 Playwright 自动化脚本中使用 DownloadHelper
 */

const { chromium } = require('playwright');
const DownloadHelper = require('./download-helper');

async function example() {
  // 1. 启动浏览器
  const browser = await chromium.launch({
    headless: false  // 显示浏览器窗口
  });

  // 2. 创建上下文（带反检测配置）
  const realChromeUA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36';

  const context = await browser.newContext({
    userAgent: realChromeUA,
    locale: 'zh-CN',
    timezoneId: 'Asia/Shanghai',
    bypassCSP: true,
    acceptDownloads: true,
  });

  const page = await context.newPage();

  // 3. 初始化下载助手
  const helper = new DownloadHelper(page, {
    downloadDir: '~/downloads',
    debug: true
  });
  const downloadDir = await helper.setup();
  console.log(`📂 下载目录: ${downloadDir}`);

  // 4. 访问网站并下载
  await page.goto('https://example.com');
  // await page.click('#download-button');  // 根据实际情况选择

  // 5. 等待下载完成
  await page.waitForTimeout(5000);

  // 6. 获取下载的文件
  const downloadedFiles = helper.getDownloadedFiles();
  console.log('✅ 下载的文件:', downloadedFiles);

  await browser.close();
}

// 运行示例
if (require.main === module) {
  example().catch(console.error);
}

module.exports = { example };
