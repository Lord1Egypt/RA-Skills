#!/usr/bin/env node
/**
 * PRD 协作进度查看脚本
 *
 * 用法：node status.js
 */

const fs = require('fs');
const path = require('path');

const statusFile = 'status.json';

if (!fs.existsSync(statusFile)) {
  console.error('❌ 找不到状态文件 status.json');
  console.log('   请确保在项目根目录运行此命令');
  process.exit(1);
}

const status = JSON.parse(fs.readFileSync(statusFile, 'utf-8'));

console.log('╔════════════════════════════════════════════════╗');
console.log(`║  📋 ${status.productName.padEnd(42)}║`);
console.log('╠════════════════════════════════════════════════╣');

// 总体进度
const completedSteps = status.steps.filter(s => s.status === 'completed').length;
const progressPercent = Math.round((completedSteps / status.totalSteps) * 100);

console.log(`║  总体进度: ${completedSteps}/${status.steps.length} 步骤 (${progressPercent}%)${' '.repeat(15)}║`);
console.log('║  ' + getProgressBar(progressPercent) + '  ║');
console.log('╠════════════════════════════════════════════════╣');

// 各步骤状态
status.steps.forEach(step => {
  const icon = getStatusIcon(step.status);
  const line = `${icon} Step ${step.step}: ${step.name}`;
  console.log(`║  ${line.padEnd(44)}║`);
});

console.log('╚════════════════════════════════════════════════╝');
console.log('');
console.log('使用提示:');
console.log('  • 在Claude中描述产品想法开始协作');
console.log('  • 每完成一步，Claude会更新 status.json');
console.log('  • 使用 "node status.js" 随时查看进度');

function getStatusIcon(status) {
  switch (status) {
    case 'completed': return '✅';
    case 'in_progress': return '▶️';
    case 'pending': return '⏳';
    default: return '⭕';
  }
}

function getProgressBar(percent) {
  const filled = Math.round(percent / 10);
  const empty = 10 - filled;
  return '█'.repeat(filled) + '░'.repeat(empty) + ` ${percent}%`;
}
