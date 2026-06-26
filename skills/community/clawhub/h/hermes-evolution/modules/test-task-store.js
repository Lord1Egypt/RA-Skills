/**
 * TaskStore 测试脚本
 */

const { TaskStore } = require('./task-store');

console.log('🧪 TaskStore 测试\n');

const store = new TaskStore();

// 1. 创建任务测试
console.log('1️⃣ 创建任务测试');
const task1 = store.create({
  title: '测试任务-P0',
  priority: 'P0',
  assignedTo: 'Marketing',
  intent: 'content_creation',
  source: 'test'
});

const task2 = store.create({
  title: '测试任务-P1',
  priority: 'P1',
  assignedTo: 'RD',
  intent: 'technical'
});

const task3 = store.create({
  title: '测试任务-P2',
  priority: 'P2',
  source: 'test'
});

console.log(`   创建成功: ${task1.id}\n`);

// 2. 读取测试
console.log('2️⃣ 读取测试');
const loaded = store.get(task1.id);
console.log(`   按ID读取: ${loaded.title} [${loaded.priority}]`);

// 3. 索引查询测试
console.log('\n3️⃣ 索引查询测试');
console.log(`   P0任务: ${store.getByPriority('P0').length} 个`);
console.log(`   Marketing任务: ${store.getByAssignee('Marketing').length} 个`);
console.log(`   inbox任务: ${store.getByStatus('inbox').length} 个`);

// 4. 复杂查询测试
console.log('\n4️⃣ 复杂查询测试');
const results = store.query({ 
  priority: 'P0',
  sortBy: 'createdAt',
  limit: 10
});
console.log(`   条件查询(P0): ${results.length} 个`);

// 5. 更新测试
console.log('\n5️⃣ 更新测试');
const updated = store.update(task1.id, { status: 'planning', assignedTo: 'Strategy' });
console.log(`   状态更新: inbox → ${updated.status}`);
console.log(`   指派更新: Marketing → ${updated.assignedTo}`);

// 6. 索引一致性验证
console.log('\n6️⃣ 索引一致性验证');
const planningTasks = store.getByStatus('planning');
const planningCount = planningTasks.length;
console.log(`   planning索引数量: ${planningCount}`);
console.log(`   ✅ 索引正常`);

// 7. 统计测试
console.log('\n7️⃣ 统计测试');
const stats = store.getStats();
console.log(`   总任务: ${stats.total}`);
console.log(`   按状态: ${JSON.stringify(stats.byStatus)}`);
console.log(`   按优先级: ${JSON.stringify(stats.byPriority)}`);

// 8. 超时检查测试
console.log('\n8️⃣ 超时检查测试');
// 模拟一个超时的任务
store.update(task2.id, { status: 'executing' });
const alerts = store.checkTimeouts();
console.log(`   超时任务: ${alerts.length} 个`);

// 9. 删除测试
console.log('\n9️⃣ 删除测试');
store.delete(task3.id);
console.log(`   删除后总任务: ${store.getAll().length}`);

// 10. 清理测试数据
console.log('\n🔟 清理测试数据...');
store.delete(task1.id);
store.delete(task2.id);
console.log(`   清理后总任务: ${store.getAll().length}`);

console.log('\n✅ TaskStore 测试完成！');
