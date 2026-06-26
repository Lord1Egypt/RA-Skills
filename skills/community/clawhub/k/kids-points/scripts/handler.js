/**
 * 积分管理核心处理器
 * 
 * 职责：
 * - ✅ 记账操作（写入 balance.json + input.log）
 * - ✅ 防重复检查
 * - ✅ 余额查询
 * 
 * 注意：语义理解由 Agent (LLM) 完成，本模块只负责确定性操作
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE = process.env.WORKSPACE || '/home/wang/.openclaw/agents/kids-study/workspace';
const POINTS_DIR = process.env.POINTS_DIR || path.join(WORKSPACE, 'kids-points');
const BALANCE_FILE = path.join(POINTS_DIR, 'balance.json');
const LOG_FILE = path.join(POINTS_DIR, 'logs', 'input.log');

/**
 * 获取今日日期字符串（北京时间）
 */
function getTodayStr() {
  const now = new Date();
  // 转为北京时间 (UTC+8)
  const bj = new Date(now.getTime() + 8 * 60 * 60 * 1000);
  return bj.toISOString().split('T')[0];
}

/**
 * 获取北京时间格式化时间字符串 YYYY-MM-DD HH:mm:ss
 */
function getBeijingTimeStr() {
  const now = new Date();
  // 转为北京时间 (UTC+8)
  const bj = new Date(now.getTime() + 8 * 60 * 60 * 1000);
  return bj.toISOString().replace('T', ' ').substring(0, 19);
}

/**
 * 获取当前余额（强制每次读取文件，不缓存）
 */
function getCurrentBalance() {
  if (!fs.existsSync(BALANCE_FILE)) {
    return 0;
  }
  
  try {
    const content = fs.readFileSync(BALANCE_FILE, 'utf8');
    const data = JSON.parse(content);
    const balance = data.currentBalance || 0;
    console.log('💾 [强制读取] 当前余额:', balance);
    return balance;
  } catch (e) {
    console.error('读取余额失败:', e.message);
    return 0;
  }
}

/**
 * 更新 balance.json
 */
function updateBalance(dateStr, type, change, description) {
  let data = {
    currentBalance: 0,
    lastUpdated: dateStr,
    history: []
  };
  
  if (fs.existsSync(BALANCE_FILE)) {
    try {
      const content = fs.readFileSync(BALANCE_FILE, 'utf8');
      data = JSON.parse(content);
    } catch (e) {
      console.error('读取现有 JSON 失败，使用默认数据:', e.message);
    }
  }
  
  // 计算新余额
  const currentBalance = data.currentBalance || 0;
  const newBalance = currentBalance + change;
  
  // 映射操作类型到英文
  const typeMap = {
    '收入': 'income',
    '支出': 'expense',
    '初始化': 'init'
  };
  const enType = typeMap[type] || type;
  
  // 添加新记录到历史（添加到数组开头，保持最新在前）
  const newRecord = {
    date: dateStr,
    type: enType,
    change: change,
    balance: newBalance,
    description: description
  };
  
  data.history.unshift(newRecord);
  data.currentBalance = newBalance;
  data.lastUpdated = dateStr;
  
  fs.writeFileSync(BALANCE_FILE, JSON.stringify(data, null, 2));
  return newBalance;
}

/**
 * 写入输入日志
 */
function writeLog(inputType, rawInput, tasks, totalChange, newBalance) {
  try {
    const dateStr = getTodayStr();
    const timeStr = getBeijingTimeStr();
    
    const taskStr = tasks.map(t => `${t.task} (${t.points >= 0 ? '+' : ''}${t.points}分)`).join(', ');
    const logEntry = `[${timeStr}] ${inputType} | "${rawInput}"\n` +
      `  → 提取任务：${taskStr}\n` +
      `  → 积分变动：${totalChange >= 0 ? '+' : ''}${totalChange}分\n` +
      `  → 最终余额：${newBalance.toFixed(1)}分\n\n`;
    
    const logDir = path.dirname(LOG_FILE);
    if (!fs.existsSync(logDir)) {
      fs.mkdirSync(logDir, { recursive: true });
    }
    
    let logContent = '';
    if (fs.existsSync(LOG_FILE)) {
      logContent = fs.readFileSync(LOG_FILE, 'utf8');
    } else {
      logContent = '# 积分输入日志\n\n格式说明：\n[时间戳] 输入类型 | "原始输入内容"\n  → 提取任务：任务名 (+/-分数)\n  → 积分变动：+/-X 分\n  → 最终余额：X.X 分\n\n---\n\n';
    }
    
    const todayHeader = `## ${dateStr}`;
    if (!logContent.includes(todayHeader)) {
      logContent += `\n${todayHeader}\n\n`;
    }
    
    logContent += logEntry;
    fs.writeFileSync(LOG_FILE, logContent);
  } catch (e) {
    console.error('写入日志失败:', e.message);
  }
}

/**
 * 请求去重文件（防止同一消息被处理多次）
 * 格式：{"om_xxx": {"processed": true, "input": "xxx", "points": 1, "timestamp": "..."}}
 */
const REQUEST_LOG_FILE = path.join(POINTS_DIR, 'logs', 'request.json');

/**
 * 检查请求是否已处理（基于 message_id）
 */
