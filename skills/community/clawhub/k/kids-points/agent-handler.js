/**
 * kids-points 技能 - OpenClaw Agent 集成入口
 * 
 * 核心功能：
 * - ✅ 积分记录（语意识别 + 自动记账）
 * - ✅ 积分消费（语意识别 + 自动扣减）
 * - ✅ 余额查询（读取 balance.md，跨 Session 一致）
 * - ✅ 输入日志（审计追踪，防重复）
 */

const path = require('path');
const fs = require('fs');

// 依赖检查
const { checkSkillDependencies, checkApiKey } = require('./scripts/install-dependencies');

// 导入处理函数
const { recordPoints, recordExpense, getBalanceInfo, checkDuplicate, checkRequestProcessed, markRequestProcessed } = require('./scripts/handler');
const { handleImage } = require('./scripts/handle-image');
const { enhanceMessage, speak, toPlainText } = require('./scripts/tips');

// 数据文件路径
const POINTS_DIR = process.env.POINTS_DIR || path.join(__dirname, '..', '..', 'kids-points');
const BALANCE_FILE = path.join(POINTS_DIR, 'balance.json');
const LOG_FILE = path.join(POINTS_DIR, 'logs', 'input.log');

/**
 * 获取今日日期字符串
 */
function getTodayStr() {
  // 北京时间 = UTC + 8
  const bj = new Date(Date.now() + 8 * 3600 * 1000);
  return bj.toISOString().split('T')[0];
}

/**
 * 获取周统计范围
 */
function getWeekRange(weekType = 'this') {
  const now = new Date();
  const dayOfWeek = now.getDay(); // 0=周日，1=周一
  const mondayOffset = dayOfWeek === 0 ? -6 : 1 - dayOfWeek;
  
  let monday, sunday;
  
  if (weekType === 'this') {
    // 本周一到今天
    monday = new Date(now);
    monday.setDate(now.getDate() + mondayOffset);
    sunday = now;
  } else {
    // 上周一到上周日
    monday = new Date(now);
    monday.setDate(now.getDate() + mondayOffset - 7);
    sunday = new Date(monday);
    sunday.setDate(monday.getDate() + 6);
  }
  
  return {
    monday: monday.toISOString().split('T')[0],
    sunday: sunday.toISOString().split('T')[0],
    today: now.toISOString().split('T')[0]
  };
}

/**
 * 获取周统计数据
 */
function getWeeklyStats(weekType = 'this') {
  const range = getWeekRange(weekType);
  const content = fs.readFileSync(BALANCE_FILE, 'utf8');
  const data = JSON.parse(content);
  const history = data.history || [];
  
  const expenses = [];
  const incomes = [];
  
  for (const record of history) {
    const date = record.date;
    const type = record.type;
    const change = record.change;
    const desc = record.description;
    
    if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) continue;
    
    if (date >= range.monday && date <= range.sunday) {
      if (type === 'expense') {
        expenses.push({ date, amount: Math.abs(parseFloat(change)), desc });
      } else if (type === 'income') {
        incomes.push({ date, amount: parseFloat(change), desc });
      }
    }
  }
  
  expenses.sort((a, b) => a.date.localeCompare(b.date));
  incomes.sort((a, b) => a.date.localeCompare(b.date));
  
  const totalExpense = expenses.reduce((sum, e) => sum + e.amount, 0);
  const totalIncome = incomes.reduce((sum, i) => sum + i.amount, 0);
  
  return {
    range,
    expenses,
    incomes,
    totalExpense,
    totalIncome,
    netChange: totalIncome - totalExpense
  };
}

/**
 * 格式化周统计报告
 */
