/**
 * 积分管理主处理器
 * 处理用户输入，更新账本，生成响应
 * 支持多语言：中文、英语、日语
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const { parsePointsInput, calculatePoints } = require('./parse-input');

// 多语言配置
const I18N = {
  zh: {
    welcome: '🎉 欢迎使用 kids-points 儿童积分语音助手！',
    pointsRecorded: '✅ 今日积分已记录!',
    expenseRecorded: '✅ 消费已记录!',
    noTasks: '😕 没有识别到任何任务，请再说详细一点哦~',
    checkConditions: '🤔 任务都识别到了，但是没有获得积分呢~\n\n请检查是否满足积分条件哦',
    voiceHint: '\n\n💡 **提示：配置 API Key 后可解锁语音功能**\n   • 🎤 语音记账 - 发送音频自动识别\n   • 🔊 语音播报 - 积分变动自动鼓励（童声）\n   • 📻 日报朗读 - 每天自动播报积分\n\n👉 **快速配置**（目前基本免费）：\n   1. 访问 https://senseaudio.cn\n   2. 免费注册账号（送免费额度）\n   3. 创建应用获取 API Key\n   4. 添加到 ~/.openclaw/openclaw.json\n\n📋 详细文档：查看 DEPENDENCIES.md'
  },
  en: {
    welcome: '🎉 Welcome to kids-points Voice Assistant!',
    pointsRecorded: '✅ Points recorded for today!',
    expenseRecorded: '✅ Expense recorded!',
    noTasks: '😕 No tasks recognized, please be more specific~',
    checkConditions: '🤔 Tasks recognized but no points earned~\n\nPlease check if conditions are met',
    voiceHint: '\n\n💡 **Hint: Configure API Key to unlock voice features**\n   • 🎤 Voice Recording - Send audio to auto-record\n   • 🔊 Voice Broadcasting - Auto encouragement for points\n   • 📻 Daily Report - Auto broadcast at 7 AM\n\n👉 **Quick Setup** (Currently Free):\n   1. Visit https://senseaudio.cn\n   2. Register free account (free credits)\n   3. Create app to get API Key\n   4. Add to ~/.openclaw/openclaw.json\n\n📋 Docs: Check DEPENDENCIES.md'
  },
  ja: {
    welcome: '🎉 kids-points 音声アシスタントへようこそ！',
    pointsRecorded: '✅ 今日のポイントが記録されました！',
    expenseRecorded: '✅ 支出が記録されました！',
    noTasks: '😕 タスクが認識されませんでした。詳しく教えてください~',
    checkConditions: '🤔 タスクは認識されましたが、ポイントが獲得できませんでした~\n\n条件を満たしているか確認してください',
    voiceHint: '\n\n💡 **ヒント：API キーを設定して音声機能をアンロック**\n   • 🎤 音声記録 - 音声で自動記録\n   • 🔊 音声放送 - ポイント獲得時に自動音声\n   • 📻 日報 - 毎朝 7 時に自動放送\n\n👉 **クイック設定**（現在無料）：\n   1. https://senseaudio.cn にアクセス\n   2. 無料アカウント登録（無料クレジット付与）\n   3. アプリ作成して API キー取得\n   4. ~/.openclaw/openclaw.json に追加\n\n📋 ドキュメント：DEPENDENCIES.md を確認'
  }
};

const WORKSPACE = process.env.WORKSPACE || '/home/wang/.openclaw/agents/kids-study/workspace';
const POINTS_DIR = process.env.POINTS_DIR || path.join(WORKSPACE, 'kids-points');
const RULES_FILE = path.join(__dirname, '..', 'config', 'rules.json');
// 使用 Kid Point Voice Component
const TTS_SCRIPT = path.join(WORKSPACE, 'skills/senseaudio-voice/scripts/tts.py');

/**
 * 获取今日日期字符串
 */
function getTodayStr() {
  const now = new Date();
  return now.toISOString().split('T')[0];
}

/**
 * 检测消息语言
 * @param {string} message - 用户消息
 * @returns {string} 语言代码 (zh/en/ja)
 */
