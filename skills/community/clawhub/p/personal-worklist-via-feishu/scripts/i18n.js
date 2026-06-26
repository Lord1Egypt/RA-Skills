/**
 * 国际化文本模板
 * 用于定时提醒的文本输出
 */

const I18N = {
  // ==================== 早晨提醒 ====================
  zh: {
    morning: {
      greeting: '早呀～花半小时处理邮件和OA，理清今日待办，以最佳状态开启今天！',
      urgentTitle: '今日重点（紧急且重要 × {count}）：',
      taskItem: '• {name} | 优先级：{priority} | 截止：{deadline}',
      noUrgent: '今日暂无紧急且重要的任务',
      inProgressTitle: '进行中/待办任务（{count} 项）：',
      tableHeader: '任务名 | 状态 | 截止 | 优先级',
      tableRow: '{name} | {status} | {deadline} | {priority}',
      suggestion: '建议时间安排：先抽 30 分钟处理 OA待办审批、工作邮件处理，再补充/更新当日工作清单，之后根据任务紧急程度推进。'
    },
    afternoon: {
      greeting: '下午好～开始前建议先花半小时清一下邮件和待办，理顺思路，下午工作更顺～',
      urgentTitle: '今日重点（紧急且重要 × {count}）：',
      taskItem: '• {name} | 优先级：{priority} | 截止：{deadline}',
      noUrgent: '今日暂无紧急且重要的任务',
      inProgressTitle: '进行中/待办任务（{count} 项）：',
      suggestion: '建议时间安排：先抽 30 分钟处理 OA待办审批、工作邮件处理，再补充/更新当日工作清单，之后根据任务紧急程度推进。'
    },
    review: {
      intro: '下午好！开始今日进度复盘——',
      completionRate: '📊 今日完成率：今日工作清单共 {total} 项（截止日期为今天），完成 {done} 项，完成率 {rate}%。',
      uncompletedTitle: '📋 未完成任务（截止日期为今天）：',
      taskItem: '{index}. {name} — 状态：{status}。处理方式：{action}',
      noUncompleted: '今日已全部完成，棒棒的 🎉',
      obstaclesPrompt: '🔍 阻碍分析：以上未完成任务中，存在哪些问题或阻碍？请告诉我，我来帮你分析并填写记录。',
      tomorrowPreview: '⏰ 明日预告：明天重要且紧急的工作是 {tasks}，建议优先处理。',
      noTomorrow: '明日暂无紧急重要的任务。'
    },
    status: {
      todo: '待办',
      inProgress: '进行中',
      done: '已完成',
      cancelled: '取消'
    },
    priority: {
      urgent: '①紧急且重要',
      important: '②重要不紧急',
      urgentLess: '③紧急不重要',
      normal: '④不紧急不重要'
    },
    source: {
      planned: '计划任务[P]',
      urgent: '临时任务[U]',
      routine: '例行任务[R]',
      collab: '协作任务[C]'
    },
    listTasks: {
      header: '📋 任务列表 (共 {count} 条)：\n',
      empty: '(暂无任务记录)',
      item: '{index}. {name}',
      details: '   来源: {source} | 优先级: {priority} | 状态: {status}',
      deadline: '   截止: {deadline} | 时长: {duration} | 开始: {start}',
      requirement: '   工作要求: {req}',
      stakeholder: '   干系人: {stakeholder}',
      issues: '   存在问题: {issues}',
      notes: '   备注: {notes}',
      id: '   ID: {id}'
    },
    confirm: {
      insertSuccess: '✅ 录入成功！',
      recordId: 'record_id: {id}',
      insertFailed: '❌ 录入失败: {msg}',
      updateSuccess: '✅ 更新成功！',
      updateFailed: '❌ 更新失败: {msg}'
    },
    initTable: {
      checking: '🔄 初始化多维表格...',
      step1: '📋 Step 1: 检查表格...',
      tableNotFound: '⚠️  表格不存在，正在创建...',
      tableCreated: '✅ 表格创建成功，ID: {id}',
      tableCreationFailed: '❌ 表格创建失败: {msg}',
      tableExists: '✅ 表格已存在',
      step2: '📋 Step 2: 检查字段...',
      existingFields: '   已有的字段 ({count}): {fields}',
      step3: '📋 Step 3: 创建缺失的字段...',
      fieldExists: '   ✓ {name} (已存在)',
      fieldCreating: '   + {name} (创建中...)',
      fieldCreated: '   ✅ {name} 创建成功',
      fieldFailed: '   ❌ {name} 创建失败: {msg}',
      reportTitle: '\n📊 初始化完成报告：',
      reportTable: '   表格: {status}, ID: {id}',
      reportNew: '   本次新增字段: {fields}',
      reportFailed: '   失败字段: {fields}',
      manualCreate: '\n💡 请在飞书中手动创建以下字段：',
      complete: '\n✅ 多维表格初始化完成！',
      ready: '   现在可以开始使用任务管理功能了。'
    },
    permission: {
      adding: '🔄 正在为您添加多维表格编辑权限...',
      success: '权限添加成功',
      failed: '权限添加失败',
      error: '权限添加异常',
      closed: '\n✅ 权限配置完成，台账已就绪！'
    }
  },

  en: {
    morning: {
      greeting: 'Good morning! Start with 30 minutes to handle emails and OA, clear your to-do list, and kick off the day right!',
      urgentTitle: '🔥 Today\'s Focus (Urgent & Important × {count}):',
      taskItem: '• {name} | Priority: {priority} | Deadline: {deadline}',
      noUrgent: 'No urgent & important tasks today',
      inProgressTitle: 'In Progress / To Do ({count} items):',
      tableHeader: 'Task | Status | Deadline | Priority',
      tableRow: '{name} | {status} | {deadline} | {priority}',
      suggestion: 'Suggested schedule: Spend 30 min on OA approvals & emails first, then update your work list. Push forward based on urgency.'
    },
    afternoon: {
      greeting: 'Good afternoon! Before diving in, suggest clearing emails and pending tasks for 30 min to get organized～',
      urgentTitle: '🔥 Today\'s Focus (Urgent & Important × {count}):',
      taskItem: '• {name} | Priority: {priority} | Deadline: {deadline}',
      noUrgent: 'No urgent & important tasks today',
      inProgressTitle: 'In Progress / To Do ({count} items):',
      suggestion: 'Suggested schedule: Spend 30 min on OA approvals & emails first, then update your work list. Push forward based on urgency.'
    },
    review: {
      intro: 'Good afternoon! Let\'s start today\'s review——',
      completionRate: '📊 Completion Rate: {total} tasks due today, {done} completed, {rate}% done.',
      uncompletedTitle: '📋 Uncompleted Tasks (due today):',
      taskItem: '{index}. {name} — Status: {status}. Action: {action}',
      noUncompleted: 'All tasks completed today, great job! 🎉',
      obstaclesPrompt: '🔍 Obstacle Analysis: What issues or blockers do you have for the above uncompleted tasks? Let me know and I\'ll log them.',
      tomorrowPreview: '⏰ Tomorrow\'s Focus: {tasks} are urgent & important tomorrow, prioritize them.',
      noTomorrow: 'No urgent tasks tomorrow.'
    },
    status: {
      todo: 'To Do',
      inProgress: 'In Progress',
      done: 'Done',
      cancelled: 'Cancelled'
    },
    priority: {
      urgent: '① Urgent and Important',
      important: '② Not Urgent but Important',
      urgentLess: '③ Urgent but Not Important',
      normal: '④ Not Urgent and Not Important'
    },
    source: {
      planned: 'Planned[P]',
      urgent: 'Urgent[U]',
      routine: 'Routine[R]',
      collab: 'Collab[C]'
    },
    listTasks: {
      header: '📋 Task List ({count} items):\n',
      empty: '(No tasks yet)',
      item: '{index}. {name}',
      details: '   Source: {source} | Priority: {priority} | Status: {status}',
      deadline: '   Deadline: {deadline} | Duration: {duration} | Start: {start}',
      requirement: '   Requirements: {req}',
      stakeholder: '   Stakeholder: {stakeholder}',
      issues: '   Issues: {issues}',
      notes: '   Notes: {notes}',
      id: '   ID: {id}'
    },
    confirm: {
      insertSuccess: '✅ Task added!',
      recordId: 'record_id: {id}',
      insertFailed: '❌ Insert failed: {msg}',
      updateSuccess: '✅ Update successful!',
      updateFailed: '❌ Update failed: {msg}'
    },
    initTable: {
      checking: '🔄 Initializing bitable...',
      step1: '📋 Step 1: Checking table...',
      tableNotFound: '⚠️  Table not found, creating...',
      tableCreated: '✅ Table created, ID: {id}',
      tableCreationFailed: '❌ Table creation failed: {msg}',
      tableExists: '✅ Table exists',
      step2: '📋 Step 2: Checking fields...',
      existingFields: '   Existing fields ({count}): {fields}',
      step3: '📋 Step 3: Creating missing fields...',
      fieldExists: '   ✓ {name} (exists)',
      fieldCreating: '   + {name} (creating...)',
      fieldCreated: '   ✅ {name} created',
      fieldFailed: '   ❌ {name} failed: {msg}',
      reportTitle: '\n📊 Initialization Report:',
      reportTable: '   Table: {status}, ID: {id}',
      reportNew: '   New fields created: {fields}',
      reportFailed: '   Failed fields: {fields}',
      manualCreate: '\n💡 Please create these fields manually in Feishu:',
      complete: '\n✅ Bitable initialization complete!',
      ready: '   You can now start using the task management.'
    },
    permission: {
      adding: '🔄 Adding bitable edit permission for you...',
      success: 'Permission added successfully',
      failed: 'Permission add failed',
      error: 'Permission add error',
      closed: '\n✅ Permission configured. Your worklist is ready!'
    }
  }
};

/**
 * 获取指定语言的文本模板
 * @param {string} lang - 'zh' 或 'en'
 * @returns {object} 文本模板对象
 */
function getTemplates(lang) {
  return I18N[lang] || I18N.zh;
}

/**
 * 获取用户偏好语言
 * @returns {string} 'zh' 或 'en'
 */
function getLanguage() {
  const preferences = require('./preferences');
  const lang = preferences.getLanguage();
  return lang === 'en' ? 'en' : 'zh';
}

/**
 * 格式化模板字符串
 * @param {string} template - 模板字符串
 * @param {object} data - 填充数据
 * @returns {string} 格式化后的字符串
 */
function format(template, data) {
  let result = template;
  for (const key in data) {
    const regex = new RegExp(`\\{${key}\\}`, 'g');
    result = result.replace(regex, data[key]);
  }
  return result;
}

module.exports = { I18N, getTemplates, getLanguage, format };