/**
 * Task Dependency Manager - 任务依赖管理器
 * 管理任务之间的依赖关系，确保任务按正确顺序执行
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
 * 初始化任务依赖表
 */
function initDependencies() {
  const db = getDb();
  
  try {
    const createTableSQL = `
      CREATE TABLE IF NOT EXISTS task_dependencies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER NOT NULL,
        depends_on_task_id INTEGER NOT NULL,
        dependency_type TEXT NOT NULL DEFAULT 'BLOCKING',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        resolved_at DATETIME,
        status TEXT NOT NULL DEFAULT 'pending',
        FOREIGN KEY (task_id) REFERENCES tasks(id),
        FOREIGN KEY (depends_on_task_id) REFERENCES tasks(id)
      )
    `;
    
    db.run(createTableSQL);
    
    // 创建索引
    db.run(`
      CREATE INDEX IF NOT EXISTS idx_task_dependencies_task_id 
      ON task_dependencies(task_id)
    `);
    
    db.run(`
      CREATE INDEX IF NOT EXISTS idx_task_dependencies_depends_on 
      ON task_dependencies(depends_on_task_id)
    `);
    
    db.run(`
      CREATE INDEX IF NOT EXISTS idx_task_dependencies_status 
      ON task_dependencies(status)
    `);
    
    logger.info('✅ 任务依赖表初始化完成');
    return true;
  } catch (error) {
    logger.error('❌ 初始化任务依赖表失败:', error);
    return false;
  } finally {
    db.close();
  }
}

/**
 * 添加任务依赖
 */
function addDependency(taskId, dependsOnTaskId, type = 'BLOCKING') {
  const db = getDb();
  
  try {
    // 检查循环依赖
    if (hasCircularDependency(db, taskId, dependsOnTaskId)) {
      logger.warn(`❌ 检测到循环依赖：${taskId} -> ${dependsOnTaskId}`);
      return null;
    }
    
    const insertSQL = `
      INSERT INTO task_dependencies 
      (task_id, depends_on_task_id, dependency_type)
      VALUES (?, ?, ?)
    `;
    
    const insertStmt = db.prepare(insertSQL);
    const result = insertStmt.run(taskId, dependsOnTaskId, type);
    
    logger.info(`✅ 已添加依赖：任务 ${taskId} 依赖于 ${dependsOnTaskId} (${type})`);
    return result.lastInsertRowid;
  } catch (error) {
    logger.error('❌ 添加任务依赖失败:', error);
    return null;
  } finally {
    db.close();
  }
}

/**
 * 检测循环依赖
 */
function hasCircularDependency(db, taskId, dependsOnTaskId) {
  try {
    // 深度优先搜索检测循环
    const visited = new Set();
    const stack = [dependsOnTaskId];
    
    while (stack.length > 0) {
      const current = stack.pop();
      
      if (current === taskId) {
        return true; // 发现循环
      }
      
      if (visited.has(current)) {
        continue;
      }
      
      visited.add(current);
      
      // 查找当前任务依赖的所有任务
      const deps = db.prepare(`
        SELECT depends_on_task_id FROM task_dependencies
        WHERE task_id = ? AND status = 'pending'
      `).all(current);
      
      deps.forEach(dep => {
        stack.push(dep.depends_on_task_id);
      });
    }
    
    return false;
  } catch (error) {
    logger.error('❌ 检测循环依赖失败:', error);
    return false;
  }
}

/**
 * 获取任务的所有依赖
 */
function getTaskDependencies(taskId) {
  const db = getDb();
  
  try {
    const rows = db.prepare(`
      SELECT * FROM task_dependencies
      WHERE task_id = ?
      ORDER BY created_at
    `).all(taskId);
    
    return rows;
  } catch (error) {
    logger.error(`❌ 获取任务依赖失败 (ID: ${taskId}):`, error);
    return [];
  } finally {
    db.close();
  }
}

/**
 * 获取任务的所有被依赖任务
 */
function getDependentTasks(taskId) {
  const db = getDb();
  
  try {
    const rows = db.prepare(`
      SELECT * FROM task_dependencies
      WHERE depends_on_task_id = ?
      ORDER BY created_at
    `).all(taskId);
    
    return rows;
  } catch (error) {
    logger.error(`❌ 获取被依赖任务失败 (ID: ${taskId}):`, error);
    return [];
  } finally {
    db.close();
  }
}

