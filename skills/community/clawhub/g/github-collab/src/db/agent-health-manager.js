/**
 * Agent 健康检查管理器
 * 监控 Agent 状态，实现心跳检测和自动故障恢复
 */

const { DatabaseManager } = require('./database-manager');

class AgentHealthManager {
  constructor(dbPath = null) {
    this.db = new DatabaseManager(dbPath).getDb();
    this.healthThreshold = 3; // 连续失败次数阈值
    this.heartbeatInterval = 300000; // 5 分钟
  }

  /**
   * 初始化健康检查表
   */
  async initHealthCheck() {
    try {
      const createTableSQL = `
        CREATE TABLE IF NOT EXISTS agent_health (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          agent_name TEXT NOT NULL UNIQUE,
          status TEXT NOT NULL DEFAULT 'unknown',
          last_heartbeat DATETIME,
          consecutive_failures INTEGER DEFAULT 0,
          cpu_usage REAL,
          memory_usage REAL,
          disk_usage REAL,
          response_time_ms INTEGER,
          error_count INTEGER DEFAULT 0,
          last_error TEXT,
          created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
          updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
      `;
      
      this.db.run(createTableSQL);
      
      // 创建索引
      this.db.run(`
        CREATE INDEX IF NOT EXISTS idx_agent_status 
        ON agent_health(status);
      `);
      
      this.db.run(`
        CREATE INDEX IF NOT EXISTS idx_last_heartbeat 
        ON agent_health(last_heartbeat);
      `);
      
      console.log('✅ Agent 健康检查表初始化完成');
      return true;
    } catch (error) {
      console.error('❌ 初始化健康检查表失败:', error.message);
      return false;
    }
  }

  /**
   * 注册 Agent 心跳
   */
  async registerHeartbeat(agentName, metrics = {}) {
    try {
      const upsertSQL = `
        INSERT INTO agent_health 
        (agent_name, status, last_heartbeat, cpu_usage, memory_usage, disk_usage, response_time_ms, updated_at)
        VALUES (?, 'healthy', CURRENT_TIMESTAMP, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(agent_name) DO UPDATE SET
          status = 'healthy',
          last_heartbeat = CURRENT_TIMESTAMP,
          consecutive_failures = 0,
          cpu_usage = excluded.cpu_usage,
          memory_usage = excluded.memory_usage,
          disk_usage = excluded.disk_usage,
          response_time_ms = excluded.response_time_ms,
          updated_at = CURRENT_TIMESTAMP;
      `;
      
      const cpu = metrics.cpu || 0;
      const memory = metrics.memory || 0;
      const disk = metrics.disk || 0;
      const responseTime = metrics.responseTime || 0;
      
      this.db.run(upsertSQL, [agentName, cpu, memory, disk, responseTime]);
      
      console.log(`✅ Agent ${agentName} 心跳已记录`);
      return true;
    } catch (error) {
      console.error('❌ 记录心跳失败:', error.message);
      return false;
    }
  }

  /**
   * 记录 Agent 错误
   */
  async recordError(agentName, errorMessage) {
    try {
      const updateSQL = `
        UPDATE agent_health
        SET status = 'error',
            consecutive_failures = consecutive_failures + 1,
            error_count = error_count + 1,
            last_error = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE agent_name = ?;
      `;
      
      const updateStmt = this.db.prepare(updateSQL);
      const result = updateStmt.run(errorMessage, agentName);
      
      if (result.changes > 0) {
        console.log(`⚠️ Agent ${agentName} 记录错误：${errorMessage}`);
        return true;
      }
      
      console.log(`⚠️ Agent ${agentName} 未找到`);
      return false;
    } catch (error) {
      console.error('❌ 记录错误失败:', error.message);
      return false;
    }
  }

  /**
   * 检查所有 Agent 健康状态
   */
  async checkAllAgents() {
    try {
      const querySQL = `
        SELECT * FROM agent_health
        ORDER BY last_heartbeat DESC;
      `;
      
      const agents = this.db.all(querySQL);
      const results = [];
      
      for (const agent of agents) {
        const healthStatus = await this.checkAgentHealth(agent);
        results.push(healthStatus);
      }
      
      return results;
    } catch (error) {
      console.error('❌ 检查 Agent 健康状态失败:', error.message);
      return [];
    }
  }

