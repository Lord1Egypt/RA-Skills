/**
 * setup_reminders.js - 定时提醒设置脚本
 *
 * 功能：
 * 1. 生成三条定时提醒的 cron 配置
 * 2. 直接通过 exec 执行 openclaw cron add 命令（无需用户手动执行）
 *
 * 使用场景：
 * - 用户首次通过 AI 成功录入第一条任务后，AI 自动调用本脚本
 * - 由 AI 直接执行，用户无感知
 *
 * 用法：node setup_reminders.js [--lang zh|en] [--open-id USER_OPEN_ID]
 *   --lang: 指定输出语言，默认读取 memory/preferences.json
 *   --open-id: 可选，传入时同时配置用户 ID（预留字段，当前未使用）
 */

const { execSync } = require('child_process');
const { getLanguage } = require('./preferences');
const path = require('path');
const fs = require('fs');

// 三条定时提醒的配置（Prompt 优化版本 - 2026-05-12）
const REMINDERS = [
  {
    name: '工作日早晨提醒',
    cron: '28 8 * * *',
    tz: 'Asia/Shanghai',
    description_zh: '每天 08:28 发送当日工作重点（优先级/进行中任务）',
    description_en: 'Daily at 08:28 - sends morning work focus (priority tasks + in-progress)',
    message_zh: `早呀~今日工作提醒如下：

【工作日判断】
调用 http://api.jiejiariapi.com/v1/holidays/2026 → 查 isOffDay(false=工作日/调休) → 是则继续，否则静默

【飞书多维表格查询】（APP_TOKEN: YOUR_APP_TOKEN / TABLE_ID: YOUR_TABLE_ID）
- 截止日期为今天且状态<>已完成且状态<>取消的任务（视为今日待办）
- 截止日期为今天且状态=已完成的任务（今日已完成）

【输出格式】
1. 今日完成(X项)
2. 今日重点（优先级①的任务，注明任务名和截止时间）
3. 进行中/待办任务（任务名、状态、截止日期、优先级）
4. 建议时间安排（先处理邮件和OA审批）`,
    message_en: `Good morning! Here's today's work reminder:

【Workday Check】
Call http://api.jiejiariapi.com/v1/holidays/2026 → check isOffDay(false=workday/adjustment) → continue if yes, otherwise stay silent

【Feishu Bitable Query】（APP_TOKEN: YOUR_APP_TOKEN / TABLE_ID: YOUR_TABLE_ID）
- Completed: deadline = today AND status = Done
- Incomplete: start time <= today AND status <> Done AND status <> Cancelled

【Output Format】
1. Completed today (X items)
2. Priority tasks (priority ①, name + deadline)
3. In-progress / To-do tasks (name, status, deadline, priority)
4. Suggested time allocation (process emails and OA first)`,
  },
  {
    name: '工作日下午提醒',
    cron: '0 14 * * *',
    tz: 'Asia/Shanghai',
    description_zh: '每天 14:00 发送下午工作安排（上午未完成任务回顾）',
    description_en: 'Daily at 14:00 - sends afternoon work arrangement (morning incomplete tasks review)',
    message_zh: `下午好~开始前建议先花半小时清一下邮件和待办，理顺思路，下午工作更顺~

【工作日判断】
调用 http://api.jiejiariapi.com/v1/holidays/2026 → 查 isOffDay(false=工作日/调休) → 是则继续，否则静默

【飞书多维表格查询】（APP_TOKEN: YOUR_APP_TOKEN / TABLE_ID: YOUR_TABLE_ID）
- 截止日期为今天且状态<>已完成且状态<>取消的任务（视为今日待办）
- 截止日期为今天且状态=已完成的任务（今日已完成）

【输出格式】
1. 上午复盘（今日已完成 X 项）
2. 今日待办（任务名、状态、截止日期、优先级）
3. 下午建议（优先处理紧急且重要的任务）`,
    message_en: `Good afternoon! Before diving in, suggest clearing emails and pending tasks for 30 min to get organized.

【Workday Check】
Call http://api.jiejiariapi.com/v1/holidays/2026 → check isOffDay(false=workday/adjustment) → continue if yes, otherwise stay silent

【Feishu Bitable Query】（APP_TOKEN: YOUR_APP_TOKEN / TABLE_ID: YOUR_TABLE_ID）
- Completed: deadline = today AND status = Done
- Incomplete: start time <= today AND status <> Done AND status <> Cancelled

【Output Format】
1. Morning review (completed X items today)
2. Today's to-do (name, status, deadline, priority)
3. Afternoon suggestion (prioritize urgent and important tasks)`,
  },
  {
    name: '工作日下班前复盘',
    cron: '30 17 * * 1-5',
    tz: 'Asia/Shanghai',
    description_zh: '每周一至周五 17:30 发送 PMBOK 式进度复盘（完成率/未完成决策/明日预告）',
    description_en: 'Weekdays (Mon-Fri) at 17:30 - sends PMBOK-style progress review (completion rate / pending decisions / tomorrow preview)',
    message_zh: `下班前复盘来了~

【工作日判断】
调用 http://api.jiejiariapi.com/v1/holidays/2026 → 查 isOffDay(false=工作日/调休) → 是则继续，否则静默

【飞书多维表格查询】（APP_TOKEN: YOUR_APP_TOKEN / TABLE_ID: YOUR_TABLE_ID）
- 截止日期为今天且状态<>已完成且状态<>取消的任务（今日未完成）
- 截止日期为今天且状态=已完成的任务（今日已完成）

【PMBOK 五步复盘输出格式】
1. 量化复盘（今日截止共X项，完成X项，完成率X%）
2. 未完成任务逐一决策（推迟/取消/已有计划）
3. 阻碍分析（询问原因，填入存在问题字段）
4. 工作建议（风险应对：规避/转移/缓解/接受；进度纠偏：赶工/快速跟进/调整范围）
5. 明日预告（截止日期为明天且状态<>已完成且状态<>取消的重要任务）`,
    message_en: `Before end-of-day review time!

【Workday Check】
Call http://api.jiejiariapi.com/v1/holidays/2026 → check isOffDay(false=workday/adjustment) → continue if yes, otherwise stay silent

【Feishu Bitable Query】（APP_TOKEN: YOUR_APP_TOKEN / TABLE_ID: YOUR_TABLE_ID）
- Completed: deadline = today AND status = Done
- Incomplete: start time <= today AND status <> Done AND status <> Cancelled

【PMBOK 5-Step Review Output Format】
1. Quantified review (X total, X completed, X% done today)
2. Pending task decisions one by one (defer/cancel/has follow-up plan)
3. Bottleneck analysis (ask for reasons, fill Issues field)
4. Work suggestions (risk response: avoid/transfer/mitigate/accept; schedule recovery: crash/fast-track/scope change)
5. Tomorrow preview (important & urgent tasks with status <> Done AND status <> Cancelled)`,
  },
];

