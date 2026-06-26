#!/usr/bin/env node

/**
 * 检查场景中是否已有夹具
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

async function checkGrippers() {
  console.log('🔍 检查场景中的夹具\n');
  
  const allInfo = await callAPI('/GetAllModelInfo', {});
  const models = allInfo.data?.models || [];
  
  console.log(`场景中共有 ${models.length} 个模型:\n`);
  
  // 查找夹具
  const gripperKeywords = ['DH_', 'Gripper', '夹具', 'RGD', 'PGE', 'PGS', 'PGI', 'Mechanical'];
  const grippers = models.filter(m => 
    gripperKeywords.some(k => m.modelName?.includes(k))
  );
  
  if (grippers.length > 0) {
    console.log('📦 找到的夹具:\n');
    grippers.forEach((g, i) => {
      console.log(`${i+1}. ${g.modelName}`);
      console.log(`   ID: ${g.modelId}`);
      console.log(`   Type: ${g.type || 'N/A'}`);
      console.log();
    });
  } else {
    console.log('❌ 没有找到夹具');
  }
  
  // 列出所有模型
  console.log('\n📋 所有模型:\n');
  models.forEach((m, i) => {
    console.log(`${i+1}. ${m.modelName}`);
  });
  
  // 检查本地模型库
  console.log('\n\n🔍 本地模型库中的夹具:\n');
  const localResult = await callAPI('/model/library/local', {});
  const localModels = localResult.data?.models || [];
  
  const localGrippers = localModels.filter(m => 
    gripperKeywords.some(k => m.modelName?.includes(k))
  );
  
  localGrippers.forEach((m, i) => {
    console.log(`${i+1}. ${m.modelName}`);
    console.log(`   路径：${m.relativePath}`);
    console.log();
  });
}

checkGrippers().catch(console.error);
