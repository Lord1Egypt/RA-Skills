#!/usr/bin/env node

/**
 * 智能 50 轮测试 - 自动准备测试环境
 * 先下载所需设备到场景，再测试相关 API
 */

import http from 'http';
import fs from 'fs';

const HOST = '100.85.119.45';  // Tailscale IP
const PORT = 16888;
const TEST_LOG = 'test-results-smart-2026-03-13.json';

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
      timeout: 30000,  // 30 秒超时
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
    req.on('timeout', () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });
    req.write(body);
    req.end();
  });
}

// 测试环境状态
let testEnv = {
  models: [],        // 场景中的模型
  cameras: [],       // 场景中的相机
  sensors: [],       // 场景中的传感器
  robots: [],        // 场景中的机器人
  conveyors: [],     // 场景中的传送带
};

// 准备工作：下载测试所需设备到场景
async function prepareTestEnvironment() {
  console.log('\n🔧 准备测试环境...');
  
  try {
    // 1. 下载纸箱（通用模型）
    console.log('  📦 下载纸箱...');
    const boxResult = await call('/model/download', {
      id: '纸箱',
      createInScene: true,
      position: [0, 0, 0],
      eulerAngle: [0, 0, 0],
      rename: 'test_box'
    });
    if (boxResult.code === 200) {
      testEnv.models.push('test_box');
      console.log('    ✅ 纸箱下载成功');
    }
    
    // 2. 下载相机设备
    console.log('  📷 下载相机...');
    const camResult = await call('/model/download', {
      id: '相机',
      createInScene: true,
      position: [1000, 0, 2000],
      eulerAngle: [0, 0, 0],
      rename: 'test_camera'
    });
    if (camResult.code === 200) {
      testEnv.cameras.push('test_camera');
      console.log('    ✅ 相机下载成功');
    }
    
    // 3. 查询场景中的所有模型，获取真实 ID
    console.log('  🔍 查询场景模型...');
    const allModels = await call('/GetAllModelInfo', {});
    if (allModels.code === 200 && allModels.data.models) {
      testEnv.models = allModels.data.models.map(m => ({
        modelId: m.modelId,
        modelName: m.modelName
      }));
      console.log(`    ✅ 场景中有 ${testEnv.models.length} 个模型`);
    }
    
    // 4. 查询相机列表
    console.log('  📷 查询相机列表...');
    const camList = await call('/sensor/queryCameralist', {});
    if (camList.code === 200 && camList.data) {
      testEnv.cameras = camList.data;
      console.log(`    ✅ 场景中有 ${testEnv.cameras.length} 个相机`);
    }
    
  } catch (err) {
    console.log('  ⚠️ 准备环境失败:', err.message);
  }
  
  console.log('✅ 测试环境准备完成\n');
}

// 清理环境：销毁测试创建的模型
async function cleanupTestEnvironment() {
  console.log('\n🧹 清理测试环境...');
  
  // 销毁测试创建的模型
  for (const model of testEnv.models) {
    if (model.modelName && model.modelName.startsWith('test_')) {
      try {
        await call('/model/destroy', {
          id: model.modelId,
          useModeId: true
        });
        console.log(`  ✅ 销毁 ${model.modelName}`);
      } catch (err) {
        // 忽略清理错误
      }
    }
  }
  
  console.log('✅ 清理完成\n');
}

// 智能测试用例（带前置条件检查）
const testCases = [
  // === 基础查询（无需前置条件） ===
  { 
    name: '获取所有模型', 
    endpoint: '/GetAllModelInfo', 
    data: {},
    expectSuccess: true
  },
  { 
    name: '获取层级树', 
    endpoint: '/models/tree', 
    data: { rootId: 'scene', useModeId: true, includeRoot: true },
    expectSuccess: true
  },
  { 
    name: '本地模型库查询', 
    endpoint: '/model/library/local', 
    data: {},
    expectSuccess: true
  },
  { 
    name: '远程模型库查询', 
    endpoint: '/model/library/remote', 
    data: { pageNum: 1, pageSize: 5 },
    expectSuccess: true
  },
  
  // === 模式切换（无需前置条件） ===
  { 
    name: '切换模式 - 场景构建', 
    endpoint: '/ChangeMode', 
    data: { id: 0 },
    expectSuccess: true
  },
  { 
    name: '切换模式 - 行为信号', 
    endpoint: '/ChangeMode', 
    data: { id: 1 },
    expectSuccess: true
  },
  { 
    name: '切换模式 - 机器人', 
    endpoint: '/ChangeMode', 
    data: { id: 2 },
    expectSuccess: true
  },
  { 
    name: '切换模式 - 数字孪生', 
    endpoint: '/ChangeMode', 
    data: { id: 3 },
    expectSuccess: true
  },
  
  // === 模型操作（需要先有模型） ===
  { 
    name: '获取模型信息', 
    endpoint: '/GetModelInfo', 
    data: { id: 'test_box', useModeId: false },
    expectSuccess: true,
    check: () => testEnv.models.length > 0
  },
  { 
    name: '设置模型姿态', 
    endpoint: '/model/set_pose', 
    data: { id: 'test_box', position: [100, 100, 50], eulerAngle: [0, 0, 45] },
    expectSuccess: true,
    check: () => testEnv.models.some(m => m.modelName === 'test_box')
  },
  { 
    name: '设置模型颜色', 
    endpoint: '/model/set_render', 
    data: { id: 'test_box', tempColor: [1, 0, 0, 1] },
    expectSuccess: true,
    check: () => testEnv.models.some(m => m.modelName === 'test_box')
  },
  
  // === 相机相关（需要先有相机） ===
  { 
    name: '相机拍照', 
    endpoint: '/sbt/sensor', 
    data: { id: 'test_camera', type: 1 },
    expectSuccess: true,
    check: () => testEnv.cameras.length > 0
  },
  
  // === 批量执行（无需前置条件） ===
  { 
    name: '批量执行', 
    endpoint: '/batch/execute', 
    data: { 
      atomic: false, 
      commands: [
        { url: '/GetAllModelInfo', body: {} }, 
        { url: '/models/tree', body: { rootId: 'scene' } }
      ] 
    },
    expectSuccess: true
  },
  
  // === 下载模型（无需前置条件） ===
  { 
    name: '下载模型并创建', 
    endpoint: '/model/download', 
    data: { 
      id: '纸箱', 
      createInScene: true, 
      position: [0, 0, 0], 
      eulerAngle: [0, 0, 0],
      rename: `test_box_${Date.now()}` 
    },
    expectSuccess: true
  },
  
  // === 销毁模型（无需前置条件） ===
  { 
    name: '销毁物体', 
    endpoint: '/model/destroy', 
    data: { id: 'test_box', useModeId: false },
    expectSuccess: true,
    check: () => testEnv.models.some(m => m.modelName === 'test_box')
  },
];

