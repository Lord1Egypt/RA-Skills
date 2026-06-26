#!/usr/bin/env node

/**
 * 从本地模型库加载夹具，配置行为动作
 * 日期：2026-03-16
 * 
 * 本地模型库中的夹具（EOAT/Gripping Jaws）：
 * - DH_PGE_100_26
 * - DH_PGI_140_80
 * - DH_PGS_5_5
 * - DH_RGD_5_14
 * - Mechanical Gripper
 */

import http from 'http';

const BASE_URL = 'http://100.85.119.45:16888';

function callAPI(endpoint, data) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify(data);
    const options = {
      hostname: new URL(BASE_URL).hostname,
      port: new URL(BASE_URL).port,
      path: endpoint,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body),
      },
    };

    const req = http.request(options, (res) => {
      let responseData = '';
      res.on('data', (chunk) => {
        responseData += chunk;
      });
      res.on('end', () => {
        try {
          resolve(JSON.parse(responseData));
        } catch (e) {
          reject(new Error(`Parse error: ${e.message}`));
        }
      });
    });

    req.on('error', (e) => {
      reject(new Error(`Connection error: ${e.message}`));
    });

    req.write(body);
    req.end();
  });
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function getModelIdByName(modelName) {
  const allInfo = await callAPI('/GetAllModelInfo', {});
  const models = allInfo.data?.models || [];
  const matched = models.filter(m => m.modelName === modelName);
  if (matched.length === 0) throw new Error(`Model not found: ${modelName}`);
  const model = matched[matched.length - 1];
  return model.modelId || model.id;
}

async function downloadAndWait(modelName, rename, position) {
  const result = await callAPI('/model/download', {
    id: modelName,
    createInScene: true,
    position: position || [0, 0, 0],
    rename: rename
  });
  
  if (result.data?.taskId) {
    for (let i = 0; i < 15; i++) {
      await sleep(1000);
      const status = await callAPI('/task/query', { taskId: result.data.taskId });
      
      if (status.data.done) {
        if (status.data.resultCode === 200) {
          const modelId = await getModelIdByName(rename);
          return { modelId, info: status.data.resultData };
        } else {
          throw new Error(`Download failed: ${status.data.resultMsg}`);
        }
      }
    }
    throw new Error('Download timeout');
  }
  throw new Error('No taskId returned');
}

async function addBehavior(params) {
  return await callAPI('/behavior/add', params);
}

// 行为类型常量
const BehavioralType = {
  TRANSLATION: 1,  // 直线运动
  ROTATION: 2,     // 旋转运动
  SIGNAL: 3,       // 信号
  PATH: 4,         // 路径
  CUSTOM: 5        // 自定义
};

// 参考轴常量
const ReferenceAxis = {
  X: 0,
  Y: 1,
  Z: 2,
  X_NEGATIVE: 3,
  Y_NEGATIVE: 4,
  Z_NEGATIVE: 5
};