function formatWeeklyStats(stats) {
  const { range, expenses, incomes, totalExpense, totalIncome, netChange } = stats;
  const weekLabel = range.monday === range.today ? '本周' : '上周';
  
  let msg = `📊 **${weekLabel}积分统计**\n\n`;
  msg += `**统计范围**: ${range.monday} 至 ${range.sunday}\n\n`;
  
  msg += `## 📈 收入记录（${incomes.length}笔）\n\n`;
  if (incomes.length === 0) {
    msg += '无收入记录\n\n';
  } else {
    msg += '| 日期 | 加分 | 任务 |\n|------|------|------|\n';
    incomes.slice(0, 10).forEach(i => {
      msg += `| ${i.date} | +${i.amount.toFixed(1)}分 | ${i.desc} |\n`;
    });
    if (incomes.length > 10) {
      msg += `\n...还有 ${incomes.length - 10} 笔\n`;
    }
    msg += `\n**💰 总收入**: ${totalIncome.toFixed(1)}分\n\n`;
  }
  
  msg += `## 💸 支出记录（${expenses.length}笔）\n\n`;
  if (expenses.length === 0) {
    msg += '无支出记录\n\n';
  } else {
    msg += '| 日期 | 扣分 | 原因 |\n|------|------|------|\n';
    expenses.forEach(e => {
      msg += `| ${e.date} | -${e.amount.toFixed(1)}分 | ${e.desc} |\n`;
    });
    msg += `\n**💰 总支出**: ${totalExpense.toFixed(1)}分\n\n`;
  }
  
  msg += `## 📊 总结\n\n`;
  msg += `| 项目 | 数值 |\n|------|------|\n`;
  msg += `| 收入笔数 | ${incomes.length}笔 |\n`;
  msg += `| 支出笔数 | ${expenses.length}笔 |\n`;
  msg += `| 总收入 | +${totalIncome.toFixed(1)}分 |\n`;
  msg += `| 总支出 | -${totalExpense.toFixed(1)}分 |\n`;
  msg += `| **净变动** | **${netChange >= 0 ? '+' : ''}${netChange.toFixed(1)}分** |\n`;
  
  // 添加简短分析
  if (netChange >= 0) {
    msg += `\n🌟 **表现不错**！${weekLabel}是正收益，继续保持~`;
  } else {
    msg += `\n💡 **注意**：${weekLabel}是负收益，注意控制开销哦~`;
  }
  
  return msg;
}

/**
 * 生成周统计的纯文本播报版本（只播报总计和分析）
 */
function formatWeeklyStatsForSpeech(stats) {
  const { range, expenses, incomes, totalExpense, totalIncome, netChange } = stats;
  const weekLabel = range.monday === range.today ? '本周' : '上周';
  
  let plain = `${weekLabel}积分统计，统计范围从${range.monday}到${range.sunday}。`;
  plain += `总收入${totalIncome.toFixed(1)}分，共${incomes.length}笔。`;
  plain += `总支出${totalExpense.toFixed(1)}分，共${expenses.length}笔。`;
  plain += `净变动${netChange >= 0 ? '正' : '负'}${Math.abs(netChange).toFixed(1)}分。`;
  
  if (netChange >= 0) {
    plain += '表现不错，是正收益，继续保持。';
  } else {
    plain += '注意，是负收益，注意控制开销哦。';
  }
  
  return plain;
}

/**
 * 获取当前余额（强制每次读取文件，不缓存）
 * 注意：不允许 Agent 直接读文件，必须通过这个函数
 */
function refreshBalanceCache() {
  // 实际上不缓存，每次都调用 handler.getCurrentBalance()
  // 这个函数只是为了保持接口兼容
  return require('./scripts/handler').getCurrentBalance();
}

// 首次使用标志
const FIRST_RUN_FILE = path.join(__dirname, 'scripts', '.first-run-check');

function checkAndShowDependencies() {
  if (!fs.existsSync(FIRST_RUN_FILE)) {
    console.log('🔍 检查 kids-points 依赖...');
    const result = checkSkillDependencies();
    const apiKeyStatus = checkApiKey();
    
    if (result.missing.length === 0 && apiKeyStatus.configured) {
      console.log('✅ 所有依赖已就绪，语音功能可用！');
    } else if (result.missing.length > 0) {
      console.log('💡 文字记账功能可以直接使用~');
    }
    
    fs.writeFileSync(FIRST_RUN_FILE, new Date().toISOString());
  }
}

checkAndShowDependencies();

/**
 * 获取指定日期字符串
 * @param {string} dateRef - 日期引用：'today' | 'yesterday' | 'YYYY-MM-DD'
 */
function getDateStr(dateRef = 'today') {
  if (dateRef === 'today') {
    return getTodayStr();
  }
  if (dateRef === 'yesterday') {
    // 用北京时间计算昨天
    const bj = new Date(Date.now() + 8 * 3600 * 1000);
    bj.setDate(bj.getDate() - 1);
    return bj.toISOString().split('T')[0];
  }
  // 假设是 YYYY-MM-DD 格式
  return dateRef;
}

/**
 * 处理飞书消息
 */
