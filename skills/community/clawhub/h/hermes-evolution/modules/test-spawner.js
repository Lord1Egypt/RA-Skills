/**
 * SENSEN Spawner - 测试脚本
 */

const Spawner = require('./sensen-spawner');

async function runTests() {
  console.log('🚀 SENSEN Sub-Agent Spawner Phase 4.2 - 测试开始\n');

  // 1. 入队测试
  console.log('='.repeat(60));
  console.log('测试1: 任务入队');
  console.log('='.repeat(60));

  const task1 = Spawner.enqueueTask('Marketing', '发布小红书内容', 'subtask_0', 'collab_test_1', 'P0');
  const task2 = Spawner.enqueueTask('CEO', '审核内容质量', 'subtask_1', 'collab_test_1', 'P1');
  const task3 = Spawner.enqueueTask('Strategy', '分析今日热点', 'subtask_2', 'collab_test_2', 'P2');

  // 2. 查看队列
  console.log('\n' + '='.repeat(60));
  console.log('测试2: 查看任务队列');
  console.log('='.repeat(60));
  Spawner.printQueue();

  // 3. 生成Spawn命令
  console.log('\n' + '='.repeat(60));
  console.log('测试3: 生成Sessions Spawn命令');
  console.log('='.repeat(60));

  const pending = Spawner.getPendingTasks();
  for (const task of pending) {
    const cmd = Spawner.generateSpawnCommand(task);
    console.log(`\n@${task.agent} 任务:`);
    console.log(JSON.stringify(cmd, null, 2));
  }

  // 4. 模拟执行
  console.log('\n' + '='.repeat(60));
  console.log('测试4: 模拟执行任务');
  console.log('='.repeat(60));

  for (const task of Spawner.getPendingTasks()) {
    await Spawner.simulateTask(task);
  }

  // 5. 再次查看队列（应该为空）
  console.log('\n' + '='.repeat(60));
  console.log('测试5: 执行后队列状态');
  console.log('='.repeat(60));
  Spawner.printQueue();

  // 6. 生成Cron配置
  console.log('\n' + '='.repeat(60));
  console.log('测试6: Cron配置模板');
  console.log('='.repeat(60));
  console.log(Spawner.generateCronConfig());

  console.log('\n✅ Phase 4.2 测试完成!');
}

runTests().catch(console.error);
