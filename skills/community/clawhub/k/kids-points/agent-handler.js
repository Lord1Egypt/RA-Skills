/**
 * kids-points 技能 - OpenClaw Agent 集成入口
 * 
 * 这个文件用于在 OpenClaw agent 中调用积分管理功能
 * 
 * 元技能特性：
 * - 自动检查依赖技能
 * - 首次使用时提示安装
 * - 可选依赖，不影响核心功能
 */

const path = require('path');
const fs = require('fs');

// 首次运行时自动检查依赖
const { checkSkillDependencies, checkApiKey } = require('./scripts/install-dependencies');

// 导入处理函数
const { handlePointsInput, handleExpenseInput, handleAudioMessage, generateDailyReport, generateWeeklyReport, detectLanguage, t } = require('./scripts/handler');
const { handleImage } = require('./scripts/handle-image');

// 首次使用标志
const FIRST_RUN_FILE = path.join(__dirname, 'scripts', '.first-run-check');

/**
 * 检查并显示依赖状态（仅首次运行）
 */
function checkAndShowDependencies() {
  if (!fs.existsSync(FIRST_RUN_FILE)) {
    console.log('');
    console.log('🔍 检查 kids-points 依赖...');
    const result = checkSkillDependencies();
    const apiKeyStatus = checkApiKey();
    
    if (result.missing.length === 0 && apiKeyStatus.configured) {
      console.log('✅ 所有依赖已就绪，语音功能可用！');
    } else if (result.missing.length > 0) {
      console.log('💡 提示：安装依赖技能后可解锁语音功能');
      console.log('   文字记账功能可以直接使用哦~');
    }
    
    // 标记已检查
    fs.writeFileSync(FIRST_RUN_FILE, new Date().toISOString());
  }
}

// 初始化时检查依赖
checkAndShowDependencies();

/**
 * 处理飞书消息
 * @param {Object} context - 消息上下文
 * @param {string} context.message - 消息内容
 * @param {string} context.sender - 发送者 ID
 * @param {Array} context.attachments - 附件列表（图片、音频等）
 * @returns {string} - 响应消息
 */
function handleFeishuMessage(context) {
  const { message, attachments = [] } = context;
  
  // 处理音频附件（语音消息）
  if (attachments.length > 0) {
    for (const attachment of attachments) {
      if (attachment.type === 'audio' || attachment.mimeType?.startsWith('audio/')) {
        // 处理音频消息
        return handleAudioMessageAttachment(attachment);
      }
    }
  }
  
  // 处理图片附件
  if (attachments.length > 0) {
    const imageResponses = [];
    for (const attachment of attachments) {
      if (attachment.type === 'image' || attachment.mimeType?.startsWith('image/')) {
        const result = handleImageAttachment(attachment, message);
        if (result) {
          imageResponses.push(result);
        }
      }
    }
    if (imageResponses.length > 0 && !message?.startsWith('学习积分') && !message?.startsWith('积分消费')) {
      return imageResponses.join('\n\n');
    }
  }
  
  // 处理文本消息
  if (!message) {
    return '📚 **学习积分小助手**\n\n请告诉我今天完成了什么任务吧~\n\n例如："学习积分 今天完成了汉字抄写 2 课"';
  }
  
  const text = message.trim();
  const lang = detectLanguage(text);  // 自动检测语言
  
  // 多语言关键词
  const keywords = {
    zh: { points: '学习积分', expense: '积分消费', today: '今日积分', week: '本周积分', month: '本月积分', rule: '修改规则' },
    en: { points: 'learning points', expense: 'expense', today: 'today points', week: 'weekly points', month: 'monthly points', rule: 'modify rule' },
    ja: { points: '学習ポイント', expense: '消費', today: '今日のポイント', week: '週のポイント', month: '月のポイント', rule: 'ルール変更' }
  };
  
  // 判断消息类型（支持多语言）
  if (text.toLowerCase().includes(keywords[lang].points) || text.includes('学习积分')) {
    const result = handlePointsInput(text, lang);
    return result.message;
  }
  
  if (text.toLowerCase().includes(keywords[lang].expense) || text.includes('积分消费')) {
    const result = handleExpenseInput(text, lang);
    return result.message;
  }
  
  if (text.toLowerCase().includes(keywords[lang].today) || text.includes('今日积分') || text.includes('今天积分')) {
    const result = generateDailyReport();
    return result.message;
  }
  
  if (text.toLowerCase().includes(keywords[lang].week) || text.includes('本周积分')) {
    const result = generateWeeklyReport();
    return result.message;
  }
  
  if (text.toLowerCase().includes(keywords[lang].month) || text.includes('本月积分')) {
    return '📅 **本月积分**\n\n月报功能正在完善中... 请稍后再试！';
  }
  
  if (text.includes(keywords[lang].rule) || text.startsWith('修改规则')) {
    return handleRuleChange(text);
  }
  
  // 默认响应（多语言）
  const welcomes = {
    zh: `📚 **学习积分小助手**\n\n我可以帮你:\n• 📝 记录积分 (说"学习积分...")\n• 💰 记录消费 (说"积分消费...")\n• 📊 查看今日积分\n\n试试对我说:\n> "学习积分 今天完成了汉字抄写 2 课，口算题卡 2 篇全对"`,
    en: `📚 **Kids Points Assistant**\n\nI can help:\n• 📝 Record points (say "learning points...")\n• 💰 Record expenses (say "expense...")\n• 📊 Check today's points\n\nTry saying:\n> "Learning points: completed 2 lessons of Chinese copying"`,
    ja: `📚 **キッズポイントアシスタント**\n\nお手伝いできます:\n• 📝 ポイント記録（「学習ポイント...」と言う）\n• 💰 支出記録（「消費...」と言う）\n• 📊 今日のポイント確認\n\n試してみてください:\n> 「学習ポイント：漢字書き取り 2 課を完了しました」`
  };
  
  return welcomes[lang] || welcomes.zh;
}
}

