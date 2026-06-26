const ExpenseTrackerSkill = require('./index.js');

console.log('🚀 OpenClaw 智能记账本演示');
console.log('=' .repeat(40));

const tracker = new ExpenseTrackerSkill();

// 演示记账功能
console.log('\n📝 测试记账功能：');

const testCases = [
  '记账：今天午饭花了35元',
  '记录：打车花了25元',
  '添加：超市购物120元',
  '记账：看电影花了80元',
  '记录：去医院花了150元'
];

testCases.forEach((test, index) => {
  console.log(`\n${index + 1}. 输入: ${test}`);
  const result = tracker.handleMessage({ content: test });
  console.log(`   输出: ${result}`);
});

// 演示统计功能
console.log('\n📊 测试统计功能：');
const stats = tracker.getStatistics('month');
console.log(`本月总支出: ¥${stats.total}`);
console.log(`记账笔数: ${stats.count}`);

console.log('\n✅ 演示完成！');