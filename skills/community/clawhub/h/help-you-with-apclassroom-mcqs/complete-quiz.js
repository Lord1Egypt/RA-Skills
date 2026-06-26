// 使用 workspace 中已安装的 playwright
const { chromium } = require('C:/Users/ASUS/.openclaw/workspace/node_modules/playwright');

/**
 * 完成 AP Classroom 测验
 * 
 * 使用方法：
 * 1. 修改 assignmentName 为要完成的作业名称
 * 2. 在 answerQuestion() 函数中添加答题逻辑
 * 3. 运行：node complete-quiz.js
 */

const assignmentName = 'Unit 9: Claims and Evidence - Reading Quiz';

// 答题函数（需要根据实际题目修改）
async function answerQuestion(page, questionNumber) {
  console.log(`\n📝 正在回答第 ${questionNumber} 题...`);
  
  // 获取题目文本
  const questionText = await page.evaluate(() => {
    const questionEl = document.querySelector('[class*="question"], [class*="stem"]');
    return questionEl ? questionEl.textContent.trim() : '';
  });
  
  console.log(`题目: ${questionText.substring(0, 200)}...`);
  
  // 获取选项
  const options = await page.evaluate(() => {
    const labels = Array.from(document.querySelectorAll('label'));
    return labels
      .filter(l => l.textContent.trim().length > 0)
      .map(l => l.textContent.trim())
      .filter(t => t.length < 200);
  });
  
  console.log('选项:');
  options.forEach((opt, i) => {
    console.log(`  ${String.fromCharCode(65 + i)}. ${opt}`);
  });
  
  // ⚠️ 在这里添加你的答案逻辑
  // 示例：选择第一个选项
  const answerIndex = 0;
  
  // 使用 JavaScript 点击（避免触发划掉选项）
  await page.evaluate((index) => {
    const labels = document.querySelectorAll('label');
    if (labels[index]) {
      labels[index].click();
    }
  }, answerIndex);
  
  await page.waitForTimeout(2000);
  
  console.log(`✅ 已选择选项 ${String.fromCharCode(65 + answerIndex)}`);
}

// 主程序
(async () => {
  let browser;
  try {
    console.log('🔌 连接到浏览器...');
    browser = await chromium.connectOverCDP('http://localhost:9223');
    
    const context = browser.contexts()[0];
    const page = context.pages()[0];
    
    console.log(`📍 当前页面: ${page.url()}`);
    
    // 1. 导航到作业列表
    console.log('\n🚀 导航到作业列表...');
    await page.goto('https://apclassroom.collegeboard.org/12/assignments', { 
      timeout: 30000,
      waitUntil: 'domcontentloaded'
    });
    
    await page.waitForTimeout(10000);
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(3000);
    
    // 2. 查找并点击作业
    console.log(`\n🔍 查找作业: ${assignmentName}`);
    
    const rows = await page.$$('tr');
    let found = false;
    
    for (const row of rows) {
      const text = await row.textContent();
      if (text && text.includes(assignmentName)) {
        console.log('✅ 找到作业');
        
        const beginBtn = await row.$('button:has-text("Begin")');
        if (beginBtn) {
          console.log('🖱️ 点击 Begin...');
          await beginBtn.click({ force: true });
          found = true;
          break;
        }
      }
    }
    
    if (!found) {
      console.log('❌ 未找到作业或作业已开始');
      return;
    }
    
    // 3. 等待测验加载
    console.log('\n⏳ 等待测验加载...');
    await page.waitForTimeout(10000);
    
    // 检查是否有 Resume 对话框
    const resumeBtn = await page.$('button:has-text("Resume")');
    if (resumeBtn) {
      console.log('🔄 检测到 Resume 对话框，点击 Resume');
      await resumeBtn.click({ force: true });
      await page.waitForTimeout(5000);
    }
    
    // 4. 答题循环
    let questionNumber = 1;
    let hasNext = true;
    
    while (hasNext) {
      // 答题
      await answerQuestion(page, questionNumber);
      
      // 检查是否有 Next 按钮
      const nextBtn = await page.$('button:has-text("Next")');
      if (nextBtn) {
        console.log('🖱️ 点击 Next...');
        await nextBtn.click({ force: true });
        await page.waitForTimeout(5000);
        questionNumber++;
      } else {
        // 检查是否有 Submit 按钮
        const submitBtn = await page.$('button:has-text("Submit")');
        if (submitBtn) {
          console.log('\n✅ 所有题目已完成，准备提交');
          hasNext = false;
        } else {
          console.log('⚠️ 未找到 Next 或 Submit 按钮');
          hasNext = false;
        }
      }
    }
    
    // 5. 提交测验
    console.log('\n📤 提交测验...');
    
    const submitBtn = await page.$('button:has-text("Submit")');
    if (submitBtn) {
      await submitBtn.click({ force: true });
      await page.waitForTimeout(3000);
      
      // 确认提交
      const confirmBtn = await page.$('button:has-text("Yes"), button:has-text("Confirm")');
      if (confirmBtn) {
        console.log('🖱️ 确认提交');
        await confirmBtn.click({ force: true });
        await page.waitForTimeout(5000);
      }
      
      console.log('✅ 测验已提交！');
      
      // 截图
      await page.screenshot({ path: 'quiz-submitted.png', fullPage: true });
      console.log('📸 已保存截图: quiz-submitted.png');
    }
    
    // 6. 返回 Dashboard
    const exitBtn = await page.$('button:has-text("Exit"), a:has-text("Exit")');
    if (exitBtn) {
      console.log('🖱️ 点击 Exit 返回 Dashboard');
      await exitBtn.click({ force: true });
      await page.waitForTimeout(5000);
    }
    
    console.log('\n✅ 作业完成！');
    
  } catch (error) {
    console.error('❌ 错误:', error.message);
    console.error(error.stack);
  } finally {
    // ⚠️ 重要：只断开连接，不关闭浏览器
    if (browser) {
      browser.close();
      console.log('\n🔌 已断开连接（浏览器保持打开）');
    }
  }
})();
