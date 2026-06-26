#!/usr/bin/env node

/**
 * 调试任务查询返回格式
 */

import { createModel, taskQuery, waitForTask } from './kunwu-tool.js';

async function debugTask() {
  console.log('🔍 调试任务查询返回格式\n');
  
  // 创建模型
  const result = await createModel({
    id: '方形',
    rename: '调试测试',
    position: [0, 0, 0],
    parameterizationCfg: {
      length: 100,
      width: 100,
      height: 100
    }
  });
  
  console.log('1. createModel 原始返回:');
  console.log(JSON.stringify(result, null, 2));
  
  if (result.data?.taskId) {
    const taskId = result.data.taskId;
    console.log(`\n2. 查询任务状态 (taskId: ${taskId}):`);
    
    const status = await taskQuery({ taskId });
    console.log(JSON.stringify(status, null, 2));
    
    console.log('\n3. 等待任务完成:');
    const waitResult = await waitForTask(taskId);
    console.log(JSON.stringify(waitResult, null, 2));
    
    console.log('\n4. resultData 字段:');
    console.log(JSON.stringify(waitResult.resultData, null, 2));
  }
}

debugTask().catch(console.error);
