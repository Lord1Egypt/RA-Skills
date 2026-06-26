/**
 * OpenClaw AI 专用入口
 *
 * 用途：为 OpenClaw AI 提供统一的技能调用接口
 * 特点：错误处理 + 锁释放 + 结果格式化
 *
 * 功能：
 * - 内容检查问答引导
 * - fixContentIssue() 处理单个内容检查问题
 * - getIssueFixOptions() 获取问题的修补选项
 */

const VERSION = require('./version');
const { prdWorkflow } = require('./main');
const fs = require('fs');
const path = require('path');

/**
 * AI 调用入口
 * 
 * @param {string} userInput - 用户需求（如"生成养老规划 PRD"）
 * @param {object} options - 配置选项
 * @param {string} options.userId - 用户 ID（从 OpenClaw 上下文获取）
 * @param {string} options.mode - 执行模式：'auto' | 'iteration' | 'fresh' | 'rollback'
 * @param {boolean} options.autoRetry - 自动重试（默认 true）
 * 
 * @returns {Promise<object>} AI 友好的结果
 */
async function executeForAI(userInput, options = {}) {
  const startTime = Date.now();
  
  console.log('\n🤖 AI 调用入口：executeForAI');
  console.log(`   用户需求：${userInput}`);
  console.log(`   用户 ID: ${options.userId || 'default'}`);
  console.log(`   执行模式：${options.mode || 'auto'}`);
  console.log(`   自动重试：${options.autoRetry !== false}\n`);
  
  // AI 执行器（用于 interview 模块）
  const aiExecutor = async (prompt) => {
    return await sessions_spawn({
      runtime: 'subagent',
      mode: 'run',
      task: prompt,
      timeoutSeconds: 120
    });
  };
  
  try {
    // 调用主工作流
    const result = await prdWorkflow(userInput, {
      userId: options.userId,
      mode: options.mode || 'auto',
      autoRetry: options.autoRetry !== false,
      aiExecutor: aiExecutor
    });
    
    const duration = Date.now() - startTime;

    // ✅ 直接访问 outputDir（DataBus 一定会设置）
    const outputDir = result.status.outputDir;

    // ⭐ v3.1.0 新增：检查是否有内容检查问题需要引导
    const reviewResult = result.results?.review;
    const contentIssues = reviewResult?.content?.issues || [];
    const needsContentFixGuide = contentIssues.length > 0;

    // 返回 AI 友好的结果
    return {
      success: true,
      duration: duration,
      outputDir: outputDir,
      prdPath: `${outputDir}PRD.md`,
      wordPath: `${outputDir}PRD.docx`,
      versionsDir: `${outputDir}.versions/`,
      summary: {
        features: extractFeatures(result),
        wordCount: extractWordCount(result),
        version: getCurrentVersion(result),
        reviewScore: reviewResult?.overall || 0,
        contentIssues: contentIssues.length
      },
      // ⭐ v3.1.0 新增：内容检查问答引导信息
      contentFixGuide: needsContentFixGuide ? {
        needed: true,
        issues: contentIssues.map(issue => ({
          id: issue.id,
          checkItem: issue.check_item_name,
          priority: issue.priority,
          section: issue.section_title,
          description: issue.description,
          suggestion: issue.suggestion
        })),
        message: `内容检查发现 ${contentIssues.length} 个问题，需要逐个引导用户处理`
      } : {
        needed: false
      },
      message: needsContentFixGuide
        ? `⚠️ PRD 生成完成，但内容检查发现 ${contentIssues.length} 个问题需要处理`
        : `✅ PRD 生成完成，耗时 ${Math.round(duration/1000)}秒`
    };
    
  } catch (error) {
    const duration = Date.now() - startTime;
    
    console.error('\n❌ AI 调用失败:', error.message);
    console.error(`   错误码：${getErrorCode(error)}`);
    console.error(`   耗时：${Math.round(duration/1000)}秒\n`);
    
    // 确保释放锁（重要！）
    await cleanupLock(options);
    
    return {
      success: false,
      duration: duration,
      error: error.message,
      errorCode: getErrorCode(error),
      suggestion: getSuggestion(error),
      message: `❌ 执行失败：${error.message}`
    };
  }
}

/**
 * 清理锁文件
 */
async function cleanupLock(options) {
  try {
    // ✅ 使用技能根目录
    const skillRootDir = path.resolve(__dirname, '..');
    const lockFile = path.join(skillRootDir, 'output', '.lock');
    if (fs.existsSync(lockFile)) {
      fs.unlinkSync(lockFile);
      console.log('🔓 已清理残留锁文件');
    }
  } catch (cleanupError) {
    console.warn('⚠️  清理锁文件失败:', cleanupError.message);
  }
}

/**
 * 从结果中提取功能数量
 */
function extractFeatures(result) {
  try {
    return result?.prd?.features?.length || 0;
  } catch {
    return 0;
  }
}

/**
 * 从结果中提取字数
 */
function extractWordCount(result) {
  try {
    return result?.prd?.wordCount || 0;
  } catch {
    return 0;
  }
}

/**
 * 获取当前版本号
 */
function getCurrentVersion(result) {
  try {
    return result?.version || 'v1';
  } catch {
    return 'v1';
  }
}

/**
 * 获取错误码
 */
