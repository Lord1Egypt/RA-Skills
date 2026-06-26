/**
 * Enhanced Main Controller - 增强主控制器
 * 整合数据库任务管理 + OpenClaw 原生 Agent 调度
 * 提供完整的任务队列管理和自动处理功能
 */

const { Database } = require('../db/database');
const { OpenClawAgentOrchestrator } = require('./openclaw-agent-orchestrator');
const { OpenClawTools } = require('./openclaw-tools');
const DatabaseManager = require('../db/database-manager');

class EnhancedMainController {
    constructor(config = {}) {
        this.config = {
            dbPath: config.dbPath || process.env.GITHUB_COLLAB_DB_PATH || './github-collab.db',
            maxParallelAgents: config.maxParallelAgents || 3,
            agentTimeout: config.agentTimeout || 300,
            autoRecovery: config.autoRecovery !== false,
            autoProcessQueue: config.autoProcessQueue !== false,
            processQueueInterval: config.processQueueInterval || 5000,
            defaultModel: config.defaultModel || 'ollama/qwen3.5-code',
            ...config
        };

        this.db = null;
        this.dbWrapper = null;
        this.orchestrator = null;
        this.tools = null;
        
        this.running = false;
        this.queueProcessor = null;
        this.cleanupInterval = null;

        this.logger = {
            info: (msg) => console.log(`[EnhancedController] ${msg}`),
            warn: (msg) => console.warn(`[EnhancedController] ${msg}`),
            error: (msg) => console.error(`[EnhancedController] ${msg}`),
            debug: (msg) => console.log(`[EnhancedController DEBUG] ${msg}`)
        };
    }

    /**
     * 初始化控制器
     */
    async initialize() {
        this.logger.info('Initializing Enhanced Main Controller...');

        try {
            // 1. 初始化数据库
            await this.initializeDatabase();

            // 2. 初始化 Orchestrator
            await this.initializeOrchestrator();

            // 3. 初始化 Tools
            this.initializeTools();

            // 4. 恢复未完成任务
            if (this.config.autoRecovery) {
                await this.recoverIncompleteTasks();
            }

            this.logger.info('Enhanced Main Controller initialized successfully');
            return { success: true };
        } catch (error) {
            this.logger.error(`Failed to initialize: ${error.message}`);
            return { success: false, error: error.message };
        }
    }

    /**
     * 初始化数据库
     */
    async initializeDatabase() {
        this.logger.info(`Initializing database: ${this.config.dbPath}`);

        try {
            // 使用 DatabaseManager 初始化数据库
            this.dbWrapper = new DatabaseManager(this.config.dbPath);
            await this.dbWrapper.initialize();
            this.db = this.dbWrapper.getDatabaseInstance();

            this.logger.info('Database initialized successfully');
            return { success: true };
        } catch (error) {
            this.logger.error(`Failed to initialize database: ${error.message}`);
            throw error;
        }
    }

    /**
     * 初始化 Orchestrator
     */
    async initializeOrchestrator() {
        this.logger.info('Initializing Agent Orchestrator...');

        try {
            this.orchestrator = new OpenClawAgentOrchestrator({
                defaultModel: this.config.defaultModel,
                maxParallelAgents: this.config.maxParallelAgents,
                agentTimeout: this.config.agentTimeout,
                autoRecovery: this.config.autoRecovery
            });

            this.logger.info('Agent Orchestrator initialized successfully');
            return { success: true };
        } catch (error) {
            this.logger.error(`Failed to initialize orchestrator: ${error.message}`);
            throw error;
        }
    }

    /**
     * 初始化 Tools
     */
    initializeTools() {
        this.tools = new OpenClawTools({
            defaultModel: this.config.defaultModel,
            defaultTimeout: this.config.agentTimeout
        });
    }

    /**
     * 恢复未完成任务
     */
    async recoverIncompleteTasks() {
        this.logger.info('Recovering incomplete tasks...');

        try {
            // 获取所有 in_progress 状态的任务
            const tasks = await this.db.getTasks();
            const incompleteTasks = tasks.filter(t => 
                t.status === 'in_progress' || t.status === 'pending'
            );

            this.logger.info(`Found ${incompleteTasks.length} incomplete tasks`);

            for (const task of incompleteTasks) {
                // 重新分配任务
                await this.processSingleTask(task.id);
            }

            this.logger.info('Task recovery complete');
        } catch (error) {
            this.logger.error(`Failed to recover tasks: ${error.message}`);
        }
    }

