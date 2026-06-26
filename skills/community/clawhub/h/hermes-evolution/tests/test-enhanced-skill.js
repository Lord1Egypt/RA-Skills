/**
 * EnhancedSkill 测试
 */

const {
  EnhancedSkill,
  auditSkills,
  printSkillDetails
} = require('./enhanced-skill');

console.log('🧪 EnhancedSkill 测试\n');

// 1. 创建增强 Skill
console.log('1️⃣ 创建增强 Skill');
const skill = new EnhancedSkill({
  name: 'task-router',
  description: '智能任务路由，根据意图置信度分配Agent'
});

// 添加步骤
skill
  .addStep('1', '解析输入文本', ['使用 IntentRouter 进行分词'])
  .addStep('2', '计算置信度', ['多词命中加权', '排除词过滤'])
  .addStep('3', '路由到 Agent', ['显式指定 > 置信度'])
  .addStep('4', '构建执行 Prompt', ['注入 Agent Profile']);

// 添加陷阱
skill
  .addPitfall(
    '关键词完全匹配',
    '无法处理同义词，导致误路由',
    '使用语义相似度计算而非精确匹配'
  )
  .addPitfall(
    '置信度阈值过低',
    '模糊输入被错误路由',
    '设置最低置信度门限 (如 0.5)'
  );

// 设置验证方法
skill.setVerification(
  '运行 test-intent-router.js',
  '23/23 测试通过',
  '有测试用例失败'
);

// 添加示例
skill
  .addExample(
    '@marketing 发布小红书',
    'Marketing Agent',
    '显式指定场景'
  )
  .addExample(
    '帮我分析一下市场机会',
    'Strategy Agent',
    '意图识别场景'
  )
  .addExample(
    'Gateway进程挂了吗',
    'RD Agent',
    '运维识别场景'
  );

console.log('   Skill 创建完成');
console.log(`   完整度: ${skill.calculateCompleteness()}%`);

// 2. 验证 Skill
console.log('\n2️⃣ 验证 Skill 完整性');
const validation = skill.validate();
console.log(`   验证结果: ${validation.valid ? '✅ 通过' : '❌ 失败'}`);
if (validation.errors.length > 0) {
  console.log('   错误:');
  for (const err of validation.errors) {
    console.log(`   - ${err}`);
  }
}

// 3. 打印详情
console.log('\n3️⃣ 打印 Skill 详情');
printSkillDetails(skill);

// 4. 审计现有 Skills
console.log('\n4️⃣ 审计现有 Skills');
const auditResult = auditSkills();
if (auditResult.error) {
  console.log(`   错误: ${auditResult.error}`);
} else {
  console.log(`   总计: ${auditResult.total} 个文件`);
  console.log(`   增强型: ${auditResult.enhanced}`);
  console.log(`   传统型: ${auditResult.legacy}`);
  
  if (auditResult.issues.length > 0) {
    console.log('\n   问题列表:');
    for (const issue of auditResult.issues) {
      console.log(`   - ${issue.file}`);
      if (issue.errors) {
        for (const err of issue.errors) {
          console.log(`     ${err}`);
        }
      }
    }
  }
}

// 5. 测试序列化
console.log('\n5️⃣ 测试 JSON 序列化');
const json = skill.toJSON();
console.log('   序列化字段:');
console.log(`   - name: ${json.name}`);
console.log(`   - description: ${json.description.substring(0, 30)}...`);
console.log(`   - procedure: ${json.procedure.length} 步`);
console.log(`   - pitfalls: ${json.pitfalls.length} 个`);
console.log(`   - verification: ${json.verification ? '✓' : '✗'}`);
console.log(`   - examples: ${json.examples.length} 个`);

// 6. 测试 load/save
console.log('\n6️⃣ 测试保存和加载');
const testPath = 'C:\\Users\\t\\.openclaw\\workspace\\skills\\sensen-pm-router\\test-skill.json';
skill.metadata.tags = ['router', 'pm', 'intent'];
skill.save(testPath);

const loaded = EnhancedSkill.load(testPath);
console.log(`   加载成功: ${loaded.name}`);
console.log(`   标签: ${loaded.metadata.tags.join(', ')}`);

// 清理测试文件
console.log('\n7️⃣ 清理测试文件');
require('fs').unlinkSync(testPath);
console.log('   已删除测试文件');

console.log('\n✅ EnhancedSkill 测试完成！');
console.log('\nP0-3 Skill结构增强 总结:');
console.log('  📝 procedure - 使用步骤（how to use）');
console.log('  ⚠️ pitfalls - 常见错误（common mistakes）');
console.log('  ✅ verification - 验证方法（how to verify）');
console.log('  📖 examples - 使用示例');
console.log('  📊 validate() - 验证完整性');
console.log('  📊 calculateCompleteness() - 完整度得分');
