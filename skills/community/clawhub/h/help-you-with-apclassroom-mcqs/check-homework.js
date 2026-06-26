const { chromium } = require('C:/Users/ASUS/.openclaw/workspace/node_modules/playwright');
const fs = require('fs');

/**
 * 检查 AP Classroom 作业（通用版）
 * 自动检测当前课程
 * 
 * 使用方法：
 * node check-homework.js
 */

(async () => {
  let browser;
  try {
    console.log('🔌 连接到浏览器...\n');
    browser = await chromium.connectOverCDP('http://localhost:9223');
    
    const context = browser.contexts()[0];
    const page = context.pages()[0];
    
    console.log(`📍 当前页面: ${page.url()}`);
    
    // 自动检测课程 ID
    let courseId = null;
    const currentUrl = page.url();
    
    const courseIdMatch = currentUrl.match(/\/(\d+)\/assignments/);
    if (courseIdMatch) {
      courseId = courseIdMatch[1];
      console.log(`📚 检测到课程 ID: ${courseId}`);
    }
    
    // 如果没有检测到课程 ID，尝试从保存的文件读取
    if (!courseId && fs.existsSync('current-course.json')) {
      const data = fs.readFileSync('current-course.json', 'utf8');
      const course = JSON.parse(data);
      courseId = course.id;
      console.log(`📚 使用保存的课程 ID: ${courseId} (${course.name})`);
    }
    
    // 如果还是没有，使用默认值
    if (!courseId) {
      console.log('⚠️ 未检测到课程 ID，使用默认值');
      courseId = '12'; // 默认 AP Lang
    }
    
    // 导航到 Active 作业
    console.log('\n🚀 导航到 AP Classroom Active 作业...');
    const assignmentsUrl = `https://apclassroom.collegeboard.org/${courseId}/assignments?status=active`;
    
    await page.goto(assignmentsUrl, { 
      timeout: 30000,
      waitUntil: 'domcontentloaded'
    });
    
    await page.waitForTimeout(10000);
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(3000);
    
    // 截图
    await page.screenshot({ path: 'homework-check.png', fullPage: true });
    
    // 获取页面文本
    const bodyText = await page.textContent('body');
    
    // 提取作业信息
    const lines = bodyText.split('\n')
      .map(l => l.trim())
      .filter(l => l.length > 30 && (
        l.includes('Unit') ||
        l.includes('Quiz') ||
        l.includes('Progress Check') ||
        l.includes('Test') ||
        l.includes('Begin') ||
        l.includes('Continue')
      ));
    
    // 分类作业
    const todo = [];
    const inProgress = [];
    
    lines.forEach(line => {
      if (line.includes('Begin') && !line.includes('Continue')) {
        todo.push(line);
      } else if (line.includes('Continue')) {
        inProgress.push(line);
      }
    });
    
    // 显示结果
    console.log('\n═══════════════════════════════════════');
    console.log('📋 AP 作业清单');
    console.log('═══════════════════════════════════════\n');
    
    if (todo.length > 0) {
      console.log('🔴 待完成:');
      todo.forEach((item, i) => {
        console.log(`\n${i + 1}. ${item}`);
      });
    }
    
    if (inProgress.length > 0) {
      console.log('\n\n🔵 进行中:');
      inProgress.forEach((item, i) => {
        console.log(`\n${i + 1}. ${item}`);
      });
    }
    
    if (todo.length === 0 && inProgress.length === 0) {
      console.log('✅ 没有待完成的作业！');
    }
    
    console.log('\n═══════════════════════════════════════');
    console.log(`📊 统计: 待完成 ${todo.length}, 进行中 ${inProgress.length}`);
    console.log('═══════════════════════════════════════\n');
    
    // 保存结果
    fs.writeFileSync('homework-list.json', JSON.stringify({ 
      courseId,
      todo, 
      inProgress,
      checkedAt: new Date().toISOString()
    }, null, 2));
    console.log('💾 已保存到: homework-list.json');
    console.log('📸 已保存截图: homework-check.png');
    
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
