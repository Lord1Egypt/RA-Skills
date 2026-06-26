#!/usr/bin/env node

/**
 * 下料分拣场景搭建脚本 v3 - 从场景树获取 modelId
 */

import { callAPI } from './kunwu-tool.js';

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

// 从场景树中通过名称获取 modelId
function findModelId(treeData, modelName) {
  if (!treeData?.models) return null;
  const model = treeData.models.find(m => m.modelName === modelName);
  return model?.modelId || null;
}

async function buildScene() {
  console.log('=== 🏭 下料分拣场景搭建 v3 ===\n');
  
  try {
    // 0. 重置场景
    console.log('0️⃣ 重置场景...');
    await callAPI('/ResetScene', {});
    await sleep(3000);
    
    // 1. 创建输送线
    console.log('\n1️⃣ 创建输送线...');
    await callAPI('/model/download', {
      id: '方形',
      rename: 'Conveyor',
      position: [0, 0, 0],
      createInScene: true
    });
    await sleep(3000);
    
    let tree = await callAPI('/models/tree', {});
    const conveyorId = findModelId(tree.data, 'Conveyor');
    console.log('  输送线 modelId:', conveyorId);
    
    if (conveyorId) {
      await callAPI('/model/set_pose', {
        id: conveyorId,
        useModeId: true,
        parameterizationCfg: [
          { type: 0, value: 3000 },
          { type: 1, value: 600 },
          { type: 2, value: 200 }
        ]
      });
      console.log('  ✓ 输送线尺寸设置 (3000×600×200mm)');
    }
    
    // 2. 创建机器人基座
    console.log('\n2️⃣ 创建机器人基座...');
    await callAPI('/model/download', {
      id: '方形',
      rename: 'RobotBase',
      position: [1500, 500, 0],
      createInScene: true
    });
    await sleep(3000);
    
    tree = await callAPI('/models/tree', {});
    const robotId = findModelId(tree.data, 'RobotBase');
    console.log('  机器人基座 modelId:', robotId);
    
    if (robotId) {
      await callAPI('/model/set_pose', {
        id: robotId,
        useModeId: true,
        parameterizationCfg: [
          { type: 0, value: 300 },
          { type: 1, value: 300 },
          { type: 2, value: 50 }
        ]
      });
      console.log('  ✓ 机器人基座完成');
    }
    
    // 3. 创建料框（3 个）
    console.log('\n3️⃣ 创建分拣料框...');
    const binConfigs = [
      { name: 'Bin_A', pos: [2500, -400, 0] },
      { name: 'Bin_B', pos: [2500, 0, 0] },
      { name: 'Bin_Reject', pos: [2500, 400, 0] }
    ];
    
    for (const bin of binConfigs) {
      await callAPI('/model/download', {
        id: '方形',
        rename: bin.name,
        position: bin.pos,
        createInScene: true
      });
      await sleep(2000);
    }
    
    tree = await callAPI('/models/tree', {});
    for (const bin of binConfigs) {
      const binId = findModelId(tree.data, bin.name);
      console.log('  ' + bin.name + ' modelId:', binId);
      
      if (binId) {
        await callAPI('/model/set_pose', {
          id: binId,
          useModeId: true,
          parameterizationCfg: [
            { type: 0, value: 400 },
            { type: 1, value: 400 },
            { type: 2, value: 300 }
          ]
        });
        console.log('    ✓ 尺寸设置 (400×400×300mm)');
      }
    }
    
    // 4. 创建相机支架
    console.log('\n4️⃣ 创建相机支架...');
    await callAPI('/model/download', {
      id: '方形',
      rename: 'CameraStand',
      position: [1500, -300, 0],
      createInScene: true
    });
    await sleep(3000);
    
    tree = await callAPI('/models/tree', {});
    const standId = findModelId(tree.data, 'CameraStand');
    console.log('  相机支架 modelId:', standId);
    
    if (standId) {
      await callAPI('/model/set_pose', {
        id: standId,
        useModeId: true,
        parameterizationCfg: [
          { type: 0, value: 100 },
          { type: 1, value: 100 },
          { type: 2, value: 1800 }
        ]
      });
      console.log('  ✓ 相机支架完成 (高 1.8m)');
    }
    
    // 5. 创建相机
    console.log('\n5️⃣ 创建相机...');
    await callAPI('/model/download', {
      id: '方形',
      rename: 'Camera',
      position: [1500, -300, 1750],
      eulerAngle: [90, 0, 0],
      createInScene: true
    });
    await sleep(3000);
    
    tree = await callAPI('/models/tree', {});
    const camId = findModelId(tree.data, 'Camera');
    console.log('  相机 modelId:', camId);
    
    if (camId) {
      await callAPI('/model/set_pose', {
        id: camId,
        useModeId: true,
        parameterizationCfg: [
          { type: 0, value: 150 },
          { type: 1, value: 100 },
          { type: 2, value: 80 }
        ]
      });
      console.log('  ✓ 相机完成 (俯视 90°)');
    }
    
    // 6. 创建工件（3 个）
    console.log('\n6️⃣ 创建工件...');
    const partConfigs = [
      { name: 'Part_1', pos: [500, 0, 220] },
      { name: 'Part_2', pos: [1000, 0, 220] },
      { name: 'Part_3', pos: [1500, 0, 220] }
    ];
    
    for (const part of partConfigs) {
      await callAPI('/model/download', {
        id: '方形',
        rename: part.name,
        position: part.pos,
        createInScene: true
      });
      await sleep(2000);
    }
    
    tree = await callAPI('/models/tree', {});
    for (const part of partConfigs) {
      const partId = findModelId(tree.data, part.name);
      if (partId) {
        await callAPI('/model/set_pose', {
          id: partId,
          useModeId: true,
          parameterizationCfg: [
            { type: 0, value: 100 },
            { type: 1, value: 100 },
            { type: 2, value: 100 }
          ]
        });
      }
    }
    console.log('  ✓ 3 个工件创建完成');
    
    // 7. 获取完整场景树
    console.log('\n7️⃣ 场景模型列表:');
    tree = await callAPI('/models/tree', {});
    const models = tree?.data?.models || [];
    console.log('  场景模型总数:', models.length);
    models.forEach(m => {
      console.log('   - ' + m.modelName + ' (ID: ' + m.modelId.slice(0, 8) + '...)');
    });
    
    // 8. 切换到行为模式
    console.log('\n8️⃣ 切换模式...');
    const modeResult = await callAPI('/ChangeMode', { mode: 1 });
    console.log('  当前模式:', modeResult?.data?.resultMsg);
    
    console.log('\n=== ✅ 场景搭建完成 ===\n');
    console.log('📋 场景配置:');
    console.log('  ┌──────────────────────────────────────┐');
    console.log('  │  [相机]←支架                         │');
    console.log('  │      ↓                               │');
    console.log('  │  [工件]→[工件]→[工件]  [机器人]      │');
    console.log('  │  ──────────────────                  │');
    console.log('  │     输送线 (3000×600mm)              │');
    console.log('  │                                      │');
    console.log('  │              [A] [B] [不良品]        │');
    console.log('  └──────────────────────────────────────┘');
    
    console.log('\n💡 下一步建议:');
    console.log('  1. 在 Kunwu Builder 中查看场景');
    console.log('  2. 添加机器人模型（替换基座）');
    console.log('  3. 配置行为：输送线运动 + 机器人抓取');
    console.log('  4. 添加相机拍照和视觉定位');
    
  } catch (err) {
    console.error('\n❌ 错误:', err.message);
    console.error(err.stack);
  }
}

buildScene();
