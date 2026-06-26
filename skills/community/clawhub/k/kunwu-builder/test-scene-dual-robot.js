#!/usr/bin/env node

/**
 * 测试：双机器人工作站场景搭建（带托盘布局）
 * 使用统一的 /model/create + checkFromCloud:true 机制
 * 
 * 需求：
 * 1. 输送线：辊床_01，参数化 (长=7940, 宽=4340, 高=708)
 * 2. 双机器人：M900iB_280L × 2，对称放置，底座 方形底座_02 (1000×1000×515)
 * 3. 吸盘：吸盘_10 × 2，装配在机器人上
 * 4. 托盘：托盘_07 × 4，分布在两台机器人前后两侧
 */

import {
  createModel,
  setModelPose,
  assemble,
  getAllModelInfo,
  destroyObject
} from './kunwu-tool.js';

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function getModelIdByName(modelName) {
  const allInfo = await getAllModelInfo();
  const models = allInfo.data?.models || [];
  const matched = models.filter(m => m.modelName === modelName);
  if (matched.length === 0) throw new Error(`Model not found: ${modelName}`);
  const model = matched[matched.length - 1];
  return model.modelId || model.id;
}

async function cleanupTestModels() {
  console.log('🧹 清理之前的测试模型...');
  const allInfo = await getAllModelInfo();
  const models = allInfo.data?.models || [];
  
  const testPrefixes = ['辊床', '底座', '机器人', '吸盘', '托盘'];
  const toDelete = models.filter(m => 
    testPrefixes.some(prefix => m.modelName?.includes(prefix))
  );
  
  for (const model of toDelete) {
    try {
      await destroyObject({ id: model.modelId, useModeId: true });
      console.log(`   ✓ 删除：${model.modelName}`);
    } catch (e) {
      console.log(`   ⚠ 删除失败：${model.modelName}`);
    }
  }
  await sleep(1000);
}

