#!/usr/bin/env node

/**
 * 从本地模型库加载相机和相机支架，完成装配
 * 日期：2026-03-16
 * 
 * 使用本地模型库中的真实模型：
 * - Camera Bracket（相机支架）
 * - Dufault 2D（2D 相机）
 */

import {
  assemble,
  getAllModelInfo,
  getModelInfo,
  destroyObject,
  waitForTask,
  getLocalModelLibrary
} from './kunwu-tool.js';

// 直接调用 API 下载
import http from 'http';

const BASE_URL = 'http://100.85.119.45:16888';

function callAPI(endpoint, data) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify(data);
    const options = {
      hostname: new URL(BASE_URL).hostname,
      port: new URL(BASE_URL).port,
      path: endpoint,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body),
      },
    };

    const req = http.request(options, (res) => {
      let responseData = '';
      res.on('data', (chunk) => {
        responseData += chunk;
      });
      res.on('end', () => {
        try {
          resolve(JSON.parse(responseData));
        } catch (e) {
          reject(new Error(`Parse error: ${e.message}`));
        }
      });
    });

    req.on('error', (e) => {
      reject(new Error(`Connection error: ${e.message}`));
    });

    req.write(body);
    req.end();
  });
}

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

async function createModelFromCloud(modelName, rename, position) {
  // 使用 /model/create + checkFromCloud:true（统一推荐方式）
  const result = await callAPI('/model/create', {
    id: modelName,
    rename: rename,
    position: position || [0, 0, 0],
    checkFromCloud: true
  });
  
  await sleep(500);
  return await getModelIdByName(rename);
}

async function testCameraBracketAssemble() {
  const results = { passed: [], failed: [], warnings: [] };
  
  console.log('🧪 从本地模型库加载相机和相机支架，完成装配\n');
  
  try {
    // ========== 1. 查看本地模型库 ==========
    console.log('📦 本地模型库内容:');
    const localResult = await getLocalModelLibrary({});
    const localModels = localResult.data?.models || [];
    localModels.forEach((m, i) => {
      console.log(`   ${i+1}. ${m.modelName}`);
    });
    console.log();
    
    // ========== 2. 清理之前的测试模型 ==========
    console.log('🧹 清理之前的测试模型...');
    let allInfo = await getAllModelInfo();
    let models = allInfo.data?.models || [];
    const testModels = models.filter(m => 
      m.modelName?.includes('测试_') || 
      m.modelName?.includes('Camera') ||
      m.modelName?.includes('Bracket') ||
      m.modelName?.includes('Dufault')
    );
    if (testModels.length > 0) {
      console.log(`   发现 ${testModels.length} 个模型，准备清理`);
      const ids = testModels.map(m => m.modelId || m.id);
      await destroyObject({ ids });
      await sleep(2000);
      console.log(`   ✅ 清理完成\n`);
    }
    
    // ========== 3. 创建相机支架 ==========
    console.log('📦 创建 Camera Bracket（相机支架）...');
    const bracketId = await createModelFromCloud(
      'Camera Bracket',
      '测试_相机支架',
      [0, 0, 0]
    );
    console.log(`   ✅ 相机支架创建完成：${bracketId}`);
    results.passed.push('创建相机支架');
    
    // ========== 4. 创建 2D 相机 ==========
    console.log('\n📦 创建 Dufault 2D（2D 相机）...');
    const cameraId = await createModelFromCloud(
      'Dufault 2D',
      '测试_2D 相机',
      [0, 0, 100]
    );
    console.log(`   ✅ 2D 相机创建完成：${cameraId}`);
    results.passed.push('下载 2D 相机');
    
    await sleep(1000);
    
    // ========== 5. 获取模型信息 ==========
    console.log('\n🔍 获取模型信息...');
    allInfo = await getAllModelInfo();
    models = allInfo.data?.models || [];
    
    const bracket = models.find(m => m.modelName === '测试_相机支架');
    const camera = models.find(m => m.modelName === '测试_2D 相机');
    
    if (bracket && camera) {
      console.log(`   相机支架：${bracket.modelId}`);
      console.log(`   2D 相机：${camera.modelId}`);
      
      // 查看详细信息
      const bracketInfo = await getModelInfo({ id: bracket.modelId, useModeId: true });
      console.log(`\n   相机支架信息:`);
      console.log(`     - modelName: ${bracketInfo.data?.modelName}`);
      console.log(`     - type: ${bracketInfo.data?.type || 'N/A'}`);
      
    } else {
      console.log(`   ❌ 未找到模型`);
      results.failed.push('未找到下载的模型');
      return results;
    }
    
    // ========== 6. 执行装配：相机 -> 支架 ==========
    console.log('\n🔧 执行装配：2D 相机 -> 相机支架（使用 /model/assemble）');
    console.log(`   childId: ${camera.modelId}`);
    console.log(`   parentId: ${bracket.modelId}`);
    
    const assembleResult = await assemble({
      childId: camera.modelId,
      parentId: bracket.modelId,
      childUseModeId: true,
      parentUseModeId: true,
      assemblePosIndex: -1,  // 自动选择装配位
      replaceExisting: true
    });
    
    console.log(`\n   响应:`, JSON.stringify(assembleResult, null, 2));
    
    if (assembleResult.code === 200) {
      console.log(`   ✅ /model/assemble 成功（同步）`);
      results.passed.push('/model/assemble 同步成功');
      
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
      
    } else if (assembleResult.code === 202) {
      console.log(`   ⏳ 异步任务，等待完成...`);
      const waitResult = await waitForTask(assembleResult.data.taskId);
      console.log(`   任务结果:`, JSON.stringify(waitResult, null, 2));
      
      if (waitResult.resultCode === 200) {
        console.log(`   ✅ 装配任务完成`);
        results.passed.push('/model/assemble 异步完成');
        
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

testCameraBracketAssemble().then(results => {
  process.exit(results.failed.length > 0 ? 1 : 0);
});
