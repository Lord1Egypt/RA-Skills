#!/usr/bin/env node

/**
 * 查询任务详细结果
 */

import { callAPI, createModel } from './kunwu-tool.js';

async function testQuery() {
  console.log('🔍 查询任务详细结果\n');
  
  // 创建模型（使用 checkFromCloud=true）
  console.log('📦 创建 Camera Bracket...');
  const result = await createModel({
    id: 'Camera Bracket',
    rename: '测试_支架',
    position: [0, 0, 0],
    checkFromCloud: true
  });
  
  console.log('创建响应:', JSON.stringify(result, null, 2));
  console.log('\n✅ 模型创建完成');
}

testQuery().catch(console.error);
