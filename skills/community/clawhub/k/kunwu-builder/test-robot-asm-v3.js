#!/usr/bin/env node

/**
 * 机器人装配 v3 - 修正模型名称查找
 */

import { callAPI } from './kunwu-tool.js';

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

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

async function main() {
  console.log('=== 🤖 机器人装配 v3 ===\n');
  
  try {
    // 1. 重置场景
    console.log('1️⃣ 重置场景...');
    await callAPI('/ResetScene', {});
    await sleep(4000);
    console.log('  ✓ 完成\n');
    
    // 2. 获取机器人模型
    console.log('2️⃣ 获取云端机器人...');
    const all = await callAPI('/model/library/remote', { searchKey: '' });
    const rows = all?.data?.rows || [];
    const robotModel = rows.find(m => m.classify_name === '机器人');
    console.log('  机器人:', robotModel?.name || '未找到');
    if (!robotModel) return;
    console.log('  ID:', robotModel.id.slice(0, 12) + '...\n');
    
    // 3. 创建地轨
    console.log('3️⃣ 创建地轨...');
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
    console.log('  任务:', trackTask?.data?.taskId);
    await waitForTask(trackTask.data.taskId);
    console.log('  ✓ 地轨完成\n');
    
    // 4. 创建机器人
    console.log('4️⃣ 创建机器人...');
    const robotTask = await callAPI('/model/download', {
      id: robotModel.id,
      rename: 'RobotArm',
      position: [2000, 0, 200],
      createInScene: true
    });
    console.log('  任务:', robotTask?.data?.taskId);
    await waitForTask(robotTask.data.taskId);
    console.log('  ✓ 机器人完成\n');
    
    // 5. 创建夹具
    console.log('5️⃣ 创建夹具...');
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
    console.log('  任务:', gripperTask?.data?.taskId);
    await waitForTask(gripperTask.data.taskId);
    console.log('  ✓ 夹具完成\n');
    
    // 6. 获取场景树，通过 rename 查找
    console.log('6️⃣ 获取模型 ID...');
    await sleep(2000);
    let tree = await callAPI('/models/tree', {});
    const models = tree?.data?.models || [];
    
    console.log('  场景模型:');
    models.forEach(m => {
      console.log('    - ' + m.modelName + ' (' + m.modelId.slice(0, 8) + '...)');
    });
    
    // 查找模型（通过名称包含关系）
    const trackModel = models.find(m => m.modelName === 'LinearTrack');
    const robotModel_ = models.find(m => m.modelName === 'RobotArm' || m.modelName.includes('夹爪'));
    const gripperModel = models.find(m => m.modelName === 'Gripper' || (m.modelName.includes('夹爪') && m.modelId !== robotModel_?.modelId));
    
    const trackId = trackModel?.modelId;
    const robotId = robotModel_?.modelId;
    const gripperId = gripperModel?.modelId;
    
    console.log('\n  找到模型 ID:');
    console.log('    LinearTrack:', trackId?.slice(0, 8) || '未找到');
    console.log('    RobotArm:', robotId?.slice(0, 8) || '未找到');
    console.log('    Gripper:', gripperId?.slice(0, 8) || '未找到');
    
    if (!trackId || !robotId || !gripperId) {
      console.log('\n  ❌ 模型 ID 不完整，退出');
      return;
    }
    console.log();
    
    // 7. 添加夹具行为
    console.log('7️⃣ 添加夹具行为...');
    const behavior = await callAPI('/behavior/add', {
      modelId: gripperId,
      behavioralType: 2,
      referenceAxis: 2,
      minPos: -45,
      maxPos: 45,
      speed: 90,
      runState: 0
    });
    console.log('  结果:', behavior?.data?.resultMsg || '成功');
    console.log('  旋转：-45° ~ 45°\n');
    
    // 8. 夹具装配到机器人
    console.log('8️⃣ 夹具 → 机器人装配...');
    const asm1 = await callAPI('/model/assemble', {
      id: gripperId,
      useModeId: true,
      targetId: robotId,
      targetUseModeId: true,
      position: [0, 0, 500]
    });
    console.log('  结果:', asm1?.data?.resultMsg || '成功\n');
    await sleep(2000);
    
    // 9. 机器人装配到地轨
    console.log('9️⃣ 机器人 → 地轨装配...');
    const asm2 = await callAPI('/model/assemble', {
      id: robotId,
      useModeId: true,
      targetId: trackId,
      targetUseModeId: true,
      position: [0, 0, 200]
    });
    console.log('  结果:', asm2?.data?.resultMsg || '成功\n');
    await sleep(2000);
    
    // 10. 最终场景树
    console.log('🔟 最终场景层级...');
    tree = await callAPI('/models/tree', {});
    const finalModels = tree?.data?.models || [];
    
    console.log('  模型总数:', finalModels.length);
    finalModels.forEach(m => {
      let line = '  - ' + m.modelName + ' (' + m.modelId.slice(0, 8) + ')';
      if (m.children && m.children.length > 0) {
        line += ' [有 ' + m.children.length + ' 子节点]';
      }
      console.log(line);
    });
    
    console.log('\n=== ✅ 完成 ===');
    
  } catch (err) {
    console.error('❌ 错误:', err.message);
  }
}

main();