async function testGrippersBehavior() {
  console.log('🧪 从本地模型库加载夹具，配置行为动作\n');
  console.log('=' .repeat(60));
  
  const results = {
    downloaded: [],
    behaviors: [],
    failed: []
  };
  
  try {
    // 1. 清理场景
    console.log('\n🧹 清理场景...');
    const allInfo0 = await callAPI('/GetAllModelInfo', {});
    const testModels = (allInfo0.data?.models || []).filter(m => 
      m.modelName?.includes('测试_') || 
      m.modelName?.includes('DH_') ||
      m.modelName?.includes('Mechanical') ||
      m.modelName?.includes('夹具_')
    );
    if (testModels.length > 0) {
      const ids = testModels.map(m => m.modelId || m.id);
      await callAPI('/model/destroy', { ids });
      await sleep(2000);
      console.log(`   清理了 ${testModels.length} 个模型`);
    }
    
    // 2. 定义要下载的夹具
    const grippers = [
      { name: 'DH_RGD_5_14', rename: '测试_夹具_RGD', position: [0, 0, 0] },
      { name: 'DH_PGE_100_26', rename: '测试_夹具_PGE', position: [200, 0, 0] },
      { name: 'DH_PGS_5_5', rename: '测试_夹具_PGS', position: [400, 0, 0] },
      { name: 'DH_PGI_140_80', rename: '测试_夹具_PGI', position: [600, 0, 0] },
      { name: 'Mechanical Gripper', rename: '测试_夹具_Mechanical', position: [800, 0, 0] }
    ];
    
    // 3. 下载夹具
    console.log('\n📥 下载夹具...\n');
    
    for (const gripper of grippers) {
      console.log(`- 下载 ${gripper.name}...`);
      try {
        const result = await downloadAndWait(
          gripper.name,
          gripper.rename,
          gripper.position
        );
        console.log(`   ✅ ${gripper.rename}: ${result.modelId}`);
        results.downloaded.push({
          name: gripper.name,
          rename: gripper.rename,
          modelId: result.modelId
        });
      } catch (error) {
        console.log(`   ❌ 失败：${error.message}`);
        results.failed.push({
          name: gripper.name,
          error: error.message
        });
      }
      await sleep(500);
    }
    
    console.log('\n' + '=' .repeat(60));
    console.log(`\n✅ 成功下载 ${results.downloaded.length} 个夹具\n`);
    
    // 4. 配置行为动作
    console.log('🔧 配置行为动作...\n');
    
    for (const gripper of results.downloaded) {
      console.log(`- 为 ${gripper.rename} 配置行为...`);
      
      // 获取模型信息（查看 bounding box）
      const modelInfo = await callAPI('/GetModelInfo', { id: gripper.modelId, useModeId: true });
      const boundSize = modelInfo.data?.boundSize || [100, 100, 100];
      const volume = boundSize[0] * boundSize[1] * boundSize[2];
      
      console.log(`   尺寸：${boundSize.join(' x ')} mm`);
      console.log(`   体积：${(volume / 1000).toFixed(1)} cm³`);
      
      // 根据体积判断夹具大小，配置不同的行为
      const isLarge = volume > 100000000; // 1 亿立方毫米
      
      // 配置旋转行为（绕 Z 轴旋转 ±90°）
      const behaviorResult = await addBehavior({
        id: gripper.modelId,
        useModeId: true,
        behavioralType: BehavioralType.ROTATION,
        referenceAxis: ReferenceAxis.Z,
        minValue: -90,
        maxValue: 90,
        runSpeed: isLarge ? 30 : 90,
        runState: 0  // 循环
      });
      
      if (behaviorResult.code === 200) {
        console.log(`   ✅ 旋转行为已配置（±90°, ${isLarge ? '慢速' : '快速'}）`);
        results.behaviors.push({
          modelId: gripper.modelId,
          type: 'rotation',
          axis: 'Z',
          range: '±90°'
        });
      } else {
        console.log(`   ❌ 行为配置失败：${behaviorResult.msg}`);
        results.failed.push({
          model: gripper.rename,
          error: behaviorResult.msg
        });
      }
      
      await sleep(300);
    }
    
    // 5. 验证行为配置
    console.log('\n' + '=' .repeat(60));
    console.log('\n🔍 验证行为配置...\n');
    
    for (const gripper of results.downloaded) {
      const behaviorInfo = await callAPI('/behavior/get', {
        id: gripper.modelId,
        useModeId: true
      });
      
      const behaviors = behaviorInfo.data?.behaviors || [];
      console.log(`${gripper.rename}:`);
      console.log(`   行为数量：${behaviors.length}`);
      
      if (behaviors.length > 0) {
        behaviors.forEach((b, i) => {
          console.log(`   ${i+1}. 类型=${b.behavioralType}, 轴=${b.referenceAxis}, 范围=[${b.minValue}, ${b.maxValue}]`);
        });
      }
      console.log();
    }
    
    // 6. 输出总结
    console.log('=' .repeat(60));
    console.log('\n📊 测试总结\n');
    console.log(`✅ 下载成功：${results.downloaded.length}/${grippers.length}`);
    console.log(`✅ 行为配置：${results.behaviors.length} 个`);
    console.log(`❌ 失败：${results.failed.length} 个\n`);
    
    if (results.downloaded.length > 0) {
      console.log('📋 夹具列表:\n');
      results.downloaded.forEach((g, i) => {
        console.log(`   ${i+1}. ${g.rename}`);
        console.log(`      - 原始名称：${g.name}`);
        console.log(`      - Model ID: ${g.modelId}`);
        console.log(`      - 行为：旋转 ±90°（Z 轴）\n`);
      });
    }
    
  } catch (error) {
    console.log('\n❌ 测试异常:', error.message);
    console.log(error.stack);
  }
}

testGrippersBehavior().catch(console.error);
