#!/usr/bin/env node
/**
 * Long Task Manager - 长任务管理器
 * 
 * 提供任务队列管理、进度追踪、状态持久化功能
 */

const fs = require('fs');
const path = require('path');

const STATE_FILE = path.join(__dirname, 'task-state.json');

class TaskManager {
  constructor() {
    this.tasks = new Map();
    this.queue = [];
    this.loadState();
  }

  loadState() {
    try {
      if (fs.existsSync(STATE_FILE)) {
        const data = JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
        this.tasks = new Map(Object.entries(data.tasks || {}));
        this.queue = data.queue || [];
      }
    } catch (e) {
      console.error('Failed to load task state:', e);
    }
  }

  saveState() {
    try {
      const data = {
        tasks: Object.fromEntries(this.tasks),
        queue: this.queue
      };
      fs.writeFileSync(STATE_FILE, JSON.stringify(data, null, 2));
    } catch (e) {
      console.error('Failed to save task state:', e);
    }
  }

  /**
   * 注册新任务
   */
  register(sessionId, options) {
    const task = {
      sessionId,
      status: 'running',
      createdAt: Date.now(),
      updatedAt: Date.now(),
      command: options.command,
      estimatedDuration: options.estimatedDuration,
      pollInterval: options.pollInterval || 30000,
      lastOutput: '',
      exitCode: null,
      timedOut: false,
      ...options
    };

    this.tasks.set(sessionId, task);
    this.saveState();
    return task;
  }

  /**
   * 更新任务状态
   */
  update(sessionId, updates) {
    const task = this.tasks.get(sessionId);
    if (!task) return null;

    Object.assign(task, updates, { updatedAt: Date.now() });
    
    if (updates.exitCode !== null || updates.timedOut) {
      task.status = updates.exitCode === 0 ? 'completed' : 'failed';
      task.completedAt = Date.now();
    }

    this.saveState();
    return task;
  }

  /**
   * 获取任务状态
   */
  get(sessionId) {
    return this.tasks.get(sessionId);
  }

  /**
   * 列出所有任务
   */
  list(options = {}) {
    const { status, limit = 20 } = options;
    
    let tasks = Array.from(this.tasks.values());
    
    if (status) {
      tasks = tasks.filter(t => t.status === status);
    }

    // 按创建时间倒序
    tasks.sort((a, b) => b.createdAt - a.createdAt);
    
    return tasks.slice(0, limit);
  }

  /**
   * 获取运行中的任务数
   */
  getRunningCount() {
    return Array.from(this.tasks.values())
      .filter(t => t.status === 'running').length;
  }

  /**
   * 添加到队列
   */
  enqueue(taskInfo) {
    const item = {
      id: `task_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
      status: 'queued',
      queuedAt: Date.now(),
      ...taskInfo
    };
    
    this.queue.push(item);
    this.saveState();
    return item;
  }

  /**
   * 从队列取出下一个任务
   */
  dequeue() {
    const item = this.queue.shift();
    if (item) {
      this.saveState();
    }
    return item;
  }

  /**
   * 获取队列状态
   */
  getQueueStatus() {
    return {
      queued: this.queue.length,
      running: this.getRunningCount(),
      next: this.queue[0] || null
    };
  }

  /**
   * 清理旧任务 (保留最近 24 小时)
   */
  cleanup(retainHours = 24) {
    const cutoff = Date.now() - (retainHours * 60 * 60 * 1000);
    let cleaned = 0;

    for (const [sessionId, task] of this.tasks) {
      if (task.completedAt && task.completedAt < cutoff) {
        this.tasks.delete(sessionId);
        cleaned++;
      }
    }

    if (cleaned > 0) {
      this.saveState();
    }

    return cleaned;
  }

  /**
   * 终止任务
   */
  async kill(sessionId) {
    const task = this.tasks.get(sessionId);
    if (!task) return { success: false, error: 'Task not found' };

    try {
      // 这里需要调用 process kill 工具
      // 由于这是技能脚本，实际 kill 操作由 agent 执行
      return {
        success: true,
        message: `Task ${sessionId} marked for termination`
      };
    } catch (e) {
      return { success: false, error: e.message };
    }
  }

  /**
   * 获取任务日志摘要
   */
  summarize(sessionId) {
    const task = this.tasks.get(sessionId);
    if (!task) return null;

    const duration = task.completedAt 
      ? task.completedAt - task.createdAt 
      : Date.now() - task.createdAt;

    return {
      sessionId,
      command: task.command,
      status: task.status,
      duration: formatDuration(duration),
      createdAt: new Date(task.createdAt).toISOString(),
      completedAt: task.completedAt ? new Date(task.completedAt).toISOString() : null,
      exitCode: task.exitCode,
      timedOut: task.timedOut
    };
  }
}

function formatDuration(ms) {
  const seconds = Math.floor(ms / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);

  if (hours > 0) {
    return `${hours}h ${minutes % 60}m ${seconds % 60}s`;
  } else if (minutes > 0) {
    return `${minutes}m ${seconds % 60}s`;
  } else {
    return `${seconds}s`;
  }
}

// CLI 接口
if (require.main === module) {
  const manager = new TaskManager();
  const command = process.argv[2];

  switch (command) {
    case 'list':
      console.log(JSON.stringify(manager.list(), null, 2));
      break;
    case 'queue':
      console.log(JSON.stringify(manager.getQueueStatus(), null, 2));
      break;
    case 'cleanup':
      const cleaned = manager.cleanup();
      console.log(`Cleaned up ${cleaned} old tasks`);
      break;
    default:
      console.log('Usage: task-manager.js <list|queue|cleanup>');
  }
}

module.exports = TaskManager;
