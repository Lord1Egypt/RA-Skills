/**
 * 报表生成器
 * 
 * 职责：
 * - 生成积分统计报表（供自动日报和手动查询共用）
 * - 只读操作，绝不修改 balance.json
 * - 返回结构化消息 + TTS 纯文本
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE = process.env.WORKSPACE || '/home/wang/.openclaw/agents/kids-study/workspace';
const POINTS_DIR = process.env.POINTS_DIR || path.join(WORKSPACE, 'kids-points');
const BALANCE_FILE = path.join(POINTS_DIR, 'balance.json');

/**
 * 获取指定日期的日期字符串（YYYY-MM-DD）
 * @param {Date} date - 日期对象
 * @returns {string} YYYY-MM-DD 格式
 */
function formatDate(date) {
  return date.toISOString().split('T')[0];
}

/**
 * 获取"昨天"的日期（基于 UTC，对应北京时间昨天）
 * @returns {string} YYYY-MM-DD 格式
 */
function getYesterdayStr() {
  const now = new Date();
  // UTC 时间加 8 小时得到北京时间
  const beijingTime = new Date(now.getTime() + 8 * 60 * 60 * 1000);
  // 减 1 天得到昨天
  beijingTime.setDate(beijingTime.getDate() - 1);
  return formatDate(beijingTime);
}

/**
 * 读取 balance.json（只读）
 * @returns {Object|null} 数据对象或 null
 */
function readBalanceData() {
  if (!fs.existsSync(BALANCE_FILE)) {
    return null;
  }
  
  try {
    const content = fs.readFileSync(BALANCE_FILE, 'utf8');
    return JSON.parse(content);
  } catch (e) {
    console.error('读取 balance.json 失败:', e.message);
    return null;
  }
}

/**
 * 筛选指定日期的记录
 * @param {Array} history - 历史记录数组
 * @param {string} dateStr - 日期字符串 YYYY-MM-DD
 * @returns {Object} { incomes: [], expenses: [] }
 */
function filterRecordsByDate(history, dateStr) {
  const incomes = [];
  const expenses = [];
  
  for (const record of history || []) {
    if (record.date !== dateStr) continue;
    
    if (record.type === 'income') {
      incomes.push(record);
    } else if (record.type === 'expense') {
      expenses.push(record);
    }
  }
  
  return { incomes, expenses };
}

/**
 * 生成昨日日报报表
 * @returns {Object} { message: string, speechText: string, data: Object }
 */
function generateDailyReport() {
  const yesterdayStr = getYesterdayStr();
  
  // 读取数据
  const data = readBalanceData();
  if (!data) {
    return {
      message: '⚠️ **日报生成失败**\n\n未找到积分数据，请先记录一些积分。',
      speechText: '日报生成失败，未找到积分数据，请先记录一些积分。',
      data: null
    };
  }
  
  const history = data.history || [];
  const currentBalance = data.currentBalance || 0;
  
  // 筛选昨日记录
  const { incomes, expenses } = filterRecordsByDate(history, yesterdayStr);
  
  // 计算统计
  const totalIncome = incomes.reduce((sum, r) => sum + (r.change || 0), 0);
  const totalExpense = expenses.reduce((sum, r) => sum + Math.abs(r.change || 0), 0);
  const netChange = totalIncome - totalExpense;
  
  // 生成 Markdown 消息
  let message = `📊 **昨日积分日报**（${yesterdayStr}）\n\n`;
  
  // 收入部分
  message += `## 💰 收入：+${totalIncome.toFixed(1)} 分（${incomes.length} 笔）\n\n`;
  if (incomes.length === 0) {
    message += '昨日无收入记录\n\n';
  } else {
    for (const record of incomes) {
      const desc = record.description || '未知';
      const change = record.change || 0;
      message += `• ${desc}：+${change.toFixed(1)} 分\n`;
    }
    message += '\n';
  }
  
  // 支出部分
  message += `## 💸 支出：-${totalExpense.toFixed(1)} 分（${expenses.length} 笔）\n\n`;
  if (expenses.length === 0) {
    message += '昨日无支出记录\n\n';
  } else {
    for (const record of expenses) {
      const desc = record.description || '未知';
      const change = Math.abs(record.change || 0);
      message += `• ${desc}：-${change.toFixed(1)} 分\n`;
    }
    message += '\n';
  }
  
  // 汇总
  message += `## 📈 汇总\n\n`;
  message += `昨日净变动：${netChange >= 0 ? '+' : ''}${netChange.toFixed(1)} 分\n`;
  message += `当前余额：${currentBalance.toFixed(1)} 分\n`;
  
  // 添加评价
  if (netChange > 0) {
    message += '\n🌟 昨日表现不错，继续保持！';
  } else if (netChange < 0) {
    message += '\n💡 昨日支出较多，注意控制哦~';
  } else {
    message += '\n📋 昨日收支平衡，今天加油！';
  }
  
  // 生成 TTS 纯文本
  let speechText = `昨日积分日报。日期 ${yesterdayStr}。`;
  speechText += `总收入 ${totalIncome.toFixed(1)} 分，共 ${incomes.length} 笔。`;
  speechText += `总支出 ${totalExpense.toFixed(1)} 分，共 ${expenses.length} 笔。`;
  speechText += `净变动 ${netChange >= 0 ? '正' : '负'}${Math.abs(netChange).toFixed(1)} 分。`;
  speechText += `当前余额 ${currentBalance.toFixed(1)} 分。`;
  
  if (netChange > 0) {
    speechText += '昨日表现不错，继续保持。';
  } else if (netChange < 0) {
    speechText += '昨日支出较多，注意控制哦。';
  } else {
    speechText += '昨日收支平衡，今天加油。';
  }
  
  return {
    message,
    speechText,
    data: {
      date: yesterdayStr,
      incomes,
      expenses,
      totalIncome,
      totalExpense,
      netChange,
      currentBalance
    }
  };
}

module.exports = {
  generateDailyReport,
  getYesterdayStr,
  readBalanceData
};
