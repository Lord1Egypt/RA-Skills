#!/usr/bin/env node

/**
 * 下料分拣场景 - 最终版本
 * 使用已验证的 API：model/download（带 position 参数）
 */

import { callAPI } from './kunwu-tool.js';

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

async function buildScene() {
  console.log('=== 🏭 下料分拣场景搭建 ===\n');
  console.log('场景布局:');
  console.log('  ┌────────────────────────────────────────┐');
  console.log('  │           [相机支架] [相机]            │');
  console.log('  │               ↓                        │');
  console.log('  │  [Part1]→[Part2]→[Part3]   [Robot]    │');
  console.log('  │  ────────────────────────              │');
  console.log('  │        输送线 (3000mm)                 │');
  console.log('  │                                        │');
  console.log('  │                 [A] [B] [Reject]       │');
  console.log('  └────────────────────────────────────────┘\n');
  
  try {
    // 0. 重置场景
    console.log('0️⃣ 重置场景...');
    await callAPI('/ResetScene', {});
    await sleep(3000);
    console.log('  ✓ 场景已重置\n');
    
    // 1. 创建输送线（长方块）
    console.log('1️⃣ 创建输送线...');
    await callAPI('/model/download', {
      id: '方形',
      rename: 'Conveyor',
      position: [0, 0, 0],
      parameterizationCfg: [
        { type: 0, value: 3000 },  // 长 3000mm
        { type: 1, value: 600 },   // 宽 600mm
        { type: 2, value: 200 }    // 高 200mm
      ],
      createInScene: true
    });
    console.log('  ✓ 输送线创建请求已发送 (3000×600×200mm)\n');
    await sleep(3000);
    
    // 2. 创建机器人基座
    console.log('2️⃣ 创建机器人基座...');
    await callAPI('/model/download', {
      id: '方形',
      rename: 'RobotBase',
      position: [1500, 600, 0],
      parameterizationCfg: [
        { type: 0, value: 400 },
        { type: 1, value: 400 },
        { type: 2, value: 100 }
      ],
      createInScene: true
    });
    console.log('  ✓ 机器人基座创建请求已发送\n');
    await sleep(3000);
    
    // 3. 创建 3 个料框
    console.log('3️⃣ 创建分拣料框...');
    const bins = [
      { name: 'Bin_A', pos: [2800, -300, 0] },
      { name: 'Bin_B', pos: [2800, 0, 0] },
      { name: 'Bin_Reject', pos: [2800, 300, 0] }
    ];
    
    for (const bin of bins) {
      await callAPI('/model/download', {
        id: '方形',
        rename: bin.name,
        position: bin.pos,
        parameterizationCfg: [
          { type: 0, value: 350 },
          { type: 1, value: 350 },
          { type: 2, value: 250 }
        ],
        createInScene: true
      });
      console.log('  - ' + bin.name + ' @ ' + bin.pos.join(','));
      await sleep(1500);
    }
    console.log();
    
    // 4. 创建相机支架
    console.log('4️⃣ 创建相机支架...');
    await callAPI('/model/download', {
      id: '方形',
      rename: 'CameraStand',
      position: [1500, -400, 0],
      parameterizationCfg: [
        { type: 0, value: 100 },
        { type: 1, value: 100 },
        { type: 2, value: 1600 }
      ],
      createInScene: true
    });
    console.log('  ✓ 相机支架创建请求已发送 (高 1.6m)\n');
    await sleep(3000);
    
    // 5. 创建相机
    console.log('5️⃣ 创建相机...');
    await callAPI('/model/download', {
      id: '方形',
      rename: 'Camera',
      position: [1500, -400, 1600],
      eulerAngle: [90, 0, 0],  // 向下俯视
      parameterizationCfg: [
        { type: 0, value: 120 },
        { type: 1, value: 80 },
        { type: 2, value: 60 }
      ],
      createInScene: true
    });
    console.log('  ✓ 相机创建请求已发送 (俯视 90°)\n');
    await sleep(3000);
    
    // 6. 创建 3 个工件
    console.log('6️⃣ 创建工件...');
    const parts = [
      { name: 'Part_1', pos: [500, 0, 210] },
      { name: 'Part_2', pos: [1200, 0, 210] },
      { name: 'Part_3', pos: [2000, 0, 210] }
    ];
    
    for (const part of parts) {
      await callAPI('/model/download', {
        id: '方形',
        rename: part.name,
        position: part.pos,
        parameterizationCfg: [
          { type: 0, value: 80 },
          { type: 1, value: 80 },
          { type: 2, value: 80 }
        ],
        createInScene: true
      });
      console.log('  - ' + part.name + ' @ ' + part.pos.join(','));
      await sleep(1500);
    }
    console.log();
    
    // 7. 等待所有模型创建完成
    console.log('7️⃣ 等待模型创建完成...');
    await sleep(5000);
    
    // 8. 获取场景树
    console.log('8️⃣ 获取场景模型列表...');
    const tree = await callAPI('/models/tree', {});
    const models = tree?.data?.models || [];
    console.log('  场景模型总数:', models.length);
    models.forEach(m => {
      console.log('   - ' + m.modelName + ' (ID: ' + m.modelId.slice(0, 8) + '...)');
    });
    console.log();
    
    // 9. 切换到行为模式
    console.log('9️⃣ 切换到行为信号模式...');
    const modeResult = await callAPI('/ChangeMode', { mode: 1 });
    console.log('  模式:', modeResult?.data?.resultMsg || '切换成功');
    
    console.log('\n=== ✅ 场景搭建完成 ===\n');
    console.log('📋 设备清单:');
    console.log('  • 输送线：Conveyor (3000×600×200mm)');
    console.log('  • 机器人基座：RobotBase (400×400×100mm)');
    console.log('  • 料框：Bin_A, Bin_B, Bin_Reject (各 350×350×250mm)');
    console.log('  • 相机支架：CameraStand (高 1.6m)');
    console.log('  • 相机：Camera (俯视)');
    console.log('  • 工件：Part_1, Part_2, Part_3 (各 80mm 立方体)');
    console.log('\n💡 后续工作:');
    console.log('  1. 在 Kunwu Builder 中打开场景查看');
    console.log('  2. 替换机器人基座为真实机器人模型');
    console.log('  3. 添加输送线运动行为 (/motion/IndustrialEquipment)');
    console.log('  4. 添加机器人抓取/放置行为');
    console.log('  5. 配置相机拍照和视觉定位');
    console.log('  6. 编写分拣逻辑脚本');
    
  } catch (err) {
    console.error('\n❌ 错误:', err.message);
  }
}

buildScene();
