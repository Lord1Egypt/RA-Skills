const { chromium } = require('C:/Users/ASUS/.openclaw/workspace/node_modules/playwright');

/**
 * 选择答案并进入下一题
 * 
 * 使用方法：
 * node answer-question.js A    # 选择 A
 * node answer-question.js B    # 选择 B
 * node answer-question.js C    # 选择 C
 * node answer-question.js D    # 选择 D
 * 
 * ⚠️ 前提：已经在浏览器中打开了某个作业并获取了题目
 */

const answer = process.argv[2]?.toUpperCase();

if (!answer || !['A', 'B', 'C', 'D', 'E'].includes(answer)) {
  console.log('❌ 请提供正确的答案选项（A/B/C/D/E）');
  console.log('示例: node answer-question.js A');
  process.exit(1);
}

(async () => {
  let browser;
  try {
    console.log('🔌 连接到浏览器...\n');
    browser = await chromium.connectOverCDP('http://localhost:9223');
    
    const context = browser.contexts()[0];
    const page = context.pages()[0];
    
    console.log(`📍 当前页面: ${page.url()}\n`);
    
    // 计算选项索引
    const answerIndex = answer.charCodeAt(0) - 65; // A=0, B=1, C=2, D=3, E=4
    
    console.log(`🎯 选择答案: ${answer}\n`);
    
    // 使用 JavaScript 点击（避免触发划掉选项）
    const selected = await page.evaluate((index) => {
      const labels = document.querySelectorAll('label');
      const validLabels = Array.from(labels).filter(l => {
        const text = l.textContent.trim();
        return text.length > 0 && 
               text.length < 200 && 
               !text.includes('Cookie') &&
               !text.includes('checkbox');
      });
      
      if (validLabels[index]) {
        validLabels[index].click();
        return true;
      }
      return false;
    }, answerIndex);
    
    if (selected) {
      console.log('✅ 已选择答案');
      await page.waitForTimeout(2000);
      
      // 检查是否选中
      const isSelected = await page.evaluate((index) => {
        const labels = document.querySelectorAll('label');
        const validLabels = Array.from(labels).filter(l => {
          const text = l.textContent.trim();
          return text.length > 0 && 
                 text.length < 200 && 
                 !text.includes('Cookie') &&
                 !text.includes('checkbox');
        });
        
        if (validLabels[index]) {
          const li = validLabels[index].closest('li');
          return li && li.classList.contains('lrn_selected');
        }
        return false;
      }, answerIndex);
      
      if (isSelected) {
        console.log('✅ 答案已成功选中');
      } else {
        console.log('⚠️ 无法确认是否选中');
      }
      
      // 截图
      await page.screenshot({ path: 'answer-selected.png', fullPage: false });
      console.log('📸 已保存截图: answer-selected.png');
      
      console.log('\n💡 下一步操作:');
      console.log('  - 继续下一题: node next-question.js');
      console.log('  - 提交测验: node submit-quiz.js');
      
    } else {
      console.log('❌ 无法选择答案（选项不存在）');
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