// 测试结果
let results = {
  startTime: new Date().toISOString(),
  totalTests: 0,
  successCount: 0,
  failCount: 0,
  skipCount: 0,
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
  
  // 每轮随机选择 3-5 个测试用例
  const numTests = Math.floor(Math.random() * 3) + 3;
  const shuffled = testCases.sort(() => 0.5 - Math.random());
  const selected = shuffled.slice(0, numTests);
  
  for (const tc of selected) {
    results.totalTests++;
    
    // 检查前置条件
    if (tc.check && !tc.check()) {
      results.skipCount++;
      console.log(`  ⏭️  ${tc.name} (跳过 - 前置条件不满足)`);
      roundResult.tests.push({
        name: tc.name,
        endpoint: tc.endpoint,
        success: false,
        skipped: true,
        reason: '前置条件不满足'
      });
      continue;
    }
    
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
        
        // 如果成功下载模型，更新环境
        if (tc.endpoint === '/model/download' && response.data?.created) {
          testEnv.models.push({
            modelId: response.data.modelId,
            modelName: response.data.modelName
          });
        }
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
      results.apiStats[tc.endpoint] = { calls: 0, success: 0, fail: 0, skip: 0 };
    }
    results.apiStats[tc.endpoint].calls++;
    if (result.success) results.apiStats[tc.endpoint].success++;
    else if (result.skipped) results.apiStats[tc.endpoint].skip++;
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
      successRate: ((results.successCount / (results.totalTests - results.skipCount)) * 100).toFixed(2) + '%',
      successCount: results.successCount,
      failCount: results.failCount,
      skipCount: results.skipCount
    },
    apiStats: results.apiStats,
    topErrors: results.errorDetails.slice(0, 10),
    recommendations: []
  };
  
  // 分析 API 成功率（排除跳过的）
  for (const [endpoint, stats] of Object.entries(results.apiStats)) {
    const actualCalls = stats.calls - stats.skip;
    if (actualCalls > 0) {
      const rate = (stats.success / actualCalls) * 100;
      if (rate < 90) {
        report.recommendations.push({
          endpoint,
          issue: `成功率低 (${rate.toFixed(1)}%)`,
          suggestion: '检查参数或文档'
        });
      }
    }
  }
  
  return report;
}

// 主函数
async function main() {
  console.log('🚀 开始智能 50 轮 API 自动化测试\n');
  console.log('目标主机:', HOST + ':' + PORT);
  console.log('测试用例:', testCases.length, '个');
  console.log('特点：自动准备测试环境，智能跳过不满足条件的测试');
  
  // 准备测试环境
  await prepareTestEnvironment();
  
  // 执行 50 轮测试
  for (let i = 1; i <= 50; i++) {
    await runRound(i);
  }
  
  // 清理测试环境
  await cleanupTestEnvironment();
  
  // 生成报告
  console.log('\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('📊 测试报告');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
  
  const report = generateReport();
  
  console.log('总体统计:');
  console.log('  总测试数:', report.summary.totalTests);
  console.log('  成功:', report.summary.successCount);
  console.log('  失败:', report.summary.failCount);
  console.log('  跳过:', report.summary.skipCount);
  console.log('  成功率:', report.summary.successRate);
  
  console.log('\nAPI 使用统计:');
  for (const [endpoint, stats] of Object.entries(results.apiStats)) {
    const actualCalls = stats.calls - stats.skip;
    const rate = actualCalls > 0 ? ((stats.success / actualCalls) * 100).toFixed(1) : 'N/A';
    console.log(`  ${endpoint}`);
    console.log(`    调用：${stats.calls} | 成功：${stats.success} | 失败：${stats.fail} | 跳过：${stats.skip} | 成功率：${rate}%`);
  }
  
  if (results.errorDetails.length > 0) {
    console.log('\n常见错误:');
    results.errorDetails.slice(0, 5).forEach((err, i) => {
      console.log(`  ${i+1}. ${err.test}: ${err.error}`);
    });
  }
  
  if (report.recommendations.length > 0) {
    console.log('\n改进建议:');
    report.recommendations.forEach(rec => {
      console.log(`  ⚠️  ${rec.endpoint}: ${rec.issue} - ${rec.suggestion}`);
    });
  }
  
  // 保存结果
  fs.writeFileSync(TEST_LOG, JSON.stringify({ report, results }, null, 2));
  console.log('\n💾 详细结果已保存到:', TEST_LOG);
  
  console.log('\n✅ 50 轮智能测试完成!');
}

main().catch(err => {
  console.error('❌ 测试中断:', err.message);
  process.exit(1);
});
