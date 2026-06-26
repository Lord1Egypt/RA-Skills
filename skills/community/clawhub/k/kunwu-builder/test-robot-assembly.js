#!/usr/bin/env node

/**
 * 机器人装配演示脚本
 * 1. 从云端下载机器人、地轨、夹具
 * 2. 创建夹具行为
 * 3. 夹具装配到机器人
 * 4. 机器人装配到地轨
 */

import { callAPI } from './kunwu-tool.js';

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

// 从场景树获取 modelId
function findModelId(treeData, modelName) {
  if (!treeData?.models) return null;
  const model = treeData.models.find(m => m.modelName === modelName);
  return model?.modelId || null;
}

async function buildRobotAssembly() {
  console.log('=== 🤖 机器人装配演示 ===\n');
  console.log('目标:');
  console.log('  1. 加载机器人 LR_MATE_200ID_7L');
  console.log('  2. 加载地轨_02');
  console.log('  3. 加载夹具模型');
  console.log('  4. 夹具绑定行为后装配至机器人');
  console.log('  5. 机器人装配至地轨\n');
  
  try {
    // 0. 重置场景
    console.log('0️⃣ 重置场景...');
    await callAPI('/ResetScene', {});
    await sleep(3000);
    console.log('  ✓ 场景已重置\n');
    
    // 1. 查询云端模型
    console.log('1️⃣ 查询云端模型...');
    const allModels = await callAPI('/model/library/remote', { searchKey: '' });
    const rows = allModels?.data?.rows || [];
    
    // 查找机器人
    const robotModel = rows.find(m => m.classify_name === '机器人' && m.name.includes('KR'));
    console.log('  机器人:', robotModel?.name || '使用 KR300_R2700_2');
    
    // 查找地轨（如果没有，用方形模拟）
    const trackModel = rows.find(m => m.name.includes('地轨'));
    console.log('  地轨:', trackModel?.name || '用方形模拟');
    
    // 查找夹具（如果没有，用方形模拟）
    const gripperModel = rows.find(m => m.name.includes('夹具') || m.name.includes('gripper'));
    console.log('  夹具:', gripperModel?.name || '用方形模拟\n');
    
    // 2. 创建地轨
    console.log('2️⃣ 创建地轨...');
    if (trackModel) {
      await callAPI('/model/download', {
        id: trackModel.id,
        rename: 'LinearTrack',
        position: [0, 0, 0],
        createInScene: true
      });
      console.log('  ✓ 地轨下载请求已发送');
    } else {
      // 用方形模拟地轨（长条形）
      await callAPI('/model/download', {
        id: '方形',
        rename: 'LinearTrack',
        position: [0, 0, 0],
        parameterizationCfg: [
          { type: 0, value: 4000 },  // 长 4m
          { type: 1, value: 300 },   // 宽 300mm
          { type: 2, value: 200 }    // 高 200mm
        ],
        createInScene: true
      });
      console.log('  ✓ 地轨（模拟）创建请求已发送 (4000×300×200mm)');
    }
    await sleep(4000);
    
    // 3. 创建机器人
    console.log('\n3️⃣ 创建机器人...');
    if (robotModel) {
      await callAPI('/model/download', {
        id: robotModel.id,
        rename: 'Robot_LR_MATE',
        position: [2000, 0, 200],  // 放置在地轨上
        createInScene: true
      });
      console.log('  ✓ 机器人下载请求已发送 (' + robotModel.name + ')');
    } else {
      // 用方形模拟机器人基座
      await callAPI('/model/download', {
        id: '方形',
        rename: 'Robot_LR_MATE',
        position: [2000, 0, 200],
        parameterizationCfg: [
          { type: 0, value: 300 },
          { type: 1, value: 300 },
          { type: 2, value: 500 }
        ],
        createInScene: true
      });
      console.log('  ✓ 机器人（模拟）创建请求已发送');
    }
    await sleep(4000);
    
    // 4. 创建夹具
    console.log('\n4️⃣ 创建夹具...');
    if (gripperModel) {
      await callAPI('/model/download', {
        id: gripperModel.id,
        rename: 'Gripper',
        position: [2000, 0, 750],  // 机器人顶部
        createInScene: true
      });
      console.log('  ✓ 夹具下载请求已发送');
    } else {
      // 用方形模拟夹具
      await callAPI('/model/download', {
        id: '方形',
        rename: 'Gripper',
        position: [2000, 0, 750],
        parameterizationCfg: [
          { type: 0, value: 200 },
          { type: 1, value: 150 },
          { type: 2, value: 100 }
        ],
        createInScene: true
      });
      console.log('  ✓ 夹具（模拟）创建请求已发送 (200×150×100mm)');
    }
    await sleep(4000);
    
    // 5. 获取场景树和 modelId
    console.log('\n5️⃣ 获取模型 ID...');
    let tree = await callAPI('/models/tree', {});
    
    const trackId = findModelId(tree.data, 'LinearTrack');
    const robotId = findModelId(tree.data, 'Robot_LR_MATE');
    const gripperId = findModelId(tree.data, 'Gripper');
    
    console.log('  地轨 modelId:', trackId?.slice(0, 8) + '...');
    console.log('  机器人 modelId:', robotId?.slice(0, 8) + '...');
    console.log('  夹具 modelId:', gripperId?.slice(0, 8) + '...');
    
    // 6. 为夹具添加行为（开合动作）
    console.log('\n6️⃣ 为夹具添加行为...');
    if (gripperId) {
      // 添加旋转行为模拟开合
      const behaviorResult = await callAPI('/behavior/add', {
        modelId: gripperId,
        behavioralType: 2,  // 旋转
        referenceAxis: 2,   // Z 轴
        minPos: -45,
        maxPos: 45,
        speed: 90,
        runState: 0
      });
      console.log('  ✓ 夹具行为添加请求已发送 (旋转开合 -45°~45°)');
    }
    
    // 7. 夹具装配到机器人
    console.log('\n7️⃣ 夹具装配到机器人...');
    if (gripperId && robotId) {
      const assembleGripper = await callAPI('/model/assemble', {
        id: gripperId,
        useModeId: true,
        targetId: robotId,
        targetUseModeId: true,
        position: [0, 0, 500]  // 相对于机器人顶部
      });
      console.log('  ✓ 夹具装配到机器人请求已发送');
      console.log('    相对位置：[0, 0, 500]');
    }
    await sleep(3000);
    
    // 8. 机器人装配到地轨
    console.log('\n8️⃣ 机器人装配到地轨...');
    if (robotId && trackId) {
      const assembleRobot = await callAPI('/model/assemble', {
        id: robotId,
        useModeId: true,
        targetId: trackId,
        targetUseModeId: true,
        position: [0, 0, 200]  // 相对于地轨顶面
      });
      console.log('  ✓ 机器人装配到地轨请求已发送');
      console.log('    相对位置：[0, 0, 200]');
    }
    await sleep(3000);
    
    // 9. 获取最终场景树
    console.log('\n9️⃣ 获取最终场景层级...');
    tree = await callAPI('/models/tree', {});
    const models = tree?.data?.models || [];
    console.log('  场景模型总数:', models.length);
    models.forEach(m => {
      console.log('   - ' + m.modelName + ' (ID: ' + m.modelId.slice(0, 8) + '...)');
    });
    
    // 10. 切换到行为模式
    console.log('\n🔟 切换到行为信号模式...');
    const modeResult = await callAPI('/ChangeMode', { mode: 1 });
    console.log('  模式:', modeResult?.data?.resultMsg || '切换成功');
    
    console.log('\n=== ✅ 装配完成 ===\n');
    console.log('📋 装配层级:');
    console.log('  地轨 (LinearTrack)');
    console.log('    └─ 机器人 (Robot_LR_MATE)');
    console.log('        └─ 夹具 (Gripper) [带旋转行为]');
    console.log('\n💡 后续操作:');
    console.log('  1. 在 Kunwu Builder 中查看装配结果');
    console.log('  2. 测试夹具开合行为');
    console.log('  3. 添加地轨直线运动行为');
    console.log('  4. 配置机器人运动轨迹');
    
  } catch (err) {
    console.error('\n❌ 错误:', err.message);
    console.error(err.stack);
  }
}

buildRobotAssembly();
