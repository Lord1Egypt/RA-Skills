#!/usr/bin/env node
/**
 * Update Agent Address Script
 * 更新 Agent 地址脚本
 */

const { updateAgentAddress, getAgentByName, getAllAgents, validateAgentAddress } = require('../db/agent-manager');
const { syncToCode } = require('../db/config-sync');

function listAgents() {
  console.log('\n=== 当前 Agent 列表 ===\n');
  
  try {
    const agents = getAllAgents();
    
    if (agents.length === 0) {
      console.log('📭 暂无 Agent');
      return;
    }
    
    agents.forEach((agent, index) => {
      const status = agent.is_active === 1 ? '✅ 活跃' : '⏸️ 停用';
      console.log(`${index + 1}. ${agent.name}`);
      console.log(`   角色：${agent.role}`);
      console.log(`   地址：${agent.target}`);
      console.log(`   描述：${agent.description || '无'}`);
      console.log(`   状态：${status}`);
      console.log('');
    });
  } catch (error) {
    console.error('❌ 获取 Agent 列表失败:', error.message);
  }
}

function updateAgent(name, newAddress) {
  try {
    // 校验地址格式
    const isValid = validateAgentAddress(newAddress);
    if (!isValid) {
      console.error('❌ 地址格式无效！请使用格式：qqbot:c2c:USER_ID 或 qqbot:group:GROUP_ID');
      return;
    }
    
    const result = updateAgentAddress(name, newAddress);
    console.log(`✅ 已更新 Agent ${name} 的地址`);
    console.log(`   修改次数：${result.changes}`);
    
    // 同步到代码文件
    syncToCode();
    console.log('✅ 配置已同步到代码文件');
  } catch (error) {
    console.error('❌ 更新失败:', error.message);
  }
}

function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log('🚀 Agent 配置管理工具\n');
    console.log('用法:');
    console.log('  node scripts/update-agent.js list                    # 列出所有 Agent');
    console.log('  node scripts/update-agent.js update <name> <address> # 更新 Agent 地址');
    console.log('\n示例:');
    console.log('  node scripts/update-agent.js list');
    console.log('  node scripts/update-agent.js update coder-agent qqbot:c2c:NEW_ID');
    console.log('');
    return;
  }
  
  const command = args[0];
  
  if (command === 'list') {
    listAgents();
  } else if (command === 'update' && args.length >= 3) {
    const name = args[1];
    const address = args[2];
    updateAgent(name, address);
  } else {
    console.error('❌ 参数错误！');
    console.log('用法:');
    console.log('  node scripts/update-agent.js list');
    console.log('  node scripts/update-agent.js update <name> <address>');
  }
}

main();
