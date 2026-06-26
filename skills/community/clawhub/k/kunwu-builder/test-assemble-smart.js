#!/usr/bin/env node

/**
 * 智能装配测试 - 根据 ModelType 自动识别装配关系
 * 日期：2026-03-16
 * 
 * 装配规则：
 * 1. 相机 -> 相机支架
 * 2. 机器人相机 -> 机器人抓手上的支架 -> 机器人 -> 机器人底座/地轨
 * 3. 桁架相机 -> 桁架抓手 -> 桁架两个自由臂
 */

import {
  createModel,
  getAllModelInfo,
  getModelInfo,
  setParent,
  destroyObject,
  waitForTask
} from './kunwu-tool.js';

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * 模型类型识别
 */
const ModelType = {
  CAMERA: 'camera',
  CAMERA_MOUNT: 'camera_mount',
  ROBOT: 'robot',
  ROBOT_CAMERA: 'robot_camera',
  ROBOT_GRIPPER: 'robot_gripper',
  ROBOT_BASE: 'robot_base',
  ROBOT_RAIL: 'robot_rail',
  GANTRY: 'gantry',
  GANTRY_GRIPPER: 'gantry_gripper',
  GANTRY_ARM: 'gantry_arm',
  OTHER: 'other'
};

/**
 * 根据模型名称识别类型
 */
function identifyModelType(modelName) {
  const name = modelName.toLowerCase();
  
  // 相机相关
  if (name.includes('camera') || name.includes('相机')) {
    if (name.includes('robot') || name.includes('机器人')) {
      return ModelType.ROBOT_CAMERA;
    }
    if (name.includes('gantry') || name.includes('桁架')) {
      return ModelType.GANTRY;
    }
    return ModelType.CAMERA;
  }
  
  // 支架相关
  if (name.includes('mount') || name.includes('支架') || name.includes('bracket')) {
    if (name.includes('camera') || name.includes('相机')) {
      return ModelType.CAMERA_MOUNT;
    }
    if (name.includes('gripper') || name.includes('抓手')) {
      return ModelType.ROBOT_GRIPPER;
    }
    return ModelType.CAMERA_MOUNT;
  }
  
  // 机器人相关
  if (name.includes('robot') || name.includes('机器人') || name.includes('arm') || name.includes('机械臂')) {
    return ModelType.ROBOT;
  }
  
  // 抓手相关
  if (name.includes('gripper') || name.includes('抓手') || name.includes('end effector')) {
    return ModelType.ROBOT_GRIPPER;
  }
  
  // 底座/地轨相关
  if (name.includes('base') || name.includes('底座') || name.includes('rail') || name.includes('地轨')) {
    return ModelType.ROBOT_BASE;
  }
  
  // 桁架相关
  if (name.includes('gantry') || name.includes('桁架')) {
    return ModelType.GANTRY;
  }
  
  // 桁架手臂
  if (name.includes('arm') && name.includes('gantry')) {
    return ModelType.GANTRY_ARM;
  }
  
  return ModelType.OTHER;
}

/**
 * 获取装配目标（根据规则）
 */
function getAssemblyTarget(childType, allModels) {
  switch (childType) {
    case ModelType.CAMERA:
      // 相机 -> 相机支架
      return allModels.find(m => identifyModelType(m.modelName) === ModelType.CAMERA_MOUNT);
    
    case ModelType.ROBOT_CAMERA:
      // 机器人相机 -> 机器人抓手上的支架
      return allModels.find(m => 
        identifyModelType(m.modelName) === ModelType.CAMERA_MOUNT ||
        identifyModelType(m.modelName) === ModelType.ROBOT_GRIPPER
      );
    
    case ModelType.ROBOT_GRIPPER:
      // 机器人抓手 -> 机器人
      return allModels.find(m => identifyModelType(m.modelName) === ModelType.ROBOT);
    
    case ModelType.ROBOT:
      // 机器人 -> 机器人底座/地轨
      return allModels.find(m => 
        identifyModelType(m.modelName) === ModelType.ROBOT_BASE
      );
    
    case ModelType.GANTRY:
      // 桁架相机 -> 桁架抓手
      return allModels.find(m => identifyModelType(m.modelName) === ModelType.GANTRY_GRIPPER);
    
    case ModelType.GANTRY_GRIPPER:
      // 桁架抓手 -> 桁架两个自由臂
      return allModels.find(m => identifyModelType(m.modelName) === ModelType.GANTRY_ARM);
    
    default:
      return null;
  }
}

