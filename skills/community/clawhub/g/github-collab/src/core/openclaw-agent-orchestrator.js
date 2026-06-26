/**
 * OpenClaw Agent Orchestrator - OpenClaw Agent 调度器
 * 使用 OpenClaw 原生 sessions_spawn 创建和管理子 Agent
 * 集成数据库任务状态同步
 */

const { OpenClawTools } = require('./openclaw-tools');

class OpenClawAgentOrchestrator {
    constructor(config = {}) {
        this.config = {
            defaultModel: config.defaultModel || 'ollama/qwen3.5-code',
            maxParallelAgents: config.maxParallelAgents || 3,
            agentTimeout: config.agentTimeout || 300,
            autoRecovery: config.autoRecovery !== false,
            ...config
        };

        this.tools = new OpenClawTools({
            defaultModel: this.config.defaultModel,
            defaultTimeout: this.config.agentTimeout
        });

        this.activeAgents = new Map(); // sessionKey -> agentInfo
        this.taskToAgent = new Map(); // taskId -> sessionKey
        this.agentTypes = new Map(); // agentType -> capabilities

        // 初始化 Agent 类型配置
        this.initializeAgentTypes();

        this.logger = {
            info: (msg) => console.log(`[Orchestrator] ${msg}`),
            warn: (msg) => console.warn(`[Orchestrator] ${msg}`),
            error: (msg) => console.error(`[Orchestrator] ${msg}`),
            debug: (msg) => console.log(`[Orchestrator DEBUG] ${msg}`)
        };
    }

    /**
     * 初始化 Agent 类型配置
     */
    initializeAgentTypes() {
        this.agentTypes.set('coder', {
            capabilities: ['code-writing', 'debugging', 'testing'],
            description: '代码开发智能体',
            promptPrefix: '你是专业的代码开发助手，负责编写高质量、可测试的代码。'
        });

        this.agentTypes.set('tester', {
            capabilities: ['testing', 'debugging', 'quality-assurance'],
            description: '测试智能体',
            promptPrefix: '你是专业的测试工程师，负责设计测试用例、执行测试、发现 bug。'
        });

        this.agentTypes.set('reviewer', {
            capabilities: ['code-review', 'quality-assurance'],
            description: '代码审查智能体',
            promptPrefix: '你是资深代码审查专家，负责代码审查、质量把控、最佳实践建议。'
        });

        this.agentTypes.set('architect', {
            capabilities: ['architecture', 'design', 'planning'],
            description: '架构设计智能体',
            promptPrefix: '你是资深系统架构师，负责系统设计、技术选型、架构规划。'
        });
    }

    /**
     * 创建子 Agent
     * 使用 sessions_spawn 创建独立的子 Agent 会话
     * 
     * @param {object} options - 创建选项
     * @param {string} options.task - 任务描述
     * @param {string} options.agentType - Agent 类型 (coder|tester|reviewer|architect)
     * @param {string} options.label - 会话标签
     * @param {string} options.model - 使用的模型
     * @param {boolean} options.persistent - 是否持久化会话
     * @returns {Promise<object>} 创建结果
     */
    async createAgent(options) {
        const {
            task,
            agentType = 'coder',
            label = null,
            model = this.config.defaultModel,
            persistent = false
        } = options;

        // 检查并行限制
        const activeCount = this.activeAgents.size;
        if (activeCount >= this.config.maxParallelAgents) {
            this.logger.warn(`Max parallel agents (${this.config.maxParallelAgents}) reached`);
            return {
                success: false,
                error: 'Max parallel agents limit reached',
                waiting: true
            };
        }

        // 获取 Agent 类型配置
        const typeConfig = this.agentTypes.get(agentType);
        if (!typeConfig) {
            this.logger.error(`Unknown agent type: ${agentType}`);
            return {
                success: false,
                error: `Unknown agent type: ${agentType}`
            };
        }

        // 生成标签
        const agentLabel = label || `${agentType}-agent-${Date.now()}`;

        // 构建任务提示
        const enhancedTask = this.buildAgentPrompt(task, agentType, typeConfig);

        this.logger.info(`Creating ${agentType} agent: ${agentLabel}`);

        try {
            // 使用 OpenClaw 原生 sessions_spawn 创建子 Agent
            const result = await this.tools.spawnSubAgent({
                task: enhancedTask,
                label: agentLabel,
                runtime: 'subagent',
                mode: persistent ? 'session' : 'run',
                model,
                timeoutSeconds: this.config.agentTimeout,
                thread: false
            });

            if (result.success) {
                // 记录 Agent 信息
                const sessionKey = result.sessionKey || agentLabel;
                this.activeAgents.set(sessionKey, {
                    label: agentLabel,
                    type: agentType,
                    task: task,
                    model,
                    persistent,
                    createdAt: new Date().toISOString(),
                    status: 'running'
                });

                this.logger.info(`Agent created successfully: ${sessionKey}`);

                return {
                    success: true,
                    sessionKey,
                    label: agentLabel,
                    type: agentType,
                    status: 'running'
                };
            } else {
                return result;
            }
        } catch (error) {
            this.logger.error(`Failed to create agent: ${error.message}`);
            return {
                success: false,
                error: error.message
            };
        }
    }

