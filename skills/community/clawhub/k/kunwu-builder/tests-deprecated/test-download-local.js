#!/usr/bin/env node

/**
 * 测试下载本地模型
 */

import { getLocalModelLibrary, downloadModel, waitForTask, getAllModelInfo } from './kunwu-tool.js';

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function testDownload() {
  console.log('📥 测试下载本地模型\n');
  
  // 获取本地模型库 - 直接调用 API 查看原始响应
  const { callAPI } = await import('./kunwu-tool.js');
  const localResult = await callAPI('/model/library/local', {});
  
  console.log('原始响应:', JSON.stringify(localResult, null, 2));
  
  const models = localResult.data?.models || [];
  
  console.log('\n本地模型:');
  models.forEach((m, i) => {
    console.log(`  ${i+1}. keys=${Object.keys(m).join(',')}`);
    console.log(`      name="${m.name}", id="${m.id}", modelId="${m.modelId}", modelName="${m.modelName}"`);
  });
  
  // 尝试下载 Camera Bracket
  console.log('\n📥 尝试下载 Camera Bracket...');
  try {
    const result = await downloadModel({
      id: 'Camera Bracket',  // 使用 modelName 作为 id
      rename: '测试_相机支架',
      position: [0, 0, 0],
      createInScene: true
    });
    
    console.log('下载响应:', JSON.stringify(result, null, 2));
    
    if (result.data?.taskId) {
      console.log('⏳ 等待任务完成...');
      const waitResult = await waitForTask(result.data.taskId);
      console.log('任务结果:', JSON.stringify(waitResult, null, 2));
      
      if (waitResult.resultCode === 200) {
        console.log('✅ 下载成功');
        
        // 验证
        await sleep(500);
        const allInfo = await getAllModelInfo();
        const testModel = allInfo.data?.models?.find(m => m.modelName === '测试_相机支架');
        if (testModel) {
          console.log(`✅ 模型已创建：${testModel.modelId}`);
        }
      }
    }
  } catch (error) {
    console.log('❌ 下载失败:', error.message);
  }
}

testDownload().catch(console.error);
