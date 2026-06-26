#!/usr/bin/env node

/**
 * 调试夹具下载 - 查看详细状态
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

async function testGripperDownload() {
  console.log('🔍 调试夹具下载\n');
  
  // 1. 下载 DH_RGD_5_14
  console.log('📥 下载 DH_RGD_5_14...');
  const result = await callAPI('/model/download', {
    id: 'DH_RGD_5_14',
    createInScene: true,
    position: [0, 0, 0],
    rename: '测试_夹具_RGD'
  });
  
  console.log('初始响应:', JSON.stringify(result, null, 2));
  
  if (result.data?.taskId) {
    console.log('\n⏳ 轮询任务状态（每 2 秒，最多 30 秒）...\n');
    
    for (let i = 0; i < 15; i++) {
      await sleep(2000);
      
      const status = await callAPI('/task/query', { taskId: result.data.taskId });
      console.log(`轮询 ${i+1}: ${status.data.status}`);
      
      if (status.data.done) {
        console.log('\n最终状态:');
        console.log('  - resultCode:', status.data.resultCode);
        console.log('  - resultMsg:', status.data.resultMsg);
        console.log('  - resultData:', JSON.stringify(status.data.resultData, null, 2));
        break;
      }
    }
  }
  
  // 2. 查看场景中的模型
  console.log('\n\n🔍 场景中的模型:');
  const allInfo = await callAPI('/GetAllModelInfo', {});
  const models = allInfo.data?.models || [];
  
  models.forEach((m, i) => {
    console.log(`   ${i+1}. ${m.modelName} (${m.modelId})`);
  });
}

testGripperDownload().catch(console.error);
