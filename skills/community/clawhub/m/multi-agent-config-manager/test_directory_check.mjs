/**
 * 工作区目录检查测试
 * 测试目录检查功能是否明确提示用户需要搭建的目录
 */

import { checkWorkspaceStructure, checkAgentConfig } from './lib/config_validator.js';

console.log('📁 工作区目录检查测试');
console.log('═'.repeat(60) + '\n');

console.log('## 测试 1: 工作区目录结构检查');
console.log('─'.repeat(60) + '\n');

const workspaceResult = checkWorkspaceStructure();

console.log(`检查结果: ${workspaceResult.status === 'pass' ? '✅ 通过' : '❌ 有错误'}`);
console.log(`检查项数: ${workspaceResult.checks.length}\n`);

// 显示每个目录的详细信息
for (const check of workspaceResult.checks) {
  const icon = check.status === 'pass' ? '✅' : check.status === 'warning' ? '⚠️' : '❌';
  console.log(`${icon} ${check.name}`);
  console.log(`   路径: ${check.path}`);
  console.log(`   状态: ${check.status}`);
  console.log(`   描述: ${check.description || 'N/A'}`);
  
  if (check.impact) {
    console.log(`   影响: ${check.impact}`);
  }
  
  // 解析消息中的说明
  console.log(`   消息:`);
  const messageLines = check.message.split('\n');
  for (const line of messageLines) {
    console.log(`       ${line}`);
  }
  console.log();
}

console.log('\n## 测试 2: 代理配置检查');
console.log('─'.repeat(60) + '\n');

const agentResult = checkAgentConfig();

console.log(`检查结果: ${agentResult.status === 'pass' ? '✅ 通过' : '❌ 有错误'}`);

if (agentResult.status === 'pass') {
  console.log(`代理数量: ${agentResult.agentCount}`);
  
  if (agentResult.agentResults && agentResult.agentResults.length > 0) {
    console.log('\n代理工作区检查:');
    for (const agentCheck of agentResult.agentResults) {
      const icon = agentCheck.status === 'pass' ? '✅' : '❌';
      console.log(`\n${icon} ${agentCheck.name}`);
      console.log(`   状态: ${agentCheck.status}`);
      
      const messageLines = agentCheck.message.split('\n');
      for (const line of messageLines) {
        console.log(`       ${line}`);
      }
    }
  }
} else {
  console.log('\n配置错误详情:');
  const messageLines = agentResult.message.split('\n');
  for (const line of messageLines) {
    console.log(`   ${line}`);
  }
}

console.log('\n═'.repeat(60));
console.log('📋 目录检查总结:');
console.log('\n✅ 必需的工作区目录:');

const requiredDirs = [
  { name: '工作区根目录', path: 'C:\\Users\\mrcft\\.openclaw\\workspace', purpose: 'OpenClaw 工作区根目录' },
  { name: '代理工作区', path: 'C:\\Users\\mrcft\\.openclaw\\workspace\\agents', purpose: '每个代理的独立工作空间' },
  { name: '共享输出目录', path: 'C:\\Users\\mrcft\\.openclaw\\workspace\\shared', purpose: '研究结果共享目录' },
  { name: '研究任务目录', path: 'C:\\Users\\mrcft\\.openclaw\\workspace\\shared\\researches', purpose: '按任务组织的研究目录' },
  { name: '最终报告目录', path: 'C:\\Users\\mrcft\\.openclaw\\workspace\\shared\\final', purpose: '最终报告存放目录' }
];

for (const dir of requiredDirs) {
  console.log(`   📁 ${dir.name}`);
  console.log(`       路径: ${dir.path}`);
  console.log(`       作用: ${dir.purpose}`);
}

console.log('\n🎯 工作区目录作用说明:');
console.log('   1. **agents/ 代理工作区**: 每个子代理都有独立的工作空间，存放该代理的历史研究文件');
console.log('   2. **shared/researches/**: 按研究任务组织的目录，每次研究都会创建新的子目录');
console.log('   3. **shared/final/**: 最终报告输出目录，用户查看和下载研究成果的地方');
console.log('   4. **.cache/**: 系统缓存目录，可选但建议创建');
console.log('   5. **logs/**: 系统日志目录，用于调试和问题排查，可选');

console.log('\n🔧 自动配置功能:');
console.log('   如果检测到目录缺失，系统会：');
console.log('   1. 显示详细的目录说明和作用');
console.log('   2. 等待用户确认是否自动创建');
console.log('   3. 用户同意后自动创建所有必需目录');
console.log('   4. 确保多代理系统可以正常运行');

console.log('\n✅ 测试完成！');
