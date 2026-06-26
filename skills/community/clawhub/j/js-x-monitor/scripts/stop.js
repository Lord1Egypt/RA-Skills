#!/usr/bin/env node
/**
 * 停止监控任务
 */

const { exec } = require('child_process');
const util = require('util');
const execAsync = util.promisify(exec);

async function main() {
  console.log('🛑 停止 X-Monitor 监控任务');
  console.log('');
  
  try {
    // 查找并删除 cron 任务
    const { stdout } = await execAsync('openclaw cron list --json');
    const jobs = JSON.parse(stdout);
    
    const monitorJobs = jobs.filter(j => j.name.includes('x-monitor'));
    
    if (monitorJobs.length === 0) {
      console.log('⚠️ 没有运行中的监控任务');
      return;
    }
    
    for (const job of monitorJobs) {
      await execAsync(`openclaw cron remove --id ${job.id}`);
      console.log(`✅ 已停止: ${job.name}`);
    }
    
    console.log('');
    console.log('✅ 所有监控任务已停止');
    
  } catch (err) {
    console.error('❌ 停止失败:', err.message);
    process.exit(1);
  }
}

main();
