/**
 * SENSEN Scheduler - 测试脚本
 */

const Scheduler = require('./sensen-scheduler');
const TaskManager = require('./task-manager');
const FeishuNotifier = require('./sensen-feishu-notifier');

// 包装TaskManager
const TM = FeishuNotifier.wrapTaskManagerWithFeishu(TaskManager);

async function runTests() {
  console.log('🚀 SENSEN Scheduler Phase 4.3 - 测试开始\n');

  // 1. 初始化默认定时任务
  console.log('='.repeat(60));
  console.log('测试1: 初始化默认定时任务');
  console.log('='.repeat(60));
  Scheduler.initDefaultSchedules();

  // 2. 查看调度状态
  console.log('\n' + '='.repeat(60));
  console.log('测试2: 查看调度状态');
  console.log('='.repeat(60));
  Scheduler.printScheduleStatus();

  // 3. 创建自定义定时任务
  console.log('\n' + '='.repeat(60));
  console.log('测试3: 创建自定义定时任务');
  console.log('='.repeat(60));

  const customSchedule = Scheduler.createSchedule({
    name: '测试定时任务',
    title: '测试任务',
    description: '这是一个测试用的定时任务',
    time: '23:00',
    daysOfWeek: [1, 3, 5],
    priority: 'P2',
    assignedTo: 'CEO'
  });

  // 4. 模拟触发检查
  console.log('\n' + '='.repeat(60));
  console.log('测试4: 模拟触发检查（模拟已到期的任务）');
  console.log('='.repeat(60));

  // 修改一个任务的nextTrigger为过去时间
  const schedules = Scheduler.getAllSchedules();
  if (schedules.length > 0) {
    const testSchedule = schedules[0];
    const pastTime = new Date(Date.now() - 60000); // 1分钟前
    testSchedule.nextTrigger = pastTime.toISOString();
    
    const schedulePath = `C:\\Users\\t\\.openclaw\\workspace\\skills\\sensen-pm-router\\schedules\\${testSchedule.id}.json`;
    require('fs').writeFileSync(schedulePath, JSON.stringify(testSchedule, null, 2), 'utf-8');
    
    console.log(`已将 ${testSchedule.name} 的下次触发时间设为1分钟前`);
    
    // 触发检查
    const triggered = await Scheduler.checkAndTrigger(TM, null, FeishuNotifier);
    console.log('触发结果:', triggered);
  }

  // 5. 检查超时
  console.log('\n' + '='.repeat(60));
  console.log('测试5: 检查超时任务');
  console.log('='.repeat(60));

  const timeouts = await Scheduler.checkTimeouts(TM, FeishuNotifier);
  console.log('超时任务数:', timeouts.length);

  // 6. 最终调度状态
  console.log('\n' + '='.repeat(60));
  console.log('测试6: 最终调度状态');
  console.log('='.repeat(60));
  Scheduler.printScheduleStatus();

  console.log('\n✅ Phase 4.3 测试完成!');
}

runTests().catch(console.error);