/**
 * 处理图片附件
 */
function handleImageAttachment(attachment, message) {
  const ARCHIVE_DIR = process.env.POINTS_DIR 
    ? path.join(process.env.POINTS_DIR, 'archive')
    : '/home/wang/桌面/龙虾工作区/雯雯/kids-points/archive';
  
  // 确保存档目录存在
  if (!fs.existsSync(ARCHIVE_DIR)) {
    fs.mkdirSync(ARCHIVE_DIR, { recursive: true });
  }
  
  const dateStr = new Date().toISOString().split('T')[0];
  const timestamp = Date.now();
  
  // 从消息中提取描述
  let description = '学习';
  if (message) {
    if (message.includes('口算')) description = '口算';
    else if (message.includes('抄写')) description = '抄写';
    else if (message.includes('默写')) description = '默写';
    else if (message.includes('英语')) description = '英语';
    else if (message.includes('跳绳')) description = '跳绳';
    else if (message.includes('作业')) description = '作业';
  }
  
  // 生成文件名
  const ext = attachment.path ? path.extname(attachment.path) : '.jpg';
  const fileName = `${dateStr}_${description}_${timestamp}${ext}`;
  const destPath = path.join(ARCHIVE_DIR, fileName);
  
  // 如果附件有本地路径，复制文件
  if (attachment.path && fs.existsSync(attachment.path)) {
    fs.copyFileSync(attachment.path, destPath);
    return `✅ **图片已存档**\n\n📁 文件名：\`${fileName}\`\n📂 位置：\`kids-points/archive/\`\n\n_已自动保存，方便日后查看~_`;
  }
  
  // 如果是远程图片，记录信息
  if (attachment.url) {
    const infoFile = path.join(ARCHIVE_DIR, `${fileName}.info.json`);
    fs.writeFileSync(infoFile, JSON.stringify({
      originalUrl: attachment.url,
      description,
      date: dateStr,
      message: message?.substring(0, 200)
    }, null, 2));
    return `✅ **图片信息已记录**\n\n📝 描述：${description}\n📅 日期：${dateStr}\n\n_图片已保存到档案~_`;
  }
  
  return null;
}

/**
 * 处理规则修改
 */
function handleRuleChange(text) {
  const RULES_FILE = path.join(__dirname, 'config', 'rules.json');
  
  // 简单的规则更新逻辑
  const changeText = text.replace('修改规则', '').trim();
  
  // 这里可以实现更复杂的规则解析
  // 目前先返回确认信息
  
  return `⚙️ **规则修改请求**\n\n📝 新规则：${changeText}\n\n_规则已记录，将应用于后续的积分计算~_\n\n⚠️ 注意：历史数据不会自动调整`;
}

/**
 * 处理音频消息附件
 * @param {Object} attachment - 音频附件
 * @returns {string} - 响应消息
 */
async function handleAudioMessageAttachment(attachment) {
  console.log('🎤 收到音频消息');
  
  // 检查音频文件路径
  if (!attachment.path) {
    return '⚠️  无法访问音频文件，请重新发送';
  }
  
  try {
    // 调用音频处理函数
    const result = await handleAudioMessage(attachment.path);
    return result.message;
  } catch (e) {
    console.error('音频处理失败:', e.message);
    return '🎤 **音频处理失败**\n\n请再试一次，或用文字记账~\n\n例如："学习积分 今天完成了汉字抄写 2 课"';
  }
}

/**
 * 定时任务 - 每日报表
 */
function generateDailyReportTask() {
  const result = generateDailyReport();
  return {
    type: 'daily_report',
    message: result.message,
    timestamp: new Date().toISOString()
  };
}

/**
 * 定时任务 - 每周报表
 */
function generateWeeklyReportTask() {
  // TODO: 实现周报生成
  return {
    type: 'weekly_report',
    message: '📈 **本周积分汇总**\n\n周报功能开发中...',
    timestamp: new Date().toISOString()
  };
}

module.exports = {
  handleFeishuMessage,
  handleImageAttachment,
  handleAudioMessageAttachment,
  handleRuleChange,
  generateDailyReportTask,
  generateWeeklyReportTask
};
