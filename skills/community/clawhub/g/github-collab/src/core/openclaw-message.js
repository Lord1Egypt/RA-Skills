/**
 * OpenClaw Message Tool Integration
 * 集成 OpenClaw message 工具接口调用能力
 * 
 * 功能增强：
 * 1. 指挥其他 Agent 工作
 * 2. 发送任务指令
 * 3. 进度跟踪与报告
 * 4. 多通道消息发送
 * 5. 富媒体支持
 * 
 * 注意：OpenClaw message 工具是内置工具，直接调用 message() 函数即可
 * 不需要通过 CLI 命令调用
 */

/**
 * 发送消息到 OpenClaw 通道
 * @param {object} options - 消息选项
 * @param {string} options.channel - 目标通道（qqbot, telegram 等）
 * @param {string} options.target - 目标用户/群聊 ID
 * @param {string} options.message - 消息内容
 * @param {string} [options.media] - 媒体 URL 或本地路径
 * @param {string} [options.filename] - 文件名
 * @param {string} [options.contentType] - 内容类型
 * @returns {Promise<object>} - 消息发送结果
 */
async function sendMessage(options) {
    const {
        channel,
        target,
        message,
        media,
        filename,
        contentType
    } = options;

    // 构建消息参数
    const messageParams = {
        action: 'send',
        channel,
        target,
        message
    };

    if (media) {
        messageParams.media = media;
        if (filename) messageParams.filename = filename;
        if (contentType) messageParams.contentType = contentType;
    }

    // 调用 OpenClaw message 工具（内置工具函数）
    try {
        const result = await message(messageParams);
        return {
            success: true,
            result
        };
    } catch (error) {
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * 指挥 Agent 执行任务
 * @param {object} options - 任务指令选项
 * @param {string} options.agentId - Agent 标识
 * @param {string} options.task - 任务描述
 * @param {string} options.channel - 目标通道
 * @param {string} options.target - 目标用户/群聊 ID
 * @param {object} [options.params] - 任务参数
 * @returns {Promise<object>} - 发送结果
 */
async function assignTaskToAgent(options) {
    const { agentId, task, channel, target, params = {} } = options;

    const taskPayload = {
        agent: agentId,
        task: task,
        params: params,
        timestamp: new Date().toISOString(),
        priority: params.priority || 'normal'
    };

    const messageText = `🤖 Agent 任务指令
目标 Agent: ${agentId}
任务：${task}
参数：${JSON.stringify(params)}
优先级：${taskPayload.priority}
时间：${new Date().toLocaleString('zh-CN')}`;

    return await sendMessage({
        channel,
        target,
        message: messageText
    });
}

/**
 * 发送进度更新
 * @param {object} options - 进度更新选项
 * @param {string} options.channel - 目标通道
 * @param {string} options.target - 目标用户/群聊 ID
 * @param {number} options.taskId - 任务 ID
 * @param {number} options.progress - 进度百分比
 * @param {string} options.status - 状态
 * @param {string} [options.agentId] - 执行 Agent ID
 * @returns {Promise<object>} - 发送结果
 */
async function sendProgressUpdate(options) {
    const { channel, target, taskId, progress, status, agentId } = options;

    const progressBar = '█'.repeat(Math.floor(progress / 5)) + '░'.repeat(20 - Math.floor(progress / 5));
    
    const messageText = `📊 任务进度更新
任务 ID: ${taskId}
执行 Agent: ${agentId || 'N/A'}
进度：[${progressBar}] ${progress}%
状态：${status}
时间：${new Date().toLocaleString('zh-CN')}`;

    return await sendMessage({
        channel,
        target,
        message: messageText
    });
}

/**
 * 发送任务完成通知
 * @param {object} options - 通知选项
 * @param {string} options.channel - 目标通道
 * @param {string} options.target - 目标用户/群聊 ID
 * @param {number} options.taskId - 任务 ID
 * @param {string} options.taskName - 任务名称
 * @param {string} options.agentName - Agent 名称
 * @param {string} [options.result] - 任务结果
 * @param {string} [options.duration] - 执行时长
 * @returns {Promise<object>} - 发送结果
 */
async function sendTaskCompletion(options) {
    const { channel, target, taskId, taskName, agentName, result, duration } = options;

    const messageText = `✅ 任务完成
任务 ID: ${taskId}
任务名称：${taskName}
执行 Agent: ${agentName}
执行时长：${duration || 'N/A'}
结果：${result || '成功'}
时间：${new Date().toLocaleString('zh-CN')}`;

    return await sendMessage({
        channel,
        target,
        message: messageText
    });
}

/**
 * 发送错误通知
 * @param {object} options - 错误选项
 * @param {string} options.channel - 目标通道
 * @param {string} options.target - 目标用户/群聊 ID
 * @param {number} options.taskId - 任务 ID
 * @param {string} options.taskName - 任务名称
 * @param {string} options.error - 错误信息
 * @param {string} [options.agentId] - 执行 Agent ID
 * @returns {Promise<object>} - 发送结果
 */
async function sendErrorNotification(options) {
    const { channel, target, taskId, taskName, error, agentId } = options;

    const messageText = `❌ 任务失败
任务 ID: ${taskId}
任务名称：${taskName}
执行 Agent: ${agentId || 'N/A'}
错误：${error}
时间：${new Date().toLocaleString('zh-CN')}`;

    return await sendMessage({
        channel,
        target,
        message: messageText
    });
}

/**
 * 发送项目报告
 * @param {object} options - 报告选项
 * @param {string} options.channel - 目标通道
 * @param {string} options.target - 目标用户/群聊 ID
 * @param {string} options.report - 报告内容
 * @param {string} [options.projectName] - 项目名称
 * @returns {Promise<object>} - 发送结果
 */
async function sendProjectReport(options) {
    const { channel, target, report, projectName } = options;

    const filename = `${projectName || 'project'}-report-${Date.now()}.md`;
    
    return await sendMessage({
        channel,
        target,
        message: `📋 ${projectName || '项目'}报告已生成`,
        media: report,
        filename,
        contentType: 'text/markdown'
    });
}

/**
 * 发送图片
 * @param {object} options - 图片选项
 * @param {string} options.channel - 目标通道
 * @param {string} options.target - 目标用户/群聊 ID
 * @param {string} options.imageUrl - 图片 URL 或本地路径
 * @param {string} [options.caption] - 图片说明
 * @returns {Promise<object>} - 发送结果
 */
async function sendImage(options) {
    const { channel, target, imageUrl, caption = '' } = options;

    return await sendMessage({
        channel,
        target,
        message: caption,
        media: imageUrl,
        contentType: 'image'
    });
}

/**
 * 发送语音
 * @param {object} options - 语音选项
 * @param {string} options.channel - 目标通道
 * @param {string} options.target - 目标用户/群聊 ID
 * @param {string} options.audioPath - 音频文件路径
 * @returns {Promise<object>} - 发送结果
 */
async function sendVoice(options) {
    const { channel, target, audioPath } = options;

    return await sendMessage({
        channel,
        target,
        message: '',
        media: audioPath,
        contentType: 'audio'
    });
}

/**
 * 发送文件
 * @param {object} options - 文件选项
 * @param {string} options.channel - 目标通道
 * @param {string} options.target - 目标用户/群聊 ID
 * @param {string} options.filePath - 文件路径或 URL
 * @param {string} [options.filename] - 文件名
 * @returns {Promise<object>} - 发送结果
 */
async function sendFile(options) {
    const { channel, target, filePath, filename } = options;

    return await sendMessage({
        channel,
        target,
        message: `📎 文件：${filename || require('path').basename(filePath)}`,
        media: filePath,
        filename: filename || require('path').basename(filePath),
        contentType: 'file'
    });
}

/**
 * 发送 Agent 状态报告
 * @param {object} options - 状态报告选项
 * @param {string} options.channel - 目标通道
 * @param {string} options.target - 目标用户/群聊 ID
 * @param {string} options.agentId - Agent ID
 * @param {string} options.status - 状态（idle, busy, error）
 * @param {number} [options.tasksCompleted] - 完成任务数
 * @param {number} [options.tasksFailed] - 失败任务数
 * @returns {Promise<object>} - 发送结果
 */
async function sendAgentStatusReport(options) {
    const { channel, target, agentId, status, tasksCompleted = 0, tasksFailed = 0 } = options;

    const statusEmoji = {
        idle: '🟢',
        busy: '🟡',
        error: '🔴'
    }[status] || '⚪';

    const messageText = `📊 Agent 状态报告
Agent ID: ${agentId}
状态：${statusEmoji} ${status}
完成任务：${tasksCompleted}
失败任务：${tasksFailed}
时间：${new Date().toLocaleString('zh-CN')}`;

    return await sendMessage({
        channel,
        target,
        message: messageText
    });
}

/**
 * 发送多 Agent 协作状态
 * @param {object} options - 协作状态选项
 * @param {string} options.channel - 目标通道
 * @param {string} options.target - 目标用户/群聊 ID
 * @param {Array} options.agents - Agent 状态列表
 * @param {string} options.projectName - 项目名称
 * @returns {Promise<object>} - 发送结果
 */
async function sendMultiAgentStatus(options) {
    const { channel, target, agents, projectName } = options;

    let messageText = `🔄 ${projectName} 多 Agent 协作状态\n\n`;
    
    agents.forEach((agent, index) => {
        const statusEmoji = {
            idle: '🟢',
            busy: '🟡',
            error: '🔴'
        }[agent.status] || '⚪';
        
        messageText += `${index + 1}. ${statusEmoji} ${agent.name} (${agent.status})\n`;
        if (agent.currentTask) {
            messageText += `   当前任务：${agent.currentTask}\n`;
        }
    });

    messageText += `\n时间：${new Date().toLocaleString('zh-CN')}`;

    return await sendMessage({
        channel,
        target,
        message: messageText
    });
}

// 导出所有消息发送函数
module.exports = {
    sendMessage,
    assignTaskToAgent,
    sendProgressUpdate,
    sendTaskCompletion,
    sendErrorNotification,
    sendProjectReport,
    sendImage,
    sendVoice,
    sendFile,
    sendAgentStatusReport,
    sendMultiAgentStatus
};
