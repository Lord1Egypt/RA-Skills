#!/usr/bin/env node

/**
 * 查看本地模型库内容
 */

import { getLocalModelLibrary, getModelInfo } from './kunwu-tool.js';

async function testLocalLibrary() {
  console.log('📦 本地模型库内容\n');
  
  const result = await getLocalModelLibrary({});
  const models = result.data?.models || [];
  
  console.log(`总数：${models.length}\n`);
  
  models.forEach((m, i) => {
    console.log(`${i+1}. ${m.name || m.modelName}`);
    console.log(`   ID: ${m.id || m.modelId}`);
    console.log(`   Type: ${m.type || 'N/A'}`);
    console.log(`   Category: ${m.category || 'N/A'}`);
    console.log();
  });
  
  // 查看场景中现有模型
  console.log('\n🔍 场景中现有模型:\n');
  const { getAllModelInfo } = await import('./kunwu-tool.js');
  const allInfo = await getAllModelInfo();
  const sceneModels = allInfo.data?.models || [];
  
  sceneModels.forEach((m, i) => {
    console.log(`${i+1}. ${m.modelName}`);
    console.log(`   ID: ${m.modelId}`);
    console.log(`   Type: ${m.type || 'N/A'}`);
    console.log();
  });
}

testLocalLibrary().catch(console.error);
