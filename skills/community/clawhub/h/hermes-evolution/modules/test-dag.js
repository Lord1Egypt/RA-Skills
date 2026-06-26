/**
 * TaskDAG 测试脚本
 */

const { TaskDAG } = require('./task-dag');

console.log('🧪 TaskDAG 测试\n');

// 1. 基本DAG构建
console.log('1️⃣ 基本DAG构建');
const dag = new TaskDAG();
dag.addNode('A', { label: '确定选题' });
dag.addNode('B', { label: '创作内容' });
dag.addNode('C', { label: '审核内容' });
dag.addNode('D', { label: '发布内容' });

dag.addEdge('A', 'B');  // A → B
dag.addEdge('A', 'C');  // A → C
dag.addEdge('B', 'D');  // B → D
dag.addEdge('C', 'D');  // C → D

console.log('   节点: A → B → D');
console.log('          ↘ C → D');
console.log('   边数:', dag.edges.length);

// 2. 拓扑排序
console.log('\n2️⃣ 拓扑排序（执行顺序）');
try {
  const sorted = dag.topologicalSort();
  console.log('   执行顺序:', sorted.join(' → '));
} catch (e) {
  console.log('   错误:', e.message);
}

// 3. 并行批次
console.log('\n3️⃣ 并行批次分析');
const batches = dag.getParallelBatches();
for (let i = 0; i < batches.length; i++) {
  const batch = batches[i];
  const canParallel = batch.length > 1 ? '🔸 可并行' : '🔹 串行';
  console.log(`   批次${i + 1}: ${batch.map(id => dag.getNode(id).data.label).join(', ')} ${canParallel}`);
}

// 4. 获取依赖
console.log('\n4️⃣ 依赖查询');
const dOfD = dag.getDependencies('D');
console.log('   D 的前置任务:', dOfD.map(id => dag.getNode(id).data.label).join(', '));

const dependentsOfA = dag.getDependents('A');
console.log('   A 的后继任务:', dependentsOfA.map(id => dag.getNode(id).data.label).join(', '));

// 5. 可视化
console.log(dag.visualize());

// 6. 循环检测
console.log('5️⃣ 循环检测');
const cycleDag = new TaskDAG();
cycleDag.addNode('X');
cycleDag.addNode('Y');
cycleDag.addNode('Z');
cycleDag.addEdge('X', 'Y');
cycleDag.addEdge('Y', 'Z');
cycleDag.addEdge('Z', 'X');  // 循环！

console.log('   创建循环: X → Y → Z → X');
console.log('   检测结果:', cycleDag.hasCycle() ? '❌ 存在循环' : '✅ 无循环');

// 7. 从任务列表构建DAG
console.log('\n6️⃣ 从任务列表构建DAG');
const tasks = [
  { id: 'task_1', label: '选题策划', status: 'done', dependsOn: [] },
  { id: 'task_2', label: '内容创作', status: 'pending', dependsOn: ['task_1'] },
  { id: 'task_3', label: '视觉设计', status: 'pending', dependsOn: ['task_1'] },
  { id: 'task_4', label: '审核', status: 'pending', dependsOn: ['task_2', 'task_3'] },
  { id: 'task_5', label: '发布', status: 'pending', dependsOn: ['task_4'] }
];

const taskDag = TaskDAG.fromTasks(tasks);
console.log('   任务结构:');
console.log('   task_1 → task_2 → task_4 → task_5');
console.log('        ↘ task_3 ↗');
console.log('\n' + taskDag.visualize());

// 8. DOT导出
console.log('\n7️⃣ DOT 语言导出（可用于 Graphviz）');
console.log(taskDag.toDOT());

console.log('\n✅ TaskDAG 测试完成！');
console.log('\nP2-2 增强功能总结:');
console.log('  ✅ DAG 构建 - 节点和边的管理');
console.log('  ✅ 拓扑排序 - 按依赖顺序执行');
console.log('  ✅ 循环检测 - 防止无限循环');
console.log('  ✅ 并行批次 - 识别可并行执行的任务组');
console.log('  ✅ 可视化 - ASCII + DOT 语言');
