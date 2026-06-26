/**
 * Agent Addresses Configuration
 * 独立 QQ 机器人地址配置（方案 C）
 * ⚠️ 此文件由数据库自动生成，请勿手动修改
 * 生成时间：2026-03-24T09:03:55.082Z
 */

const AGENT_ADDRESSES = {
  'checker-agent': {
    role: 'checker',
    target: process.env.CHECKER_AGENT_QQ_ID || 'qqbot:c2c:CHECKER_AGENT_PLACEHOLDER',
    description: '审查测试',
    capabilities: ["code-review","testing","quality-assurance"]
  },
  'coder-agent': {
    role: 'coder',
    target: process.env.CODER_AGENT_QQ_ID || 'qqbot:c2c:CODER_AGENT_PLACEHOLDER',
    description: '代码开发',
    capabilities: ["code-writing","debugging","testing"]
  },
  'main-agent': {
    role: 'main',
    target: process.env.MAIN_AGENT_QQ_ID || 'qqbot:c2c:MAIN_AGENT_PLACEHOLDER',
    description: '任务管理与调度',
    capabilities: ["task-management","scheduling","reporting"]
  },
  'memowriter-agent': {
    role: 'memowriter',
    target: process.env.MEMOWRITER_AGENT_QQ_ID || 'qqbot:c2c:MEMOWRITER_AGENT_PLACEHOLDER',
    description: '文档记录',
    capabilities: ["documentation","reporting","knowledge-management"]
  }
};

/**
 * 获取 Agent 地址
 * @param {string} agentName - Agent 名称
 * @returns {string} Agent 地址
 */
function getAgentAddress(agentName) {
  const agent = AGENT_ADDRESSES[agentName];
  if (!agent) {
    throw new Error(`Unknown agent: ${agentName}`);
  }
  return agent.target;
}

/**
 * 获取 Agent 信息
 * @param {string} agentName - Agent 名称
 * @returns {object} Agent 信息
 */
function getAgentInfo(agentName) {
  return AGENT_ADDRESSES[agentName];
}

/**
 * 获取所有 Agent 地址
 * @returns {object} 所有 Agent 地址
 */
function getAllAgentAddresses() {
  return AGENT_ADDRESSES;
}

module.exports = {
  AGENT_ADDRESSES,
  getAgentAddress,
  getAgentInfo,
  getAllAgentAddresses
};
