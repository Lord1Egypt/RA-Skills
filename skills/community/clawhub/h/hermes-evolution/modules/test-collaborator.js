/**
 * SENSEN Multi-Agent Collaborator - Phase 4 测试脚本
 */

const Collaborator = require('./sensen-collaborator');

async function runTests() {
  console.log('🚀 SENSEN Multi-Agent Collaborator Phase 4 - 测试开始\n');

  // 1. 创建顺序执行协作
  console.log('='.repeat(60));
  console.log('测试1: 顺序执行 (Sequential)');
  console.log('='.repeat(60));
  
  const seqCollab = Collaborator.createCollaboration({
    name: '每日内容发布流程',
    type: Collaborator.CollabType.SEQUENTIAL,
    description: '小红书内容制作流程：选题 → 创作 → 审核 → 发布',
    tasks: [
      { agent: 'Strategy', description: '确定今日选题方向' },
      { agent: 'Marketing', description: '根据选题创作内容' },
      { agent: 'CEO', description: '审核内容质量' },
      { agent: 'Marketing', description: '发布到小红书' }
    ]
  });

  console.log('\n执行前状态:');
  Collaborator.printCollaborationStatus(seqCollab);

  await Collaborator.runCollaboration(seqCollab.id);

  console.log('\n执行后状态:');
  const seqResult = Collaborator.loadCollaboration(seqCollab.id);
  Collaborator.printCollaborationStatus(seqResult);

  // 2. 创建并行执行协作
  console.log('\n' + '='.repeat(60));
  console.log('测试2: 并行执行 (Parallel)');
  console.log('='.repeat(60));
  
  const parCollab = Collaborator.createCollaboration({
    name: '多平台内容分发',
    type: Collaborator.CollabType.PARALLEL,
    description: '同一内容同时分发到多个平台',
    tasks: [
      { agent: 'Marketing', description: '发布到小红书' },
      { agent: 'Marketing', description: '发布到知乎' },
      { agent: 'Marketing', description: '发布到公众号' }
    ]
  });

  console.log('\n执行前状态:');
  Collaborator.printCollaborationStatus(parCollab);

  await Collaborator.runCollaboration(parCollab.id);

  console.log('\n执行后状态:');
  const parResult = Collaborator.loadCollaboration(parCollab.id);
  Collaborator.printCollaborationStatus(parResult);

  // 3. 创建层级执行协作
  console.log('\n' + '='.repeat(60));
  console.log('测试3: 层级执行 (Hierarchical)');
  console.log('='.repeat(60));
  
  const hierCollab = Collaborator.createCollaboration({
    name: '产品开发项目',
    type: Collaborator.CollabType.HIERARCHICAL,
    description: 'PRD → 技术开发 → 测试 → 上线',
    tasks: [
      { agent: 'Product', description: '制定产品PRD', dependsOn: [] },
      { agent: 'RD', description: '技术架构设计', dependsOn: [0] },
      { agent: 'RD', description: '功能开发', dependsOn: [1] },
      { agent: 'RD', description: '单元测试', dependsOn: [2] },
      { agent: 'CEO', description: '上线审批', dependsOn: [3] }
    ]
  });

  console.log('\n执行前状态:');
  Collaborator.printCollaborationStatus(hierCollab);

  await Collaborator.runCollaboration(hierCollab.id);

  console.log('\n执行后状态:');
  const hierResult = Collaborator.loadCollaboration(hierCollab.id);
  Collaborator.printCollaborationStatus(hierResult);

  // 4. 统计信息
  console.log('\n' + '='.repeat(60));
  console.log('📊 协作统计');
  console.log('='.repeat(60));
  console.log(Collaborator.getCollabStats());

  // 5. 清理测试数据
  console.log('\n🧹 清理测试协作...');
  // 注意：保留协作记录用于演示

  console.log('\n✅ Phase 4 测试完成!');
}

runTests().catch(console.error);
