/**
 * SENSEN Task Manager - Phase 2
 * 任务状态机 + 持久化 + 超时提醒
 * 
 * 状态流转: Inbox → Planning → Executing → Review → Done | Failed
 * 
 * P0-1 升级: 使用 TaskStore 内存缓存层
 */

const fs = require('fs');
const path = require('path');
const { TaskStore } = require('./task-store');

const TASKS_DIR = path.join(__dirname, 'tasks');

// 状态定义
const TaskState = {
  INBOX: 'inbox',           // 新任务，待处理
  PLANNING: 'planning',     // 规划中
  EXECUTING: 'executing',   // 执行中
  REVIEW: 'review',         // 待审核
  DONE: 'done',             // 已完成
  FAILED: 'failed'          // 失败
};

// 超时配置（分钟）
const TIMEOUT_CONFIG = {
  inbox: 30,        // Inbox 超过30分钟未处理 → 提醒
  planning: 60,    // Planning 超过60分钟未完成 → 警告
  executing: 120,  // Executing 超过2小时 → 检查
  review: 60       // Review 超过60分钟 → 确认
};

// 初始化 TaskStore 单例
let _store = null;
function getStore() {
  if (!_store) {
    _store = new TaskStore();
  }
  return _store;
}

/**
 * 创建新任务
 * @param {Object} taskData - 任务数据
 * @returns {Object} 创建的任务对象
 */
function createTask(taskData) {
  return getStore().create(taskData);
}

/**
 * 更新任务状态
 * @param {string} taskId - 任务ID
 * @param {string} newState - 新状态
 * @param {Object} extra - 额外数据
 */
function updateTaskState(taskId, newState, extra = {}) {
  const task = getStore().get(taskId);
  if (!task) {
    console.error(`[TaskManager] ❌ 任务不存在: ${taskId}`);
    return null;
  }
  
  const oldState = task.status;
  
  // 状态转换验证
  if (!isValidTransition(oldState, newState)) {
    console.error(`[TaskManager] ❌ 无效转换: ${oldState} → ${newState}`);
    return null;
  }
  
  const updates = { status: newState, ...extra };
  const updated = getStore().update(taskId, updates);
  console.log(`[TaskManager] 📍 状态更新: ${taskId} ${oldState} → ${newState}`);
  
  return updated;
}

/**
 * 验证状态转换是否合法
 */
function isValidTransition(from, to) {
  const transitions = {
    [TaskState.INBOX]: [TaskState.PLANNING, TaskState.EXECUTING, TaskState.FAILED],
    [TaskState.PLANNING]: [TaskState.EXECUTING, TaskState.FAILED],
    [TaskState.EXECUTING]: [TaskState.REVIEW, TaskState.FAILED],
    [TaskState.REVIEW]: [TaskState.DONE, TaskState.EXECUTING, TaskState.FAILED],
    [TaskState.DONE]: [],
    [TaskState.FAILED]: [TaskState.INBOX]  // 可以重新打开
  };
  
  return transitions[from]?.includes(to) || false;
}

/**
 * 获取所有任务
 */
function getAllTasks() {
  return getStore().getAll().sort((a, b) => {
    const priorityOrder = { P0: 0, P1: 1, P2: 2, P3: 3 };
    if (priorityOrder[a.priority] !== priorityOrder[b.priority]) {
      return priorityOrder[a.priority] - priorityOrder[b.priority];
    }
    return new Date(b.createdAt) - new Date(a.createdAt);
  });
}

/**
 * 按状态获取任务
 */
function getTasksByStatus(status) {
  return getStore().getByStatus(status);
}

/**
 * 加载单个任务
 */
function loadTask(taskId) {
  return getStore().get(taskId);
}

/**
 * 保存任务到文件（保留用于兼容）
 */
function saveTask(task) {
  getStore().update(task.id, task);
}

/**
 * 删除任务
 */
function deleteTask(taskId) {
  return getStore().delete(taskId);
}

/**
 * 检查任务超时
 * @returns {Array} 超时任务列表
 */
function checkTimeouts() {
  const alerts = getStore().checkTimeouts(TIMEOUT_CONFIG);
  
  // 更新超时计数
  for (const alert of alerts) {
    const task = getStore().get(alert.taskId);
    if (task) {
      getStore().update(alert.taskId, {
        timeoutCount: (task.timeoutCount || 0) + 1,
        alerts: [...(task.alerts || []), {
          type: 'timeout',
          message: `${alert.status}状态已超过${alert.elapsedMinutes}分钟`,
          at: new Date().toISOString()
        }]
      });
    }
  }
  
  return alerts;
}

/**
 * 获取任务统计
 */
function getStats() {
  return getStore().getStats();
}

/**
 * 打印任务看板
 */
function printKanban() {
  const tasks = getAllTasks();
  const byStatus = {};
  
  for (const state of Object.values(TaskState)) {
    byStatus[state] = tasks.filter(t => t.status === state);
  }
  
  console.log('\n📋 SENSEN Task Kanban');
  console.log('═══════════════════════════════════════════════════════════════');
  
  for (const [state, stateTasks] of Object.entries(byStatus)) {
    if (stateTasks.length === 0) continue;
    
    const stateLabel = {
      inbox: '📥 Inbox',
      planning: '📐 Planning',
      executing: '⚡ Executing',
      review: '👀 Review',
      done: '✅ Done',
      failed: '❌ Failed'
    }[state] || state;
    
    console.log(`\n${stateLabel} (${stateTasks.length})`);
    console.log('───────────────────────────────────────────────────────────────');
    
    for (const task of stateTasks) {
      const elapsed = Math.round((Date.now() - new Date(task.stateChangedAt)) / 1000 / 60);
      const timeout = TIMEOUT_CONFIG[task.status] || 120;
      const timeIndicator = elapsed > timeout ? ' ⚠️' : '';
      
      console.log(`  [${task.priority}] ${task.id.slice(-8)} | ${task.title}${timeIndicator}`);
      if (task.assignedTo) console.log(`         → @${task.assignedTo}`);
    }
  }
  
  console.log('\n═══════════════════════════════════════════════════════════════');
  
  const stats = getStats();
  console.log(`总计: ${stats.total} | 超时任务: ${stats.timeouts}`);
  console.log('');
}

// 导出模块
module.exports = {
  TaskState,
  TaskStore,
  createTask,
  updateTaskState,
  getAllTasks,
  getTasksByStatus,
  loadTask,
  deleteTask,
  checkTimeouts,
  getStats,
  printKanban,
  TASKS_DIR,
  getStore  // 导出获取store的方法
};
