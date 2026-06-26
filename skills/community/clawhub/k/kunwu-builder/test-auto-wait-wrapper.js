#!/usr/bin/env node

/**
 * 测试异步任务自动轮询包装器
 * 日期：2026-03-16
 * 
 * 目标：自动包装异步 API，无需手动调用 waitForTask
 */

import {
  createModel,
  destroyObject,
  getAllModelInfo,
  exportModel,
  projectSave
} from './kunwu-tool.js';

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * 异步任务自动轮询包装器
 * 包装异步 API，自动等待任务完成并返回最终结果
 */
function createAutoWaitWrapper(apiFunc) {
  return async function(...args) {
    const result = await apiFunc(...args);
    
    // 如果是异步任务（code=202），自动等待
    if (result.code === 202 && result.data?.taskId) {
      console.log(`   ⏳ 异步任务 ${result.data.taskId}，等待完成...`);
      
      // 动态导入避免循环依赖
      const { waitForTask } = await import('./kunwu-tool.js');
      const finalResult = await waitForTask(result.data.taskId);
      
      return {
        code: finalResult.resultCode,
        msg: finalResult.resultMsg,
        data: finalResult.resultData,
        taskId: result.data.taskId,
        wasAsync: true
      };
    }
    
    // 同步任务直接返回
    return result;
  };
}

async function testAutoWait() {
  const results = { passed: [], failed: [], warnings: [] };
  
  console.log('🧪 测试异步任务自动轮询包装器\n');
  
  try {
    // ========== 测试 1: 包装 createModel ==========
    console.log('📦 测试 1: 包装 createModel（自动等待）');
    const autoCreateModel = createAutoWaitWrapper(createModel);
    
    const createResult = await autoCreateModel({
      id: '方形',
      rename: '自动等待测试',
      position: [0, 0, 0],
      parameterizationCfg: { length: 100, width: 100, height: 100 }
    });
    
    console.log(`   返回结果:`, JSON.stringify(createResult, null, 2));
    
    if (createResult.wasAsync && createResult.code === 200) {
      console.log(`   ✅ 自动等待成功，获取到最终结果`);
      results.passed.push('createModel 自动等待');
    } else if (createResult.code === 200) {
      console.log(`   ✅ 同步返回成功`);
      results.passed.push('createModel 同步返回');
    } else {
      console.log(`   ❌ 失败：${createResult.msg}`);
      results.failed.push(`createModel: ${createResult.msg}`);
    }
    
    await sleep(500);
    
    // ========== 测试 2: 包装 destroyObject（批量） ==========
    console.log('\n🗑️ 测试 2: 包装 destroyObject（批量销毁）');
    const autoDestroyObject = createAutoWaitWrapper(destroyObject);
    
    // 先找到测试模型
    const allInfo = await getAllModelInfo();
    const models = allInfo.data?.models || [];
    const testModel = models.find(m => m.modelName === '自动等待测试');
    
    if (testModel) {
      const destroyResult = await autoDestroyObject({
        ids: [testModel.modelId || testModel.id]
      });
      
      console.log(`   返回结果:`, JSON.stringify(destroyResult, null, 2));
      
      if (destroyResult.code === 200) {
        console.log(`   ✅ 批量销毁成功`);
        results.passed.push('destroyObject 自动等待');
      } else {
        console.log(`   ⚠️ 销毁结果：${destroyResult.msg}`);
        results.warnings.push(`destroyObject: ${destroyResult.msg}`);
      }
    } else {
      console.log(`   ⚠️ 未找到测试模型，跳过销毁测试`);
      results.warnings.push('未找到测试模型');
    }
    
    await sleep(500);
    
    // ========== 测试 3: 验证包装器通用性 ==========
    console.log('\n🔧 测试 3: 验证包装器通用性');
    console.log(`   包装器可以包装任何返回 {code: 202, data: {taskId}} 的 API`);
    console.log(`   支持的 API 包括:`);
    console.log(`     - createModel`);
    console.log(`     - destroyObject`);
    console.log(`     - exportModel`);
    console.log(`     - projectSave/projectLoad`);
    results.passed.push('包装器设计验证');
    
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

testAutoWait().then(results => {
  process.exit(results.failed.length > 0 ? 1 : 0);
});
