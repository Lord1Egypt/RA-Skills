/**
 * 分布式任务分配管理器
 * 实现负载均衡和智能任务分配
 */

const { DatabaseManager } = require('./database-manager');

class TaskDistributionManager {
  constructor(dbPath = null) {
    this.db = new DatabaseManager(dbPath).getDb();
  }

  /**
   * 初始化任务分配表
   */
  async initDistribution() {
    try {
      const createTableSQL = `
        CREATE TABLE IF NOT EXISTS task_distribution (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          task_id INTEGER NOT NULL,
          agent_name TEXT NOT NULL,
          assigned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
          completed_at DATETIME,
          status TEXT NOT NULL DEFAULT 'assigned',
          load_factor REAL DEFAULT 1.0,
          execution_time_ms INTEGER,
          result TEXT,
          error_message TEXT,
          retry_count INTEGER DEFAULT 0,
          max_retries INTEGER DEFAULT 3
        );
      `;
      
      this.db.run(createTableSQL);
      
      // 创建索引
      this.db.run(`
        CREATE INDEX IF NOT EXISTS idx_task_distribution_task_id 
        ON task_distribution(task_id);
      `);
      
      this.db.run(`
        CREATE INDEX IF NOT EXISTS idx_task_distribution_agent 
        ON task_distribution(agent_name);
      `);
      
      this.db.run(`
        CREATE INDEX IF NOT EXISTS idx_task_distribution_status 
        ON task_distribution(status);
      `);
      
      console.log('✅ 任务分配表初始化完成');
      return true;
    } catch (error) {
      console.error('❌ 初始化任务分配表失败:', error.message);
      return false;
    }
  }

  /**
   * 获取 Agent 当前负载
   */
  async getAgentLoad(agentName) {
    try {
      const querySQL = `
        SELECT 
          COUNT(*) as total_tasks,
          SUM(CASE WHEN status = 'assigned' THEN 1 ELSE 0 END) as pending_tasks,
          AVG(execution_time_ms) as avg_execution_time
        FROM task_distribution
        WHERE agent_name = ?
        AND assigned_at > datetime('now', '-1 hour');
      `;
      
      const result = this.db.get(querySQL, agentName);
      
      return {
        agent_name: agentName,
        total_tasks: result.total_tasks || 0,
        pending_tasks: result.pending_tasks || 0,
        avg_execution_time: result.avg_execution_time || 0
      };
    } catch (error) {
      console.error('❌ 获取 Agent 负载失败:', error.message);
      return null;
    }
  }

  /**
   * 获取所有 Agent 负载
   */
  async getAllAgentLoads(agentNames) {
    try {
      const loads = [];
      
      for (const agentName of agentNames) {
        const load = await this.getAgentLoad(agentName);
        loads.push(load);
      }
      
      return loads;
    } catch (error) {
      console.error('❌ 获取所有 Agent 负载失败:', error.message);
      return [];
    }
  }

  /**
   * 智能分配任务（负载均衡）
   */
  async distributeTask(taskId, availableAgents = []) {
    try {
      // 获取所有可用 Agent 的负载
      const loads = await this.getAllAgentLoads(availableAgents);
      
      if (loads.length === 0) {
        console.log('⚠️ 没有可用的 Agent');
        return null;
      }
      
      // 计算每个 Agent 的负载因子
      const agentWithLoad = loads.map(load => {
        const loadFactor = 1 + (load.pending_tasks * 0.1) + (load.avg_execution_time / 10000);
        return {
          ...load,
          load_factor: loadFactor
        };
      });
      
      // 选择负载最低的 Agent
      const selectedAgent = agentWithLoad.reduce((min, current) => {
        return current.load_factor < min.load_factor ? current : min;
      });
      
      // 分配任务
      const result = await this.assignTask(taskId, selectedAgent.agent_name, selectedAgent.load_factor);
      
      if (result) {
        console.log(`✅ 任务 ${taskId} 已分配给 ${selectedAgent.agent_name} (负载因子：${selectedAgent.load_factor.toFixed(2)})`);
      }
      
      return result;
    } catch (error) {
      console.error('❌ 分布式任务分配失败:', error.message);
      return null;
    }
  }

  /**
   * 分配任务给指定 Agent
   */
  async assignTask(taskId, agentName, loadFactor = 1.0) {
    try {
      const insertSQL = `
        INSERT INTO task_distribution 
        (task_id, agent_name, load_factor)
        VALUES (?, ?, ?);
      `;
      
      const insertStmt = this.db.prepare(insertSQL);
      const result = insertStmt.run(taskId, agentName, loadFactor);
      
      console.log(`✅ 任务 ${taskId} 已分配给 ${agentName}`);
      return result.lastInsertRowid;
    } catch (error) {
      console.error('❌ 分配任务失败:', error.message);
      return null;
    }
  }

  /**
   * 标记任务完成
   */
  async completeTask(distributionId, executionTime = 0, result = null) {
    try {
      const updateSQL = `
        UPDATE task_distribution
        SET status = 'completed',
            completed_at = CURRENT_TIMESTAMP,
            execution_time_ms = ?,
            result = ?
        WHERE id = ?;
      `;
      
      const updateStmt = this.db.prepare(updateSQL);
      const result = updateStmt.run(executionTime, result ? JSON.stringify(result) : null, distributionId);
      
      if (result.changes > 0) {
        console.log(`✅ 任务分配 ${distributionId} 已完成`);
        return true;
      }
      
      console.log(`⚠️ 任务分配 ${distributionId} 未找到`);
      return false;
    } catch (error) {
      console.error('❌ 完成任务失败:', error.message);
      return false;
    }
  }

