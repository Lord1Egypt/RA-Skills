/**
 * Collaboration Visualizer 测试脚本
 */

const {
  createCollaboration,
  runCollaboration,
  printCollaborationStatus,
  getAllCollaborations
} = require('./sensen-collaborator');

const {
  printVisualReport,
  printRecentCollabsOverview,
  generateFullReport
} = require('./sensen-collab-visualizer');

console.log('🧪 Collaboration Visualizer 测试\n');

// 创建测试协作
console.log('1️⃣ 创建测试协作...');
const collab = createCollaboration({
  name: '测试内容发布流程',
  type: 'sequential',
  description: '测试多Agent协作流程',
  tasks: [
    { agent: 'Strategy', description: '确定选题方向', dependsOn: [] },
    { agent: 'Marketing', description: '创作内容', dependsOn: [0] },
    { agent: 'CEO', description: '审核内容', dependsOn: [1] },
    { agent: 'Marketing', description: '发布到平台', dependsOn: [2] }
  ]
});

console.log('\n2️⃣ 模拟执行（不真实spawn）...');
// 直接修改状态模拟执行
collab.tasks[0].status = 'done';
collab.tasks[0].startedAt = new Date(Date.now() - 3000).toISOString();
collab.tasks[0].completedAt = new Date(Date.now() - 2000).toISOString();
collab.tasks[0].result = { output: '选题方向已确定：AI时代HR转型' };

collab.tasks[1].status = 'done';
collab.tasks[1].startedAt = new Date(Date.now() - 2000).toISOString();
collab.tasks[1].completedAt = new Date(Date.now() - 1000).toISOString();
collab.tasks[1].result = { output: '内容创作完成：2000字干货文章' };

collab.tasks[2].status = 'working';
collab.tasks[2].startedAt = new Date(Date.now() - 500).toISOString();

collab.tasks[3].status = 'idle';

// 保存模拟状态
const fs = require('fs');
const path = require('path');
const collabPath = path.join(__dirname, 'collaborations', `${collab.id}.json`);
fs.writeFileSync(collabPath, JSON.stringify(collab, null, 2), 'utf-8');

// 测试可视化
console.log('\n3️⃣ 完整可视化报告...');
printVisualReport(collab.id);

console.log('\n4️⃣ 最近协作概览...');
printRecentCollabsOverview(3);

console.log('\n5️⃣ 原始状态打印（对比）...');
printCollaborationStatus(collab);

// 清理
console.log('\n6️⃣ 清理测试数据...');
fs.unlinkSync(collabPath);
console.log('   测试数据已清理');

console.log('\n✅ Collaboration Visualizer 测试完成！');
console.log('\nP1-2 增强功能总结:');
console.log('  ✅ Timeline 视图 - ASCII 水平时间线');
console.log('  ✅ 状态面板 - 进度条+统计');
console.log('  ✅ 任务详情 - 带依赖关系显示');
console.log('  ✅ 紧凑视图 - 实时进度一行流');
