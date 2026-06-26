#!/usr/bin/env node
/**
 * 查看监控状态
 */

const { exec } = require('child_process');
const util = require('util');
const execAsync = util.promisify(exec);
const { loadConfig, loadState, getUsername } = require('./lib/utils');

async function main() {
  console.log('📊 X-Monitor 监控状态');
  console.log('');

  try {
    let cronStatus = '🔴 未运行';
    try {
      const { stdout } = await execAsync('openclaw cron list');
      if (stdout.includes('x-monitor')) {
        cronStatus = '🟢 运行中';
      }
    } catch {}

    console.log('定时任务:', cronStatus);
    console.log('');

    const config = await loadConfig();
    console.log('监控账号:', config.accounts?.length || 0);
    console.log('');

    if (config.accounts && config.accounts.length > 0) {
      console.log('账号详情:');
      console.log('');

      let totalTweets = 0;
      let totalNew = 0;

      for (const account of config.accounts) {
        const username = getUsername(account);
        const state = await loadState(username);

        const lastCheck = state?.lastCheck
          ? new Date(state.lastCheck).toLocaleString('zh-CN')
          : '从未检查';

        const tweetCount = state?.tweets?.length || 0;
        totalTweets += tweetCount;

        const newCount = state?.tweets?.filter(t => !t.notified)?.length || 0;
        totalNew += newCount;

        console.log(`  @${username}`);
        console.log(`    最后检查: ${lastCheck}`);
        console.log(`    已知推文: ${tweetCount}`);
        console.log(`    未读通知: ${newCount}`);
        console.log('');
      }

      console.log('统计:');
      console.log(`  总推文: ${totalTweets}`);
      console.log(`  未读通知: ${totalNew}`);
    }
  } catch (err) {
    console.error('❌ 读取失败:', err.message);
    console.error('   请先运行: openclaw x-monitor init');
    process.exit(1);
  }
}

main();