  /**
   * 标记任务失败并重试
   */
  async failTask(distributionId, errorMessage) {
    try {
      // 获取当前重试次数
      const querySQL = `
        SELECT retry_count, max_retries, task_id, agent_name
        FROM task_distribution
        WHERE id = ?;
      `;
      
      const task = this.db.get(querySQL, distributionId);
      
      if (!task) {
        console.log(`⚠️ 任务分配 ${distributionId} 未找到`);
        return false;
      }
      
      // 检查是否超过最大重试次数
      if (task.retry_count >= task.max_retries) {
        const updateSQL = `
          UPDATE task_distribution
          SET status = 'failed',
              error_message = ?,
              completed_at = CURRENT_TIMESTAMP
          WHERE id = ?;
        `;
        
        this.db.run(updateSQL, errorMessage, distributionId);
        console.log(`❌ 任务分配 ${distributionId} 失败（超过最大重试次数）: ${errorMessage}`);
        return false;
      }
      
      // 更新重试次数
      const updateSQL = `
        UPDATE task_distribution
        SET status = 'assigned',
            retry_count = retry_count + 1,
            error_message = ?,
            completed_at = NULL
        WHERE id = ?;
      `;
      
      const updateStmt = this.db.prepare(updateSQL);
      const result = updateStmt.run(errorMessage, distributionId);
      
      if (result.changes > 0) {
        console.log(`⚠️ 任务分配 ${distributionId} 失败，将重试 (${task.retry_count + 1}/${task.max_retries}): ${errorMessage}`);
        
        // 重新分配任务
        return await this.distributeTask(task.task_id, [task.agent_name]);
      }
      
      return false;
    } catch (error) {
      console.error('❌ 标记任务失败失败:', error.message);
      return false;
    }
  }

  /**
   * 获取任务分配统计
   */
  async getDistributionStats() {
    try {
      const statsSQL = `
        SELECT 
          agent_name,
          COUNT(*) as total_assigned,
          SUM(CASE WHEN status = 'assigned' THEN 1 ELSE 0 END) as pending,
          SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
          SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed,
          AVG(execution_time_ms) as avg_execution_time,
          AVG(load_factor) as avg_load_factor
        FROM task_distribution
        GROUP BY agent_name
        ORDER BY total_assigned DESC;
      `;
      
      const stats = this.db.all(statsSQL);
      return stats || [];
    } catch (error) {
      console.error('❌ 获取任务分配统计失败:', error.message);
      return [];
    }
  }

  /**
   * 获取待处理的任务分配
   */
  async getPendingDistributions() {
    try {
      const querySQL = `
        SELECT td.*, t.title, t.description, t.priority
        FROM task_distribution td
        JOIN tasks t ON td.task_id = t.id
        WHERE td.status = 'assigned'
        ORDER BY t.priority DESC, td.assigned_at ASC;
      `;
      
      const distributions = this.db.all(querySQL);
      return distributions || [];
    } catch (error) {
      console.error('❌ 获取待处理任务分配失败:', error.message);
      return [];
    }
  }

  /**
   * 获取 Agent 的任务历史
   */
  async getAgentHistory(agentName, limit = 10) {
    try {
      const querySQL = `
        SELECT td.*, t.title, t.description
        FROM task_distribution td
        JOIN tasks t ON td.task_id = t.id
        WHERE td.agent_name = ?
        ORDER BY td.assigned_at DESC
        LIMIT ?;
      `;
      
      const history = this.db.all(querySQL, agentName, limit);
      return history || [];
    } catch (error) {
      console.error('❌ 获取 Agent 任务历史失败:', error.message);
      return [];
    }
  }

  /**
   * 清理过期任务分配记录
   */
  async cleanupOldDistributions(days = 30) {
    try {
      const deleteSQL = `
        DELETE FROM task_distribution
        WHERE status IN ('completed', 'failed')
        AND completed_at < datetime('now', ? || ' days');
      `;
      
      const deleteStmt = this.db.prepare(deleteSQL);
      const result = deleteStmt.run(`-${days}`);
      
      console.log(`✅ 已清理 ${result.changes} 个过期任务分配记录`);
      return result.changes;
    } catch (error) {
      console.error('❌ 清理过期任务分配记录失败:', error.message);
      return 0;
    }
  }

  /**
   * 获取分配摘要
   */
  async getDistributionSummary() {
    try {
      const summary = {
        total: 0,
        assigned: 0,
        completed: 0,
        failed: 0,
        byAgent: {}
      };
      
      const totalSQL = 'SELECT COUNT(*) as count FROM task_distribution';
      summary.total = this.db.get(totalSQL).count;
      
      const statusSQL = `
        SELECT status, COUNT(*) as count
        FROM task_distribution
        GROUP BY status;
      `;
      
      const statusStats = this.db.all(statusSQL);
      for (const stat of statusStats) {
        summary[stat.status] = stat.count;
      }
      
      const agentStats = await this.getDistributionStats();
      for (const stat of agentStats) {
        summary.byAgent[stat.agent_name] = stat;
      }
      
      return summary;
    } catch (error) {
      console.error('❌ 获取分配摘要失败:', error.message);
      return null;
    }
  }
}

module.exports = { TaskDistributionManager };
