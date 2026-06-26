/**
 * FrozenMemory 测试
 */

const {
  readMemory,
  readAllMemoryForSession,
  stageEdit,
  freezeMemory,
  applyPendingChanges,
  getFrozenStatus,
  clearStaging
} = require('./frozen-memory');

const fs = require('fs');
const path = require('path');

console.log('🧪 FrozenMemory 测试\n');

// 初始化
const today = new Date().toISOString().split('T')[0];

// 1. 查看当前状态
console.log('1️⃣ 查看记忆状态');
const status = getFrozenStatus();
console.log(`   Frozen: ${status.frozen.join(', ') || '(无)'}`);
console.log(`   Staging: ${status.staging.join(', ') || '(无)'}`);
console.log(`   Memory: ${status.memory.join(', ') || '(无)'}`);

// 2. 测试 stagedit
console.log('\n2️⃣ 测试 stageEdit（编辑存入 staging）');
stageEdit(today, `# 今天的学习\n\n- 完成P0-P2优化\n- TaskStore性能提升\n- IntentRouter智能路由`, '今日工作记录');

const staged = readMemory(today);
console.log(`   读取结果: source=${staged.source}, pending=${staged.pending || false}`);
console.log(`   内容前50字: ${staged.content.substring(0, 50)}...`);

// 3. 测试冻结
console.log('\n3️⃣ 测试 freezeMemory（staging → frozen）');
freezeMemory(today);

const frozen = readMemory(today);
console.log(`   冻结后读取: source=${frozen.source}`);
console.log(`   内容前50字: ${frozen.content.substring(0, 50)}...`);

// 4. 测试会话初始化
console.log('\n4️⃣ 测试 readAllMemoryForSession（启动时调用）');
const allMemories = readAllMemoryForSession();
console.log(`   读取到 ${allMemories.length} 个记忆`);
for (const m of allMemories) {
  console.log(`   - ${m.date}: ${m.source} ${m.pending ? '(待生效)' : ''}`);
}

// 5. 清理测试数据
console.log('\n5️⃣ 清理测试数据');
clearStaging(today);
console.log('   已清理 staging');

console.log('\n✅ FrozenMemory 测试完成！');
console.log('\nP0-2 Frozen记忆 核心概念:');
console.log('  📝 stageEdit() - 编辑存入 staging，当前会话不受影响');
console.log('  ❄️ freezeMemory() - 手动触发合并');
console.log('  🚀 applyPendingChanges() - 启动时自动合并');
console.log('  ✅ readMemory() - 优先读取 frozen');
console.log('\n效果: 记忆编辑仅下次会话生效，避免上下文抖动');
