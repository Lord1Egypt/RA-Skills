/**
 * TaskStore - P0-1 任务存储升级
 * 混合存储层：内存缓存 + JSON持久化 + 索引加速
 * 
 * 优势：
 * - 热查询在内存完成（O(1)）
 * - 持久化到JSON（便于调试）
 * - 索引文件加速条件查询
 * - 零外部依赖
 * - 100%向后兼容JSON格式
 */

const fs = require('fs');
const path = require('path');

const TASKS_DIR = path.join(__dirname, 'tasks');
const INDEX_FILE = path.join(__dirname, 'task-index.json');

class TaskStore {
  constructor() {
    this.memoryCache = new Map();  // id -> task
    this.statusIndex = {};         // status -> [taskIds]
    this.priorityIndex = {};       // priority -> [taskIds]
    this.assigneeIndex = {};       // assignee -> [taskIds]
    this._dirty = false;
    
    this._loadAll();
  }

  /**
   * 加载所有任务到内存
   */
  _loadAll() {
    if (!fs.existsSync(TASKS_DIR)) {
      fs.mkdirSync(TASKS_DIR, { recursive: true });
      return;
    }

    const files = fs.readdirSync(TASKS_DIR).filter(f => f.endsWith('.json'));
    
    for (const file of files) {
      try {
        const content = fs.readFileSync(path.join(TASKS_DIR, file), 'utf-8');
        const task = JSON.parse(content);
        this._cacheTask(task);
      } catch (e) {
        console.error(`[TaskStore] ❌ 加载失败: ${file}`, e.message);
      }
    }

    console.log(`[TaskStore] ✅ 已加载 ${this.memoryCache.size} 个任务到内存`);
  }

  /**
   * 将任务加入缓存和索引
   */
  _cacheTask(task) {
    this.memoryCache.set(task.id, task);
    
    // 状态索引
    if (!this.statusIndex[task.status]) this.statusIndex[task.status] = [];
    if (!this.statusIndex[task.status].includes(task.id)) {
      this.statusIndex[task.status].push(task.id);
    }
    
    // 优先级索引
    const priority = task.priority || 'P2';
    if (!this.priorityIndex[priority]) this.priorityIndex[priority] = [];
    if (!this.priorityIndex[priority].includes(task.id)) {
      this.priorityIndex[priority].push(task.id);
    }
    
    // 指派人索引
    if (task.assignedTo) {
      if (!this.assigneeIndex[task.assignedTo]) this.assigneeIndex[task.assignedTo] = [];
      if (!this.assigneeIndex[task.assignedTo].includes(task.id)) {
        this.assigneeIndex[task.assignedTo].push(task.id);
      }
    }
  }

  /**
   * 保存任务到文件
   */
  _persistTask(task) {
    const filePath = path.join(TASKS_DIR, `${task.id}.json`);
    fs.writeFileSync(filePath, JSON.stringify(task, null, 2), 'utf-8');
    this._dirty = true;
  }

  /**
   * 创建任务
   */
  create(taskData) {
    const now = new Date();
    const taskId = `task_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`;
    
    const task = {
      id: taskId,
      title: taskData.title || '未命名任务',
      description: taskData.description || '',
      source: taskData.source || 'boss_dm',
      assignedTo: taskData.assignedTo || null,
      status: 'inbox',
      priority: taskData.priority || 'P2',
      intent: taskData.intent || 'unknown',
      subtasks: taskData.subtasks || [],
      createdAt: now.toISOString(),
      updatedAt: now.toISOString(),
      stateChangedAt: now.toISOString(),
      createdBy: taskData.createdBy || 'sensen',
      result: null,
      error: null,
      timeoutCount: 0,
      alerts: []
    };
    
    this._cacheTask(task);
    this._persistTask(task);
    this._saveIndex();
    
    console.log(`[TaskStore] ✅ 创建任务: ${taskId} - ${task.title}`);
    return task;
  }

