/**
 * OpenClaw Tools - OpenClaw 原生工具封装
 * 封装 sessions_spawn、subagents、sessions_send、message 等原生能力
 */

/**
 * OpenClaw 工具集
 */
class OpenClawTools {
    constructor(options = {}) {
        this.config = {
            defaultModel: options.defaultModel || 'ollama/qwen3.5-code',
            defaultTimeout: options.defaultTimeout || 300,
            ...options
        };
        
        this.logger = {
            info: (msg) => console.log(`[OpenClawTools] ${msg}`),
            warn: (msg) => console.warn(`[OpenClawTools] ${msg}`),
            error: (msg) => console.error(`[OpenClawTools] ${msg}`),
            debug: (msg) => console.log(`[OpenClawTools DEBUG] ${msg}`)
        };
    }

    /**
     * 创建子 Agent 会话
     * 使用 sessions_spawn 创建独立的子 Agent
     * 
     * @param {object} options - 配置选项
     * @param {string} options.task - 任务描述
     * @param {string} options.label - 会话标签
     * @param {string} options.runtime - 运行时类型 (subagent|acp)
     * @param {string} options.mode - 运行模式 (run|session)
     * @param {string} options.model - 使用的模型
     * @param {number} options.timeoutSeconds - 超时时间
     * @param {boolean} options.thread - 是否在独立线程运行
     * @returns {Promise<object>} 会话创建结果
     */
    async spawnSubAgent(options) {
        const {
            task,
            label = `agent-${Date.now()}`,
            runtime = 'subagent',
            mode = 'run',
            model = this.config.defaultModel,
            timeoutSeconds = this.config.defaultTimeout,
            thread = false
        } = options;

        this.logger.info(`Spawning sub-agent: ${label}`);
        
        // 调用 sessions_spawn 工具
        const spawnOptions = {
            task,
            label,
            runtime,
            mode,
            model,
            timeoutSeconds,
            thread
        };

        try {
            // 这里需要调用 OpenClaw 的 sessions_spawn 工具
            // 在实际运行中，这会被 OpenClaw 框架处理
            const result = await this._callTool('sessions_spawn', spawnOptions);
            return { success: true, sessionKey: result.sessionKey, ...result };
        } catch (error) {
            this.logger.error(`Failed to spawn sub-agent: ${error.message}`);
            return { success: false, error: error.message };
        }
    }

    /**
     * 管理子 Agent
     * 使用 subagents 工具列、杀、引导子 Agent
     * 
     * @param {string} action - 操作类型 (list|kill|steer)
     * @param {string} target - 目标 Agent ID (kill/steer 时需要)
     * @param {string} message - 引导消息 (steer 时需要)
     * @param {number} recentMinutes - 最近分钟数 (list 时可选)
     * @returns {Promise<object>} 操作结果
     */
    async manageSubAgents(action, target = null, message = null, recentMinutes = null) {
        const options = { action };
        
        if (target) options.target = target;
        if (message) options.message = message;
        if (recentMinutes !== null) options.recentMinutes = recentMinutes;

        this.logger.info(`Managing sub-agents: action=${action}, target=${target || 'all'}`);

        try {
            const result = await this._callTool('subagents', options);
            return { success: true, ...result };
        } catch (error) {
            this.logger.error(`Failed to manage sub-agents: ${error.message}`);
            return { success: false, error: error.message };
        }
    }

    /**
     * 列出所有子 Agent
     * @param {number} recentMinutes - 最近分钟数
     * @returns {Promise<Array>} 子 Agent 列表
     */
    async listSubAgents(recentMinutes = null) {
        return await this.manageSubAgents('list', null, null, recentMinutes);
    }

    /**
     * 终止子 Agent
     * @param {string} agentId - Agent ID
     * @returns {Promise<object>} 操作结果
     */
    async killSubAgent(agentId) {
        return await this.manageSubAgents('kill', agentId);
    }

    /**
     * 引导子 Agent
     * @param {string} agentId - Agent ID
     * @param {string} message - 引导消息
     * @returns {Promise<object>} 操作结果
     */
    async steerSubAgent(agentId, message) {
        return await this.manageSubAgents('steer', agentId, message);
    }

    /**
     * 向会话发送消息
     * 使用 sessions_send 工具向指定会话发送消息
     * 
     * @param {string} sessionKey - 会话密钥
     * @param {string} message - 消息内容
     * @param {string} label - 会话标签（可选）
     * @param {string} agentId - Agent ID（可选）
     * @param {number} timeoutSeconds - 超时时间
     * @returns {Promise<object>} 发送结果
     */
    async sendToSession(sessionKey, message, options = {}) {
        const {
            label = null,
            agentId = null,
            timeoutSeconds = this.config.defaultTimeout
        } = options;

        const sendOptions = {
            message,
            timeoutSeconds
        };

        if (sessionKey) sendOptions.sessionKey = sessionKey;
        if (label) sendOptions.label = label;
        if (agentId) sendOptions.agentId = agentId;

        this.logger.info(`Sending message to session: ${sessionKey || label}`);

        try {
            const result = await this._callTool('sessions_send', sendOptions);
            return { success: true, ...result };
        } catch (error) {
            this.logger.error(`Failed to send message: ${error.message}`);
            return { success: false, error: error.message };
        }
    }

