const { chromium } = require('C:/Users/ASUS/.openclaw/workspace/node_modules/playwright');

/**
 * 提交测验
 * 
 * 使用方法：
 * node submit-quiz.js
 * 
 * ⚠️ 注意：此操作会提交测验，请确认所有题目都已回答
 */

(async () => {
  let browser;
  try {
    console.log('🔌 连接到浏览器...\n');
    browser = await chromium.connectOverCDP('http://localhost:9223');
    
    const context = browser.contexts()[0];
    const page = context.pages()[0];
    
    console.log(`📍 当前页面: ${page.url()}\n`);
    
    console.log('⚠️ 准备提交测验...');
    console.log('💡 请确认所有题目都已回答\n');
    
    // 截图当前状态
    await page.screenshot({ path: 'before-submit.png', fullPage: true });
    console.log('📸 已保存提交前截图: before-submit.png');
    
    // 查找 Submit 按钮
    const submitBtn = await page.$('button:has-text("Submit")');
    
    if (submitBtn) {
      console.log('\n🖱️ 点击 Submit...');
      await submitBtn.click({ force: true });
      await page.waitForTimeout(3000);
      
      // 查找确认按钮
      const confirmBtn = await page.$('button:has-text("Yes"), button:has-text("Confirm")');
      
      if (confirmBtn) {
        console.log('🖱️ 确认提交...');
        await confirmBtn.click({ force: true });
        await page.waitForTimeout(5000);
        
        console.log('✅ 测验已提交！');
        
        // 截图提交后状态
        await page.screenshot({ path: 'after-submit.png', fullPage: true });
        console.log('📸 已保存提交后截图: after-submit.png');
        
        // 尝试返回 Dashboard
        const exitBtn = await page.$('button:has-text("Exit"), a:has-text("Exit")');
        if (exitBtn) {
          console.log('\n🖱️ 点击 Exit 返回 Dashboard...');
          await exitBtn.click({ force: true });
          await page.waitForTimeout(5000);
          console.log('✅ 已返回 Dashboard');
        }
        
      } else {
        console.log('⚠️ 未找到确认按钮，可能需要手动确认');
      }
      
    } else {
      console.log('❌ 未找到 Submit 按钮');
      console.log('💡 可能还没有到最后一题，使用 node next-question.js 继续');
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
