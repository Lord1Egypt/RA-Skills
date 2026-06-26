#!/usr/bin/env node
/**
 * 启动监控任务
 */

const { exec } = require('child_process');
const util = require('util');
const execAsync = util.promisify(exec);

async function main() {
  console.log('🚀 启动 X-Monitor 监控任务');
  console.log('');
  
  try {
    // 检查 cron 任务是否已存在
    const { stdout } = await execAsync('openclaw cron list');
    
    if (stdout.includes('x-monitor')) {
      console.log('⚠️ 监控任务已在运行');
      console.log('   查看状态: openclaw x-monitor status');
      return;
    }
    
    // 创建 cron 任务
    console.log('📝 创建定时任务...');
    
    await execAsync(`openclaw cron add --name "x-monitor-check" --schedule "0 * * * *" --command "openclaw x-monitor check"`);
    
    console.log('✅ 监控任务已启动');
    console.log('');
    console.log('📊 任务信息');
    console.log('   频率: 每小时检查一次');
    console.log('   查看状态: openclaw x-monitor status');
    console.log('   停止监控: openclaw x-monitor stop');
    
  } catch (err) {
    console.error('❌ 启动失败:', err.message);
    process.exit(1);
  }
}

main();