    /**
     * 获取会话历史
     * 使用 sessions_history 工具获取会话历史
     * 
     * @param {string} sessionKey - 会话密钥
     * @param {number} limit - 消息数量限制
     * @param {boolean} includeTools - 是否包含工具调用
     * @returns {Promise<object>} 会话历史
     */
    async getSessionHistory(sessionKey, limit = 50, includeTools = false) {
        this.logger.info(`Fetching session history: ${sessionKey}, limit=${limit}`);

        try {
            const result = await this._callTool('sessions_history', {
                sessionKey,
                limit,
                includeTools
            });
            return { success: true, ...result };
        } catch (error) {
            this.logger.error(`Failed to fetch session history: ${error.message}`);
            return { success: false, error: error.message };
        }
    }

    /**
     * 列出可见会话
     * 使用 sessions_list 工具列出会话
     * 
     * @param {object} options - 筛选选项
     * @param {Array} options.kinds - 会话类型筛选
     * @param {number} options.limit - 数量限制
     * @param {number} options.activeMinutes - 活跃分钟数
     * @param {number} options.messageLimit - 消息限制
     * @returns {Promise<object>} 会话列表
     */
    async listSessions(options = {}) {
        const {
            kinds = null,
            limit = null,
            activeMinutes = null,
            messageLimit = null
        } = options;

        const listOptions = {};
        if (kinds) listOptions.kinds = kinds;
        if (limit !== null) listOptions.limit = limit;
        if (activeMinutes !== null) listOptions.activeMinutes = activeMinutes;
        if (messageLimit !== null) listOptions.messageLimit = messageLimit;

        this.logger.info(`Listing sessions with options: ${JSON.stringify(listOptions)}`);

        try {
            const result = await this._callTool('sessions_list', listOptions);
            return { success: true, ...result };
        } catch (error) {
            this.logger.error(`Failed to list sessions: ${error.message}`);
            return { success: false, error: error.message };
        }
    }

    /**
     * 获取会话状态
     * 使用 session_status 工具获取会话状态
     * 
     * @param {string} sessionKey - 会话密钥
     * @param {string} model - 模型设置（可选）
     * @returns {Promise<object>} 会话状态
     */
    async getSessionStatus(sessionKey = null, model = null) {
        const options = {};
        if (sessionKey) options.sessionKey = sessionKey;
        if (model) options.model = model;

        this.logger.info(`Fetching session status: ${sessionKey || 'current'}`);

        try {
            const result = await this._callTool('session_status', options);
            return { success: true, ...result };
        } catch (error) {
            this.logger.error(`Failed to fetch session status: ${error.message}`);
            return { success: false, error: error.message };
        }
    }

    /**
     * 发送消息
     * 使用 message 工具发送消息到指定渠道
     * 
     * @param {object} options - 发送选项
     * @param {string} options.action - 操作类型 (send|read|edit 等)
     * @param {string} options.channel - 渠道名称
     * @param {string} options.target - 目标用户/群组
     * @param {string} options.message - 消息内容
     * @param {string} options.media - 媒体 URL
     * @param {string} options.buffer - Base64 媒体数据
     * @returns {Promise<object>} 发送结果
     */
    async sendMessage(options) {
        const {
            action = 'send',
            channel = null,
            target = null,
            message: msg = null,
            media = null,
            buffer = null,
            ...extraOptions
        } = options;

        const sendOptions = { action };
        if (channel) sendOptions.channel = channel;
        if (target) sendOptions.target = target;
        if (msg !== null) sendOptions.message = msg;
        if (media) sendOptions.media = media;
        if (buffer) sendOptions.buffer = buffer;
        Object.assign(sendOptions, extraOptions);

        this.logger.info(`Sending message via ${channel || 'default'} channel`);

        try {
            const result = await this._callTool('message', sendOptions);
            return { success: true, ...result };
        } catch (error) {
            this.logger.error(`Failed to send message: ${error.message}`);
            return { success: false, error: error.message };
        }
    }

    /**
     * 发送通知消息
     * 封装常用的通知发送功能
     * 
     * @param {string} channel - 渠道名称
     * @param {string} target - 目标用户/群组
     * @param {string} content - 通知内容
     * @param {object} options - 额外选项
     * @returns {Promise<object>} 发送结果
     */
    async sendNotification(channel, target, content, options = {}) {
        return await this.sendMessage({
            action: 'send',
            channel,
            target,
            message: content,
            ...options
        });
    }

    /**
     * 内部工具调用方法
     * 在实际 OpenClaw 环境中，这会调用对应的工具
     * 
     * @param {string} toolName - 工具名称
     * @param {object} params - 工具参数
     * @returns {Promise<object>} 工具执行结果
     * @private
     */
    async _callTool(toolName, params) {
        // 在 OpenClaw 环境中，这里会实际调用工具
        // 目前作为占位符，返回模拟结果
        this.logger.debug(`Calling tool: ${toolName} with params: ${JSON.stringify(params)}`);
        
        // 模拟延迟
        await new Promise(resolve => setTimeout(resolve, 10));
        
        // 返回模拟结果（实际使用时会被 OpenClaw 替换）
        return {
            tool: toolName,
            params,
            timestamp: new Date().toISOString()
        };
    }
}

module.exports = { OpenClawTools };
