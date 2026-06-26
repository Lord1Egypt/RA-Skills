/**
 * Session Validator
 * 会话配置校验模块
 */

const { getAllAgents, getAgentByName, validateAgentAddress } = require('./agent-manager');
const { loadFromDatabase, syncToCode } = require('./config-sync');

/**
 * 会话开始时校验配置
 */
function validateSessionConfig() {
  try {
    console.log('🔍 会话开始：校验 Agent 配置...\n');
    
    // 1. 从数据库加载最新配置
    const agents = getAllAgents();
    
    if (agents.length === 0) {
      console.warn('⚠️ 警告：数据库中没有 Agent 配置！');
      return { valid: false, error: 'No agents configured' };
    }
    
    // 2. 校验每个 Agent 的地址格式
    const validationResults = [];
    let allValid = true;
    
    for (const agent of agents) {
      const isValid = validateAgentAddress(agent.target);
      validationResults.push({
        name: agent.name,
        target: agent.target,
        isValid,
        isActive: agent.is_active === 1
      });
      
      if (!isValid) {
        console.warn(`⚠️ 警告：Agent ${agent.name} 地址格式无效：${agent.target}`);
        allValid = false;
      }
      
      if (agent.is_active === 0) {
        console.log(`ℹ️ 提示：Agent ${agent.name} 已停用`);
      }
    }
    
    // 3. 同步配置到代码文件
    if (allValid) {
      syncToCode();
      console.log('✅ 配置已同步到代码文件');
    }
    
    console.log(`\n✅ 会话配置校验完成：${agents.length} 个 Agent`);
    
    return {
      valid: allValid,
      agents: validationResults,
      count: agents.length
    };
  } catch (error) {
    console.error('❌ 会话配置校验失败:', error.message);
    return { valid: false, error: error.message };
  }
}

/**
 * 获取当前会话可用的 Agent
 */
function getAvailableAgents() {
  try {
    const agents = getAllAgents();
    const available = agents
      .filter(agent => agent.is_active === 1)
      .map(agent => ({
        name: agent.name,
        role: agent.role,
        target: agent.target,
        description: agent.description
      }));
    
    return available;
  } catch (error) {
    console.error('❌ 获取可用 Agent 失败:', error.message);
    return [];
  }
}

/**
 * 记录会话活动
 */
function logSessionActivity(agentName, activity, details = {}) {
  try {
    const message = JSON.stringify({
      activity,
      details,
      timestamp: new Date().toISOString()
    });
    
    require('./agent-manager').logMessage('session', agentName, message, 'activity');
    return true;
  } catch (error) {
    console.error('❌ 记录会话活动失败:', error.message);
    return false;
  }
}

/**
 * 检查配置是否需要更新
 */
function checkConfigUpdateNeeded() {
  try {
    const dbAgents = getAllAgents();
    const codeAgents = require('../agent-addresses').AGENT_ADDRESSES;
    
    const dbNames = new Set(dbAgents.map(a => a.name));
    const codeNames = new Set(Object.keys(codeAgents));
    
    const needsUpdate = !dbNames.size === codeNames.size || 
                       [...dbNames].some(name => !codeNames.has(name)) ||
                       [...codeNames].some(name => !dbNames.has(name));
    
    if (needsUpdate) {
      console.log('🔄 检测到配置差异，需要同步...');
      syncToCode();
      return true;
    }
    
    return false;
  } catch (error) {
    console.error('❌ 检查配置更新失败:', error.message);
    return false;
  }
}

module.exports = {
  validateSessionConfig: validateSessionConfig,
  getAvailableAgents: getAvailableAgents,
  logSessionActivity: logSessionActivity,
  checkConfigUpdateNeeded: checkConfigUpdateNeeded
};