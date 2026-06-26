/**
 * 读取飞书多维表格任务列表
 * 用法: node list_tasks.js
 * 
 * 根据用户语言偏好，输出格式化后的任务列表
 */

const { apiGet } = require('./request');
const { CONFIG } = require('./config');
const { getLanguage, getTemplates, format } = require('./i18n');

// 中文字段 → 英文字段映射（用于英文模式）
const FIELD_MAP_ZH_TO_EN = {
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

// 中文状态值 → 英文状态值映射
const STATUS_MAP = {
  '待办': 'To Do',
  '进行中': 'In Progress',
  '已完成': 'Done',
  '取消': 'Cancelled'
};

// 中文优先级值 → 英文优先级值映射
const PRIORITY_MAP = {
  '①紧急且重要': '① Urgent and Important',
  '②重要不紧急': '② Not Urgent but Important',
  '③紧急不重要': '③ Urgent but Not Important',
  '④不紧急不重要': '④ Not Urgent and Not Important'
};

function translateFieldValue(key, value, lang) {
  if (!value) return value;
  
  if (lang === 'en') {
    if (key === '状态' && STATUS_MAP[value]) return STATUS_MAP[value];
    if (key === '优先级' && PRIORITY_MAP[value]) return PRIORITY_MAP[value];
  }
  
  return value;
}

function formatDate(dateStr, lang) {
  if (!dateStr) return '-';
  const date = new Date(dateStr);
  if (lang === 'zh') {
    return date.toLocaleDateString('zh-CN');
  } else {
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
  }
}

async function main() {
  try {
    const lang = getLanguage();
    const t = getTemplates(lang);

    console.log(lang === 'zh' ? '🔄 获取任务列表...' : '🔄 Fetching task list...');
    
    const result = await apiGet(`/bitable/v1/apps/${CONFIG.APP_TOKEN}/tables/${CONFIG.TABLE_ID}/records`);
    
    if (result.code === 0) {
      const items = result.data?.items || [];
      const count = items.length;
      
      if (lang === 'zh') {
        console.log(`\n📋 任务列表 (共 ${count} 条):\n`);
      } else {
        console.log(`\n${format(t.listTasks.header, { count })}`);
      }
      
      if (items.length === 0) {
        console.log(`   ${t.listTasks.empty}`);
      }
      
      items.forEach((item, index) => {
        const f = item.fields;
        const name = f['任务名称'] || f['Task Name'] || '(无标题)' || '(No title)';
        const source = translateFieldValue('来源分类', f['来源分类'] || f['Source Category'], lang);
        const priority = translateFieldValue('优先级', f['优先级'] || f['Priority'], lang);
        const status = translateFieldValue('状态', f['状态'] || f['Status'], lang);
        const deadline = formatDate(f['截止日期'] || f['Deadline'], lang);
        const duration = f['预计时长'] || f['Estimated Time'] || '-';
        const start = f['开始时间'] || f['Start Time'] || '-';
        const requirement = f['工作要求'] || f['Requirements'] || '';
        const stakeholder = f['干系人'] || f['Stakeholder'] || '';
        const issues = f['存在问题'] || f['Issues'] || '';
        const notes = f['备注'] || f['Notes'] || '';

        if (lang === 'zh') {
          console.log(`${index + 1}. ${name}`);
          console.log(`   来源: ${source} | 优先级: ${priority} | 状态: ${status}`);
          console.log(`   截止: ${deadline} | 时长: ${duration} | 开始: ${start}`);
          if (requirement) console.log(`   工作要求: ${requirement}`);
          if (stakeholder) console.log(`   干系人: ${stakeholder}`);
          if (issues) console.log(`   存在问题: ${issues}`);
          if (notes) console.log(`   备注: ${notes}`);
          console.log(`   ID: ${item.record_id}\n`);
        } else {
          console.log(format(t.listTasks.item, { index: index + 1, name }));
          console.log(format(t.listTasks.details, { source, priority, status }));
          console.log(format(t.listTasks.deadline, { deadline, duration, start }));
          if (requirement) console.log(format(t.listTasks.requirement, { req: requirement }));
          if (stakeholder) console.log(format(t.listTasks.stakeholder, { stakeholder }));
          if (issues) console.log(format(t.listTasks.issues, { issues }));
          if (notes) console.log(format(t.listTasks.notes, { notes }));
          console.log(format(t.listTasks.id, { id: item.record_id }) + '\n');
        }
      });
    } else {
      const errMsg = lang === 'zh' ? `❌ 获取失败: ${result.msg}` : `❌ Fetch failed: ${result.msg}`;
      console.error(errMsg);
      process.exit(1);
    }
  } catch (error) {
    const lang = getLanguage();
    const errMsg = lang === 'zh' ? `❌ 错误: ${error.response?.data?.msg || error.message}` : `❌ Error: ${error.response?.data?.msg || error.message}`;
    console.error(errMsg);
    process.exit(1);
  }
}

main();