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
  console.log('🧪 测试新增 API 功能\n');
  
  // 1. 获取层级树（用于后续测试）
  console.log('1️⃣ 获取场景层级树...');
  const treeResult = await call('/models/tree', { rootId: 'scene', useModeId: true, includeRoot: false });
  console.log('   状态:', treeResult.code === 200 ? '✅' : '❌');
  if (treeResult.data?.models) {
    console.log('   模型:');
    treeResult.data.models.forEach(m => {
      console.log(`      - ${m.modelName}`);
      if (m.children?.length > 0) {
        m.children.forEach(c => console.log(`         └─ ${c.modelName}`));
      }
    });
  }
  
  // 2. 获取所有模型
  console.log('\n2️⃣ 获取所有模型...');
  const allModels = await call('/GetAllModelInfo');
  console.log('   状态:', allModels.code === 200 ? '✅' : '❌');
  console.log('   数量:', allModels.data?.models?.length || 0);
  
  // 3. 测试创建测试模型
  console.log('\n3️⃣ 创建测试模型...');
  const createResult = await call('/model/create', {
    id: '纸箱',
    rename: '测试_父',
    position: [0, 0, 0],
    eulerAngle: [0, 0, 0]
  });
  console.log('   状态:', createResult.code === 200 ? '✅' : '❌', createResult.msg);
  
  // 4. 创建子模型
  console.log('\n4️⃣ 创建子测试模型...');
  const createChild = await call('/model/create', {
    id: '纸箱',
    rename: '测试_子',
    position: [50, 0, 0],
    eulerAngle: [0, 0, 0]
  });
  console.log('   状态:', createChild.code === 200 ? '✅' : '❌', createChild.msg);
  
  // 5. 测试设置层级关系
  console.log('\n5️⃣ 设置层级关系（测试_子 → 测试_父）...');
  const parentResult = await call('/model/set_parent', {
    childId: '测试_子',
    parentId: '测试_父',
    useModeId: false
  });
  console.log('   状态:', parentResult.code === 200 ? '✅' : '❌', parentResult.msg);
  
  // 6. 获取本地模型库
  console.log('\n6️⃣ 获取本地模型库...');
  const localLib = await call('/model/library/local');
  console.log('   状态:', localLib.code === 200 ? '✅' : '❌', localLib.msg);
  if (localLib.data) {
    console.log('   数据:', JSON.stringify(localLib.data).substring(0, 100) + '...');
  }
  
  // 7. 获取远程模型库
  console.log('\n7️⃣ 获取远程模型库...');
  const remoteLib = await call('/model/library/remote', { page: 1, pageSize: 5 });
  console.log('   状态:', remoteLib.code === 200 ? '✅' : '❌', remoteLib.msg);
  if (remoteLib.data) {
    console.log('   数据:', JSON.stringify(remoteLib.data).substring(0, 100) + '...');
  }
  
  // 8. 获取模型分类
  console.log('\n8️⃣ 获取模型分类...');
  const categories = await call('/model/library/categories');
  console.log('   状态:', categories.code === 200 ? '✅' : '❌', categories.msg);
  
  // 9. 测试销毁子模型
  console.log('\n9️⃣ 销毁测试模型...');
  const destroyResult = await call('/model/destroy', {
    id: '测试_子',
    useModeId: false
  });
  console.log('   状态:', destroyResult.code === 200 ? '✅' : '❌', destroyResult.msg);
  
  // 10. 验证层级树
  console.log('\n🔟 验证最终层级树...');
  const finalTree = await call('/models/tree', { rootId: 'scene' });
  console.log('   状态:', finalTree.code === 200 ? '✅' : '❌');
  
  console.log('\n✅ 新 API 测试完成!');
  console.log('\n📝 提示:');
  console.log('   - 层级关系 API 需要场景中已有物体');
  console.log('   - 模型库 API 依赖软件配置的网络连接');
  console.log('   - 销毁操作不可恢复，请谨慎使用');
}

main().catch(err => {
  console.error('❌ 错误:', err.message);
  process.exit(1);
});