async function handleFeishuMessage(context) {
  const { message, attachments = [], date = 'today', messageId, enableSpeech = true } = context; // ✅ 默认开启语音播报
  
  // ✅ 请求去重检查（防止同一消息被处理多次）
  const checkResult = messageId ? checkRequestProcessed(messageId) : { processed: false };
  if (checkResult.processed) {
    console.log('⚠️ 请求已处理，跳过:', messageId);
    console.log('  原始输入:', checkResult.input);
    console.log('  原始分数:', checkResult.points);
    return null; // 返回 null 表示已处理，不需要重复响应
  }
  
  // ✅ 强制每次读取最新余额（不缓存）
  const currentBalance = refreshBalanceCache();
  
  // 处理音频附件（语音消息）
  if (attachments.length > 0) {
    for (const attachment of attachments) {
      if (attachment.type === 'audio' || attachment.mimeType?.startsWith('audio/')) {
        return handleAudioMessageAttachment(attachment);
      }
    }
  }
  
  // 处理图片附件
  if (attachments.length > 0) {
    for (const attachment of attachments) {
      if (attachment.type === 'image' || attachment.mimeType?.startsWith('image/')) {
        const result = handleImage(attachment, message);
        if (result) return result;
      }
    }
  }
  
  // 处理文本消息
  if (!message) {
    return '📚 **积分助手**\n\n请告诉我今天完成了什么任务吧~\n\n例如："今天完成了汉字抄写 2 课，口算题卡 2 篇全对"';
  }
  
  const text = message.trim();
  const dateStr = getDateStr(date);
  
  // ✅ 查询类关键词（优先检查，避免被误判为收入/支出）
  const queryKeywords = ['多少分', '余额', '今日积分', '今天积分', '本周积分', '这周积分', '上周积分', '上周统计', '本周统计', '这周统计', '本周积分记录'];
  const isQuery = queryKeywords.some(keyword => text.includes(keyword));
  
  if (isQuery) {
    const balance = refreshBalanceCache(); // ✅ 强制读取最新
    const msg = `📊 **当前积分**\n\n当前余额：**${balance.toFixed(1)}分**\n\n_数据来自 balance.json，随时可以查看_`;
    const plainText = toPlainText(msg);
    // ✅ 语音播报（默认开启）
    speak(plainText).catch(() => {});
    return msg + '\n\n---\n🔊 **朗读文本**: ' + plainText;
  }
  
  // ✅ 支出类关键词（第二优先，避免被收入关键词覆盖）
  const expenseKeywords = ['积分消费', '花了', '买了', '忘带', '忘了', '忘记', '没写', '没完成', '迟到', '看动画', '吃零食', '买玩具', '忘写', '扣'];
  const isExpense = expenseKeywords.some(keyword => text.includes(keyword));
  
  if (isExpense) {
    // ✅ 使用 LLM 提取结构化数据（金额 + 用途）
    const llmResult = await callLLM_ExtractExpense(text);
    
    if (!llmResult.success) {
      // LLM 无法提取，返回提示让用户说清楚
      const msg = '😕 请说清楚花了多少分，例如："积分消费 买零食花了 20 分"';
      const plainText = toPlainText(msg);
      speak(plainText).catch(() => {});
      return msg + '\n\n---\n🔊 **朗读文本**: ' + plainText;
    }
    
    const { amount, description } = llmResult;
    const result = recordExpense(amount, description, text);
    
    // ✅ 标记请求已处理（防止重复）- 传入消费金额
    if (messageId) markRequestProcessed(messageId, text, -result.amount);
    // ✅ 添加小贴士
    const enhancedMessage = enhanceMessage(result.message, 'expense', true);
    // ✅ 生成纯文本版本用于语音朗读
    const plainText = toPlainText(enhancedMessage);
    // ✅ 语音播报（默认开启）
    speak(plainText).catch(() => {});
    // ✅ 返回带纯文本的版本
    return enhancedMessage + '\n\n---\n🔊 **朗读文本**: ' + plainText;
  }
  
  // ✅ 收入类关键词（最后检查）
  // 注意：'分' 不能放在这里，会误判 "多少分" 这种查询
  const incomeKeywords = ['学习积分', '完成了', '做了', '写了', '读了', '加了', '加', '全对', '没全对', '作业', '口算', '语文', '数学', '英语', '汉字', '跳绳', '起床', '收拾', '表扬', '老师表扬'];
  const isIncome = incomeKeywords.some(keyword => text.includes(keyword));
  
  if (isIncome) {
    // ✅ 使用 LLM 提取结构化数据（任务列表 + 积分）
    const llmResult = await callLLM_ExtractIncome(text);
    
    if (!llmResult.success) {
      // LLM 无法提取，返回提示
      const msg = '😕 没有识别到有效的积分任务，请说清楚完成了什么，例如："汉字抄写2课加3分"';
      const plainText = toPlainText(msg);
      speak(plainText).catch(() => {});
      return msg + '\n\n---\n🔊 **朗读文本**: ' + plainText;
    }
    
    const { tasks } = llmResult;
    const result = recordPoints(text, tasks, dateStr, messageId);
    // ✅ 标记请求已处理（防止重复）- 传入实际积分
    const totalPoints = tasks.reduce((sum, t) => sum + (t.points || 0), 0);
    if (messageId) markRequestProcessed(messageId, text, totalPoints);
    // ✅ 添加小贴士
    const enhancedMessage = enhanceMessage(result.message, 'income', true);
    // ✅ 生成纯文本版本用于语音朗读
    const plainText = toPlainText(enhancedMessage);
    // ✅ 语音播报（默认开启）
    speak(plainText).catch(() => {});
    // ✅ 返回带纯文本的版本
    return enhancedMessage + '\n\n---\n🔊 **朗读文本**: ' + plainText;
  }
  
  if (text.includes('本周积分') || text.includes('这周积分')) {
    const balanceInfo = getBalanceInfo();
    const msg = `📈 **本周积分**\n\n${balanceInfo.message}\n\n_周报功能开发中..._`;
    const plainText = toPlainText(msg);
    return msg + '\n\n---\n🔊 **朗读文本**: ' + plainText;
  }
  
  // 上周积分统计
  if (text.includes('上周积分') || text.includes('上一周') || text.includes('上周统计')) {
    const stats = getWeeklyStats('last');
    const msg = formatWeeklyStats(stats);
    // ✅ 统计任务：只播报总计和分析，不逐条念记录
    const speechText = formatWeeklyStatsForSpeech(stats);
    return msg + '\n\n---\n🔊 **朗读文本**: ' + speechText;
  }
  
  // 本周积分统计
  if (text.includes('本周统计') || text.includes('这周统计') || text.includes('本周积分记录')) {
    const stats = getWeeklyStats('this');
    const msg = formatWeeklyStats(stats);
    // ✅ 统计任务：只播报总计和分析，不逐条念记录
    const speechText = formatWeeklyStatsForSpeech(stats);
    return msg + '\n\n---\n🔊 **朗读文本**: ' + speechText;
  }
  
  // 默认响应
  return `📚 **积分助手**\n\n我可以帮你:\n• 📝 记录积分 (说"今天完成了 xxx")\n• 💰 记录消费 (说"积分消费 xxx")\n• 📊 查询余额 (说"多少分")\n\n试试对我说:\n> "今天完成了汉字抄写 2 课，口算题卡 2 篇全对"`;
}

