/**
 * 每日积分日报生成器
 * 生成独立的日报文件，并准备发送到飞书
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE = '/home/wang/.openclaw/agents/kids-study/workspace';
const POINTS_DIR = path.join(WORKSPACE, 'kids-points');
const DAILY_DIR = path.join(POINTS_DIR, 'daily');

/**
 * 获取日期字符串（本地时间）
 */
function getLocalDateStr(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

/**
 * 获取昨天日期字符串
 */
function getYesterdayStr() {
  const yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - 1);
  return getLocalDateStr(yesterday);
}

/**
 * 获取今天日期字符串
 */
function getTodayStr() {
  return getLocalDateStr(new Date());
}

/**
 * 获取今天日期字符串
 */
function getTodayStr() {
  const now = new Date();
  return now.toISOString().split('T')[0];
}

/**
 * 获取当前月份字符串
 */
function getMonthStr() {
  // 使用 Asia/Shanghai timezone
  const now = new Date(new Date().toLocaleString('en-US', {timeZone: 'Asia/Shanghai'}));
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;
}

/**
 * 读取月度账本
 */
function loadMonthlyLog(monthStr) {
  const filePath = path.join(POINTS_DIR, 'monthly', `${monthStr}.md`);
  if (fs.existsSync(filePath)) {
    return fs.readFileSync(filePath, 'utf8');
  }
  return null;
}

/**
 * 从 balance.md 解析指定日期的积分明细
 */
function parseDayDetailsFromBalance(balanceContent, date) {
  const lines = balanceContent.split('\n');
  const income = [];
  const expense = [];
  let total = 0;
  
  // 查找日期对应的行
  for (const line of lines) {
    if (line.includes(date) && (line.includes('收入') || line.includes('支出'))) {
      // 简化解析：| 2026-03-13 | 收入 | +1 | 107.3 | 早上自主起床 |
      const parts = line.split('|').map(p => p.trim()).filter(p => p);
      if (parts.length >= 5) {
        const [, type, pointsStr, , description] = parts;
        const points = parseFloat(pointsStr.replace('+', ''));
        
        const item = {
          task: description.replace(/。*$/, '').trim(),  // 移除句号后的内容
          points: points,
          note: ''
        };
        
        if (type === '收入') {
          income.push(item);
          total += points;
        } else if (type === '支出') {
          expense.push(item);
          // 支出已经在 points 中是正数，不需要再减
          // total 计算由调用方处理
        }
      }
    }
  }
  
  return { income, expense, total };
}

/**
 * 解析昨日积分明细（从月度账本，向后兼容）
 */
function parseYesterdayDetails(content, yesterday) {
  const yesterdayHeader = `### ${yesterday}`;
  const yesterdayIndex = content.indexOf(yesterdayHeader);
  
  if (yesterdayIndex === -1) {
    return {
      income: [],
      expense: [],
      total: 0
    };
  }
  
  const nextDayIndex = content.indexOf('### ', yesterdayIndex + 1);
  const yesterdaySection = content.slice(
    yesterdayIndex, 
    nextDayIndex === -1 ? content.length : nextDayIndex
  );
  
  // 解析收入
  const incomeMatch = yesterdaySection.match(/\*\*收入\*\*:[\s\S]*?(?=\*\*支出\*\*|$)/);
  const income = [];
  if (incomeMatch) {
    const incomeLines = incomeMatch[0].split('\n').filter(line => line.trim().startsWith('-'));
    incomeLines.forEach(line => {
      // 支持中文和英文冒号，允许空格
      const match = line.match(/- (.+?)[:：]\s*(\d+(?:\.\d+)?)\s*分\s*\((.+?)\)/);
      if (match) {
        income.push({
          task: match[1],
          points: parseFloat(match[2]),
          note: match[3]
        });
      }
    });
  }
  
  // 解析支出
  const expenseMatch = yesterdaySection.match(/\*\*支出\*\*:[\s\S]*?(?=\*\*小计\*\*|$)/);
  const expense = [];
  if (expenseMatch && !expenseMatch[0].includes('_暂无记录_')) {
    const expenseLines = expenseMatch[0].split('\n').filter(line => line.trim().startsWith('-'));
    expenseLines.forEach(line => {
      // 支持中文和英文冒号，允许空格
      const match = line.match(/- (.+?)[:：]\s*(\d+(?:\.\d+)?)\s*分/);
      if (match) {
        expense.push({
          task: match[1],
          points: parseFloat(match[2])
        });
      }
    });
  }
  
  // 解析小计
  const totalMatch = yesterdaySection.match(/\*\*小计\*\*: ([+-]?\d+(?:\.\d+)?) 分/);
  const total = totalMatch ? parseFloat(totalMatch[1]) : 0;
  
  return { income, expense, total };
}

