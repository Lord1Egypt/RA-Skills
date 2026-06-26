#!/usr/bin/env node
/**
 * 列出监控账号
 */

const { loadConfig, loadState, getUsername } = require('./lib/utils');

async function main() {
  try {
    const config = await loadConfig();

    if (!config.accounts || config.accounts.length === 0) {
      console.log('📭 监控列表为空');
      console.log('   添加账号: openclaw x-monitor add <username>');
      return;
    }

    console.log('📋 监控账号列表');
    console.log('');
    console.log('| # | 账号 | 状态 | 最后检查 | 已知推文 |');
    console.log('|---|------|------|----------|----------|');

    for (let i = 0; i < config.accounts.length; i++) {
      const account = config.accounts[i];
      const username = getUsername(account);
      const enabled = typeof account === 'string' ? true : account.enabled !== false;

      const state = await loadState(username);
      const lastCheck = state?.lastCheck
        ? new Date(state.lastCheck).toLocaleString('zh-CN', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
        : '从未';
      const tweetCount = state?.tweets?.length || 0;

      const status = enabled ? '🟢' : '🔴';

      console.log(`| ${i + 1} | @${username} | ${status} | ${lastCheck} | ${tweetCount} |`);
    }

    console.log('');
    console.log(`总计: ${config.accounts.length} 个账号`);
  } catch (err) {
    console.error('❌ 读取失败:', err.message);
    console.error('   请先运行: openclaw x-monitor init');
    process.exit(1);
  }
}

main();
