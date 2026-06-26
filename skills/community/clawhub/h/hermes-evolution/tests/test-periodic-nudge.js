/**
 * PeriodicNudge 测试
 */

const {
  Nudge,
  NudgeType,
  NudgePriority,
  PeriodicNudgeEngine,
  createEngine
} = require('./periodic-nudge');

console.log('🧪 PeriodicNudge 测试\n');

// 1. 创建 Nudge
console.log('1️⃣ 创建 Nudge');
const nudge1 = new Nudge(
  NudgeType.TASK_TIMEOUT,
  '任务 "小红书发布" 超时 2小时',
  {
    priority: NudgePriority.HIGH,
    source: 'test',
    action: '重新分配给其他Agent'
  }
);
console.log(`   创建: ${nudge1.id}`);
console.log(`   类型: ${nudge1.type}`);
console.log(`   优先级: ${nudge1.priority}`);

// 2. Nudge 状态转换
console.log('\n2️⃣ Nudge 状态转换');
nudge1.acknowledge();
console.log(`   确认后: acknowledged=${nudge1.acknowledged}`);
nudge1.resolve('已重新分配给Marketing');
console.log(`   解决后: resolved=${nudge1.resolved}`);
console.log(`   解决方案: ${nudge1.resolution}`);

// 3. 创建引擎
console.log('\n3️⃣ 创建 Periodic Nudge 引擎');
const engine = createEngine({ interval: 1000 });  // 1秒用于测试
console.log(`   引擎状态: ${engine.enabled ? '运行中' : '未启动'}`);

// 4. 手动添加 Nudge
console.log('\n4️⃣ 手动添加 Nudge');
engine.addNudge(new Nudge(
  NudgeType.RULE_VIOLATION,
  '检测到格式违反: 输出太长',
  { priority: NudgePriority.MEDIUM }
));
engine.addNudge(new Nudge(
  NudgeType.PATTERN_ANOMALY,
  'HR类型纠正出现3次',
  { priority: NudgePriority.HIGH, action: '生成规则' }
));
engine.addNudge(new Nudge(
  NudgeType.OPPORTUNITY,
  '系统有10个超时任务，可优化配置',
  { priority: NudgePriority.LOW }
));

const summary = engine.getSummary();
console.log(`   待处理: ${summary.total} 个`);
console.log(`   按类型:`, summary.byType);
console.log(`   按优先级:`, summary.byPriority);

// 5. 打印状态
console.log('\n5️⃣ 打印引擎状态');
engine.printStatus();

// 6. 启动引擎并运行一次检查
console.log('\n6️⃣ 启动引擎并执行一次检查');
engine.start();

// 等待检查完成
setTimeout(() => {
  const summary2 = engine.getSummary();
  console.log(`\n   检查后待处理: ${summary2.total} 个`);
  
  if (summary2.total > 0) {
    console.log('\n   最新 Nudges:');
    const pending = engine.getPendingNudges();
    for (const n of pending.slice(0, 3)) {
      console.log(`   - [${n.priority}] ${n.message.substring(0, 40)}...`);
    }
  }
  
  // 停止引擎
  engine.stop();
  
  // 7. 测试获取特定优先级的 Nudges
  console.log('\n7️⃣ 按优先级筛选');
  const highNudges = engine.getPendingNudges(NudgePriority.HIGH);
  console.log(`   高优先级: ${highNudges.length} 个`);
  
  console.log('\n✅ PeriodicNudge 测试完成！');
  console.log('\nP1-3 Periodic Nudge 核心概念:');
  console.log('  🔍 runChecks() - 周期性自检（规则违反/超时/模式异常）');
  console.log('  📊 getSummary() - 状态摘要');
  console.log('  📝 getPendingNudges() - 获取待处理项');
  console.log('  ⚙️ start()/stop() - 引擎启停');
  console.log('\n从被动纠正 → 主动自检，提前发现问题！');
}, 2000);