/**
 * 删除任务依赖
 */
function removeDependency(taskId, dependsOnTaskId) {
  const db = getDb();
  
  try {
    const stmt = db.prepare(`
      DELETE FROM task_dependencies
      WHERE task_id = ? AND depends_on_task_id = ?
    `);
    const result = stmt.run(taskId, dependsOnTaskId);
    
    logger.info(`✅ 已删除依赖：任务 ${taskId} -> ${dependsOnTaskId}`);
    return result.changes;
  } catch (error) {
    logger.error('❌ 删除任务依赖失败:', error);
    return 0;
  } finally {
    db.close();
  }
}

/**
 * 更新依赖状态
 */
function updateDependencyStatus(dependencyId, status, resolvedAt = null) {
  const db = getDb();
  
  try {
    const stmt = db.prepare(`
      UPDATE task_dependencies
      SET status = ?, resolved_at = ?
      WHERE id = ?
    `);
    const result = stmt.run(status, resolvedAt || null, dependencyId);
    
    logger.info(`✅ 依赖状态更新成功：ID ${dependencyId} -> ${status}`);
    return result.changes;
  } catch (error) {
    logger.error('❌ 更新依赖状态失败:', error);
    return 0;
  } finally {
    db.close();
  }
}

/**
 * 检查任务是否可以执行
 */
function canExecuteTask(taskId) {
  const db = getDb();
  
  try {
    // 获取任务的所有未完成依赖
    const pendingDeps = db.prepare(`
      SELECT * FROM task_dependencies
      WHERE task_id = ? AND status != 'resolved'
    `).all(taskId);
    
    if (pendingDeps.length === 0) {
      return true;
    }
    
    // 检查所有依赖任务是否都已完成
    for (const dep of pendingDeps) {
      const depTask = db.prepare(`
        SELECT status FROM tasks WHERE id = ?
      `).get(dep.depends_on_task_id);
      
      if (!depTask || depTask.status !== 'completed') {
        return false;
      }
    }
    
    return true;
  } catch (error) {
    logger.error(`❌ 检查任务可执行性失败 (ID: ${taskId}):`, error);
    return false;
  } finally {
    db.close();
  }
}

/**
 * 获取任务执行顺序
 */
function getTaskExecutionOrder(taskIds) {
  const db = getDb();
  
  try {
    // 拓扑排序
    const inDegree = {};
    const graph = {};
    
    // 初始化
    taskIds.forEach(id => {
      inDegree[id] = 0;
      graph[id] = [];
    });
    
    // 构建图
    for (const taskId of taskIds) {
      const deps = db.prepare(`
        SELECT depends_on_task_id FROM task_dependencies
        WHERE task_id = ? AND depends_on_task_id IN (${taskIds.map(() => '?').join(',')})
      `).all(taskId, ...taskIds);
      
      for (const dep of deps) {
        if (graph[dep.depends_on_task_id]) {
          graph[dep.depends_on_task_id].push(taskId);
          inDegree[taskId]++;
        }
      }
    }
    
    // 拓扑排序
    const queue = [];
    const result = [];
    
    // 找到所有入度为 0 的任务
    for (const taskId of taskIds) {
      if (inDegree[taskId] === 0) {
        queue.push(taskId);
      }
    }
    
    while (queue.length > 0) {
      const current = queue.shift();
      result.push(current);
      
      for (const next of graph[current]) {
        inDegree[next]--;
        if (inDegree[next] === 0) {
          queue.push(next);
        }
      }
    }
    
    // 检查是否有循环依赖
    if (result.length !== taskIds.length) {
      logger.warn('⚠️ 检测到循环依赖，无法确定执行顺序');
      return [];
    }
    
    return result;
  } catch (error) {
    logger.error('❌ 获取任务执行顺序失败:', error);
    return [];
  } finally {
    db.close();
  }
}

module.exports = {
  initDependencies,
  addDependency,
  removeDependency,
  getTaskDependencies,
  getDependentTasks,
  updateDependencyStatus,
  canExecuteTask,
  getTaskExecutionOrder,
  hasCircularDependency
};
