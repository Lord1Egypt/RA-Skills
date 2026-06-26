#!/usr/bin/env node

/**
 * 装配演示 - 用方形模拟所有模型（确保流程可用）
 * 实际使用时替换为真实机器人模型
 */

import { callAPI } from './kunwu-tool.js';

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

async function waitForTask(taskId) {
  for (let i = 0; i < 30; i++) {
    const status = await callAPI('/task/query', { taskId });
    if (status?.data?.done) return status.data;
    await sleep(1000);
  }
  throw new Error('Timeout');
}

(async () => {
  console.log('=== 🤖 机器人装配演示 ===\n');
  console.log('说明：由于云端机器人模型下载失败，本演示使用方形模型模拟');
  console.log('     实际使用时可替换为 LR_MATE_200ID_7L 等真实机器人模型\n');
  
  try {
    const ts = Date.now();
    
    // 1. 创建地轨
    console.log('1️⃣ 创建地轨...');
    const t1 = await callAPI('/model/download', {
      id: '方形',
      rename: 'Demo_Track_' + ts,
      position: [0, 0, 0],
      parameterizationCfg: [{ type: 0, value: 4000 }, { type: 1, value: 300 }, { type: 2, value: 200 }],
      createInScene: true
    });
    await waitForTask(t1.data.taskId);
    console.log('  ✓ 地轨完成 (4000×300×200mm)\n');
    
    // 2. 创建机器人（用方形模拟）
    console.log('2️⃣ 创建机器人（模拟）...');
    const t2 = await callAPI('/model/download', {
      id: '方形',
      rename: 'Demo_Robot_' + ts,
      position: [2000, 0, 200],
      parameterizationCfg: [{ type: 0, value: 300 }, { type: 1, value: 300 }, { type: 2, value: 600 }],
      createInScene: true
    });
    await waitForTask(t2.data.taskId);
    console.log('  ✓ 机器人完成 (300×300×600mm)\n');
    
    // 3. 创建夹具
    console.log('3️⃣ 创建夹具...');
    const t3 = await callAPI('/model/download', {
      id: '方形',
      rename: 'Demo_Gripper_' + ts,
      position: [2000, 0, 850],
      parameterizationCfg: [{ type: 0, value: 200 }, { type: 1, value: 150 }, { type: 2, value: 100 }],
      createInScene: true
    });
    await waitForTask(t3.data.taskId);
    console.log('  ✓ 夹具完成 (200×150×100mm)\n');
    
    // 4. 获取模型 ID
    console.log('4️⃣ 获取模型 ID...');
    await sleep(2000);
    const tree = await callAPI('/models/tree', {});
    const models = tree?.data?.models || [];
    
    const track = models.find(m => m.modelName.startsWith('Demo_Track_'));
    const robot = models.find(m => m.modelName.startsWith('Demo_Robot_'));
    const gripper = models.find(m => m.modelName.startsWith('Demo_Gripper_'));
    
    console.log('  Track:', track?.modelId?.slice(0, 8));
    console.log('  Robot:', robot?.modelId?.slice(0, 8));
    console.log('  Gripper:', gripper?.modelId?.slice(0, 8));
    
    if (!track?.modelId || !robot?.modelId || !gripper?.modelId) {
      console.log('  ❌ 未找到模型');
      return;
    }
    console.log();
    
    // 5. 添加夹具行为
    console.log('5️⃣ 添加夹具行为（旋转开合）...');
    const behavior = await callAPI('/behavior/add', {
      id: gripper.modelId,
      useModeId: true,
      behavioralType: 2,    // 旋转
      referenceAxis: 2,     // Z 轴
      minValue: -45,
      maxValue: 45,
      runSpeed: 90
    });
    console.log('  ✓ 行为添加:', behavior?.data?.resultMsg || '成功');
    console.log('  参数：旋转 -45° ~ 45°, 速度 90°/s\n');
    
    // 6. 夹具装配到机器人
    console.log('6️⃣ 夹具 → 机器人装配...');
    const asm1 = await callAPI('/model/assemble', {
      id: gripper.modelId,
      useModeId: true,
      targetId: robot.modelId,
      targetUseModeId: true,
      position: [0, 0, 500],
      eulerAngle: [0, 0, 0]
    });
    console.log('  ✓ 装配结果:', asm1?.data?.resultMsg || '成功');
    console.log('  相对位置：[0, 0, 500]\n');
    await sleep(2000);
    
    // 7. 机器人装配到地轨
    console.log('7️⃣ 机器人 → 地轨装配...');
    const asm2 = await callAPI('/model/assemble', {
      id: robot.modelId,
      useModeId: true,
      targetId: track.modelId,
      targetUseModeId: true,
      position: [0, 0, 200],
      eulerAngle: [0, 0, 0]
    });
    console.log('  ✓ 装配结果:', asm2?.data?.resultMsg || '成功');
    console.log('  相对位置：[0, 0, 200]\n');
    await sleep(2000);
    
    // 8. 最终场景
    console.log('8️⃣ 最终场景层级...');
    const finalTree = await callAPI('/models/tree', {});
    const finalModels = finalTree?.data?.models || [];
    
    console.log('  模型总数:', finalModels.length);
    console.log('\n  层级结构:');
    finalModels.forEach(m => {
      if (m.modelName.startsWith('Demo_')) {
        const hasChildren = m.children && m.children.length > 0;
        console.log('  ┌─ ' + m.modelName);
        if (hasChildren) {
          m.children.forEach(c => {
            console.log('  │   └─ ' + c.modelName);
          });
        }
      }
    });
    
    // 9. 切换模式
    console.log('\n9️⃣ 切换到行为信号模式...');
    const mode = await callAPI('/ChangeMode', { mode: 1 });
    console.log('  ✓ 模式:', mode?.data?.resultMsg || '成功');
    
    console.log('\n=== ✅ 装配完成 ===\n');
    console.log('📋 装配关系:');
    console.log('  地轨 (Demo_Track_*)');
    console.log('    └─ 机器人 (Demo_Robot_*)');
    console.log('        └─ 夹具 (Demo_Gripper_*) [带旋转行为]');
    console.log('\n💡 下一步:');
    console.log('  • 在 Kunwu Builder 中查看装配结果');
    console.log('  • 测试夹具旋转行为');
    console.log('  • 添加地轨直线运动行为');
    console.log('  • 替换为真实机器人模型（LR_MATE_200ID_7L 等）');
    
  } catch (err) {
    console.error('\n❌ 错误:', err.message);
  }
})();
