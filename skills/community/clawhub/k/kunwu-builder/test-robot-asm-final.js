#!/usr/bin/env node

/**
 * 机器人装配最终版 - 带完整等待逻辑
 */

import { callAPI } from './kunwu-tool.js';

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

// 等待任务完成
async function waitForTask(taskId, timeout = 30000) {
  const start = Date.now();
  while (Date.now() - start < timeout) {
    const status = await callAPI('/task/query', { taskId });
    if (status?.data?.done) {
      return status.data;
    }
    await sleep(1000);
  }
  throw new Error('Task timeout: ' + taskId);
}

// 从场景树获取 modelId
function findModelId(treeData, modelName) {
  if (!treeData?.models) return null;
  const model = treeData.models.find(m => m.modelName === modelName);
  return model?.modelId || null;
}

async function main() {
  console.log('=== 🤖 机器人装配（完整版）===\n');
  console.log('步骤:');
  console.log('  1. 创建地轨 (4000mm 直线)');
  console.log('  2. 创建机器人 (GCR25_1800)');
  console.log('  3. 创建夹具 (带旋转行为)');
  console.log('  4. 夹具 → 机器人装配');
  console.log('  5. 机器人 → 地轨装配\n');
  
  try {
    // 1. 获取云端机器人模型
    console.log('1️⃣ 获取云端机器人模型...');
    const all = await callAPI('/model/library/remote', { searchKey: '' });
    const rows = all?.data?.rows || [];
    const robotModel = rows.find(m => m.classify_name === '机器人');
    
    if (!robotModel) {
      console.log('  ❌ 未找到机器人模型');
      return;
    }
    
    console.log('  ✓ 机器人:', robotModel.name, '(' + robotModel.brand + ')');
    console.log('    ID:', robotModel.id.slice(0, 12) + '...\n');
    
    // 2. 创建地轨
    console.log('2️⃣ 创建地轨...');
    const trackTask = await callAPI('/model/download', {
      id: '方形',
      rename: 'LinearTrack',
      position: [0, 0, 0],
      parameterizationCfg: [
        { type: 0, value: 4000 },
        { type: 1, value: 300 },
        { type: 2, value: 200 }
      ],
      createInScene: true
    });
    console.log('  任务 ID:', trackTask?.data?.taskId);
    await waitForTask(trackTask.data.taskId);
    console.log('  ✓ 地轨创建完成\n');
    
    // 3. 创建机器人
    console.log('3️⃣ 创建机器人...');
    const robotTask = await callAPI('/model/download', {
      id: robotModel.id,
      rename: 'Robot_Arm',
      position: [2000, 0, 200],
      createInScene: true
    });
    console.log('  任务 ID:', robotTask?.data?.taskId);
    await waitForTask(robotTask.data.taskId);
    console.log('  ✓ 机器人创建完成\n');
    
    // 4. 创建夹具
    console.log('4️⃣ 创建夹具...');
    const gripperTask = await callAPI('/model/download', {
      id: '方形',
      rename: 'Gripper',
      position: [2000, 0, 700],
      parameterizationCfg: [
        { type: 0, value: 200 },
        { type: 1, value: 150 },
        { type: 2, value: 100 }
      ],
      createInScene: true
    });
    console.log('  任务 ID:', gripperTask?.data?.taskId);
    await waitForTask(gripperTask.data.taskId);
    console.log('  ✓ 夹具创建完成\n');
    
    // 5. 获取模型 ID
    console.log('5️⃣ 获取模型 ID...');
    let tree = await callAPI('/models/tree', {});
    
    const trackId = findModelId(tree.data, 'LinearTrack');
    const robotId = findModelId(tree.data, 'Robot_Arm');
    const gripperId = findModelId(tree.data, 'Gripper');
    
    if (!trackId || !robotId || !gripperId) {
      console.log('  ❌ 未找到模型 ID');
      console.log('    Track:', trackId);
      console.log('    Robot:', robotId);
      console.log('    Gripper:', gripperId);
      return;
    }
    
    console.log('  ✓ LinearTrack:', trackId.slice(0, 8) + '...');
    console.log('  ✓ Robot_Arm:', robotId.slice(0, 8) + '...');
    console.log('  ✓ Gripper:', gripperId.slice(0, 8) + '...\n');
    
    // 6. 为夹具添加行为
    console.log('6️⃣ 添加夹具行为（旋转开合）...');
    const behaviorResult = await callAPI('/behavior/add', {
      modelId: gripperId,
      behavioralType: 2,    // 旋转
      referenceAxis: 2,     // Z 轴
      minPos: -45,
      maxPos: 45,
      speed: 90,
      runState: 0
    });
    console.log('  结果:', behaviorResult?.data?.resultMsg || '成功');
    console.log('  行为：旋转 -45° ~ 45°, 速度 90°/s\n');
    
    // 7. 夹具装配到机器人
    console.log('7️⃣ 夹具装配到机器人...');
    const asmGripper = await callAPI('/model/assemble', {
      id: gripperId,
      useModeId: true,
      targetId: robotId,
      targetUseModeId: true,
      position: [0, 0, 500],
      eulerAngle: [0, 0, 0]
    });
    console.log('  结果:', asmGripper?.data?.resultMsg || '成功');
    console.log('  相对位置：[0, 0, 500]\n');
    await sleep(2000);
    
    // 8. 机器人装配到地轨
    console.log('8️⃣ 机器人装配到地轨...');
    const asmRobot = await callAPI('/model/assemble', {
      id: robotId,
      useModeId: true,
      targetId: trackId,
      targetUseModeId: true,
      position: [0, 0, 200],
      eulerAngle: [0, 0, 0]
    });
    console.log('  结果:', asmRobot?.data?.resultMsg || '成功');
    console.log('  相对位置：[0, 0, 200]\n');
    await sleep(2000);
    
    // 9. 最终场景树
    console.log('9️⃣ 最终场景层级...');
    tree = await callAPI('/models/tree', {});
    const models = tree?.data?.models || [];
    console.log('  模型总数:', models.length);
    
    // 显示层级关系
    console.log('\n📋 装配层级:');
    const rootModels = models.filter(m => !m.children || m.children.length === 0 || 
      !models.some(child => child.modelId === m.modelId));
    
    models.forEach(m => {
      const indent = m.children && m.children.length > 0 ? '└─ ' : '   ';
      console.log('  ' + indent + m.modelName + ' (' + m.modelId.slice(0, 8) + '...)');
      if (m.children && m.children.length > 0) {
        m.children.forEach(c => {
          console.log('      └─ ' + c.modelName + ' (' + c.modelId.slice(0, 8) + '...)');
        });
      }
    });
    
    // 10. 切换到行为模式
    console.log('\n🔟 切换到行为信号模式...');
    const modeResult = await callAPI('/ChangeMode', { mode: 1 });
    console.log('  模式:', modeResult?.data?.resultMsg || '成功');
    
    console.log('\n=== ✅ 装配完成 ===\n');
    console.log('💡 后续操作:');
    console.log('  • 在 Kunwu Builder 中查看装配结果');
    console.log('  • 测试夹具旋转行为 (-45° ~ 45°)');
    console.log('  • 添加地轨直线运动行为');
    console.log('  • 配置机器人轨迹运动');
    
  } catch (err) {
    console.error('\n❌ 错误:', err.message);
    console.error(err.stack);
  }
}

main();
