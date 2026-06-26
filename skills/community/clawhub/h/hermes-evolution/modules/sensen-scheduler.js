/**
 * SENSEN Task Scheduler - Phase 4.3
 * 定时任务自动触发器
 * 
 * 功能：
 * 1. 读取定时任务配置
 * 2. 到期时自动创建Task → 触发Collaborator → 发送飞书通知
 * 3. 超时检查 → 发送提醒
 * 4. 每日汇总 → 发送日报
 */

const fs = require('fs');
const path = require('path');

// 调度器配置
const SCHEDULER_CONFIG = {
  SCHEDULE_DIR: path.join(__dirname, 'schedules'),
  STATE_FILE: path.join(__dirname, 'scheduler-state.json'),
  CHECK_INTERVAL: 60 * 1000,  // 1分钟检查一次
};

// 任务类型
const TaskType = {
  SCHEDULED: 'scheduled',    // 定时任务
  RECURRING: 'recurring',    // 循环任务
  ONESHOT: 'oneshot'        // 单次任务
};

// 任务状态
const ScheduleStatus = {
  ACTIVE: 'active',
  PAUSED: 'paused',
  COMPLETED: 'completed'
};

/**
 * 初始化调度器目录
 */
function init() {
  if (!fs.existsSync(SCHEDULER_CONFIG.SCHEDULE_DIR)) {
    fs.mkdirSync(SCHEDULER_CONFIG.SCHEDULE_DIR, { recursive: true });
  }
}

/**
 * 加载调度器状态
 */
function loadState() {
  if (!fs.existsSync(SCHEDULER_CONFIG.STATE_FILE)) {
    return {
      lastCheck: null,
      schedules: {},
      completedOneshots: []
    };
  }
  return JSON.parse(fs.readFileSync(SCHEDULER_CONFIG.STATE_FILE, 'utf-8'));
}

/**
 * 保存调度器状态
 */
function saveState(state) {
  state.lastCheck = new Date().toISOString();
  fs.writeFileSync(SCHEDULER_CONFIG.STATE_FILE, JSON.stringify(state, null, 2), 'utf-8');
}

/**
 * 创建定时任务配置
 */
function createSchedule(config) {
  init();
  
  const id = `schedule_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`;
  
  const schedule = {
    id,
    name: config.name,
    description: config.description || '',
    type: config.type || TaskType.RECURRING,
    
    // Cron表达式或时间配置
    cron: config.cron || null,
    time: config.time || null,  // HH:MM 格式
    daysOfWeek: config.daysOfWeek || [1, 2, 3, 4, 5],  // 周一到周五
    
    // 关联的协作ID（可选）
    collaborationId: config.collaborationId || null,
    
    // 创建时触发的任务模板
    taskTemplate: {
      title: config.title || config.name,
      description: config.description || '',
      priority: config.priority || 'P1',
      assignedTo: config.assignedTo || 'CEO'
    },
    
    // 状态
    status: ScheduleStatus.ACTIVE,
    createdAt: new Date().toISOString(),
    lastTriggered: null,
    nextTrigger: calculateNextTrigger(config),
    triggerCount: 0
  };
  
  const filePath = path.join(SCHEDULER_CONFIG.SCHEDULE_DIR, `${id}.json`);
  fs.writeFileSync(filePath, JSON.stringify(schedule, null, 2), 'utf-8');
  
  console.log(`[Scheduler] ✅ 创建定时任务: ${schedule.name}`);
  console.log(`  ID: ${id}`);
  console.log(`  下次触发: ${schedule.nextTrigger}`);
  
  return schedule;
}

/**
 * 计算下次触发时间
 */
function calculateNextTrigger(config) {
  const now = new Date();
  const timeStr = config.time || config.cron;
  
  if (!timeStr) return null;
  
  // 支持 HH:MM 格式
  if (timeStr.includes(':')) {
    const [hours, minutes] = timeStr.split(':').map(Number);
    const next = new Date();
    next.setHours(hours, minutes, 0, 0);
    
    // 如果今天已过，调到明天
    if (next <= now) {
      next.setDate(next.getDate() + 1);
    }
    
    // 检查是否在允许的星期内
    const daysOfWeek = config.daysOfWeek || [1, 2, 3, 4, 5];
    while (!daysOfWeek.includes(next.getDay())) {
      next.setDate(next.getDate() + 1);
    }
    
    return next.toISOString();
  }
  
  return null;
}

/**
 * 获取所有调度任务
 */
