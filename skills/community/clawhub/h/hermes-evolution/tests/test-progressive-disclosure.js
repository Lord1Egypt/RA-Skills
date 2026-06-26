/**
 * ProgressiveDisclosure 测试
 */

const {
  TieredSkill,
  ProgressiveDisclosureLoader,
  LEVEL_DESCRIPTIONS
} = require('./progressive-disclosure');

console.log('🧪 ProgressiveDisclosure 测试\n');

// 1. 创建分级 Skill
console.log('1️⃣ 创建分级 Skills');
const skills = [
  {
    name: 'task-router',
    description: '智能任务路由，根据意图分配Agent',
    tier: 1,
    usage: '调用 route(input) 进行路由',
    examples: ['route("发布小红书") → Marketing'],
    tips: ['优先显式指定']
  },
  {
    name: 'task-store',
    description: '任务存储层，内存缓存+索引',
    tier: 2,
    usage: 'TaskStore.create(taskData) 创建任务',
    examples: ['create({title: "测试"})']
  },
  {
    name: 'intent-router',
    description: '意图置信度计算路由',
    tier: 1,
    usage: '使用 TF-IDF 计算置信度',
    examples: ['route("分析市场机会") → Strategy']
  }
];

const loader = new ProgressiveDisclosureLoader({ budget: 5000 });

for (const skill of skills) {
  loader.register(skill);
}

console.log('   已注册 3 个 Skills');

// 2. 查看加载摘要
console.log('\n2️⃣ 查看当前加载摘要');
const summary = loader.getLoadedSummary();
console.log(`   总 Skills: ${summary.totalSkills}`);
console.log(`   已加载: ${summary.loadedCount}`);
console.log(`   总 Tokens: ${summary.totalTokens}`);
console.log(`   可用预算: ${summary.availableBudget}`);

// 3. 测试搜索匹配
console.log('\n3️⃣ 测试搜索匹配');
const matches = loader.findMatching({ keywords: ['路由', '路由'] });
console.log(`   搜索 "路由": ${matches.length} 个匹配`);
for (const m of matches) {
  console.log(`   - ${m.name} (层级:${m.tier}, 当前:${m.currentLevel}, 相关性:${m.score})`);
}

// 4. 测试升级
console.log('\n4️⃣ 测试升级 task-router 到 L2');
const upgrade = loader.tryUpgrade('task-router', 2);
console.log(`   结果: ${upgrade.success ? '✅ 成功' : '❌ 失败'}`);
if (upgrade.success) {
  console.log(`   ${upgrade.fromLevel} → ${upgrade.toLevel}`);
  console.log(`   新增 Tokens: +${upgrade.additionalTokens}`);
} else {
  console.log(`   原因: ${upgrade.reason}`);
}

// 5. 测试预算不足
console.log('\n5️⃣ 测试预算不足场景');
const smallLoader = new ProgressiveDisclosureLoader({ budget: 100 });
smallLoader.register({ name: 'big-skill', description: '这是一个非常大的技能描述，需要很多Token来存储相关信息', tier: 1 });
smallLoader.register({ name: 'another', description: '另一个技能', tier: 1 });
const upgrade2 = smallLoader.tryUpgrade('big-skill', 3);
console.log(`   结果: ${upgrade2.success ? '✅ 成功' : '❌ 失败'}`);
if (!upgrade2.success) {
  console.log(`   原因: ${upgrade2.reason}`);
  console.log(`   需要: ${upgrade2.required} Tokens`);
  console.log(`   可用: ${upgrade2.available} Tokens`);
}

// 6. 测试上下文生成
console.log('\n6️⃣ 测试上下文文本生成');
const contextText = loader.getContextText({ format: 'markdown', maxLevel: 2 });
console.log('   生成内容预览:');
console.log('   ' + contextText.substring(0, 200).split('\n').join('\n   '));

// 7. 测试智能加载
console.log('\n7️⃣ 测试智能加载');
const autoLoadResult = loader.autoLoad({ keywords: ['意图', '置信度'] });
console.log(`   自动升级: ${autoLoadResult.upgraded.length} 个`);
for (const u of autoLoadResult.upgraded) {
  console.log(`   - ${u.name} → L${u.level} (+${u.additionalTokens} Tokens)`);
}

// 8. 测试重置
console.log('\n8️⃣ 测试重置');
loader.reset();
const afterReset = loader.getLoadedSummary();
console.log(`   重置后已加载: ${afterReset.loadedCount}`);
console.log(`   重置后 Tokens: ${afterReset.totalTokens}`);

// 9. 查看分级描述
console.log('\n9️⃣ 分级说明');
for (const [level, info] of Object.entries(LEVEL_DESCRIPTIONS)) {
  console.log(`   L${level} ${info.name}: ${info.desc} (最多 ${info.maxTokens} Tokens)`);
}

console.log('\n✅ ProgressiveDisclosure 测试完成！');
console.log('\nP1-2 渐进式披露 核心概念:');
console.log('  L1 核心 - 始终加载，基础描述 (<200 Tokens)');
console.log('  L2 标准 - 按需加载，详细说明 (<800 Tokens)');
console.log('  L3 完整 - 显式请求，完整文档 (<3000 Tokens)');
console.log('  预算管理 - Token 开销稳定');
console.log('  autoLoad() - 根据上下文智能加载');
