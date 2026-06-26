#!/usr/bin/env node

/**
 * 装配测试 v4 - 使用唯一命名
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
    console.log('=== 装配测试 v4 ===\n');
    
    // 1. 获取机器人模型
    const all = await callAPI('/model/library/remote', { searchKey: '' });
    const robotModel = (all?.data?.rows || []).find(m => m.classify_name === '机器人');
    console.log('机器人:', robotModel?.name);
    
    // 2. 创建模型（用唯一名称）
    console.log('\n创建模型...');
    
    const ts = Date.now();
    
    // 地轨
    const t1 = await callAPI('/model/download', {
      id: '方形',
      rename: 'Track_' + ts,
      position: [0, 0, 0],
      parameterizationCfg: [{ type: 0, value: 4000 }, { type: 1, value: 300 }, { type: 2, value: 200 }],
      createInScene: true
    });
    
    // 机器人（用机器人模型，但 rename 用唯一名称）
    const t2 = await callAPI('/model/download', {
      id: robotModel?.id || '方形',
      rename: 'Robot_' + ts,
      position: [2000, 0, 200],
      createInScene: true
    });
    
    // 夹具
    const t3 = await callAPI('/model/download', {
      id: '方形',
      rename: 'Gripper_' + ts,
      position: [2000, 0, 700],
      parameterizationCfg: [{ type: 0, value: 200 }, { type: 1, value: 150 }, { type: 2, value: 100 }],
      createInScene: true
    });
    
    console.log('  Track:', t1?.data?.taskId);
    console.log('  Robot:', t2?.data?.taskId);
    console.log('  Gripper:', t3?.data?.taskId);
    
    // 3. 等待
    console.log('\n等待完成...');
    await waitForTask(t1.data.taskId);
    await waitForTask(t2.data.taskId);
    await waitForTask(t3.data.taskId);
    console.log('  ✓ 完成\n');
    
    // 4. 获取场景树
    await sleep(2000);
    const tree = await callAPI('/models/tree', {});
    const models = tree?.data?.models || [];
    
    console.log('场景模型:');
    models.forEach(m => {
      console.log('  - ' + m.modelName + ' (' + m.modelId.slice(0, 8) + ')');
    });
    
    // 5. 通过时间戳后缀查找
    const track = models.find(m => m.modelName.startsWith('Track_'));
    const robot = models.find(m => m.modelName.startsWith('Robot_'));
    const gripper = models.find(m => m.modelName.startsWith('Gripper_'));
    
    console.log('\n找到:');
    console.log('  Track:', track?.modelId?.slice(0, 8));
    console.log('  Robot:', robot?.modelId?.slice(0, 8));
    console.log('  Gripper:', gripper?.modelId?.slice(0, 8));
    
    if (!track?.modelId || !robot?.modelId || !gripper?.modelId) {
      console.log('\n❌ 未找到所有模型');
      return;
    }
    
    // 6. 添加行为
    console.log('\n添加夹具行为...');
    const behavior = await callAPI('/behavior/add', {
      modelId: gripper.modelId,
      behavioralType: 2,
      referenceAxis: 2,
      minPos: -45,
      maxPos: 45,
      speed: 90,
      runState: 0
    });
    console.log('  ', behavior?.data?.resultMsg || '成功');
    
    // 7. 装配：夹具 → 机器人
    console.log('\n装配：夹具 → 机器人...');
    const asm1 = await callAPI('/model/assemble', {
      id: gripper.modelId,
      useModeId: true,
      targetId: robot.modelId,
      targetUseModeId: true,
      position: [0, 0, 500]
    });
    console.log('  ', asm1?.data?.resultMsg || '成功');
    await sleep(2000);
    
    // 8. 装配：机器人 → 地轨
    console.log('\n装配：机器人 → 地轨...');
    const asm2 = await callAPI('/model/assemble', {
      id: robot.modelId,
      useModeId: true,
      targetId: track.modelId,
      targetUseModeId: true,
      position: [0, 0, 200]
    });
    console.log('  ', asm2?.data?.resultMsg || '成功');
    await sleep(2000);
    
    // 9. 最终场景
    console.log('\n最终场景...');
    const finalTree = await callAPI('/models/tree', {});
    const finalModels = finalTree?.data?.models || [];
    
    console.log('模型数:', finalModels.length);
    finalModels.forEach(m => {
      const children = m.children?.length ? ` [${m.children.length} 子节点]` : '';
      console.log('  - ' + m.modelName + children);
      if (m.children) {
        m.children.forEach(c => {
          console.log('    └─ ' + c.modelName);
        });
      }
    });
    
    console.log('\n✅ 装配完成!');
    
  } catch (err) {
    console.error('❌', err.message);
  }
})();
