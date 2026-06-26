/**
 * MiMo 联网搜索技能测试
 */

const { mimoWebSearch, searchAndFormat } = require('./index.js');

async function test() {
  console.log('=== MiMo 联网搜索技能测试 ===\n');

  // 测试 1: 搜索 MiMo 基准测试
  console.log('测试 1: 搜索 MiMo 基准测试');
  try {
    const result = await mimoWebSearch('MiMo-V2-Flash 的基准测试结果是什么？');
    if (result.success) {
      console.log('✅ 搜索成功');
      console.log('内容预览:', result.content.substring(0, 200) + '...');
      console.log('使用量:', JSON.stringify(result.usage));
    } else {
      console.log('❌ 搜索失败:', result.error);
    }
  } catch (error) {
    console.log('❌ 测试失败:', error.message);
  }

  console.log('\n---\n');

  // 测试 2: 格式化搜索结果
  console.log('测试 2: 格式化搜索结果');
  try {
    const formatted = await searchAndFormat('2026 年 AI 大模型最新进展');
    console.log('✅ 格式化成功');
    console.log('格式化结果预览:', formatted.substring(0, 300) + '...');
  } catch (error) {
    console.log('❌ 格式化失败:', error.message);
  }

  console.log('\n=== 测试完成 ===');
}

// 运行测试
if (require.main === module) {
  test().catch(console.error);
}