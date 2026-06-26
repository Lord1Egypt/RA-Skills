/**
 * AutoSkillGenerator 测试
 */

const { AutoSkillGenerator } = require('./auto-skill-generator');

console.log('🧪 AutoSkillGenerator 测试\n');

const generator = new AutoSkillGenerator({ minFrequency: 2 });

// 1. 记录工具调用
console.log('1️⃣ 记录工具调用序列');

// 模拟一个典型工作流：小红书内容发布
const workflow1 = [
  { tool: 'tavily_search', args: { query: '小红书热门话题' } },
  { tool: 'tavily_search', args: { query: '职场成长内容' } },
  { tool: 'content_writer', args: { topic: 'AI时代HR转型', platform: '小红书' } },
  { tool: 'message', args: { action: 'send', content: '生成的文案' } }
];

console.log('   记录工作流 1...');
for (const step of workflow1) {
  generator.recordCall(step.tool, step.args, { success: true });
}

console.log('   记录工作流 2 (重复)...');
for (const step of workflow1) {
  generator.recordCall(step.tool, step.args, { success: true });
}

console.log('   记录工作流 3 (重复)...');
for (const step of workflow1) {
  generator.recordCall(step.tool, step.args, { success: true });
}

// 2. 查看统计
console.log('\n2️⃣ 查看统计');
const stats = generator.getStats();
console.log(`   总调用: ${stats.totalCalls}`);
console.log(`   发现模式: ${stats.patterns}`);
console.log(`   候选模式: ${stats.candidatePatterns}`);
console.log(`   已生成 Skills: ${stats.generatedSkills}`);

// 3. 查看状态
console.log('\n3️⃣ 打印状态');
generator.printStatus();

// 4. 查看生成的 Skill
console.log('\n4️⃣ 查看生成的 Skill');
if (generator.generatedSkills.length > 0) {
  const skill = generator.generatedSkills[0];
  console.log(`   名称: ${skill.name}`);
  console.log(`   描述: ${skill.description}`);
  console.log(`   步骤数: ${skill.procedure.length}`);
  console.log(`   示例数: ${skill.examples.length}`);
  console.log(`   元数据:`, skill.metadata);
}

// 5. 模拟不同工作流
console.log('\n5️⃣ 模拟不同工作流');
const workflow2 = [
  { tool: 'task_manager', args: { action: 'create' } },
  { tool: 'task_manager', args: { action: 'update' } },
  { tool: 'feishu_notify', args: { message: '任务完成' } }
];

console.log('   记录工作流 2...');
for (const step of workflow2) {
  generator.recordCall(step.tool, step.args, { success: true });
}

console.log('   记录工作流 2 (重复)...');
for (const step of workflow2) {
  generator.recordCall(step.tool, step.args, { success: true });
}

const stats2 = generator.getStats();
console.log(`   更新后已生成 Skills: ${stats2.generatedSkills}`);

// 6. 清理测试文件
console.log('\n6️⃣ 清理测试生成的文件');
const fs = require('fs');
const path = require('path');
const outputDir = 'C:\\Users\\t\\.openclaw\\workspace\\skills\\auto-generated';
if (fs.existsSync(outputDir)) {
  const files = fs.readdirSync(outputDir).filter(f => f.includes('自动模式'));
  for (const file of files) {
    fs.unlinkSync(path.join(outputDir, file));
    console.log(`   已删除: ${file}`);
  }
}

console.log('\n✅ AutoSkillGenerator 测试完成！');
console.log('\nP2-1 自动技能创建 核心概念:');
console.log('  📝 recordCall() - 记录工具调用');
console.log('  🔍 detectPatterns() - 检测工作流模式');
console.log('  ⚙️ generateSkillFromPattern() - 自动生成 Skill');
console.log('  📊 getStats() - 获取统计信息');
console.log('\n效果: 观察重复工作流，自动封装为可复用 Skill');
