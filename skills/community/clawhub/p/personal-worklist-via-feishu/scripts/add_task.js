/**
 * 添加任务到飞书多维表格
 * 
 * 【日期格式】截止日期支持：YYYY-MM-DD / YYYY/MM/DD
 * 【时间戳】日期字段以毫秒时间戳存储（飞书create API要求毫秒，update API要求秒，需分开处理）
 * 【开始时间】默认值为任务录入当天，不传则自动填充
 * 
 * 用法: node add_task.js --task "任务名称" --source "计划任务[P]" --priority "①紧急且重要" --deadline "2026-04-25" --duration "2h" --start "9:00" --notes "备注" --link "https://..." --requirement "工作要求" --stakeholders "张三,李四" [--lang zh|en]
 * 
 * 至少需要 --task（任务名称）才能执行
 * 
 * 英文模式下可用：
 * node add_task.js --task "Task name" --source "Planned[P]" --priority "① Urgent and Important" --deadline "2026-04-25" --lang "en"
 */

const { apiPost, apiGet } = require('./request');
const { CONFIG } = require('./config');
const { getLanguage, getTemplates, format } = require('./i18n');
const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

// memory 目录下提醒标记文件路径
const REMINDER_DONE_FILE = path.join(__dirname, '..', 'memory', 'reminder_setup_done');

// 检查是否已完成定时提醒设置
function isReminderSetupDone() {
  return fs.existsSync(REMINDER_DONE_FILE);
}

// 标记定时提醒设置已完成
function markReminderSetupDone() {
  try {
    fs.writeFileSync(REMINDER_DONE_FILE, new Date().toISOString(), 'utf8');
    return true;
  } catch (e) {
    return false;
  }
}

// 自动执行定时提醒设置
async function autoSetupReminders(lang) {
  const t = getTemplates(lang);
  const scriptPath = path.join(__dirname, 'setup_reminders.js');

  console.log(lang === 'zh'
    ? '\n🔔 检测到首次任务录入，自动创建定时提醒...'
    : '\n🔔 First task detected, automatically setting up reminders...');

  try {
    const output = execSync(`node "${scriptPath}" --lang ${lang}`, {
      encoding: 'utf8',
      timeout: 60000,
      windowsHide: true
    });
    console.log(output);

    if (output.includes('成功') || output.includes('succeeded') || output.includes('✅')) {
      markReminderSetupDone();
      console.log(lang === 'zh'
        ? '\n✅ 定时提醒设置完成！'
        : '\n✅ Reminder setup complete!');
      return { success: true };
    } else {
      console.log(lang === 'zh'
        ? '\n⚠️ 定时提醒设置可能有失败，请检查上方输出'
        : '\n⚠️ Some reminders may have failed - please check output above');
      return { success: false };
    }
  } catch (error) {
    const errMsg = error.stdout || error.stderr || error.message;
    console.log(lang === 'zh'
      ? `❌ 定时提醒设置失败: ${errMsg}`
      : `❌ Reminder setup failed: ${errMsg}`);
    return { success: false, error: errMsg };
  }
}

function parseArgs() {
  const args = process.argv.slice(2);
  const config = {};
  for (let i = 0; i < args.length; i += 2) {
    const key = args[i].replace('--', '');
    const value = args[i + 1];
    config[key] = value;
  }
  return config;
}

