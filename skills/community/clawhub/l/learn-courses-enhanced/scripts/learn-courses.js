const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// ==================== 配置常量 ====================
const CONFIG = {
  // 目标URL（支持多个课程）
  COURSES: [
    {
      id: 'course-1',
      name: '课程1',
      url: 'https://mooc.ctt.cn/#/study/subject/detail/dfa84528-8f8c-4b0a-a049-81bf3e86276e'
    },
    {
      id: 'course-2',
      name: '课程2',
      url: 'https://mooc.ctt.cn/#/study/subject/detail/c5f08b78-3325-4775-a2dc-81ef230e76a4'
    }
  ],
  
  // 视频学习配置
  VIDEO: {
    MAX_WAIT_SECONDS: 3600,
    CHECK_INTERVAL: 5000,
    STABLE_COUNT: 6,
    COMPLETION_CHECK_INTERVAL: 10000
  },
  
  // 登录相关配置
  LOGIN: {
    LOGIN_TIMEOUT: 60,
    PAGE_WAIT_TIMEOUT: 30,
    CHECK_INTERVAL: 2000,
    POST_LOGIN_WAIT: 5000
  },
  
  // 浏览器配置
  BROWSER: {
    HEADLESS: false,
    EXECUTABLE_PATH: process.pkg 
      ? './chrome-win64/chrome.exe' 
      : undefined,
    CHANNEL: process.pkg ? undefined : 'chrome',
    ARGS: ['--start-maximized', '--disable-blink-features=AutomationControlled']
  },
  
  // 后台运行配置
  BACKGROUND: {
    ENABLED: false,  // 是否后台运行
    MINIMIZE_TO_TRAY: true  // 最小化到托盘
  },
  
  // 进度保存配置
  PROGRESS: {
    SAVE_FILE: './learning-progress.json',
    SAVE_INTERVAL: 30000  // 30秒保存一次
  },
  
  // 统计报告配置
  STATS: {
    REPORT_FILE: './learning-report.json'
  }
};

// 全局状态
let shouldStop = false;
let browser = null;
let progressData = {
  courses: {},
  stats: {
    totalTime: 0,
    completedChapters: 0,
    failedChapters: 0,
    sessions: []
  },
  lastUpdate: null
};

// ==================== 进度管理 ====================
function loadProgress() {
  try {
    if (fs.existsSync(CONFIG.PROGRESS.SAVE_FILE)) {
      const data = fs.readFileSync(CONFIG.PROGRESS.SAVE_FILE, 'utf-8');
      progressData = JSON.parse(data);
      console.log('✓ 已加载上次学习进度');
      return true;
    }
  } catch (err) {
    console.log('加载进度失败:', err.message);
  }
  return false;
}

function saveProgress() {
  try {
    progressData.lastUpdate = new Date().toISOString();
    fs.writeFileSync(CONFIG.PROGRESS.SAVE_FILE, JSON.stringify(progressData, null, 2));
  } catch (err) {
    console.log('保存进度失败:', err.message);
  }
}

function updateProgress(courseId, chapterIndex, status, timeSpent = 0) {
  if (!progressData.courses[courseId]) {
    progressData.courses[courseId] = {
      chapters: {},
      currentChapter: 0,
      completedChapters: []
    };
  }
  
  progressData.courses[courseId].chapters[chapterIndex] = {
    status,
    timeSpent,
    timestamp: new Date().toISOString()
  };
  
  if (status === 'completed') {
    if (!progressData.courses[courseId].completedChapters.includes(chapterIndex)) {
      progressData.courses[courseId].completedChapters.push(chapterIndex);
    }
    progressData.stats.completedChapters++;
  } else if (status === 'failed') {
    progressData.stats.failedChapters++;
  }
  
  progressData.stats.totalTime += timeSpent;
  
  // 立即保存
  saveProgress();
}

// ==================== 统计报告 ====================
function generateReport() {
  const report = {
    generatedAt: new Date().toISOString(),
    summary: {
      totalTime: formatTime(progressData.stats.totalTime),
      totalTimeSeconds: progressData.stats.totalTime,
      completedChapters: progressData.stats.completedChapters,
      failedChapters: progressData.stats.failedChapters,
      sessionsCount: progressData.stats.sessions.length
    },
    courses: {},
    sessions: progressData.stats.sessions.slice(-10)  // 最近10次会话
  };
  
  for (const [courseId, courseData] of Object.entries(progressData.courses)) {
    const course = CONFIG.COURSES.find(c => c.id === courseId);
    report.courses[courseId] = {
      name: course?.name || courseId,
      completedChapters: courseData.completedChapters?.length || 0,
      chapters: courseData.chapters
    };
  }
  
  // 保存报告
  try {
    fs.writeFileSync(CONFIG.STATS.REPORT_FILE, JSON.stringify(report, null, 2));
    console.log(`\n✓ 学习报告已保存到: ${CONFIG.STATS.REPORT_FILE}`);
  } catch (err) {
    console.log('保存报告失败:', err.message);
  }
  
  return report;
}

