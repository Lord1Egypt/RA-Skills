#!/usr/bin/env node

/**
 * 使用 createModel 创建模型，然后测试 /model/assemble
 * 日期：2026-03-16
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

async function testAssembleWithCreate() {
  console.log('🧪 使用 createModel 创建模型，测试 /model/assemble\n');
  console.log('目标：验证 /model/assemble 是否需要特定类型的模型\n');
  
  try {
    // 清理
    console.log('🧹 清理测试模型...');
    const allInfo0 = await callAPI('/GetAllModelInfo', {});
    const testModels = (allInfo0.data?.models || []).filter(m => 
      m.modelName?.includes('测试_') || 
      m.modelName?.includes('2D 相机')
    );
    if (testModels.length > 0) {
      const ids = testModels.map(m => m.modelId || m.id);
      await callAPI('/model/destroy', { ids });
      await sleep(1500);
      console.log(`   清理了 ${testModels.length} 个模型`);
    }
    console.log();
    
    // 1. 使用 /model/create 创建支架（使用机器人底座模型类型）
    console.log('📦 创建支架（尝试使用 Robot Base 类型）...');
    
    // 先尝试创建简单的方形
    const parentResult = await callAPI('/model/create', {
      id: '方形',
      rename: '测试_支架',
      position: [0, 0, 0],
      eulerAngle: [0, 0, 0],
      parameterizationCfg: {
        length: 100,
        width: 100,
        height: 20
      },
      checkFromCloud: false
    });
    
    console.log('创建响应:', JSON.stringify(parentResult, null, 2));
    
    if (parentResult.data?.taskId) {
      await sleep(2000);
      const status = await callAPI('/task/query', { taskId: parentResult.data.taskId });
      console.log('支架创建状态:', status.data.status);
      
      if (status.data.resultCode !== 200) {
        console.log('❌ 支架创建失败:', status.data.resultMsg);
        return;
      }
    }
    
    // 2. 创建相机（使用 Box Sensor 模拟）
    console.log('\n📦 创建相机（使用 Box Sensor 类型）...');
    const childResult = await callAPI('/model/create', {
      id: 'Box Sensor_Tra',
      rename: '测试_相机',
      position: [0, 0, 50],
      eulerAngle: [0, 0, 0],
      checkFromCloud: true
    });
    
    console.log('创建响应:', JSON.stringify(childResult, null, 2));
    
    if (childResult.data?.taskId) {
      await sleep(3000);
      const status = await callAPI('/task/query', { taskId: childResult.data.taskId });
      console.log('相机创建状态:', status.data.status);
      console.log('resultData:', JSON.stringify(status.data.resultData, null, 2));
      
      if (status.data.resultCode !== 200) {
        console.log('⚠️ 相机创建失败，尝试使用方形代替');
        // 使用方形代替
        const childResult2 = await callAPI('/model/create', {
          id: '方形',
          rename: '测试_相机',
          position: [0, 0, 50],
          parameterizationCfg: {
            length: 40,
            width: 40,
            height: 40
          },
          checkFromCloud: false
        });
        
        if (childResult2.data?.taskId) {
          await sleep(2000);
          const status2 = await callAPI('/task/query', { taskId: childResult2.data.taskId });
          console.log('相机创建状态:', status2.data.status);
        }
      }
    }
    
    await sleep(1000);
    
    // 3. 获取模型 ID
    console.log('\n🔍 获取模型 ID...');
    const allInfo = await callAPI('/GetAllModelInfo', {});
    const models = allInfo.data?.models || [];
    
    const parent = models.find(m => m.modelName === '测试_支架');
    const child = models.find(m => m.modelName === '测试_相机');
    
    if (!parent || !child) {
      console.log('❌ 未找到模型');
      console.log('场景中的模型:', models.map(m => m.modelName).join(', '));
      return;
    }
    
    console.log(`   支架：${parent.modelId}`);
    console.log(`   相机：${child.modelId}`);
    
    // 4. 检查模型类型
    console.log('\n🔍 检查模型信息...');
    const parentInfo = await callAPI('/GetModelInfo', { id: parent.modelId, useModeId: true });
    const childInfo = await callAPI('/GetModelInfo', { id: child.modelId, useModeId: true });
    
    console.log('支架信息:');
    console.log('  - type:', parentInfo.data?.type || 'N/A');
    console.log('  - modelName:', parentInfo.data?.modelName);
    
    console.log('相机信息:');
    console.log('  - type:', childInfo.data?.type || 'N/A');
    console.log('  - modelName:', childInfo.data?.modelName);
    
    // 5. 执行装配
    console.log('\n🔧 执行装配：相机 -> 支架（使用 /model/assemble）');
    const assembleResult = await callAPI('/model/assemble', {
      childId: child.modelId,
      parentId: parent.modelId,
      childUseModeId: true,
      parentUseModeId: true,
      assemblePosIndex: -1,
      replaceExisting: true
    });
    
    console.log('\n装配响应:', JSON.stringify(assembleResult, null, 2));
    
    if (assembleResult.code === 200) {
      console.log('\n✅ 装配成功（同步）');
      
      // 验证
      const cameraInfo = await callAPI('/GetModelInfo', { id: child.modelId, useModeId: true });
      console.log('\n相机父节点:', cameraInfo.data?.parentName || 'null');
      
    } else if (assembleResult.code === 202) {
      console.log('\n⏳ 等待异步任务...');
      await sleep(2000);
      const status = await callAPI('/task/query', { taskId: assembleResult.data.taskId });
      console.log('任务状态:', JSON.stringify(status.data, null, 2));
      
      if (status.data.resultCode === 200) {
        console.log('\n✅ 装配成功');
        
        // 验证
        const cameraInfo = await callAPI('/GetModelInfo', { id: child.modelId, useModeId: true });
        console.log('\n相机父节点:', cameraInfo.data?.parentName || 'null');
      } else {
        console.log('\n❌ 装配失败:', status.data.resultMsg);
      }
      
    } else {
      console.log('\n❌ 装配失败:', assembleResult.msg);
    }
    
  } catch (error) {
    console.log('\n❌ 测试异常:', error.message);
    console.log(error.stack);
  }
}

testAssembleWithCreate().catch(console.error);