  /**
   * 检查单个 Agent 健康状态
   */
  async checkAgentHealth(agent) {
    try {
      const now = new Date();
      const lastHeartbeat = new Date(agent.last_heartbeat);
      const timeSinceHeartbeat = (now - lastHeartbeat) / 1000; // 秒
      
      let status = 'healthy';
      let isHealthy = true;
      
      // 检查心跳超时（超过 10 分钟无心跳）
      if (timeSinceHeartbeat > 600) {
        status = 'unreachable';
        isHealthy = false;
      }
      
      // 检查连续失败次数
      if (agent.consecutive_failures >= this.healthThreshold) {
        status = 'unhealthy';
        isHealthy = false;
      }
      
      // 更新状态
      if (status !== agent.status) {
        const updateSQL = `
          UPDATE agent_health
          SET status = ?, updated_at = CURRENT_TIMESTAMP
          WHERE agent_name = ?;
        `;
        
        this.db.run(updateSQL, status, agent.agent_name);
        console.log(`⚠️ Agent ${agent.agent_name} 状态变化：${agent.status} -> ${status}`);
      }
      
      return {
        agent_name: agent.agent_name,
        status: status,
        isHealthy: isHealthy,
        last_heartbeat: agent.last_heartbeat,
        time_since_heartbeat: timeSinceHeartbeat,
        consecutive_failures: agent.consecutive_failures,
        error_count: agent.error_count,
        last_error: agent.last_error
      };
    } catch (error) {
      console.error('❌ 检查 Agent 健康状态失败:', error.message);
      return null;
    }
  }

  /**
   * 获取健康 Agent 列表
   */
  async getHealthyAgents() {
    try {
      const querySQL = `
        SELECT * FROM agent_health
        WHERE status = 'healthy'
        ORDER BY last_heartbeat DESC;
      `;
      
      const agents = this.db.all(querySQL);
      return agents || [];
    } catch (error) {
      console.error('❌ 获取健康 Agent 列表失败:', error.message);
      return [];
    }
  }

  /**
   * 获取不健康 Agent 列表
   */
  async getUnhealthyAgents() {
    try {
      const querySQL = `
        SELECT * FROM agent_health
        WHERE status != 'healthy'
        ORDER BY last_heartbeat ASC;
      `;
      
      const agents = this.db.all(querySQL);
      return agents || [];
    } catch (error) {
      console.error('❌ 获取不健康 Agent 列表失败:', error.message);
      return [];
    }
  }

  /**
   * 自动故障恢复：重置失败计数器
   */
  async autoRecover(agentName) {
    try {
      const updateSQL = `
        UPDATE agent_health
        SET consecutive_failures = 0,
            status = 'healthy',
            updated_at = CURRENT_TIMESTAMP
        WHERE agent_name = ?;
      `;
      
      const updateStmt = this.db.prepare(updateSQL);
      const result = updateStmt.run(agentName);
      
      if (result.changes > 0) {
        console.log(`✅ Agent ${agentName} 已自动恢复`);
        return true;
      }
      
      console.log(`⚠️ Agent ${agentName} 未找到`);
      return false;
    } catch (error) {
      console.error('❌ 自动恢复失败:', error.message);
      return false;
    }
  }

  /**
   * 获取健康检查摘要
   */
  async getHealthSummary() {
    try {
      const summary = {
        total: 0,
        healthy: 0,
        unhealthy: 0,
        unreachable: 0,
        error: 0,
        agents: []
      };
      
      const totalSQL = 'SELECT COUNT(*) as count FROM agent_health';
      summary.total = this.db.get(totalSQL).count;
      
      const statusSQL = `
        SELECT status, COUNT(*) as count
        FROM agent_health
        GROUP BY status;
      `;
      
      const statusStats = this.db.all(statusSQL);
      for (const stat of statusStats) {
        summary[stat.status] = stat.count;
      }
      
      const allAgents = await this.checkAllAgents();
      summary.agents = allAgents;
      
      return summary;
    } catch (error) {
      console.error('❌ 获取健康检查摘要失败:', error.message);
      return null;
    }
  }

  /**
   * 清理过期 Agent 记录
   */
  async cleanupOldAgents(days = 30) {
    try {
      const deleteSQL = `
        DELETE FROM agent_health
        WHERE last_heartbeat < datetime('now', ? || ' days');
      `;
      
      const deleteStmt = this.db.prepare(deleteSQL);
      const result = deleteStmt.run(`-${days}`);
      
      console.log(`✅ 已清理 ${result.changes} 个过期 Agent 记录`);
      return result.changes;
    } catch (error) {
      console.error('❌ 清理过期 Agent 记录失败:', error.message);
      return 0;
    }
  }

  /**
   * 启动健康检查定时任务
   */
  startHealthCheckLoop() {
    console.log('🔄 启动 Agent 健康检查定时任务...');
    
    setInterval(async () => {
      try {
        const summary = await this.getHealthSummary();
        
        console.log(`\n=== Agent 健康检查报告 ===`);
        console.log(`总 Agent 数：${summary.total}`);
        console.log(`健康：${summary.healthy}`);
        console.log(`不健康：${summary.unhealthy}`);
        console.log(`不可达：${summary.unreachable}`);
        console.log(`错误：${summary.error}`);
        
        // 自动恢复连续失败次数过多的 Agent
        const unhealthyAgents = await this.getUnhealthyAgents();
        for (const agent of unhealthyAgents) {
          if (agent.consecutive_failures >= this.healthThreshold) {
            await this.autoRecover(agent.agent_name);
          }
        }
        
      } catch (error) {
        console.error('❌ 健康检查循环失败:', error.message);
      }
    }, this.heartbeatInterval);
  }
}

module.exports = { AgentHealthManager };
