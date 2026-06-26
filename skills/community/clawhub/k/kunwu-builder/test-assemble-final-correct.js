#!/usr/bin/env node

/**
 * 正确的装配测试 - 使用 /model/assemble
 * 日期：2026-03-16
 * 
 * 使用本地模型库中的真实模型：
 * - Camera Bracket（相机支架）
 * - Box Sensor_Tra（桁架传感器/相机）
 */

import {
  assemble,
  createModel,
  getAllModelInfo,
  getModelInfo,
  destroyObject,
  waitForTask,
  getLocalModelLibrary
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

async function testAssemble() {
  const results = { passed: [], failed: [], warnings: [] };
  
  console.log('🧪 正确的装配测试 - 使用 /model/assemble\n');
  console.log('规则：相机 -> 相机支架（使用本地模型库）\n');
  
  try {
    // 清理之前的测试模型
    console.log('🧹 清理之前的测试模型...');
    let allInfo = await getAllModelInfo();
    let models = allInfo.data?.models || [];
    const testModels = models.filter(m => 
      m.modelName?.includes('测试_') || 
      m.modelName?.includes('装配_') ||
      m.modelName?.includes('Camera') ||
      m.modelName?.includes('Bracket')
    );
    if (testModels.length > 0) {
      const ids = testModels.map(m => m.modelId || m.id);
      console.log(`   发现 ${testModels.length} 个模型：${testModels.map(m => m.modelName).join(', ')}`);
      await destroyObject({ ids });
      await sleep(1500);
      console.log(`   ✅ 清理完成\n`);
    }
    
    // ========== 查看本地模型库 ==========
    console.log('📦 本地模型库内容:');
    const localResult = await getLocalModelLibrary({});
    const localModels = localResult.data?.models || [];
    localModels.forEach((m, i) => {
      console.log(`   ${i+1}. ${m.name}`);
    });
    console.log();
    
    // ========== 创建相机支架 ==========
    console.log('📦 创建 Camera Bracket（相机支架）...');
    await createModel({
      id: 'Camera Bracket',
      rename: '测试_相机支架',
      position: [0, 0, 0],
      checkFromCloud: true
    });
    await sleep(1000);
    const bracketId = await getModelIdByName('测试_相机支架');
    console.log(`   ✅ 相机支架创建完成：${bracketId}`);
    results.passed.push('创建相机支架');
    
    // ========== 创建相机（用 Box Sensor 代替） ==========
    console.log('\n📦 创建 Box Sensor_Tra（相机/传感器）...');
    await createModel({
      id: 'Box Sensor_Tra',
      rename: '测试_相机',
      position: [0, 0, 100],
      checkFromCloud: true
    });
    await sleep(1000);
    const sensorId = await getModelIdByName('测试_相机');
    console.log(`   ✅ 相机创建完成：${sensorId}`);
    results.passed.push('创建相机');
    
    await sleep(1000);
    
    // ========== 获取模型信息 ==========
    console.log('\n🔍 获取模型信息...');
    allInfo = await getAllModelInfo();
    models = allInfo.data?.models || [];
    
    const bracket = models.find(m => m.modelName === '测试_相机支架');
    const camera = models.find(m => m.modelName === '测试_相机');
    
    if (bracket && camera) {
      console.log(`   相机支架：${bracket.modelId}`);
      console.log(`   相机：${camera.modelId}`);
      
      // 查看模型详细信息
      const bracketInfo = await getModelInfo({ id: bracket.modelId, useModeId: true });
      console.log(`\n   相机支架信息:`);
      console.log(`     - type: ${bracketInfo.data?.type || 'N/A'}`);
      console.log(`     - hasAssemblyPositions: ${bracketInfo.data?.hasAssemblyPositions ? 'Yes' : 'No'}`);
      
    } else {
      console.log(`   ❌ 未找到模型`);
      results.failed.push('未找到下载的模型');
      return results;
    }
    
    // ========== 执行装配：相机 -> 支架 ==========
    console.log('\n🔧 执行装配：相机 -> 支架（使用 /model/assemble）');
    
    const assembleResult = await assemble({
      childId: camera.modelId,
      parentId: bracket.modelId,
      childUseModeId: true,
      parentUseModeId: true,
      assemblePosIndex: -1,  // 自动选择装配位
      replaceExisting: true
    });
    
    console.log(`\n   响应:`, JSON.stringify(assembleResult, null, 2));
    
    if (assembleResult.code === 200 || assembleResult.code === 202) {
      console.log(`   ✅ /model/assemble 请求成功`);
      results.passed.push('/model/assemble 基本调用');
      
      if (assembleResult.data?.taskId) {
        console.log(`   ⏳ 等待装配任务完成...`);
        const waitResult = await waitForTask(assembleResult.data.taskId);
        console.log(`   任务结果:`, JSON.stringify(waitResult, null, 2));
        
        if (waitResult.resultCode === 200) {
          console.log(`   ✅ 装配任务完成`);
          results.passed.push('/model/assemble 任务完成');
          
          // 验证父子关系
          const cameraInfo = await getModelInfo({ id: camera.modelId, useModeId: true });
          console.log(`\n   🔍 验证父子关系:`);
          console.log(`     - parentId: ${cameraInfo.data?.parentId || 'null'}`);
          console.log(`     - parentName: ${cameraInfo.data?.parentName || 'null'}`);
          
          if (cameraInfo.data?.parentId || cameraInfo.data?.parentName) {
            console.log(`   ✅ 父子关系建立成功`);
            results.passed.push('父子关系验证');
          } else {
            console.log(`   ⚠️ 未检测到父子关系`);
            results.warnings.push('父子关系未建立');
          }
        } else {
          console.log(`   ❌ 装配任务失败：${waitResult.resultMsg}`);
          results.failed.push(`装配任务：${waitResult.resultMsg}`);
        }
      }
    } else {
      console.log(`   ❌ /model/assemble 失败：${assembleResult.msg}`);
      results.failed.push(`/model/assemble: ${assembleResult.msg}`);
    }
    
  } catch (error) {
    console.log(`\n❌ 测试异常：${error.message}`);
    console.log(error.stack);
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

testAssemble().then(results => {
  process.exit(results.failed.length > 0 ? 1 : 0);
});
