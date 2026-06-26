#!/usr/bin/env node

/**
 * 使用 relativePath 下载模型
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

async function testDownloadWithPath() {
  console.log('📥 使用 relativePath 下载模型\n');
  
  // 1. 先获取本地模型库，查看正确的路径
  console.log('🔍 获取本地模型库...');
  const localResult = await callAPI('/model/library/local', {});
  const models = localResult.data?.models || [];
  
  const bracket = models.find(m => m.modelName === 'Camera Bracket');
  const camera = models.find(m => m.modelName === 'Dufault 2D');
  
  console.log('\nCamera Bracket:');
  console.log(`  - modelName: ${bracket?.modelName}`);
  console.log(`  - nameExt: ${bracket?.nameExt}`);
  console.log(`  - relativePath: ${bracket?.relativePath}`);
  
  console.log('\nDufault 2D:');
  console.log(`  - modelName: ${camera?.modelName}`);
  console.log(`  - nameExt: ${camera?.nameExt}`);
  console.log(`  - relativePath: ${camera?.relativePath}`);
  
  // 2. 尝试使用不同的参数下载
  console.log('\n' + '='.repeat(50));
  console.log('测试 1: 使用 id="Camera Bracket"');
  const r1 = await callAPI('/model/download', {
    id: 'Camera Bracket',
    createInScene: true,
    position: [0, 0, 0],
    rename: '支架_测试 1'
  });
  console.log('响应:', r1.code, r1.msg);
  if (r1.data?.taskId) {
    await sleep(2000);
    const status = await callAPI('/task/query', { taskId: r1.data.taskId });
    console.log('状态:', status.data.status, status.data.resultMsg);
  }
  
  console.log('\n' + '='.repeat(50));
  console.log('测试 2: 使用 relativePath');
  const r2 = await callAPI('/model/download', {
    relativePath: 'CloudModel/Camera/Camera Bracket/Camera Bracket.rtprefab',
    createInScene: true,
    position: [0, 0, 50],
    rename: '支架_测试 2'
  });
  console.log('响应:', r2.code, r2.msg);
  if (r2.data?.taskId) {
    await sleep(2000);
    const status = await callAPI('/task/query', { taskId: r2.data.taskId });
    console.log('状态:', status.data.status, status.data.resultMsg);
  }
  
  console.log('\n' + '='.repeat(50));
  console.log('测试 3: 使用 nameExt');
  const r3 = await callAPI('/model/download', {
    nameExt: 'Camera Bracket.rtprefab',
    createInScene: true,
    position: [0, 0, 100],
    rename: '支架_测试 3'
  });
  console.log('响应:', r3.code, r3.msg);
  if (r3.data?.taskId) {
    await sleep(2000);
    const status = await callAPI('/task/query', { taskId: r3.data.taskId });
    console.log('状态:', status.data.status, status.data.resultMsg);
  }
  
  console.log('\n' + '='.repeat(50));
  console.log('测试 4: Dufault 2D (已知可用)');
  const r4 = await callAPI('/model/download', {
    id: 'Dufault 2D',
    createInScene: true,
    position: [0, 0, 150],
    rename: '相机_测试 4'
  });
  console.log('响应:', r4.code, r4.msg);
  if (r4.data?.taskId) {
    await sleep(2000);
    const status = await callAPI('/task/query', { taskId: r4.data.taskId });
    console.log('状态:', status.data.status, status.data.resultMsg);
  }
}

testDownloadWithPath().catch(console.error);