    /**
     * 构建 Agent 提示
     * @param {string} task - 原始任务
     * @param {string} agentType - Agent 类型
     * @param {object} typeConfig - 类型配置
     * @returns {string} 增强后的任务描述
     */
    buildAgentPrompt(task, agentType, typeConfig) {
        const promptParts = [
            typeConfig.promptPrefix,
            '',
            '## 任务要求',
            task,
            '',
            '## 输出格式',
            '请按照以下格式输出：',
            '【功能说明】',
            '【代码实现】',
            '【单元测试】',
            '【测试预期结果】',
            '【风险与注意事项】',
            '',
            '## 要求',
            '- 代码必须完整、可运行',
            '- 必须包含单元测试',
            '- 主动说明风险和依赖'
        ];

        return promptParts.join('\n');
    }

    /**
     * 向 Agent 发送消息
     * 使用 sessions_send 向指定 Agent 发送消息
     * 
     * @param {string} sessionKey - Agent 会话密钥
     * @param {string} message - 消息内容
     * @param {number} timeoutSeconds - 超时时间
     * @returns {Promise<object>} 发送结果
     */
    async sendToAgent(sessionKey, message, timeoutSeconds = null) {
        if (!this.activeAgents.has(sessionKey)) {
            this.logger.warn(`Agent not found: ${sessionKey}`);
            return {
                success: false,
                error: `Agent not found: ${sessionKey}`
            };
        }

        this.logger.info(`Sending message to agent: ${sessionKey}`);

        const result = await this.tools.sendToSession(
            sessionKey,
            message,
            { timeoutSeconds: timeoutSeconds || this.config.agentTimeout }
        );

        return result;
    }

    /**
     * 获取 Agent 会话历史
     * @param {string} sessionKey - Agent 会话密钥
     * @param {number} limit - 消息数量限制
     * @returns {Promise<object>} 会话历史
     */
    async getAgentHistory(sessionKey, limit = 50) {
        return await this.tools.getSessionHistory(sessionKey, limit, true);
    }

    /**
     * 列出所有活跃 Agent
     * @returns {Promise<Array>} Agent 列表
     */
    async listAgents() {
        const agents = [];

        for (const [sessionKey, info] of this.activeAgents) {
            agents.push({
                sessionKey,
                ...info
            });
        }

        return agents;
    }

    /**
     * 获取 Agent 信息
     * @param {string} sessionKey - Agent 会话密钥
     * @returns {object|null} Agent 信息
     */
    getAgentInfo(sessionKey) {
        return this.activeAgents.get(sessionKey) || null;
    }

    /**
     * 终止 Agent
     * 使用 subagents kill 终止指定 Agent
     * 
     * @param {string} sessionKey - Agent 会话密钥
     * @returns {Promise<object>} 操作结果
     */
    async terminateAgent(sessionKey) {
        if (!this.activeAgents.has(sessionKey)) {
            this.logger.warn(`Agent not found: ${sessionKey}`);
            return {
                success: false,
                error: `Agent not found: ${sessionKey}`
            };
        }

        this.logger.info(`Terminating agent: ${sessionKey}`);

        // 从本地记录中移除
        const agentInfo = this.activeAgents.get(sessionKey);
        this.activeAgents.delete(sessionKey);

        // 从任务映射中移除
        for (const [taskId, key] of this.taskToAgent) {
            if (key === sessionKey) {
                this.taskToAgent.delete(taskId);
                break;
            }
        }

        // 调用 subagents kill
        const result = await this.tools.killSubAgent(sessionKey);

        this.logger.info(`Agent terminated: ${sessionKey}`);

        return result;
    }

