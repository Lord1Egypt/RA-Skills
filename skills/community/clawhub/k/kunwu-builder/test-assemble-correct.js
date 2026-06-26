#!/usr/bin/env node

/**
 * 正确的装配测试 - 使用 /model/assemble
 * 日期：2026-03-16
 * 
 * 装配规则：
 * 1. 相机 -> 相机支架
 * 2. 机器人相机 -> 机器人抓手上的支架 -> 机器人 -> 机器人底座/地轨
 * 3. 桁架相机 -> 桁架抓手 -> 桁架两个自由臂
 * 
 * 关键：使用 /model/assemble（内部自动处理父子关系）
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

async function testAssemble() {
  const results = { passed: [], failed: [], warnings: [] };
  
  console.log('🧪 正确的装配测试 - 使用 /model/assemble\n');
  
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
    
    // ========== 场景 1: 查询模型库中的相机和支架 ==========
    console.log('📦 场景 1: 从模型库下载相机和支架');
    
    // 查询模型库
    const { getLocalModelLibrary, getRemoteModelLibrary } = await import('./kunwu-tool.js');
    
    console.log('   🔍 查询本地模型库...');
    const localResult = await getLocalModelLibrary({});
    console.log(`   本地模型数量：${localResult.data?.models?.length || 0}`);
    
    console.log('\n   🔍 查询远程模型库（搜索：camera, 相机）...');
    const remoteResult = await getRemoteModelLibrary({ search: 'camera' });
    const cameraModels = remoteResult.data?.models || [];
    console.log(`   找到相机相关模型：${cameraModels.length} 个`);
    
    if (cameraModels.length > 0) {
      console.log('\n   前 5 个相机模型:');
      cameraModels.slice(0, 5).forEach((m, i) => {
        console.log(`     ${i+1}. ${m.name} (${m.id})`);
      });
    }
    
    // 搜索支架
    console.log('\n   🔍 查询远程模型库（搜索：mount, 支架）...');
    const mountResult = await getRemoteModelLibrary({ search: 'mount' });
    const mountModels = mountResult.data?.models || [];
    console.log(`   找到支架相关模型：${mountModels.length} 个`);
    
    if (mountModels.length > 0) {
      console.log('\n   前 5 个支架模型:');
      mountModels.slice(0, 5).forEach((m, i) => {
        console.log(`     ${i+1}. ${m.name} (${m.id})`);
      });
    }
    
    // 创建相机和支架（使用 checkFromCloud=true）
    if (cameraModels.length > 0 && mountModels.length > 0) {
      const cameraModel = cameraModels[0];
      const mountModel = mountModels[0];
      
      console.log(`\n   📦 创建相机：${cameraModel.name}`);
      await createModel({
        id: cameraModel.id,
        rename: '测试_相机',
        position: [0, 0, 100],
        checkFromCloud: true
      });
      await sleep(500);
      const cameraId = await getModelIdByName('测试_相机');
      console.log(`   ✅ 相机创建完成：${cameraId}`);
      results.passed.push('创建相机');
      
      console.log(`\n   📦 创建支架：${mountModel.name}`);
      await createModel({
        id: mountModel.id,
        rename: '测试_相机支架',
        position: [0, 0, 0],
        checkFromCloud: true
      });
      await sleep(500);
      const mountId = await getModelIdByName('测试_相机支架');
      console.log(`   ✅ 支架创建完成：${mountId}`);
      results.passed.push('创建支架');
      
      await sleep(1000);
      
      // ========== 执行装配：相机 -> 支架 ==========
      console.log('\n🔧 执行装配：相机 -> 支架（使用 /model/assemble）');
      
      allInfo = await getAllModelInfo();
      models = allInfo.data?.models || [];
      const camera = models.find(m => m.modelName === '测试_相机');
      const mount = models.find(m => m.modelName === '测试_相机支架');
      
      if (camera && mount) {
        console.log(`   相机：${camera.modelId}`);
        console.log(`   支架：${mount.modelId}`);
        
        const assembleResult = await assemble({
          childId: camera.modelId,
          parentId: mount.modelId,
          childUseModeId: true,
          parentUseModeId: true,
          assemblePosIndex: -1,
          replaceExisting: true
        });
        
        console.log(`\n   响应：`, JSON.stringify(assembleResult, null, 2));
        
        if (assembleResult.code === 200 || assembleResult.code === 202) {
          console.log(`   ✅ /model/assemble 请求成功`);
          results.passed.push('/model/assemble 基本调用');
          
          if (assembleResult.data?.taskId) {
            console.log(`   ⏳ 等待装配任务完成...`);
            const waitResult = await waitForTask(assembleResult.data.taskId);
            console.log(`   任务结果：`, JSON.stringify(waitResult, null, 2));
            
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
      } else {
        console.log(`   ⚠️ 未找到相机或支架`);
        results.warnings.push('未找到相机或支架');
      }
    } else {
      console.log(`   ⚠️ 模型库中没有找到合适的模型`);
      results.warnings.push('模型库查询失败');
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
