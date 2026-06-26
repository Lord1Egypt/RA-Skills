#!/usr/bin/env node

/**
 * 使用 createModel 创建夹具（而不是 download）
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

async function createGripper() {
  console.log('📦 使用 createModel 创建夹具（从本地模型库）\n');
  
  // 使用 createModel 并设置 checkFromCloud: false 从本地创建
  console.log('创建 DH_PGS_5_5...');
  const result = await callAPI('/model/create', {
    id: 'DH_PGS_5_5',
    rename: '测试_夹具_PGS',
    position: [0, 0, 0],
    eulerAngle: [0, 0, 0],
    checkFromCloud: false  // 从本地模型库创建
  });
  
  console.log('响应:', JSON.stringify(result, null, 2));
  
  if (result.data?.taskId) {
    console.log('\n⏳ 等待创建完成...');
    
    for (let i = 0; i < 15; i++) {
      await sleep(2000);
      
      const status = await callAPI('/task/query', { taskId: result.data.taskId });
      console.log(`[${(i+1)*2}s] ${status.data.status}`);
      
      if (status.data.done) {
        console.log('\n最终状态:');
        console.log('  - resultCode:', status.data.resultCode);
        console.log('  - resultMsg:', status.data.resultMsg);
        console.log('  - resultData:', JSON.stringify(status.data.resultData, null, 2));
        
        if (status.data.resultCode === 200) {
          const modelId = await getModelIdByName('测试_夹具_PGS');
          console.log('\n✅ Model ID:', modelId);
          
          // 配置行为
          console.log('\n\n🔧 配置行为动作...');
          const behaviorResult = await callAPI('/behavior/add', {
            id: modelId,
            useModeId: true,
            behavioralType: 2,  // ROTATION
            referenceAxis: 2,   // Z axis
            minValue: -90,
            maxValue: 90,
            runSpeed: 90,
            runState: 0
          });
          
          console.log('行为配置响应:', JSON.stringify(behaviorResult, null, 2));
          
          if (behaviorResult.code === 200) {
            console.log('\n✅ 行为配置成功!');
            
            // 验证
            const behaviorInfo = await callAPI('/behavior/get', {
              id: modelId,
              useModeId: true
            });
            
            console.log('\n行为信息:');
            console.log(JSON.stringify(behaviorInfo.data, null, 2));
          }
        }
        break;
      }
    }
  }
}

createGripper().catch(console.error);
