const { chromium } = require('C:/Users/ASUS/.openclaw/workspace/node_modules/playwright');
const fs = require('fs');

/**
 * 打开指定的 AP Classroom 作业（通用版）
 * 自动检测当前课程
 * 
 * 使用方法：
 * node open-assignment.js "作业名称"
 * 
 * 示例：
 * node open-assignment.js "Unit 9: Claims and Evidence - Reading Quiz"
 */

const assignmentName = process.argv[2];

if (!assignmentName) {
  console.log('❌ 请提供作业名称');
  console.log('示例: node open-assignment.js "Unit 9 Reading Quiz"');
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
    
    // 自动检测课程 ID
    let courseId = null;
    const currentUrl = page.url();
    
    const courseIdMatch = currentUrl.match(/\/(\d+)\/assignments/);
    if (courseIdMatch) {
      courseId = courseIdMatch[1];
      console.log(`📚 检测到课程 ID: ${courseId}`);
    }
    
    // 如果没有检测到，尝试从保存的文件读取
    if (!courseId && fs.existsSync('current-course.json')) {
      const data = fs.readFileSync('current-course.json', 'utf8');
      const course = JSON.parse(data);
      courseId = course.id;
      console.log(`📚 使用保存的课程 ID: ${courseId} (${course.name})`);
    }
    
    // 如果还是没有，使用默认值
    if (!courseId) {
      console.log('⚠️ 未检测到课程 ID，使用默认值');
      courseId = '12';
    }
    
    // 导航到作业列表
    console.log('🚀 导航到作业列表...');
    const assignmentsUrl = `https://apclassroom.collegeboard.org/${courseId}/assignments`;
    
    await page.goto(assignmentsUrl, { 
      timeout: 30000,
      waitUntil: 'domcontentloaded'
    });
    
    await page.waitForTimeout(10000);
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(3000);
    
    // 查找作业
    console.log(`\n🔍 查找作业: ${assignmentName}`);
    
    const rows = await page.$$('tr');
    let found = false;
    
    for (const row of rows) {
      const text = await row.textContent();
      if (text && text.includes(assignmentName)) {
        console.log('✅ 找到作业');
        
        // 查找按钮
        const beginBtn = await row.$('button:has-text("Begin")');
        const continueBtn = await row.$('button:has-text("Continue")');
        
        if (beginBtn) {
          console.log('🖱️ 点击 Begin...');
          await beginBtn.click({ force: true });
          found = true;
        } else if (continueBtn) {
          console.log('🖱️ 点击 Continue...');
          await continueBtn.click({ force: true });
          found = true;
        }
        
        break;
      }
    }
    
    if (!found) {
      console.log('❌ 未找到作业');
      return;
    }
    
    // 等待作业加载
    console.log('\n⏳ 等待作业加载...');
    await page.waitForTimeout(10000);
    
    // 检查 Resume 对话框
    const resumeBtn = await page.$('button:has-text("Resume")');
    if (resumeBtn) {
      console.log('🔄 检测到 Resume 对话框');
      console.log('💡 点击 Resume 继续...');
      await resumeBtn.click({ force: true });
      await page.waitForTimeout(5000);
    }
    
    // 截图
    await page.screenshot({ path: 'assignment-opened.png', fullPage: true });
    console.log('📸 已保存截图: assignment-opened.png');
    
    console.log('\n✅ 作业已打开！');
    console.log('💡 现在可以查看题目并决定如何答题');
    
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
