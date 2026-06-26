#!/bin/bash
# prd-workflow v2.5.0 测试脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKFLOW_DIR="$SCRIPT_DIR"
OUTPUT_DIR="$WORKFLOW_DIR/test-output"

echo "=========================================="
echo "prd-workflow v2.5.0 测试"
echo "=========================================="
echo ""

# 清理测试输出
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# 测试 1：数据总线
echo "📦 测试 1：数据总线"
echo "----------------------------------------"
node -e "
const { DataBus } = require('./workflows/data_bus');
const dataBus = new DataBus('$OUTPUT_DIR');

// 测试写入
dataBus.write('interview', { keyDecisions: Array(12).fill({id: 'd1'}) }, { passed: true });
dataBus.write('decomposition', { features: [], userStories: ['As a...'], acceptanceCriteria: ['Given...'] }, { passed: true });

// 测试读取
const interview = dataBus.read('interview');
console.log('✅ 读取访谈结果:', interview ? '成功' : '失败');

// 测试状态
const status = dataBus.getStatus();
console.log('✅ 状态报告:', status.progress);
"
echo ""

# 测试 2：智能路由
echo "🧭 测试 2：智能路由"
echo "----------------------------------------"
node -e "
const { SmartRouter } = require('./workflows/smart_router');
const router = new SmartRouter();

// 测试解析
const skills1 = router.parseUserRequest('生成养老规划 PRD，包含评审和流程图');
console.log('✅ 识别技能:', skills1.join(', '));

// 测试模板
const skills2 = router.parseUserRequest('使用轻量流程');
console.log('✅ 模板识别:', skills2.join(', '));

// 测试执行计划
const plan = router.getExecutionPlan('生成 PRD，包含评审', '$OUTPUT_DIR');
console.log('✅ 执行计划:', plan.skillsToExecute.join(' → '));
"
echo ""

# 测试 3：质量门禁
echo "🔒 测试 3：质量门禁"
echo "----------------------------------------"
node -e "
const { QualityGate } = require('./workflows/quality_gates');

async function test() {
  const qualityGate = new QualityGate();
  
  // 测试通过
  const result1 = await qualityGate.pass('gate2_decomposition', {
    userStories: ['As a user, I want feature, So that value'],
    acceptanceCriteria: ['Given condition, When action, Then result']
  });
  console.log('✅ 门禁测试 1:', result1.passed ? '通过' : '失败');
  
  // 测试失败
  const result2 = await qualityGate.pass('gate2_decomposition', {
    userStories: ['invalid story'],
    acceptanceCriteria: ['invalid']
  });
  console.log('✅ 门禁测试 2:', result2.passed ? '通过' : '失败（预期）');
}

test().catch(console.error);
"
echo ""

# 测试 4：模块执行
echo "🧩 测试 4：模块执行"
echo "----------------------------------------"
node -e "
const { DataBus } = require('./workflows/data_bus');
const DecompositionModule = require('./workflows/modules/decomposition_module');
const PRDModule = require('./workflows/modules/prd_module');

async function test() {
  const dataBus = new DataBus('$OUTPUT_DIR');
  const decompositionModule = new DecompositionModule();
  const prdModule = new PRDModule();
  
  // 先创建访谈结果
  dataBus.write('interview', { keyDecisions: Array(12).fill({id: 'd1', topic: 'test'}) }, { passed: true });
  
  // 执行需求拆解
  console.log('执行需求拆解...');
  const decompResult = await decompositionModule.execute({
    dataBus: dataBus,
    outputDir: '$OUTPUT_DIR'
  });
  console.log('✅ 需求拆解完成');
  
  // 执行 PRD 生成
  console.log('执行 PRD 生成...');
  const prdResult = await prdModule.execute({
    dataBus: dataBus,
    outputDir: '$OUTPUT_DIR'
  });
  console.log('✅ PRD 生成完成');
  console.log('   章节数:', prdResult.chapters.length);
  console.log('   吸收率:', prdResult.absorptionCheck.absorptionRate + '%');
}

test().catch(console.error);
"
echo ""

# 测试 5：完整流程
echo "🚀 测试 5：完整流程（简化版）"
echo "----------------------------------------"
node -e "
const { prdWorkflow } = require('./workflows/main');

prdWorkflow('生成养老规划 PRD，包含评审和流程图', {
  outputDir: '$OUTPUT_DIR',
  autoRetry: true
}).then(result => {
  console.log('✅ 完整流程测试通过');
  console.log('   状态:', result.status.progress);
}).catch(error => {
  console.error('❌ 完整流程测试失败:', error.message);
  process.exit(1);
});
"
echo ""

# 输出测试报告
echo "=========================================="
echo "📊 测试报告"
echo "=========================================="
echo ""

if [ -f "$OUTPUT_DIR/interview.json" ]; then
  echo "✅ interview.json 已生成"
else
  echo "❌ interview.json 未生成"
fi

if [ -f "$OUTPUT_DIR/decomposition.json" ]; then
  echo "✅ decomposition.json 已生成"
else
  echo "❌ decomposition.json 未生成"
fi

if [ -f "$OUTPUT_DIR/prd.json" ]; then
  echo "✅ prd.json 已生成"
else
  echo "❌ prd.json 未生成"
fi

if [ -f "$OUTPUT_DIR/PRD.md" ]; then
  echo "✅ PRD.md 已生成"
  echo "   文件大小: $(wc -c < "$OUTPUT_DIR/PRD.md") bytes"
else
  echo "❌ PRD.md 未生成"
fi

echo ""
echo "=========================================="
echo "✅ 测试完成！"
echo "=========================================="
