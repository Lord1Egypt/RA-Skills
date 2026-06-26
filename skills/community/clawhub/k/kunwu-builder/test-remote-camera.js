#!/usr/bin/env node

/**
 * 从远程模型库下载相机和支架
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

async function testRemote() {
  console.log('📥 从远程模型库下载相机支架\n');
  
  // 1. 搜索远程模型库
  console.log('🔍 搜索远程模型库：camera bracket...');
  const searchResult = await callAPI('/model/library/remote', {
    search: 'camera bracket',
    page: 1,
    pageSize: 10
  });
  
  const remoteModels = searchResult.data?.models || [];
  console.log(`找到 ${remoteModels.length} 个模型:\n`);
  
  remoteModels.forEach((m, i) => {
    console.log(`${i+1}. ${m.name}`);
    console.log(`   id: ${m.id}`);
    console.log(`   type: ${m.type || 'N/A'}`);
    console.log();
  });
  
  if (remoteModels.length > 0) {
    // 2. 下载第一个匹配的模型
    const model = remoteModels[0];
    console.log('=' .repeat(50));
    console.log(`📥 下载：${model.name}`);
    
    const downloadResult = await callAPI('/model/download', {
      id: model.id,
      createInScene: true,
      position: [0, 0, 0],
      rename: '测试_相机支架'
    });
    
    console.log('响应:', downloadResult.code, downloadResult.msg);
    
    if (downloadResult.data?.taskId) {
      console.log('⏳ 等待下载完成...');
      await sleep(5000);
      
      const status = await callAPI('/task/query', { taskId: downloadResult.data.taskId });
      console.log('状态:', status.data.status, status.data.resultMsg);
      console.log('resultData:', JSON.stringify(status.data.resultData, null, 2));
      
      if (status.data.resultCode === 200) {
        const modelId = await getModelIdByName('测试_相机支架');
        console.log(`✅ 下载成功，modelId: ${modelId}`);
        
        // 3. 查看模型信息
        const modelInfo = await callAPI('/GetModelInfo', { id: modelId, useModeId: true });
        console.log('\n模型信息:');
        console.log('  - type:', modelInfo.data?.type || 'N/A');
        console.log('  - modelName:', modelInfo.data?.modelName);
      }
    }
  }
}

testRemote().catch(console.error);