    /**
     * 引导 Agent
     * 使用 subagents steer 引导 Agent 行为
     * 
     * @param {string} sessionKey - Agent 会话密钥
     * @param {string} message - 引导消息
     * @returns {Promise<object>} 操作结果
     */
    async steerAgent(sessionKey, message) {
        if (!this.activeAgents.has(sessionKey)) {
            this.logger.warn(`Agent not found: ${sessionKey}`);
            return {
                success: false,
                error: `Agent not found: ${sessionKey}`
            };
        }

        this.logger.info(`Steering agent: ${sessionKey}`);

        const result = await this.tools.steerSubAgent(sessionKey, message);
        return result;
    }

    /**
     * 分配任务给 Agent
     * 创建或分配任务给指定类型的 Agent
     * 
     * @param {object} task - 任务对象
     * @param {string} task.id - 任务 ID
     * @param {string} task.title - 任务标题
     * @param {string} task.description - 任务描述
     * @param {string} agentType - Agent 类型
     * @param {string} existingAgentKey - 使用现有 Agent（可选）
     * @returns {Promise<object>} 分配结果
     */
    async assignTask(task, agentType = 'coder', existingAgentKey = null) {
        this.logger.info(`Assigning task ${task.id} to ${agentType} agent`);

        let agentKey;

        if (existingAgentKey) {
            // 使用现有 Agent
            agentKey = existingAgentKey;
        } else {
            // 创建新 Agent
            const createResult = await this.createAgent({
                task: task.description || task.title,
                agentType,
                label: `task-${task.id}-${agentType}`,
                persistent: true
            });

            if (!createResult.success) {
                return createResult;
            }

            agentKey = createResult.sessionKey;
        }

        // 记录任务映射
        this.taskToAgent.set(task.id, agentKey);

        // 更新 Agent 状态
        if (this.activeAgents.has(agentKey)) {
            const info = this.activeAgents.get(agentKey);
            info.currentTask = task.id;
            info.status = 'busy';
        }

        this.logger.info(`Task ${task.id} assigned to agent ${agentKey}`);

        return {
            success: true,
            taskId: task.id,
            agentKey,
            agentType
        };
    }

    /**
     * 更新任务状态
     * 同步任务状态到数据库
     * 
     * @param {string} taskId - 任务 ID
     * @param {string} status - 任务状态
     * @param {object} db - 数据库实例
     * @returns {Promise<object>} 更新结果
     */
    async updateTaskStatus(taskId, status, db) {
        this.logger.info(`Updating task ${taskId} status to ${status}`);

        try {
            const result = await db.updateTaskStatus(taskId, status);
            
            // 如果任务完成，释放 Agent
            if (status === 'completed') {
                const agentKey = this.taskToAgent.get(taskId);
                if (agentKey) {
                    this.taskToAgent.delete(taskId);
                    
                    if (this.activeAgents.has(agentKey)) {
                        const info = this.activeAgents.get(agentKey);
                        info.currentTask = null;
                        info.status = 'idle';
                    }
                }
            }

            return { success: true, ...result };
        } catch (error) {
            this.logger.error(`Failed to update task status: ${error.message}`);
            return { success: false, error: error.message };
        }
    }

    /**
     * 获取活跃 Agent 数量
     * @returns {number} 活跃 Agent 数量
     */
    getActiveAgentCount() {
        return this.activeAgents.size;
    }

    /**
     * 获取空闲 Agent
     * @param {string} agentType - Agent 类型（可选）
     * @returns {Array} 空闲 Agent 列表
     */
    getIdleAgents(agentType = null) {
        const idleAgents = [];

        for (const [sessionKey, info] of this.activeAgents) {
            if (info.status === 'idle' || info.status === 'running') {
                if (!agentType || info.type === agentType) {
                    idleAgents.push({ sessionKey, ...info });
                }
            }
        }

        return idleAgents;
    }

    /**
     * 清理离线 Agent
     * 清理超过超时时间的 Agent
     */
    async cleanupOfflineAgents() {
        const now = new Date();
        const timeoutMs = this.config.agentTimeout * 1000;
        const offlineAgents = [];

        for (const [sessionKey, info] of this.activeAgents) {
            const createdAt = new Date(info.createdAt);
            if (now - createdAt > timeoutMs) {
                offlineAgents.push(sessionKey);
            }
        }

        for (const sessionKey of offlineAgents) {
            this.logger.info(`Cleaning up offline agent: ${sessionKey}`);
            await this.terminateAgent(sessionKey);
        }

        return offlineAgents;
    }
}

module.exports = { OpenClawAgentOrchestrator };