function detectLanguage(message) {
  if (!message) return 'zh';
  
  // 检测日语（平假名、片假名）
  if (/[\u3040-\u309f\u30a0-\u30ff]/.test(message)) {
    return 'ja';
  }
  
  // 检测英语（简单检测）
  if (/[a-zA-Z]{3,}/.test(message) && !/[\u4e00-\u9fff]/.test(message)) {
    return 'en';
  }
  
  // 默认中文
  return 'zh';
}

/**
 * 获取多语言文本
 * @param {string} key - 文本键
 * @param {string} lang - 语言代码
 * @returns {string} 翻译后的文本
 */
function t(key, lang = 'zh') {
  return I18N[lang]?.[key] || I18N.zh[key] || key;
}

/**
 * 获取当前月份字符串
 */
function getMonthStr() {
  const now = new Date();
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;
}

/**
 * 获取当前周信息
 */
function getWeekInfo() {
  const now = new Date();
  const dayOfWeek = now.getDay(); // 0=周日，1=周一...
  const diff = now.getDate() - dayOfWeek + (dayOfWeek === 0 ? -6 : 1); // 周一为起点
  const monday = new Date(now);
  monday.setDate(diff);
  
  const weekNum = getWeekNumber(now);
  return {
    weekNum,
    startDate: monday.toISOString().split('T')[0],
    endDate: new Date(monday.getTime() + 6 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
  };
}

/**
 * 获取周数
 */
function getWeekNumber(date) {
  const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
  const dayNum = d.getUTCDay() || 7;
  d.setUTCDate(d.getUTCDate() + 4 - dayNum);
  const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
  return Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
}

/**
 * 读取规则配置
 */
function loadRules() {
  try {
    const data = fs.readFileSync(RULES_FILE, 'utf8');
    return JSON.parse(data);
  } catch (e) {
    return { rules: { tasks: {}, limits: { monthlyMax: 400 } } };
  }
}

/**
 * 读取月度账本
 */
function loadMonthlyLog(monthStr) {
  const filePath = path.join(POINTS_DIR, 'monthly', `${monthStr}.md`);
  if (fs.existsSync(filePath)) {
    return fs.readFileSync(filePath, 'utf8');
  }
  return createMonthlyLog(monthStr);
}

/**
 * 创建月度账本模板
 */
function createMonthlyLog(monthStr) {
  const [year, month] = monthStr.split('-');
  const monthName = `${year}年${parseInt(month)}月`;
  
  return `# 积分账本 - ${monthName}

## 本月汇总

| 项目 | 数值 |
|------|------|
| 总收入 | 0 分 |
| 总支出 | 0 分 |
| 结余 | 0 分 |
| 距离上限 (400 分) | 400 分 |

---

## 每日明细

_暂无记录_

---

## 每周汇总

_暂无记录_

---

_最后更新：${getTodayStr()}_
`;
}

/**
 * 记录积分收入
 */
function recordIncome(dateStr, details, total) {
  const monthStr = getMonthStr();
  let content = loadMonthlyLog(monthStr);
  
  // 检查是否已有今日记录
  const todayHeader = `### ${dateStr}`;
  const todayIndex = content.indexOf(todayHeader);
  
  const incomeLine = `- ${details.map(d => `${d.task}: ${d.points}分 (${d.note})`).join(', ')}`;
  const incomeSection = `**收入**:\n${incomeLine}`;
  
  if (todayIndex === -1) {
    // 添加新的一天记录
    const newEntry = `
${todayHeader}

${incomeSection}

**支出**:
- _暂无记录_

**小计**: +${total}分

---
`;
    // 插入到"每日明细"标题后面
    const dailyHeader = '## 每日明细';
    const dailyIndex = content.indexOf(dailyHeader);
    if (dailyIndex !== -1) {
      // 找到标题后的第一个空行
      const afterHeader = content.indexOf('\n\n', dailyIndex + dailyHeader.length);
      content = content.slice(0, afterHeader + 2) + newEntry + content.slice(afterHeader + 2);
    }
  } else {
    // 更新已有记录
    const nextDayIndex = content.indexOf('### ', todayIndex + 1);
    const sectionEnd = nextDayIndex === -1 ? content.length : nextDayIndex;
    const todaySection = content.slice(todayIndex, sectionEnd);
    
    // 更新收入部分
    const oldIncomeSection = todaySection.match(/\*\*收入\*\*:[\s\S]*?\n- [^\n]+/);
    if (oldIncomeSection) {
      const newIncomeSection = `**收入**:\n${incomeLine}`;
      const oldFull = oldIncomeSection[0];
      content = content.replace(oldFull, newIncomeSection);
    }
    
    // 更新小计
    const currentTotal = todaySection.match(/\*\*小计\*\*: ([+-]?\d+)分/);
    if (currentTotal) {
      const newTotal = parseInt(currentTotal[1]) + total;
      content = content.replace(`**小计**: ${currentTotal[1]}分`, `**小计**: +${newTotal}分`);
    }
  }
  
  // 更新本月汇总
  const totalMatch = content.match(/总收入 \| (\d+) 分/);
  if (totalMatch) {
    const newTotal = parseInt(totalMatch[1]) + total;
    content = content.replace(/总收入 \| \d+ 分/, `总收入 | ${newTotal} 分`);
    
    // 更新结余
    const expenseMatch = content.match(/总支出 \| (\d+) 分/);
    if (expenseMatch) {
      const expense = parseInt(expenseMatch[1]);
      const balance = newTotal - expense;
      content = content.replace(/结余 \| -?\d+ 分/, `结余 | ${balance} 分`);
    }
    
    // 更新距离上限
    const remaining = 400 - newTotal;
    content = content.replace(/距离上限 \(400 分\) \| \d+ 分/, `距离上限 (400 分) | ${Math.max(0, remaining)} 分`);
  }
  
  // 更新最后更新时间
  content = content.replace(/_最后更新：[\d-]+_/, `_最后更新：${dateStr}_`);
  
  // 保存
  const filePath = path.join(POINTS_DIR, 'monthly', `${monthStr}.md`);
  fs.writeFileSync(filePath, content);
  
  return content;
}

/**
 * 记录积分消费
 */
function recordExpense(dateStr, amount, description) {
  const monthStr = getMonthStr();
  let content = loadMonthlyLog(monthStr);
  
  const todayHeader = `### ${dateStr}`;
  const todayIndex = content.indexOf(todayHeader);
  
  const expenseLine = `- ${description}: ${amount}分`;
  
  if (todayIndex !== -1) {
    // 更新已有记录
    const expenseSection = `**支出**:\n${expenseLine}`;
    const todaySection = content.slice(todayIndex);
    const expenseMatch = todaySection.match(/\*\*支出\*\*:[\s\S]*?(?=\*\*小计\*\*|$)/);
    
    if (expenseMatch && expenseMatch[0].includes('_暂无记录_')) {
      content = content.replace('**支出**:\n- _暂无记录_', expenseSection);
    } else {
      // 追加支出
      const insertPos = todayIndex + todaySection.indexOf(expenseLine || '**支出**:') + expenseLine.length;
      content = content.replace('**支出**:\n- _暂无记录_', `**支出**:\n${expenseLine}`);
    }
    
    // 更新小计
    const currentTotal = todaySection.match(/\*\*小计\*\*: ([+-]?\d+)分/);
    if (currentTotal) {
      const newTotal = parseInt(currentTotal[1]) - amount;
      content = content.replace(`**小计**: ${currentTotal[1]}分`, `**小计**: ${newTotal >= 0 ? '+' : ''}${newTotal}分`);
    }
  }
  
  // 更新本月汇总
  const expenseMatch = content.match(/总支出 \| (\d+) 分/);
  if (expenseMatch) {
    const newTotal = parseInt(expenseMatch[1]) + amount;
    content = content.replace(/总支出 \| \d+ 分/, `总支出 | ${newTotal} 分`);
    
    // 更新结余
    const incomeMatch = content.match(/总收入 \| (\d+) 分/);
    if (incomeMatch) {
      const income = parseInt(incomeMatch[1]);
      const balance = income - newTotal;
      content = content.replace(/结余 \| \d+ 分/, `结余 | ${balance} 分`);
      
      // 更新距离上限
      const remaining = 400 - income;
      content = content.replace(/距离上限 \(400 分\) \| \d+ 分/, `距离上限 (400 分) | ${Math.max(0, remaining)} 分`);
    }
  }
  
  // 保存
  const filePath = path.join(POINTS_DIR, 'monthly', `${monthStr}.md`);
  fs.writeFileSync(filePath, content);
  
  return content;
}

/**
 * 获取上月月份字符串
 */
function getLastMonthStr() {
  const now = new Date();
  const lastMonth = new Date(now.getFullYear(), now.getMonth() - 1, 1);
  return `${lastMonth.getFullYear()}-${String(lastMonth.getMonth() + 1).padStart(2, '0')}`;
}

/**
 * 检查并记录上月欠费
 * 在每月 1 号调用，从上月账本读取总支出，计算欠费
 * @returns {Object|null} - 欠费信息或 null（无欠费）
 */
function checkMonthlyOverdraft() {
  const lastMonthStr = getLastMonthStr();
  const currentMonthStr = getMonthStr();
  const spendingLimit = 400;
  
  // 读取上月账本
  const lastMonthFile = path.join(POINTS_DIR, 'monthly', `${lastMonthStr}.md`);
  if (!fs.existsSync(lastMonthFile)) {
    return null;  // 上月无账本
  }
  
  const lastMonthLog = fs.readFileSync(lastMonthFile, 'utf8');
  const expenseMatch = lastMonthLog.match(/总支出 \| (\d+) 分/);
  
  if (!expenseMatch) {
    return null;  // 上月无支出记录
  }
  
  const lastMonthExpense = parseInt(expenseMatch[1]);
  const overdraft = Math.max(0, lastMonthExpense - spendingLimit);
  
  if (overdraft > 0) {
    // 有欠费，记录到本月账本
    const currentMonthFile = path.join(POINTS_DIR, 'monthly', `${currentMonthStr}.md`);
    let currentLog = '';
    
    if (fs.existsSync(currentMonthFile)) {
      currentLog = fs.readFileSync(currentMonthFile, 'utf8');
    } else {
      currentLog = createMonthlyLog(currentMonthStr);
    }
    
    // 检查是否已记录过欠费
    if (currentLog.includes('上月欠费结转')) {
      return {
        lastMonthExpense,
        spendingLimit,
        overdraft,
        availableLimit: spendingLimit - overdraft,
        alreadyRecorded: true
      };
    }
    
    // 在本月账本中添加欠费记录
    const overdraftLine = `| ${currentMonthStr}-01 | 欠费结转 | -${overdraft} | 上月超额消费结转 |`;
    
    // 找到调账记录部分，插入欠费记录
    const adjustmentIndex = currentLog.indexOf('## 调账记录');
    if (adjustmentIndex !== -1) {
      // 找到调账记录表格的末尾
      const tableEnd = currentLog.indexOf('---', adjustmentIndex);
      if (tableEnd !== -1) {
        const insertPos = currentLog.lastIndexOf('\n', tableEnd);
        currentLog = currentLog.slice(0, insertPos) + '\n' + overdraftLine + currentLog.slice(insertPos);
      }
    }
    
    // 更新本月汇总（减去欠费）
    const balanceMatch = currentLog.match(/当前结余 \| (\d+) 分/);
    if (balanceMatch) {
      const currentBalance = parseInt(balanceMatch[1]);
      const newBalance = currentBalance - overdraft;
      currentLog = currentLog.replace(/当前结余 \| \d+ 分/, `当前结余 | ${newBalance} 分`);
    }
    
    // 计算可用额度
    const availableLimit = spendingLimit - overdraft;
    
    // 更新距离上限显示
    const remainingMatch = currentLog.match(/距离上限 \(400 分\) \| \d+ 分/);
    if (remainingMatch) {
      currentLog = currentLog.replace(/距离上限 \(400 分\) \| \d+ 分/, `距离上限 (400 分) | ${Math.max(0, availableLimit)} 分`);
    }
    
    // 保存更新后的账本
    fs.writeFileSync(currentMonthFile, currentLog);
    
    return {
      lastMonthExpense,
      spendingLimit,
      overdraft,
      availableLimit,
      alreadyRecorded: false
    };
  }
  
  return null;  // 无欠费
}

/**
 * 检查 SenseAudio API Key 是否配置
 */
function checkSenseApiKey() {
  try {
    const configPath = path.join(process.env.HOME || '~', '.openclaw/openclaw.json');
    const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    const apiKey = config.env?.SENSE_API_KEY;
    return apiKey && apiKey.length > 10;
  } catch (e) {
    return false;
  }
}

/**
 * 获取友好的 API Key 提示文案
 */
function getApiKeyHint() {
  return `
  
💡 **提示：配置 API Key 后可解锁语音功能**
   • 🎤 语音记账 - 发送音频自动识别
   • 🔊 语音播报 - 积分变动自动鼓励（童声）
   • 📻 日报朗读 - 每天自动播报积分

👉 **快速配置**（目前基本免费）：
   1. 访问 https://senseaudio.cn
   2. 免费注册账号（送免费额度）
   3. 创建应用获取 API Key
   4. 添加到 ~/.openclaw/openclaw.json

📋 详细文档：查看 DEPENDENCIES.md`;
}

/**
 * 播放语音播报（使用 SenseAudio TTS，童声）
 */
function playTTS(text, callback) {
  // 检查 API Key 是否配置
  if (!checkSenseApiKey()) {
    // API Key 未配置，不播放语音，但可以返回提示
    if (callback) {
      callback(null, '', 'API_KEY_NOT_CONFIGURED');
    }
    return;
  }
  
  // 使用 child_0001_a 童声，更适合儿童学习场景
  const cmd = `python3 "${TTS_SCRIPT}" --voice child_0001_a --play "${text.replace(/"/g, '\\"')}"`;
  exec(cmd, (error, stdout, stderr) => {
    if (callback) callback(error, stdout, stderr);
  });
}

/**
 * 处理积分输入（支持多语言）
 */
function handlePointsInput(input, lang = 'zh') {
  const rules = loadRules();
  const tasks = parsePointsInput(input);
  
  if (tasks.length === 0) {
    return {
      success: false,
      message: t('noTasks', lang) + '\n\n' + (lang === 'zh' ? '例如："今天完成了汉字抄写 2 课，口算题卡 2 篇全对"' : lang === 'en' ? 'Example: "Completed 2 lessons of Chinese copying, 2 math cards all correct"' : '例：「漢字書き取り 2 課、算数カード 2 枚全て正解」')
    };
  }
  
  const result = calculatePoints(tasks, rules.rules);
  
  if (result.total === 0) {
    return {
      success: false,
      message: t('checkConditions', lang)
    };
  }
  
  // 记录到账本
  const dateStr = getTodayStr();
  recordIncome(dateStr, result.details, result.total);
  
  // 多语言响应
  let response;
  if (lang === 'en') {
    response = `✅ **${t('pointsRecorded', 'en')}**\n\n`;
    response += `📊 **Details**:\n`;
    for (const detail of result.details) {
      response += `• ${detail.task}: **+${detail.points} pts** (${detail.note})\n`;
    }
    response += `\n💰 **Total**: +${result.total} pts\n`;
    response += `\n_Automatically recorded. Check anytime!_`;
  } else if (lang === 'ja') {
    response = `✅ **${t('pointsRecorded', 'ja')}**\n\n`;
    response += `📊 **詳細**:\n`;
    for (const detail of result.details) {
      response += `• ${detail.task}: **+${detail.points} ポイント** (${detail.note})\n`;
    }
    response += `\n💰 **合計**: +${result.total} ポイント\n`;
    response += `\n_自動的に記録されました。いつでも確認できます！_`;
  } else {
    response = `✅ **${t('pointsRecorded', 'zh')}**\n\n`;
    response += `📊 **得分详情**:\n`;
    for (const detail of result.details) {
      response += `• ${detail.task}: **${detail.points}分** (${detail.note})\n`;
    }
    response += `\n💰 **总计**: +${result.total}分\n`;
    response += `\n_已自动记入账本，随时可以查看哦~_`;
  }
  
  // 语音播报（仅中文）
  if (lang === 'zh') {
    const ttsText = `太棒啦！获得${result.total}积分，${result.details.map(d => `${d.task}${d.note}`).join('，')}！继续加油哦！`;
    playTTS(ttsText, (error, stdout, stderr) => {
      if (stderr === 'API_KEY_NOT_CONFIGURED') {
        response += t('voiceHint', 'zh');
      }
    });
  } else if (lang === 'en') {
    response += t('voiceHint', 'en');
  } else if (lang === 'ja') {
    response += t('voiceHint', 'ja');
  }
  
  return {
    success: true,
    total: result.total,
    details: result.details,
    message: response,
    lang: lang
  };
}

/**
 * 处理消费输入（支持多语言）
 */
function handleExpenseInput(input, lang = 'zh') {
  // 多语言关键词
  const expenseKeywords = {
    zh: /积分消费|花了|支出|消费/,
    en: /expense|spent|cost|points/,
    ja: /消費|使った|支出|ポイント/
  };
  
  // 提取金额（支持多种格式）
  const amountMatch = input.match(/(\d+)\s*(分|pts|ポイント)/);
  const amount = amountMatch ? parseInt(amountMatch[1]) : 0;
  
  if (amount <= 0) {
    const hints = {
      zh: '请说清楚花了多少分，例如："积分消费 买零食花了 20 分"',
      en: 'Please specify points spent, e.g., "Expense: snacks 20 points"',
      ja: 'ポイント数を教えてください。例：「消費：お菓子 20 ポイント」'
    };
    return {
      success: false,
      message: `😕 ${t('noTasks', lang)}\n\n💡 ${hints[lang]}`
    };
  }
  
  // 提取消费描述
  let description = input;
  Object.values(expenseKeywords).forEach(regex => {
    description = description.replace(regex, '');
  });
  description = description.replace(/\d+\s*(分 | pts|ポイント)/, '').trim() || (lang === 'en' ? 'Expense' : lang === 'ja' ? '消費' : '消费');
  
  // 记录到账本
  const dateStr = getTodayStr();
  recordExpense(dateStr, amount, description);
  
  // 多语言响应
  let response;
  if (lang === 'en') {
    response = `✅ **${t('expenseRecorded', 'en')}**\n\n`;
    response += `💸 **Amount**: ${amount} pts\n`;
    response += `📝 **For**: ${description}\n\n`;
    response += `_Automatically recorded._\n\n`;
    response += t('voiceHint', 'en');
  } else if (lang === 'ja') {
    response = `✅ **${t('expenseRecorded', 'ja')}**\n\n`;
    response += `💸 **金額**: ${amount} ポイント\n`;
    response += `📝 **用途**: ${description}\n\n`;
    response += `_自動的に記録されました。_\n\n`;
    response += t('voiceHint', 'ja');
  } else {
    response = `✅ **${t('expenseRecorded', 'zh')}**\n\n`;
    response += `💸 **支出**: ${amount}分\n`;
    response += `📝 **用途**: ${description}\n\n`;
    response += `_已自动记入账本_\n\n`;
  }
  
  // 语音播报（仅中文）
  if (lang === 'zh') {
    const ttsText = `好的，已记录消费${amount}分，${description}。要合理消费哦！`;
    playTTS(ttsText, (error, stdout, stderr) => {
      if (stderr === 'API_KEY_NOT_CONFIGURED') {
        // 仅在 API Key 未配置时显示提示
        response += t('voiceHint', 'zh');
      }
    });
  }
  
  return {
    success: true,
    amount,
    description,
    message: response,
    lang: lang
  };
}

/**
 * 处理音频消息（语音记账）
 */
function handleAudioMessage(audioPath) {
  // 首先检查 API Key 是否配置
  if (!checkSenseApiKey()) {
    return {
      success: false,
      message: `🎤 **收到音频消息！**

⚠️ **语音识别功能需要配置 SenseAudio API Key**

📋 **快速配置**（目前基本免费）：
1. 访问 https://senseaudio.cn
2. 免费注册账号（送免费额度）
3. 创建应用获取 API Key
4. 添加到 ~/.openclaw/openclaw.json

💡 **提示**：
   • 目前基本免费，个人使用足够
   • 文字记账功能不受影响
   • 配置后发送音频即可自动识别

📝 **你也可以用文字记账**：
"学习积分 今天完成了汉字抄写 2 课"

${getApiKeyHint()}`
    };
  }
  
  // API Key 已配置，调用 ASR 识别
  const ASR_SCRIPT = path.join(WORKSPACE, 'skills/senseaudio-voice/scripts/asr.py');
  const cmd = `python3 "${ASR_SCRIPT}" "${audioPath}"`;
  
  return new Promise((resolve) => {
    exec(cmd, (error, stdout, stderr) => {
      if (error) {
        resolve({
          success: false,
          message: `🎤 **语音识别失败**\n\n${error.message}\n\n请再试一次，或用文字记账~`
        });
        return;
      }
      
      // 识别成功，提取文本
      const recognizedText = stdout.trim();
      
      if (!recognizedText) {
        resolve({
          success: false,
          message: `🎤 **没有识别到内容**\n\n请再说一次，声音大一点哦~`
        });
        return;
      }
      
      // 自动处理识别的文本
      if (recognizedText.includes('学习积分')) {
        const result = handlePointsInput(recognizedText);
        resolve(result);
      } else if (recognizedText.includes('积分消费')) {
        const result = handleExpenseInput(recognizedText);
        resolve(result);
      } else {
        resolve({
          success: false,
          message: `🎤 **识别成功**：${recognizedText}\n\n但不知道要做什么哦~\n\n请说"学习积分 xxx"或"积分消费 xxx"`
        });
      }
    });
  });
}

/**
 * 从 balance.md 解析指定日期的积分明细
 */
function parseDayFromBalance(dateStr) {
  const balanceFile = path.join(POINTS_DIR, 'balance.md');
  
  if (!fs.existsSync(balanceFile)) {
    return null;
  }
  
  const content = fs.readFileSync(balanceFile, 'utf8');
  const lines = content.split('\n');
  const income = [];
  const expense = [];
  let totalIncome = 0;
  let totalExpense = 0;
  
  for (const line of lines) {
    if (line.includes(dateStr) && (line.includes('收入') || line.includes('支出'))) {
      const parts = line.split('|').map(p => p.trim()).filter(p => p);
      if (parts.length >= 5) {
        const [, type, pointsStr, , description] = parts;
        const points = parseFloat(pointsStr.replace('+', '').replace('-', ''));
        
        if (type === '收入') {
          income.push({ task: description.replace(/。*$/, '').trim(), points });
          totalIncome += points;
        } else if (type === '支出') {
          expense.push({ task: description.replace(/。*$/, '').trim(), points });
          totalExpense += points;
        }
      }
    }
  }
  
  return { income, expense, totalIncome, totalExpense, net: totalIncome - totalExpense };
}

/**
 * 生成日报（从 balance.md 读取实时数据）
 */
function generateDailyReport(dateStr = null) {
  const targetDate = dateStr || getTodayStr();
  const data = parseDayFromBalance(targetDate);
  
  if (!data || (data.income.length === 0 && data.expense.length === 0)) {
    let message = `📅 **${targetDate} 日报**\n\n_今天还没有积分记录哦~\n\n快来说说今天完成了什么任务吧!_`;
    
    if (!checkSenseApiKey()) {
      message += getApiKeyHint();
    }
    
    return { message, date: targetDate, hasData: false };
  }
  
  // 生成日报内容
  let message = `📅 **${targetDate} 积分日报**\n\n`;
  message += `━━━━━━━━━━━━━━━━━━\n\n`;
  message += `📊 **今日概览**:\n\n`;
  message += `| 项目 | 数值 |\n`;
  message += `|------|------|\n`;
  message += `| 总收入 | ${data.totalIncome} 分 |\n`;
  message += `| 总支出 | ${data.totalExpense} 分 |\n`;
  message += `| 净收益 | ${data.net >= 0 ? '+' : ''}${data.net} 分 |\n`;
  message += `| 当前余额 | 待计算 |\n\n`;
  
  if (data.income.length > 0) {
    message += `**💰 收入明细**:\n`;
    for (const item of data.income) {
      message += `• ${item.task}: **+${item.points}分**\n`;
    }
    message += `\n`;
  }
  
  if (data.expense.length > 0) {
    message += `**💸 支出明细**:\n`;
    for (const item of data.expense) {
      message += `• ${item.task}: **-${item.points}分**\n`;
    }
    message += `\n`;
  }
  
  message += `━━━━━━━━━━━━━━━━━━\n\n`;
  
  // 鼓励语
  if (data.net > 0) {
    message += `🎉 今天表现不错，继续加油！\n\n`;
  } else if (data.net < 0) {
    message += `⚠️ 今天支出有点多哦，明天继续努力！\n\n`;
  } else {
    message += `💪 今天争取更多积分吧！\n\n`;
  }
  
  if (!checkSenseApiKey()) {
    message += `💡 **提示**：配置 API Key 后可启用语音播报，每天早上 7 点自动朗读日报（童声）\n\n👉 https://senseaudio.cn`;
  }
  
  return { 
    message, 
    date: targetDate, 
    hasData: true,
    data: data
  };
}

/**
 * 生成周报（从 balance.md 读取实时数据）
 */
function generateWeeklyReport() {
  const today = new Date();
  const dayOfWeek = today.getDay();
  const diff = today.getDate() - dayOfWeek + (dayOfWeek === 0 ? -6 : 1);
  const monday = new Date(today);
  monday.setDate(diff);
  
  const weekStart = monday.toISOString().split('T')[0];
  const weekEnd = today.toISOString().split('T')[0];
  
  // 获取本周所有数据
  const balanceFile = path.join(POINTS_DIR, 'balance.md');
  if (!fs.existsSync(balanceFile)) {
    return { message: '📈 **本周积分**\n\n暂无数据~' };
  }
  
  const content = fs.readFileSync(balanceFile, 'utf8');
  const lines = content.split('\n');
  const dailyData = {};
  let totalIncome = 0;
  let totalExpense = 0;
  
  for (const line of lines) {
    if (line >= weekStart && line <= weekEnd) {
      const date = line.split('|')[1]?.trim();
      if (date && !dailyData[date]) {
        dailyData[date] = { income: 0, expense: 0 };
      }
      
      if (line.includes('收入')) {
        const points = parseFloat(line.split('|')[3]?.trim().replace('+', '')) || 0;
        if (dailyData[date]) dailyData[date].income += points;
        totalIncome += points;
      } else if (line.includes('支出')) {
        const points = parseFloat(line.split('|')[3]?.trim().replace('-', '')) || 0;
        if (dailyData[date]) dailyData[date].expense += points;
        totalExpense += points;
      }
    }
  }
  
  if (totalIncome === 0 && totalExpense === 0) {
    return { message: '📈 **本周积分**\n\n本周还没有积分记录哦~\n\n快开始赚取积分吧！' };
  }
  
  let message = `📈 **本周积分汇总** (${weekStart} ~ ${weekEnd})\n\n`;
  message += `━━━━━━━━━━━━━━━━━━\n\n`;
  message += `**📊 本周概览**:\n\n`;
  message += `| 项目 | 数值 |\n`;
  message += `|------|------|\n`;
  message += `| 总收入 | ${totalIncome} 分 |\n`;
  message += `| 总支出 | ${totalExpense} 分 |\n`;
  message += `| 净收益 | ${totalIncome - totalExpense >= 0 ? '+' : ''}${totalIncome - totalExpense} 分 |\n\n`;
  
  message += `**📅 每日明细**:\n\n`;
  for (const [date, data] of Object.entries(dailyData)) {
    const net = data.income - data.expense;
    message += `• **${date}**: 收入 ${data.income}分，支出 ${data.expense}分，净收益 ${net >= 0 ? '+' : ''}${net}分\n`;
  }
  
  message += `\n━━━━━━━━━━━━━━━━━━\n\n`;
  
  if (totalIncome - totalExpense > 0) {
    message += `🎉 本周表现不错，继续加油！\n\n`;
  } else {
    message += `💪 下周继续努力！\n\n`;
  }
  
  return { 
    message, 
    weekStart, 
    weekEnd, 
    totalIncome, 
    totalExpense,
    net: totalIncome - totalExpense
  };
}

module.exports = {
  handlePointsInput,
  handleExpenseInput,
  handleAudioMessage,
  generateDailyReport,
  generateWeeklyReport,
  getTodayStr,
  getMonthStr,
  getLastMonthStr,
  checkMonthlyOverdraft,
  checkSenseApiKey,
  getApiKeyHint,
  detectLanguage,
  t,
  parseDayFromBalance
};
