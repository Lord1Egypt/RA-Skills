#!/usr/bin/env node

import http from 'http';
import fs from 'fs';

const HOST = '100.85.119.45';  // Tailscale IP
const PORT = 16888;
const TEST_LOG = 'test-results-2026-03-13.json';

// API 调用函数
async function call(endpoint, data = {}) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify(data);
    const req = http.request({
      hostname: HOST,
      port: PORT,
      path: endpoint,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body),
      },
    }, (res) => {
      let responseData = '';
      res.on('data', chunk => responseData += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(responseData));
        } catch (e) {
          reject(new Error('Parse error: ' + e.message));
        }
      });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

// 测试用例定义（2026-03-13 更新 - 包含新 API）
const testCases = [
  // 基础查询
  { name: '获取所有模型', endpoint: '/GetAllModelInfo', data: {} },
  { name: '获取层级树', endpoint: '/models/tree', data: { rootId: 'scene', useModeId: true, includeRoot: true } },
  { name: '获取场景 JSON', endpoint: '/scene/get_scene_json', data: {} },
  
  // 模型库管理（新增）
  { name: '本地模型库查询', endpoint: '/model/library/local', data: {} },
  { name: '远程模型库查询', endpoint: '/model/library/remote', data: { pageNum: 1, pageSize: 5 } },
  { name: '下载模型并创建', endpoint: '/model/download', data: { id: '纸箱', createInScene: true, position: [0, 0, 0], eulerAngle: [0, 0, 0], rename: 'test_box' } },
  
  // 模型操作
  { name: '获取模型信息', endpoint: '/GetModelInfo', data: { id: 'test_box', useModeId: false } },
  { name: '设置模型姿态', endpoint: '/model/set_pose', data: { id: 'test_box', position: [100, 100, 50], eulerAngle: [0, 0, 45] } },
  { name: '设置模型颜色', endpoint: '/model/set_render', data: { id: 'test_box', tempColor: [1, 0, 0, 1] } },
  
  // 层级与销毁（新增）
  { name: '销毁物体', endpoint: '/model/destroy', data: { id: 'test_box', useModeId: false } },
  
  // 场景控制
  { name: '重置场景', endpoint: '/ResetScene', data: {} },
  { name: '切换模式 - 场景构建', endpoint: '/ChangeMode', data: { id: 0 } },
  { name: '切换模式 - 行为信号', endpoint: '/ChangeMode', data: { id: 1 } },
  { name: '切换模式 - 机器人', endpoint: '/ChangeMode', data: { id: 2 } },
  { name: '切换模式 - 数字孪生', endpoint: '/ChangeMode', data: { id: 3 } },
  
  // 机器人（需要场景中有机器人）
  { name: '查询机器人 ID', endpoint: '/query/robot_id', data: {} },
  { name: '查询机器人位姿 (关节)', endpoint: '/query/robot_pos', data: { poseType: 1 } },
  
  // 传感器与物流
  { name: '传感器状态', endpoint: '/GetSensorStatus', data: { id: 'sensor1' } },
  { name: '传送带距离', endpoint: '/GetConveyorMoveDistance', data: { id: 'conveyor1' } },
  
  // 相机
  { name: '相机列表', endpoint: '/sensor/queryCameralist', data: {} },
  { name: '相机拍照', endpoint: '/sbt/sensor', data: { id: 'camera1', type: 1 } },
  
  // 高级功能
  { name: '批量执行', endpoint: '/batch/execute', data: { atomic: false, commands: [{ url: '/GetAllModelInfo', body: {} }, { url: '/models/tree', body: { rootId: 'scene' } }] } },
  { name: '添加行为', endpoint: '/behavior/add', data: { id: 'test_model', behavioralType: 1, referenceAxis: 0, minValue: -1000, maxValue: 1000, runSpeed: 200 } },
  { name: '获取行为', endpoint: '/behavior/get', data: { id: 'test_model', useModeId: false } },
];

// 测试结果
let results = {
  startTime: new Date().toISOString(),
  totalTests: 0,
  successCount: 0,
  failCount: 0,
  errorDetails: [],
  apiStats: {},
  roundResults: []
};