  /**
   * 获取单个任务
   */
  get(taskId) {
    return this.memoryCache.get(taskId) || null;
  }

  /**
   * 获取所有任务
   */
  getAll() {
    return Array.from(this.memoryCache.values());
  }

  /**
   * 按状态获取任务（使用索引加速）
   */
  getByStatus(status) {
    const ids = this.statusIndex[status] || [];
    return ids.map(id => this.memoryCache.get(id)).filter(Boolean);
  }

  /**
   * 按优先级获取任务
   */
  getByPriority(priority) {
    const ids = this.priorityIndex[priority] || [];
    return ids.map(id => this.memoryCache.get(id)).filter(Boolean);
  }

  /**
   * 按指派人获取任务
   */
  getByAssignee(assignee) {
    const ids = this.assigneeIndex[assignee] || [];
    return ids.map(id => this.memoryCache.get(id)).filter(Boolean);
  }

  /**
   * 更新任务
   */
  update(taskId, updates) {
    const task = this.memoryCache.get(taskId);
    if (!task) return null;
    
    const now = new Date();
    const oldStatus = task.status;
    const oldAssignee = task.assignedTo;
    
    // 应用更新
    Object.assign(task, updates, { updatedAt: now.toISOString() });
    
    // 如果状态变了，更新索引
    if (updates.status && updates.status !== oldStatus) {
      this._removeFromIndex(taskId, 'status', oldStatus);
      this._addToIndex(taskId, 'status', task.status);
      task.stateChangedAt = now.toISOString();
    }
    
    // 如果指派人变了，更新索引
    if (updates.assignedTo !== undefined && updates.assignedTo !== oldAssignee) {
      if (oldAssignee) this._removeFromIndex(taskId, 'assignee', oldAssignee);
      if (updates.assignedTo) this._addToIndex(taskId, 'assignee', updates.assignedTo);
    }
    
    // 如果优先级变了，更新索引
    if (updates.priority && updates.priority !== task.priority) {
      this._removeFromIndex(taskId, 'priority', task.priority);
      this._addToIndex(taskId, 'priority', updates.priority);
    }
    
    this._persistTask(task);
    this._saveIndex();
    
    return task;
  }

  /**
   * 删除任务
   */
  delete(taskId) {
    const task = this.memoryCache.get(taskId);
    if (!task) return false;
    
    // 从所有索引移除
    this._removeFromIndex(taskId, 'status', task.status);
    this._removeFromIndex(taskId, 'priority', task.priority);
    if (task.assignedTo) this._removeFromIndex(taskId, 'assignee', task.assignedTo);
    
    // 从内存移除
    this.memoryCache.delete(taskId);
    
    // 删除文件
    const filePath = path.join(TASKS_DIR, `${taskId}.json`);
    if (fs.existsSync(filePath)) fs.unlinkSync(filePath);
    
    this._saveIndex();
    console.log(`[TaskStore] 🗑️ 删除任务: ${taskId}`);
    return true;
  }

  /**
   * 复杂查询（支持多个条件）
   */
  query(filters = {}) {
    let results = this.getAll();
    
    if (filters.status) {
      results = results.filter(t => t.status === filters.status);
    }
    if (filters.priority) {
      results = results.filter(t => t.priority === filters.priority);
    }
    if (filters.assignedTo) {
      results = results.filter(t => t.assignedTo === filters.assignedTo);
    }
    if (filters.intent) {
      results = results.filter(t => t.intent === filters.intent);
    }
    if (filters.source) {
      results = results.filter(t => t.source === filters.source);
    }
    if (filters.minTimeoutCount) {
      results = results.filter(t => (t.timeoutCount || 0) >= filters.minTimeoutCount);
    }
    
    // 排序
    if (filters.sortBy) {
      const order = filters.sortOrder === 'asc' ? 1 : -1;
      results.sort((a, b) => {
        if (filters.sortBy === 'createdAt' || filters.sortBy === 'updatedAt') {
          return (new Date(b[filters.sortBy]) - new Date(a[filters.sortBy])) * order;
        }
        if (filters.sortBy === 'priority') {
          const order_map = { P0: 0, P1: 1, P2: 2, P3: 3 };
          return (order_map[a.priority] - order_map[b.priority]) * order;
        }
        return 0;
      });
    }
    
    // 分页
    if (filters.limit) {
      const offset = filters.offset || 0;
      results = results.slice(offset, offset + filters.limit);
    }
    
    return results;
  }

