/**
 * Main Controller - 总控主进程
 * 控制 Agent 启动、停止、并行数量、任务调度
 */

const path = require('path');
const fs = require('fs');

class MainController {
    constructor(config = {}) {
        this.config = {
            maxParallelAgents: config.maxParallelAgents || 3,
            agentTypes: config.agentTypes || ['dev', 'test', 'review'],
            autoRecovery: config.autoRecovery !== false,
            priorityThreshold: config.priorityThreshold || 5,
            ...config
        };
        
        this.agents = new Map();
        this.taskQueue = [];
        this.running = false;
        this.locks = new Map();
        this.recoveryAttempts = new Map();
        
        this.logger = this.createLogger();
    }

    /**
     * 创建日志器
     */
    createLogger() {
        return {
            info: (msg) => console.log(`[INFO] ${msg}`),
            warn: (msg) => console.warn(`[WARN] ${msg}`),
            error: (msg) => console.error(`[ERROR] ${msg}`),
            debug: (msg) => console.log(`[DEBUG] ${msg}`)
        };
    }

    /**
     * 初始化控制器
     */
    async initialize() {
        this.logger.info('Main Controller initializing...');
        
        // 加载配置
        await this.loadConfig();
        
        // 恢复未完成任务
        if (this.config.autoRecovery) {
            await this.recoverTasks();
        }
        
        this.logger.info('Main Controller initialized');
    }

    /**
     * 加载配置
     */
    async loadConfig() {
        const configPath = path.join(__dirname, '.github-collab-config.json');
        if (fs.existsSync(configPath)) {
            try {
                const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
                Object.assign(this.config, config);
                this.logger.info('Configuration loaded');
            } catch (error) {
                this.logger.error('Failed to load config:', error.message);
            }
        }
    }