function printReport() {
  const report = generateReport();
  
  console.log('\n========== 学习统计报告 ==========');
  console.log(`总学习时间: ${report.summary.totalTime}`);
  console.log(`完成章节: ${report.summary.completedChapters}`);
  console.log(`失败章节: ${report.summary.failedChapters}`);
  console.log(`学习次数: ${report.summary.sessionsCount}`);
  console.log('=====================================\n');
}

// ==================== 工具函数 ====================
function formatTime(seconds) {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = seconds % 60;

  if (hours > 0) {
    return `${hours}时${minutes}分${secs}秒`;
  } else if (minutes > 0) {
    return `${minutes}分${secs}秒`;
  } else {
    return `${secs}秒`;
  }
}

function logSeparator(title = '') {
  console.log('\n========================================');
  if (title) {
    console.log(title);
    console.log('========================================\n');
  }
}

// ==================== 增强弹窗识别 ====================
async function handlePopupSmart(page, elapsedSeconds) {
  const popupActions = [];
  
  try {
    // 1. 文本匹配弹窗识别
    const textPatterns = [
      { text: '学习计时中', button: ['确定', '我已知悉'] },
      { text: '亲爱的学员', button: ['确定', '我已知悉'] },
      { text: '学习完成', button: ['确定', '关闭', '知道了'] },
      { text: '播放结束', button: ['确定', '下一章', '继续'] },
      { text: '恭喜', button: ['确定', '关闭'] },
      { text: '温馨提示', button: ['确定', '我已知悉'] },
      { text: '注意', button: ['确定', '我已知悉'] },
      { text: '认证', button: ['确定', '取消'] }
    ];
    
    for (const pattern of textPatterns) {
      // 检查页面是否包含相关文本
      const content = await page.content();
      if (content.includes(pattern.text)) {
        // 查找可能的按钮
        for (const btnText of pattern.button) {
          const buttons = await page.locator(`button:has-text("${btnText}"), a:has-text("${btnText}"), span:has-text("${btnText}")`).all();
          for (const btn of buttons) {
            try {
              if (await btn.isVisible()) {
                await btn.click();
                popupActions.push(`点击按钮: ${btnText}`);
                await page.waitForTimeout(500);
                break;
              }
            } catch (e) {}
          }
        }
      }
    }
    
    // 2. 模态框/弹窗检测
    const modalSelectors = [
      '.modal:visible',
      '.dialog:visible',
      '.popup:visible',
      '[role="dialog"]:visible',
      '.el-dialog:visible',
      '.ant-modal:visible',
      '.ivu-modal:visible'
    ];
    
    for (const selector of modalSelectors) {
      const modal = await page.locator(selector).first();
      try {
        if (await modal.isVisible()) {
          // 查找弹窗内的按钮
          const modalButtons = await modal.locator('button').all();
          for (const btn of modalButtons) {
            try {
              const text = await btn.textContent();
              if (text && (text.includes('确定') || text.includes('关闭') || text.includes('知道'))) {
                await btn.click();
                popupActions.push(`关闭弹窗按钮: ${text.trim()}`);
                await page.waitForTimeout(500);
                break;
              }
            } catch (e) {}
          }
        }
      } catch (e) {}
    }
    
    // 3. 屏幕中央弹窗检测
    const centerButtons = await page.evaluate(() => {
      const btn = document.elementFromPoint(window.innerWidth / 2, window.innerHeight / 2);
      if (btn && (btn.tagName === 'BUTTON' || btn.tagName === 'A')) {
        return btn.textContent.trim();
      }
      return null;
    });
    
    if (centerButtons && (centerButtons.includes('确定') || centerButtons.includes('知道'))) {
      await page.click(`button:has-text("${centerButtons}"), a:has-text("${centerButtons}")`);
      popupActions.push(`点击中央按钮: ${centerButtons}`);
    }
    
    // 4. ESC键关闭
    await page.keyboard.press('Escape');
    await page.waitForTimeout(300);
    
  } catch (error) {
    // 静默处理
  }
  
  if (popupActions.length > 0) {
    console.log(`[${formatTime(elapsedSeconds)}] 智能弹窗处理: ${popupActions.join(', ')}`);
  }
  
  return popupActions.length > 0;
}

// ==================== 异常自动恢复 ====================
class NetworkRecovery {
  constructor(page, browser) {
    this.page = page;
    this.browser = browser;
    this.retryCount = 0;
    this.maxRetries = 3;
  }
  
  async checkAndRecover() {
    try {
      // 检查页面是否可访问
      const url = this.page.url();
      if (!url || url === 'about:blank') {
        return await this.recover('页面为空');
      }
      
      // 尝试获取页面标题
      await this.page.title().catch(() => '');
      
      return true;
    } catch (error) {
      return await this.recover(error.message);
    }
  }
  
