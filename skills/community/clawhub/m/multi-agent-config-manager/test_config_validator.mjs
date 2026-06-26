/**
 * 配置检查器测试脚本
 * 测试 config_validator 模块的功能
 */

import { generateConfigReport, generateConfigGuide, autoConfigure } from './lib/config_validator.js';

console.log('🧪 多代理引擎 - 配置检查器测试\n');
console.log('═'.repeat(60) + '\n');

// 测试 1: 生成配置检查报告
console.log('测试 1: 生成配置检查报告');
console.log('─'.repeat(60));
const report = generateConfigReport();

console.log('\n📊 配置概览:');
console.log(`  总检查项: ${report.summary.total}`);
console.log(`  ✅ 通过: ${report.summary.pass}`);
console.log(`  ⚠️  警告: ${report.summary.warning}`);
console.log(`  ❌ 错误: ${report.summary.error}`);

console.log('\n详细检查结果:');
for (const check of report.checks) {
  const icon = check.status === 'pass' ? '✅' : check.status === 'warning' ? '⚠️' : '❌';
  console.log(`  ${icon} ${check.name}: ${check.status}`);
  if (check.message) {
    console.log(`     ${check.message}`);
  }
}

// 测试 2: 生成配置指南
console.log('\n\n测试 2: 生成配置指南');
console.log('─'.repeat(60));
const guide = generateConfigGuide();
console.log(guide);

// 测试 3: 自动配置（仅演示，不实际执行）
console.log('\n\n测试 3: 自动配置演示');
console.log('─'.repeat(60));
console.log('⚠️  注意：自动配置功能需要用户明确同意才能执行');
console.log('   本测试仅演示配置检查流程，不会实际修改系统文件。\n');

if (report.errors.length > 0) {
  console.log('检测到配置错误，需要修复：');
  for (const error of report.errors) {
    console.log(`  - ${error.name}: ${error.message}`);
  }
} else {
  console.log('✅ 所有必需配置项已满足');
}

console.log('\n══════════════════════════════════════════════════════════════');
console.log('✅ 配置检查器测试完成\n');
