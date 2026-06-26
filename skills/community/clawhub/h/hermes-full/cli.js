#!/usr/bin/env node

/**
 * HERMES CLI - 命令行入口
 */

const HERMES = require('./index');

const args = process.argv.slice(2);
const command = args[0] || 'help';

const hermes = HERMES.create({ nodeId: 'node_hermes_cli' });

switch (command) {
  case 'predict':
    const task = args[1] || '处理 API 错误';
    console.log(`\n🔮 预测任务: ${task}`);
    console.log(JSON.stringify(hermes.predictTask(task), null, 2));
    break;
    
  case 'compose':
    const genes = args.slice(1) || [];
    console.log(`\n🧩 组合技能: ${genes.join(', ')}`);
    console.log(JSON.stringify(hermes.composeGenes(genes), null, 2));
    break;
    
  case 'trust':
    const agentId = args[1] || 'node_test';
    console.log(`\n⭐ Agent 信任: ${agentId}`);
    console.log(JSON.stringify(hermes.getAgentTrust(agentId), null, 2));
    break;
    
  case 'leaderboard':
    console.log('\n🏆 信任排行榜:');
    console.log(JSON.stringify(hermes.getTrustLeaderboard(10), null, 2));
    break;
    
  case 'test':
    console.log('\n=== HERMES 系统测试 ===\n');
    
    const gene = hermes.createGene({ category: 'innovate', signals_match: ['api'], strategy: ['重试'], validation: [] });
    const capsule = hermes.createCapsule({ gene: gene.asset_id, summary: '测试', confidence: 0.8 });
    const bundle = hermes.createBundle(gene, capsule);
    const prediction = hermes.predictTask('调用 API');
    
    console.log('✅ Gene:', gene.asset_id);
    console.log('✅ Capsule:', capsule.asset_id);
    console.log('✅ Bundle:', bundle.bundle_id);
    console.log('✅ 预测:', prediction.confidence.toFixed(3));
    console.log('\n=== 测试完成 ===\n');
    break;
    
  default:
    console.log(`
🤖 HERMES CLI

用法: hermes <命令> [参数]

命令:
  predict [任务]    预测任务需要的技能
  compose [genes]   组合多个 Gene
  trust [agent]     查询 Agent 信任分数
  leaderboard       查看信任排行榜
  test              运行系统测试
  help              显示帮助

示例:
  hermes predict "调用第三方 API"
  hermes compose gene1 gene2 gene3
  hermes trust node_abc123
`);
}

module.exports = { hermes };