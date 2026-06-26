#!/usr/bin/env node

/**
 * 下料分拣场景搭建脚本
 * 包含：输送线、机器人、相机、料框、安全围栏
 */

import { callAPI } from './kunwu-tool.js';

const BASE_URL = process.env.KUNWU_API_URL || 'http://100.85.119.45:16888';

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function buildPickSortScene() {
  console.log('=== 🏭 下料分拣场景搭建 ===\n');
  
  try {
    // 0. 重置场景
    console.log('0️⃣ 重置场景...');
    await callAPI('/ResetScene', {});
    await sleep(2000);
    
    // 1. 查询模型库
    console.log('\n1️⃣ 查询云端模型库...');
    
    // 输送线
    const conveyorSearch = await callAPI('/model/library/remote', { searchKey: '输送' });
    console.log('输送线模型:', conveyorSearch?.data?.rows?.length || 0, '个');
    if (conveyorSearch?.data?.rows?.length > 0) {
      console.log('  -', conveyorSearch.data.rows[0].name, `(ID: ${conveyorSearch.data.rows[0].id})`);
    }
    
    // 机器人
    const robotSearch = await callAPI('/model/library/remote', { searchKey: '机器人' });
    console.log('机器人模型:', robotSearch?.data?.rows?.length || 0, '个');
    if (robotSearch?.data?.rows?.length > 0) {
      console.log('  -', robotSearch.data.rows[0].name, `(ID: ${robotSearch.data.rows[0].id})`);
    }
    
    // 料框
    const binSearch = await callAPI('/model/library/remote', { searchKey: '箱子' });
    console.log('料箱模型:', binSearch?.data?.rows?.length || 0, '个');
    if (binSearch?.data?.rows?.length > 0) {
      console.log('  -', binSearch.data.rows[0].name, `(ID: ${binSearch.data.rows[0].id})`);
    }
    
    // 相机
    const cameraSearch = await callAPI('/model/library/remote', { searchKey: '相机' });
    console.log('相机模型:', cameraSearch?.data?.rows?.length || 0, '个');
    
    // 2. 下载并创建基础设备
    console.log('\n2️⃣ 下载并创建设备...');
    
    const modelsToCreate = [
      {
        id: conveyorSearch?.data?.rows?.[0]?.id || '皮带输送线',
        rename: 'MainConveyor',
        position: [0, 0, 0]
      },
      {
        id: robotSearch?.data?.rows?.[0]?.id || '工业机器人_6 轴',
        rename: 'Robot_Arm',
        position: [1500, 500, 0]
      },
      {
        id: binSearch?.data?.rows?.[0]?.id || '料框',
        rename: 'Bin_A',
        position: [2000, -500, 0]
      },
      {
        id: binSearch?.data?.rows?.[0]?.id || '料框',
        rename: 'Bin_B',
        position: [2000, 0, 0]
      },
      {
        id: binSearch?.data?.rows?.[0]?.id || '料框',
        rename: 'Bin_Reject',
        position: [2000, 500, 0]
      }
    ];
    
    // 并行下载
    const tasks = [];
    for (const model of modelsToCreate) {
      console.log(`  创建 ${model.rename}...`);
      const result = await callAPI('/model/download', {
        id: model.id,
        rename: model.rename,
        position: model.position,
        createInScene: true
      });
      if (result?.data?.taskId) {
        tasks.push(result.data.taskId);
        console.log(`    ✓ 任务 ID: ${result.data.taskId}`);
      }
    }
    
    // 等待所有任务完成
    console.log('\n3️⃣ 等待模型创建完成...');
    for (const taskId of tasks) {
      let done = false;
      while (!done) {
        const status = await callAPI('/task/query', { taskId });
        if (status?.data?.done) {
          done = true;
          if (status.data.resultCode === 200) {
            console.log(`  ✓ ${taskId} 完成`);
          } else {
            console.log(`  ✗ ${taskId} 失败：${status.data.resultMsg}`);
          }
        } else {
          await sleep(1000);
        }
      }
    }
    
    // 4. 创建相机支架（用参数化方块）
    console.log('\n4️⃣ 创建相机支架...');
    const cameraStand = await callAPI('/model/create', {
      id: '方形',
      rename: 'CameraStand',
      position: [1500, -300, 0],
      parameterizationCfg: [
        { type: 0, value: 100 },  // 宽度
        { type: 1, value: 100 },  // 深度
        { type: 2, value: 1800 }  // 高度
      ]
    });
    console.log('  相机支架创建:', cameraStand?.data?.taskId);
    
    // 5. 创建相机（用小型方块模拟）
    const camera = await callAPI('/model/create', {
      id: '方形',
      rename: 'Camera_3D',
      position: [1500, -300, 1700],
      eulerAngle: [90, 0, 0],  // 向下俯视
      parameterizationCfg: [
        { type: 0, value: 150 },
        { type: 1, value: 100 },
        { type: 2, value: 80 }
      ]
    });
    console.log('  相机创建:', camera?.data?.taskId);
    
    // 6. 创建安全围栏（用多个柱子）
    console.log('\n5️⃣ 创建安全围栏...');
    const fencePosts = [
      { name: 'Fence_1', pos: [-500, -800, 0] },
      { name: 'Fence_2', pos: [3500, -800, 0] },
      { name: 'Fence_3', pos: [3500, 1200, 0] },
      { name: 'Fence_4', pos: [-500, 1200, 0] }
    ];
    
    for (const post of fencePosts) {
      await callAPI('/model/create', {
        id: '方形',
        rename: post.name,
        position: post.pos,
        parameterizationCfg: [
          { type: 0, value: 50 },
          { type: 1, value: 50 },
          { type: 2, value: 2000 }
        ]
      });
    }
    console.log('  ✓ 4 个围栏立柱创建完成');
    
    // 7. 获取场景树
    console.log('\n6️⃣ 获取场景层级树...');
    const sceneTree = await callAPI('/models/tree', {});
    console.log('  场景模型总数:', sceneTree?.data?.list?.length || 0);
    
    // 8. 切换到行为模式
    console.log('\n7️⃣ 切换到行为信号模式...');
    const modeResult = await callAPI('/ChangeMode', { mode: 1 });
    console.log('  模式切换:', modeResult?.data?.resultMsg);
    
    console.log('\n=== ✅ 场景搭建完成 ===');
    console.log('\n📋 场景配置:');
    console.log('  - 输送线：MainConveyor (来料输入)');
    console.log('  - 机器人：Robot_Arm (6 轴，分拣作业)');
    console.log('  - 料框：Bin_A, Bin_B, Bin_Reject (3 个分拣区)');
    console.log('  - 相机：Camera_3D (视觉定位，高度 1.7m)');
    console.log('  - 围栏：4 个立柱 (安全区域 4m×2m)');
    
  } catch (err) {
    console.error('\n❌ 错误:', err.message);
    console.error(err.stack);
  }
}

buildPickSortScene();
