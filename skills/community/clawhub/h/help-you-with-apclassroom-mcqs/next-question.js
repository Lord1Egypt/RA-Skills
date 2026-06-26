const { chromium } = require('C:/Users/ASUS/.openclaw/workspace/node_modules/playwright');

/**
 * 点击 Next 进入下一题
 * 
 * 使用方法：
 * node next-question.js
 */

(async () => {
  let browser;
  try {
    console.log('🔌 连接到浏览器...\n');
    browser = await chromium.connectOverCDP('http://localhost:9223');
    
    const context = browser.contexts()[0];
    const page = context.pages()[0];
    
    console.log(`📍 当前页面: ${page.url()}\n`);
    
    // 查找 Next 按钮
    const nextBtn = await page.$('button:has-text("Next")');
    
    if (nextBtn) {
      console.log('🖱️ 点击 Next...');
      await nextBtn.click({ force: true });
      await page.waitForTimeout(5000);
      
      console.log('✅ 已进入下一题');
      console.log('\n💡 下一步: node get-questions.js 获取新题目');
      
    } else {
      // 可能是最后一题，检查是否有 Submit
      const submitBtn = await page.$('button:has-text("Submit")');
      
      if (submitBtn) {
        console.log('⚠️ 这是最后一题！');
        console.log('💡 使用 node submit-quiz.js 提交测验');
      } else {
        console.log('❌ 未找到 Next 或 Submit 按钮');
      }
    }
    
  } catch (error) {
    console.error('❌ 错误:', error.message);
  } finally {
    // ⚠️ 重要：只断开连接，不关闭浏览器
    if (browser) {
      browser.close();
      console.log('\n🔌 已断开连接（浏览器保持打开）');
    }
  }
})();
