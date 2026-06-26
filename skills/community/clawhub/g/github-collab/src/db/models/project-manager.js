/**
 * Project Manager - 项目数据库操作模块
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
                 path.join(__dirname, 'projects.db');
  
  return new Database(dbPath);
}

/**
 * 初始化数据库表
 */
function initDatabase() {
  const db = getDb();
  
  try {
    // 创建项目表
    db.exec(`
      CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        description TEXT,
        status TEXT DEFAULT 'active',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `);
    
    // 创建索引
    db.exec(`
      CREATE INDEX IF NOT EXISTS idx_projects_name ON projects(name)
    `);
    db.exec(`
      CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status)
    `);
    
    logger.info('✅ 项目数据库表已初始化');
  } catch (error) {
    logger.error('❌ 项目数据库初始化失败:', error);
    throw error;
  } finally {
    db.close();
  }
}

/**
 * 创建项目
 */
function createProject(project) {
  const db = getDb();
  
  try {
    const stmt = db.prepare('INSERT INTO projects (name, description, status) VALUES (?, ?, ?)');
    const info = stmt.run(project.name, project.description || '', project.status || 'active');
    logger.info(`✅ 项目创建成功：${project.name} (ID: ${info.lastInsertRowid})`);
    return { id: info.lastInsertRowid, ...project };
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
 * 根据 ID 获取项目
 */
function getProjectById(id) {
  const db = getDb();
  
  try {
    const row = db.prepare('SELECT * FROM projects WHERE id = ?').get(id);
    return row;
  } catch (error) {
    logger.error(`❌ 获取项目失败 (ID: ${id}):`, error);
    throw error;
  } finally {
    db.close();
  }
}

/**
 * 更新项目
 */
function updateProject(id, updates) {
  const db = getDb();
  
  try {
    const fields = [];
    const values = [];
    
    if (updates.name !== undefined) {
      fields.push('name = ?');
      values.push(updates.name);
    }
    
    if (updates.description !== undefined) {
      fields.push('description = ?');
      values.push(updates.description);
    }
    
    if (updates.status !== undefined) {
      fields.push('status = ?');
      values.push(updates.status);
    }
    
    if (fields.length === 0) {
      throw new Error('No fields to update');
    }
    
    fields.push('updated_at = CURRENT_TIMESTAMP');
    values.push(id);
    
    const stmt = db.prepare(`UPDATE projects SET ${fields.join(', ')} WHERE id = ?`);
    const info = stmt.run(...values);
    
    logger.info(`✅ 项目更新成功：ID ${id}`);
    return { changes: info.changes };
  } catch (error) {
    logger.error(`❌ 更新项目失败 (ID: ${id}):`, error);
    throw error;
  } finally {
    db.close();
  }
}

/**
 * 删除项目
 */
function deleteProject(id) {
  const db = getDb();
  
  try {
    const stmt = db.prepare('DELETE FROM projects WHERE id = ?');
    const info = stmt.run(id);
    
    logger.info(`✅ 项目删除成功：ID ${id}`);
    return { changes: info.changes };
  } catch (error) {
    logger.error(`❌ 删除项目失败 (ID: ${id}):`, error);
    throw error;
  } finally {
    db.close();
  }
}

/**
 * 获取项目统计
 */
function getProjectStats() {
  const db = getDb();
  
  try {
    const stats = db.prepare(`
      SELECT 
        COUNT(*) as total,
        SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active,
        SUM(CASE WHEN status = 'inactive' THEN 1 ELSE 0 END) as inactive
      FROM projects
    `).get();
    return stats;
  } catch (error) {
    logger.error('❌ 获取项目统计失败:', error);
    throw error;
  } finally {
    db.close();
  }
}

module.exports = {
  initDatabase,
  createProject,
  getAllProjects,
  getProjectById,
  updateProject,
  deleteProject,
  getProjectStats
};
