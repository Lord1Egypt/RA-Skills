#!/usr/bin/env node

import http from 'http';

const HOST = process.env.KUNWU_HOST || '192.168.176.1';
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
  console.log('🔍 测试 Kunwu Builder API (host: ' + HOST + ')\n');
  
  // 测试 1: 获取所有模型
  console.log('1️⃣ 获取所有模型...');
  let result = await call('/GetAllModelInfo');
  console.log('   模型数量:', result.data?.models?.length || 0);
  
  // 测试 2: 获取层级树
  console.log('\n2️⃣ 获取层级树...');
  result = await call('/models/tree', { rootId: 'scene', useModeId: true, includeRoot: true });
  console.log('   根节点:', result.data?.rootId);
  
  // 测试 3: 获取场景 JSON
  console.log('\n3️⃣ 获取场景 JSON...');
  result = await call('/scene/get_scene_json');
  console.log('   场景数据长度:', result.data?.sceneJson?.length || 0);
  
  // 测试 4: 查询机器人 ID (如果有机器人)
  console.log('\n4️⃣ 查询机器人 ID...');
  result = await call('/query/robot_id', {});
  console.log('   机器人 ID:', result.data || '无机器人');
  
  console.log('\n✅ 所有测试完成!');
}

main().catch(err => {
  console.error('❌ 错误:', err.message);
  process.exit(1);
});
