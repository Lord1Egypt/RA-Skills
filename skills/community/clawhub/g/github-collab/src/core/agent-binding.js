/**
 * Agent Binding - Agent 任务绑定管理
 */

class AgentBinding {
  constructor(options = {}) {
    // 支持自定义数据库路径
    this.taskManager = options.taskManager || new TaskManager(options);
  }

  /**
   * 分配任务给 Agent
   */
  assignTask(taskId, agentName) {
    return this.taskManager.assignTaskToAgent(taskId, agentName);
  }

  /**
   * 获取 Agent 状态
   */
  getAgentStatus(agentName) {
    return this.taskManager.getAgentStatus(agentName);
  }

  /**
   * 完成 Agent 任务
   */
  completeTask(taskId, agentName, result) {
    return this.taskManager.completeTask(taskId, result);
  }

  /**
   * 获取 Agent 任务队列
   */
  getAgentQueue(agentName) {
    return this.taskManager.getAgentQueue(agentName);
  }

  /**
   * 更新 Agent 任务状态
   */
  updateAgentTaskStatus(taskId, status, agentName) {
    return this.taskManager.updateTaskStatus(taskId, status);
  }
}

module.exports = AgentBinding;