async function buildScene() {
  const results = { passed: [], failed: [] };
  
  try {
    // ========== 1. 创建输送线（辊床_01） ==========
    console.log('\n📦 步骤 1: 创建输送线（辊床_01）');
    await createModel({
      id: '辊床_01',
      rename: '输送线',
      position: [0, 0, 0],
      eulerAngle: [0, 0, 0],
      checkFromCloud: true
    });
    await sleep(1500);
    
    // 设置参数化（必须同时传 position + eulerAngle + parameterizationCfg！）
    console.log('   ⚙️  设置参数化：长=7940, 宽=4340, 高=708');
    const conveyorId = await getModelIdByName('输送线');
    await setModelPose({
      id: conveyorId,
      useModeId: true,
      position: [0, 0, 0],       // 必须传！
      eulerAngle: [0, 0, 0],     // 必须传！
      parameterizationCfg: [
        { type: 0, value: 7940 },  // 长
        { type: 1, value: 4340 },  // 宽
        { type: 2, value: 708 }    // 高
      ]
    });
    console.log('   ✅ 输送线创建完成');
    results.passed.push('输送线');
    
    // ========== 2. 创建底座 × 2 ==========
    console.log('\n📦 步骤 2: 创建底座（方形底座_02 × 2）');
    
    // 右侧底座
    await createModel({
      id: '方形底座_02',
      rename: '底座_右',
      position: [0, 2500, 0],
      eulerAngle: [0, 0, 0],
      checkFromCloud: true,
      parameterizationCfg: [
        { type: 0, value: 1000 },
        { type: 1, value: 1000 },
        { type: 2, value: 515 }
      ]
    });
    console.log('   ✓ 底座_右 创建中...');
    
    // 左侧底座
    await createModel({
      id: '方形底座_02',
      rename: '底座_左',
      position: [0, -2500, 0],
      eulerAngle: [0, 0, 0],
      checkFromCloud: true,
      parameterizationCfg: [
        { type: 0, value: 1000 },
        { type: 1, value: 1000 },
        { type: 2, value: 515 }
      ]
    });
    console.log('   ✓ 底座_左 创建中...');
    await sleep(1500);
    console.log('   ✅ 底座创建完成');
    results.passed.push('底座×2');
    
    // ========== 3. 创建机器人 × 2 ==========
    console.log('\n📦 步骤 3: 创建机器人（M900iB_280L × 2）');
    
    // 右侧机器人
    await createModel({
      id: 'M900iB_280L',
      rename: '机器人_右',
      position: [0, 2500, 515],  // 放在底座上
      eulerAngle: [0, 0, 0],
      checkFromCloud: true
    });
    console.log('   ✓ 机器人_右 创建中...');
    
    // 左侧机器人
    await createModel({
      id: 'M900iB_280L',
      rename: '机器人_左',
      position: [0, -2500, 515],  // 放在底座上
      eulerAngle: [0, 0, 0],
      checkFromCloud: true
    });
    console.log('   ✓ 机器人_左 创建中...');
    await sleep(1500);
    console.log('   ✅ 机器人创建完成');
    results.passed.push('机器人×2');
    
    // ========== 4. 创建吸盘 × 2 ==========
    console.log('\n📦 步骤 4: 创建吸盘（吸盘_10 × 2）');
    
    // 右侧吸盘
    await createModel({
      id: '吸盘_10',
      rename: '吸盘_右',
      position: [0, 2500, 2000],  // 临时位置，后续装配
      eulerAngle: [0, 0, 0],
      checkFromCloud: true
    });
    console.log('   ✓ 吸盘_右 创建中...');
    
    // 左侧吸盘
    await createModel({
      id: '吸盘_10',
      rename: '吸盘_左',
      position: [0, -2500, 2000],  // 临时位置，后续装配
      eulerAngle: [0, 0, 0],
      checkFromCloud: true
    });
    console.log('   ✓ 吸盘_左 创建中...');
    await sleep(1500);
    console.log('   ✅ 吸盘创建完成');
    results.passed.push('吸盘×2');
    
    // ========== 5. 创建托盘 × 4 ==========
    console.log('\n📦 步骤 5: 创建托盘（托盘_07 × 4）');
    
    // 托盘位置布局（相对于机器人）
    // 机器人_右 (Y=2500): 前侧 Y=4500, 后侧 Y=500
    // 机器人_左 (Y=-2500): 前侧 Y=-500, 后侧 Y=-4500
    const trayPositions = [
      { name: '托盘_右前', position: [3000, 4500, 0] },   // 机器人_右 前侧
      { name: '托盘_右后', position: [3000, 500, 0] },    // 机器人_右 后侧
      { name: '托盘_左前', position: [3000, -500, 0] },   // 机器人_左 前侧
      { name: '托盘_左后', position: [3000, -4500, 0] }   // 机器人_左 后侧
    ];
    
    for (const tray of trayPositions) {
      await createModel({
        id: '托盘_07',
        rename: tray.name,
        position: tray.position,
        eulerAngle: [0, 0, 0],
        checkFromCloud: true
      });
      console.log(`   ✓ ${tray.name} 创建中...`);
    }
    await sleep(1500);
    console.log('   ✅ 托盘创建完成');
    results.passed.push('托盘×4');
    
    // ========== 6. 装配 ==========
    console.log('\n🔧 步骤 6: 执行装配');
    
    // 获取所有模型 ID
    const baseRightId = await getModelIdByName('底座_右');
    const baseLeftId = await getModelIdByName('底座_左');
    const robotRightId = await getModelIdByName('机器人_右');
    const robotLeftId = await getModelIdByName('机器人_左');
    const gripperRightId = await getModelIdByName('吸盘_右');
    const gripperLeftId = await getModelIdByName('吸盘_左');
    
    // 吸盘 → 机器人
    console.log('   🔩 装配：吸盘_右 → 机器人_右');
    await assemble({
      childId: gripperRightId,
      parentId: robotRightId,
      assemblePosIndex: 0,
      useModeId: true
    });
    
    console.log('   🔩 装配：吸盘_左 → 机器人_左');
    await assemble({
      childId: gripperLeftId,
      parentId: robotLeftId,
      assemblePosIndex: 0,
      useModeId: true
    });
    
    // 机器人 → 底座
    console.log('   🔩 装配：机器人_右 → 底座_右');
    await assemble({
      childId: robotRightId,
      parentId: baseRightId,
      assemblePosIndex: 0,
      useModeId: true
    });
    
    console.log('   🔩 装配：机器人_左 → 底座_左');
    await assemble({
      childId: robotLeftId,
      parentId: baseLeftId,
      assemblePosIndex: 0,
      useModeId: true
    });
    
    console.log('   ✅ 装配完成');
    results.passed.push('装配');
    
    // ========== 最终统计 ==========
    console.log('\n' + '═'.repeat(50));
    console.log('✅ 场景搭建完成！');
    console.log('═'.repeat(50));
    console.log('📊 统计:');
    console.log(`   输送线 × 1`);
    console.log(`   底座 × 2`);
    console.log(`   机器人 × 2`);
    console.log(`   吸盘 × 2`);
    console.log(`   托盘 × 4`);
    console.log(`   总计：11 个模型`);
    console.log('═'.repeat(50));
    
  } catch (error) {
    console.log(`\n❌ 错误：${error.message}`);
    results.failed.push(error.message);
  }
  
  return results;
}

// ========== 主流程 ==========
async function main() {
  console.log('🏗️  双机器人工作站场景搭建测试');
  console.log('使用机制：/model/create + checkFromCloud:true');
  console.log('═'.repeat(50));
  
  await cleanupTestModels();
  const results = await buildScene();
  
  if (results.failed.length > 0) {
    console.log('\n⚠️  失败项:');
    results.failed.forEach(f => console.log(`   - ${f}`));
    process.exit(1);
  }
}

main().catch(console.error);
