#!/usr/bin/env node

/**
 * 机器人装配 v2 - 快速版本
 */

import { callAPI } from './kunwu-tool.js';

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

async function main() {
  console.log('=== 🤖 机器人快速装配 ===\n');
  
  try {
    // 1. 获取云端模型
    console.log('1️⃣ 获取云端模型...');
    const all = await callAPI('/model/library/remote', { searchKey: '' });
    const rows = all?.data?.rows || [];
    
    const robotModel = rows.find(m => m.classify_name === '机器人');
    console.log('  机器人:', robotModel?.name || '无');
    console.log('  ID:', robotModel?.id?.slice(0, 12) + '...');
    
    // 2. 创建地轨（用方形）
    console.log('\n2️⃣ 创建地轨...');
    const track = await callAPI('/model/download', {
      id: '方形',
      rename: 'Track',
      position: [0, 0, 0],
      parameterizationCfg: [
        { type: 0, value: 4000 },
        { type: 1, value: 300 },
        { type: 2, value: 200 }
      ],
      createInScene: true
    });
    console.log('  任务 ID:', track?.data?.taskId);
    await sleep(4000);
    
    // 3. 创建机器人
    console.log('\n3️⃣ 创建机器人...');
    const robot = await callAPI('/model/download', {
      id: robotModel?.id || '方形',
      rename: 'Robot',
      position: [2000, 0, 200],
      createInScene: true
    });
    console.log('  任务 ID:', robot?.data?.taskId);
    await sleep(4000);
    
    // 4. 创建夹具
    console.log('\n4️⃣ 创建夹具...');
    const gripper = await callAPI('/model/download', {
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
    console.log('  任务 ID:', gripper?.data?.taskId);
    await sleep(4000);
    
    // 5. 获取场景树
    console.log('\n5️⃣ 获取模型 ID...');
    const tree = await callAPI('/models/tree', {});
    const models = tree?.data?.models || [];
    
    const trackModel = models.find(m => m.modelName === 'Track');
    const robotModel_ = models.find(m => m.modelName === 'Robot');
    const gripperModel = models.find(m => m.modelName === 'Gripper');
    
    console.log('  Track:', trackModel?.modelId?.slice(0, 8));
    console.log('  Robot:', robotModel_?.modelId?.slice(0, 8));
    console.log('  Gripper:', gripperModel?.modelId?.slice(0, 8));
    
    // 6. 添加夹具行为
    if (gripperModel?.modelId) {
      console.log('\n6️⃣ 添加夹具行为...');
      const behavior = await callAPI('/behavior/add', {
        modelId: gripperModel.modelId,
        behavioralType: 2,
        referenceAxis: 2,
        minPos: -45,
        maxPos: 45,
        speed: 90,
        runState: 0
      });
      console.log('  行为添加:', behavior?.data?.resultMsg || '成功');
    }
    
    // 7. 装配
    if (gripperModel?.modelId && robotModel_?.modelId) {
      console.log('\n7️⃣ 夹具装配到机器人...');
      const asm1 = await callAPI('/model/assemble', {
        id: gripperModel.modelId,
        useModeId: true,
        targetId: robotModel_.modelId,
        targetUseModeId: true,
        position: [0, 0, 500]
      });
      console.log('  装配结果:', asm1?.data?.resultMsg || '成功');
      await sleep(2000);
    }
    
    if (robotModel_?.modelId && trackModel?.modelId) {
      console.log('\n8️⃣ 机器人装配到地轨...');
      const asm2 = await callAPI('/model/assemble', {
        id: robotModel_.modelId,
        useModeId: true,
        targetId: trackModel.modelId,
        targetUseModeId: true,
        position: [0, 0, 200]
      });
      console.log('  装配结果:', asm2?.data?.resultMsg || '成功');
      await sleep(2000);
    }
    
    // 9. 最终场景树
    console.log('\n9️⃣ 最终场景...');
    const finalTree = await callAPI('/models/tree', {});
    console.log('  模型数:', finalTree?.data?.models?.length || 0);
    
    console.log('\n✅ 完成!');
    
  } catch (err) {
    console.error('❌ 错误:', err.message);
  }
}

main();
