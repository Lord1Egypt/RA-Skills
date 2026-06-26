#!/usr/bin/env node

/**
 * 调试下载 API - 查看详细错误
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
        console.log(`\nHTTP ${res.statusCode} 响应:`);
        console.log(responseData);
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

async function testDownload() {
  console.log('📥 调试下载 API\n');
  
  // 测试 1: 下载 Camera Bracket
  console.log('测试 1: 下载 Camera Bracket');
  const result1 = await callAPI('/model/download', {
    id: 'Camera Bracket',
    createInScene: true,
    position: [0, 0, 0],
    rename: '相机支架_001'
  });
  
  console.log('\n初始响应:', JSON.stringify(result1, null, 2));
  
  if (result1.data?.taskId) {
    console.log('\n⏳ 轮询任务状态...');
    await sleep(2000);
    
    const status = await callAPI('/task/query', { taskId: result1.data.taskId });
    console.log('\n任务状态:', JSON.stringify(status, null, 2));
    
    if (status.data?.resultCode === 400) {
      console.log('\n❌ 失败原因:', status.data.resultMsg);
      console.log('resultData:', JSON.stringify(status.data.resultData, null, 2));
    }
  }
  
  // 测试 2: 下载 Dufault 2D
  console.log('\n\n========================================\n');
  console.log('测试 2: 下载 Dufault 2D');
  const result2 = await callAPI('/model/download', {
    id: 'Dufault 2D',
    createInScene: true,
    position: [0, 0, 100],
    rename: '2D 相机_001'
  });
  
  console.log('\n初始响应:', JSON.stringify(result2, null, 2));
  
  if (result2.data?.taskId) {
    console.log('\n⏳ 轮询任务状态...');
    await sleep(2000);
    
    const status = await callAPI('/task/query', { taskId: result2.data.taskId });
    console.log('\n任务状态:', JSON.stringify(status, null, 2));
  }
}

testDownload().catch(console.error);
