/**
 * Agent 通讯辅助模块
 * 提供简化版的跨 Agent 通讯功能
 * 
 * 注意：此模块需要在 OpenClaw 环境中运行
 * 使用方式：
 * const { sendToAgent, findSession, createSession } = require('./communicator.js');
 */

/**
 * 查找现有会话
 * @param {string} sender - 发起方名称 (如 'main')
 * @param {string} receiver - 接收方名称 (如 'maxwell')
 * @returns {object|null} sessionKey 或 null
 */
async function findSession(sender, receiver) {
  // 注意：此函数需要在 OpenClaw 环境中通过 tool 调用
  // 这里提供逻辑参考
  
  const sessions = await sessions_list({ limit: 50 });
  
  // 查找匹配 label 的会话
  const label1 = `${sender}-to-${receiver}`;
  const label2 = `${receiver}-to-${sender}`;
  
  for (const session of sessions) {
    if (session.key.includes('subagent')) {
      const label = session.label || '';
      if (label === label1 || label === label2) {
        return session.key;
      }
    }
  }
  
  return null;
}

/**
 * 创建新会话
 * @param {string} sender - 发起方名称
 * @param {string} receiver - 接收方名称
 * @returns {object} 创建结果
 */
async function createSession(sender, receiver) {
  const label = `${sender}-to-${receiver}`;
  
  const result = await sessions_spawn({
    label: label,
    runtime: 'subagent',
    task: '',
    mode: 'run'
  });
  
  return result;
}

/**
 * 发送消息到另一个 Agent
 * @param {string} sender - 发起方名称
 * @param {string} receiver - 接收方名称  
 * @param {string} message - 消息内容
 * @returns {object} 发送结果
 */
async function sendToAgent(sender, receiver, message) {
  // 步骤1：查找现有会话
  let sessionKey = await findSession(sender, receiver);
  
  // 步骤2：如无可用则创建
  if (!sessionKey) {
    const result = await createSession(sender, receiver);
    sessionKey = result.childSessionKey;
  }
  
  // 步骤3：发送消息
  const sendResult = await sessions_send({
    sessionKey: sessionKey,
    message: message
  });
  
  return sendResult;
}

/**
 * 保护会话不被自动清理
 * @param {string} sessionKey - 会话 Key
 * @returns {object} 执行结果
 */
async function protectSession(sessionKey) {
  const result = await exec({
    command: `openclaw sessions cleanup --active-key "${sessionKey}" --enforce`
  });
  
  return result;
}

/**
 * 获取所有活跃的 Agent 通讯会话
 * @returns {array} 会话列表
 */
async function listAllAgentSessions() {
  const sessions = await sessions_list({ limit: 50 });
  
  return sessions
    .filter(s => s.key.includes('subagent'))
    .map(s => ({
      key: s.key,
      label: s.label,
      updatedAt: s.updatedAt
    }));
}

module.exports = {
  findSession,
  createSession,
  sendToAgent,
  protectSession,
  listAllAgentSessions
};