    /**
     * 启动 Agent
     * @param {string} agentType - Agent 类型
     * @param {string} agentId - Agent ID
     * @param {object} options - 选项
     */
    async startAgent(agentType, agentId = null, options = {}) {
        // 检查并行数量限制
        const runningAgents = Array.from(this.agents.values()).filter(a => a.running);
        if (runningAgents.length >= this.config.maxParallelAgents) {
            this.logger.warn(`Max parallel agents (${this.config.maxParallelAgents}) reached`);
            return null;
        }

        // 生成 Agent ID
        if (!agentId) {
            agentId = `${agentType}-agent-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
        }

        // 动态加载 Agent 类
        let AgentClass;
        try {
            switch (agentType.toLowerCase()) {
                case 'dev':
                    const DevModule = require('./dev-agent');
                    AgentClass = DevModule.DevAgent;
                    break;
                case 'test':
                    const TestModule = require('./test-agent');
                    AgentClass = TestModule.TestAgent;
                    break;
                case 'review':
                    // 未来扩展
                    this.logger.warn('Review agent not implemented yet');
                    return null;
                default:
                    this.logger.error(`Unknown agent type: ${agentType}`);
                    return null;
            }
        } catch (error) {
            this.logger.error(`Failed to load ${agentType} agent:`, error.message);
            return null;
        }

        // 创建 Agent 实例
        const agent = new AgentClass(agentId);
        agent.controller = this; // 设置控制器引用
        
        try {
            await agent.initialize();
            agent.running = true;
            this.agents.set(agentId, agent);
            
            this.logger.info(`Agent ${agentId} started (type: ${agentType})`);
            
            // 启动崩溃恢复监听
            if (this.config.autoRecovery) {
                this.setupCrashRecovery(agent);
            }
            
            return agent;
        } catch (error) {
            this.logger.error(`Failed to start agent ${agentId}:`, error.message);
            return null;
        }
    }

    /**
     * 停止 Agent
     * @param {string} agentId - Agent ID
     */
    async stopAgent(agentId) {
        const agent = this.agents.get(agentId);
        if (!agent) {
            this.logger.warn(`Agent ${agentId} not found`);
            return false;
        }

        try {
            agent.running = false;
            await agent.shutdown();
            this.agents.delete(agentId);
            
            this.logger.info(`Agent ${agentId} stopped`);
            return true;
        } catch (error) {
            this.logger.error(`Failed to stop agent ${agentId}:`, error.message);
            return false;
        }
    }

    /**
     * 设置最大并行 Agent 数量
     * @param {number} count - 数量
     */
    setMaxParallelAgents(count) {
        this.config.maxParallelAgents = count;
        this.logger.info(`Max parallel agents set to ${count}`);
    }

    /**
     * 获取当前运行的 Agent 数量
     */
    getRunningAgentCount() {
        return Array.from(this.agents.values()).filter(a => a.running).length;
    }

    /**
     * 添加任务到队列
     * @param {object} task - 任务对象
     * @param {string} agentType - 目标 Agent 类型
     */
    async addTask(task, agentType = 'dev') {
        // 检查依赖
        const dependenciesMet = await this.checkTaskDependencies(task);
        
        if (!dependenciesMet) {
            // 依赖未满足，降级优先级
            task.priority = Math.min(task.priority || 10, this.config.priorityThreshold - 1);
            this.logger.info(`Task ${task.id} dependencies not met, priority lowered to ${task.priority}`);
        }

        // 添加到队列
        this.taskQueue.push({
            task,
            agentType,
            addedAt: Date.now(),
            dependenciesMet
        });

        // 按优先级排序
        this.taskQueue.sort((a, b) => b.task.priority - a.task.priority);

        this.logger.info(`Task ${task.id} added to queue (priority: ${task.priority})`);
    }

    /**
     * 检查任务依赖
     */
    async checkTaskDependencies(task) {
        if (!task.dependencies || task.dependencies.length === 0) {
            return true;
        }

        for (const depId of task.dependencies) {
            const depTask = await this.getTask(depId);
            if (!depTask || depTask.status !== 'completed') {
                return false;
            }
        }

        return true;
    }

    /**
     * 获取任务
     */
    async getTask(taskId) {
        // 从任务管理器获取
        const TaskManager = require('./task-manager-enhanced');
        const taskManager = new TaskManager.TaskManagerEnhanced({
            dbPath: this.config.dbPath || process.env.GITHUB_COLLAB_DB_PATH || './github-collab.db'
        });
        return await taskManager.getTask(taskId);
    }

    /**
     * 处理任务队列
     */
    async processQueue() {
        while (this.running && this.taskQueue.length > 0) {
            // 检查是否有可用 Agent
            const runningAgents = Array.from(this.agents.values()).filter(a => a.running);
            
            if (runningAgents.length === 0) {
                // 没有运行中的 Agent，等待或启动新 Agent
                await this.delay(1000);
                continue;
            }

            // 获取最高优先级任务
            const queueItem = this.taskQueue[0];
            const task = queueItem.task;

            // 检查依赖
            const dependenciesMet = await this.checkTaskDependencies(task);
            
            if (!dependenciesMet) {
                // 依赖未满足，移到队列末尾并降级
                this.taskQueue.shift();
                task.priority = Math.min(task.priority || 10, this.config.priorityThreshold - 1);
                this.taskQueue.push(queueItem);
                this.taskQueue.sort((a, b) => b.task.priority - a.task.priority);
                await this.delay(500);
                continue;
            }

            // 分配任务给 Agent
            const agent = this.findAvailableAgent(queueItem.agentType);
            if (agent) {
                this.taskQueue.shift();
                await this.assignTaskToAgent(task, agent);
            } else {
                // 没有可用 Agent，等待
                await this.delay(1000);
            }
        }
    }

    /**
     * 查找可用 Agent
     */
    findAvailableAgent(agentType) {
        return Array.from(this.agents.values()).find(
            a => a.running && a.type === agentType && !a.busy
        );
    }

    /**
     * 分配任务给 Agent
     */
    async assignTaskToAgent(task, agent) {
        try {
            agent.busy = true;
            await agent.processTask(task);
            agent.busy = false;
        } catch (error) {
            this.logger.error(`Failed to assign task ${task.id} to agent ${agent.id}:`, error.message);
            agent.busy = false;
            
            // 崩溃恢复
            if (this.config.autoRecovery) {
                await this.handleTaskFailure(task, agent, error);
            }
        }
    }

    /**
     * 处理任务失败
     */
    async handleTaskFailure(task, agent, error) {
        const attempts = this.recoveryAttempts.get(task.id) || 0;
        
        if (attempts < 3) {
            this.recoveryAttempts.set(task.id, attempts + 1);
            this.logger.warn(`Task ${task.id} failed, retry ${attempts + 1}/3`);
            
            // 重新添加到队列
            await this.addTask(task, agent.type);
        } else {
            this.logger.error(`Task ${task.id} failed after 3 attempts`);
        }
    }

    /**
     * 设置崩溃恢复
     */
    setupCrashRecovery(agent) {
        // 监听进程崩溃
        process.on('SIGTERM', async () => {
            this.logger.info('Received SIGTERM, saving state...');
            await this.saveState();
        });

        process.on('uncaughtException', async (error) => {
            this.logger.error('Uncaught exception:', error);
            await this.saveState();
        });
    }

    /**
     * 恢复任务
     */
    async recoverTasks() {
        const statePath = path.join(__dirname, 'controller-state.json');
        if (fs.existsSync(statePath)) {
            try {
                const state = JSON.parse(fs.readFileSync(statePath, 'utf-8'));
                
                this.logger.info(`Recovering ${state.pendingTasks.length} pending tasks`);
                
                for (const task of state.pendingTasks) {
                    await this.addTask(task, task.agentType || 'dev');
                }
                
                this.logger.info('Task recovery complete');
            } catch (error) {
                this.logger.error('Failed to recover tasks:', error.message);
            }
        }
    }

    /**
     * 保存状态
     */
    async saveState() {
        const state = {
            timestamp: Date.now(),
            pendingTasks: this.taskQueue.map(item => ({
                task: item.task,
                agentType: item.agentType
            })),
            runningAgents: Array.from(this.agents.keys())
        };

        const statePath = path.join(__dirname, 'controller-state.json');
        fs.writeFileSync(statePath, JSON.stringify(state, null, 2));
        
        this.logger.info('State saved');
    }

    /**
     * 启动控制器
     */
    async start() {
        this.running = true;
        this.logger.info('Main Controller started');
        
        // 启动任务队列处理
        this.processQueue();
    }

    /**
     * 停止控制器
     */
    async stop() {
        this.running = false;
        
        // 停止所有 Agent
        for (const [id, agent] of this.agents) {
            await this.stopAgent(id);
        }
        
        // 保存状态
        await this.saveState();
        
        this.logger.info('Main Controller stopped');
    }

    /**
     * 延迟
     */
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

module.exports = { MainController };