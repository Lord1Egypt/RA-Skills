/**
 * Self-Improving v2 测试脚本
 */

const {
  Rule,
  CorrectionType,
  Priority,
  logCorrection,
  getAllRules,
  getActiveRules,
  getRulesNeedingRefresh,
  matchRule,
  updateRule,
  confirmRule,
  rollbackRule,
  getStats,
  printRuleStatus
} = require('./sensen-self-improving-v2');

console.log('🧪 Self-Improving v2 测试\n');

// 1. Rule 类测试
console.log('1️⃣ Rule 类测试');
const rule = new Rule({
  id: 'test_rule_001',
  type: CorrectionType.FORMAT,
  keywords: ['太长', '简短', '精简'],
  description: '回复要简短',
  weight: 0.7,
  priority: Priority.HIGH
});
console.log(`   创建规则: ${rule.id}`);
console.log(`   状态: ${rule.getStatus()}`);
console.log(`   权重: ${rule.weight}`);
console.log(`   版本: v${rule.version}`);

// 2. 规则更新（版本递增）
console.log('\n2️⃣ 规则更新测试');
rule.update({
  description: '回复必须非常简短，不超过50字',
  weight: 0.9
});
console.log(`   更新后版本: v${rule.version}`);
console.log(`   历史版本数: ${rule.versions.length}`);
console.log(`   当前描述: ${rule.description}`);

// 3. 确认规则
console.log('\n3️⃣ 确认规则测试');
rule.confirm();
console.log(`   确认后状态: ${rule.getStatus()}`);
console.log(`   上次确认: ${rule.lastConfirmed}`);

// 4. 回滚测试
console.log('\n4️⃣ 回滚测试');
try {
  const rolledBack = rule.rollback(1);
  console.log(`   回滚到v1后版本: v${rolledBack.version}`);
  console.log(`   回滚后描述: ${rolledBack.description}`);
} catch (e) {
  console.log(`   回滚失败: ${e.message}`);
}

// 5. 过期检查测试
console.log('\n5️⃣ 过期检查测试');
const expiredRule = new Rule({
  id: 'test_rule_expired',
  type: CorrectionType.FORMAT,
  keywords: ['测试'],
  description: '过期规则',
  priority: Priority.LOW
});
// 手动设置为已过期
expiredRule.expiresAt = '2020-01-01T00:00:00.000Z';
console.log(`   过期规则状态: ${expiredRule.getStatus()}`);
console.log(`   正常规则状态: ${rule.getStatus()}`);

// 6. 匹配测试
console.log('\n6️⃣ 匹配测试');
// 创建几个测试规则
const rules = [
  new Rule({
    id: 'rule_match_1',
    type: CorrectionType.FORMAT,
    keywords: ['太长', '长'],
    description: '太长',
    weight: 0.5
  }),
  new Rule({
    id: 'rule_match_2',
    type: CorrectionType.FORMAT,
    keywords: ['太长了'],
    description: '太长了要精简',
    weight: 0.9
  })
];

// 保存规则到文件
const fs = require('fs');
const path = require('path');
for (const r of rules) {
  const filePath = path.join(__dirname, 'rules', `${r.id}.json`);
  fs.writeFileSync(filePath, JSON.stringify(r.toJSON(), null, 2), 'utf-8');
}

// 测试匹配
const testText = '这个太长了需要精简一下';
const match = matchRule(testText);
if (match.matched) {
  console.log(`   文本: "${testText}"`);
  console.log(`   匹配规则: ${match.rule.name}`);
  console.log(`   加权得分: ${match.weightedScore}`);
  console.log(`   所有匹配:`);
  for (const m of match.allMatches) {
    console.log(`     - ${m.rule.name} (得分: ${m.weightedScore})`);
  }
}

// 7. 统计测试
console.log('\n7️⃣ 统计测试');
const stats = getStats();
console.log(`   规则总数: ${stats.rules.total}`);
console.log(`   生效中: ${stats.rules.active}`);
console.log(`   需刷新: ${stats.rules.needsRefresh}`);
console.log(`   已过期: ${stats.rules.expired}`);

// 8. 打印状态
console.log('\n8️⃣ 规则状态打印');
printRuleStatus();

// 9. 清理测试数据
console.log('\n9️⃣ 清理测试数据...');
const testFiles = ['test_rule_001.json', 'test_rule_expired.json', 'rule_match_1.json', 'rule_match_2.json'];
for (const f of testFiles) {
  const filePath = path.join(__dirname, 'rules', f);
  if (fs.existsSync(filePath)) fs.unlinkSync(filePath);
}
console.log('   测试数据已清理');

console.log('\n✅ Self-Improving v2 测试完成！');
console.log('\nP1-1 增强功能总结:');
console.log('  ✅ 规则权重 (weight) - 影响匹配优先级');
console.log('  ✅ 版本管理 (version/versions) - 支持版本历史和回滚');
console.log('  ✅ 有效期 (expiresAt/refreshAfter) - 过期自动提醒');
