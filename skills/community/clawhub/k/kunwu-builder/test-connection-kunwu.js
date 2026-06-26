#!/usr/bin/env node

/**
 * Kunwu Builder 连接测试
 */

import http from 'http';

async function testConnection() {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: '127.0.0.1',
      port: 16888,
      path: '/GetAllModelInfo',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          resolve(result);
        } catch (e) {
          reject(new Error('Parse error: ' + e.message));
        }
      });
    });

    req.on('error', (e) => {
      reject(new Error('Connection failed: ' + e.message));
    });

    req.write(JSON.stringify({}));
    req.end();
  });
}

console.log('🔍 测试 Kunwu Builder 连接...\n');

try {
  const result = await testConnection();
  console.log('✅ 连接成功！');
  console.log('\n响应:', JSON.stringify(result, null, 2));
  
  if (result.data?.models) {
    console.log(`\n📦 场景中有 ${result.data.models.length} 个模型`);
    result.data.models.forEach((m, i) => {
      console.log(`  ${i + 1}. ${m.modelName} (${m.modelType})`);
    });
  }
} catch (error) {
  console.log('❌ 连接失败');
  console.log('\n错误:', error.message);
  console.log('\n请检查:');
  console.log('  1. Kunwu Builder 是否正在运行');
  console.log('  2. 端口是否为 16888（菜单栏 - 编辑 - 偏好设置）');
  console.log('  3. 防火墙是否阻止了本地连接');
  process.exit(1);
}
