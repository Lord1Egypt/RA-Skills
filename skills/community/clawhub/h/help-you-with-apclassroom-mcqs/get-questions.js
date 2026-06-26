const { chromium } = require('C:/Users/ASUS/.openclaw/workspace/node_modules/playwright');

/**
 * 获取当前打开的作业题目
 * 
 * 使用方法：
 * node get-questions.js
 * 
 * ⚠️ 前提：已经在浏览器中打开了某个作业
 */

(async () => {
  let browser;
  try {
    console.log('🔌 连接到浏览器...\n');
    browser = await chromium.connectOverCDP('http://localhost:9223');
    
    const context = browser.contexts()[0];
    const page = context.pages()[0];
    
    console.log(`📍 当前页面: ${page.url()}\n`);
    
    // 等待页面加载
    await page.waitForTimeout(3000);
    
    // 关闭可能的对话框
    const closeBtn = await page.$('button:has-text("Close")');
    if (closeBtn) {
      console.log('🖱️ 关闭对话框...\n');
      await closeBtn.click({ force: true });
      await page.waitForTimeout(2000);
    }
    
    // 获取题目信息
    console.log('📝 获取题目信息...\n');
    console.log('═══════════════════════════════════════');
    
    // 方法1: 尝试获取题目文本
    const questionText = await page.evaluate(() => {
      const selectors = [
        '[class*="question"]',
        '[class*="stem"]',
        '[class*="prompt"]',
        '.question-text',
        '.stem-text'
      ];
      
      for (const selector of selectors) {
        const el = document.querySelector(selector);
        if (el) {
          const text = el.textContent.trim();
          if (text.length > 10) {
            return text;
          }
        }
      }
      
      return null;
    });
    
    if (questionText) {
      console.log('📋 题目:');
      console.log(questionText);
      console.log('\n═══════════════════════════════════════');
    }
    
    // 方法2: 获取选项
    const options = await page.evaluate(() => {
      const labels = Array.from(document.querySelectorAll('label'));
      return labels
        .filter(l => {
          const text = l.textContent.trim();
          return text.length > 0 && 
                 text.length < 200 && 
                 !text.includes('Cookie') &&
                 !text.includes('checkbox');
        })
        .map((l, i) => ({
          letter: String.fromCharCode(65 + i),
          text: l.textContent.trim()
        }));
    });
    
    if (options.length > 0) {
      console.log('\n🎯 选项:');
      options.forEach(opt => {
        console.log(`${opt.letter}. ${opt.text}`);
      });
      console.log('\n═══════════════════════════════════════');
    }
    
    // 方法3: 获取题号和进度
    const progress = await page.evaluate(() => {
      const text = document.body.textContent;
      const match = text.match(/Question\s+(\d+)\s+of\s+(\d+)/i);
      if (match) {
        return {
          current: match[1],
          total: match[2]
        };
      }
      return null;
    });
    
    if (progress) {
      console.log(`\n📊 进度: 第 ${progress.current} 题 / 共 ${progress.total} 题`);
      console.log('═══════════════════════════════════════');
    }
    
    // 截图
    await page.screenshot({ path: 'current-question.png', fullPage: true });
    console.log('\n📸 已保存截图: current-question.png');
    
    console.log('\n✅ 题目获取完成！');
    console.log('💡 现在可以告诉我答案，我会帮你选择');
    
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
