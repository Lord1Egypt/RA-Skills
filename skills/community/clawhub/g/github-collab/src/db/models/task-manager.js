/**
 * Task Manager - 任务数据库操作模块
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
  const dbPath = config.db.path || process.env.DB_PATH || 
                 process.env.OPENCLAW_DB_PATH || 
                 path.join(__dirname, 'tasks.db');
  
  return new Database(dbPath);
}

/**
 * 初始化数据库表
 */
function initDatabase() {
  const db = getDb();
  
  try {
    // 创建任务表
    db.exec(`
      CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT DEFAULT 'pending',
        priority INTEGER DEFAULT 3,
        assigned_to TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        completed_at DATETIME
      )
    `);
    
    // 创建项目表
    db.exec(`
      CREATE TABLE IF NOT EXISTS projects (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `);
    
    // 创建索引
    db.exec(`
      CREATE INDEX IF NOT EXISTS idx_tasks_project_id ON tasks(project_id)
    `);
    db.exec(`
      CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)
    `);
    db.exec(`
      CREATE INDEX IF NOT EXISTS idx_tasks_assigned_to ON tasks(assigned_to)
    `);
    db.exec(`
      CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority)
    `);
    
    logger.info('✅ 任务数据库表已初始化');
  } catch (error) {
    logger.error('❌ 数据库初始化失败:', error);
    throw error;
  } finally {
    db.close();
  }
}

/**
 * 创建任务
 */
function createTask(task) {
  const db = getDb();
  
  try {
    const stmt = db.prepare(`
      INSERT INTO tasks (project_id, title, description, status, priority)
      VALUES (?, ?, ?, ?, ?)
    `);
    
    const info = stmt.run(
      task.project_id,
      task.title,
      task.description || '',
      task.status || 'pending',
      task.priority || 3
    );
    
    logger.info(`✅ 任务创建成功：${task.title} (ID: ${info.lastInsertRowid})`);
    
    return { id: info.lastInsertRowid, ...task };
  } catch (error) {
    logger.error('❌ 创建任务失败:', error);
    throw error;
  } finally {
    db.close();
  }
}

/**
 * 获取所有任务
 */
function getAllTasks(projectId = null) {
  const db = getDb();
  
  try {
    if (projectId) {
      const rows = db.prepare('SELECT * FROM tasks WHERE project_id = ? ORDER BY priority, created_at').all(projectId);
      return rows;
    }
    
    const rows = db.prepare('SELECT * FROM tasks ORDER BY priority, created_at').all();
    return rows;
  } catch (error) {
    logger.error('❌ 获取任务列表失败:', error);
    throw error;
  } finally {
    db.close();
  }
}

/**
 * 根据 ID 获取任务
 */
function getTaskById(id) {
  const db = getDb();
  
  try {
    const row = db.prepare('SELECT * FROM tasks WHERE id = ?').get(id);
    return row;
  } catch (error) {
    logger.error(`❌ 获取任务失败 (ID: ${id}):`, error);
    throw error;
  } finally {
    db.close();
  }
}

/**
 * 更新任务状态
 */
function updateTaskStatus(id, status) {
  const db = getDb();
  
  try {
    const completedAt = status === 'completed' ? new Date().toISOString() : null;
    
    if (completedAt) {
      const stmt = db.prepare('UPDATE tasks SET status = ?, updated_at = CURRENT_TIMESTAMP, completed_at = ? WHERE id = ?');
      const info = stmt.run(status, completedAt, id);
      logger.info(`✅ 任务状态更新成功：ID ${id} -> ${status}`);
      return { changes: info.changes };
    }
    
    const stmt = db.prepare('UPDATE tasks SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?');
    const info = stmt.run(status, id);
    logger.info(`✅ 任务状态更新成功：ID ${id} -> ${status}`);
    return { changes: info.changes };
  } catch (error) {
    logger.error(`❌ 更新任务状态失败 (ID: ${id}):`, error);
    throw error;
  } finally {
    db.close();
  }
}

/**
 * 分配任务
 */
function assignTask(id, agentName) {
  const db = getDb();
  
  try {
    const stmt = db.prepare('UPDATE tasks SET assigned_to = ?, status = "in_progress", updated_at = CURRENT_TIMESTAMP WHERE id = ?');
    const info = stmt.run(agentName, id);
    logger.info(`✅ 任务分配成功：ID ${id} -> ${agentName}`);
    return { changes: info.changes };
  } catch (error) {
    logger.error(`❌ 分配任务失败 (ID: ${id}):`, error);
    throw error;
  } finally {
    db.close();
  }
}

/**
 * 完成任务
 */
function completeTask(id) {
  return updateTaskStatus(id, 'completed');
}

/**
 * 取消任务
 */
function cancelTask(id) {
  return updateTaskStatus(id, 'cancelled');
}

/**
 * 创建项目
 */
function createProject(project) {
  const db = getDb();
  
  try {
    const stmt = db.prepare('INSERT OR REPLACE INTO projects (id, name, description) VALUES (?, ?, ?)');
    stmt.run(project.id, project.name, project.description || '');
    logger.info(`✅ 项目创建成功：${project.name}`);
    return project;
  } catch (error) {
    logger.error('❌ 创建项目失败:', error);
    throw error;
  } finally {
    db.close();
  }
}

/**
 * 获取所有项目
 */
function getAllProjects() {
  const db = getDb();
  
  try {
    const rows = db.prepare('SELECT * FROM projects ORDER BY created_at').all();
    return rows;
  } catch (error) {
    logger.error('❌ 获取项目列表失败:', error);
    throw error;
  } finally {
    db.close();
  }
}

/**
 * 获取项目任务统计
 */
function getProjectStats(projectId) {
  const db = getDb();
  
  try {
    const stats = db.prepare(`
      SELECT 
        COUNT(*) as total,
        SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending,
        SUM(CASE WHEN status = 'in_progress' THEN 1 ELSE 0 END) as in_progress,
        SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
        SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) as cancelled
      FROM tasks
      WHERE project_id = ?
    `).get(projectId);
    return stats;
  } catch (error) {
    logger.error(`❌ 获取项目统计失败 (ID: ${projectId}):`, error);
    throw error;
  } finally {
    db.close();
  }
}

module.exports = {
  initDatabase,
  createTask,
  getAllTasks,
  getTaskById,
  updateTaskStatus,
  assignTask,
  completeTask,
  cancelTask,
  createProject,
  getAllProjects,
  getProjectStats
};
