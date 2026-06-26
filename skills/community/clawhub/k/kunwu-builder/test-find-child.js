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

// 递归打印层级树
function printTree(models, indent = 0) {
  let found = [];
  for (const model of models) {
    const prefix = '  '.repeat(indent);
    console.log(`${prefix}- ${model.modelName} (type: ${model.modelType})`);
    found.push(model.modelName);
    if (model.children && model.children.length > 0) {
      found = found.concat(printTree(model.children, indent + 1));
    }
  }
  return found;
}

async function main() {
  console.log('🔍 搜索层级树查找 "方形 rot-x"\n');
  
  // 获取完整层级树
  console.log('📊 场景层级结构:\n');
  const treeResult = await call('/models/tree', {
    rootId: 'scene',
    useModeId: true,
    includeRoot: false
  });
  
  if (treeResult.data?.models) {
    const allModels = printTree(treeResult.data.models);
    
    console.log('\n📋 所有模型名称:');
    allModels.forEach(name => console.log('   - ' + name));
    
    // 查找目标
    const targetName = "方形 rot-x";
    const found = allModels.find(name => name.includes(targetName) || name === targetName);
    
    if (found) {
      console.log('\n✅ 找到目标:', found);
    } else {
      console.log('\n❌ 未找到 "方形 rot-x"');
      console.log('   可能的名称:');
      allModels.filter(n => n.includes('方形') || n.includes('rot')).forEach(n => {
        console.log('      - ' + n);
      });
    }
  }
}

main().catch(err => {
  console.error('❌ 错误:', err.message);
  process.exit(1);
});
