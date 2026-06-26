#!/usr/bin/env node

/**
 * 快速装配测试 - 不重置场景
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
  try {
    console.log('=== 快速装配测试 ===\n');
    
    // 1. 获取机器人模型
    console.log('1. 获取机器人模型...');
    const all = await callAPI('/model/library/remote', { searchKey: '' });
    const robotModel = (all?.data?.rows || []).find(m => m.classify_name === '机器人');
    console.log('   ', robotModel?.name, robotModel?.id?.slice(0, 8));
    
    // 2. 创建 3 个模型
    console.log('\n2. 创建模型...');
    
    const tasks = [];
    
    // 地轨
    const t1 = await callAPI('/model/download', {
      id: '方形',
      rename: 'MyTrack',
      position: [0, 0, 0],
      parameterizationCfg: [{ type: 0, value: 4000 }, { type: 1, value: 300 }, { type: 2, value: 200 }],
      createInScene: true
    });
    tasks.push({ name: 'MyTrack', taskId: t1?.data?.taskId });
    console.log('   MyTrack:', t1?.data?.taskId);
    
    // 机器人
    const t2 = await callAPI('/model/download', {
      id: robotModel?.id || '方形',
      rename: 'MyRobot',
      position: [2000, 0, 200],
      createInScene: true
    });
    tasks.push({ name: 'MyRobot', taskId: t2?.data?.taskId });
    console.log('   MyRobot:', t2?.data?.taskId);
    
    // 夹具
    const t3 = await callAPI('/model/download', {
      id: '方形',
      rename: 'MyGripper',
      position: [2000, 0, 700],
      parameterizationCfg: [{ type: 0, value: 200 }, { type: 1, value: 150 }, { type: 2, value: 100 }],
      createInScene: true
    });
    tasks.push({ name: 'MyGripper', taskId: t3?.data?.taskId });
    console.log('   MyGripper:', t3?.data?.taskId);
    
    // 3. 等待完成
    console.log('\n3. 等待完成...');
    for (const t of tasks) {
      await waitForTask(t.taskId);
      console.log('   ✓', t.name);
    }
    
    // 4. 获取模型 ID
    console.log('\n4. 获取模型 ID...');
    await sleep(2000);
    const tree = await callAPI('/models/tree', {});
    const models = tree?.data?.models || [];
    
    const track = models.find(m => m.modelName === 'MyTrack');
    const robot = models.find(m => m.modelName === 'MyRobot');
    const gripper = models.find(m => m.modelName === 'MyGripper');
    
    console.log('   MyTrack:', track?.modelId?.slice(0, 8));
    console.log('   MyRobot:', robot?.modelId?.slice(0, 8));
    console.log('   MyGripper:', gripper?.modelId?.slice(0, 8));
    
    if (!track?.modelId || !robot?.modelId || !gripper?.modelId) {
      console.log('   ❌ 未找到所有模型');
      console.log('   实际模型:', models.map(m => m.modelName).join(', '));
      return;
    }
    
    // 5. 添加行为
    console.log('\n5. 添加夹具行为...');
    const behavior = await callAPI('/behavior/add', {
      modelId: gripper.modelId,
      behavioralType: 2,
      referenceAxis: 2,
      minPos: -45,
      maxPos: 45,
      speed: 90,
      runState: 0
    });
    console.log('   ', behavior?.data?.resultMsg);
    
    // 6. 装配
    console.log('\n6. 夹具 → 机器人...');
    const asm1 = await callAPI('/model/assemble', {
      id: gripper.modelId,
      useModeId: true,
      targetId: robot.modelId,
      targetUseModeId: true,
      position: [0, 0, 500]
    });
    console.log('   ', asm1?.data?.resultMsg);
    
    console.log('\n7. 机器人 → 地轨...');
    const asm2 = await callAPI('/model/assemble', {
      id: robot.modelId,
      useModeId: true,
      targetId: track.modelId,
      targetUseModeId: true,
      position: [0, 0, 200]
    });
    console.log('   ', asm2?.data?.resultMsg);
    
    // 8. 最终结果
    console.log('\n8. 最终场景...');
    await sleep(2000);
    const finalTree = await callAPI('/models/tree', {});
    const finalModels = finalTree?.data?.models || [];
    console.log('   模型数:', finalModels.length);
    finalModels.forEach(m => {
      console.log('   -', m.modelName, m.children?.length ? `[${m.children.length} 子节点]` : '');
    });
    
    console.log('\n✅ 完成!');
    
  } catch (err) {
    console.error('❌', err.message);
  }
})();