  async recover(reason) {
    this.retryCount++;
    console.log(`\n⚠ 检测到异常 (${reason}), 尝试恢复... (${this.retryCount}/${this.maxRetries})`);
    
    if (this.retryCount >= this.maxRetries) {
      console.log('✗ 恢复失败次数过多，跳过当前章节');
      return false;
    }
    
    try {
      // 等待网络稳定
      await this.page.waitForTimeout(2000);
      
      // 刷新页面
      await this.page.reload({ waitUntil: 'domcontentloaded', timeout: 15000 });
      await this.page.waitForTimeout(3000);
      
      console.log('✓ 页面已刷新');
      return true;
    } catch (err) {
      console.log(`恢复失败: ${err.message}`);
      
      // 尝试创建新页面
      try {
        const context = this.browser.contexts()[0];
        const newPage = await context.newPage();
        console.log('✓ 已创建新页面');
        this.page = newPage;
        return true;
      } catch (e) {
        return false;
      }
    }
  }
  
  reset() {
    this.retryCount = 0;
  }
}

// ==================== 获取需要学习的章节 ====================
async function getChaptersToLearn(page, courseId) {
  logSeparator('分析章节学习状态');

  try {
    await page.waitForSelector('[id^="D395finishStatus-"]', { timeout: 15000 });
  } catch (err) {
    // 继续尝试
  }

  await page.waitForTimeout(2000);

  const reviewElements = await page.locator('text=复习').all();
  const startElements = await page.locator('text=开始学习').all();
  const continueElements = await page.locator('text=继续学习').all();

  let statusElements = [...reviewElements, ...startElements, ...continueElements];

  const chapters = [];

  for (let i = 0; i < statusElements.length; i++) {
    try {
      const elem = statusElements[i];
      const text = await elem.textContent();

      const actionText = text?.trim() || '';

      let needLearn = false;
      let statusText = '';

      if (actionText.includes('开始学习') || actionText.includes('继续学习')) {
        needLearn = true;
        statusText = '待学习';
      } else if (actionText.includes('复习')) {
        needLearn = false;
        statusText = '已学完';
      } else {
        needLearn = false;
        statusText = actionText;
      }

      // 检查是否已完成
      const isCompleted = progressData.courses[courseId]?.completedChapters?.includes(i + 1);
      
      const statusIcon = needLearn && !isCompleted ? '⏳' : '✓';
      const learnStatus = isCompleted ? '(已完成)' : '';
      console.log(`第 ${i + 1} 章节: ${statusIcon} [${actionText}] ${statusText} ${learnStatus}`);

      chapters.push({
        index: i + 1,
        courseId: `chapter-${i + 1}`,
        actionText: actionText,
        needLearn: needLearn && !isCompleted
      });
    } catch (err) {
      // 跳过处理失败的元素
    }
  }

  const needLearnCount = chapters.filter(c => c.needLearn).length;
  const completedCount = chapters.filter(c => !c.needLearn).length;

  console.log(`总章节数: ${chapters.length}, 需要学习: ${needLearnCount} 章, 已完成: ${completedCount} 章\n`);

  return chapters.filter(c => c.needLearn);
}