// 相对日期转换为具体日期
// 触发词：今天/明天/后天/今天上午/今天下午/明天上午/明天下午 等
function parseRelativeDate(dateStr) {
  if (!dateStr || typeof dateStr !== 'string') return dateStr;
  
  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  
  const lower = dateStr.toLowerCase();
  
  // 今天 / 今天上午 / 今天下午
  if (lower === '今天' || lower === 'today') {
    return formatDateStr(today);
  }
  if (lower === '明天' || lower === 'tomorrow') {
    const d = new Date(today);
    d.setDate(d.getDate() + 1);
    return formatDateStr(d);
  }
  if (lower === '后天' || lower === 'day after tomorrow') {
    const d = new Date(today);
    d.setDate(d.getDate() + 2);
    return formatDateStr(d);
  }
  
  // 明天上午 / 明天下午 / 今天上午 / 今天下午
  const amPmMatch = lower.match(/^(今天|明天|后天)(上午|下午|晚上)?$/);
  if (amPmMatch) {
    const dayWord = amPmMatch[1];
    const timePart = amPmMatch[2] || '';
    let targetDay;
    if (dayWord === '今天') targetDay = new Date(today);
    else if (dayWord === '明天') { targetDay = new Date(today); targetDay.setDate(targetDay.getDate() + 1); }
    else if (dayWord === '后天') { targetDay = new Date(today); targetDay.setDate(targetDay.getDate() + 2); }
    
    if (timePart === '上午') return formatDateStr(targetDay) + ' 09:00';
    if (timePart === '下午') return formatDateStr(targetDay) + ' 14:00';
    if (timePart === '晚上') return formatDateStr(targetDay) + ' 18:00';
    return formatDateStr(targetDay);
  }
  
  // 本周一/本周二 ... 本周日
  const weekMatch = lower.match(/^本周([一二三四五六日天])/);
  if (weekMatch) {
    const dayMap = { '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '日': 7, '天': 7 };
    const targetWeekday = dayMap[weekMatch[1]];
    const currentWeekday = today.getDay() || 7; // 周日为7
    let diff = targetWeekday - currentWeekday;
    if (diff <= 0) diff += 7;
    const targetDay = new Date(today);
    targetDay.setDate(targetDay.getDate() + diff);
    return formatDateStr(targetDay);
  }
  
  // 下周一 / 下周二 ...
  const nextWeekMatch = lower.match(/^下周([一二三四五六日天])/);
  if (nextWeekMatch) {
    const dayMap = { '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '日': 7, '天': 7 };
    const targetWeekday = dayMap[nextWeekMatch[1]];
    const currentWeekday = today.getDay() || 7;
    let diff = targetWeekday - currentWeekday + 7;
    const targetDay = new Date(today);
    targetDay.setDate(targetDay.getDate() + diff);
    return formatDateStr(targetDay);
  }
  
  return dateStr; // 非相对日期，原样返回
}

// 格式化日期为 YYYY-MM-DD
function formatDateStr(date) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, '0');
  const d = String(date.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

// 中文字段名 → 英文字段名映射
const FIELD_NAME_MAP = {
  '任务名称': 'Task Name',
  '来源分类': 'Source Category',
  '优先级': 'Priority',
  '状态': 'Status',
  '截止日期': 'Deadline',
  '预计时长': 'Estimated Time',
  '开始时间': 'Start Time',
  '工作链接': 'Work Link',
  '工作要求': 'Requirements',
  '干系人': 'Stakeholder',
  '存在问题': 'Issues',
  '备注': 'Notes'
};

// 获取多维表格实际字段名（根据语言）
function getFieldName(zhName, lang) {
  if (lang === 'en') {
    return FIELD_NAME_MAP[zhName] || zhName;
  }
  return zhName;
}

// 转换字段值（优先级/状态/来源）
function translateFieldValue(fieldName, value, lang) {
  // 不再翻译，直接返回原值（中文模式用中文值，英文模式用英文值）
  return value;
}

// 选项值白名单（必须从这些值中选择，禁止自行填入其他值）
const VALID_SOURCES = ['计划任务[P]', '临时任务[U]', '例行任务[R]', '协作任务[C]', 'Planned[P]', 'Urgent[U]', 'Routine[R]', 'Collab[C]'];
const VALID_PRIORITIES = ['①紧急且重要', '②重要不紧急', '③紧急不重要', '④不紧急不重要', '① Urgent and Important', '② Not Urgent but Important', '③ Urgent but Not Important', '④ Not Urgent and Not Important'];
const VALID_STATUSES = ['待办', '进行中', '已完成', '取消', 'To Do', 'In Progress', 'Done', 'Cancelled'];

// 验证选项值是否合法
function validateOption(fieldName, value, validOptions, lang) {
  if (!value) return { valid: true, value: value };
  if (validOptions.includes(value)) return { valid: true, value: value };
  return { valid: false, value: value };
}

async function addTask(config) {
  if (!config.task) {
    const lang = config.lang || getLanguage();
    const t = getTemplates(lang);
    console.error(lang === 'zh' ? '❌ 任务名称不能为空' : '❌ Task name is required');
    console.error(lang === 'zh' ? `   用法: node add_task.js --task "任务名称" --source "计划任务[P]" --priority "①紧急且重要" --deadline "2026-04-25"` : `   Usage: node add_task.js --task "Task name" --source "Planned[P]" --priority "① Urgent and Important" --deadline "2026-04-25"`);
    process.exit(1);
  }

  const lang = config.lang || getLanguage();

  // ================================================================
  // 【重要】飞书多维表格日期字段要求：毫秒时间戳（create API 期望毫秒）
  // 传入日期格式支持：YYYY-MM-DD / YYYY/MM/DD / MM-DD / MM/DD
  // 所有日期入库前统一转换为毫秒时间戳
  // ================================================================
  
  // 【重要】来源分类、优先级、状态必须使用表格中的选项值，禁止自行填入其他值
  // 验证来源分类
  const defaultSource = lang === 'zh' ? '计划任务[P]' : 'Planned[P]';
  const sourceInput = config.source || defaultSource;
  if (!VALID_SOURCES.includes(sourceInput)) {
    console.error(lang === 'zh' 
      ? `❌ 来源分类「${sourceInput}」不在允许的选项中。允许的选项：计划任务[P] / 临时任务[U] / 例行任务[R] / 协作任务[C]`
      : `❌ Source "${sourceInput}" is not a valid option. Valid options: Planned[P] / Urgent[U] / Routine[R] / Collab[C]`);
    process.exit(1);
  }

  // 验证优先级
  const defaultPriority = lang === 'zh' ? '②重要不紧急' : '② Not Urgent but Important';
  const priorityInput = config.priority || defaultPriority;
  if (!VALID_PRIORITIES.includes(priorityInput)) {
    console.error(lang === 'zh'
      ? `❌ 优先级「${priorityInput}」不在允许的选项中。允许的选项：①紧急且重要 / ②重要不紧急 / ③紧急不重要 / ④不紧急不重要`
      : `❌ Priority "${priorityInput}" is not a valid option. Valid options: ① Urgent and Important / ② Not Urgent but Important / ③ Urgent but Not Important / ④ Not Urgent and Not Important`);
    process.exit(1);
  }

  // 验证状态
  const defaultStatus = lang === 'zh' ? '待办' : 'To Do';
  const statusInput = config.status || defaultStatus;
  if (!VALID_STATUSES.includes(statusInput)) {
    console.error(lang === 'zh'
      ? `❌ 状态「${statusInput}」不在允许的选项中。允许的选项：待办 / 进行中 / 已完成 / 取消`
      : `❌ Status "${statusInput}" is not a valid option. Valid options: To Do / In Progress / Done / Cancelled`);
    process.exit(1);
  }
  
  // 【重要】相对日期转换：今天/明天/后天 等词必须转换为具体日期
  // 禁止写入"今天/明天/后天"等模糊词
  const parsedDeadline = parseRelativeDate(config.deadline);
  const parsedStart = parseRelativeDate(config.start);
  
  // 转换日期为时间戳（飞书需要毫秒）
  let deadlineTs = null;
  let deadlineTimeStr = null;
  if (parsedDeadline) {
    const date = new Date(parsedDeadline);
    date.setHours(0, 0, 0, 0);
    deadlineTs = date.getTime();
    // 提取截止时间中的时间部分（如 "14:30"）
    const deadlineHasTime = /\s\d{1,2}:\d{2}$/.test(parsedDeadline);
    if (deadlineHasTime) {
      deadlineTimeStr = parsedDeadline.match(/\s(\d{1,2}:\d{2})$/)?.[1] || null;
    }
  }

  // 开始时间默认值：任务录入当天（格式：YYYY-MM-DD）
  // 使用 config.start !== undefined 判断是否有传入值，避免空字符串覆盖默认值
  const today = new Date();
  const todayStr = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;
  const startTimeRaw = parsedStart !== undefined ? parsedStart : todayStr;
  // 提取开始时间中的时间部分（如 "14:30"）
  let startTimeStr = null;
  const startHasTime = /\s\d{1,2}:\d{2}$/.test(startTimeRaw);
  if (startHasTime) {
    startTimeStr = startTimeRaw.match(/\s(\d{1,2}:\d{2})$/)?.[1] || null;
  }
  // 转换为毫秒时间戳（处理 YYYY-MM-DD HH:MM 格式，保留具体时间）
  const startTimeTs = (() => {
    if (!startTimeRaw) return null;
    const d = new Date(startTimeRaw);
    // 如果 parsed date 包含时间部分（如 "2026-05-09 14:00"），保留时间
    // 否则默认 00:00:00
    if (!startHasTime) {
      d.setHours(0, 0, 0, 0);
    }
    return d.getTime();
  })();

  // 构建时间备注：当开始时间或截止时间含具体时间点时，同步写入工作要求
  const timeRemarkParts = [];
  if (startTimeStr) timeRemarkParts.push(startTimeStr + '开始');
  if (deadlineTimeStr) timeRemarkParts.push(deadlineTimeStr + '截止');
  const timeRemark = timeRemarkParts.length > 0 ? '⏰ ' + timeRemarkParts.join('，') + '。' : '';

  // 将时间备注追加到工作要求开头
  const finalRequirement = timeRemark + (config.requirement || '');

  // 获取字段名（根据语言）
  const fieldName_task = getFieldName('任务名称', lang);
  const fieldName_source = getFieldName('来源分类', lang);
  const fieldName_priority = getFieldName('优先级', lang);
  const fieldName_status = getFieldName('状态', lang);
  const fieldName_deadline = getFieldName('截止日期', lang);
  const fieldName_duration = getFieldName('预计时长', lang);
  const fieldName_start = getFieldName('开始时间', lang);
  const fieldName_notes = getFieldName('备注', lang);
  const fieldName_link = getFieldName('工作链接', lang);
  const fieldName_req = getFieldName('工作要求', lang);
  const fieldName_stakeholder = getFieldName('干系人', lang);

  // 转换字段值
  const source = translateFieldValue('来源分类', config.source || (lang === 'zh' ? '计划任务[P]' : 'Planned[P]'), lang);
  const priority = translateFieldValue('优先级', config.priority || (lang === 'zh' ? '②重要不紧急' : '② Important'), lang);
  const status = translateFieldValue('状态', config.status || (lang === 'zh' ? '待办' : 'To Do'), lang);

  const fields = {};
  fields[fieldName_task] = config.task;
  fields[fieldName_source] = source;
  fields[fieldName_priority] = priority;
  fields[fieldName_status] = status;
  fields[fieldName_duration] = config.duration || '';
  fields[fieldName_start] = startTimeTs;

  if (config.notes) {
    fields[fieldName_notes] = config.notes;
  }

  if (deadlineTs) {
    fields[fieldName_deadline] = deadlineTs;
  }

  if (config.link) {
    fields[fieldName_link] = { "link": config.link, "text": config.link };
  }

  if (finalRequirement) {
    fields[fieldName_req] = finalRequirement;
  }

  // 允许 --stakeholder 和 --stakeholders 两种参数名
  if (config.stakeholder !== undefined && config.stakeholders === undefined) {
    config.stakeholders = config.stakeholder;
  }

  if (config.stakeholders) {
    fields[fieldName_stakeholder] = config.stakeholders;
  }

  const result = await apiPost(
    `/bitable/v1/apps/${CONFIG.APP_TOKEN}/tables/${CONFIG.TABLE_ID}/records`,
    { fields }
  );

  return result;
}

async function main() {
  try {
    const config = parseArgs();
    const lang = config.lang || getLanguage();

    // 【强制检查】语言环境必须已设置（通过 --lang 参数或 preferences.json）
    // 如果语言未设置，脚本必须退出并报错，禁止在语言不明的情况下录入任务
    if (!lang) {
      console.error('============================================================');
      console.error('❌ 错误：语言环境未设置');
      console.error('');
      console.error('在录入任务之前，必须先确认语言环境。');
      console.error('');
      console.error('请先告诉 AI 您的语言偏好：');
      console.error('  - 输入 "中文" 或 "c" → 使用中文');
      console.error('  - 输入 "英文" 或 "e" → Use English');
      console.error('');
      console.error('示例：告诉 AI "我想用中文" 或 "I prefer English"');
      console.error('============================================================');
      process.exit(1);
    }

    const t = getTemplates(lang);

    console.log(lang === 'zh' ? '🔄 录入任务:' : '🔄 Adding task:', config.task);

    // 【重要】首次录入检测：写入前先统计当前任务数
    const existingResult = await apiGet(`/bitable/v1/apps/${CONFIG.APP_TOKEN}/tables/${CONFIG.TABLE_ID}/records`);
    const existingCount = existingResult.data?.items?.length || 0;


    const result = await addTask(config);


    if (result.code === 0) {
      console.log(t.confirm.insertSuccess);
      console.log(format(t.confirm.recordId, { id: result.data?.record?.record_id }));

      // 【强制】首条任务录入成功后，自动创建定时提醒（仅执行一次）
      if (existingCount === 0 && !isReminderSetupDone()) {
        await autoSetupReminders(lang);
      }
    } else {
      console.error(format(t.confirm.insertFailed, { msg: result.msg }));
      process.exit(1);
    }
  } catch (error) {
    const lang = getLanguage();
    const t = getTemplates(lang);
    console.error(format(t.confirm.insertFailed, { msg: error.response?.data?.msg || error.message }));
    process.exit(1);
  }
}

main();