function getAllSchedules() {
  init();
  const files = fs.readdirSync(SCHEDULER_CONFIG.SCHEDULE_DIR).filter(f => f.endsWith('.json'));
  
  return files.map(f => {
    const content = fs.readFileSync(path.join(SCHEDULER_CONFIG.SCHEDULE_DIR, f), 'utf-8');
    return JSON.parse(content);
  }).sort((a, b) => {
    // 按下次触发时间排序
    if (!a.nextTrigger && !b.nextTrigger) return 0;
    if (!a.nextTrigger) return 1;
    if (!b.nextTrigger) return -1;
    return new Date(a.nextTrigger) - new Date(b.nextTrigger);
  });
}

/**
 * 检查并触发到期的任务
 */
async function checkAndTrigger(TaskManager, Collaborator, FeishuNotifier) {
  const state = loadState();
  const now = new Date();
  const triggered = [];
  
  for (const schedule of getAllSchedules()) {
    if (schedule.status !== ScheduleStatus.ACTIVE) continue;
    if (!schedule.nextTrigger) continue;
    
    const nextTime = new Date(schedule.nextTrigger);
    
    if (nextTime <= now) {
      console.log(`[Scheduler] 🔔 触发定时任务: ${schedule.name}`);
      
      try {
        // 创建任务
        const task = TaskManager.createTask({
          title: schedule.taskTemplate.title,
          description: schedule.taskTemplate.description,
          source: 'scheduled',
          priority: schedule.taskTemplate.priority,
          assignedTo: schedule.taskTemplate.assignedTo,
          intent: 'scheduled'
        });
        
        // 如果有协作，触发协作
        if (schedule.collaborationId) {
          const collab = Collaborator.loadCollaboration(schedule.collaborationId);
          if (collab) {
            await Collaborator.runCollaboration(collab.id);
          }
        }
        
        // 发送飞书通知
        if (FeishuNotifier) {
          await FeishuNotifier.notifyTaskCreated(task);
        }
        
        // 更新调度状态
        schedule.lastTriggered = now.toISOString();
        schedule.triggerCount++;
        schedule.nextTrigger = calculateNextTrigger(schedule);
        
        const filePath = path.join(SCHEDULER_CONFIG.SCHEDULE_DIR, `${schedule.id}.json`);
        fs.writeFileSync(filePath, JSON.stringify(schedule, null, 2), 'utf-8');
        
        triggered.push(schedule.name);
        
        console.log(`[Scheduler] ✅ 任务触发成功: ${schedule.name}`);
        
      } catch (error) {
        console.error(`[Scheduler] ❌ 任务触发失败: ${schedule.name}`, error.message);
      }
    }
  }
  
  saveState(state);
  return triggered;
}

/**
 * 检查超时任务
 */
async function checkTimeouts(TaskManager, FeishuNotifier) {
  const alerts = TaskManager.checkTimeouts();
  
  if (alerts.length > 0 && FeishuNotifier) {
    console.log(`[Scheduler] ⏰ 检测到 ${alerts.length} 个超时任务`);
    await FeishuNotifier.sendTimeoutSummary(alerts);
  }
  
  return alerts;
}

/**
 * 发送每日汇总
 */
async function sendDailySummary(TaskManager, FeishuNotifier) {
  if (FeishuNotifier) {
    console.log('[Scheduler] 📊 发送每日汇总');
    await TaskManager.sendDailySummary();
  }
}

/**
 * 打印调度状态
 */
function printScheduleStatus() {
  const schedules = getAllSchedules();
  
  console.log('\n📅 SENSEN 定时任务调度');
  console.log('═'.repeat(60));
  
  if (schedules.length === 0) {
    console.log('(暂无定时任务)');
  }
  
  for (const s of schedules) {
    const statusIcon = s.status === ScheduleStatus.ACTIVE ? '✅' : 
                       s.status === ScheduleStatus.PAUSED ? '⏸️' : '✅';
    const nextTime = s.nextTrigger ? 
      new Date(s.nextTrigger).toLocaleString('zh-CN', { 
        month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' 
      }) : 'N/A';
    
    console.log(`${statusIcon} ${s.name}`);
    console.log(`   时间: ${s.time || s.cron}`);
    console.log(`   触发: ${s.triggerCount}次`);
    console.log(`   下次: ${nextTime}`);
    console.log(`   任务: ${s.taskTemplate.title}`);
    console.log('');
  }
  
  console.log('═'.repeat(60));
  
  const state = loadState();
  console.log(`最后检查: ${state.lastCheck || '从未'}`);
}

/**
 * 内置默认定时任务
 */
