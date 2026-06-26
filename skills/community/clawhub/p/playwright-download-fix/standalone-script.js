/**
 * 独立运行的 Playwright 下载脚本
 * 启动浏览器后可以手动操作，自动处理下载文件名
 */

const { chromium } = require('playwright');
const DownloadHelper = require('./download-helper');

async function run() {
  const realChromeUA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36';

  console.log('🚀 启动 Playwright 下载助手...');
  console.log('');

  // 启动浏览器
  const browser = await chromium.launch({
    headless: false  // 显示浏览器窗口
  });

  // 创建上下文（带反检测配置）
  const context = await browser.newContext({
    userAgent: realChromeUA,
    locale: 'zh-CN',
    timezoneId: 'Asia/Shanghai',
    bypassCSP: true,
    javaScriptEnabled: true,
    acceptDownloads: true,
  });

  const page = await context.newPage();

  // 初始化下载助手
  const helper = new DownloadHelper(page, {
    downloadDir: '~/downloads',
    debug: true
  });
  const downloadDir = await helper.setup();

  console.log('========================================');
  console.log('📋 配置信息');
  console.log('========================================');
  console.log('🌐 User-Agent:', realChromeUA);
  console.log('📂 下载目录:', downloadDir);
  console.log('🔍 调试模式: 开启');
  console.log('========================================');
  console.log('');
  console.log('💡 现在可以在浏览器中进行下载操作');
  console.log('⏱️  浏览器将在 30 分钟后自动关闭');
  console.log('');

  // 自动导航到指定URL
  console.log('🌐 正在打开: https://rd6.zhaopin.com/app/search');
  await page.goto('https://rd6.zhaopin.com/app/search');
  console.log('✅ 页面已打开，请手动登录...\n');

  // 保持运行 30 分钟
  await page.waitForTimeout(1800000);

  // 输出下载总结
  const downloadedFiles = helper.getDownloadedFiles();
  console.log('');
  console.log('========================================');
  console.log('📊 下载总结');
  console.log('========================================');
  if (downloadedFiles.length > 0) {
    console.log(`✅ 共下载 ${downloadedFiles.length} 个文件:`);
    downloadedFiles.forEach((file, index) => {
      console.log(`   ${index + 1}. ${file}`);
    });
  } else {
    console.log('⚠️  没有检测到下载');
  }
  console.log('========================================');

  await browser.close();
}

run().catch(error => {
  console.error('❌ 发生错误:', error);
  process.exit(1);
});