// 执行单轮测试
async function runRound(roundNum) {
  console.log(`\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
  console.log(`📍 第 ${roundNum} 轮测试`);
  console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
  
  const roundResult = {
    round: roundNum,
    timestamp: new Date().toISOString(),
    tests: []
  };
  
  // 随机选择 3-5 个测试用例执行
  const numTests = Math.floor(Math.random() * 3) + 3;
  const shuffled = testCases.sort(() => 0.5 - Math.random());
  const selected = shuffled.slice(0, numTests);
  
  for (const tc of selected) {
    results.totalTests++;
    
    const startTime = Date.now();
    let result = {
      name: tc.name,
      endpoint: tc.endpoint,
      success: false,
      duration: 0,
      error: null
    };
    
    try {
      const response = await call(tc.endpoint, tc.data);
      result.duration = Date.now() - startTime;
      result.success = response.code === 200;
      result.response = response;
      
      if (result.success) {
        results.successCount++;
        console.log(`  ✅ ${tc.name} (${result.duration}ms)`);
      } else {
        results.failCount++;
        result.error = response.msg;
        console.log(`  ❌ ${tc.name}: ${response.msg}`);
        results.errorDetails.push({
          round: roundNum,
          test: tc.name,
          endpoint: tc.endpoint,
          error: response.msg
        });
      }
    } catch (err) {
      result.duration = Date.now() - startTime;
      result.success = false;
      result.error = err.message;
      results.failCount++;
      console.log(`  ❌ ${tc.name}: ${err.message}`);
      results.errorDetails.push({
        round: roundNum,
        test: tc.name,
        endpoint: tc.endpoint,
        error: err.message
      });
    }
    
    roundResult.tests.push(result);
    
    // 统计 API 使用情况
    if (!results.apiStats[tc.endpoint]) {
      results.apiStats[tc.endpoint] = { calls: 0, success: 0, fail: 0, avgDuration: 0 };
    }
    results.apiStats[tc.endpoint].calls++;
    if (result.success) results.apiStats[tc.endpoint].success++;
    else results.apiStats[tc.endpoint].fail++;
  }
  
  results.roundResults.push(roundResult);
  
  // 短暂延迟
  await new Promise(r => setTimeout(r, 200));
}

// 生成报告
function generateReport() {
  const report = {
    summary: {
      totalRounds: 50,
      totalTests: results.totalTests,
      successRate: ((results.successCount / results.totalTests) * 100).toFixed(2) + '%',
      successCount: results.successCount,
      failCount: results.failCount
    },
    apiStats: results.apiStats,
    topErrors: results.errorDetails.slice(0, 10),
    recommendations: []
  };
  
  // 分析 API 成功率
  for (const [endpoint, stats] of Object.entries(results.apiStats)) {
    const rate = (stats.success / stats.calls) * 100;
    if (rate < 80) {
      report.recommendations.push({
        endpoint,
        issue: `成功率低 (${rate.toFixed(1)}%)`,
        suggestion: '检查参数或文档'
      });
    }
  }
  
  return report;
}

// 主函数
async function main() {
  console.log('🚀 开始 50 轮 API 自动化测试\n');
  console.log('目标主机:', HOST + ':' + PORT);
  console.log('测试用例:', testCases.length, '个');
  
  // 执行 50 轮测试
  for (let i = 1; i <= 50; i++) {
    await runRound(i);
  }
  
  // 生成报告
  console.log('\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('📊 测试报告');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
  
  const report = generateReport();
  
  console.log('总体统计:');
  console.log('  总测试数:', report.summary.totalTests);
  console.log('  成功:', report.summary.successCount);
  console.log('  失败:', report.summary.failCount);
  console.log('  成功率:', report.summary.successRate);
  
  console.log('\nAPI 使用统计:');
  for (const [endpoint, stats] of Object.entries(results.apiStats)) {
    const rate = ((stats.success / stats.calls) * 100).toFixed(1);
    console.log(`  ${endpoint}`);
    console.log(`    调用：${stats.calls} | 成功：${stats.success} | 失败：${stats.fail} | 成功率：${rate}%`);
  }
  
  if (results.errorDetails.length > 0) {
    console.log('\n常见错误:');
    results.errorDetails.slice(0, 5).forEach((err, i) => {
      console.log(`  ${i+1}. ${err.test}: ${err.error}`);
    });
  }
  
  // 保存结果
  fs.writeFileSync(TEST_LOG, JSON.stringify({ report, results }, null, 2));
  console.log('\n💾 详细结果已保存到:', TEST_LOG);
  
  console.log('\n✅ 50 轮测试完成!');
}

main().catch(err => {
  console.error('❌ 测试中断:', err.message);
  process.exit(1);
});
