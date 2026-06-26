#!/usr/bin/env node

/**
 * 从本地模型库加载所有夹具，配置行为动作
 * 日期：2026-03-16
 * 
 * 关键发现：使用 /model/create + checkFromCloud: false
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

async function createGripper(name, rename, position) {
  const result = await callAPI('/model/create', {
    id: name,
    rename: rename,
    position: position,
    eulerAngle: [0, 0, 0],
    checkFromCloud: false  // 从本地模型库创建
  });
  
  if (result.data?.taskId) {
    // 轮询等待
    for (let i = 0; i < 10; i++) {
      await sleep(1000);
      const status = await callAPI('/task/query', { taskId: result.data.taskId });
      
      if (status.data.done) {
        if (status.data.resultCode === 200) {
          return await getModelIdByName(rename);
        } else {
          throw new Error(`Create failed: ${status.data.resultMsg}`);
        }
      }
    }
    throw new Error('Create timeout');
  }
  throw new Error('No taskId');
}

async function addBehavior(modelId, behavioralType, referenceAxis, minValue, maxValue, runSpeed) {
  return await callAPI('/behavior/add', {
    id: modelId,
    useModeId: true,
    behavioralType,
    referenceAxis,
    minValue,
    maxValue,
    runSpeed,
    runState: 0  // 循环
  });
}

async function testAllGrippers() {
  console.log('🧪 从本地模型库加载所有夹具，配置行为动作\n');
  console.log('方法：/model/create + checkFromCloud: false\n');
  console.log('=' .repeat(70));
  
  const results = {
    created: [],
    behaviors: [],
    failed: []
  };
  
  try {
    // 1. 清理
    console.log('\n🧹 清理场景中的测试夹具...');
    const allInfo0 = await callAPI('/GetAllModelInfo', {});
    const testModels = (allInfo0.data?.models || []).filter(m => 
      m.modelName?.includes('测试_夹具')
    );
    if (testModels.length > 0) {
      const ids = testModels.map(m => m.modelId || m.id);
      await callAPI('/model/destroy', { ids });
      await sleep(1500);
      console.log(`   清理了 ${testModels.length} 个模型`);
    }
    
    // 2. 定义夹具列表
    const grippers = [
      { 
        name: 'DH_RGD_5_14', 
        rename: '测试_夹具_RGD', 
        position: [0, 0, 0],
        behavior: { type: 2, axis: 2, min: -90, max: 90, speed: 90 }  // 旋转 Z 轴
      },
      { 
        name: 'DH_PGE_100_26', 
        rename: '测试_夹具_PGE', 
        position: [200, 0, 0],
        behavior: { type: 2, axis: 2, min: -90, max: 90, speed: 90 }
      },
      { 
        name: 'DH_PGS_5_5', 
        rename: '测试_夹具_PGS', 
        position: [400, 0, 0],
        behavior: { type: 2, axis: 2, min: -90, max: 90, speed: 90 }
      },
      { 
        name: 'DH_PGI_140_80', 
        rename: '测试_夹具_PGI', 
        position: [600, 0, 0],
        behavior: { type: 2, axis: 2, min: -90, max: 90, speed: 60 }  // 大型夹具，慢速
      },
      { 
        name: 'Mechanical Gripper', 
        rename: '测试_夹具_Mechanical', 
        position: [800, 0, 0],
        behavior: { type: 2, axis: 2, min: -90, max: 90, speed: 30 }  // 超大型，最慢
      }
    ];
    
    // 3. 创建夹具
    console.log('\n📦 创建夹具...\n');
    
    for (const g of grippers) {
      console.log(`- 创建 ${g.name}...`);
      try {
        const modelId = await createGripper(g.name, g.rename, g.position);
        console.log(`   ✅ ${g.rename}: ${modelId}`);
        results.created.push({
          name: g.name,
          rename: g.rename,
          modelId: modelId
        });
      } catch (error) {
        console.log(`   ❌ 失败：${error.message}`);
        results.failed.push({
          name: g.name,
          error: error.message
        });
      }
      await sleep(500);
    }
    
    console.log('\n' + '=' .repeat(70));
    console.log(`\n✅ 成功创建 ${results.created.length}/${grippers.length} 个夹具\n`);
    
    // 4. 配置行为
    console.log('🔧 配置行为动作...\n');
    
    for (const g of grippers) {
      const created = results.created.find(c => c.rename === g.rename);
      if (!created) continue;
      
      console.log(`- ${g.rename}:`);
      
      // 获取模型信息
      const modelInfo = await callAPI('/GetModelInfo', { id: created.modelId, useModeId: true });
      const boundSize = modelInfo.data?.boundSize || [100, 100, 100];
      const volume = boundSize[0] * boundSize[1] * boundSize[2];
      
      console.log(`   尺寸：${boundSize.join(' x ')} mm`);
      console.log(`   体积：${(volume / 1000).toFixed(1)} cm³`);
      
      // 配置行为
      const behaviorResult = await addBehavior(
        created.modelId,
        g.behavior.type,
        g.behavior.axis,
        g.behavior.min,
        g.behavior.max,
        g.behavior.speed
      );
      
      if (behaviorResult.code === 200) {
        console.log(`   ✅ 行为已配置：旋转 ${g.behavior.min}° ~ ${g.behavior.max}° (${g.behavior.speed}°/s)`);
        results.behaviors.push({
          modelId: created.modelId,
          type: 'rotation',
          axis: 'Z',
          range: `${g.behavior.min}° ~ ${g.behavior.max}°`
        });
      } else {
        console.log(`   ❌ 行为配置失败：${behaviorResult.msg}`);
        results.failed.push({
          model: g.rename,
          error: behaviorResult.msg
        });
      }
      
      console.log();
    }
    
    // 5. 验证所有行为
    console.log('=' .repeat(70));
    console.log('\n🔍 验证行为配置...\n');
    
    for (const g of results.created) {
      const behaviorInfo = await callAPI('/behavior/get', {
        id: g.modelId,
        useModeId: true
      });
      
      console.log(`${g.rename}:`);
      if (behaviorInfo.data?.hasBehavior) {
        console.log(`   ✅ 有行为配置`);
        console.log(`      - 类型：${behaviorInfo.data.behavioralType} (2=旋转)`);
        console.log(`      - 轴：${behaviorInfo.data.referenceAxis} (2=Z 轴)`);
        console.log(`      - 范围：[${behaviorInfo.data.minValue}, ${behaviorInfo.data.maxValue}]`);
        console.log(`      - 速度：${behaviorInfo.data.runSpeed}°/s`);
      } else {
        console.log(`   ❌ 无行为配置`);
      }
      console.log();
    }
    
    // 6. 总结
    console.log('=' .repeat(70));
    console.log('\n📊 测试总结\n');
    console.log(`✅ 创建成功：${results.created.length}/${grippers.length}`);
    console.log(`✅ 行为配置：${results.behaviors.length} 个`);
    console.log(`❌ 失败：${results.failed.length} 个\n`);
    
    if (results.created.length > 0) {
      console.log('📋 夹具列表:\n');
      results.created.forEach((g, i) => {
        console.log(`   ${i+1}. ${g.rename}`);
        console.log(`      - 原始名称：${g.name}`);
        console.log(`      - Model ID: ${g.modelId}`);
        console.log(`      - 位置：${g.position.join(', ')}`);
        console.log(`      - 行为：旋转 ±90°（Z 轴）\n`);
      });
    }
    
  } catch (error) {
    console.log('\n❌ 测试异常:', error.message);
    console.log(error.stack);
  }
}

testAllGrippers().catch(console.error);
