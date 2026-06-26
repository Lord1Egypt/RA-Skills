const { chromium } = require('C:/Users/ASUS/.openclaw/workspace/node_modules/playwright');
const fs = require('fs');

/**
 * 检测并列出所有可用的 AP 课程
 */

(async () => {
  let browser;
  try {
    console.log('🔌 连接到浏览器...\n');
    browser = await chromium.connectOverCDP('http://localhost:9223');
    
    const context = browser.contexts()[0];
    const page = context.pages()[0];
    
    console.log('🔍 检测所有可用课程...\n');
    console.log('═══════════════════════════════════════');
    console.log('📚 可用的 AP 课程');
    console.log('═══════════════════════════════════════\n');
    
    // 导航到 My AP 主页
    await page.goto('https://myap.collegeboard.org/', { 
      timeout: 30000,
      waitUntil: 'domcontentloaded'
    });
    
    await page.waitForTimeout(10000);
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(5000);
    
    // 获取页面文本
    const bodyText = await page.textContent('body');
    
    // 查找所有课程
    const courses = [];
    
    // 方法1: 查找包含 AP 的课程名称
    const lines = bodyText.split('\n')
      .map(l => l.trim())
      .filter(l => l.length > 10);
    
    const apKeywords = [
      'AP English Language',
      'AP English Literature',
      'AP Statistics',
      'AP Calculus',
      'AP Computer Science',
      'AP Biology',
      'AP Chemistry',
      'AP Physics',
      'AP World History',
      'AP US History',
      'AP European History',
      'AP Psychology',
      'AP Economics',
      'AP Macroeconomics',
      'AP Microeconomics'
    ];
    
    for (const line of lines) {
      for (const keyword of apKeywords) {
        if (line.includes(keyword)) {
          // 提取课程名称（假设格式为 "课程名称 with 教师")
          const match = line.match(/(AP[^w]+?)\s+with/);
          if (match) {
            const courseName = match[1].trim();
            if (!courses.some(c => c.name === courseName)) {
              courses.push({
                name: courseName,
                fullText: line
              });
            }
          } else if (line.includes(keyword) && line.length < 100) {
            // 直接使用包含关键词的短文本
            if (!courses.some(c => c.name === line)) {
              courses.push({
                name: line,
                fullText: line
              });
            }
          }
          break;
        }
      }
    }
    
    // 显示找到的课程
    if (courses.length > 0) {
      courses.forEach((course, i) => {
        console.log(`[${i + 1}] ${course.name}`);
        if (course.fullText !== course.name) {
          console.log(`    ${course.fullText}`);
        }
        console.log('');
      });
      
      // 保存课程列表
      fs.writeFileSync('available-courses.json', JSON.stringify(courses, null, 2));
      console.log('💾 已保存课程列表到: available-courses.json');
      
    } else {
      console.log('⚠️ 未找到任何课程');
      console.log('💡 请确保:');
      console.log('  1. 已登录 College Board 账号');
      console.log('  2. 已注册 AP 课程');
      console.log('  3. 页面已完全加载');
    }
    
    console.log('\n═══════════════════════════════════════');
    console.log(`📊 共找到 ${courses.length} 门课程`);
    console.log('═══════════════════════════════════════\n');
    
    // 截图
    await page.screenshot({ path: 'courses-list.png', fullPage: true });
    console.log('📸 已保存截图: courses-list.png');
    
  } catch (error) {
    console.error('❌ 错误:', error.message);
  } finally {
    if (browser) {
      browser.close();
      console.log('\n🔌 已断开连接（浏览器保持打开）');
    }
  }
})();