// ==================== 进入章节学习 ====================
async function startChapterLearning(page, chapter, context) {
  console.log(`\n开始学习第 ${chapter.index} 章 (章节ID: ${chapter.courseId}, 状态: ${chapter.actionText})`);

  try {
    let actionButton = null;
    let buttonText = '';

    // 优先查找"继续学习"元素
    const continueElement = page.locator('button:has-text("继续学习"), a:has-text("继续学习"), span:has-text("继续学习")').first();
    const continueElemCount = await continueElement.count();

    if (continueElemCount > 0) {
      const pagePromise = context.waitForEvent('page', { timeout: 10000 });

      try {
        const info = await continueElement.evaluate(el => {
          let current = el;
          const path = [];

          while (current && current.tagName !== 'BODY') {
            path.push(`${current.tagName}.${current.className || ''}`);

            const rect = current.getBoundingClientRect();
            if (rect.width < 10 || rect.height < 10) {
              current = current.parentElement;
              continue;
            }

            if (rect.width > 50 || rect.height > 30) {
              current.click();
              return { clicked: true, path: path.join(' > ') };
            }

            current = current.parentElement;
          }

          el.click();
          path.push(`CLICKED_ORIGINAL`);
          return { clicked: true, path: path.join(' > ') };
        });

        if (info.clicked) {
          buttonText = '继续学习';
          console.log('✓ 点击"继续学习"按钮');

          const initialUrl = page.url();

          let newPage = null;
          try {
            newPage = await pagePromise;
            console.log('✓ 检测到新标签页打开');
            return { success: true, page: newPage };
          } catch (err) {
            console.log('⚠ 未检测到新标签页打开，检查URL变化...');
          }

          await page.waitForTimeout(3000);

          const currentUrl = page.url();
          const urlChanged = currentUrl !== initialUrl;
          const inPlayPage = currentUrl.includes('play') || currentUrl.includes('video') || currentUrl.includes('player');

          if (urlChanged || inPlayPage) {
            console.log('✓ 页面已跳转到播放页面\n');
            return { success: true, page: page };
          } else {
            console.log('⚠ 页面未跳转\n');
            return { success: false, page: null };
          }
        }
      } catch (err) {
        console.log(`点击失败: ${err.message}`);
      }
    } else {
      console.log('未找到"继续学习"元素，查找"开始学习"元素...');

      const startElement = page.locator('button:has-text("开始学习"), a:has-text("开始学习"), span:has-text("开始学习")').first();
      const startElemCount = await startElement.count();

      console.log(`查找"开始学习"元素: ${startElemCount > 0 ? '找到' : '未找到'}`);

      if (startElemCount > 0) {
        try {
          console.log('找到"开始学习"元素，尝试查找可点击父元素...');
          const info = await startElement.evaluate(el => {
            let current = el;
            const path = [];
            let triedClick = false;

            while (current && current.tagName !== 'BODY') {
              path.push(`${current.tagName}.${current.className || ''}`);

              const rect = current.getBoundingClientRect();
              if (rect.width < 10 || rect.height < 10) {
                current = current.parentElement;
                continue;
              }

              if (current.onclick ||
                  current.href ||
                  current.tagName === 'A' ||
                  current.tagName === 'BUTTON' ||
                  current.tagName === 'LI' ||
                  window.getComputedStyle(current).cursor === 'pointer' ||
                  current.classList.contains('item') ||
                  current.classList.contains('course') ||
                  current.classList.contains('chapter') ||
                  current.classList.contains('lesson')) {
                current.click();
                triedClick = true;
                return { clicked: true, path: path.join(' > ') };
              }

              current = current.parentElement;
            }

            el.click();
            path.push(`CLICKED_ORIGINAL`);
            return { clicked: true, path: path.join(' > ') };
          });

          console.log(`元素路径: ${info.path}`);

          if (info.clicked) {
            buttonText = '开始学习';
            console.log('✓ 找到并点击包含"开始学习"的可点击元素');

            const initialUrl = page.url();
            console.log(`点击前URL: ${initialUrl}`);

            const pagePromise = context.waitForEvent('page');

            console.log('等待新标签页/页面加载...');

            let newPage = null;
            try {
              newPage = await Promise.race([
                pagePromise,
                page.waitForTimeout(2500).then(() => null)
              ]);

              if (newPage) {
                console.log('✓ 检测到新标签页打开');
                console.log(`新页面URL: ${newPage.url()}`);
                return { success: true, page: newPage };
              } else {
                console.log('⚠ 未检测到新标签页打开');
              }
            } catch (err) {
              console.log(`等待新页面时出错: ${err.message}`);
            }

            const allPages = context.pages();
            console.log(`当前共有 ${allPages.length} 个页面`);
            if (allPages.length > 1) {
              console.log('检测到额外的页面');
              for (let i = 0; i < allPages.length; i++) {
                console.log(`  页面${i + 1}: ${allPages[i].url()}`);
              }
              const lastPage = allPages[allPages.length - 1];
              if (lastPage !== page) {
                console.log('✓ 找到新标签页');
                return { success: true, page: lastPage };
              }
            }

            await page.waitForTimeout(2000);
            const currentUrl = page.url();
            console.log(`当前URL: ${currentUrl}`);

            const urlChanged = currentUrl !== initialUrl;
            const inPlayPage = currentUrl.includes('play') || currentUrl.includes('video') || currentUrl.includes('player');

            console.log(`  URL改变: ${urlChanged}`);
            console.log(`  URL包含play/video/player: ${inPlayPage}`);

            if (urlChanged || inPlayPage) {
              console.log('✓ 页面已跳转到播放页面\n');
              return { success: true, page: page };
            } else {
              console.log('⚠ 页面未跳转');
              console.log();
              return { success: false, page: null };
            }
          } else {
            actionButton = startElement;
            buttonText = '开始学习';
            console.log('✓ 找到包含"开始学习"的元素（未找到可点击父元素）');
          }
        } catch (err) {
          console.log(`点击可点击元素失败: ${err.message}`);
          actionButton = startElement;
          buttonText = '开始学习';
          console.log('✓ 找到包含"开始学习"的元素');
        }
      }
    }
    
    if (actionButton && await actionButton.count() > 0) {
      console.log(`点击 "${buttonText}" 按钮进入播放页面...`);

      const initialUrl = page.url();
      console.log(`点击前URL: ${initialUrl}`);

      console.log('设置新标签页监听器...');
      const pagePromise = context.waitForEvent('page');

      try {
        await actionButton.scrollIntoViewIfNeeded();
        await page.waitForTimeout(1000);
        await actionButton.waitFor({ state: 'visible', timeout: 5000 });
      } catch (scrollError) {
        console.log(`滚动操作失败: ${scrollError.message}`);
      }

      let clickSuccess = false;
      let clickError = null;

      try {
        console.log('尝试方法1: JavaScript点击');
        await actionButton.evaluate(el => el.click());
        clickSuccess = true;
        console.log('✓ JavaScript点击成功');
      } catch (jsClickError) {
        console.log(`JavaScript点击失败: ${jsClickError.message}`);
        clickError = jsClickError;

        try {
          console.log('尝试方法2: 双击');
          await actionButton.dblclick({ timeout: 10000 });
          clickSuccess = true;
          console.log('✓ 双击成功');
        } catch (dblClickError) {
          console.log(`双击失败: ${dblClickError.message}`);
          clickError = dblClickError;

          try {
            console.log('尝试方法3: 强制点击');
            await actionButton.click({ force: true, timeout: 10000 });
            clickSuccess = true;
            console.log('✓ 强制点击成功');
          } catch (forceClickError) {
            console.log(`强制点击失败: ${forceClickError.message}`);
          }
        }
      }

      if (!clickSuccess) {
        console.log('⚠ 所有点击方式都失败了');
        console.log(`最后错误: ${clickError?.message || '未知错误'}`);

        try {
          console.log('尝试方法4: 获取href并直接打开新标签页');
          const href = await actionButton.evaluate(el => el.href || el.getAttribute('data-href') || el.getAttribute('data-url'));

          if (href) {
            console.log(`找到链接: ${href}`);
            const newPage = await context.newPage();
            await newPage.goto(href, { waitUntil: 'domcontentloaded', timeout: 30000 });
            console.log('✓ 直接打开新标签页成功');
            console.log(`新页面URL: ${newPage.url()}`);
            return { success: true, page: newPage };
          } else {
            console.log('未找到href属性');
          }
        } catch (hrefError) {
          console.log(`通过href打开失败: ${hrefError.message}`);
        }

        return { success: false, page: null };
      }

      console.log('等待新标签页/页面加载...');

      let newPage = null;
      try {
        newPage = await Promise.race([
          pagePromise,
          page.waitForTimeout(2500).then(() => null)
        ]);

        if (newPage) {
          console.log('✓ 检测到新标签页打开');
          console.log(`新页面URL: ${newPage.url()}`);
          return { success: true, page: newPage };
        } else {
          console.log('⚠ 未检测到新标签页打开，等待5秒后继续...');
        }
      } catch (err) {
        console.log(`等待新页面时出错: ${err.message}`);
      }

      const allPages = context.pages();
      console.log(`当前共有 ${allPages.length} 个页面`);
      if (allPages.length > 1) {
        console.log('检测到额外的页面');
        for (let i = 0; i < allPages.length; i++) {
          console.log(`  页面${i + 1}: ${allPages[i].url()}`);
        }
        const lastPage = allPages[allPages.length - 1];
        if (lastPage !== page) {
          console.log('✓ 找到新标签页');
          return { success: true, page: lastPage };
        }
      }

      await page.waitForTimeout(2000);

      const currentUrl = page.url();
      console.log(`当前URL: ${currentUrl}`);

      const urlChanged = currentUrl !== initialUrl;
      const hasVideoElement = await page.locator('video').count() > 0;
      const hasVideoClass = await page.locator('[class*="video-player"], [class*="VideoPlayer"]').count() > 0;
      const inPlayPage = currentUrl.includes('play') || currentUrl.includes('video') || currentUrl.includes('player');

      console.log(`  URL改变: ${urlChanged}`);
      console.log(`  包含video标签: ${hasVideoElement}`);
      console.log(`  包含video-player类: ${hasVideoClass}`);
      console.log(`  URL包含play/video/player: ${inPlayPage}`);

      if (urlChanged || inPlayPage || hasVideoElement || hasVideoClass) {
        console.log('✓ 页面已加载视频播放器\n');
        return { success: true, page: page };
      } else {
        console.log('⚠ 未检测到视频播放器');
        console.log('⚠ 点击可能没有实际触发导航或新标签页打开');
        console.log();
        return { success: false, page: null };
      }
    } else {
      console.log('⚠ 未找到任何学习按钮');
      console.log('调试信息: 尝试查找所有按钮...');
      
      try {
        const allButtons = await page.locator('button').all();
        console.log(`页面共有 ${allButtons.length} 个按钮`);
        
        for (let i = 0; i < Math.min(allButtons.length, 5); i++) {
          const btnText = await allButtons[i].textContent();
          console.log(`  按钮${i + 1}: "${btnText?.trim()}"`);
        }
      } catch (err) {
        console.log('无法获取按钮信息:', err.message);
      }
      
      return false;
    }
    
  } catch (error) {
    console.error('点击学习按钮失败:', error.message);
    return false;
  }
}