    /**
     * 创建任务
     * @param {object} taskData - 任务数据
     * @returns {Promise<object>} 创建结果
     */
    async createTask(taskData) {
        this.logger.info(`Creating task: ${taskData.title}`);

        try {
            const task = await this.db.createTask(taskData);
            
            // 自动添加到处理队列
            if (this.config.autoProcessQueue) {
                // 任务创建后会自动被队列处理器处理
                this.logger.info(`Task ${task.id} created and will be auto-processed`);
            }

            return { success: true, task };
        } catch (error) {
            this.logger.error(`Failed to create task: ${error.message}`);
            return { success: false, error: error.message };
        }
    }

    /**
     * 获取任务
     * @param {number} taskId - 任务 ID
     * @returns {Promise<object>} 任务对象
     */
    async getTask(taskId) {
        return await this.db.getTask(taskId);
    }

    /**
     * 更新任务
     * @param {number} taskId - 任务 ID
     * @param {object} updates - 更新数据
     * @returns {Promise<object>} 更新结果
     */
    async updateTask(taskId, updates) {
        this.logger.info(`Updating task ${taskId}: ${JSON.stringify(updates)}`);

        try {
            // 获取当前任务
            const task = await this.db.getTask(taskId);
            if (!task) {
                return { success: false, error: 'Task not found' };
            }

            // 合并更新
            const updatedTask = { ...task, ...updates, updated_at: new Date().toISOString() };

            // 更新到数据库（手动执行 SQL）
            const fields = Object.keys(updates).filter(f => 
                ['title', 'description', 'priority', 'status', 'assignee_id'].includes(f)
            );

            if (fields.length > 0) {
                const setClause = fields.map(f => `${f} = ?`).join(', ');
                const values = [
                    ...fields.map(f => updates[f]),
                    new Date().toISOString(),
                    taskId
                ];

                await this.db.db.prepare(`
                    UPDATE tasks SET ${setClause}, updated_at = ? WHERE id = ?
                `).run(...values);
            }

            return { success: true, task: await this.db.getTask(taskId) };
        } catch (error) {
            this.logger.error(`Failed to update task: ${error.message}`);
            return { success: false, error: error.message };
        }
    }

    /**
     * 删除任务
     * @param {number} taskId - 任务 ID
     * @returns {Promise<object>} 删除结果
     */
    async deleteTask(taskId) {
        this.logger.info(`Deleting task ${taskId}`);

        try {
            // 如果任务已分配给 Agent，先终止 Agent
            const agentKey = this.orchestrator.taskToAgent.get(taskId);
            if (agentKey) {
                await this.orchestrator.terminateAgent(agentKey);
            }

            const result = await this.db.deleteTask(taskId);
            return { success: true, ...result };
        } catch (error) {
            this.logger.error(`Failed to delete task: ${error.message}`);
            return { success: false, error: error.message };
        }
    }

    /**
     * 处理单个任务
     * @param {number} taskId - 任务 ID
     * @returns {Promise<object>} 处理结果
     */
    async processSingleTask(taskId) {
        this.logger.info(`Processing task ${taskId}`);

        try {
            // 1. 获取任务
            const task = await this.db.getTask(taskId);
            if (!task) {
                return { success: false, error: 'Task not found' };
            }

            // 2. 检查任务状态
            if (task.status === 'completed') {
                this.logger.info(`Task ${taskId} already completed`);
                return { success: true, task };
            }

            // 3. 更新任务状态为 in_progress
            await this.updateTaskStatus(taskId, 'in_progress');

            // 4. 查找空闲 Agent 或创建新 Agent
            const idleAgents = this.orchestrator.getIdleAgents('coder');
            let agentKey = null;

            if (idleAgents.length > 0) {
                // 使用空闲 Agent
                agentKey = idleAgents[0].sessionKey;
                this.logger.info(`Using existing idle agent: ${agentKey}`);
            } else {
                // 创建新 Agent
                const createResult = await this.orchestrator.createAgent({
                    task: task.description || task.title,
                    agentType: 'coder',
                    label: `task-${taskId}-coder`,
                    persistent: true
                });

                if (!createResult.success) {
                    await this.updateTaskStatus(taskId, 'pending');
                    return createResult;
                }

                agentKey = createResult.sessionKey;
            }

            // 5. 记录任务-Agent 映射
            this.orchestrator.taskToAgent.set(taskId, agentKey);

            // 6. 发送任务给 Agent
            const taskPrompt = this.buildTaskPrompt(task);
            await this.orchestrator.sendToAgent(agentKey, taskPrompt);

            this.logger.info(`Task ${taskId} assigned to agent ${agentKey}`);

            return {
                success: true,
                taskId,
                agentKey,
                status: 'processing'
            };
        } catch (error) {
            this.logger.error(`Failed to process task ${taskId}: ${error.message}`);
            return { success: false, error: error.message };
        }
    }

