/**
 * Config Sync
 * 数据库与代码配置同步模块
 */

const fs = require('fs');
const path = require('path');
const { getAllAgents, updateAgentAddress } = require('./agent-manager');

/**
 * 从数据库加载 Agent 配置
 */
async function loadFromDatabase() {
  try {
    const agents = await getAllAgents();
    const config = {};
    
    agents.forEach(agent => {
      config[agent.name] = {
        role: agent.role,
        target: agent.target,
        description: agent.description,
        capabilities: JSON.parse(agent.capabilities || '[]'),
        isActive: agent.is_active === 1
      };
    });
    
    console.log('✅ 已从数据库加载 Agent 配置:', Object.keys(config).length, '个 Agent');
    return config;
  } catch (error) {
    console.error('❌ 从数据库加载配置失败:', error.message);
    throw error;
  }
}

/**
 * 将配置保存到数据库
 */
async function saveToDatabase(config) {
  try {
    const updates = Object.entries(config).map(([name, agentConfig]) => ({
      name,
      role: agentConfig.role,
      target: agentConfig.target,
      description: agentConfig.description,
      capabilities: JSON.stringify(agentConfig.capabilities)
    }));
    
    const results = [];
    for (const update of updates) {
      try {
        const result = await updateAgentAddress(update.name, update.target);
        results.push({ name: update.name, success: true });
      } catch (error) {
        results.push({ name: update.name, success: false, error: error.message });
      }
    }
    
    const successCount = results.filter(r => r.success).length;
    console.log(`✅ 已保存 ${successCount}/${updates.length} 个 Agent 配置到数据库`);
    return results;
  } catch (error) {
    console.error('❌ 保存配置到数据库失败:', error.message);
    throw error;
  }
}

/**
 * 同步数据库配置到代码
 */
async function syncToCode() {
  try {
    const config = await loadFromDatabase();
    
    // 更新 agent-addresses.js 文件
    const addressesPath = path.join(__dirname, '..', 'agent-addresses.js');
    const content = generateAddressesFile(config);
    
    fs.writeFileSync(addressesPath, content, 'utf8');
    console.log('✅ 已同步配置到 agent-addresses.js');
    
    return config;
  } catch (error) {
    console.error('❌ 同步配置到代码失败:', error.message);
    throw error;
  }
}

/**
 * 生成 agent-addresses.js 文件内容
 */
function generateAddressesFile(config) {
  const agentEntries = Object.entries(config)
    .map(([name, agent]) => {
      return `  '${name}': {
    role: '${agent.role}',
    target: process.env.${name.toUpperCase().replace(/-/g, '_')}_QQ_ID || '${agent.target}',
    description: '${agent.description}',
    capabilities: ${JSON.stringify(agent.capabilities)}
  }`;
    })
    .join(',\n');
  
  return `/**
 * Agent Addresses Configuration
 * 独立 QQ 机器人地址配置（方案 C）
 * ⚠️ 此文件由数据库自动生成，请勿手动修改
 * 生成时间：${new Date().toISOString()}
 */

const AGENT_ADDRESSES = {
${agentEntries}
};

/**
 * 获取 Agent 地址
 * @param {string} agentName - Agent 名称
 * @returns {string} Agent 地址
 */
function getAgentAddress(agentName) {
  const agent = AGENT_ADDRESSES[agentName];
  if (!agent) {
    throw new Error(\`Unknown agent: \${agentName}\`);
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
`;
}

/**
 * 校验并更新配置
 */
async function validateAndUpdate() {
  try {
    console.log('🔍 开始校验并更新配置...\n');
    
    // 从数据库加载最新配置
    const dbConfig = await loadFromDatabase();
    
    // 同步到代码文件
    await syncToCode();
    
    console.log('\n✅ 配置校验和更新完成！');
    console.log('当前配置的 Agent:', Object.keys(dbConfig));
    
    return dbConfig;
  } catch (error) {
    console.error('❌ 配置校验和更新失败:', error.message);
    throw error;
  }
}

module.exports = {
  loadFromDatabase,
  saveToDatabase,
  syncToCode,
  validateAndUpdate
};