// ==================== 监控视频学习完成 ====================
async function waitForVideoCompletion(page, recovery) {
  logSeparator('等待视频学习完成');
  
  const startTime = Date.now();
  const maxWaitSeconds = CONFIG.VIDEO.MAX_WAIT_SECONDS;
  let completionCount = 0;
  let lastSaveTime = Date.now();

  console.log('监控方式: 智能检测学习完成提示 + 自动处理弹窗\n');

  while (!shouldStop) {
    const elapsedSeconds = Math.floor((Date.now() - startTime) / 1000);

    if (elapsedSeconds > maxWaitSeconds) {
      console.log(`\n⚠ 等待超时 (${formatTime(maxWaitSeconds)})`);
      return false;
    }

    try {
      // 1. 智能弹窗处理
      await handlePopupSmart(page, elapsedSeconds);
      
      // 2. 网络异常检测与恢复
      const networkOk = await recovery.checkAndRecover();
      if (!networkOk) {
        console.log('网络恢复失败');
      }
      recovery.reset();

      // 3. 检测学习完成弹窗
      const completionPopup = await page.locator('text=学习完成, text=播放结束, text=已完成, text=恭喜').all();
      if (completionPopup.length > 0) {
        console.log('\n✓ 检测到学习完成弹窗');

        const buttonSelectors = [
          'button:has-text("确定")',
          'button:has-text("关闭")', 
          'button:has-text("知道了")',
          'a:has-text("确定")',
          'a:has-text("关闭")',
          '.el-button:has-text("确定")',
          '.el-button:has-text("关闭")'
        ];
        
        for (const selector of buttonSelectors) {
          const confirmButton = page.locator(selector).first();
          if (await confirmButton.count() > 0) {
            const isVisible = await confirmButton.isVisible().catch(() => false);
            if (isVisible) {
              console.log('关闭弹窗...');
              await confirmButton.click();
              await page.waitForTimeout(1000);
              break;
            }
          }
        }

        return true;
      }

      // 4. 检测是否自动返回章节列表
      const backToChapter = await page.locator('div.small.inline-block[id^="D395finishStatus-"]').count() > 0;
      if (backToChapter && elapsedSeconds > 10) {
        completionCount++;

        if (completionCount >= 3) {
          console.log('\n✓ 已返回章节列表页面');
          return true;
        }
      }

      // 5. 检测视频是否播放结束
      const videoElements = await page.locator('video').all();
      for (const video of videoElements) {
        const ended = await video.evaluate(v => v.ended).catch(() => false);
        if (ended) {
          console.log('\n✓ 视频播放已结束');

          await page.waitForTimeout(2000);

          const popup = await page.locator('text=学习完成, text=播放结束').all();
          if (popup.length === 0) {
            return true;
          }
        }
      }

      // 6. 定期保存进度
      if (Date.now() - lastSaveTime > CONFIG.PROGRESS.SAVE_INTERVAL) {
        saveProgress();
        lastSaveTime = Date.now();
      }

      // 7. 定期输出进度（每5分钟）
      if (elapsedSeconds % 300 === 0 && elapsedSeconds > 0) {
        console.log(`学习进行中... (${formatTime(elapsedSeconds)})`);
      }

      // 8. 防屏保点击
      const randomClickInterval = Math.floor(Math.random() * 30) + 30;
      if (elapsedSeconds % randomClickInterval === 0 && elapsedSeconds > 10) {
        try {
          await page.evaluate(() => {
            const body = document.body;
            if (body) {
              const x = Math.random() * 100 + 20;
              const y = window.innerHeight - 50;
              const event = new MouseEvent('click', {
                bubbles: true,
                cancelable: true,
                clientX: x,
                clientY: y
              });
              body.dispatchEvent(event);
            }
          });
          console.log(`[${formatTime(elapsedSeconds)}] 防屏保: 点击空白处`);
        } catch (err) {
          // 忽略
        }
      }

    } catch (error) {
      console.log(`[检测错误] ${error.message}`);
    }

    await page.waitForTimeout(CONFIG.VIDEO.CHECK_INTERVAL);
  }
  
  return false;
}

