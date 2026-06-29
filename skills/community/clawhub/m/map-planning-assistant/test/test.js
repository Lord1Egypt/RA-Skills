/**
 * 全能地图规划助理测试文件
 */

const { main, parseIntent } = require('../src/index');

// 测试意图解析
function testParseIntent() {
  console.log('=== 测试意图解析 ===\n');

  const testCases = [
    '帮我生成郑州市全能游玩地图',
    '给我制作成都市全套休闲地图',
    '帮我做杭州西湖区溜娃地图',
    '给我找武汉适合夜跑的路线',
    '生成西安人间烟火夜市清单',
    '查看我的用户画像',
    '调取历史游历城市',
    '推送本周本地活动',
    '开启旅行模式规划3日自驾游',
    '讲解开封鼓楼人文历史'
  ];

  for (const testCase of testCases) {
    const intent = parseIntent(testCase);
    console.log(`输入: ${testCase}`);
    console.log(`意图: ${JSON.stringify(intent, null, 2)}`);
    console.log('---');
  }
}

// 测试主函数（模拟）
async function testMain() {
  console.log('\n=== 测试主函数 ===\n');

  // 注意：这个测试需要配置AMAP_API_KEY环境变量才能正常运行
  if (!process.env.AMAP_API_KEY) {
    console.log('跳过主函数测试：未配置AMAP_API_KEY环境变量');
    return;
  }

  const testCases = [
    { message: '帮我生成北京市全能游玩地图', userId: 'test_user_1' },
    { message: '帮我做上海溜娃地图', userId: 'test_user_2' },
    { message: '查看我的用户画像', userId: 'test_user_1' }
  ];

  for (const testCase of testCases) {
    console.log(`测试: ${testCase.message}`);
    try {
      const result = await main({
        userMessage: testCase.message,
        userId: testCase.userId
      });
      console.log('结果类型:', result.type);
      console.log('内容预览:', result.content ? result.content.substring(0, 200) + '...' : '无内容');
    } catch (error) {
      console.error('错误:', error.message);
    }
    console.log('---');
  }
}

// 运行测试
async function runTests() {
  console.log('🗺️ 全能地图规划助理测试\n');

  testParseIntent();
  await testMain();

  console.log('\n✅ 测试完成');
}

// 如果直接运行此文件
if (require.main === module) {
  runTests().catch(console.error);
}

module.exports = {
  testParseIntent,
  testMain,
  runTests
};
