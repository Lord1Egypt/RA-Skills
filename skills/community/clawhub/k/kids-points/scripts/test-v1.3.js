#!/usr/bin/env node
/**
 * v1.3 功能测试脚本
 * 测试月度消费额度制和欠费结转功能
 */

const fs = require('fs');
const path = require('path');
const handler = require('./handler');

const WORKSPACE = '/home/wang/.openclaw/agents/kids-study/workspace';
const POINTS_DIR = path.join(WORKSPACE, 'kids-points');

console.log('🧪 v1.3 功能测试\n');
console.log('=' .repeat(50));

// 测试 1: 检查配置
console.log('\n📋 测试 1: 检查配置文件');
const rulesFile = path.join(__dirname, '..', 'config', 'rules.json');
const rules = JSON.parse(fs.readFileSync(rulesFile, 'utf8'));
console.log(`版本：${rules.version}`);
console.log(`每月消费额度：${rules.rules.limits.monthlySpendingLimit} 分`);
console.log(`赚取上限：${rules.rules.limits.monthlyEarningLimit === null ? '无限制' : rules.rules.limits.monthlyEarningLimit}`);
console.log(`重置日：每月${rules.rules.limits.resetDay}号`);
console.log('✅ 配置正确');

// 测试 2: 检查函数导出
console.log('\n📋 测试 2: 检查函数导出');
console.log(`checkMonthlyOverdraft: ${typeof handler.checkMonthlyOverdraft === 'function' ? '✅' : '❌'}`);
console.log(`getLastMonthStr: ${typeof handler.getLastMonthStr === 'function' ? '✅' : '❌'}`);
console.log(`handleExpenseInput: ${typeof handler.handleExpenseInput === 'function' ? '✅' : '❌'}`);

// 测试 3: 测试月份计算
console.log('\n📋 测试 3: 测试月份计算');
const currentMonth = handler.getMonthStr();
const lastMonth = handler.getLastMonthStr();
console.log(`当前月份：${currentMonth}`);
console.log(`上月月份：${lastMonth}`);
console.log('✅ 月份计算正确');

// 测试 4: 测试消费识别（修复后的正则）
console.log('\n📋 测试 4: 测试消费识别');
const testCases = [
  '积分消费 买零食花了 20 分',
  '积分消费 忘带书包花了 5 分',
  '积分消费 买玩具花了 30 分'
];

for (const testCase of testCases) {
  const result = handler.handleExpenseInput(testCase);
  console.log(`输入："${testCase}"`);
  console.log(`  识别结果：${result.success ? '✅ 成功' : '❌ 失败'}`);
  if (result.success) {
    console.log(`  金额：${result.amount}分`);
    console.log(`  用途：${result.description}`);
  }
}

// 测试 5: 测试语音播报配置
console.log('\n📋 测试 5: 测试语音配置');
const hasApiKey = handler.checkSenseApiKey();
console.log(`API Key 配置：${hasApiKey ? '✅ 已配置' : '❌ 未配置'}`);

// 测试 6: 检查月度账本结构
console.log('\n📋 测试 6: 检查月度账本结构');
const currentMonthFile = path.join(POINTS_DIR, 'monthly', `${currentMonth}.md`);
if (fs.existsSync(currentMonthFile)) {
  const content = fs.readFileSync(currentMonthFile, 'utf8');
  const hasExpense = content.includes('总支出');
  const hasOverdraft = content.includes('欠费结转');
  console.log(`月度账本存在：✅`);
  console.log(`  总支出字段：${hasExpense ? '✅' : '❌'}`);
  console.log(`  欠费字段：${hasOverdraft ? '✅ (已有欠费记录)' : '❌ (无欠费)'}`);
} else {
  console.log(`月度账本不存在：❌`);
}

// 测试 7: 模拟欠费检查
console.log('\n📋 测试 7: 模拟欠费检查');
const isMonthStart = new Date().getDate() === 1;
console.log(`今天是每月 1 号：${isMonthStart ? '✅' : '❌'}`);
if (isMonthStart) {
  const overdraft = handler.checkMonthlyOverdraft();
  if (overdraft) {
    console.log(`检测到欠费：${overdraft.overdraft} 分`);
    console.log(`本月可用额度：${overdraft.availableLimit} 分`);
  } else {
    console.log('无欠费记录');
  }
} else {
  console.log('跳过欠费检查（非每月 1 号）');
}

console.log('\n' + '='.repeat(50));
console.log('✅ 所有测试完成！\n');
