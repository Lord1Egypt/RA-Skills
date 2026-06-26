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
  console.log('🧪 为 "方形 rot-x" 添加绕 X 轴旋转行为\n');
  
  const modelName = "方形rot-x";  // 正确的名称（无空格）
  
  // 1. 添加行为
  console.log('1️⃣ 添加绕 X 轴旋转行为...');
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
    console.log('   行为类型：旋转 (Type 2)');
    console.log('   参考轴：X 轴 (Axis 0)');
    console.log('   角度范围:', addResult.data.minValue, '° ~', addResult.data.maxValue, '°');
    console.log('   旋转速度:', addResult.data.runSpeed, '°/s');
    console.log('   目标角度:', addResult.data.targetValue, '°');
  }
  
  // 2. 验证
  console.log('\n2️⃣ 验证行为...');
  const verifyResult = await call('/behavior/get', {
    id: modelName,
    useModeId: false
  });
  
  if (verifyResult.data?.hasBehavior) {
    console.log('   ✅ 验证成功!');
    console.log('      类型：旋转 (Type 2)');
    console.log('      轴向：X 轴 (Axis 0)');
    console.log('      范围:', verifyResult.data.minValue, '° ~', verifyResult.data.maxValue, '°');
  } else {
    console.log('   ⚠️  响应码:', verifyResult.code, verifyResult.msg);
  }
  
  console.log('\n✅ 完成！在 Kunwu Builder 中:');
  console.log('   1. 展开 "方形" 节点');
  console.log('   2. 选中 "方形rot-x" 子节点');
  console.log('   3. 查看属性面板的行为组件');
}

main().catch(err => {
  console.error('❌ 错误:', err.message);
  process.exit(1);
});
