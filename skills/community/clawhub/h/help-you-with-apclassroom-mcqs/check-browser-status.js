const { chromium } = require('C:/Users/ASUS/.openclaw/workspace/node_modules/playwright');
const fs = require('fs');

/**
 * 检查当前浏览器状态
 * - 显示登录用户
 * - 自动检测当前课程
 * - 显示待完成作业
 * 
 * ⚠️ 不会关闭浏览器，只断开连接
 */

(async () => {
  let browser;
  try {
    console.log('🔌 连接到浏览器...\n');
    browser = await chromium.connectOverCDP('http://localhost:9223');
    
    const context = browser.contexts()[0];
    const pages = context.pages();
    
    console.log('═══════════════════════════════════════');
    console.log('🌐 浏览器状态');
    console.log('═══════════════════════════════════════\n');
    
    console.log(`📊 打开的页面: ${pages.length} 个\n`);
    
    // 显示所有页面
    for (let i = 0; i < pages.length; i++) {
      const page = pages[i];
      const url = page.url();
      const title = await page.title();
      
      console.log(`📄 页面 ${i + 1}:`);
      console.log(`   标题: ${title}`);
      console.log(`   URL: ${url}`);
      
      // 如果是 AP Classroom 页面，自动检测课程
      if (url.includes('apclassroom.collegeboard.org')) {
        console.log('   ✅ AP Classroom 页面');
        
        try {
          // 自动提取课程 ID
          const courseIdMatch = url.match(/\/(\d+)\/assignments/);
          const courseId = courseIdMatch ? courseIdMatch[1] : null;
          
          if (courseId) {
            console.log(`   📚 课程 ID: ${courseId}`);
          }
          
          const bodyText = await page.textContent('body');
          
          // 查找用户名
          const lines = bodyText.split('\n').map(l => l.trim());
          for (const line of lines) {
            if (line.match(/^[A-Z][a-z]+$/) && line.length < 20) {
              console.log(`   👤 用户: ${line}`);
              break;
            }
          }
          
          // 查找课程名称
          const courseKeywords = [
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
            'AP Psychology'
          ];
          
          for (const line of lines) {
            for (const keyword of courseKeywords) {
              if (line.includes(keyword)) {
                console.log(`   📚 课程: ${line}`);
                
                // 保存当前课程信息
                const currentCourse = {
                  name: line,
                  id: courseId,
                  lastChecked: new Date().toISOString()
                };
                fs.writeFileSync('current-course.json', JSON.stringify(currentCourse, null, 2));
                
                break;
              }
            }
          }
          
        } catch (e) {
          console.log('   ⚠️ 无法获取详细信息');
        }
      }
      
      console.log('');
    }
    
    console.log('═══════════════════════════════════════');
    console.log('✅ 检查完成');
    console.log('═══════════════════════════════════════\n');
    
  } catch (error) {
    console.error('❌ 错误:', error.message);
    console.log('\n💡 请确保:');
    console.log('  1. Chrome 已启动（带 --remote-debugging-port=9223）');
    console.log('  2. 端口 9223 已开启');
  } finally {
    // ⚠️ 重要：只断开连接，不关闭浏览器
    if (browser) {
      browser.close();
      console.log('🔌 已断开连接（浏览器保持打开）\n');
    }
  }
})();