function checkRequestProcessed(messageId) {
  if (!messageId) return { processed: false };
  
  if (!fs.existsSync(REQUEST_LOG_FILE)) {
    return { processed: false };
  }
  
  try {
    const content = fs.readFileSync(REQUEST_LOG_FILE, 'utf8');
    const data = JSON.parse(content);
    const record = data[messageId];
    
    if (!record) {
      return { processed: false };
    }
    
    // 返回已处理的信息（用于判断是否需要修正）
    return {
      processed: true,
      input: record.input,
      points: record.points,
      timestamp: record.timestamp
    };
  } catch (e) {
    console.error('检查请求重复失败:', e.message);
    return { processed: false };
  }
}

/**
 * 标记请求已处理
 */
function markRequestProcessed(messageId, input, points) {
  if (!messageId) return;
  
  try {
    const logDir = path.dirname(REQUEST_LOG_FILE);
    if (!fs.existsSync(logDir)) {
      fs.mkdirSync(logDir, { recursive: true });
    }
    
    let data = {};
    if (fs.existsSync(REQUEST_LOG_FILE)) {
      data = JSON.parse(fs.readFileSync(REQUEST_LOG_FILE, 'utf8'));
    }
    
    data[messageId] = {
      input: input,
      points: points,
      timestamp: new Date().toISOString()
    };
    
    fs.writeFileSync(REQUEST_LOG_FILE, JSON.stringify(data, null, 2));
  } catch (e) {
    console.error('标记请求失败:', e.message);
  }
}

/**
 * 检查输入是否重复
 */
function checkDuplicate(input) {
  if (!fs.existsSync(LOG_FILE)) {
    return false;
  }
  
  try {
    const logContent = fs.readFileSync(LOG_FILE, 'utf8');
    const today = getTodayStr();
    const todaySection = logContent.split(`## ${today}`)[1] || '';
    const normalizedInput = input.trim();
    
    if (todaySection.includes(`"${normalizedInput}"`) || todaySection.includes(`'${normalizedInput}'`)) {
      return true;
    }
    
    return false;
  } catch (e) {
    console.error('检查重复失败:', e.message);
    return false;
  }
}

/**
 * 记录积分收入
 * 
 * 注意：语义理解由 Agent 完成，这里只负责记账操作
 * @param {string} input - 用户输入（原始文本）
 * @param {Array} items - Agent 提取的任务列表（可选，如果不传则简单记录）
 * @param {string} dateStr - 日期字符串（可选，默认今天，格式：YYYY-MM-DD）
 * @param {string} messageId - 消息 ID（用于去重）
 */
function recordPoints(input, items = null, dateStr = null, messageId = null) {
  if (!dateStr) {
    dateStr = getTodayStr();
  }
  
  // 简单处理：如果没有 items，记录为"自主申报"
  const tasks = items || [{ task: '自主申报', points: 0, note: input }];
  
  // 计算总分
  const total = tasks.reduce((sum, t) => sum + (t.points || 0), 0);
  
  // 更新余额
  const newBalance = updateBalance(dateStr, '收入', total, input);
  
  // 写入日志
  writeLog('文字', input, tasks, total, newBalance);
  
  // 生成响应
  let message = `✅ **积分已记录**\n\n`;
  message += `📊 **任务**:\n`;
  for (const task of tasks) {
    const sign = task.points >= 0 ? '+' : '';
    message += `• ${task.task}: **${sign}${task.points}分**\n`;
  }
  message += `\n💰 **本次**: ${total >= 0 ? '+' : ''}${total}分\n`;
  message += `💰 **当前余额**: **${newBalance.toFixed(1)}分**\n`;
  if (dateStr !== getTodayStr()) {
    message += `\n📅 **日期**: ${dateStr}（补录）`;
  }
  message += `\n_已自动记入账本，随时可以查看_`;
  
  return {
    success: true,
    total,
    tasks,
    newBalance,
    message
  };
}

/**
 * 记录积分消费
 * 
 * 注意：现在由 Agent (LLM) 提取金额和用途，
 *       这里只负责记账操作（更新余额 + 写日志）
 * 
 * @param {number} amount - 消费金额（正数）
 * @param {string} description - 消费用途描述
 * @param {string} originalInput - 原始输入（用于日志）
 */
function recordExpense(amount, description, originalInput) {
  // 参数类型检查 - amount 必须是数字
  if (typeof amount !== 'number' || isNaN(amount)) {
    return {
      success: false,
      message: '😕 金额格式错误，请说清楚花了多少分'
    };
  }
  
  if (amount <= 0) {
    return {
      success: false,
      message: '😕 金额必须大于 0'
    };
  }
  
  const dateStr = getTodayStr();
  
  // 更新余额
  const newBalance = updateBalance(dateStr, '支出', -amount, description);
  
  // 写入日志
  const tasks = [{ task: description, points: -amount }];
  writeLog('文字', originalInput, tasks, -amount, newBalance);
  
  // 生成响应
  let message = `✅ **消费已记录**\n\n`;
  message += `💸 **金额**: ${amount}分\n`;
  message += `📝 **用途**: ${description}\n`;
  message += `💰 **当前余额**: **${newBalance.toFixed(1)}分**\n`;
  message += `\n_已自动记入账本_`;
  
  return {
    success: true,
    amount,
    description,
    newBalance,
    message
  };
}

/**
 * 获取余额信息
 */
function getBalanceInfo() {
  const balance = getCurrentBalance();
  return {
    exists: true,
    balance,
    message: `当前余额：**${balance.toFixed(1)}分**`
  };
}

module.exports = {
  recordPoints,
  recordExpense,
  getBalanceInfo,
  getCurrentBalance,
  checkDuplicate,
  checkRequestProcessed,
  markRequestProcessed,
  updateBalance,
  writeLog
};
