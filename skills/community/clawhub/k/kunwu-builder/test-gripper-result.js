#!/usr/bin/env node

/**
 * 检查夹具下载结果
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

async function checkResult() {
  console.log('🔍 检查夹具下载结果\n');
  
  const allInfo = await callAPI('/GetAllModelInfo', {});
  const models = allInfo.data?.models || [];
  
  // 查找夹具
  const gripperKeywords = ['DH_', 'Gripper', '夹具', 'RGD', 'PGE', 'PGS', 'PGI', 'Mechanical', '测试_'];
  const grippers = models.filter(m => 
    gripperKeywords.some(k => m.modelName?.includes(k))
  );
  
  console.log(`场景中共有 ${models.length} 个模型`);
  console.log(`找到 ${grippers.length} 个夹具/测试模型:\n`);
  
  grippers.forEach((g, i) => {
    console.log(`${i+1}. ${g.modelName}`);
    console.log(`   ID: ${g.modelId}`);
    console.log();
  });
  
  // 检查是否有测试_夹具_PGS
  const testGripper = grippers.find(m => m.modelName === '测试_夹具_PGS');
  
  if (testGripper) {
    console.log('✅ 测试夹具下载成功!\n');
    
    // 获取详细信息
    const modelInfo = await callAPI('/GetModelInfo', { id: testGripper.modelId, useModeId: true });
    console.log('模型详情:');
    console.log('  - modelName:', modelInfo.data?.modelName);
    console.log('  - type:', modelInfo.data?.type || 'N/A');
    console.log('  - boundSize:', JSON.stringify(modelInfo.data?.boundSize));
    
    // 配置行为
    console.log('\n\n🔧 配置行为动作...');
    
    const behaviorResult = await callAPI('/behavior/add', {
      id: testGripper.modelId,
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
      console.log('\n✅ 行为配置成功!\n');
      
      // 验证行为
      const behaviorInfo = await callAPI('/behavior/get', {
        id: testGripper.modelId,
        useModeId: true
      });
      
      console.log('行为信息:', JSON.stringify(behaviorInfo.data, null, 2));
    }
  } else {
    console.log('❌ 测试夹具未找到');
  }
}

checkResult().catch(console.error);