/**
 * 通过 modelName 获取 modelId
 */
async function getModelIdByName(modelName) {
  const allInfo = await getAllModelInfo();
  const models = allInfo.data?.models || [];
  const matched = models.filter(m => m.modelName === modelName);
  if (matched.length === 0) throw new Error(`Model not found: ${modelName}`);
  const model = matched[matched.length - 1];
  return model.modelId || model.id;
}

/**
 * 智能装配主函数
 */
async function smartAssemble() {
  const results = { passed: [], failed: [], warnings: [] };
  
  console.log('🧪 智能装配测试 - 根据 ModelType 自动识别\n');
  
  try {
    // 清理之前的测试模型
    console.log('🧹 清理之前的测试模型...');
    let allInfo = await getAllModelInfo();
    let models = allInfo.data?.models || [];
    const testModels = models.filter(m => 
      m.modelName?.includes('测试_') || m.modelName?.includes('装配_')
    );
    if (testModels.length > 0) {
      const ids = testModels.map(m => m.modelId || m.id);
      await destroyObject({ ids });
      await sleep(1000);
      console.log(`   ✅ 清理了 ${testModels.length} 个模型\n`);
    }
    
    // ========== 场景 1: 相机 -> 相机支架 ==========
    console.log('📷 场景 1: 相机 -> 相机支架');
    
    // 创建相机支架
    const mountResult = await createModel({
      id: '方形',
      rename: '测试_相机支架',
      position: [0, 100, 200],
      parameterizationCfg: { length: 50, width: 50, height: 20 }
    });
    await waitForTask(mountResult.data.taskId);
    await sleep(500);
    const mountId = await getModelIdByName('测试_相机支架');
    console.log(`   ✅ 创建相机支架：${mountId}`);
    results.passed.push('创建相机支架');
    
    // 创建相机
    const cameraResult = await createModel({
      id: '方形',
      rename: '测试_相机',
      position: [0, 100, 250],
      parameterizationCfg: { length: 30, width: 30, height: 30 }
    });
    await waitForTask(cameraResult.data.taskId);
    await sleep(500);
    const cameraId = await getModelIdByName('测试_相机');
    console.log(`   ✅ 创建相机：${cameraId}`);
    results.passed.push('创建相机');
    
    // 执行装配：相机 -> 支架
    const cameraType = identifyModelType('测试_相机');
    console.log(`   🔍 识别相机类型：${cameraType}`);
    
    allInfo = await getAllModelInfo();
    models = allInfo.data?.models || [];
    const target = getAssemblyTarget(cameraType, models);
    
    if (target) {
      console.log(`   🎯 装配目标：${target.modelName} (${target.modelId})`);
      
      const setResult = await setParent({
        childId: cameraId,
        childUseModeId: true,
        parentId: target.modelId,
        parentUseModeId: true
      });
      
      if (setResult.code === 200) {
        console.log(`   ✅ 相机 -> 支架 装配成功`);
        results.passed.push('相机->支架装配');
      } else {
        console.log(`   ❌ 装配失败：${setResult.msg}`);
        results.failed.push(`相机->支架：${setResult.msg}`);
      }
    } else {
      console.log(`   ⚠️ 未找到装配目标`);
      results.warnings.push('相机未找到支架');
    }
    
    await sleep(500);
    
    // ========== 场景 2: 机器人完整层级 ==========
    console.log('\n🤖 场景 2: 机器人完整层级');
    console.log('   规则：机器人相机 -> 抓手支架 -> 机器人 -> 底座');
    
    // 创建底座
    const baseResult = await createModel({
      id: '方形',
      rename: '测试_机器人底座',
      position: [500, 0, 0],
      parameterizationCfg: { length: 300, width: 300, height: 50 }
    });
    await waitForTask(baseResult.data.taskId);
    await sleep(500);
    const baseId = await getModelIdByName('测试_机器人底座');
    console.log(`   ✅ 创建底座：${baseId}`);
    results.passed.push('创建机器人底座');
    
    // 创建机器人
    const robotResult = await createModel({
      id: '方形',
      rename: '测试_机器人',
      position: [500, 0, 100],
      parameterizationCfg: { length: 100, width: 100, height: 200 }
    });
    await waitForTask(robotResult.data.taskId);
    await sleep(500);
    const robotId = await getModelIdByName('测试_机器人');
    console.log(`   ✅ 创建机器人：${robotId}`);
    results.passed.push('创建机器人');
    
    // 创建抓手支架
    const gripperMountResult = await createModel({
      id: '方形',
      rename: '测试_抓手支架',
      position: [500, 0, 320],
      parameterizationCfg: { length: 80, width: 80, height: 30 }
    });
    await waitForTask(gripperMountResult.data.taskId);
    await sleep(500);
    const gripperMountId = await getModelIdByName('测试_抓手支架');
    console.log(`   ✅ 创建抓手支架：${gripperMountId}`);
    results.passed.push('创建抓手支架');
    
    // 创建机器人相机
    const robotCameraResult = await createModel({
      id: '方形',
      rename: '测试_机器人相机',
      position: [500, 0, 370],
      parameterizationCfg: { length: 40, width: 40, height: 40 }
    });
    await waitForTask(robotCameraResult.data.taskId);
    await sleep(500);
    const robotCameraId = await getModelIdByName('测试_机器人相机');
    console.log(`   ✅ 创建机器人相机：${robotCameraId}`);
    results.passed.push('创建机器人相机');
    
    await sleep(500);
    
    // 执行层级装配
    console.log('\n   🔧 执行层级装配...');
    
    // 1. 机器人 -> 底座
    const r1 = await setParent({
      childId: robotId,
      childUseModeId: true,
      parentId: baseId,
      parentUseModeId: true
    });
    if (r1.code === 200) {
      console.log(`   ✅ 机器人 -> 底座`);
      results.passed.push('机器人->底座装配');
    }
    
    // 2. 抓手支架 -> 机器人
    const r2 = await setParent({
      childId: gripperMountId,
      childUseModeId: true,
      parentId: robotId,
      parentUseModeId: true
    });
    if (r2.code === 200) {
      console.log(`   ✅ 抓手支架 -> 机器人`);
      results.passed.push('抓手支架->机器人装配');
    }
    
    // 3. 机器人相机 -> 抓手支架
    const r3 = await setParent({
      childId: robotCameraId,
      childUseModeId: true,
      parentId: gripperMountId,
      parentUseModeId: true
    });
    if (r3.code === 200) {
      console.log(`   ✅ 机器人相机 -> 抓手支架`);
      results.passed.push('机器人相机->抓手支架装配');
    }
    
    await sleep(500);
    
    // ========== 验证层级关系 ==========
    console.log('\n🔍 验证层级关系...');
    const cameraInfo = await getModelInfo({ id: robotCameraId, useModeId: true });
    console.log(`   机器人相机父节点：${cameraInfo.data?.parentName || 'null'}`);
    
    if (cameraInfo.data?.parentName) {
      console.log(`   ✅ 层级关系验证成功`);
      results.passed.push('层级关系验证');
    } else {
      console.log(`   ⚠️ 层级关系未建立`);
      results.warnings.push('层级关系验证失败');
    }
    
  } catch (error) {
    console.log(`\n❌ 测试异常：${error.message}`);
    results.failed.push(`测试异常：${error.message}`);
  }
  
  // 输出报告
  console.log('\n' + '='.repeat(60));
  console.log('📊 测试报告汇总');
  console.log('='.repeat(60));
  console.log(`✅ 通过：${results.passed.length}`);
  results.passed.forEach(item => console.log(`   - ${item}`));
  
  if (results.failed.length > 0) {
    console.log(`\n❌ 失败：${results.failed.length}`);
    results.failed.forEach(item => console.log(`   - ${item}`));
  }
  
  if (results.warnings.length > 0) {
    console.log(`\n⚠️ 警告：${results.warnings.length}`);
    results.warnings.forEach(item => console.log(`   - ${item}`));
  }
  
  console.log('\n' + '='.repeat(60));
  
  return results;
}

smartAssemble().then(results => {
  process.exit(results.failed.length > 0 ? 1 : 0);
});
