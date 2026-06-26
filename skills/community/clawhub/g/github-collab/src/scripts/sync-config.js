/**
 * Sync Configuration Script
 * 配置同步脚本
 */

const { validateAndUpdate } = require('../db/config-sync');
const { loadFromDatabase } = require('../db/config-sync');

async function main() {
  console.log('🔄 开始同步配置...\n');
  
  try {
    const config = await loadFromDatabase();
    
    console.log('\n✅ 配置同步完成！');
    console.log(`   已同步 ${Object.keys(config).length} 个 Agent`);
    console.log('\n同步的 Agent:');
    Object.entries(config).forEach(([name, agent]) => {
      console.log(`   - ${name}: ${agent.target}`);
    });
  } catch (error) {
    console.error('❌ 同步失败:', error.message);
    process.exit(1);
  }
}

main();