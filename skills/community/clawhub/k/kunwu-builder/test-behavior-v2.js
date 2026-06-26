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
  console.log('🧪 测试行为动作功能 v2\n');
  
  const modelName = "纸箱_01";
  
  // 1. 添加平移行为（只使用枚举值）
  console.log('1️⃣ 添加行为：沿 X 轴平移...');
  const result1 = await call('/behavior/add', {
    id: modelName,
    useModeId: false,
    behavioralType: 1,    // Translation
    referenceAxis: 0,     // X
    minValue: -500,
    maxValue: 500,
    runSpeed: 100,
    targetValue: 0,
    isHaveElectricalMachinery: true
  });
  console.log('   状态:', result1.code === 200 ? '✅ 成功' : '⚠️ ' + result1.msg);
  
  // 2. 添加旋转行为
  console.log('\n2️⃣ 添加行为：绕 Z 轴旋转...');
  const result2 = await call('/behavior/add', {
    id: modelName,
    useModeId: false,
    behavioralType: 2,    // Rotation
    referenceAxis: 2,     // Z
    minValue: -180,
    maxValue: 180,
    runSpeed: 90,
    targetValue: 45,
    isHaveElectricalMachinery: true
  });
  console.log('   状态:', result2.code === 200 ? '✅ 成功' : '⚠️ ' + result2.msg);
  
  // 3. 添加缩放行为
  console.log('\n3️⃣ 添加行为：缩放...');
  const result3 = await call('/behavior/add', {
    id: modelName,
    useModeId: false,
    behavioralType: 3,    // Scale
    referenceAxis: 3,     // Uniform
    minValue: 0.1,
    maxValue: 2.0,
    runSpeed: 0.5,
    targetValue: 1.0,
    isHaveElectricalMachinery: false
  });
  console.log('   状态:', result3.code === 200 ? '✅ 成功' : '⚠️ ' + result3.msg);
  
  // 4. 获取行为参数
  console.log('\n4️⃣ 获取模型行为参数...');
  const behaviorResult = await call('/behavior/get', {
    id: modelName,
    useModeId: false
  });
  
  if (behaviorResult.data?.hasBehavior) {
    console.log('   ✅ 模型有行为组件');
    console.log('   类型:', behaviorResult.data.behavioralType);
    console.log('   参考轴:', behaviorResult.data.referenceAxis);
    console.log('   范围:', behaviorResult.data.minValue, '~', behaviorResult.data.maxValue);
    console.log('   速度:', behaviorResult.data.runSpeed);
    console.log('   目标值:', behaviorResult.data.targetValue);
  } else {
    console.log('   ❌ 未找到行为组件');
  }
  
  // 5. 获取层级树查看行为
  console.log('\n5️⃣ 获取层级树...');
  const treeResult = await call('/models/tree', {
    rootId: 'scene',
    useModeId: true,
    includeRoot: false
  });
  
  if (treeResult.data?.models) {
    console.log('   场景模型:');
    treeResult.data.models.forEach(m => {
      console.log(`   - ${m.modelName} (type: ${m.modelType})`);
    });
  }
  
  console.log('\n✅ 测试完成!');
  console.log('\n💡 在 Kunwu Builder 中:');
  console.log('   1. 选中 "纸箱_01"');
  console.log('   2. 查看属性面板的行为组件');
  console.log('   3. 可以手动调整行为参数或播放动画');
}

main().catch(err => {
  console.error('❌ 错误:', err.message);
  process.exit(1);
});
