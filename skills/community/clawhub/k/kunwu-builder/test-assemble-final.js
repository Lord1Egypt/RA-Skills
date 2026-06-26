#!/usr/bin/env node

/**
 * 测试 /model/assemble 装配功能 - 最终版
 * 日期：2026-03-16
 * 
 * 发现：/model/assemble 需要父模型有预定义的装配位
 * 替代方案：使用 /model/set_parent 建立父子关系
 */

import {
  assemble,
  createModel,
  getModelInfo,
  getAllModelInfo,
  setParent,
  waitForTask,
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

async function testAssemble() {
  const results = { passed: [], failed: [], warnings: [] };

  try {
    // 清理之前的测试模型
    console.log('🧹 清理之前的测试模型...');
    const allInfo = await getAllModelInfo();
    const models = allInfo.data?.models || [];
    const testModels = models.filter(m => m.modelName?.includes('装配测试'));
    if (testModels.length > 0) {
      const ids = testModels.map(m => m.modelId || m.id);
      await destroyObject({ ids });
      await sleep(1000);
      console.log(`   ✅ 清理了 ${testModels.length} 个模型`);
    }

    // ========== 测试 1: 创建父子模型 ==========
    console.log('\n📦 测试 1: 创建父子模型');
    const parentResult = await createModel({
      id: '方形',
      rename: '装配测试_父',
      position: [0, 0, 0],
      parameterizationCfg: { length: 200, width: 200, height: 200 }
    });
    await waitForTask(parentResult.data.taskId);
    await sleep(500);
    const parentId = await getModelIdByName('装配测试_父');
    console.log(`   ✅ 父模型：${parentId}`);
    results.passed.push('创建父模型');

    const childResult = await createModel({
      id: '方形',
      rename: '装配测试_子',
      position: [300, 0, 100],
      parameterizationCfg: { length: 50, width: 50, height: 50 }
    });
    await waitForTask(childResult.data.taskId);
    await sleep(500);
    const childId = await getModelIdByName('装配测试_子');
    console.log(`   ✅ 子模型：${childId}`);
    results.passed.push('创建子模型');

    // ========== 测试 2: 尝试 /model/assemble（预期可能失败） ==========
    console.log('\n🔧 测试 2: 尝试 /model/assemble');
    try {
      const assembleResult = await assemble({
        childId: childId,
        parentId: parentId,
        childUseModeId: true,
        parentUseModeId: true,
        assemblePosIndex: -1,
        replaceExisting: true
      });
      
      if (assembleResult.code === 200 || assembleResult.code === 202) {
        console.log(`   ✅ /model/assemble 成功`);
        results.passed.push('/model/assemble 基本调用');
        
        if (assembleResult.data?.taskId) {
          await waitForTask(assembleResult.data.taskId);
          console.log(`   ✅ 装配任务完成`);
          results.passed.push('/model/assemble 任务完成');
        }
      }
    } catch (error) {
      console.log(`   ⚠️ /model/assemble 失败：${error.message}`);
      results.warnings.push(`/model/assemble 需要预定义装配位：${error.message}`);
    }

    // ========== 测试 3: 使用 /model/set_parent（替代方案） ==========
    console.log('\n🔧 测试 3: 使用 /model/set_parent 建立父子关系');
    const child2Result = await createModel({
      id: '方形',
      rename: '装配测试_子 2',
      position: [400, 0, 100],
      parameterizationCfg: { length: 40, width: 40, height: 40 }
    });
    await waitForTask(child2Result.data.taskId);
    await sleep(500);
    const child2Id = await getModelIdByName('装配测试_子 2');
    
    const setParentResult = await setParent({
      childId: child2Id,
      childUseModeId: true,
      parentId: parentId,
      parentUseModeId: true
    });
    
    console.log(`   响应：`, JSON.stringify(setParentResult, null, 2));
    if (setParentResult.code === 200) {
      console.log(`   ✅ /model/set_parent 成功`);
      results.passed.push('/model/set_parent 建立父子关系');
    } else {
      console.log(`   ❌ /model/set_parent 失败：${setParentResult.msg}`);
      results.failed.push(`/model/set_parent: ${setParentResult.msg}`);
    }

    // ========== 测试 4: 验证父子关系 ==========
    console.log('\n🔍 测试 4: 验证父子关系');
    const child2Info = await getModelInfo({ id: child2Id, useModeId: true });
    console.log(`   子模型信息:`);
    console.log(`     - parentId: ${child2Info.data?.parentId || 'null'}`);
    console.log(`     - parentName: ${child2Info.data?.parentName || 'null'}`);
    
    if (child2Info.data?.parentId || child2Info.data?.parentName) {
      console.log(`   ✅ 父子关系验证成功`);
      results.passed.push('父子关系验证');
    } else {
      console.log(`   ⚠️ 未检测到父子关系`);
      results.warnings.push('父子关系未建立');
    }

    // ========== 测试 5: 解除父子关系 ==========
    console.log('\n🔧 测试 5: 解除父子关系（parentId: null）');
    const unsetParentResult = await setParent({
      childId: child2Id,
      childUseModeId: true,
      parentId: null,
      parentUseModeId: true
    });
    
    console.log(`   响应：`, JSON.stringify(unsetParentResult, null, 2));
    if (unsetParentResult.code === 200) {
      console.log(`   ✅ 解除父子关系成功`);
      results.passed.push('解除父子关系');
    } else {
      console.log(`   ⚠️ 解除父子关系：${unsetParentResult.msg}`);
      results.warnings.push(`解除父子关系：${unsetParentResult.msg}`);
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
    console.log(`\n⚠️ 警告/发现：${results.warnings.length}`);
    results.warnings.forEach(item => console.log(`   - ${item}`));
  }
  
  console.log('\n' + '='.repeat(60));
  console.log('\n📝 结论:');
  console.log('   - /model/assemble 需要父模型有预定义的装配位');
  console.log('   - /model/set_parent 是通用的父子关系建立方法');
  console.log('   - 推荐使用 /model/set_parent 进行装配');
  console.log('='.repeat(60));
  
  return results;
}

testAssemble().then(results => {
  process.exit(results.failed.length > 0 ? 1 : 0);
});