function getDefaultSchedules() {
  return [
    {
      name: '09:00 小红书热门话题',
      title: '09:00 小红书热门话题汇总',
      description: '每天9点推送5个热门话题到飞书群',
      time: '09:00',
      daysOfWeek: [1, 2, 3, 4, 5],
      priority: 'P0',
      assignedTo: 'Marketing'
    },
    {
      name: '12:00 超级森森觉醒日记',
      title: '12:00 超级森森觉醒日记',
      description: '每天12点推送觉醒日记到飞书群',
      time: '12:00',
      daysOfWeek: [1, 2, 3, 4, 5],
      priority: 'P1',
      assignedTo: 'Marketing'
    },
    {
      name: '16:00 干货教程',
      title: '16:00 干货教程',
      description: '每天16点推送干货教程到飞书群',
      time: '16:00',
      daysOfWeek: [1, 2, 3, 4, 5],
      priority: 'P1',
      assignedTo: 'Marketing'
    },
    {
      name: '20:00 观点思考',
      title: '20:00 观点思考',
      description: '每天20点推送观点思考到飞书群',
      time: '20:00',
      daysOfWeek: [1, 2, 3, 4, 5],
      priority: 'P1',
      assignedTo: 'Marketing'
    },
    {
      name: '健康检查',
      title: 'Gateway健康检查',
      description: '检查Gateway状态、端口可用性、备份执行',
      time: '09:00',
      daysOfWeek: [1, 2, 3, 4, 5],
      priority: 'P0',
      assignedTo: 'CEO'
    },
    {
      name: '23:50 日度汇总',
      title: '23:50 日度汇总',
      description: '各Agent进展汇总，发送日报到飞书',
      time: '23:50',
      daysOfWeek: [1, 2, 3, 4, 5],
      priority: 'P0',
      assignedTo: 'CEO'
    }
  ];
}

/**
 * 初始化默认定时任务
 */
function initDefaultSchedules() {
  const existing = getAllSchedules();
  if (existing.length > 0) {
    console.log(`[Scheduler] 已存在 ${existing.length} 个定时任务，跳过初始化`);
    return;
  }
  
  console.log('[Scheduler] 初始化默认定时任务...');
  const defaults = getDefaultSchedules();
  
  for (const config of defaults) {
    createSchedule(config);
  }
  
  console.log(`[Scheduler] ✅ 已创建 ${defaults.length} 个默认定时任务`);
}

/**
 * 主入口
 */
async function main() {
  const args = process.argv.slice(2);
  
  // 加载依赖模块
  const TaskManager = require('./task-manager');
  const FeishuNotifier = require('./sensen-feishu-notifier');
  const WrappedTM = FeishuNotifier.wrapTaskManagerWithFeishu(TaskManager);
  
  if (args.includes('--status')) {
    printScheduleStatus();
  } else if (args.includes('--init')) {
    initDefaultSchedules();
  } else if (args.includes('--check')) {
    const triggered = await checkAndTrigger(WrappedTM, null, FeishuNotifier);
    if (triggered.length > 0) {
      console.log(`触发了 ${triggered.length} 个任务`);
    } else {
      console.log('没有任务触发');
    }
  } else if (args.includes('--timeout')) {
    await checkTimeouts(WrappedTM, FeishuNotifier);
  } else if (args.includes('--daily')) {
    await sendDailySummary(WrappedTM, FeishuNotifier);
  } else if (args.includes('--all')) {
    // 执行所有检查
    console.log('[Scheduler] 执行所有检查...');
    
    // 1. 检查定时任务
    const triggered = await checkAndTrigger(WrappedTM, null, FeishuNotifier);
    console.log(`触发了 ${triggered.length} 个定时任务`);
    
    // 2. 检查超时
    await checkTimeouts(WrappedTM, FeishuNotifier);
    
    // 3. 检查是否需要发送日报
    const now = new Date();
    if (now.getHours() === 23 && now.getMinutes() >= 50) {
      await sendDailySummary(WrappedTM, FeishuNotifier);
    }
    
    console.log('[Scheduler] ✅ 所有检查完成');
  } else {
    console.log(`
SENSEN Task Scheduler - Phase 4.3
用法:
  --status    查看调度状态
  --init      初始化默认定时任务
  --check     检查并触发到期任务
  --timeout   检查超时任务
  --daily     发送每日汇总
  --all       执行所有检查（用于cron）
`);
  }
}

// 如果直接运行
if (require.main === module) {
  main().catch(console.error);
}

// 导出模块
module.exports = {
  TaskType,
  ScheduleStatus,
  createSchedule,
  getAllSchedules,
  checkAndTrigger,
  checkTimeouts,
  sendDailySummary,
  printScheduleStatus,
  initDefaultSchedules,
  getDefaultSchedules,
  SCHEDULER_CONFIG
};
