/**
 * GitHub Collaboration Skill - Main Entry
 * GitHub 项目协作开发技能
 * 
 * @module github-collab
 */

// 核心模块
const TaskManager = require('./core/task-manager').TaskManager;
const AgentManager = require('./core/agent-manager').AgentManager;
const ProjectManager = require('./core/project-manager').ProjectManager;
const ConfigManager = require('./core/config-manager').ConfigManager;

// 数据库层
const Database = require('./db/database');

// 工具函数
const Logger = require('./utils/logger');
const Cache = require('./utils/cache');
const Helpers = require('./utils/helpers');

// 导出所有模块
module.exports = {
    // 核心模块
    TaskManager,
    AgentManager,
    ProjectManager,
    ConfigManager,
    
    // 数据库
    Database,
    
    // 工具
    Logger,
    Cache,
    Helpers
};

/**
 * 快速开始示例
 */
async function quickStart() {
    const { TaskManager, AgentManager, ProjectManager } = module.exports;
    
    // 初始化配置
    const config = new ConfigManager();
    await config.initialize();
    
    // 初始化数据库
    const db = new Database();
    await db.connect();
    
    // 创建任务管理器
    const taskManager = new TaskManager(db);
    
    // 创建项目
    const project = await taskManager.createProject({
        name: 'Example Project',
        description: 'An example project',
        github_url: 'https://github.com/example/repo'
    });
    
    console.log(`Created project: ${project.id}`);
    
    // 创建任务
    const task = await taskManager.createTask({
        project_id: project.id,
        name: 'Implement feature',
        description: 'Implement new feature',
        priority: 10
    });
    
    console.log(`Created task: ${task.id}`);
    
    // 初始化 Agent
    const agentManager = new AgentManager(db);
    await agentManager.initialize();
    
    // 关闭数据库连接
    await db.close();
}

// 如果直接运行此文件
if (require.main === module) {
    quickStart().catch(console.error);
}
