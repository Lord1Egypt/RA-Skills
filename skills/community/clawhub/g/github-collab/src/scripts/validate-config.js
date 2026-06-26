/**
 * Validate Configuration Script
 * 配置验证脚本
 */

const { validateSessionConfig } = require('../db/session-validator');

async function main() {
  console.log('🔍 开始验证配置...\n');
  
  try {
    const result = await validateSessionConfig();
    
    if (result.valid) {
      console.log('\n✅ 配置验证通过！');
      console.log(`   Agent 数量：${result.count}`);
      console.log('\n当前配置的 Agent:');
      result.agents.forEach(agent => {
        const status = agent.isActive ? '✅ 活跃' : '⏸️ 停用';
        console.log(`   - ${agent.name}: ${agent.target} ${status}`);
      });
    } else {
      console.log('\n❌ 配置验证失败！');
      console.log(`   错误：${result.error}`);
      process.exit(1);
    }
  } catch (error) {
    console.error('❌ 验证失败:', error.message);
    process.exit(1);
  }
}

main();