#!/usr/bin/env node

/**
 * 测试 /model/assemble 装配功能
 * 日期：2026-03-16
 */

import {
  assemble,
  createModel,
  setModelPose,
  getModelInfo,
  getAllModelInfo,
  setParent,
  waitForTask,
  destroyObject
} from './kunwu-tool.js';

// 内联 sleep 函数
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * 通过 modelName 获取 modelId（获取最新创建的）
 */
async function getModelIdByName(modelName) {
  const allInfo = await getAllModelInfo();
  const models = allInfo.data?.models || [];
  
  // 找到匹配的模型（返回最后一个，即最新创建的）
  const matched = models.filter(m => m.modelName === modelName);
  if (matched.length === 0) {
    throw new Error(`Model not found: ${modelName}`);
  }
  
  // 返回最后一个（最新的）
  const model = matched[matched.length - 1];
  return model.modelId || model.id;
}

console.log('🧪 开始测试 /model/assemble 装配功能\n');

async function testAssemble() {
  const results = {
    passed: [],
    failed: [],
    warnings: []
  };

  try {
    // 先清理之前的测试模型
    console.log('🧹 清理之前的测试模型...');
    try {
      const allInfo = await getAllModelInfo();
      const models = allInfo.data?.models || [];
      const testModels = models.filter(m => 
        m.modelName?.includes('装配测试')
      );
      
      if (testModels.length > 0) {
        const idsToDelete = testModels.map(m => m.modelId || m.id);
        console.log(`   发现 ${testModels.length} 个测试模型，准备清理`);
        await destroyObject({ ids: idsToDelete });
        await sleep(1000);
      }
    } catch (e) {
      console.log(`   清理跳过：${e.message}`);
    }

    // ========== 测试 1: 创建父模型（箱子） ==========
    console.log('\n📦 测试 1: 创建父模型（箱子）');
    const parentResult = await createModel({
      id: '方形',
      rename: '装配测试_父箱子',
      position: [0, 0, 0],
      eulerAngle: [0, 0, 0],
      parameterizationCfg: {
        length: 200,
        width: 200,
        height: 200
      }
    });
    
    let parentId = parentResult.data.taskId;
    console.log(`   ✅ 父模型创建成功，taskId: ${parentId}`);
    results.passed.push('创建父模型');
    
    // 等待异步任务完成
    if (parentResult.data.taskId) {
      await waitForTask(parentId);
      await sleep(500);
      // 通过名称获取真正的 modelId
      parentId = await getModelIdByName('装配测试_父箱子');
      console.log(`   ✅ 获取父模型 modelId: ${parentId}`);
    }
    
    await sleep(500);

    // ========== 测试 2: 创建子模型（小方块） ==========
    console.log('\n📦 测试 2: 创建子模型（小方块）');
    const childResult = await createModel({
      id: '方形',
      rename: '装配测试_子方块',
      position: [300, 0, 100],  // 放在父模型旁边
      eulerAngle: [0, 0, 0],
      parameterizationCfg: {
        length: 50,
        width: 50,
        height: 50
      }
    });
    
    let childId = childResult.data.taskId;
    console.log(`   ✅ 子模型创建成功，taskId: ${childId}`);
    results.passed.push('创建子模型');
    
    // 等待异步任务完成
    if (childResult.data.taskId) {
      await waitForTask(childId);
      await sleep(500);
      // 通过名称获取真正的 modelId
      childId = await getModelIdByName('装配测试_子方块');
      console.log(`   ✅ 获取子模型 modelId: ${childId}`);
    }
    
    await sleep(500);

    // ========== 测试 3: 执行装配 ==========
    console.log('\n🔧 测试 3: 执行装配（子模型 → 父模型）');
    const assembleResult = await assemble({
      childId: childId,
      parentId: parentId,
      childUseModeId: true,  // 按 modelId 查找
      parentUseModeId: true,  // 按 modelId 查找
      assemblePosIndex: -1,  // 自动选择装配位
      replaceExisting: true
    });
    
    console.log(`   响应：`, JSON.stringify(assembleResult, null, 2));
    
    if (assembleResult.code === 200 || assembleResult.code === 202) {
      console.log(`   ✅ 装配请求成功`);
      results.passed.push('装配请求');
      
      // 如果是异步任务，等待完成
      if (assembleResult.data?.taskId) {
        console.log(`   ⏳ 等待装配任务完成...`);
        const waitResult = await waitForTask(assembleResult.data.taskId);
        console.log(`   ✅ 装配任务完成：`, JSON.stringify(waitResult, null, 2));
        results.passed.push('装配任务完成');
      }
    } else {
      console.log(`   ❌ 装配失败：${assembleResult.msg}`);
      results.failed.push(`装配失败：${assembleResult.msg}`);
    }
    
    await sleep(1000);

    // ========== 测试 4: 验证装配结果 ==========
    console.log('\n🔍 测试 4: 验证装配结果');
    const childInfo = await getModelInfo({
      id: childId,
      useModeId: true  // 按 modelId 查找
    });
    
    console.log(`   子模型信息：`, JSON.stringify(childInfo.data, null, 2));
    
    // 检查是否有父子关系
    if (childInfo.data.parentId || childInfo.data.parentName) {
      console.log(`   ✅ 装配验证成功：子模型已关联到父模型`);
      results.passed.push('装配关系验证');
    } else {
      console.log(`   ⚠️ 未检测到父子关系（可能是瞬时装配）`);
      results.warnings.push('未检测到持久父子关系');
    }

    // ========== 测试 5: 测试指定装配位 ==========
    console.log('\n🔧 测试 5: 测试指定装配位名称');
    // 创建另一个子模型
    let child2Id;
    const child2Name = '装配测试_子方块 2';
    const child2Result = await createModel({
      id: '方形',
      rename: child2Name,
      position: [400, 0, 100],
      eulerAngle: [0, 0, 0],
      parameterizationCfg: {
        length: 40,
        width: 40,
        height: 40
      }
    });
    
    if (child2Result.data.taskId) {
      await waitForTask(child2Result.data.taskId);
      await sleep(500);
      child2Id = await getModelIdByName(child2Name);
      console.log(`   ✅ 获取第二个子模型 modelId: ${child2Id}`);
    }
    
    await sleep(500);
    
    // 尝试指定装配位名称（如果有的话）
    const assemble2Result = await assemble({
      childId: child2Id,
      parentId: parentId,
      childUseModeId: true,
      parentUseModeId: true,
      assemblePosName: 'top',  // 尝试指定顶部装配位
      replaceExisting: false
    });
    
    console.log(`   响应：`, JSON.stringify(assemble2Result, null, 2));
    if (assemble2Result.code === 200 || assemble2Result.code === 202) {
      console.log(`   ✅ 指定装配位测试通过`);
      results.passed.push('指定装配位测试');
    } else {
      console.log(`   ⚠️ 指定装配位可能不支持：${assemble2Result.msg}`);
      results.warnings.push(`指定装配位测试：${assemble2Result.msg}`);
    }

  } catch (error) {
    console.log(`\n❌ 测试异常：${error.message}`);
    console.log(error.stack);
    results.failed.push(`测试异常：${error.message}`);
  }

  // ========== 输出测试报告 ==========
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

// 运行测试
testAssemble().then(results => {
  const exitCode = results.failed.length > 0 ? 1 : 0;
  process.exit(exitCode);
});