/**
 * 调用 LLM 提取消费信息（金额 + 用途）
 * 使用 MiniMax 模型进行结构化信息提取
 */
async function callLLM_ExtractExpense(text) {
  try {
    const apiKey = process.env.MINIMAX_API_KEY || 'sk-cp-hXK39xUBG_wng0vkZtBa_5Kl-dAs20OiILoc3PfJNK5f5EVKVuGi9WY3b1QlpeK3iP6eJaRiUKNzBlWq4ueRVAM7H9NrEMGe8rmEyMn9xIjtTv9MZwPfZNw';
    
    const response = await fetch('https://api.minimaxi.com/v1/text/chatcompletion_v2', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
      },
      body: JSON.stringify({
        model: 'MiniMax-M2.5',
        messages: [
          { role: 'system', content: '你是一个积分消费解析器，只返回 JSON，不要其他内容。' },
          { role: 'user', content: `根据用户输入，提取"金额"和"用途"。金额必须是正数（单位：分），用途要简洁。\n\n示例：\n输入: "积分消费买零食花了30分"\n输出: {"success": true, "amount": 30, "description": "买零食"}\n\n输入: "看动画扣了20分"\n输出: {"success": true, "amount": 20, "description": "看动画"}\n\n输入: "买玩具花了5元"
输出: {"success": true, "amount": 5, "description": "买玩具"}\n\n请解析："${text}"` }
        ]
      })
    });
    
    if (!response.ok) {
      console.error('MiniMax API 错误:', response.status);
      return { success: false };
    }
    
    const data = await response.json();
    const content = data.choices?.[0]?.message?.content || '';
    
    // 解析 JSON
    let result;
    try {
      const jsonStr = content.replace(/```json\n?|\n?```/g, '').trim();
      result = JSON.parse(jsonStr);
    } catch (e) {
      console.error('LLM 返回不是有效 JSON:', content);
      return { success: false };
    }
    
    if (!result.success) {
      return { success: false };
    }
    
    // 验证数据
    if (typeof result.amount !== 'number' || result.amount <= 0) {
      return { success: false };
    }
    
    return {
      success: true,
      amount: result.amount,
      description: (result.description || '消费').trim()
    };
  } catch (e) {
    console.error('调用 LLM 失败:', e.message);
    return { success: false };
  }
}

