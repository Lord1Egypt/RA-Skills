#!/usr/bin/env node

/**
 * 检查所有未完成的任务
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

async function checkTasks() {
  console.log('🔍 检查下载任务状态\n');
  
  // 之前的任务 ID
  const taskIds = [
    'task_1773627594243_8',  // DH_PGS_5_5
    'task_1773627487027_7'   // DH_RGD_5_14
  ];
  
  for (const taskId of taskIds) {
    console.log(`任务：${taskId}`);
    const status = await callAPI('/task/query', { taskId });
    console.log('状态:', JSON.stringify(status.data, null, 2));
    console.log();
  }
  
  // 查看场景中是否有 DH_ 开头的模型
  console.log('🔍 场景中是否有 DH_ 模型?');
  const allInfo = await callAPI('/GetAllModelInfo', {});
  const models = allInfo.data?.models || [];
  
  const dhModels = models.filter(m => m.modelName?.startsWith('DH_'));
  console.log(`找到 ${dhModels.length} 个 DH_ 模型`);
  
  if (dhModels.length > 0) {
    dhModels.forEach(m => {
      console.log(`  - ${m.modelName} (${m.modelId})`);
    });
  }
}

checkTasks().catch(console.error);
