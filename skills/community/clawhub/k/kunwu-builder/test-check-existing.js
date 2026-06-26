#!/usr/bin/env node

/**
 * 检查场景中是否有相机和相机支架
 */

import { getAllModelInfo, getModelInfo } from './kunwu-tool.js';

async function checkExisting() {
  console.log('🔍 检查场景中现有模型\n');
  
  const allInfo = await getAllModelInfo();
  const models = allInfo.data?.models || [];
  
  console.log(`场景中共有 ${models.length} 个模型:\n`);
  
  models.forEach((m, i) => {
    console.log(`${i+1}. ${m.modelName}`);
    console.log(`   ID: ${m.modelId}`);
    console.log(`   Type: ${m.type || 'N/A'}`);
    console.log();
  });
  
  // 查找相机和支架
  const camera = models.find(m => 
    m.modelName?.includes('Camera') || 
    m.modelName?.includes('Dufault') ||
    m.modelName?.includes('相机')
  );
  
  const bracket = models.find(m => 
    m.modelName?.includes('Bracket') ||
    m.modelName?.includes('支架')
  );
  
  console.log('\n📊 查找结果:');
  if (camera) {
    console.log(`✅ 找到相机：${camera.modelName} (${camera.modelId})`);
  } else {
    console.log(`❌ 未找到相机`);
  }
  
  if (bracket) {
    console.log(`✅ 找到支架：${bracket.modelName} (${bracket.modelId})`);
  } else {
    console.log(`❌ 未找到支架`);
  }
  
  // 如果有相机和支架，获取详细信息
  if (camera) {
    console.log('\n🔍 相机详细信息:');
    const cameraInfo = await getModelInfo({ id: camera.modelId, useModeId: true });
    console.log(JSON.stringify(cameraInfo, null, 2));
  }
  
  if (bracket) {
    console.log('\n🔍 支架详细信息:');
    const bracketInfo = await getModelInfo({ id: bracket.modelId, useModeId: true });
    console.log(JSON.stringify(bracketInfo, null, 2));
  }
}

checkExisting().catch(console.error);