/**
 * 调用 LLM 提取收入信息（任务列表 + 积分）
 * 使用 MiniMax 模型进行结构化信息提取
 * 支持多个任务（如："汉字抄写2课 +3分，口算1篇 +2分"）
 */
async function callLLM_ExtractIncome(text) {
  try {
    const apiKey = process.env.MINIMAX_API_KEY || 'sk-cp-hXK39xUBG_wng0vkZtBa_5Kl-dAs20OiILoc3PfJNK5f5EVKVuGi9WY3b1QlpeK3iP6eJaRiUKNzBlWq4ueRVAM7H9NrEMGe8rmEyMn9xIjtTv9MZwPfZNw';
    
    const response = await fetch('https://api.minimaxi.com/v1/text/chatcompletion_v2', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
      },
      body: JSON.stringify({
        model: 'MiniMax-M2.5',
        messages: [
          { role: 'system', content: '你是一个积分收入解析器，只返回 JSON，不要其他内容。' },
          { role: 'user', content: `根据用户输入，提取所有任务和对应的积分。

规则：
- 积分必须是正数
- 每个任务独立计算积分
- 任务描述要简洁（去掉"加X分"部分）
- 如果没有明确积分，设为 0

示例：
输入: "今天完成了汉字抄写2课，加3分，口算1篇全对加2分"
输出: {"success":true,"tasks":[{"task":"汉字抄写2课","points":3},{"task":"口算1篇全对","points":2}]}

输入: "ABC Reading 读了一篇"
输出: {"success":true,"tasks":[{"task":"ABC Reading 读了一篇","points":0}]}

输入: "跳绳350个加2分"
输出: {"success":true,"tasks":[{"task":"跳绳350个","points":2}]}

请解析："${text}"` }
        ]
      })
    });
    
    if (!response.ok) {
      console.error('MiniMax API 错误:', response.status);
      return { success: false };
    }
    
    const data = await response.json();
    const content = data.choices?.[0]?.message?.content || '';
    
    // 解析 JSON
    let result;
    try {
      const jsonStr = content.replace(/```json\n?|\n?```/g, '').trim();
      result = JSON.parse(jsonStr);
    } catch (e) {
      console.error('LLM 返回不是有效 JSON:', content);
      return { success: false };
    }
    
    if (!result.success || !Array.isArray(result.tasks) || result.tasks.length === 0) {
      return { success: false };
    }
    
    // 验证数据
    const validTasks = result.tasks.filter(t => {
      return typeof t.task === 'string' && t.task.length > 0;
    });
    
    if (validTasks.length === 0) {
      return { success: false };
    }
    
    return {
      success: true,
      tasks: validTasks.map(t => ({
        task: t.task.trim(),
        points: typeof t.points === 'number' ? t.points : 0
      }))
    };
  } catch (e) {
    console.error('调用 LLM 失败:', e.message);
    return { success: false };
  }
}

/**
 * 处理音频消息附件
 */
async function handleAudioMessageAttachment(attachment) {
  if (!attachment.path) {
    return '⚠️ 无法访问音频文件，请重新发送';
  }
  
  // 检查 ASR 配置
  if (!checkApiKey().configured) {
    return '🎤 **收到音频消息！**\n\n⚠️ 语音识别需要配置 SenseAudio API Key\n\n📋 快速配置：\n1. 访问 https://senseaudio.cn\n2. 免费注册账号\n3. 添加 API Key 到 ~/.openclaw/openclaw.json';
  }
  
  const ASR_SCRIPT = path.join(POINTS_DIR, '..', 'senseaudio-voice', 'scripts', 'asr.py');
  const cmd = `python3 "${ASR_SCRIPT}" "${attachment.path}"`;
  
  return new Promise((resolve) => {
    const { exec } = require('child_process');
    exec(cmd, (error, stdout) => {
      if (error) {
        resolve({ success: false, message: '🎤 语音识别失败，请用文字记账~' });
        return;
      }
      
      const recognizedText = stdout.trim();
      if (!recognizedText) {
        resolve({ success: false, message: '🎤 没有识别到内容~' });
        return;
      }
      
      // 递归处理识别的文本
      const result = handleFeishuMessage({ message: recognizedText });
      resolve(result);
    });
  });
}

module.exports = {
  handleFeishuMessage,
  handleAudioMessageAttachment,
  refreshBalanceCache,
  getWeeklyStats,
  formatWeeklyStats,
  formatWeeklyStatsForSpeech,
  callLLM_ExtractExpense,
  callLLM_ExtractIncome
};
