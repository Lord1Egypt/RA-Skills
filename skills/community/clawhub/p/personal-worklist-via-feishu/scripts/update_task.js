/**
 * 更新任务到飞书多维表格
 * 用法:
 *   node update_task.js --record-id "recxxx" --status "已完成" [--lang zh]
 *   node update_task.js --record-id "recxxx" --status "Cancelled" --lang en
 *   node update_task.js --record-id "recxxx" --deadline "2026-04-25" [--lang zh]
 *   node update_task.js --record-id "recxxx" --problem "具体阻碍描述" [--lang zh]
 *   node update_task.js --record-id "recxxx" --notes "备注内容" [--lang zh]
 *   node update_task.js --record-id "recxxx" --start "2026-04-23"
 *   node update_task.js --record-id "recxxx" --duration "3h"
 *   node update_task.js --record-id "recxxx" --stakeholders "张三,李四"
 *   # 可组合使用：
 *   node update_task.js --record-id "recxxx" --status "进行中" --problem "超时了" --lang zh
 */

const { apiPut } = require('./request');
const { CONFIG } = require('./config');
const { getLanguage, getTemplates, format } = require('./i18n');

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

// 相对日期转换为具体日期（禁止写入"今天/明天/后天"等模糊词）
function parseRelativeDate(dateStr) {
  if (!dateStr || typeof dateStr !== 'string') return dateStr;
  
  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const lower = dateStr.toLowerCase();
  
  if (lower === '今天' || lower === 'today') return formatDateStr(today);
  if (lower === '明天' || lower === 'tomorrow') {
    const d = new Date(today); d.setDate(d.getDate() + 1); return formatDateStr(d);
  }
  if (lower === '后天' || lower === 'day after tomorrow') {
    const d = new Date(today); d.setDate(d.getDate() + 2); return formatDateStr(d);
  }
  
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
  
  const weekMatch = lower.match(/^本周([一二三四五六日天])/);
  if (weekMatch) {
    const dayMap = { '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '日': 7, '天': 7 };
    const targetWeekday = dayMap[weekMatch[1]];
    const currentWeekday = today.getDay() || 7;
    let diff = targetWeekday - currentWeekday;
    if (diff <= 0) diff += 7;
    const targetDay = new Date(today);
    targetDay.setDate(targetDay.getDate() + diff);
    return formatDateStr(targetDay);
  }
  
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
  
  return dateStr;
}

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

// 优先级中英对照
const PRIORITY_MAP = {
  '①紧急且重要': '① Urgent and Important',
  '②重要不紧急': '② Not Urgent but Important',
  '③紧急不重要': '③ Urgent but Not Important',
  '④不紧急不重要': '④ Not Urgent and Not Important',
  '① Urgent and Important': '① Urgent and Important',
  '② Not Urgent but Important': '② Not Urgent but Important',
  '③ Urgent but Not Important': '③ Urgent but Not Important',
  '④ Not Urgent and Not Important': '④ Not Urgent and Not Important'
};

// 状态中英对照
const STATUS_MAP = {
  '待办': 'To Do',
  '进行中': 'In Progress',
  '已完成': 'Done',
  '取消': 'Cancelled',
  'To Do': 'To Do',
  'In Progress': 'In Progress',
  'Done': 'Done',
  'Cancelled': 'Cancelled'
};

// 获取多维表格实际字段名（根据语言）
function getFieldName(zhName, lang) {
  if (lang === 'en') {
    return FIELD_NAME_MAP[zhName] || zhName;
  }
  return zhName;
}

// 转换字段值（优先级/状态）- 中文模式直接返回原值，不再翻译
function translateFieldValue(fieldName, value, lang) {
  return value;
}

async function updateTask(config) {
  if (!config['record-id']) {
    const lang = config.lang || getLanguage();
    const t = getTemplates(lang);
    console.error(lang === 'zh' ? '❌ record-id 不能为空' : '❌ record-id is required');
    console.error(lang === 'zh' ? `   用法: node update_task.js --record-id "recxxx" --status "已完成"` : `   Usage: node update_task.js --record-id "recxxx" --status "Done"`);
    process.exit(1);
  }

  const lang = config.lang || getLanguage();
  const fields = {};

  // 状态字段
  if (config.status) {
    const fieldName = getFieldName('状态', lang);
    const translatedValue = translateFieldValue('状态', config.status, lang);
    fields[fieldName] = translatedValue;
  }

  // 截止日期字段（相对日期转换）
  if (config.deadline) {
    const parsedDeadline = parseRelativeDate(config.deadline);
    const date = new Date(parsedDeadline);
    date.setHours(0, 0, 0, 0);
    const fieldName = getFieldName('截止日期', lang);
    fields[fieldName] = date.getTime();
  }

  // 备注字段
  if (config.notes) {
    const fieldName = getFieldName('备注', lang);
    fields[fieldName] = config.notes;
  }

  // 工作要求字段
  if (config.requirements) {
    const fieldName = getFieldName('工作要求', lang);
    fields[fieldName] = config.requirements;
  }

  // 存在问题字段
  if (config.problem) {
    const fieldName = getFieldName('存在问题', lang);
    fields[fieldName] = config.problem;
  }

  // 干系人字段
  if (config.stakeholders) {
    const fieldName = getFieldName('干系人', lang);
    fields[fieldName] = config.stakeholders;
  }

  // 开始时间字段（相对日期转换）
  if (config.start) {
    const parsedStart = parseRelativeDate(config.start);
    const startDate = new Date(parsedStart);
    startDate.setHours(0, 0, 0, 0);
    const fieldName = getFieldName('开始时间', lang);
    fields[fieldName] = startDate.getTime();
  }

  // 预计时长字段
  if (config.duration) {
    const fieldName = getFieldName('预计时长', lang);
    fields[fieldName] = config.duration;
  }

  const result = await apiPut(
    `/bitable/v1/apps/${CONFIG.APP_TOKEN}/tables/${CONFIG.TABLE_ID}/records/${config['record-id']}`,
    { fields }
  );

  return result;
}

async function main() {
  try {
    const config = parseArgs();
    const lang = config.lang || getLanguage();
    const t = getTemplates(lang);

    console.log(lang === 'zh' ? '🔄 更新任务:' : '🔄 Updating task:', config['record-id']);
    const result = await updateTask(config);

    if (result.code === 0) {
      console.log(t.confirm.updateSuccess);
    } else {
      console.error(format(t.confirm.updateFailed, { msg: result.msg }));
      process.exit(1);
    }
  } catch (error) {
    const lang = getLanguage();
    const t = getTemplates(lang);
    console.error(format(t.confirm.updateFailed, { msg: error.response?.data?.msg || error.message }));
    process.exit(1);
  }
}

main();