#!/usr/bin/env node

/**
 * 使用场景中现有模型测试 /model/assemble
 * 日期：2026-03-16
 */

import {
  assemble,
  createModel,
  getAllModelInfo,
  getModelInfo,
  destroyObject,
  waitForTask
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

async function testAssembleExisting() {
  const results = { passed: [], failed: [], warnings: [] };
  
  console.log('🧪 使用场景中现有模型测试 /model/assemble\n');
  
  try {
    // 清理测试模型
    console.log('🧹 清理测试模型...');
    let allInfo = await getAllModelInfo();
    let models = allInfo.data?.models || [];
    const testModels = models.filter(m => 
      m.modelName?.includes('测试_') || 
      m.modelName?.includes('装配_')
    );
    if (testModels.length > 0) {
      const ids = testModels.map(m => m.modelId || m.id);
      await destroyObject({ ids });
      await sleep(1500);
      console.log(`   ✅ 清理了 ${testModels.length} 个模型\n`);
    }
    
    // ========== 创建两个简单的模型 ==========
    console.log('📦 创建测试模型（使用参数化方形）...');
    
    const parentResult = await createModel({
      id: '方形',
      rename: '测试_支架',
      position: [0, 0, 0],
      parameterizationCfg: { length: 100, width: 100, height: 20 }
    });
    await waitForTask(parentResult.data.taskId);
    await sleep(500);
    const parentId = await getModelIdByName('测试_支架');
    console.log(`   ✅ 支架：${parentId}`);
    results.passed.push('创建支架');
    
    const childResult = await createModel({
      id: '方形',
      rename: '测试_相机',
      position: [0, 0, 50],
      parameterizationCfg: { length: 40, width: 40, height: 40 }
    });
    await waitForTask(childResult.data.taskId);
    await sleep(500);
    const childId = await getModelIdByName('测试_相机');
    console.log(`   ✅ 相机：${childId}`);
    results.passed.push('创建相机');
    
    await sleep(1000);
    
    // ========== 检查模型信息（是否有装配位） ==========
    console.log('\n🔍 检查模型信息...');
    const parentInfo = await getModelInfo({ id: parentId, useModeId: true });
    console.log(`   支架信息:`);
    console.log(`     - type: ${parentInfo.data?.type || 'N/A'}`);
    
    // ========== 执行装配：使用 /model/assemble ==========
    console.log('\n🔧 执行装配：相机 -> 支架（使用 /model/assemble）');
    
    const assembleResult = await assemble({
      childId: childId,
      parentId: parentId,
      childUseModeId: true,
      parentUseModeId: true,
      assemblePosIndex: -1,
      replaceExisting: true
    });
    
    console.log(`\n   响应:`, JSON.stringify(assembleResult, null, 2));
    
    if (assembleResult.code === 200) {
      console.log(`   ✅ /model/assemble 成功（同步）`);
      results.passed.push('/model/assemble 同步成功');
      
      // 验证父子关系
      const childInfo = await getModelInfo({ id: childId, useModeId: true });
      console.log(`\n   🔍 验证父子关系:`);
      console.log(`     - parentId: ${childInfo.data?.parentId || 'null'}`);
      console.log(`     - parentName: ${childInfo.data?.parentName || 'null'}`);
      
      if (childInfo.data?.parentId || childInfo.data?.parentName) {
        console.log(`   ✅ 父子关系建立成功`);
        results.passed.push('父子关系验证');
      } else {
        console.log(`   ⚠️ 未检测到父子关系`);
        results.warnings.push('父子关系未建立');
      }
      
    } else if (assembleResult.code === 202) {
      console.log(`   ⏳ 异步任务，等待完成...`);
      const waitResult = await waitForTask(assembleResult.data.taskId);
      console.log(`   任务结果:`, JSON.stringify(waitResult, null, 2));
      
      if (waitResult.resultCode === 200) {
        console.log(`   ✅ 装配任务完成`);
        results.passed.push('/model/assemble 异步完成');
        
        // 验证父子关系
        const childInfo = await getModelInfo({ id: childId, useModeId: true });
        console.log(`\n   🔍 验证父子关系:`);
        console.log(`     - parentId: ${childInfo.data?.parentId || 'null'}`);
        console.log(`     - parentName: ${childInfo.data?.parentName || 'null'}`);
        
        if (childInfo.data?.parentId || childInfo.data?.parentName) {
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
      
    } else {
      console.log(`   ❌ /model/assemble 失败：${assembleResult.msg}`);
      results.failed.push(`/model/assemble: ${assembleResult.msg}`);
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

testAssembleExisting().then(results => {
  process.exit(results.failed.length > 0 ? 1 : 0);
});
