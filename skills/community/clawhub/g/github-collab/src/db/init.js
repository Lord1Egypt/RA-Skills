/**
 * Database Initialization
 * 统一数据库初始化脚本 - 支持 Agent 和任务管理
 */

const Database = require('better-sqlite3');
const path = require('path');

// 支持从环境变量或配置指定数据库路径
const DB_PATH = process.env.DB_PATH || 
                process.env.OPENCLAW_DB_PATH || 
                path.join(__dirname, 'agents.db');

/**
 * 初始化数据库
 * @param {string} dbPath - 可选的数据库路径
 * @returns {Database}
 */
function initDatabase(dbPath = null) {
  const targetPath = dbPath || DB_PATH;
  
  const db = new Database(targetPath);
  console.log('✅ 数据库已打开:', targetPath);
  
  // 创建 agents 表
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
  console.log('✅ agents 表已创建');
  
  // 创建 agent_configs 表（存储额外配置）
  db.exec(`
    CREATE TABLE IF NOT EXISTS agent_configs (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      agent_name TEXT NOT NULL,
      config_key TEXT NOT NULL,
      config_value TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      UNIQUE(agent_name, config_key)
    )
  `);
  console.log('✅ agent_configs 表已创建');
  
  // 创建消息日志表
  db.exec(`
    CREATE TABLE IF NOT EXISTS message_logs (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      from_agent TEXT,
      to_agent TEXT,
      message TEXT,
      status TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);
  console.log('✅ message_logs 表已创建');
  
  // 创建 tasks 表（任务管理）
  db.exec(`
    CREATE TABLE IF NOT EXISTS tasks (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      task_id TEXT UNIQUE NOT NULL,
      title TEXT NOT NULL,
      description TEXT,
      status TEXT DEFAULT 'pending',
      priority TEXT DEFAULT 'medium',
      assignee TEXT,
      created_by TEXT,
      github_issue_number INTEGER,
      github_repo TEXT,
      metadata TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);
  console.log('✅ tasks 表已创建');
  
  // 创建 task_assignments 表（任务分配历史）
  db.exec(`
    CREATE TABLE IF NOT EXISTS task_assignments (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      task_id TEXT NOT NULL,
      agent_name TEXT NOT NULL,
      assigned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      completed_at DATETIME,
      status TEXT DEFAULT 'assigned',
      notes TEXT,
      FOREIGN KEY (task_id) REFERENCES tasks(task_id)
    )
  `);
  console.log('✅ task_assignments 表已创建');
  
  // 创建 task_history 表（任务变更历史）
  db.exec(`
    CREATE TABLE IF NOT EXISTS task_history (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      task_id TEXT NOT NULL,
      action TEXT NOT NULL,
      old_value TEXT,
      new_value TEXT,
      changed_by TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (task_id) REFERENCES tasks(task_id)
    )
  `);
  console.log('✅ task_history 表已创建');
  
  return db;
}

/**
 * 初始化默认 Agent 数据
 */
function initDefaultAgents(db) {
  const defaultAgents = [
    {
      name: 'main-agent',
      role: 'main',
      target: 'qqbot:c2c:MAIN_AGENT_PLACEHOLDER',
      description: '任务管理与调度',
      capabilities: JSON.stringify(['task-management', 'scheduling', 'reporting'])
    },
    {
      name: 'coder-agent',
      role: 'coder',
      target: 'qqbot:c2c:CODER_AGENT_PLACEHOLDER',
      description: '代码开发',
      capabilities: JSON.stringify(['code-writing', 'debugging', 'testing'])
    },
    {
      name: 'checker-agent',
      role: 'checker',
      target: 'qqbot:c2c:CHECKER_AGENT_PLACEHOLDER',
      description: '审查测试',
      capabilities: JSON.stringify(['code-review', 'testing', 'quality-assurance'])
    },
    {
      name: 'memowriter-agent',
      role: 'memowriter',
      target: 'qqbot:c2c:MEMOWRITER_AGENT_PLACEHOLDER',
      description: '文档记录',
      capabilities: JSON.stringify(['documentation', 'reporting', 'knowledge-management'])
    }
  ];

  let insertedCount = 0;
  defaultAgents.forEach(agent => {
    try {
      db.prepare(`
        INSERT OR REPLACE INTO agents (name, role, target, description, capabilities, is_active)
        VALUES (?, ?, ?, ?, ?, 1)
      `).run(agent.name, agent.role, agent.target, agent.description, agent.capabilities);
      insertedCount++;
    } catch (err) {
      console.error(`❌ 插入 Agent ${agent.name} 失败:`, err.message);
    }
  });
  
  console.log(`✅ 已初始化 ${insertedCount} 个默认 Agent`);
}

/**
 * 主初始化函数
 * @param {string} dbPath - 可选的数据库路径
 */
function main(dbPath = null) {
  try {
    console.log('🚀 开始初始化数据库...\n');
    
    const db = initDatabase(dbPath);
    initDefaultAgents(db);
    
    console.log('\n✅ 数据库初始化完成！');
    
    // 关闭数据库连接
    db.close();
    console.log('✅ 数据库已关闭');
  } catch (error) {
    console.error('❌ 初始化失败:', error);
    process.exit(1);
  }
}

// 如果直接运行此文件
if (require.main === module) {
  const dbPath = process.argv[2];
  main(dbPath);
}

module.exports = { initDatabase, initDefaultAgents, DB_PATH };
