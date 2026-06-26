#!/usr/bin/env node

/**
 * Camera Bracket 下载失败的变通方案
 * 使用 Cube 或其他模型代替支架进行测试
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

async function testAssembleWithCube() {
  console.log('🧪 使用 Cube 作为支架进行装配测试\n');
  
  try {
    // 1. 下载 Cube 作为"支架"
    console.log('📥 下载 Cube（作为支架）...');
    const cubeResult = await callAPI('/model/download', {
      id: 'Cube',
      createInScene: true,
      position: [0, 0, 0],
      rename: '支架_Cube'
    });
    
    if (cubeResult.data?.taskId) {
      await sleep(2000);
      const status = await callAPI('/task/query', { taskId: cubeResult.data.taskId });
      console.log('Cube 下载状态:', status.data.status);
      
      if (status.data.resultCode !== 200) {
        console.log('❌ Cube 下载失败:', status.data.resultMsg);
        return;
      }
    }
    
    // 2. 确认 2D 相机已存在
    console.log('\n🔍 检查 2D 相机...');
    const allInfo = await callAPI('/GetAllModelInfo', {});
    const models = allInfo.data?.models || [];
    const camera = models.find(m => m.modelName === '2D 相机_001');
    
    if (!camera) {
      console.log('❌ 2D 相机不存在，重新下载...');
      const cameraResult = await callAPI('/model/download', {
        id: 'Dufault 2D',
        createInScene: true,
        position: [0, 0, 100],
        rename: '2D 相机_001'
      });
      
      if (cameraResult.data?.taskId) {
        await sleep(2000);
        const status = await callAPI('/task/query', { taskId: cameraResult.data.taskId });
        console.log('相机下载状态:', status.data.status);
      }
    } else {
      console.log(`✅ 2D 相机已存在：${camera.modelId}`);
    }
    
    await sleep(1000);
    
    // 3. 获取模型 ID
    console.log('\n🔍 获取模型 ID...');
    const cubeId = await getModelIdByName('支架_Cube');
    const cameraId = await getModelIdByName('2D 相机_001');
    console.log(`   支架 (Cube): ${cubeId}`);
    console.log(`   相机：${cameraId}`);
    
    // 4. 执行装配
    console.log('\n🔧 执行装配：相机 -> 支架（使用 /model/assemble）');
    const assembleResult = await callAPI('/model/assemble', {
      childId: cameraId,
      parentId: cubeId,
      childUseModeId: true,
      parentUseModeId: true,
      assemblePosIndex: -1,
      replaceExisting: true
    });
    
    console.log('\n装配响应:', JSON.stringify(assembleResult, null, 2));
    
    if (assembleResult.code === 200) {
      console.log('\n✅ 装配成功（同步）');
      
      // 验证
      const cameraInfo = await callAPI('/GetModelInfo', { id: cameraId, useModeId: true });
      console.log('\n相机父节点:', cameraInfo.data?.parentName || 'null');
      
    } else if (assembleResult.code === 202) {
      console.log('\n⏳ 等待异步任务...');
      await sleep(2000);
      const status = await callAPI('/task/query', { taskId: assembleResult.data.taskId });
      console.log('任务状态:', JSON.stringify(status.data, null, 2));
      
      if (status.data.resultCode === 200) {
        console.log('\n✅ 装配成功');
        
        // 验证
        const cameraInfo = await callAPI('/GetModelInfo', { id: cameraId, useModeId: true });
        console.log('\n相机父节点:', cameraInfo.data?.parentName || 'null');
      }
      
    } else {
      console.log('\n❌ 装配失败:', assembleResult.msg);
    }
    
  } catch (error) {
    console.log('\n❌ 测试异常:', error.message);
  }
}

testAssembleWithCube().catch(console.error);