function getErrorCode(error) {
  const message = error.message.toLowerCase();
  
  if (message.includes('模块不存在') || message.includes('module')) {
    return 'MODULE_NOT_FOUND';
  }
  if (message.includes('锁') || message.includes('lock') || message.includes('并发')) {
    return 'LOCK_CONFLICT';
  }
  if (message.includes('质量') || message.includes('quality') || message.includes('门禁')) {
    return 'QUALITY_FAILED';
  }
  if (message.includes('需求拆解') || message.includes('decomposition')) {
    return 'DECOMPOSITION_ERROR';
  }
  if (message.includes('超时') || message.includes('timeout')) {
    return 'TIMEOUT';
  }
  
  return 'UNKNOWN_ERROR';
}

/**
 * 获取错误建议
 */
function getSuggestion(error) {
  const errorCode = getErrorCode(error);
  
  switch (errorCode) {
    case 'MODULE_NOT_FOUND':
      return '请检查技能是否正确安装，或联系技能开发者';
    
    case 'LOCK_CONFLICT':
      return '检测到并发执行，请等待其他执行完成后再试';
    
    case 'QUALITY_FAILED':
      return '请根据评审意见修改需求后重试，或降低质量要求';
    
    case 'DECOMPOSITION_ERROR':
      return '请提供更详细的需求描述，或先执行需求拆解';
    
    case 'TIMEOUT':
      return '执行超时，请检查网络或减少复杂度';
    
    default:
      return '请检查输入并重试，或查看详细错误信息';
  }
}

/**
 * 快速检查技能状态
 *
 * @returns {object} 技能状态
 */
async function checkSkillStatus() {
  console.log('🔍 检查技能状态...\n');

  const status = {
    version: VERSION.version,
    modules: {},
    templates: {},
    isValid: true
  };

  // 检查模块
  const modulesDir = path.join(__dirname, 'modules');
  if (fs.existsSync(modulesDir)) {
    const modules = fs.readdirSync(modulesDir)
      .filter(f => f.endsWith('.js'))
      .map(f => f.replace('_module.js', ''));

    status.modules = {
      available: modules,
      count: modules.length
    };
  } else {
    status.modules = {
      available: [],
      count: 0,
      error: 'modules 目录不存在'
    };
    status.isValid = false;
  }

  // 检查模板
  const templatesDir = path.join(__dirname, 'templates');
  if (fs.existsSync(templatesDir)) {
    const templates = fs.readdirDir(templatesDir)
      .filter(f => f.endsWith('.md'));

    status.templates = {
      available: templates,
      count: templates.length
    };
  } else {
    status.templates = {
      available: [],
      count: 0,
      error: 'templates 目录不存在'
    };
    status.isValid = false;
  }

  console.log(`✅ 技能版本：${status.version}`);
  console.log(`📦 可用模块：${status.modules.count}个`);
  console.log(`📄 可用模板：${status.templates.count}个`);
  console.log(`状态：${status.isValid ? '✅ 正常' : '❌ 异常'}\n`);

  return status;
}

/**
 * ⭐ v3.1.0 新增：处理内容检查问题
 *
 * 供 AI Agent 在问答引导后调用，执行用户选择的修补方式
 *
 * @param {object} options - 修补选项
 * @param {string} options.outputDir - PRD 输出目录
 * @param {object} options.issue - 问题对象
 * @param {string} options.action - 处理方式：'auto' | 'user_guide' | 'skip'
 * @param {string} options.userInstruction - 用户指令（可选）
 *
 * @returns {Promise<object>} 修补结果
 */
async function fixContentIssue(options) {
  console.log('\n🔧 处理内容检查问题...');

  const { outputDir, issue, action, userInstruction } = options;

  // 创建 aiExecutor
  const aiExecutor = async (prompt) => {
    return await sessions_spawn({
      runtime: 'subagent',
      mode: 'run',
      task: prompt,
      timeoutSeconds: 120
    });
  };

  // 加载模块
  const ReviewModule = require('./modules/review_module');
  const reviewModule = new ReviewModule();

  // 模拟 DataBus（读取 PRD）
  const { DataBus } = require('./data_bus');
  const dataBus = new DataBus('', { outputDir });

  // 读取 PRD
  const prdRecord = dataBus.read('prd');
  if (!prdRecord) {
    return {
      success: false,
      error: 'PRD 不存在'
    };
  }

  const prd = prdRecord.data;

  // 执行修补
  const fixResult = await reviewModule.fixIssue(issue, action, userInstruction, prd, aiExecutor);

  // 应用修补到 PRD
  if (fixResult.success && fixResult.action !== 'skip') {
    await reviewModule.applyFix(prd, fixResult, dataBus);
  }

  return {
    success: fixResult.success,
    action: fixResult.action,
    issue: fixResult.issue,
    message: fixResult.message || (fixResult.success ? '处理成功' : '处理失败')
  };
}

/**
 * ⭐ v3.1.0 新增：获取问题的修补选项
 *
 * 供 AI Agent 使用 AskUserQuestion 时调用
 *
 * @param {object} issue - 问题对象
 * @returns {object} 修补选项列表
 */
function getIssueFixOptions(issue) {
  const ReviewModule = require('./modules/review_module');
  const reviewModule = new ReviewModule();
  return reviewModule.getFixOptions(issue);
}

module.exports = {
  executeForAI,
  checkSkillStatus,
  fixContentIssue,
  getIssueFixOptions
};
