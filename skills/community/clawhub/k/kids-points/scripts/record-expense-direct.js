/**
 * 直接记录积分支出 - 用于子代理调用
 * 用法：node record-expense-direct.js "昨晚晚睡" 4 2026-04-17
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE = '/home/wang/.openclaw/agents/kids-study/workspace';
const POINTS_DIR = path.join(WORKSPACE, 'kids-points');
const BALANCE_FILE = path.join(POINTS_DIR, 'balance.json');
const LOG_FILE = path.join(POINTS_DIR, 'logs', 'input.log');

function getTodayStr() {
  const now = new Date();
  return now.toISOString().split('T')[0];
}

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
  
  const currentBalance = data.currentBalance || 0;
  const newBalance = currentBalance + change;
  
  const typeMap = {
    '收入': 'income',
    '支出': 'expense',
    '初始化': 'init'
  };
  const enType = typeMap[type] || type;
  
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

function writeLog(inputType, rawInput, tasks, totalChange, newBalance, dateStr) {
  try {
    const timeStr = new Date().toISOString().replace('T', ' ').substring(0, 19);
    
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

// 主程序
const args = process.argv.slice(2);
if (args.length < 3) {
  console.log('用法：node record-expense-direct.js "描述" 金额 日期');
  console.log('例如：node record-expense-direct.js "昨晚晚睡" 4 2026-04-17');
  process.exit(1);
}

const [description, amountStr, dateStr] = args;
const amount = parseInt(amountStr);

if (isNaN(amount) || amount <= 0) {
  console.log('❌ 金额必须是正整数');
  process.exit(1);
}

// 检查是否已存在相同记录
if (fs.existsSync(LOG_FILE)) {
  const logContent = fs.readFileSync(LOG_FILE, 'utf8');
  if (logContent.includes(`"${description}"`) && logContent.includes(`## ${dateStr}`)) {
    console.log('⚠️ 警告：这条记录可能已存在');
    console.log(`  描述：${description}`);
    console.log(`  日期：${dateStr}`);
    console.log('  请确认是否需要重复记录');
    process.exit(0);
  }
}

// 记录支出
const newBalance = updateBalance(dateStr, '支出', -amount, description);
writeLog('文字', description, [{ task: description, points: -amount }], -amount, newBalance, dateStr);

console.log('✅ 积分支出已记录');
console.log(`  📅 日期：${dateStr}`);
console.log(`  💸 金额：-${amount}分`);
console.log(`  📝 原因：${description}`);
console.log(`  💰 当前余额：${newBalance.toFixed(1)}分`);
