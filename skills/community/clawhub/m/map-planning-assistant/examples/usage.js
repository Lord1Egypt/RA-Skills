/**
 * 全能地图规划助理 - 使用示例
 */

const { main } = require('../src/index');

// 示例1：生成全场景地图
async function example1() {
  console.log('示例1：生成全场景地图\n');

  const result = await main({
    userMessage: '帮我生成北京市全能游玩地图',
    userId: 'example_user_1'
  });

  console.log('结果类型:', result.type);
  console.log('内容预览:\n', result.content.substring(0, 500) + '...\n');
}

// 示例2：生成单场景地图
async function example2() {
  console.log('示例2：生成溜娃地图\n');

  const result = await main({
    userMessage: '帮我做杭州西湖区溜娃地图',
    userId: 'example_user_1'
  });

  console.log('结果类型:', result.type);
  console.log('内容预览:\n', result.content.substring(0, 500) + '...\n');
}

// 示例3：查看用户画像
async function example3() {
  console.log('示例3：查看用户画像\n');

  const result = await main({
    userMessage: '查看我的用户画像',
    userId: 'example_user_1'
  });

  console.log('结果类型:', result.type);
  console.log('内容:\n', result.content, '\n');
}

// 示例4：获取本地活动
async function example4() {
  console.log('示例4：获取本地活动\n');

  const result = await main({
    userMessage: '推送本周上海本地活动',
    userId: 'example_user_1'
  });

  console.log('结果类型:', result.type);
  console.log('内容预览:\n', result.content.substring(0, 500) + '...\n');
}

// 示例5：旅行模式
async function example5() {
  console.log('示例5：旅行模式\n');

  const result = await main({
    userMessage: '开启旅行模式规划成都3日自驾游',
    userId: 'example_user_1'
  });

  console.log('结果类型:', result.type);
  console.log('内容预览:\n', result.content.substring(0, 500) + '...\n');
}

// 示例6：人文讲解
async function example6() {
  console.log('示例6：人文讲解\n');

  const result = await main({
    userMessage: '讲解故宫的历史文化',
    userId: 'example_user_1'
  });

  console.log('结果类型:', result.type);
  console.log('内容预览:\n', result.content.substring(0, 500) + '...\n');
}

// 运行所有示例
async function runAllExamples() {
  console.log('🗺️ 全能地图规划助理 - 使用示例\n');
  console.log('=' .repeat(50) + '\n');

  // 注意：运行这些示例需要配置AMAP_API_KEY环境变量
  if (!process.env.AMAP_API_KEY) {
    console.log('⚠️  请先配置AMAP_API_KEY环境变量\n');
    console.log('配置方法：');
    console.log('  export AMAP_API_KEY=你的高德API密钥\n');
    console.log('或创建 .env 文件：');
    console.log('  AMAP_API_KEY=你的高德API密钥\n');
    return;
  }

  try {
    await example1();
    await example2();
    await example3();
    await example4();
    await example5();
    await example6();
  } catch (error) {
    console.error('运行示例时出错:', error.message);
  }

  console.log('=' .repeat(50));
  console.log('\n✅ 所有示例运行完成');
}

// 如果直接运行此文件
if (require.main === module) {
  runAllExamples().catch(console.error);
}

module.exports = {
  example1,
  example2,
  example3,
  example4,
  example5,
  example6,
  runAllExamples
};