// 以下为剩余代码（不变）
function escapeForCli(str) {
  return str
    .replace(/"/g, '\\"')
    .replace(/'/g, "\\'")
    .replace(/\n/g, '\\n')
    .replace(/\r/g, '')
    .replace(/≤/g, '<=')
    .replace(/≥/g, '>=')
    .replace(/≠/g, '<>')
    .replace(/～/g, '~');
}

function formatMessage(message) {
  const now = new Date();
  const yyyy = now.getFullYear();
  const mm = String(now.getMonth() + 1).padStart(2, '0');
  const dd = String(now.getDate()).padStart(2, '0');
  const dateStr = `${yyyy}-${mm}-${dd}`;
  const weekdayMap = ['日', '一', '二', '三', '四', '五', '六'];
  const weekdayStr = weekdayMap[now.getDay()];
  return message
    .replace(/\{DATE\}/g, dateStr)
    .replace(/\{YEAR\}/g, yyyy)
    .replace(/\{MONTH\}/g, String(now.getMonth() + 1))
    .replace(/\{DAY\}/g, String(now.getDate()))
    .replace(/\{WEEKDAY\}/g, weekdayStr);
}

function buildCronCommand(reminder, lang, userOpenId) {
  const rawMessage = lang === 'zh' ? reminder.message_zh : reminder.message_en;
  const escapedMessage = escapeForCli(formatMessage(rawMessage));
  const description = lang === 'zh' ? reminder.description_zh : reminder.description_en;

  return `openclaw cron add --name "${reminder.name}" --description "${description}" --cron "${reminder.cron}" --tz "${reminder.tz}" --message "${escapedMessage}" --announce --channel feishu --to "user:${userOpenId}" --session isolated --session-key "agent:main:feishu:direct:${userOpenId}" --json`;
}

function executeCron(command, reminder, lang) {
  try {
    const output = execSync(command, {
      encoding: 'utf8',
      timeout: 30000,
      windowsHide: true
    });

    let result;
    try {
      result = JSON.parse(output.trim());
    } catch {
      result = { success: true, output: output.trim() };
    }

    if (result.success !== false && result.id) {
      console.log(lang === 'zh'
        ? `   ✅ ${reminder.name} 创建成功 (ID: ${result.id})`
        : `   ✅ ${reminder.name} created (ID: ${result.id})`);
      return { success: true, id: result.id };
    } else {
      console.log(lang === 'zh'
        ? `   ❌ ${reminder.name} 创建失败: ${result.message || output}`
        : `   ❌ ${reminder.name} failed: ${result.message || output}`);
      return { success: false, error: result.message || output };
    }
  } catch (error) {
    const errMsg = error.stdout || error.stderr || error.message;
    console.log(lang === 'zh'
      ? `   ❌ ${reminder.name} 执行失败: ${errMsg}`
      : `   ❌ ${reminder.name} execution failed: ${errMsg}`);
    return { success: false, error: errMsg };
  }
}

async function main() {
  const lang = getLanguage() || 'zh';

  const args = process.argv.slice(2);
  let userOpenId = null;
  for (const arg of args) {
    if (arg.startsWith('--open-id=')) {
      userOpenId = arg.split('=')[1];
    }
  }

  if (!userOpenId) {
    try {
      const prefPath = path.join(__dirname, '..', 'memory', 'preferences.json');
      if (fs.existsSync(prefPath)) {
        const pref = JSON.parse(fs.readFileSync(prefPath, 'utf8'));
        userOpenId = pref.openId || null;
      }
    } catch (e) {}
  }

  if (!userOpenId) {
    console.log(lang === 'zh'
      ? '\n⚠️  未提供 --open-id 参数，定时提醒将无法发送到正确用户。'
      : '\n⚠️  --open-id not provided, reminders cannot be sent to the correct user.');
    console.log(lang === 'zh'
      ? '    请使用: node scripts/setup_reminders.js --open-id "USER_OPEN_ID"'
      : '    Usage: node scripts/setup_reminders.js --open-id "USER_OPEN_ID"');
    process.exit(1);
  }

  console.log(lang === 'zh'
    ? '\n🔔 开始设置三条定时提醒...'
    : '\n🔔 Setting up 3 scheduled reminders...');

  const results = [];
  for (let i = 0; i < REMINDERS.length; i++) {
    const reminder = REMINDERS[i];
    const command = buildCronCommand(reminder, lang, userOpenId);

    if (lang === 'zh') {
      console.log(`\n【${i + 1}】${reminder.name}`);
      console.log(`   时间: ${reminder.cron} @ ${reminder.tz}`);
    } else {
      console.log(`\n【${i + 1}】${reminder.name}`);
      console.log(`   Schedule: ${reminder.cron} @ ${reminder.tz}`);
    }

    const result = executeCron(command, reminder, lang);
    results.push({ reminder: reminder.name, ...result });
  }

  const successCount = results.filter(r => r.success).length;
  const failCount = results.filter(r => !r.success).length;

  console.log(lang === 'zh'
    ? `\n📊 定时提醒设置完成：成功 ${successCount}/3`
    : `\n📊 Reminder setup complete: ${successCount}/3 succeeded`);

  if (failCount > 0) {
    console.log(lang === 'zh'
      ? `\n⚠️  有 ${failCount} 条提醒创建失败，请检查错误信息。`
      : `\n⚠️  ${failCount} reminder(s) failed - please check error messages above.`);
  } else {
    console.log(lang === 'zh'
      ? '✅ 全部设置成功，每天会在对应时间自动收到工作提醒！'
      : '✅ All reminders set up successfully! You\'ll receive work reminders at scheduled times daily.');
  }

  return {
    success: failCount === 0,
    results
  };
}

main().then(result => {
  process.exit(result.success ? 0 : 1);
}).catch(err => {
  console.error('❌ Unexpected error:', err.message);
  process.exit(1);
});