  /**
   * 获取统计
   */
  getStats() {
    const all = this.getAll();
    const stats = {
      total: all.length,
      byStatus: {},
      byPriority: { P0: 0, P1: 0, P2: 0, P3: 0 },
      timeouts: 0
    };
    
    for (const task of all) {
      stats.byStatus[task.status] = (stats.byStatus[task.status] || 0) + 1;
      if (task.priority) stats.byPriority[task.priority]++;
      if (task.timeoutCount > 0) stats.timeouts++;
    }
    
    return stats;
  }

  /**
   * 检查超时任务
   */
  checkTimeouts(timeoutConfig = {}) {
    const now = Date.now();
    const defaults = { inbox: 30, planning: 60, executing: 120, review: 60 };
    const config = { ...defaults, ...timeoutConfig };
    const alerts = [];
    
    for (const task of this.getAll()) {
      if (task.status === 'done' || task.status === 'failed') continue;
      
      const elapsed = (now - new Date(task.stateChangedAt).getTime()) / 1000 / 60;
      const timeout = config[task.status] || 120;
      
      if (elapsed > timeout) {
        alerts.push({
          taskId: task.id,
          title: task.title,
          status: task.status,
          elapsedMinutes: Math.round(elapsed),
          timeout,
          level: elapsed > timeout * 2 ? 'critical' : 'warning'
        });
      }
    }
    
    return alerts;
  }

  /**
   * 索引操作辅助
   */
  _addToIndex(taskId, indexType, key) {
    if (indexType === 'status') {
      if (!this.statusIndex[key]) this.statusIndex[key] = [];
      if (!this.statusIndex[key].includes(taskId)) this.statusIndex[key].push(taskId);
    } else if (indexType === 'priority') {
      if (!this.priorityIndex[key]) this.priorityIndex[key] = [];
      if (!this.priorityIndex[key].includes(taskId)) this.priorityIndex[key].push(taskId);
    } else if (indexType === 'assignee') {
      if (!this.assigneeIndex[key]) this.assigneeIndex[key] = [];
      if (!this.assigneeIndex[key].includes(taskId)) this.assigneeIndex[key].push(taskId);
    }
  }

  _removeFromIndex(taskId, indexType, key) {
    if (indexType === 'status' && this.statusIndex[key]) {
      this.statusIndex[key] = this.statusIndex[key].filter(id => id !== taskId);
    } else if (indexType === 'priority' && this.priorityIndex[key]) {
      this.priorityIndex[key] = this.priorityIndex[key].filter(id => id !== taskId);
    } else if (indexType === 'assignee' && this.assigneeIndex[key]) {
      this.assigneeIndex[key] = this.assigneeIndex[key].filter(id => id !== taskId);
    }
  }

  /**
   * 保存索引到文件
   */
  _saveIndex() {
    const index = {
      status: this.statusIndex,
      priority: this.priorityIndex,
      assignee: this.assigneeIndex,
      updatedAt: new Date().toISOString()
    };
    fs.writeFileSync(INDEX_FILE, JSON.stringify(index, null, 2), 'utf-8');
  }

  /**
   * 从旧JSON文件迁移
   */
  migrate() {
    console.log('[TaskStore] 🔄 开始迁移旧数据...');
    const before = this.memoryCache.size;
    
    // 重新扫描所有JSON文件
    this._loadAll();
    
    const after = this.memoryCache.size;
    console.log(`[TaskStore] ✅ 迁移完成: ${before} → ${after} 任务`);
    return { before, after };
  }
}

module.exports = { TaskStore };
