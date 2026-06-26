/**
 * HonchoProfiler 测试
 */

const { HonchoProfiler } = require('./honcho-profiler');

console.log('🧪 HonchoProfiler 测试\n');

const profiler = new HonchoProfiler();

// 1. 创建用户画像
console.log('1️⃣ 创建用户画像');
const profile = profiler.getProfile('user_001');
profile.updateIdentity({
  name: '苍苍子森',
  title: 'HR一号位',
  company: '全球五百强'
});
profile.addGoal('三年内实现财富自由');
profile.addGoal('建立AI助理团队');
profile.learnPreference('communicationStyle', 'direct');
profile.learnPreference('responseFormat', 'concise');
console.log(`   创建: ${profile.identity.name}`);
console.log(`   职位: ${profile.identity.title}`);

// 2. 记录交互
console.log('\n2️⃣ 记录交互');
profiler.recordInteraction('user_001', {
  responseTime: 5000,
  hour: 9,
  intent: '小红书发布',
  agentPreference: { taskType: 'content', agent: 'Marketing' }
});
profiler.recordInteraction('user_001', {
  responseTime: 3000,
  hour: 14,
  intent: 'HR咨询',
  agentPreference: { taskType: 'hr', agent: 'CEO' }
});
profiler.recordInteraction('user_001', {
  responseTime: 4000,
  hour: 17,
  intent: '小红书发布'
});
console.log('   已记录 3 次交互');

// 3. 学习行为
console.log('\n3️⃣ 学习行为');
profile.learnBehavior('response_time', 3500);
profile.learnBehavior('active_hour', 9);
profile.learnBehavior('active_hour', 14);
profile.learnBehavior('active_hour', 17);
profile.learnBehavior('intent', '小红书发布');
profile.learnBehavior('intent', 'HR咨询');
profile.learnBehavior('intent', '小红书发布');
profile.learnBehavior('intent', '财富自由');
profile.learnBehavior('agent_preference', { taskType: 'content', agent: 'Marketing' });
console.log('   平均响应时间: 3500ms');
console.log('   活跃时段: 9, 14, 17');
console.log('   常见意图:', profile.behaviorPattern.commonIntents);

// 4. 预测需求
console.log('\n4️⃣ 预测需求（当前时间: ' + new Date().getHours() + '点）');
const predictions = profile.predictNeeds();
console.log(`   预测数: ${predictions.length}`);
for (const p of predictions) {
  console.log(`   - ${p.need}: ${p.message} (置信度: ${p.confidence})`);
}

// 5. 获取推荐
console.log('\n5️⃣ 获取推荐');
const recs = profile.getRecommendations();
console.log(`   推荐数: ${recs.length}`);
for (const r of recs) {
  if (r.type === 'intent') {
    console.log(`   意图建议: ${r.suggestions.join(', ')}`);
  } else if (r.type === 'time') {
    console.log(`   时间建议: ${r.message}`);
  } else if (r.type === 'goal') {
    console.log(`   目标: ${r.goals.map(g => g.text).join(', ')}`);
  }
}

// 6. 设置当前用户
console.log('\n6️⃣ 设置当前用户');
profiler.setCurrentUser('user_001');

// 7. 打印画像
console.log('\n7️⃣ 打印用户画像');
profiler.printCurrentProfile();

// 8. 保存和重新加载
console.log('\n8️⃣ 保存和重新加载');
profiler.saveAll();

// 重新创建 profiler 并加载
const profiler2 = new HonchoProfiler();
const profile2 = profiler2.getProfile('user_001');
console.log(`   重新加载成功`);
console.log(`   姓名: ${profile2.identity.name}`);
console.log(`   互动次数: ${profile2.metadata.interactionCount}`);
console.log(`   常见意图: ${profile2.behaviorPattern.commonIntents}`);

console.log('\n✅ HonchoProfiler 测试完成！');
console.log('\nP2-3 Honcho用户建模 核心概念:');
console.log('  👤 UserProfile - 用户画像（身份+目标+偏好）');
console.log('  🧠 learnBehavior() - 学习行为模式');
console.log('  🔮 predictNeeds() - 预测用户需求');
console.log('  📊 getRecommendations() - 基于学习的推荐');
console.log('\n效果: 越用越懂用户，预测需求，主动服务');
