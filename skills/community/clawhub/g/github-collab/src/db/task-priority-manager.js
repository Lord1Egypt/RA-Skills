/**
 * 任务优先级管理器
 * 实现任务优先级队列，支持动态优先级调整和智能调度
 */

const { DatabaseManager } = require('./database-manager');

class TaskPriorityManager {
  constructor(dbPath = null) {
    this.db = new DatabaseManager(dbPath).getDb();
    this.priorityLevels = {
      CRITICAL: 10,
      HIGH: 8,
      MEDIUM: 5,
      LOW: 3,
      BACKGROUND: 1
    };
  }

  /**
   * 初始化优先级队列表
   */
  async initPriorityQueue() {
    try {
      const createTableSQL = `
        CREATE TABLE IF NOT EXISTS task_priority_queue (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          task_id INTEGER NOT NULL,
          priority INTEGER NOT NULL DEFAULT 5,
          priority_level TEXT NOT NULL DEFAULT 'MEDIUM',
          created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
          updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
          due_date DATETIME,
          weight REAL DEFAULT 1.0,
          estimated_hours REAL,
          dependencies TEXT,
          status TEXT DEFAULT 'pending',
          FOREIGN KEY (task_id) REFERENCES tasks(id)
        );
      `;
      
      this.db.run(createTableSQL);
      
      // 创建索引
      this.db.run(`
        CREATE INDEX IF NOT EXISTS idx_priority 
        ON task_priority_queue(priority DESC, created_at ASC);
      `);
      
      this.db.run(`
        CREATE INDEX IF NOT EXISTS idx_status 
        ON task_priority_queue(status);
      `);
      
      console.log('✅ 任务优先级队列表初始化完成');
      return true;
    } catch (error) {
      console.error('❌ 初始化优先级队列失败:', error.message);
      return false;
    }
  }

  /**
   * 添加任务到优先级队列
   */
  async addToQueue(taskId, options = {}) {
    try {
      const priorityLevel = options.priorityLevel || 'MEDIUM';
      const priority = this.priorityLevels[priorityLevel] || this.priorityLevels.MEDIUM;
      const dueDate = options.dueDate || null;
      const weight = options.weight || 1.0;
      const estimatedHours = options.estimatedHours || null;
      const dependencies = options.dependencies ? JSON.stringify(options.dependencies) : null;

      const insertSQL = `
        INSERT INTO task_priority_queue 
        (task_id, priority, priority_level, due_date, weight, estimated_hours, dependencies)
        VALUES (?, ?, ?, ?, ?, ?, ?);
      `;

      const insertStmt = this.db.prepare(insertSQL);
      const result = insertStmt.run(taskId, priority, priorityLevel, dueDate, weight, estimatedHours, dependencies);
      
      console.log(`✅ 任务 ${taskId} 已添加到优先级队列 (优先级：${priorityLevel})`);
      return result.lastInsertRowid;
    } catch (error) {
      console.error('❌ 添加任务到队列失败:', error.message);
      return null;
    }
  }

  /**
   * 更新任务优先级
   */
  async updatePriority(taskId, newPriorityLevel) {
    try {
      const newPriority = this.priorityLevels[newPriorityLevel] || this.priorityLevels.MEDIUM;
      
      const updateSQL = `
        UPDATE task_priority_queue
        SET priority = ?, priority_level = ?, updated_at = CURRENT_TIMESTAMP
        WHERE task_id = ?;
      `;
      
      const updateStmt = this.db.prepare(updateSQL);
      const result = updateStmt.run(newPriority, newPriorityLevel, taskId);
      
      if (result.changes > 0) {
        console.log(`✅ 任务 ${taskId} 优先级已更新为 ${newPriorityLevel}`);
        return true;
      }
      
      console.log(`⚠️ 任务 ${taskId} 未找到`);
      return false;
    } catch (error) {
      console.error('❌ 更新优先级失败:', error.message);
      return false;
    }
  }

  /**
   * 获取下一个最高优先级任务
   */
  async getNextTask() {
    try {
      const querySQL = `
        SELECT tpq.*, t.title, t.description, t.assignee
        FROM task_priority_queue tpq
        JOIN tasks t ON tpq.task_id = t.id
        WHERE tpq.status = 'pending'
        ORDER BY tpq.priority DESC, tpq.created_at ASC
        LIMIT 1;
      `;
      
      const task = this.db.get(querySQL);
      return task || null;
    } catch (error) {
      console.error('❌ 获取下一个任务失败:', error.message);
      return null;
    }
  }

  /**
   * 获取所有待处理任务（按优先级排序）
   */
  async getAllPendingTasks() {
    try {
      const querySQL = `
        SELECT tpq.*, t.title, t.description, t.assignee
        FROM task_priority_queue tpq
        JOIN tasks t ON tpq.task_id = t.id
        WHERE tpq.status = 'pending'
        ORDER BY tpq.priority DESC, tpq.created_at ASC;
      `;
      
      const tasks = this.db.all(querySQL);
      return tasks || [];
    } catch (error) {
      console.error('❌ 获取待处理任务失败:', error.message);
      return [];
    }
  }

