/**
 * 测试个人地图生成功能
 */

const amap = require('../src/utils/amap');

// 模拟POI数据
const mockPois = {
  dogWalking: [
    { id: '1', name: '朝阳公园', location: '116.473,39.942', address: '北京市朝阳区' },
    { id: '2', name: '奥林匹克森林公园', location: '116.385,40.015', address: '北京市朝阳区' }
  ],
  running: [
    { id: '3', name: '北京奥林匹克公园', location: '116.385,40.015', address: '北京市朝阳区' }
  ]
};

// 测试单个地图创建
async function testSingleMap() {
  console.log('=== 测试单个地图创建 ===\n');

  try {
    const result = await amap.createPersonalMap(mockPois);
    console.log('结果:', JSON.stringify(result, null, 2));
  } catch (error) {
    console.error('错误:', error.message);
  }
  console.log('\n');
}

// 测试批量地图创建
async function testBatchMap() {
  console.log('=== 测试批量地图创建 ===\n');

  // 创建大量POI数据
  const largePois = {};
  for (let i = 0; i < 5; i++) {
    largePois[`scene_${i}`] = [];
    for (let j = 0; j < 15; j++) {
      largePois[`scene_${i}`].push({
        id: `${i}_${j}`,
        name: `测试点位 ${i}-${j}`,
        location: `${116 + (i * 0.1) + (j * 0.01)},${39 + (i * 0.1) + (j * 0.01)}`,
        address: `测试地址 ${i}-${j}`
      });
    }
  }

  try {
    const result = await amap.createBatchPersonalMaps(largePois);
    console.log('结果:', JSON.stringify(result, null, 2));
  } catch (error) {
    console.error('错误:', error.message);
  }
  console.log('\n');
}

// 测试坐标验证
function testCoordinateValidation() {
  console.log('=== 测试坐标验证 ===\n');

  const testCases = [
    { location: '116.473,39.942', expected: true, desc: '有效坐标（北京）' },
    { location: '121.474,31.230', expected: true, desc: '有效坐标（上海）' },
    { location: '200,39.942', expected: false, desc: '无效经度（超出范围）' },
    { location: '116.473,60', expected: false, desc: '无效纬度（超出范围）' },
    { location: 'abc,def', expected: false, desc: '非数字坐标' },
    { location: '116.473', expected: false, desc: '缺少纬度' },
    { location: '', expected: false, desc: '空字符串' },
    { location: null, expected: false, desc: 'null值' }
  ];

  for (const testCase of testCases) {
    let result = false;
    if (testCase.location) {
      const [lng, lat] = testCase.location.split(',').map(Number);
      if (!isNaN(lng) && !isNaN(lat) && lng >= 73 && lng <= 135 && lat >= 3 && lat <= 53) {
        result = true;
      }
    }

    const status = result === testCase.expected ? '✅' : '❌';
    console.log(`${status} ${testCase.desc}: ${testCase.location} -> ${result}`);
  }
  console.log('\n');
}

// 测试格式化输出
function testFormatOutput() {
  console.log('=== 测试格式化输出 ===\n');

  const mapResult = {
    success: true,
    url: 'https://a.amap.com/xxx',
    qrCode: 'https://a.amap.com/qr/xxx',
    pointCount: 50,
    totalPoints: 75,
    truncated: true,
    message: '已创建包含前50个点位的地图（共75个点位）'
  };

  const batchResult = {
    success: true,
    totalPoints: 75,
    batchCount: 2,
    maps: [
      {
        batchIndex: 1,
        pointCount: 50,
        url: 'https://a.amap.com/batch1',
        qrCode: 'https://a.amap.com/qr/batch1',
        points: ['点位1', '点位2', '点位3', '点位4', '点位5']
      },
      {
        batchIndex: 2,
        pointCount: 25,
        url: 'https://a.amap.com/batch2',
        qrCode: 'https://a.amap.com/qr/batch2',
        points: ['点位51', '点位52', '点位53']
      }
    ],
    message: '已分2批创建地图，共75个点位'
  };

  console.log('单地图结果:');
  console.log(formatMapResultSimple(mapResult));
  console.log('\n批量地图结果:');
  console.log(formatBatchMapResultSimple(batchResult));
}

// 简单格式化函数
function formatMapResultSimple(mapResult) {
  if (!mapResult.success) {
    return `❌ ${mapResult.message}`;
  }

  let output = `📱 高德个人地图\n`;
  output += `📍 点位数量: ${mapResult.pointCount}个\n`;

  if (mapResult.truncated) {
    output += `⚠️ 注意: 已截取前${mapResult.pointCount}个点位（共${mapResult.totalPoints}个）\n`;
  }

  if (mapResult.url) {
    output += `🔗 地图链接: ${mapResult.url}\n`;
  }

  if (mapResult.qrCode) {
    output += `📸 二维码: ${mapResult.qrCode}\n`;
  }

  output += `💡 扫描二维码或点击链接可在高德App中查看全部打卡点位\n`;

  return output;
}

function formatBatchMapResultSimple(batchResult) {
  if (!batchResult.success) {
    return `❌ ${batchResult.message}`;
  }

  let output = `📱 高德个人地图（分批创建）\n`;
  output += `📍 总点位数量: ${batchResult.totalPoints}个\n`;
  output += `📦 批次数量: ${batchResult.batchCount}批\n\n`;

  for (const map of batchResult.maps) {
    output += `第${map.batchIndex}批 (${map.pointCount}个点位)\n`;

    if (map.url) {
      output += `🔗 地图链接: ${map.url}\n`;
    }
    if (map.qrCode) {
      output += `📸 二维码: ${map.qrCode}\n`;
    }
    output += `📍 包含点位: ${map.points.slice(0, 3).join('、')}`;
    if (map.points.length > 3) {
      output += `等${map.points.length}个`;
    }
    output += '\n\n';
  }

  return output;
}

// 运行测试
async function runTests() {
  console.log('🗺️ 个人地图生成功能测试\n');
  console.log('=' .repeat(50) + '\n');

  // 测试坐标验证（不需要API）
  testCoordinateValidation();

  // 测试格式化输出（不需要API）
  testFormatOutput();

  // 如果配置了API密钥，测试实际创建
  if (process.env.AMAP_API_KEY) {
    console.log('=' .repeat(50) + '\n');
    console.log('⚠️  检测到AMAP_API_KEY，将测试实际API调用\n');

    await testSingleMap();
    await testBatchMap();
  } else {
    console.log('=' .repeat(50) + '\n');
    console.log('ℹ️  未配置AMAP_API_KEY，跳过实际API调用测试\n');
  }

  console.log('=' .repeat(50));
  console.log('\n✅ 测试完成');
}

// 如果直接运行此文件
if (require.main === module) {
  runTests().catch(console.error);
}

module.exports = {
  testSingleMap,
  testBatchMap,
  testCoordinateValidation,
  testFormatOutput,
  runTests
};
