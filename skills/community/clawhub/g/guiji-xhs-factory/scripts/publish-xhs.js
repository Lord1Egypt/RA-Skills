#!/usr/bin/env node
// publish-xhs.js — 用 Playwright 自动发布小红书视频笔记
// 用法: node publish-xhs.js <video-path> <title> <content>
const { chromium } = require('/Users/houdaliang/.nvm/versions/node/v22.22.1/lib/node_modules/playwright');

const [,, videoPath, title, content] = process.argv;

if (!videoPath) {
  console.error('Usage: node publish-xhs.js <video-path> <title> <content>');
  process.exit(1);
}

const PUBLISH_URL = 'https://creator.xiaohongshu.com/publish/publish?from=homepage&target=video';

// React 受控组件赋值 hack
const SET_REACT_INPUT = `
const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
nativeSetter.call(this, value);
this.dispatchEvent(new Event('input', { bubbles: true }));
this.dispatchEvent(new Event('change', { bubbles: true }));
`;

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:18800');
  const context = browser.contexts()[0];
  
  // 打开新标签页
  const page = await context.newPage();
  await page.goto(PUBLISH_URL, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(3000);
  
  console.log('📄 页面加载完成');
  
  // 上传视频
  const fileInput = await page.$('input.upload-input');
  if (!fileInput) {
    console.error('❌ 找不到上传按钮');
    process.exit(1);
  }
  
  // 点击触发 filechooser，然后设置文件
  const [fileChooser] = await Promise.all([
    page.waitForEvent('filechooser', { timeout: 10000 }),
    page.click('.cover-container, .upload-area, [class*="upload"]')
  ]);
  
  await fileChooser.setFiles(videoPath);
  console.log(`🎬 视频已上传: ${videoPath}`);
  
  // 等待上传完成
  await page.waitForTimeout(8000);
  
  // 填写标题（用 nativeInputValueSetter 绕过 React）
  if (title) {
    await page.evaluate(({ selector, value }) => {
      const el = document.querySelector(selector);
      if (el) {
        const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        nativeSetter.call(el, value);
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
      }
    }, { selector: 'input[placeholder*="标题"]', value: title });
    console.log(`📝 标题: ${title}`);
  }
  
  // 填写正文
  if (content) {
    await page.evaluate(({ selector, value }) => {
      const el = document.querySelector(selector);
      if (el && el.contentEditable === 'true') {
        el.innerHTML = value.split('\n').map(l => `<p>${l || '<br>'}</p>`).join('');
        el.dispatchEvent(new Event('input', { bubbles: true }));
      }
    }, { selector: '[contenteditable="true"]', value: content });
    console.log('📝 正文已填写');
  }
  
  // 等待一下确保所有内容就绪
  await page.waitForTimeout(2000);
  
  console.log('✅ 发布准备完成！请手动点击"发布"按钮');
  console.log('⚠️ 不自动点击发布，由你确认后手动发布');
  
  // 不关闭浏览器，让用户手动确认发布
  // browser.close() 不调用
}

main().catch(e => {
  console.error('❌ 错误:', e.message);
  process.exit(1);
});
