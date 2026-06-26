#!/usr/bin/env node

/**
 * 下料分拣场景搭建脚本（简化版 - 使用基础几何体）
 */

import { callAPI } from './kunwu-tool.js';

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

async function buildScene() {
  console.log('=== 🏭 下料分拣场景搭建（简化版）===\n');
  
  try {
    // 0. 重置场景
    console.log('0️⃣ 重置场景...');
    await callAPI('/ResetScene', {});
    await sleep(2000);
    
    // 1. 创建输送线（用长方块模拟）
    console.log('\n1️⃣ 创建输送线...');
    const conveyor = await callAPI('/model/download', {
      id: '方形',
      rename: 'Conveyor',
      position: [0, 0, 0],
      createInScene: true
    });
    console.log('  任务 ID:', conveyor?.data?.taskId);
    
    // 等待完成并设置尺寸
    if (conveyor?.data?.taskId) {
      await waitForTask(conveyor.data.taskId);
      // 设置输送线尺寸：长 3000mm, 宽 600mm, 高 200mm
      await callAPI('/model/set_pose', {
        id: 'Conveyor',
        useModeId: false,
        parameterizationCfg: [
          { type: 0, value: 3000 },
          { type: 1, value: 600 },
          { type: 2, value: 200 }
        ]
      });
      console.log('  ✓ 输送线创建完成 (3000×600×200mm)');
    }
    
    // 2. 创建机器人基座
    console.log('\n2️⃣ 创建机器人...');
    const robotBase = await callAPI('/model/download', {
      id: '方形',
      rename: 'RobotBase',
      position: [1500, 500, 0],
      createInScene: true
    });
    if (robotBase?.data?.taskId) {
      await waitForTask(robotBase.data.taskId);
      await callAPI('/model/set_pose', {
        id: 'RobotBase',
        useModeId: false,
        parameterizationCfg: [
          { type: 0, value: 300 },
          { type: 1, value: 300 },
          { type: 2, value: 50 }
        ]
      });
      console.log('  ✓ 机器人基座完成');
    }
    
    // 创建机器人手臂（用多个方块）
    const arm1 = await callAPI('/model/download', {
      id: '方形',
      rename: 'RobotArm1',
      position: [1500, 500, 50],
      createInScene: true
    });
    if (arm1?.data?.taskId) {
      await waitForTask(arm1.data.taskId);
      await callAPI('/model/set_pose', {
        id: 'RobotArm1',
        useModeId: false,
        parameterizationCfg: [
          { type: 0, value: 100 },
          { type: 1, value: 100 },
          { type: 2, value: 400 }
        ]
      });
    }
    
    // 3. 创建料框（3 个）
    console.log('\n3️⃣ 创建分拣料框...');
    const bins = [
      { name: 'Bin_A', pos: [2500, -400, 0] },
      { name: 'Bin_B', pos: [2500, 0, 0] },
      { name: 'Bin_Reject', pos: [2500, 400, 0] }
    ];
    
    for (const bin of bins) {
      const result = await callAPI('/model/download', {
        id: '方形',
        rename: bin.name,
        position: bin.pos,
        createInScene: true
      });
      if (result?.data?.taskId) {
        await waitForTask(result.data.taskId);
        await callAPI('/model/set_pose', {
          id: bin.name,
          useModeId: false,
          parameterizationCfg: [
            { type: 0, value: 400 },
            { type: 1, value: 400 },
            { type: 2, value: 300 }
          ]
        });
        console.log('  ✓ ' + bin.name + ' 完成');
      }
    }
    
    // 4. 创建相机支架
    console.log('\n4️⃣ 创建相机支架...');
    const camStand = await callAPI('/model/download', {
      id: '方形',
      rename: 'CameraStand',
      position: [1500, -300, 0],
      createInScene: true
    });
    if (camStand?.data?.taskId) {
      await waitForTask(camStand.data.taskId);
      await callAPI('/model/set_pose', {
        id: 'CameraStand',
        useModeId: false,
        parameterizationCfg: [
          { type: 0, value: 100 },
          { type: 1, value: 100 },
          { type: 2, value: 1800 }
        ]
      });
      console.log('  ✓ 相机支架完成 (高 1.8m)');
    }
    
    // 创建相机
    const camera = await callAPI('/model/download', {
      id: '方形',
      rename: 'Camera',
      position: [1500, -300, 1750],
      eulerAngle: [90, 0, 0],
      createInScene: true
    });
    if (camera?.data?.taskId) {
      await waitForTask(camera.data.taskId);
      await callAPI('/model/set_pose', {
        id: 'Camera',
        useModeId: false,
        parameterizationCfg: [
          { type: 0, value: 150 },
          { type: 1, value: 100 },
          { type: 2, value: 80 }
        ]
      });
      console.log('  ✓ 相机完成 (俯视)');
    }
    
    // 5. 创建工件（放在输送线上）
    console.log('\n5️⃣ 创建工件...');
    const parts = [
      { name: 'Part_1', pos: [500, 0, 220] },
      { name: 'Part_2', pos: [1000, 0, 220] },
      { name: 'Part_3', pos: [1500, 0, 220] }
    ];
    
    for (const part of parts) {
      const result = await callAPI('/model/download', {
        id: '方形',
        rename: part.name,
        position: part.pos,
        createInScene: true
      });
      if (result?.data?.taskId) {
        await waitForTask(result.data.taskId);
        await callAPI('/model/set_pose', {
          id: part.name,
          useModeId: false,
          parameterizationCfg: [
            { type: 0, value: 100 },
            { type: 1, value: 100 },
            { type: 2, value: 100 }
          ]
        });
      }
    }
    console.log('  ✓ 3 个工件创建完成');
    
    // 6. 获取场景树
    console.log('\n6️⃣ 获取场景层级...');
    const tree = await callAPI('/models/tree', {});
    console.log('  场景模型总数:', tree?.data?.list?.length || 0);
    
    // 7. 切换到行为模式
    console.log('\n7️⃣ 切换模式...');
    const modeResult = await callAPI('/ChangeMode', { mode: 1 });
    console.log('  当前模式:', modeResult?.data?.resultMsg);
    
    console.log('\n=== ✅ 场景搭建完成 ===\n');
    console.log('📋 场景配置:');
    console.log('  ┌──────────────────────────────────────┐');
    console.log('  │  [相机]←支架                         │');
    console.log('  │      ↓                               │');
    console.log('  │  [工件]→[工件]→[工件]  [机器人]      │');
    console.log('  │  ──────────────────                  │');
    console.log('  │     输送线 (3000mm)                  │');
    console.log('  │                                      │');
    console.log('  │              [A] [B] [不良品]        │');
    console.log('  └──────────────────────────────────────┘');
    
  } catch (err) {
    console.error('\n❌ 错误:', err.message);
    console.error(err.stack);
  }
}

async function waitForTask(taskId) {
  for (let i = 0; i < 30; i++) {
    const status = await callAPI('/task/query', { taskId });
    if (status?.data?.done) {
      if (status.data.resultCode === 200) {
        return status.data;
      } else {
        throw new Error('Task failed: ' + status.data.resultMsg);
      }
    }
    await sleep(1000);
  }
  throw new Error('Task timeout');
}

buildScene();
