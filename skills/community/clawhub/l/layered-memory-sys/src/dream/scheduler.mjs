// scheduler.mjs - 内置调度器 (v2.0)
// 轻量 cron 实现

import { execDreamCycle } from './dream-cycle.mjs';
import { getDueReminders, updateMemory } from '../db/repository.mjs';

let _jobs = new Map();
let _intervalId = null;

// cron 解析（简化版，支持: * * * * * 格式）
function parseCron(expr) {
  const parts = expr.split(/\s+/);
  if (parts.length !== 5) return null;

  const [min, hour, dayOfMonth, month, dayOfWeek] = parts;

  return {
    minute: parseField(min, 0, 59),
    hour: parseField(hour, 0, 23),
    dayOfMonth: parseField(dayOfMonth, 1, 31),
    month: parseField(month, 1, 12),
    dayOfWeek: parseField(dayOfWeek, 0, 6),
  };
}

function parseField(field, min, max) {
  if (field === '*') return null; // any
  if (field.includes(',')) {
    return field.split(',').map(n => parseInt(n));
  }
  if (field.includes('/')) {
    const [, step] = field.split('/');
    return { step: parseInt(step), min, max };
  }
  return [parseInt(field)];
}

function matchesField(parsed, value) {
  if (!parsed) return true;
  if (Array.isArray(parsed)) return parsed.includes(value);
  if (parsed.step) return (value - parsed.min) % parsed.step === 0;
  return false;
}

// 检查是否匹配当前时间
function matchesCron(parsed, date) {
  return matchesField(parsed.minute, date.getMinutes())
    && matchesField(parsed.hour, date.getHours())
    && matchesField(parsed.dayOfMonth, date.getDate())
    && matchesField(parsed.month, date.getMonth() + 1)
    && matchesField(parsed.dayOfWeek, date.getDay());
}

// 启动调度器
export function startScheduler(config) {
  if (_intervalId) return false;

  const jobs = config?.scheduler?.jobs || [
    { id: 'dream-cycle', cron: '0 3 * * *', handler: 'dreamCycle' },
    { id: 'remind-check', cron: '* * * * *', handler: 'checkReminders' },
  ];

  for (const job of jobs) {
    const parsed = parseCron(job.cron);
    if (parsed) {
      _jobs.set(job.id, { ...job, parsed });
      console.log(`⏰ 已注册任务: ${job.id} (${job.cron})`);
    }
  }

  // 每分钟检查一次
  _intervalId = setInterval(() => {
    const now = new Date();
    for (const [id, job] of _jobs) {
      if (matchesCron(job.parsed, now)) {
        executeJob(job, config).catch(e => {
          console.error(`任务 ${id} 执行失败:`, e.message);
        });
      }
    }
  }, 60 * 1000);

  console.log('✅ 调度器已启动');
  return true;
}

// 停止调度器
export function stopScheduler() {
  if (_intervalId) {
    clearInterval(_intervalId);
    _intervalId = null;
    _jobs.clear();
    console.log('🛑 调度器已停止');
  }
}

// 执行任务
async function executeJob(job, config) {
  console.log(`⏰ 执行任务: ${job.id}`);

  switch (job.handler) {
    case 'dreamCycle':
      await execDreamCycle(config);
      break;
    case 'checkReminders':
      await checkReminders(config);
      break;
    case 'statsSnapshot':
      // TODO: 生成统计快照
      break;
    default:
      console.warn(`未知任务处理器: ${job.handler}`);
  }
}

// 检查提醒
async function checkReminders(config) {
  const due = getDueReminders();

  for (const reminder of due) {
    // 发送通知
    if (config?.reminder?.callback) {
      await config.reminder.callback(reminder);
    } else {
      // 默认：打印到控制台
      console.log(`🔔 提醒: ${reminder.title} (${reminder.summary})`);
    }

    // 标记为已完成
    updateMemory(reminder.id, { status: 'completed' });
  }

  return due.length;
}

// 手动触发任务
export async function runJob(jobId, config) {
  const job = _jobs.get(jobId);
  if (!job) throw new Error(`任务不存在: ${jobId}`);
  await executeJob(job, config);
}

// 获取任务列表
export function listJobs() {
  return Array.from(_jobs.values()).map(j => ({
    id: j.id, cron: j.cron, handler: j.handler,
  }));
}