// ==================== 关闭播放页/返回章节列表 ====================
async function closeVideoPage(page) {
  console.log('\n关闭播放页，返回章节列表...');
  
  try {
    const closeButton = page.locator('button:has-text("返回"), button:has-text("关闭"), button[title*="返回"], button[title*="关闭"]').first();
    if (await closeButton.count() > 0) {
      console.log('点击关闭/返回按钮...');
      await closeButton.click({ timeout: 5000 });
      await page.waitForTimeout(2000);
      return true;
    }
    
    console.log('使用浏览器返回...');
    await page.goBack();
    await page.waitForTimeout(2000);
    
    const backToChapter = await page.locator('div.small.inline-block[id^="D395finishStatus-"]').count() > 0;
    if (backToChapter) {
      console.log('✓ 成功返回章节列表');
      return true;
    }
    
    console.log('刷新页面...');
    await page.reload({ waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(3000);
    return true;
    
  } catch (error) {
    console.log('关闭播放页失败:', error.message);
    
    try {
      console.log('尝试刷新页面...');
      await page.reload({ waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(3000);
      return true;
    } catch (err) {
      console.log('刷新页面也失败了');
      return false;
    }
  }
}

// ==================== 单课程学习流程 ====================
async function learnSingleCourse(page, context, course) {
  let totalLearned = 0;
  let maxRounds = 3;
  const courseId = course.id;
  
  for (let round = 1; round <= maxRounds; round++) {
    console.log(`\n===== 第 ${round} 轮学习检测 =====\n`);
    
    const chaptersToLearn = await getChaptersToLearn(page, courseId);
    
    if (chaptersToLearn.length === 0) {
      console.log(`\n✓ 第 ${round} 轮检测：所有章节已完成学习！`);
      totalLearned += chaptersToLearn.length;
      break;
    }
    
    console.log(`\n本轮待学习: ${chaptersToLearn.length} 个章节\n`);

    for (let i = 0; i < chaptersToLearn.length; i++) {
      const chapter = chaptersToLearn[i];
      const chapterStartTime = Date.now();

      console.log(`\n进度: ${i + 1}/${chaptersToLearn.length}\n`);

      const result = await startChapterLearning(page, chapter, context);
      if (!result.success || !result.page) {
        console.log(`⚠ 跳过第 ${chapter.index} 章`);
        updateProgress(courseId, chapter.index, 'failed', 0);
        continue;
      }

      const videoPage = result.page;
      const recovery = new NetworkRecovery(videoPage, browser);

      const completed = await waitForVideoCompletion(videoPage, recovery);
      
      const timeSpent = Math.floor((Date.now() - chapterStartTime) / 1000);
      
      if (completed) {
        updateProgress(courseId, chapter.index, 'completed', timeSpent);
        console.log(`✓ 第 ${chapter.index} 章学习完成 (用时: ${formatTime(timeSpent)})`);
      } else {
        console.log(`⚠ 第 ${chapter.index} 章学习可能未完成，继续下一章`);
        updateProgress(courseId, chapter.index, 'incomplete', timeSpent);
      }

      await closeVideoPage(videoPage);

      if (videoPage !== page) {
        await videoPage.close();
      }

      await page.waitForTimeout(3000);

      const backToChapter = await page.locator('div.small.inline-block[id^="D395finishStatus-"]').count() > 0;
      if (!backToChapter) {
        console.log('⚠ 未返回章节列表，尝试刷新页面...');
        await page.reload({ waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(3000);
      }
    }
    
    totalLearned += chaptersToLearn.length;
  }

  return true;
}

// ==================== 多课程学习流程 ====================
async function autoLearningProcess(page, context, currentPageUrl = null) {
  const courses = CONFIG.COURSES;
  
  for (let c = 0; c < courses.length; c++) {
    const course = courses[c];
    
    logSeparator(`开始学习: ${course.name}`);
    
    // 如果传入了当前页面URL且是第一个课程，使用当前页面
    if (c === 0 && currentPageUrl) {
      console.log(`使用当前页面: ${currentPageUrl}\n`);
      // 不重新导航，直接使用当前页面
    } else {
      console.log(`URL: ${course.url}\n`);
      // 导航到课程页面
      await page.goto(course.url, { waitUntil: 'domcontentloaded', timeout: 60000 });
      await page.waitForTimeout(3000);
    }
    
    // 学习这门课程
    await learnSingleCourse(page, context, course);
    
    // 课程间休息
    if (c < courses.length - 1) {
      console.log('\n等待5秒后开始下一门课程...');
      await page.waitForTimeout(5000);
    }
  }
  
  return true;
}

// ==================== 辅助函数 ====================
function printBanner() {
  logSeparator('MOOC 自动学习脚本 - 增强版');
  console.log('版本: 4.0 (多课程/后台运行版)');
  console.log('作者: CodeBuddy');
  console.log('功能: 进度保存 | 智能弹窗 | 统计报告 | 异常恢复 | 多课程 | 后台运行');
  logSeparator();
}

function printInstructions() {
  console.log('使用说明:');
  console.log('  1. 支持多课程配置 (在 COURSES 数组中添加)');
  console.log('  2. 自动保存学习进度 (意外中断可恢复)');
  console.log('  3. 智能处理各类弹窗');
  console.log('  4. 网络异常自动恢复');
  console.log('  5. 生成学习统计报告');
  console.log('  6. 支持后台运行模式\n');
  
  console.log('配置文件:');
  console.log(`  进度文件: ${CONFIG.PROGRESS.SAVE_FILE}`);
  console.log(`  报告文件: ${CONFIG.STATS.REPORT_FILE}\n`);
}

function setupErrorHandlers(page) {
  page.on('error', () => {});
  page.on('pageerror', () => {});
}

function handleCompletion(completed) {
  if (completed) {
    console.log('\n========================================');
    console.log('✓ 课程学习全部完成!');
    console.log('========================================');
  } else {
    console.log('\n学习结束');
  }
  
  printReport();
  
  if (!CONFIG.BACKGROUND.ENABLED) {
    console.log('\n按 Ctrl+C 退出脚本(浏览器将保持打开状态)...');
  }
}

async function keepRunning() {
  await new Promise(() => {});
}

async function cleanup() {
  if (browser) {
    console.log('\n正在关闭浏览器...');
    saveProgress();
    await browser.close();
    console.log('✓ 浏览器已关闭');
  }
}

function handleError(error) {
  console.error('\n========================================');
  console.error('发生错误:', error.message);
  console.error('========================================');
  
  if (error.stack) {
    console.error('\n错误堆栈:');
    console.error(error.stack);
  }
  
  // 保存进度
  saveProgress();
  
  console.log('\n浏览器将保持打开状态,按 Ctrl+C 退出脚本...');
  keepRunning();
}

// ==================== 主流程 ====================
async function main() {
  try {
    // 加载进度
    loadProgress();
    
    printBanner();
    printInstructions();

    console.log('启动浏览器...\n');

    const launchOptions = {
      headless: CONFIG.BROWSER.HEADLESS,
      channel: CONFIG.BROWSER.CHANNEL,
      args: CONFIG.BROWSER.ARGS
    };
    
    if (CONFIG.BROWSER.EXECUTABLE_PATH) {
      launchOptions.executablePath = CONFIG.BROWSER.EXECUTABLE_PATH;
    }
    
    browser = await chromium.launch(launchOptions);

    const context = await browser.newContext();

    let page = await context.newPage();

    setupErrorHandlers(page);

    // 使用第一个课程URL
    const firstCourse = CONFIG.COURSES[0];
    console.log(`打开页面: ${firstCourse.url}\n`);
    await page.goto(firstCourse.url, { waitUntil: 'domcontentloaded', timeout: 60000 });

    await page.waitForTimeout(2000);

    // 如果不是后台模式，给用户时间
    if (!CONFIG.BACKGROUND.ENABLED) {
      console.log('='.repeat(60));
      console.log('⏰ 您有 1 分钟时间：');
      console.log('   1. 在当前标签页中粘贴并修改URL地址');
      console.log('   2. 或打开新标签页并导航到学习页面');
      console.log('   3. 如不需修改，请保持当前页面等待自动继续');
      console.log('='.repeat(60));
      console.log(`\n当前页面: ${page.url()}\n`);

      for (let i = 60; i > 0; i--) {
        process.stdout.write(`\r等待中... 剩余 ${i} 秒 `);
        await page.waitForTimeout(1000);
      }

      console.log('\n\n等待结束，开始运行脚本...\n');

      const allPages = context.pages();
      console.log(`当前浏览器共有 ${allPages.length} 个标签页`);

      for (let i = 0; i < allPages.length; i++) {
        const p = allPages[i];
        console.log(`  标签页${i + 1}: ${p.url()}`);
      }

      if (allPages.length > 1) {
        console.log('\n检测到多个标签页，将使用最新打开的标签页');
        const lastPage = allPages[allPages.length - 1];
        console.log(`使用标签页: ${lastPage.url()}\n`);
        page = lastPage;
      } else {
        console.log(`使用当前标签页: ${page.url()}\n`);
      }
    }

    logSeparator('等待进入学习页面');

    console.log('等待页面加载...');
    await page.waitForTimeout(4000);

    try {
      const hasLearningElements = await page.locator('div.small.inline-block[id^="D395finishStatus-"]').count() > 0;

      if (hasLearningElements) {
        console.log('\n✓ 已进入学习章节目录页面\n');
      }
    } catch (err) {
      console.log('检查页面状态时出错:', err.message);
    }

    // 记录本次会话
    const sessionId = Date.now();
    progressData.stats.sessions.push({
      id: sessionId,
      startTime: new Date().toISOString(),
      course: firstCourse.name
    });

    // 获取当前页面URL，传递给学习流程（避免重新导航）
    const currentPageUrl = page.url();
    const completed = await autoLearningProcess(page, context, currentPageUrl);

    handleCompletion(completed);

    await keepRunning();

  } catch (error) {
    handleError(error);
  }
}

// ==================== 启动脚本 ====================
main().catch(console.error);
