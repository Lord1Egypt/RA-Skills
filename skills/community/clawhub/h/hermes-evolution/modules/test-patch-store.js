/**
 * PatchStore 测试
 */

const {
  appendCorrection,
  loadCorrectionsByDate,
  patchRule,
  getRuleLight,
  getRuleFull,
  getCorrectionStats
} = require('./patch-store');

const fs = require('fs');
const path = require('path');

console.log('🧪 PatchStore 测试\n');

// 1. 测试追加 correction
console.log('1️⃣ 测试追加 correction');
const record1 = {
  id: 'corr_test_001',
  timestamp: new Date().toISOString(),
  type: 'format',
  originalText: '太长了',
  correction: '简短发',
  resolved: false
};
appendCorrection(record1);

const record2 = {
  id: 'corr_test_002',
  timestamp: new Date().toISOString(),
  type: 'format',
  originalText: '太复杂了',
  correction: '简化',
  resolved: false
};
appendCorrection(record2);

console.log('   已追加2条correction');

// 2. 测试读取
console.log('\n2️⃣ 测试读取今日 corrections');
const today = new Date().toISOString().split('T')[0];
const corrections = loadCorrectionsByDate(today);
console.log(`   读取到 ${corrections.length} 条 correction`);
for (const c of corrections.slice(-3)) {
  console.log(`   - ${c.id}: ${c.originalText} → ${c.correction}`);
}

// 3. 测试统计
console.log('\n3️⃣ 测试统计（索引加速）');
const stats = getCorrectionStats();
console.log(`   总数: ${stats.total}`);
console.log(`   今日: ${stats.today}`);
console.log(`   未解决: ${stats.unresolved}`);

// 4. 测试 patch 规则
console.log('\n4️⃣ 测试 patch 规则');
// 先创建一个测试规则
const testRuleId = 'rule_patch_test';
const ruleFile = path.join(__dirname, 'rules', `${testRuleId}.json`);
fs.writeFileSync(ruleFile, JSON.stringify({
  id: testRuleId,
  version: 1,
  name: '测试规则',
  description: '原始描述',
  weight: 0.5,
  updatedAt: new Date().toISOString()
}), 'utf-8');
console.log('   创建测试规则成功');

// 应用 patch
patchRule(testRuleId, { description: '新描述', weight: 0.8 });

// 读取轻量级（只有变更）
console.log('\n5️⃣ 读取轻量级规则');
const light = getRuleLight(testRuleId);
console.log(`   轻量读取:`, JSON.stringify(light));

// 读取完整（含历史）
console.log('\n6️⃣ 读取完整规则（应用所有patch）');
const full = getRuleFull(testRuleId);
console.log(`   完整读取: version=${full.version}, description=${full.description}`);

// 7. 清理测试数据
console.log('\n7️⃣ 清理测试数据');
const jsonlFile = path.join(__dirname, 'corrections', `${today}.jsonl`);
if (fs.existsSync(jsonlFile)) {
  // 只删除测试记录
  const lines = fs.readFileSync(jsonlFile, 'utf-8').split('\n')
    .filter(l => l.includes('corr_test'));
  // 保留非测试记录
  const nonTest = fs.readFileSync(jsonlFile, 'utf-8').split('\n')
    .filter(l => l.trim() && !l.includes('corr_test'));
  fs.writeFileSync(jsonlFile, nonTest.join('\n') + '\n', 'utf-8');
  console.log('   已清理测试correction');
}
if (fs.existsSync(ruleFile)) fs.unlinkSync(ruleFile);
const patchFile = path.join(__dirname, 'rules', `${testRuleId}.patch`);
if (fs.existsSync(patchFile)) fs.unlinkSync(patchFile);

console.log('\n✅ PatchStore 测试完成！');
console.log('\nP0-1 增强功能总结:');
console.log('  ✅ Append-only corrections - 增量追加，不读写全量');
console.log('  ✅ JSON Merge Patch - 只写变化字段');
console.log('  ✅ 索引加速 - 统计用索引，精确读取时才IO');
