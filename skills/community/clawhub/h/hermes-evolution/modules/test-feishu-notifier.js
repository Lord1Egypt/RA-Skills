/**
 * SENSEN Feishu Notifier - 测试脚本
 */

const FeishuNotifier = require('./sensen-feishu-notifier');
const TaskManager = require('./task-manager');

// 测试1: 单独发送卡片
async function testSendCard() {
  console.log('\n' + '='.repeat(60));
  console.log('测试1: 发送飞书卡片');
  console.log('='.repeat(60));

  const mockTask = {
    id: 'task_test_001',
    title: '测试任务：验证飞书通知',
    description: '这是一个测试任务，用于验证飞书通知功能是否正常',
    status: 'review',
    priority: 'P1',
    assignedTo: 'CEO',
    createdAt: new Date().toISOString(),
    result: null
  };

  console.log('\n发送 Review 状态卡片（含按钮）:');
  const card = FeishuNotifier.buildTaskCard(mockTask, 'status_change');
  await FeishuNotifier.sendFeishuCard(card);

  console.log('\n发送超时提醒卡片:');
  mockTask.status = 'executing';
  const timeoutCard = FeishuNotifier.buildTaskCard(mockTask, 'timeout');
  await FeishuNotifier.sendFeishuCard(timeoutCard);
}

// 测试2: 集成到TaskManager
async function testIntegratedNotifier() {
  console.log('\n' + '='.repeat(60));
  console.log('测试2: 集成飞书通知到TaskManager');
  console.log('='.repeat(60));

  // 包装TaskManager
  const TM = FeishuNotifier.wrapTaskManagerWithFeishu(TaskManager);

  // 创建任务（会自动发送飞书通知）
  console.log('\n创建新任务（应触发飞书通知）:');
  const task = TM.createTask({
    title: '飞书通知集成测试',
    description: '测试任务创建时是否发送飞书通知',
    source: 'test',
    priority: 'P2',
    assignedTo: 'CEO'
  });

  // 等待一下
  await new Promise(r => setTimeout(r, 500));

  // 更新状态（应触发飞书通知）
  console.log('\n更新任务状态（应触发飞书通知）:');
  TM.updateTaskState(task.id, 'planning');
  await new Promise(r => setTimeout(r, 500));

  TM.updateTaskState(task.id, 'executing');
  await new Promise(r => setTimeout(r, 500));

  TM.updateTaskState(task.id, 'review');
  await new Promise(r => setTimeout(r, 500));

  TM.updateTaskState(task.id, 'done', { result: '测试完成，通知已发送' });

  // 清理测试任务
  TM.deleteTask(task.id);
}

// 测试3: 发送日报汇总
async function testDailySummary() {
  console.log('\n' + '='.repeat(60));
  console.log('测试3: 发送每日任务汇总');
  console.log('='.repeat(60));

  // 先创建几个任务
  const TM = FeishuNotifier.wrapTaskManagerWithFeishu(TaskManager);
  
  TM.createTask({ title: '日报任务1', priority: 'P0', assignedTo: 'Marketing' });
  TM.createTask({ title: '日报任务2', priority: 'P1', assignedTo: 'RD' });
  
  // 发送日报
  await TM.sendDailySummary();

  // 清理
  const tasks = TM.getAllTasks();
  tasks.forEach(t => {
    if (t.source === 'test') TM.deleteTask(t.id);
  });
}

async function runTests() {
  console.log('🚀 SENSEN Feishu Notifier Phase 4.1 - 测试开始');
  console.log('注意: 如果未配置飞书API，将使用模拟模式');

  await testSendCard();
  await testIntegratedNotifier();
  await testDailySummary();

  console.log('\n✅ 测试完成!');
}

runTests().catch(console.error);