/**
 * 从 balance.md 读取当前余额（优先方案）
 */
function extractBalanceFromBalanceMd() {
  const balanceFile = path.join(POINTS_DIR, 'balance.md');
  
  if (!fs.existsSync(balanceFile)) {
    return null;
  }
  
  try {
    const content = fs.readFileSync(balanceFile, 'utf8');
    // 匹配：**104.3 分**
    const balanceMatch = content.match(/## 当前余额[\s\S]*?\*\*([\d.]+) 分\*\*/);
    
    if (balanceMatch && balanceMatch[1]) {
      return parseFloat(balanceMatch[1]);
    }
  } catch (e) {
    console.warn(`读取 balance.md 失败：${e.message}`);
  }
  
  return null;
}

/**
 * 提取当前余额（优先 balance.md，备用月度日志）
 */
function extractBalance(content) {
  // 优先从 balance.md 读取
  const balanceFromBalanceMd = extractBalanceFromBalanceMd();
  if (balanceFromBalanceMd !== null) {
    console.log(`✅ 从 balance.md 读取余额：${balanceFromBalanceMd} 分`);
    return balanceFromBalanceMd;
  }
  
  // 备用：从月度日志读取
  const balanceMatch = content.match(/当前结余 \| ([\d.]+) 分/);
  const balance = balanceMatch ? parseFloat(balanceMatch[1]) : 0;
  console.log(`⚠️  从月度日志读取余额：${balance} 分`);
  return balance;
}

/**
 * 生成日报内容
 */
function generateDailyReport(yesterday, details, balance) {
  const today = getTodayStr();
  
  let report = `# 积分日报 - ${yesterday}\n\n`;
  report += `> 生成时间：${today}\n\n`;
  report += `---\n\n`;
  
  // 今日概览
  report += `## 📊 今日概览\n\n`;
  report += `| 项目 | 数值 |\n`;
  report += `|------|------|\n`;
  report += `| 总收入 | ${details.income.reduce((sum, item) => sum + item.points, 0)} 分 |\n`;
  report += `| 总支出 | ${details.expense.reduce((sum, item) => sum + item.points, 0)} 分 |\n`;
  report += `| 净收益 | ${details.total >= 0 ? '+' : ''}${details.total} 分 |\n`;
  report += `| 当前余额 | ${balance} 分 |\n\n`;
  
  // 收入明细
  report += `## 💰 收入明细\n\n`;
  if (details.income.length === 0) {
    report += `_暂无收入记录_\n\n`;
  } else {
    report += `| 任务 | 分数 | 说明 |\n`;
    report += `|------|------|------|\n`;
    details.income.forEach(item => {
      report += `| ${item.task} | +${item.points} 分 | ${item.note} |\n`;
    });
    report += `\n`;
  }
  
  // 支出明细
  report += `## 💸 支出明细\n\n`;
  if (details.expense.length === 0) {
    report += `_暂无支出记录_\n\n`;
  } else {
    report += `| 任务 | 分数 |\n`;
    report += `|------|------|\n`;
    details.expense.forEach(item => {
      report += `| ${item.task} | -${item.points} 分 |\n`;
    });
    report += `\n`;
  }
  
  // 温馨提示
  report += `## 💡 温馨提示\n\n`;
  if (details.total > 0) {
    report += `🎉 昨天表现不错，继续加油！\n\n`;
  } else if (details.total < 0) {
    report += `⚠️ 昨天有些小失误，今天继续努力哦！\n\n`;
  } else {
    report += `😐 昨天没有积分变动，今天可以争取更多积分哦！\n\n`;
  }
  report += `_当前余额：${balance} 分，距离 400 分上限还有 ${400 - balance} 分_\n`;
  
  return report;
}

/**
 * 生成飞书消息文本
 */
function generateFeishuMessage(yesterday, details, balance) {
  const today = getTodayStr();
  
  let message = `📅 **${today} 积分日报**\n\n`;
  message += `━━━━━━━━━━━━━━━━━━\n\n`;
  message += `📊 **${yesterday} 积分情况**:\n\n`;
  
  // 收入
  if (details.income.length > 0) {
    message += `**💰 收入**:\n`;
    details.income.forEach(item => {
      message += `• ${item.task}: **+${item.points}分** (${item.note})\n`;
    });
    message += `\n`;
  }
  
  // 支出
  if (details.expense.length > 0) {
    message += `**💸 支出**:\n`;
    details.expense.forEach(item => {
      message += `• ${item.task}: **-${item.points}分**\n`;
    });
    message += `\n`;
  }
  
  if (details.income.length === 0 && details.expense.length === 0) {
    message += `_暂无积分记录_\n\n`;
  }
  
  // 汇总
  message += `━━━━━━━━━━━━━━━━━━\n\n`;
  message += `**📈 净收益**: ${details.total >= 0 ? '+' : ''}${details.total} 分\n`;
  message += `**💰 当前余额**: ${balance} 分\n`;
  
  // 月度消费额度（v1.3 新功能）
  const monthStr = getMonthStr();
  const monthlyLog = loadMonthlyLog(monthStr);
  let spendingInfo = '';
  
  if (monthlyLog) {
    // 读取本月总支出
    const expenseMatch = monthlyLog.match(/总支出 \| (\d+) 分/);
    const totalExpense = expenseMatch ? parseInt(expenseMatch[1]) : 0;
    const spendingLimit = 400;
    const remainingLimit = spendingLimit - totalExpense;
    
    // 检查是否有欠费
    const overdraftMatch = monthlyLog.match(/欠费结转.*?(\d+) 分/);
    const overdraft = overdraftMatch ? parseInt(overdraftMatch[1]) : 0;
    
    if (overdraft > 0) {
      message += `**📊 本月可用额度**: ${remainingLimit} 分（已扣减上月欠费 ${overdraft} 分）\n`;
    } else {
      message += `**📊 本月剩余消费额度**: ${remainingLimit} 分\n`;
    }
  } else {
    message += `**📏 距离上限**: ${400 - balance} 分\n`;
  }
  
  message += `\n`;
  
  // 温馨提示
  if (details.total > 0) {
    message += `🎉 昨天表现不错，继续加油！\n\n`;
  } else if (details.total < 0) {
    message += `⚠️ 昨天有些小失误，今天继续努力哦！\n\n`;
  } else {
    message += `💪 今天争取更多积分吧！\n\n`;
  }
  
  message += `_详细报告已保存到 \`kids-points/daily/${yesterday}.md\`_`;
  
  return message;
}

/**
 * 生成 TTS 语音文案（纯文本，适合朗读）
 * 根据日期动态调整称呼（昨天/今天）
 */
function generateTTSContent(reportDate, details, balance) {
  const today = getTodayStr();
  const incomeTotal = details.income.reduce((sum, item) => sum + item.points, 0);
  const expenseTotal = details.expense.reduce((sum, item) => sum + item.points, 0);
  
  // 判断是昨天还是今天
  const isToday = reportDate === today;
  const timeRef = isToday ? '今天' : '昨天';
  
  let tts = `${reportDate}积分日报。`;
  
  // 收入汇总
  if (incomeTotal > 0) {
    tts += `${timeRef}收入${incomeTotal}分。`;
    // 简要说明主要收入项（最多 3 项）
    const topItems = details.income.slice(0, 3);
    topItems.forEach(item => {
      tts += `${item.task}${item.points}分，`;
    });
  } else {
    tts += `${timeRef}没有收入记录。`;
  }
  
  // 支出汇总
  if (expenseTotal > 0) {
    tts += `支出${expenseTotal}分。`;
  }
  
  // 净收益
  if (details.total > 0) {
    tts += `净赚${details.total}分。`;
  } else if (details.total < 0) {
    tts += `净支出${Math.abs(details.total)}分。`;
  }
  
  // 当前余额
  tts += `当前余额${balance}分。`;
  
  // 距离上限
  const remaining = 400 - balance;
  tts += `距离${400}分上限还有${remaining}分。`;
  
  // 鼓励短语
  if (details.total > 0) {
    tts += `${timeRef}表现不错，继续加油！`;
  } else if (details.total < 0) {
    tts += `${timeRef}有些小失误，明天继续努力哦！`;
  } else {
    tts += `明天争取更多积分吧！`;
  }
  
  return tts;
}

/**
 * 主函数
 */
function main() {
  const args = process.argv.slice(2);
  const today = getTodayStr();
  const monthStr = getMonthStr();
  
  // 支持指定日期：node generate-daily-report.js [yesterday|today|YYYY-MM-DD]
  let targetDate;
  if (args[0] === 'yesterday' || !args[0]) {
    // 默认生成昨天的日报
    targetDate = getYesterdayStr();
  } else if (args[0] === 'today') {
    // 生成今天的日报（用于白天查看）
    targetDate = today;
  } else if (/^\d{4}-\d{2}-\d{2}$/.test(args[0])) {
    // 指定日期
    targetDate = args[0];
  } else {
    console.error('❌ 用法：node generate-daily-report.js [yesterday|today|YYYY-MM-DD]');
    process.exit(1);
  }
  
  // 确保日报目录存在
  if (!fs.existsSync(DAILY_DIR)) {
    fs.mkdirSync(DAILY_DIR, { recursive: true });
  }
  
  // 优先从 balance.md 读取数据（实时准确）
  const balanceFile = path.join(POINTS_DIR, 'balance.md');
  let balanceContent = '';
  if (fs.existsSync(balanceFile)) {
    balanceContent = fs.readFileSync(balanceFile, 'utf8');
    console.log('✅ 从 balance.md 读取数据');
  }
  
  // 读取月度账本（备用）
  const monthlyContent = loadMonthlyLog(monthStr);
  
  console.log(`📅 生成日报：${targetDate}`);
  
  // 解析目标日期数据（优先从 balance.md）
  let details;
  if (balanceContent) {
    details = parseDayDetailsFromBalance(balanceContent, targetDate);
  } else if (monthlyContent) {
    details = parseYesterdayDetails(monthlyContent, targetDate);
  } else {
    details = { income: [], expense: [], total: 0 };
  }
  
  // 获取余额（优先从 balance.md）
  const balance = balanceContent ? extractBalanceFromBalanceMd() : extractBalance(monthlyContent || '');
  
  // 生成日报文件（如果已存在则覆盖更新）
  const reportContent = generateDailyReport(targetDate, details, balance);
  const reportFile = path.join(DAILY_DIR, `${targetDate}.md`);
  fs.writeFileSync(reportFile, reportContent);
  
  // 生成飞书消息
  const feishuMessage = generateFeishuMessage(targetDate, details, balance);
  
  // 生成 TTS 语音文案
  const ttsContent = generateTTSContent(targetDate, details, balance);
  
  // 输出结果
  console.log('✅ 日报生成成功');
  console.log(`📁 文件：${reportFile}`);
  console.log('');
  console.log('📤 飞书消息内容:');
  console.log('---');
  console.log(feishuMessage);
  console.log('---');
  console.log('');
  console.log('🔊 TTS 语音文案:');
  console.log('---');
  console.log(ttsContent);
  console.log('---');
  
  // 输出 JSON 格式供脚本调用
  const output = {
    success: true,
    date: targetDate,
    reportFile: reportFile,
    feishuMessage: feishuMessage,
    ttsContent: ttsContent,
    summary: {
      income: details.income.reduce((sum, item) => sum + item.points, 0),
      expense: details.expense.reduce((sum, item) => sum + item.points, 0),
      total: details.total,
      balance: balance
    }
  };
  
  console.log('');
  console.log('JSON_OUTPUT_START');
  console.log(JSON.stringify(output, null, 2));
  console.log('JSON_OUTPUT_END');
}

// 运行
main();
