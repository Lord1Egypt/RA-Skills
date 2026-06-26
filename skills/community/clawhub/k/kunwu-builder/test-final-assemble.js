#!/usr/bin/env node

/**
 * 最终装配测试 - 使用场景中已有的 2D 相机和新创建的支架
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

async function testFinalAssemble() {
  console.log('🧪 最终装配测试 - 使用场景中已有的 2D 相机\n');
  
  try {
    // 1. 查看场景中的模型
    console.log('🔍 场景中的模型:');
    const allInfo = await callAPI('/GetAllModelInfo', {});
    const models = allInfo.data?.models || [];
    models.forEach((m, i) => {
      console.log(`   ${i+1}. ${m.modelName} (${m.modelId})`);
    });
    
    // 2. 找到 2D 相机
    const camera = models.find(m => m.modelName === '2D 相机_001');
    if (!camera) {
      console.log('\n❌ 未找到 2D 相机');
      return;
    }
    console.log(`\n✅ 找到 2D 相机：${camera.modelId}`);
    
    // 3. 创建支架（使用方形）
    console.log('\n📦 创建支架...');
    const bracketResult = await callAPI('/model/create', {
      id: '方形',
      rename: '测试_支架',
      position: [0, 0, 0],
      parameterizationCfg: {
        length: 100,
        width: 100,
        height: 20
      },
      checkFromCloud: false
    });
    
    console.log('创建响应:', JSON.stringify(bracketResult, null, 2));
    
    if (bracketResult.data?.taskId) {
      await sleep(2000);
      const status = await callAPI('/task/query', { taskId: bracketResult.data.taskId });
      console.log('支架创建状态:', status.data.status);
    }
    
    await sleep(500);
    
    // 4. 获取支架 ID
    const allInfo2 = await callAPI('/GetAllModelInfo', {});
    const models2 = allInfo2.data?.models || [];
    const bracket = models2.find(m => m.modelName === '测试_支架');
    
    if (!bracket) {
      console.log('❌ 未找到支架');
      return;
    }
    console.log(`✅ 支架：${bracket.modelId}`);
    
    // 5. 执行装配
    console.log('\n🔧 执行装配：2D 相机 -> 支架（使用 /model/assemble）');
    console.log(`   childId: ${camera.modelId}`);
    console.log(`   parentId: ${bracket.modelId}`);
    
    const assembleResult = await callAPI('/model/assemble', {
      childId: camera.modelId,
      parentId: bracket.modelId,
      childUseModeId: true,
      parentUseModeId: true,
      assemblePosIndex: -1,
      replaceExisting: true
    });
    
    console.log('\n📊 装配响应:', JSON.stringify(assembleResult, null, 2));
    
    if (assembleResult.code === 200) {
      console.log('\n✅ 装配成功（同步）');
      
      // 验证
      const cameraInfo = await callAPI('/GetModelInfo', { id: camera.modelId, useModeId: true });
      console.log('\n🔍 验证结果:');
      console.log(`   - parentId: ${cameraInfo.data?.parentId || 'null'}`);
      console.log(`   - parentName: ${cameraInfo.data?.parentName || 'null'}`);
      
      if (cameraInfo.data?.parentId || cameraInfo.data?.parentName) {
        console.log('\n✅ 父子关系建立成功！');
      } else {
        console.log('\n⚠️ 未检测到父子关系');
      }
      
    } else if (assembleResult.code === 202) {
      console.log('\n⏳ 异步任务，等待完成...');
      await sleep(2000);
      const status = await callAPI('/task/query', { taskId: assembleResult.data.taskId });
      console.log('任务状态:', JSON.stringify(status.data, null, 2));
      
      if (status.data.resultCode === 200) {
        console.log('\n✅ 装配成功');
        
        // 验证
        const cameraInfo = await callAPI('/GetModelInfo', { id: camera.modelId, useModeId: true });
        console.log('\n🔍 验证结果:');
        console.log(`   - parentId: ${cameraInfo.data?.parentId || 'null'}`);
        console.log(`   - parentName: ${cameraInfo.data?.parentName || 'null'}`);
        
        if (cameraInfo.data?.parentId || cameraInfo.data?.parentName) {
          console.log('\n✅ 父子关系建立成功！');
        }
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

testFinalAssemble().catch(console.error);
