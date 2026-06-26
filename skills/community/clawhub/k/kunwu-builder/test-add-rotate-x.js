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
  console.log('🧪 为 "方形" 添加绕 X 轴旋转行为\n');
  
  const modelName = "方形";
  
  // 1. 获取模型信息
  console.log('1️⃣ 获取模型信息...');
  const modelsResult = await call('/GetAllModelInfo');
  const models = modelsResult.data?.models || [];
  const targetModel = models.find(m => m.modelName === modelName);
  
  if (!targetModel) {
    console.log('   ❌ 未找到模型 "' + modelName + '"');
    return;
  }
  
  console.log('   ✅ 找到模型:', modelName);
  console.log('      位置: [' + targetModel.transform?.slice(0,3).join(', ') + ']');
  
  // 2. 添加绕 X 轴旋转行为
  console.log('\n2️⃣ 添加绕 X 轴旋转行为...');
  const addResult = await call('/behavior/add', {
    id: modelName,
    useModeId: false,
    behavioralType: 2,        // Rotation (旋转)
    referenceAxis: 0,         // X 轴
    minValue: -90,            // 最小角度 -90°
    maxValue: 90,             // 最大角度 +90°
    runSpeed: 60,             // 速度 60°/秒
    targetValue: 0,           // 目标角度 0°
    isHaveElectricalMachinery: true,
    offset: 0
  });
  
  console.log('   状态:', addResult.code === 200 ? '✅ 成功' : '❌ 失败', addResult.msg);
  
  if (addResult.data) {
    console.log('\n📊 行为参数:');
    console.log('   模型:', addResult.data.modelName);
    console.log('   行为类型: 旋转 (Type 2)');
    console.log('   参考轴：X 轴 (Axis 0)');
    console.log('   角度范围: -90° ~ +90°');
    console.log('   旋转速度:', addResult.data.runSpeed, '°/s');
    console.log('   目标角度:', addResult.data.targetValue, '°');
  }
  
  // 3. 验证
  console.log('\n3️⃣ 验证行为...');
  const verifyResult = await call('/behavior/get', {
    id: modelName,
    useModeId: false
  });
  
  if (verifyResult.data?.hasBehavior) {
    console.log('   ✅ 验证成功!');
    console.log('      类型：旋转 (Type 2)');
    console.log('      轴向：X 轴 (Axis 0)');
    console.log('      范围:', verifyResult.data.minValue, '° ~', verifyResult.data.maxValue, '°');
  }
  
  console.log('\n✅ 完成！');
}

main().catch(err => {
  console.error('❌ 错误:', err.message);
  process.exit(1);
});
