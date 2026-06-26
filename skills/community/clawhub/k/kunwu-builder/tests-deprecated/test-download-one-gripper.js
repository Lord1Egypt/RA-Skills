#!/usr/bin/env node

/**
 * 下载单个夹具（延长等待时间）
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

async function downloadOneGripper() {
  console.log('📥 下载 DH_PGS_5_5（小型夹具，应该较快）\n');
  
  const result = await callAPI('/model/download', {
    id: 'DH_PGS_5_5',
    createInScene: true,
    position: [0, 0, 0],
    rename: '测试_夹具_PGS'
  });
  
  console.log('初始响应:', JSON.stringify(result, null, 2));
  
  if (result.data?.taskId) {
    console.log('\n⏳ 长时间轮询（每 5 秒，最多 2 分钟）...\n');
    
    for (let i = 0; i < 24; i++) {
      await sleep(5000);
      
      const status = await callAPI('/task/query', { taskId: result.data.taskId });
      
      if (status.data.done || i % 3 === 0) {
        console.log(`[${(i+1)*5}s] ${status.data.status}`);
      }
      
      if (status.data.done) {
        console.log('\n✅ 任务完成!');
        console.log('  - resultCode:', status.data.resultCode);
        console.log('  - resultMsg:', status.data.resultMsg);
        console.log('  - resultData:', JSON.stringify(status.data.resultData, null, 2));
        
        if (status.data.resultCode === 200) {
          const modelId = await getModelIdByName('测试_夹具_PGS');
          console.log('\n✅ Model ID:', modelId);
          
          // 获取模型详情
          const modelInfo = await callAPI('/GetModelInfo', { id: modelId, useModeId: true });
          console.log('\n模型信息:');
          console.log('  - modelName:', modelInfo.data?.modelName);
          console.log('  - type:', modelInfo.data?.type || 'N/A');
          console.log('  - boundSize:', JSON.stringify(modelInfo.data?.boundSize));
        }
        break;
      }
    }
  }
  
  // 查看场景
  console.log('\n\n🔍 场景中的模型:');
  const allInfo = await callAPI('/GetAllModelInfo', {});
  const models = allInfo.data?.models || [];
  models.forEach((m, i) => {
    console.log(`   ${i+1}. ${m.modelName} (${m.modelId})`);
  });
}

downloadOneGripper().catch(console.error);
