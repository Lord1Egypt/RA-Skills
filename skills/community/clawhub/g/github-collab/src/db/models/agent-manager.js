/**
 * Agent Manager - Agent 数据库操作模块
 */

const Database = require('better-sqlite3');
const path = require('path');
const { getConfig } = require('../config');
const { createLogger } = require('../logger');

const logger = createLogger({ level: 'INFO' });

/**
 * 获取数据库连接
 */
function getDb() {
  const config = getConfig();
  const dbPath = process.env.DB_PATH || 
                 process.env.OPENCLAW_DB_PATH || 
                 path.join(__dirname, 'github-collab.db');
  
  return new Database(dbPath);
}

/**
 * 初始化数据库表
 */
function initDatabase() {
  const db = getDb();
  
  try {
    // 创建 Agent 表
    db.exec(`
      CREATE TABLE IF NOT EXISTS agents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        role TEXT NOT NULL,
        target TEXT NOT NULL,
        description TEXT,
        capabilities TEXT,
        is_active INTEGER DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `);
    
    // 创建消息日志表
    db.exec(`
      CREATE TABLE IF NOT EXISTS message_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_agent TEXT NOT NULL,
        to_agent TEXT NOT NULL,
        message TEXT NOT NULL,
        status TEXT DEFAULT 'sent',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `);
    
    // 创建索引
    db.exec(`
      CREATE INDEX IF NOT EXISTS idx_agents_name ON agents(name)
    `);
    db.exec(`
      CREATE INDEX IF NOT EXISTS idx_agents_role ON agents(role)
    `);
    db.exec(`
      CREATE INDEX IF NOT EXISTS idx_agents_active ON agents(is_active)
    `);
    db.exec(`
      CREATE INDEX IF NOT EXISTS idx_message_logs_from ON message_logs(from_agent)
    `);
    db.exec(`
      CREATE INDEX IF NOT EXISTS idx_message_logs_to ON message_logs(to_agent)
    `);
    
    logger.info('✅ Agent 数据库表已初始化');
  } catch (error) {
    logger.error('❌ Agent 数据库初始化失败:', error);
    throw error;
  } finally {
    db.close();
  }
}

/**
 * 获取所有 Agent
 */
function getAllAgents() {
  const db = getDb();
  
  try {
    const rows = db.prepare('SELECT * FROM agents WHERE is_active = 1 ORDER BY name').all();
    return rows;
  } catch (error) {
    logger.error('❌ 获取 Agent 列表失败:', error);
    throw error;
  } finally {
    db.close();
  }
}

/**
 * 根据名称获取 Agent
 */
function getAgentByName(name) {
  const db = getDb();
  
  try {
    const row = db.prepare('SELECT * FROM agents WHERE name = ? AND is_active = 1').get(name);
    return row;
  } catch (error) {
    logger.error(`❌ 获取 Agent 失败 (名称：${name}):`, error);
    throw error;
  } finally {
    db.close();
  }
}

/**
 * 获取 Agent 地址
 */
function getAgentAddress(name) {
  const agent = getAgentByName(name);
  if (!agent) {
    const error = new Error(`Agent not found: ${name}`);
    logger.error(error.message);
    throw error;
  }
  return agent.target;
}

/**
 * 更新 Agent 地址
 */
function updateAgentAddress(name, newTarget) {
  const db = getDb();
  
  try {
    const stmt = db.prepare('UPDATE agents SET target = ?, updated_at = CURRENT_TIMESTAMP WHERE name = ?');
    const info = stmt.run(newTarget, name);
    
    if (info.changes === 0) {
      const error = new Error(`Agent not found: ${name}`);
      logger.error(error.message);
      throw error;
    }
    
    logger.info(`✅ Agent 地址更新成功：${name} -> ${newTarget}`);
    return { changes: info.changes };
  } catch (error) {
    logger.error(`❌ 更新 Agent 地址失败 (名称：${name}):`, error);
    throw error;
  } finally {
    db.close();
  }
}

/**
 * 添加或更新 Agent
 */
function upsertAgent(agent) {
  const db = getDb();
  
  try {
    const stmt = db.prepare(`
      INSERT INTO agents (name, role, target, description, capabilities, is_active)
      VALUES (?, ?, ?, ?, ?, 1)
      ON CONFLICT(name) DO UPDATE SET
        role = excluded.role,
        target = excluded.target,
        description = excluded.description,
        capabilities = excluded.capabilities,
        updated_at = CURRENT_TIMESTAMP
    `);
    
    const info = stmt.run(
      agent.name,
      agent.role,
      agent.target,
      agent.description,
      agent.capabilities
    );
    
    logger.info(`✅ Agent 添加/更新成功：${agent.name} (ID: ${info.lastInsertRowid})`);
    return { changes: info.changes, lastID: info.lastInsertRowid };
  } catch (error) {
    logger.error(`❌ 添加/更新 Agent 失败 (名称：${agent.name}):`, error);
    throw error;
  } finally {
    db.close();
  }
}

/**
 * 激活或停用 Agent
 */
function toggleAgentStatus(name, isActive) {
  const db = getDb();
  
  try {
    const stmt = db.prepare('UPDATE agents SET is_active = ?, updated_at = CURRENT_TIMESTAMP WHERE name = ?');
    const info = stmt.run(isActive ? 1 : 0, name);
    
    if (info.changes === 0) {
      const error = new Error(`Agent not found: ${name}`);
      logger.error(error.message);
      throw error;
    }
    
    logger.info(`✅ Agent 状态更新成功：${name} -> ${isActive ? '激活' : '停用'}`);
    return { changes: info.changes };
  } catch (error) {
    logger.error(`❌ 更新 Agent 状态失败 (名称：${name}):`, error);
    throw error;
  } finally {
    db.close();
  }
}

/**
 * 记录消息日志
 */
function logMessage(fromAgent, toAgent, message, status = 'sent') {
  const db = getDb();
  
  try {
    const stmt = db.prepare('INSERT INTO message_logs (from_agent, to_agent, message, status) VALUES (?, ?, ?, ?)');
    const info = stmt.run(fromAgent, toAgent, message, status);
    logger.debug(`✅ 消息日志记录成功：${fromAgent} -> ${toAgent}`);
    return { id: info.lastInsertRowid };
  } catch (error) {
    logger.error('❌ 记录消息日志失败:', error);
    throw error;
  } finally {
    db.close();
  }
}

/**
 * 获取消息日志
 */
function getMessageLogs(limit = 50) {
  const db = getDb();
  
  try {
    const rows = db.prepare('SELECT * FROM message_logs ORDER BY created_at DESC LIMIT ?').all(limit);
    return rows;
  } catch (error) {
    logger.error('❌ 获取消息日志失败:', error);
    throw error;
  } finally {
    db.close();
  }
}

/**
 * 验证 Agent 地址格式
 */
function validateAgentAddress(address) {
  const pattern = /^qqbot:(c2c|group):[a-zA-Z0-9_-]+$/;
  return pattern.test(address);
}

/**
 * 批量更新 Agent 地址
 */
function batchUpdateAddresses(updates) {
  const results = [];
  
  for (const update of updates) {
    try {
      const result = updateAgentAddress(update.name, update.target);
      results.push({ name: update.name, success: true, result });
    } catch (error) {
      results.push({ name: update.name, success: false, error: error.message });
    }
  }
  
  return results;
}

module.exports = {
  initDatabase,
  getAllAgents,
  getAgentByName,
  getAgentAddress,
  updateAgentAddress,
  upsertAgent,
  toggleAgentStatus,
  logMessage,
  getMessageLogs,
  validateAgentAddress,
  batchUpdateAddresses
};