  /**
   * 获取按优先级分组的任务统计
   */
  async getPriorityStats() {
    try {
      const querySQL = `
        SELECT 
          priority_level,
          COUNT(*) as count,
          SUM(weight) as total_weight,
          SUM(estimated_hours) as total_estimated_hours
        FROM task_priority_queue
        WHERE status = 'pending'
        GROUP BY priority_level
        ORDER BY priority DESC;
      `;
      
      const stats = this.db.all(querySQL);
      return stats || [];
    } catch (error) {
      console.error('❌ 获取优先级统计失败:', error.message);
      return [];
    }
  }

  /**
   * 完成任务（从队列中移除）
   */
  async completeTask(taskId) {
    try {
      const updateSQL = `
        UPDATE task_priority_queue
        SET status = 'completed', updated_at = CURRENT_TIMESTAMP
        WHERE task_id = ?;
      `;
      
      const updateStmt = this.db.prepare(updateSQL);
      const result = updateStmt.run(taskId);
      
      if (result.changes > 0) {
        console.log(`✅ 任务 ${taskId} 已完成`);
        return true;
      }
      
      console.log(`⚠️ 任务 ${taskId} 未找到`);
      return false;
    } catch (error) {
      console.error('❌ 完成任务失败:', error.message);
      return false;
    }
  }

  /**
   * 清除过期任务
   */
  async clearExpiredTasks(days = 30) {
    try {
      const deleteSQL = `
        DELETE FROM task_priority_queue
        WHERE status = 'completed'
        AND updated_at < datetime('now', ? || ' days');
      `;
      
      const deleteStmt = this.db.prepare(deleteSQL);
      const result = deleteStmt.run(`-${days}`);
      
      console.log(`✅ 已清理 ${result.changes} 个过期任务`);
      return result.changes;
    } catch (error) {
      console.error('❌ 清理过期任务失败:', error.message);
      return 0;
    }
  }

  /**
   * 智能调度：根据 Agent 能力分配任务
   */
  async smartAssign(agentName, agentCapabilities = []) {
    try {
      // 获取最高优先级任务
      const task = await this.getNextTask();
      
      if (!task) {
        console.log('ℹ️ 没有待处理的任务');
        return null;
      }
      
      // 解析任务依赖
      const dependencies = task.dependencies ? JSON.parse(task.dependencies) : [];
      
      // 检查依赖是否满足
      if (dependencies.length > 0) {
        const unmetDeps = await this.getUnmetDependencies(dependencies);
        if (unmetDeps.length > 0) {
          console.log(`⚠️ 任务 ${task.task_id} 有待满足的依赖：${unmetDeps.join(', ')}`);
          return null;
        }
      }
      
      // 分配任务
      const updateSQL = `
        UPDATE task_priority_queue
        SET status = 'assigned', updated_at = CURRENT_TIMESTAMP
        WHERE task_id = ?;
      `;
      
      this.db.prepare(updateSQL).run(task.task_id);
      
      console.log(`✅ 已分配任务 ${task.task_id} (${task.title}) 给 ${agentName}`);
      return task;
    } catch (error) {
      console.error('❌ 智能调度失败:', error.message);
      return null;
    }
  }

  /**
   * 获取未满足的依赖
   */
  async getUnmetDependencies(dependencies) {
    try {
      const unmet = [];
      
      for (const dep of dependencies) {
        const checkSQL = `
          SELECT id FROM task_priority_queue
          WHERE task_id = ? AND status != 'completed';
        `;
        
        const result = this.db.get(checkSQL, dep);
        if (result) {
          unmet.push(dep);
        }
      }
      
      return unmet;
    } catch (error) {
      console.error('❌ 检查依赖失败:', error.message);
      return dependencies;
    }
  }

  /**
   * 获取队列状态摘要
   */
  async getQueueSummary() {
    try {
      const summary = {
        total: 0,
        pending: 0,
        assigned: 0,
        completed: 0,
        byPriority: {}
      };
      
      const totalSQL = 'SELECT COUNT(*) as count FROM task_priority_queue';
      summary.total = this.db.get(totalSQL).count;
      
      const statusSQL = `
        SELECT status, COUNT(*) as count
        FROM task_priority_queue
        GROUP BY status;
      `;
      
      const statusStats = this.db.all(statusSQL);
      for (const stat of statusStats) {
        summary[stat.status] = stat.count;
      }
      
      const priorityStats = await this.getPriorityStats();
      for (const stat of priorityStats) {
        summary.byPriority[stat.priority_level] = stat.count;
      }
      
      return summary;
    } catch (error) {
      console.error('❌ 获取队列摘要失败:', error.message);
      return null;
    }
  }
}

module.exports = { TaskPriorityManager };
