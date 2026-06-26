const { chromium } = require('C:/Users/ASUS/.openclaw/workspace/node_modules/playwright');
const fs = require('fs');
const readline = require('readline');

/**
 * 选择要操作的 AP 课程
 */

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

(async () => {
  let browser;
  try {
    console.log('🔌 连接到浏览器...\n');
    browser = await chromium.connectOverCDP('http://localhost:9223');
    
    const context = browser.contexts()[0];
    const page = context.pages()[0];
    
    // 检查是否有保存的课程列表
    let courses = [];
    if (fs.existsSync('available-courses.json')) {
      const data = fs.readFileSync('available-courses.json', 'utf8');
      courses = JSON.parse(data);
    }
    
    if (courses.length === 0) {
      console.log('⚠️ 未找到课程列表，正在检测...\n');
      
      // 导航到 My AP
      await page.goto('https://myap.collegeboard.org/', { 
        timeout: 30000,
        waitUntil: 'domcontentloaded'
      });
      
      await page.waitForTimeout(10000);
      await page.waitForLoadState('networkidle');
      await page.waitForTimeout(5000);
      
      // 检测课程（简化版）
      const bodyText = await page.textContent('body');
      const apKeywords = [
        'AP English Language',
        'AP Statistics',
        'AP Computer Science',
        'AP Calculus'
      ];
      
      apKeywords.forEach(kw => {
        if (bodyText.includes(kw)) {
          courses.push({ name: kw, keyword: kw });
        }
      });
      
      if (courses.length === 0) {
        console.log('❌ 未检测到任何课程');
        console.log('💡 请确保已登录并注册了 AP 课程');
        rl.close();
        return;
      }
    }
    
    // 显示课程列表
    console.log('═══════════════════════════════════════');
    console.log('📚 选择课程');
    console.log('═══════════════════════════════════════\n');
    
    courses.forEach((course, i) => {
      console.log(`[${i + 1}] ${course.name}`);
    });
    
    console.log('\n═══════════════════════════════════════\n');
    
    // 获取用户选择
    rl.question('请输入课程编号: ', async (answer) => {
      const index = parseInt(answer) - 1;
      
      if (index >= 0 && index < courses.length) {
        const selectedCourse = courses[index];
        
        console.log(`\n✅ 已选择: ${selectedCourse.name}`);
        
        // 尝试导航到该课程的 AP Classroom
        console.log('🚀 正在导航到课程页面...\n');
        
        // 常见的课程 ID 映射（需要根据实际情况调整）
        const courseIdMap = {
          'AP English Language': '12',
          'AP Statistics': '33',
          'AP Computer Science': '35'
        };
        
        let courseId = null;
        for (const [key, id] of Object.entries(courseIdMap)) {
          if (selectedCourse.name.includes(key)) {
            courseId = id;
            break;
          }
        }
        
        if (courseId) {
          const url = `https://apclassroom.collegeboard.org/${courseId}/assignments`;
          await page.goto(url, { timeout: 30000, waitUntil: 'domcontentloaded' });
          await page.waitForTimeout(5000);
          
          console.log('✅ 已导航到课程页面');
          console.log(`📍 URL: ${url}`);
          
          // 保存当前课程
          const currentCourse = {
            name: selectedCourse.name,
            id: courseId,
            lastAccessed: new Date().toISOString()
          };
          
          fs.writeFileSync('current-course.json', JSON.stringify(currentCourse, null, 2));
          console.log('💾 已保存当前课程信息');
          
        } else {
          console.log('⚠️ 未找到课程 ID，请手动导航到课程页面');
        }
        
      } else {
        console.log('❌ 无效的选择');
      }
      
      rl.close();
    });
    
  } catch (error) {
    console.error('❌ 错误:', error.message);
    rl.close();
  }
})();
