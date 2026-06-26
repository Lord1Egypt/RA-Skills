/**
 * SENSEN Task Manager - 测试脚本
 * Phase 2 验证
 */

const TaskManager = require('./task-manager');

// 测试辅助函数
function log(label, data) {
  console.log(`\n${'='.repeat(60)}`);
  console.log(`测试: ${label}`);
  console.log('='.repeat(60));
  if (typeof data === 'object') {
    console.log(JSON.stringify(data, null, 2));
  } else {
    console.log(data);
  }
}

// 测试用例
async function runTests() {
  console.log('🚀 SENSEN Task Manager Phase 2 - 测试开始');
  
  // 1. 创建测试任务
  log('1. 创建任务', '创建3个不同优先级的任务');
  
  const task1 = TaskManager.createTask({
    title: '小红书热门话题汇总',
    description: '每天9点推送5个热门话题',
    source: 'scheduled',
    priority: 'P0',
    intent: 'content_creation',
    assignedTo: 'Marketing'
  });
  
  const task2 = TaskManager.createTask({
    title: '备份系统配置',
    description: '备份Gateway和Agent配置',
    source: 'scheduled',
    priority: 'P1',
    intent: 'operations',
    assignedTo: 'RD'
  });
  
  const task3 = TaskManager.createTask({
    title: '财富自由路径研究',
    description: '探索3年财富自由可行方案',
    source: 'boss_dm',
    priority: 'P2',
    intent: 'strategy'
  });
  
  // 2. 状态流转测试
  log('2. 状态流转测试', '测试 Inbox → Planning → Executing → Review → Done');
  
  console.log('\n当前状态:', TaskManager.loadTask(task1.id).status);
  
  TaskManager.updateTaskState(task1.id, TaskManager.TaskState.PLANNING, {
    assignedTo: 'Marketing'
  });
  
  console.log('转换到 Planning ✓');
  TaskManager.updateTaskState(task1.id, TaskManager.TaskState.EXECUTING);
  console.log('转换到 Executing ✓');
  TaskManager.updateTaskState(task1.id, TaskManager.TaskState.REVIEW);
  console.log('转换到 Review ✓');
  TaskManager.updateTaskState(task1.id, TaskManager.TaskState.DONE, {
    result: '已完成并发布到飞书群'
  });
  console.log('转换到 Done ✓');
  
  // 3. 验证无效转换被阻止
  log('3. 无效转换测试', '尝试 Done → Executing (应该失败)');
  const result = TaskManager.updateTaskState(task1.id, TaskManager.TaskState.EXECUTING);
  console.log('结果:', result === null ? '正确拒绝 ❌' : '错误通过 ✓');
  
  // 4. 获取统计
  log('4. 任务统计', TaskManager.getStats());
  
  // 5. 打印看板
  log('5. 任务看板', '');
  TaskManager.printKanban();
  
  // 6. 按状态筛选
  log('6. Done状态任务', TaskManager.getTasksByStatus('done').map(t => ({
    id: t.id,
    title: t.title,
    result: t.result
  })));
  
  // 7. 清理测试数据
  log('7. 清理测试数据', '');
  TaskManager.deleteTask(task1.id);
  TaskManager.deleteTask(task2.id);
  TaskManager.deleteTask(task3.id);
  console.log('测试任务已清理 ✓');
  
  console.log('\n✅ 所有测试完成!');
}

// 执行测试
runTests().catch(console.error);