    /**
     * 构建任务提示
     * @param {object} task - 任务对象
     * @returns {string} 任务提示
     */
    buildTaskPrompt(task) {
        const prompt = `
## 任务详情

**标题**: ${task.title}
**描述**: ${task.description || '无'}
**优先级**: ${task.priority || '中'}
**任务 ID**: ${task.id}

## 要求

请完成以下任务：
1. 分析任务需求
2. 编写完整、可运行的代码
3. 提供单元测试
4. 说明风险和注意事项

## 输出格式

【功能说明】
【代码实现】
【单元测试】
【测试预期结果】
【风险与注意事项】
        `.trim();

        return prompt;
    }

    /**
     * 更新任务状态
     * @param {number} taskId - 任务 ID
     * @param {string} status - 新状态
     * @returns {Promise<object>} 更新结果
     */
    async updateTaskStatus(taskId, status) {
        this.logger.info(`Updating task ${taskId} status to ${status}`);

        try {
            const result = await this.orchestrator.updateTaskStatus(taskId, status, this.db);
            
            // 发送通知
            if (status === 'completed') {
                await this.sendNotification(`Task ${taskId} completed`);
            }

            return result;
        } catch (error) {
            this.logger.error(`Failed to update task status: ${error.message}`);
            return { success: false, error: error.message };
        }
    }

    /**
     * 发送通知
     * @param {string} message - 通知内容
     */
    async sendNotification(message) {
        // TODO: 实现通知功能
        this.logger.info(`Notification: ${message}`);
    }

    /**
     * 处理任务队列
     * 自动处理 pending 状态的任务
     */
    async processQueue() {
        if (!this.config.autoProcessQueue) {
            return;
        }

        this.logger.info('Starting queue processor...');

        try {
            // 获取所有 pending 任务
            const tasks = await this.db.getTasks();
            const pendingTasks = tasks.filter(t => t.status === 'pending');

            this.logger.info(`Found ${pendingTasks.length} pending tasks`);

            // 按优先级排序
            pendingTasks.sort((a, b) => (a.priority || 10) - (b.priority || 10));

            // 处理每个任务
            for (const task of pendingTasks) {
                // 检查并行限制
                const activeCount = this.orchestrator.getActiveAgentCount();
                if (activeCount >= this.config.maxParallelAgents) {
                    this.logger.info(`Max parallel agents reached (${activeCount}), waiting...`);
                    break;
                }

                await this.processSingleTask(task.id);
            }
        } catch (error) {
            this.logger.error(`Queue processing error: ${error.message}`);
        }
    }

    /**
     * 启动控制器
     */
    async start() {
        if (this.running) {
            this.logger.warn('Controller already running');
            return;
        }

        this.running = true;
        this.logger.info('Starting Enhanced Main Controller...');

        // 启动队列处理器
        if (this.config.autoProcessQueue) {
            this.queueProcessor = setInterval(async () => {
                await this.processQueue();
            }, this.config.processQueueInterval);

            // 启动清理任务
            this.cleanupInterval = setInterval(async () => {
                await this.orchestrator.cleanupOfflineAgents();
            }, 60000); // 每分钟清理一次
        }

        // 执行首次队列处理
        await this.processQueue();

        this.logger.info('Enhanced Main Controller started');
    }

    /**
     * 停止控制器
     */
    async stop() {
        this.running = false;
        this.logger.info('Stopping Enhanced Main Controller...');

        // 停止队列处理器
        if (this.queueProcessor) {
            clearInterval(this.queueProcessor);
            this.queueProcessor = null;
        }

        // 停止清理任务
        if (this.cleanupInterval) {
            clearInterval(this.cleanupInterval);
            this.cleanupInterval = null;
        }

        // 关闭数据库
        if (this.dbWrapper) {
            await this.dbWrapper.close();
        }

        this.logger.info('Enhanced Main Controller stopped');
    }

    /**
     * 获取任务统计
     * @returns {Promise<object>} 任务统计
     */
    async getTaskStats() {
        return await this.db.getTaskStats();
    }

    /**
     * 获取活跃 Agent 列表
     * @returns {Array} Agent 列表
     */
    async getActiveAgents() {
        return await this.orchestrator.listAgents();
    }
}

module.exports = { EnhancedMainController };
