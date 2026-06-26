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
  console.log('🧪 测试行为动作功能\n');
  
  // 1. 获取所有模型
  console.log('1️⃣ 获取场景中的模型...');
  const modelsResult = await call('/GetAllModelInfo');
  const models = modelsResult.data?.models || [];
  console.log('   模型数量:', models.length);
  models.forEach((m, i) => {
    console.log(`   ${i + 1}. ${m.modelName} (ID: ${m.modelId || 'N/A'})`);
  });
  
  if (models.length === 0) {
    console.log('   ⚠️  场景中没有模型，先创建一个...');
    await call('/model/create', {
      id: "纸箱",
      rename: "测试纸箱",
      position: [0, 0, 0],
      eulerAngle: [0, 0, 0]
    });
    console.log('   ✅ 已创建测试纸箱');
  }
  
  // 获取第一个模型
  const targetModel = models.length > 0 ? models[0] : { modelName: "测试纸箱" };
  const modelId = targetModel.modelName;
  console.log('\n2️⃣ 目标模型:', modelId);
  
  // 2. 先检查是否已有行为
  console.log('\n3️⃣ 检查现有行为...');
  const checkResult = await call('/behavior/get', { id: modelId, useModeId: false });
  if (checkResult.code === 200 && checkResult.data?.hasBehavior) {
    console.log('   ⚠️  已有行为组件:', checkResult.data);
  } else {
    console.log('   ℹ️  暂无行为组件');
  }
  
  // 3. 添加行为 - 沿 X 轴移动
  console.log('\n4️⃣ 添加行为：沿 X 轴平移...');
  const addResult = await call('/behavior/add', {
    id: modelId,
    useModeId: false,
    behavioralType: 1,        // 平移
    behavioralTypeName: "Translation",
    referenceAxis: 0,         // X 轴
    referenceAxisName: "X",
    minValue: -1000,
    maxValue: 1000,
    runSpeed: 100,
    targetValue: 0,
    isHaveElectricalMachinery: true,
    offset: 0
  });
  console.log('   结果:', addResult.code === 200 ? '✅ 成功' : '❌ 失败', addResult.msg);
  if (addResult.data) {
    console.log('   行为 ID:', addResult.data.modelId);
    console.log('   行为类型:', addResult.data.behavioralType);
    console.log('   参考轴:', addResult.data.referenceAxis);
  }
  
  // 4. 验证行为已添加
  console.log('\n5️⃣ 验证行为...');
  const verifyResult = await call('/behavior/get', { id: modelId, useModeId: false });
  if (verifyResult.data?.hasBehavior) {
    console.log('   ✅ 行为已添加!');
    console.log('   类型:', verifyResult.data.behavioralType);
    console.log('   参考轴:', verifyResult.data.referenceAxis);
    console.log('   范围:', verifyResult.data.minValue, '~', verifyResult.data.maxValue);
    console.log('   速度:', verifyResult.data.runSpeed);
  } else {
    console.log('   ❌ 验证失败');
  }
  
  // 5. 添加第二个行为 - 旋转
  console.log('\n6️⃣ 添加第二个行为：绕 Z 轴旋转...');
  const rotateResult = await call('/behavior/add', {
    id: modelId,
    useModeId: false,
    behavioralType: 2,        // 旋转
    behavioralTypeName: "Rotation",
    referenceAxis: 2,         // Z 轴
    referenceAxisName: "Z",
    minValue: -180,
    maxValue: 180,
    runSpeed: 50,
    targetValue: 0,
    isHaveElectricalMachinery: true,
    offset: 0
  });
  console.log('   结果:', rotateResult.code === 200 ? '✅ 成功' : '❌ 失败', rotateResult.msg);
  
  console.log('\n✅ 行为测试完成!');
  console.log('\n💡 提示：在 Kunwu Builder 中选中该模型，应该能看到行为组件了');
}

main().catch(err => {
  console.error('❌ 错误:', err.message);
  process.exit(1);
});
