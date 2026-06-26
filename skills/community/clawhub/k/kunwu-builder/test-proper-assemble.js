#!/usr/bin/env node

/**
 * 正确的装配测试 - 使用本地模型库中的真实模型
 * 日期：2026-03-16
 * 
 * 使用真实模型：
 * - Camera Bracket（相机支架）- 本地模型库
 * - Dufault 2D（2D 相机）- 本地模型库
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
  console.log(`📥 下载 ${modelName}...`);
  
  const result = await callAPI('/model/download', {
    id: modelName,
    createInScene: true,
    position: position || [0, 0, 0],
    rename: rename
  });
  
  console.log(`   响应：${result.code} ${result.msg}`);
  
  if (result.data?.taskId) {
    // 轮询等待完成
    for (let i = 0; i < 15; i++) {
      await sleep(1000);
      const status = await callAPI('/task/query', { taskId: result.data.taskId });
      
      if (status.data.done) {
        console.log(`   状态：${status.data.status} (${status.data.resultMsg})`);
        
        if (status.data.resultCode === 200) {
          const modelId = await getModelIdByName(rename);
          console.log(`   ✅ 完成，modelId: ${modelId}`);
          return modelId;
        } else {
          throw new Error(`Download failed: ${status.data.resultMsg}`);
        }
      }
    }
    throw new Error('Download timeout');
  }
  
  throw new Error('No taskId returned');
}

async function testProperAssemble() {
  console.log('🧪 正确的装配测试 - 使用本地模型库中的真实模型\n');
  console.log('模型：Camera Bracket + Dufault 2D\n');
  
  try {
    // 1. 清理
    console.log('🧹 清理场景...');
    const allInfo0 = await callAPI('/GetAllModelInfo', {});
    const testModels = (allInfo0.data?.models || []).filter(m => 
      m.modelName?.includes('测试_') || 
      m.modelName?.includes('2D 相机') ||
      m.modelName?.includes('相机支架') ||
      m.modelName?.includes('Camera') ||
      m.modelName?.includes('Bracket')
    );
    if (testModels.length > 0) {
      const ids = testModels.map(m => m.modelId || m.id);
      await callAPI('/model/destroy', { ids });
      await sleep(2000);
      console.log(`   清理了 ${testModels.length} 个模型`);
    }
    console.log();
    
    // 2. 下载 Camera Bracket（相机支架）
    console.log('=' .repeat(50));
    const bracketId = await downloadAndWait(
      'Camera Bracket',
      '测试_相机支架',
      [0, 0, 0]
    );
    console.log();
    
    // 3. 下载 Dufault 2D（2D 相机）
    console.log('=' .repeat(50));
    const cameraId = await downloadAndWait(
      'Dufault 2D',
      '测试_2D 相机',
      [0, 0, 150]
    );
    console.log();
    
    // 4. 查看模型信息
    console.log('=' .repeat(50));
    console.log('🔍 查看模型信息...');
    
    const bracketInfo = await callAPI('/GetModelInfo', { id: bracketId, useModeId: true });
    const cameraInfo = await callAPI('/GetModelInfo', { id: cameraId, useModeId: true });
    
    console.log('\n相机支架:');
    console.log(`  - modelName: ${bracketInfo.data?.modelName}`);
    console.log(`  - type: ${bracketInfo.data?.type || 'N/A'}`);
    
    console.log('\n2D 相机:');
    console.log(`  - modelName: ${cameraInfo.data?.modelName}`);
    console.log(`  - type: ${cameraInfo.data?.type || 'N/A'}`);
    console.log();
    
    // 5. 执行装配
    console.log('=' .repeat(50));
    console.log('🔧 执行装配：2D 相机 -> 相机支架（使用 /model/assemble）');
    console.log(`   childId: ${cameraId}`);
    console.log(`   parentId: ${bracketId}`);
    console.log();
    
    const assembleResult = await callAPI('/model/assemble', {
      childId: cameraId,
      parentId: bracketId,
      childUseModeId: true,
      parentUseModeId: true,
      assemblePosIndex: -1,
      replaceExisting: true
    });
    
    console.log('📊 装配响应:', JSON.stringify(assembleResult, null, 2));
    console.log();
    
    if (assembleResult.code === 200) {
      console.log('✅ 装配成功（同步）');
      
      // 验证
      const cameraInfoAfter = await callAPI('/GetModelInfo', { id: cameraId, useModeId: true });
      console.log('\n🔍 验证结果:');
      console.log(`   - parentId: ${cameraInfoAfter.data?.parentId || 'null'}`);
      console.log(`   - parentName: ${cameraInfoAfter.data?.parentName || 'null'}`);
      
      if (cameraInfoAfter.data?.parentId || cameraInfoAfter.data?.parentName) {
        console.log('\n✅ 父子关系建立成功！');
      }
      
    } else if (assembleResult.code === 202) {
      console.log('⏳ 异步任务，等待完成...');
      await sleep(2000);
      
      const status = await callAPI('/task/query', { taskId: assembleResult.data.taskId });
      console.log('任务状态:', JSON.stringify(status.data, null, 2));
      
      if (status.data.resultCode === 200) {
        console.log('\n✅ 装配成功');
        
        // 验证
        const cameraInfoAfter = await callAPI('/GetModelInfo', { id: cameraId, useModeId: true });
        console.log('\n🔍 验证结果:');
        console.log(`   - parentId: ${cameraInfoAfter.data?.parentId || 'null'}`);
        console.log(`   - parentName: ${cameraInfoAfter.data?.parentName || 'null'}`);
        
        if (cameraInfoAfter.data?.parentId || cameraInfoAfter.data?.parentName) {
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

testProperAssemble().catch(console.error);
