#!/usr/bin/env node

import http from 'http';

const HOST = '192.168.176.1';
const PORT = 16888;

async function call(endpoint, data = {}) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify(data);
    const req = http.request({
      hostname: HOST,
      port: PORT,
      path: endpoint,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body),
      },
    }, (res) => {
      let responseData = '';
      res.on('data', chunk => responseData += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(responseData));
        } catch (e) {
          reject(new Error('Parse error: ' + e.message));
        }
      });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

async function main() {
  console.log('🧪 测试创建模型功能\n');
  
  // 测试创建模型
  console.log('📦 创建测试模型 "纸箱_01"...');
  const result = await call('/model/create', {
    id: "纸箱",
    rename: "纸箱_01",
    position: [100, 200, 0],
    eulerAngle: [0, 0, 0]
  });
  console.log('   结果:', result.code === 200 ? '✅ 成功' : '❌ 失败', result.msg);
  
  // 验证模型已创建
  console.log('\n🔍 验证模型列表...');
  const models = await call('/GetAllModelInfo');
  console.log('   当前模型数量:', models.data?.models?.length || 0);
  if (models.data?.models?.length > 0) {
    models.data.models.forEach((m, i) => {
      console.log(`   ${i + 1}. ${m.modelName} - 位置：[${m.transform?.slice(0,3).join(', ')}]`);
    });
  }
  
  console.log('\n✅ 测试完成!');
}

main().catch(err => {
  console.error('❌ 错误:', err.message);
  process.exit(1);
});
